"""Publisher-catalog series identities, kept separate from edition membership."""
from copy import deepcopy
from html.parser import HTMLParser
import hashlib
import json
import re
import urllib.request
from urllib.parse import urlsplit, parse_qs


def check_url(url):
    p = urlsplit(url)
    q = parse_qs(p.query)
    if (p.scheme != 'https' or p.hostname not in ('prhcomics.com', 'penguinrandomhouselibrary.com')
            or p.username or p.password or p.port not in (None, 443) or p.fragment
            or p.path != '/book/' or set(q) != {'isbn'} or len(q['isbn']) != 1
            or not re.fullmatch(r'\d{13}', q['isbn'][0])):
        raise ValueError('Use a public PRH book URL with one ISBN')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        if parse_qs(urlsplit(req.full_url).query) != parse_qs(urlsplit(newurl).query):
            raise ValueError('Publisher redirect changed ISBN')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    check_url(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1 (personal metadata research)'})
    with urllib.request.build_opener(Redirects).open(req, timeout=25) as response:
        check_url(response.url)
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected publisher HTML')
        body = response.read(3_000_001)
        if len(body) > 3_000_000:
            raise ValueError('Publisher page exceeds limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


class Blocks(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.parts, self.lines, self.skip = [], [], 0
        self.feed(raw)
        self.flush()

    def flush(self):
        text = ' '.join(''.join(self.parts).split())
        if text:
            self.lines.append(text)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if not self.skip and tag in ('div', 'p', 'br', 'li', 'h1', 'h2'):
            self.flush()

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip-1)
        if not self.skip and tag in ('div', 'p', 'li', 'h1', 'h2'):
            self.flush()

    def handle_data(self, text):
        if not self.skip:
            self.parts.append(text)


def name_key(name):
    # Punctuation variants only; never remove an event/series prefix.
    return re.sub(r'[^a-z0-9]', '', name.casefold())


def rows_from_lines(lines):
    rows = []
    for line in lines:
        if not isinstance(line, str) or len(line) > 3000:
            continue
        match = re.fullmatch(r'COLLECT(?:ING|S)\s*:\s*(.+)', line, re.I)
        if not match:
            continue
        for clause in re.split(r'\s*[,;]\s*', match[1].rstrip('.')):
            m = re.fullmatch(r'(.+?)\s+\((\d{4})\)(?:\s+#?(\d+)(?:[-–](\d+))?)?', clause)
            if not m or not 1900 <= int(m[2]) <= 2100:
                continue
            first, last = (int(m[3]), int(m[4] or m[3])) if m[3] else (None, None)
            if first is not None and not 0 <= last-first <= 150:
                continue
            rows.append({'series': m[1], 'year': int(m[2]), 'first': first, 'last': last, 'quote': clause})
    return rows


def parse(raw, url):
    check_url(url)
    lines = list(dict.fromkeys(line for line in Blocks(raw).lines
                               if re.match(r'^COLLECT(?:ING|S)\s*:', line, re.I)))
    if not lines or len(lines) > 10 or not rows_from_lines(lines):
        raise ValueError('No bounded explicit dated publisher contents found')
    return {'url': url, 'sourceIsbn': parse_qs(urlsplit(url).query)['isbn'][0],
            'kind': 'Publisher catalog series identity reference', 'collectingLines': lines,
            'sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
            'scope': 'Series identities only; this other edition does not establish target edition membership.'}


def acquire(url, folder, fetch=download):
    check_url(url)
    folder.mkdir(exist_ok=False)
    audit = {'url': url, 'state': 'attempted'}
    try:
        body, final, encoding = fetch(url)
        check_url(final)
        if parse_qs(urlsplit(url).query) != parse_qs(urlsplit(final).query):
            raise ValueError('Publisher response changed ISBN')
        (folder/'source.html').write_bytes(body)
        record = parse(body.decode(encoding), final)
        audit.update(state='accepted', sha256=hashlib.sha256(body).hexdigest())
        with (folder/'reference.json').open('x', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        return record
    except (OSError, ValueError, LookupError, TypeError) as exc:
        audit.update(state='failed', errorType=type(exc).__name__, httpStatus=getattr(exc, 'code', None))
        return None
    finally:
        with (folder/'acquisition.json').open('x', encoding='utf-8') as f:
            json.dump(audit, f, indent=2)


def corroborate(contents, packet):
    """Only assign a year to existing membership; ambiguous names stay unresolved."""
    references = packet.get('seriesIdentityReferences', [])
    if not references or contents.get('conflict'):
        return contents
    result = deepcopy(contents)
    for entry in list(result['unresolvedEntries']):
        candidates = []
        for reference in references:
            check_url(reference['url'])
            for row in rows_from_lines(reference['collectingLines']):
                if name_key(row['series']) != name_key(entry['series']):
                    continue
                # Distinct years are a veto even when their advertised ranges differ.
                candidates.append({**row, 'url': reference['url'], 'sourceIsbn': reference['sourceIsbn'],
                                   'sha256': reference['sha256']})
        years = {c['year'] for c in candidates}
        if len(years) != 1:
            if years:
                entry['reason'] = 'Publisher references disagree on series identity; no year inferred.'
            continue
        bounded = [c for c in candidates if c['first'] is not None
                   and c['first'] <= entry['first'] <= entry['last'] <= c['last']]
        if not bounded or entry.get('identityConflicts'):
            continue
        resolved = {k: v for k, v in entry.items() if k != 'reason'}
        resolved.update(year=bounded[0]['year'], identityResolution={
            'method': 'Exact series name corroborated by explicit dated publisher contents',
            'evidence': bounded, 'state': 'draft',
            'membershipEvidence': entry['evidence'], 'doesNotTransferOtherEditionContents': True})
        result['entries'].append(resolved)
        result['unresolvedEntries'].remove(entry)
        result['unparsed'].remove(entry['evidence'])
    return result
