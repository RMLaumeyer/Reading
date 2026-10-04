"""Import a scoped independent reading guide and map it to saved edition drafts."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit

import collection_path
import series_references as refs
import order_identity


def check_url(url):
    p = urlsplit(url)
    if (p.scheme != 'https' or p.hostname != 'marvelguides.com' or p.username or p.password
            or p.port not in (None, 443) or p.query or p.fragment
            or not re.fullmatch(r'/[a-z0-9-]+-reading-order/?', p.path)):
        raise ValueError('Use a public Marvel Guides reading-order page')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        if urlsplit(req.full_url).path.rstrip('/') != urlsplit(newurl).path.rstrip('/'):
            raise ValueError('Guide redirect changed scope')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    check_url(url)
    request = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1'})
    with urllib.request.build_opener(Redirects).open(request, timeout=25) as response:
        check_url(response.url)
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected guide HTML')
        body = response.read(3_000_001)
        if len(body) > 3_000_000:
            raise ValueError('Guide exceeds limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


class Blocks(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.blocks, self.parts, self.tag, self.skip = [], [], None, 0
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav'):
            self.skip += 1
        if not self.skip and self.tag is None and tag in ('li', 'p', 'h1', 'h2', 'h3', 'h4', 'title'):
            self.tag, self.parts = tag, []

    def handle_data(self, text):
        if self.tag and not self.skip:
            self.parts.append(text)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav'):
            self.skip = max(0, self.skip-1)
        if not self.skip and tag == self.tag:
            self.blocks.append((tag, ' '.join(''.join(self.parts).split())))
            self.tag = None


def sections_with_lists(raw):
    """Discover full-page scope explicitly; never silently choose an event subset."""
    current, reading, found = None, False, []
    for tag,text in Blocks(raw).blocks:
        if re.match(r'^Part \d+(?:\.\d+)*:',text):
            current,reading=text,False
        elif current and text=='Reading Order:':
            reading=True
        elif reading and tag=='li':
            if current not in found:found.append(current)
        elif reading:
            reading=False
    if not 1<=len(found)<=10:raise ValueError('No bounded set of explicit reading-list sections')
    return found


def parse(raw, url, sections, references):
    check_url(url)
    if not sections or len(set(sections)) != len(sections) or len(sections) > 10:
        raise ValueError('Select one to ten distinct section headings')
    blocks = Blocks(raw).blocks
    titles = [text for tag, text in blocks if tag.startswith('h') and text.endswith('Reading Order')]
    document_titles = [text for tag,text in blocks if tag=='title']
    if document_titles:
        if len(document_titles)!=1:raise ValueError('Ambiguous document title')
        match=re.fullmatch(r'(.+? Reading Order)\s*[—–|]\s*Marvel Guides',document_titles[0])
        expected=urlsplit(url).path.strip('/').removesuffix('-reading-order')
        if not match or refs.name_key(match[1].removesuffix(' Reading Order'))!=refs.name_key(expected):
            raise ValueError('Document title does not match requested event')
        titles=[match[1]]
    if len(titles) != 1:
        raise ValueError('Missing unique reading-guide title')
    evidence = []
    for reference in references:
        refs.check_url(reference['url'])
        evidence.extend({**r, 'sourceUrl': reference['url'], 'sourceSha256': reference['sha256']}
                        for r in refs.rows_from_lines(reference['collectingLines']))
    current, active, seen = None, False, []
    markers = {s: 0 for s in sections}
    row_counts = {s: 0 for s in sections}
    nodes, problems, identities, sequence = [], [], set(), []
    for tag, text in blocks:
        if re.match(r'^Part \d+(?:\.\d+)*:', text):
            current, active = text, False
            if current in sections:
                seen.append(current)
            continue
        if current not in sections:
            continue
        if text == 'Reading Order:':
            markers[current] += 1
            active = True
            continue
        if not active:
            continue
        if tag != 'li':
            active = False
            continue
        row_counts[current] += 1
        match = re.fullmatch(r'(.+?)(?:\s+\((\d{4})\))?\s+#(\d+)(?:\s*[-–]\s*#?(\d+))?', text)
        if not match or not 0 <= int(match[4] or match[3])-int(match[3]) <= 150:
            sequence.append({'position': len(sequence)+1, 'section': current, 'quote': text,
                             'sourceUrl': url, 'issue': None, 'identityState': 'unsupported'})
            problems.append({'section': current, 'quote': text, 'reason': 'Unsupported issue range'})
            continue
        name, year, first, last = match.groups()
        first, last = int(first), int(last or first)
        slots = [{'position': len(sequence)+number-first+1, 'section': current, 'quote': text,
                  'sourceUrl': url, 'issue': {'series': name, 'year': None, 'number': number},
                  'identityState': 'unresolved'} for number in range(first,last+1)]
        sequence.extend(slots)
        candidates = [r for r in evidence if refs.name_key(r['series']) == refs.name_key(name)]
        years = {r['year'] for r in candidates}
        if year:
            years.add(int(year))
        supported = [r for r in candidates if r['first'] is None or r['first'] <= first <= last <= r['last']]
        if len(years) != 1 or any(not 1900 <= y <= 2100 for y in years) or (not year and not supported):
            if years:
                for slot in slots: slot['identityState'] = 'conflict' if len(years)>1 else 'unsupported'
            problems.append({'section': current, 'quote': text, 'reason': 'Series identity unresolved or conflicting'})
            continue
        resolved_year = next(iter(years))
        for slot, number in zip(slots, range(first, last+1)):
            key = refs.name_key(name), resolved_year, number
            if key in identities:
                slot['identityState'] = 'duplicate'
                problems.append({'section': current, 'quote': text, 'reason': 'Duplicate issue identity'})
                continue
            identities.add(key)
            nodes.append({'position': slot['position'], 'section': current,
                          'issue': {'series': name, 'year': resolved_year, 'number': number},
                          'quote': text, 'sourceUrl': url,
                          'identityEvidence': supported, 'identityRequiresReview': not bool(year)})
            slot.update(nodes[-1], identityState='resolved')
    if (sorted(seen) != sorted(sections) or not sequence or len(sequence) > 500
            or any(markers[s] != 1 or not row_counts[s] for s in sections)):
        raise ValueError('Missing/duplicate selected sections or unbounded/empty guide')
    return {'sourceUrl': url, 'title': titles[0], 'sourceKind': 'independent_editorial',
            'selectedSections': seen, 'orderedIssues': nodes, 'sourceSequence': sequence, 'problems': problems,
            'state': 'needs_review' if problems else 'draft',
            'scope': 'Selected sections of an independent editorial recommendation',
            'complete': False, 'requiredReadingEstablished': False, 'chronologyEstablished': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--section', action='append', required=True)
    parser.add_argument('--edition-run', type=Path, required=True)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    check_url(args.url)
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,60}', args.name):
        parser.error('Use a safe unique run name')
    folder = Path(__file__).resolve().parents[1]/'data/local-ai-trials'/args.name
    folder.mkdir(exist_ok=False)
    def save(name, value):
        with (folder/name).open('x', encoding='utf-8') as f:
            json.dump(value, f, indent=2, ensure_ascii=False)
    inputs, editions, references = {}, [], []
    for target in sorted(args.edition_run.glob('*/result.json')):
        packet_file = target.parent/'packet.json'
        packet = json.loads(packet_file.read_text(encoding='utf-8'))
        for file in (target, packet_file):
            inputs[str(file.resolve())] = hashlib.sha256(file.read_bytes()).hexdigest()
        references.extend(packet.get('seriesIdentityReferences', []))
        editions.append({'isbn': packet['book']['isbn'], 'title': packet['book']['title'],
                         'result': json.loads(target.read_text(encoding='utf-8'))})
    if not editions:
        raise ValueError('No completed edition drafts')
    editions, identity_warnings = order_identity.audit_editions(editions)
    save('edition-identity-audit.json', {'warnings': identity_warnings})
    save('manifest.json', {'inputs': inputs, 'url': args.url, 'sections': args.section,
                          'codeSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                         [Path(__file__), Path(collection_path.__file__), Path(refs.__file__), Path(order_identity.__file__)]}})
    try:
        body, url, encoding = download(args.url)
        (folder/'source.html').write_bytes(body)
        path = parse(body.decode(encoding), url, args.section, references)
        path['sha256'] = hashlib.sha256(body).hexdigest()
        save('extracted-path.json', path)
        path = order_identity.resolve(path, editions)
        save('path.json', path)
        mapped = collection_path.build(path, editions)
        save('collection-path.json', mapped)
        print(json.dumps(mapped['coverage']))
    except (OSError, ValueError, LookupError) as exc:
        save('error.json', {'errorType': type(exc).__name__, 'httpStatus': getattr(exc, 'code', None)})
        raise


if __name__ == '__main__':
    main()
