"""Bounded publisher-feature descriptions, distinct from story titles and order."""
from html.parser import HTMLParser
import re
from urllib.parse import urljoin, urlsplit

from issue_fetch import Headings
from reading_path import check_list_url


class Features(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.rows, self.current = [], None
        self.depth, self.skip = 0, 0
        self.capture = None
        self.capture_depth = 0
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if self.skip:
            return
        classes = attrs.get('class', '').split()
        if tag == 'div':
            if self.current is not None:
                self.depth += 1
            elif 'DiscoverList__Item' in classes:
                self.current = {'title': '', 'description': '', 'links': []}
                self.depth = 1
        if self.current is None:
            return
        if self.capture and tag == self.capture[1]:
            self.capture_depth += 1
        if tag == 'a' and 'DiscoverList__Item-Url' in classes:
            self.current['links'].append(attrs.get('href', ''))
        if tag == 'h3' and 'DiscoverList__Item-Title' in classes:
            self.capture = ('title', tag)
            self.capture_depth = 1
        if tag == 'span' and 'DiscoverList__Item-Description' in classes:
            self.capture = ('description', tag)
            self.capture_depth = 1
        if tag in ('br', 'p') and self.capture:
            self.current[self.capture[0]] += ' '

    def handle_data(self, text):
        if self.current is not None and self.capture and not self.skip:
            self.current[self.capture[0]] += text

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or self.current is None:
            return
        if self.capture and tag == self.capture[1]:
            self.capture_depth -= 1
            if self.capture_depth == 0:
                self.capture = None
        if tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                for key in ('title', 'description'):
                    self.current[key] = ' '.join(self.current[key].split())
                self.rows.append(self.current)
                self.current, self.capture = None, None


def parse_features(raw, url):
    check_list_url(url)
    title = next((h for h in Headings(raw).headings if h.endswith('| Reading Lists | Marvel Comics')), None)
    parser = Features(raw)
    if not title or not parser.rows or len(parser.rows) > 100 or parser.current is not None:
        raise ValueError('No complete bounded publisher-feature list')
    items, problems, seen, ids = [], [], set(), set()
    for position, row in enumerate(parser.rows, 1):
        match = re.fullmatch(r'(.+?)\s+\((\d{4})\)\s+#(\d+)', row['title'])
        links = set(row['links'])
        link = urljoin(url, next(iter(links))) if len(links) == 1 else ''
        parsed = urlsplit(link)
        issue_id = re.fullmatch(r'/comics/issue/(\d+)(?:/[a-zA-Z0-9_/-]*)?', parsed.path)
        if (not match or not 1900 <= int(match[2]) <= 2100 or not issue_id
                or parsed.scheme != 'https' or parsed.hostname not in ('share.marvel.com', 'www.marvel.com')
                or parsed.username or parsed.password or parsed.port not in (None, 443)
                or parsed.query or parsed.fragment or not 1 <= len(row['description']) <= 4000):
            problems.append({'position': position, 'row': row, 'reason': 'Unsupported feature identity, description or link'})
            continue
        issue = {'series': match[1], 'year': int(match[2]), 'number': int(match[3])}
        key = (issue['series'].casefold(), issue['year'], issue['number'])
        if key in seen or issue_id[1] in ids:
            problems.append({'position': position, 'row': row, 'reason': 'Duplicate feature identity or source ID'})
            continue
        seen.add(key)
        ids.add(issue_id[1])
        items.append({'issue': issue, 'issueUrl': link, 'identityQuote': row['title'],
                      'descriptionQuote': row['description'], 'sourcePosition': position})
    return {'sourceUrl': url, 'title': title.split('|')[0].strip(), 'features': items,
            'problems': problems, 'state': 'needs_review' if problems else 'draft',
            'complete': False, 'readingOrderEstablished': False}


def edition_evidence(pages, contents):
    """Whole, explicitly dated edition matches only; never infer backup-story scope."""
    evidence, sources, seen = [], [], set()
    for page in pages:
        if page['state'] != 'draft':
            continue
        for feature in page['features']:
            issue = feature['issue']
            matches = [e for e in contents['entries'] if e['series'].casefold() == issue['series'].casefold()
                       and e['year'] == issue['year'] and e['first'] <= issue['number'] <= e['last']
                       and e['extent'] == 'whole' and not e.get('identityResolution')]
            key = (page['sourceUrl'], issue['series'].casefold(), issue['year'], issue['number'])
            if not matches or key in seen:
                continue
            seen.add(key)
            item = {**feature, 'sourceUrl': page['sourceUrl'], 'sourceTitle': page['title'],
                    'sourceSha256': page.get('sha256'), 'state': 'draft',
                    'scope': 'Publisher description attached to this issue; may discuss a wider arc',
                    'officialStoryTitle': None, 'completeStoryScopeEstablished': False}
            evidence.append(item)
            # Arc extraction remains independently checked against literal source
            # text. Descriptions are not silently relabelled as story-title headings.
            excerpt = feature['descriptionQuote'][:450]
            if len(feature['descriptionQuote']) > 450:
                excerpt = excerpt.rsplit(' ', 1)[0]
            if re.search(r'\bPART\s+(?:\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\b', excerpt, re.I):
                sources.append({'id': f'F{len(sources)+1}', 'kind': 'publisher_issue_description',
                                'issue': issue, 'text': excerpt, 'url': page['sourceUrl'],
                                'identityMode': 'explicit_year', 'provenance': 'downloaded_html',
                                'identityQuote': feature['identityQuote'], 'sourceSha256': page.get('sha256')})
    return evidence, sources
