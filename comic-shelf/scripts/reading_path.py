"""Collect explicit issue cards from public Marvel reading lists; never publish."""
from html.parser import HTMLParser
import re
import urllib.request
from urllib.parse import urljoin, urlsplit

from issue_fetch import Headings


def check_list_url(url):
    p = urlsplit(url)
    if (p.scheme != 'https' or p.hostname != 'share.marvel.com' or p.username or p.password
            or p.port not in (None, 443) or not re.fullmatch(r'/comics/discover/\d+/[a-z0-9-]+/?', p.path)
            or p.query or p.fragment):
        raise ValueError('Use a public Marvel reading-list URL')
    return url


class ListRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_list_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_list(url):
    check_list_url(url)
    request = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1 (personal metadata research)'})
    with urllib.request.build_opener(ListRedirects).open(request, timeout=25) as response:
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected reading-list HTML')
        body = response.read(3_000_001)
        if len(body) > 3_000_000:
            raise ValueError('Reading list exceeds limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


class IssueCards(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.cards, self.current, self.in_title = [], None, False
        self.skip = 0
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if self.skip:
            return
        classes = attrs.get('class', '').split()
        if tag == 'a' and 'ComicCard__Url' in classes:
            self.current = {'href': attrs.get('href'), 'text': ''}
        if self.current is not None and tag == 'p' and 'ComicCard__Info--title' in classes:
            self.in_title = True

    def handle_data(self, text):
        if self.in_title and not self.skip:
            self.current['text'] += text

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == 'p':
            self.in_title = False
        if tag == 'a' and self.current is not None:
            self.current['text'] = ' '.join(self.current['text'].split())
            self.cards.append(self.current)
            self.current, self.in_title = None, False


def parse_list(raw, url):
    check_list_url(url)
    headings = Headings(raw).headings
    page_title = next((h for h in headings if h.endswith('| Reading Lists | Marvel Comics')), None)
    if not page_title:
        raise ValueError('Response is not an identified Marvel reading-list page')
    cards = IssueCards(raw).cards
    if not cards or len(cards) > 500:
        raise ValueError('No bounded issue-card list found')
    nodes, problems, seen, seen_ids = [], [], set(), set()
    for position, card in enumerate(cards, 1):
        match = re.fullmatch(r'(.+?)\s+\((\d{4})\)\s+#(\d+)', card['text'])
        link = urljoin(url, card['href'] or '')
        parsed = urlsplit(link)
        id_match = re.match(r'^/comics/issue/(\d+)(?:/|$)', parsed.path)
        if (not match or not 1900 <= int(match[2]) <= 2100 or not id_match
                or parsed.scheme != 'https' or parsed.hostname not in ('share.marvel.com', 'www.marvel.com')
                or parsed.username or parsed.password or parsed.port not in (None, 443)):
            problems.append({'position': position, 'card': card, 'reason': 'Unsupported or ambiguous issue card'})
            continue
        issue = {'series': match[1], 'year': int(match[2]), 'number': int(match[3])}
        identity = (issue['series'].casefold(), issue['year'], issue['number'])
        if identity in seen or id_match[1] in seen_ids:
            problems.append({'position': position, 'card': card, 'reason': 'Duplicate issue identity or source issue ID'})
            continue
        seen.add(identity)
        seen_ids.add(id_match[1])
        nodes.append({'position': position, 'issue': issue, 'issueUrl': link,
                      'sourceIssueId': id_match[1], 'quote': card['text']})
    return {'sourceUrl': url, 'title': page_title.split('|')[0].strip(),
        'state': 'needs_review' if problems else 'draft', 'orderedIssues': nodes,
        'cardCount': len(cards), 'problems': problems,
        'scope': 'Publisher-listed sequence of visible issue cards',
        'complete': False, 'requiredReadingEstablished': False, 'chronologyEstablished': False}


def map_edition(path, contents):
    placements, outside, mismatches = [], [], []
    for node in path['orderedIssues']:
        issue = node['issue']
        matches = [e for e in contents['entries'] if e['series'].casefold() == issue['series'].casefold()
                   and e['year'] == issue['year'] and e['first'] <= issue['number'] <= e['last']]
        if matches:
            placements.append({**node, 'extent': 'partial' if any(e['extent'] == 'partial' for e in matches) else 'whole',
                               'portions': [e['portion'] for e in matches if e['portion']]})
        else:
            outside.append(node)
            candidates = [e for e in contents['entries']
                          if e['series'].casefold() == issue['series'].casefold()
                          and e['first'] <= issue['number'] <= e['last'] and e['year'] != issue['year']]
            if candidates:
                mismatches.append({'issue': issue, 'position': node['position'],
                                   'quote': node['quote'],
                                   'inventoryYears': sorted({e['year'] for e in candidates}, key=str),
                                   'reason': 'Same series label and number, different year; could be a different run. No automatic identity substitution.'})
    return {'state': path['state'], 'sourceUrl': path['sourceUrl'], 'title': path['title'],
            'placements': placements, 'outsideEdition': outside,
            'identityMismatches': mismatches,
            'complete': False, 'externalIssuesAreRequired': None,
            'note': 'Positions reflect this publisher list. Outside-edition nodes are not automatically required prerequisites; partial issues remain partial.'}
