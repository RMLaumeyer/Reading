"""Public Single Issues tab adapter for Comic Book Reading Orders."""
from html.parser import HTMLParser
import re
import urllib.request
from urllib.parse import urlsplit
import issue_designators


def check_url(url):
    p = urlsplit(url)
    if (p.scheme != 'https' or p.hostname != 'comicbookreadingorders.com'
            or p.username or p.password or p.port not in (None, 443) or p.query or p.fragment
            or not re.fullmatch(r'/marvel/events/[a-z0-9-]+-reading-order/', p.path)):
        raise ValueError('Expected public event reading-order URL')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        if urlsplit(req.full_url).path != urlsplit(newurl).path:
            raise ValueError('Redirect changed event')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    check_url(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1'})
    with urllib.request.build_opener(Redirects).open(req, timeout=25) as r:
        check_url(r.url)
        if r.headers.get_content_type() != 'text/html': raise ValueError('Expected HTML')
        body = r.read(3_000_001)
        if len(body) > 3_000_000: raise ValueError('Guide exceeds limit')
        return body, r.url, r.headers.get_content_charset() or 'utf-8'


class Page(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.buttons, self.panels, self.titles = [], {}, []
        self.button = self.title = self.panel = None
        self.depth = self.skip = 0
        self.paragraph = None
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style', 'nav'): self.skip += 1
        if self.skip: return
        if tag == 'h1': self.title = []
        if tag == 'button' and attrs.get('role') == 'tab':
            self.button = {'target': attrs.get('aria-controls'), 'text': ''}
        if tag == 'div':
            if self.panel is not None: self.depth += 1
            elif attrs.get('role') == 'tabpanel':
                self.panel, self.depth = attrs.get('id'), 1
                if not self.panel or self.panel in self.panels: raise ValueError('Ambiguous panel identity')
                self.panels[self.panel] = []
        if self.panel is not None:
            if tag == 'p': self.paragraph = ['']
            if tag == 'br' and self.paragraph is not None: self.paragraph.append('')

    def handle_data(self, text):
        if self.skip: return
        if self.title is not None: self.title.append(text)
        if self.button is not None: self.button['text'] += text
        if self.panel is not None and self.paragraph is not None: self.paragraph[-1] += text

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav'):
            self.skip = max(0, self.skip-1)
            return
        if self.skip: return
        if tag == 'h1' and self.title is not None:
            self.titles.append(' '.join(''.join(self.title).split())); self.title = None
        if tag == 'button' and self.button is not None:
            self.buttons.append(self.button); self.button = None
        if tag == 'p' and self.panel is not None and self.paragraph is not None:
            self.panels[self.panel].append([' '.join(s.split()) for s in self.paragraph if s.strip()])
            self.paragraph = None
        if tag == 'div' and self.panel is not None:
            self.depth -= 1
            if not self.depth: self.panel = None


def parse(raw, url):
    check_url(url)
    page = Page(raw)
    tabs = [b for b in page.buttons if b['text'].strip() == 'Single Issues']
    if len(tabs) != 1 or len(page.titles) != 1 or tabs[0]['target'] not in page.panels:
        raise ValueError('Missing unique event title or Single Issues panel')
    expected = urlsplit(url).path.rstrip('/').split('/')[-1].removesuffix('-reading-order')
    title_key = lambda text: re.sub(r'[^a-z0-9]', '', text.casefold())
    if title_key(page.titles[0]) != title_key(expected):
        raise ValueError('Page event title does not match requested event')
    nodes, problems, seen, sequence = [], [], set(), []
    paragraphs = page.panels[tabs[0]['target']]
    parsed_paragraphs = [[re.fullmatch(r'(.+?)\s+#(\d+)(?:\s+\((\d{4})\))?', line)
                          for line in paragraph] for paragraph in paragraphs]
    years, year_quotes = {}, {}
    for paragraph, parsed in zip(paragraphs, parsed_paragraphs):
        for line, m in zip(paragraph, parsed):
            if m and m[3]:
                years.setdefault(m[1].casefold(), set()).add(int(m[3]))
                year_quotes.setdefault(m[1].casefold(), []).append(line)
    for paragraph, parsed in zip(paragraphs, parsed_paragraphs):
        for line, m in zip(paragraph, parsed):
            candidates = years.get(m[1].casefold(), set()) if m else set()
            slot = {'position': len(sequence)+1, 'quote': line, 'sourceUrl': url,
                    'issue': {'series': m[1], 'year': None, 'number': int(m[2])} if m else None,
                    'identityState': 'unresolved' if m and not candidates else 'unsupported'}
            sequence.append(slot)
            if not m:
                designation = issue_designators.decimal_issue(line)
                if designation:
                    slot['unsupportedIssueDesignation'] = designation
            if not m or len(candidates) != 1 or not 1900 <= next(iter(candidates)) <= 2100:
                problems.append({'quote': line, 'reason': 'Unsupported issue or missing/conflicting year for exact series within selected tab'})
                continue
            year = next(iter(candidates))
            key = m[1].casefold(), year, int(m[2])
            if key in seen:
                problems.append({'quote': line, 'reason': 'Duplicate issue'}); continue
            seen.add(key)
            nodes.append({'position': slot['position'], 'issue': {'series': m[1], 'year': year, 'number': int(m[2])},
                          'quote': line, 'sourceUrl': url, 'identityRequiresReview': not bool(m[3]),
                          'identityEvidence': {'datedQuotes': year_quotes[m[1].casefold()],
                                               'method': 'Unique exact-series year within selected source tab'}})
            slot.update(nodes[-1], identityState='resolved')
    if not sequence or len(sequence) > 500: raise ValueError('Empty or unbounded sequence')
    return {'sourceUrl': url, 'title': page.titles[0], 'sourceKind': 'independent_editorial',
            'selectedSections': ['Single Issues'], 'orderedIssues': nodes, 'sourceSequence': sequence, 'problems': problems,
            'state': 'needs_review' if problems else 'draft', 'scope': 'Entire public Single Issues tab',
            'complete': False, 'requiredReadingEstablished': False, 'chronologyEstablished': False}
