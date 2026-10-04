"""Build isolated edition packets and order evidence from raw cached metadata.

Does not read website annotations, invent story titles, or publish data. Optional
local inference is sequential. Every invocation requires a new output directory.
"""
import argparse
import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit
from urllib.parse import quote_plus

import edition_trial as trial
import local_ai_trial as legacy
from parse_sources import Page


def packet_from_html(book, raw):
    """Same publisher-only packet format as frozen legacy, without a cache dependency."""
    page = Page(raw)
    clean = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', raw, flags=re.S | re.I)
    plain = legacy.normalize(Page(clean).plain)
    bib = plain.partition('Bibliographic information')[2]
    description = legacy.normalize(html.unescape(page.meta.get('description', '')))
    source = {'id': 'S1', 'url': page.meta.get('og:url') or 'https://books.google.com/books?vid=ISBN'+book['isbn'],
        'kind': 'Cached Google Books publisher metadata',
        'text': 'Synopsis: '+description[:7000]+'\nBibliographic information: '+bib[:3000],
        'cacheSha256': hashlib.sha256(raw.encode('utf-8')).hexdigest()}
    return {'book': {k: book.get(k) for k in ['isbn', 'title', 'author', 'catalogUrl']},
            'sources': [source], 'constraints': legacy.constraints_for(book, description, bib)}


class EditionRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        p = urlsplit(newurl)
        if p.scheme != 'https' or p.hostname != 'books.google.com' or p.username or p.password or p.port not in (None, 443):
            raise ValueError('Edition redirect left Google Books')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_edition(isbn):
    if not re.fullmatch(r'\d{13}', isbn):
        raise ValueError('Edition lookup requires a 13-digit ISBN')
    url = 'https://books.google.com/books?vid=ISBN'+isbn
    request = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1 (personal metadata research)'})
    with urllib.request.build_opener(EditionRedirects).open(request, timeout=25) as response:
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected edition HTML')
        body = response.read(3_000_001)
        if len(body) > 3_000_000:
            raise ValueError('Edition page exceeds limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


class ContentsParser(HTMLParser):
    """Only explicit Google Books TOC cells; ignore prose, scripts and page numbers."""
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.rows, self.parts = [], None
        self.depth = 0
        self.skip = 0
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.skip += 1
        if self.skip:
            return
        if tag == 'div' and (self.depth or attrs.get('id') == 'toc'):
            self.depth += 1
        if self.depth and tag == 'td' and 'toc_entry' in attrs.get('class', '').split():
            self.parts = []

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == 'td' and self.parts is not None:
            self.rows.append(' '.join(''.join(self.parts).split()))
            self.parts = None
        if tag == 'div' and self.depth:
            self.depth -= 1

    def handle_data(self, text):
        if self.parts is not None and not self.skip:
            self.parts.append(text)


def prepare(book, raw, extra_sources=(), series_identity_references=()):
    packet = packet_from_html(book, raw)
    if series_identity_references:
        packet['seriesIdentityReferences'] = list(series_identity_references)
    for source in extra_sources:
        packet['sources'].append(source)
        extra_constraints = legacy.constraints_for(book, source['description'], 'ISBN '+source['editionIsbn'])
        if extra_constraints.get('contentsConflict'):
            packet['constraints']['contentsConflict'] = True
            packet['constraints']['additionalSourceConflict'] = {'source': source['id'], **extra_constraints}
    contents = trial.inventory(packet)
    source = packet['sources'][0]
    rows = ContentsParser(raw).rows
    omitted = [r for r in rows if r.casefold() in ('copyright', 'title page')]
    candidates = [r for r in rows if r not in omitted]
    supplement = {'isbn': book['isbn'], 'sources': [],
        'curationNote': 'Automatically parsed raw cached edition TOC; no manually supplied issue/story answers.'}
    intake = {'tocRows': rows, 'omittedNonStoryRows': omitted, 'orderState': 'missing_evidence',
        'orderError': None, 'contents': contents}
    bib = source['text'].partition('Bibliographic information:')[2]
    isbn_match = re.search(r'\bISBN\s+([\d,\sXx-]+)', bib)
    if candidates:
        evidence = {'kind': 'table_of_contents', 'isbn': book['isbn'], 'url': source['url'],
            'isbnQuote': isbn_match[0] if isbn_match else '', 'rows': candidates,
            'cacheSha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
            'curationNote': 'TOC cell text in DOM order, whitespace normalized. Unknown rows are retained and block automatic acceptance.'}
        try:
            order = trial.edition_contents_order(evidence, packet, contents, [])
            supplement['editionContentsOrder'] = evidence
            intake['orderState'] = order['state']
            intake['coversAllInventoriedWholeIssues'] = order['coversAllInventoriedWholeIssues']
        except (ValueError, KeyError, TypeError) as exc:
            intake['orderState'] = 'needs_review'
            intake['orderError'] = str(exc)
    # A retrieval queue is explicit work remaining, not a fabricated title answer.
    queue, seen = [], set()
    for entry in contents['entries']:
        for number in range(entry['first'], entry['last'] + 1):
            key = (entry['series'], entry['year'], number, entry['portion'])
            if key in seen:
                continue
            seen.add(key)
            query = f'"{entry["series"]}" ({entry["year"]}) #{number} story title'
            if entry['portion']:
                query += ' ' + entry['portion']
            queue.append({'kind': 'story_evidence', 'issue': {'series': entry['series'], 'year': entry['year'], 'number': number},
                'extent': entry['extent'], 'portion': entry['portion'],
                'needed': 'Issue-level story title/scope evidence; edition membership alone is insufficient',
                'query': query, 'searchUrl': 'https://www.google.com/search?q=' + quote_plus(query)})
    for entry in contents['unresolvedEntries']:
        query = f'"{book["isbn"]}" "{entry["series"]}" collected issues series year'
        queue.append({'kind': 'series_identity', 'entry': entry, 'needed': entry['reason'],
                      'query': query, 'searchUrl': 'https://www.google.com/search?q=' + quote_plus(query)})
    unresolved_quotes = [e['evidence'] for e in contents['unresolvedEntries']]
    for evidence in contents['unparsed']:
        if evidence not in unresolved_quotes:
            queue.append({'kind': 'contents_review', 'evidence': evidence,
                          'needed': 'Resolve unparsed collecting text before issue/story research'})
    if packet.get('constraints', {}).get('contentsConflict'):
        queue.append({'kind': 'edition_conflict', 'needed': 'Resolve edition contents conflict using ISBN-matched evidence'})
    elif not contents['entries'] and not contents['unresolvedEntries'] and not contents['unparsed']:
        queue.append({'kind': 'edition_contents', 'needed': 'Find an ISBN-matched collecting statement; this source supplied no accepted contents'})
    if intake['orderState'] == 'needs_review':
        queue.append({'kind': 'order_evidence', 'needed': intake['orderError'],
                      'rows': rows, 'url': source['url']})
    intake['researchQueue'] = queue
    return packet, supplement, intake


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--isbn', action='append', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', help='Optional loaded local model; otherwise prepare evidence only')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', args.name):
        parser.error('Invalid run name')
    if len(set(args.isbn)) != len(args.isbn) or any(not re.fullmatch(r'\d{13}', i) for i in args.isbn):
        parser.error('Use unique 13-digit ISBNs')
    books = {b['isbn']: b for b in json.loads((legacy.ROOT / 'public/catalog.json').read_text(encoding='utf-8'))['books']}
    folder = legacy.OUT / args.name
    folder.mkdir(exist_ok=False)
    def save(path, value):
        with path.open('x', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
    save(folder / 'run.json', {'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'isbns': args.isbn, 'model': args.model, 'purpose': 'Source intake development, not an accuracy benchmark',
        'codeSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [Path(__file__), Path(trial.__file__), Path(trial.edition_highlights.__file__), Path(trial.series_references.__file__), Path(legacy.__file__), Path(__file__).with_name('parse_sources.py'), Path(__file__).with_name('local_ai_quality.py')]}})
    report = []
    for isbn in args.isbn:
        target = folder / isbn
        target.mkdir()
        try:
            raw_path = legacy.ROOT / f'data/cache/google-{isbn}.html'
            raw = raw_path.read_text(encoding='utf-8')
            packet, supplement, intake = prepare(books[isbn], raw)
            # Keep exact cached bytes as well as normalized source excerpts.
            (target / 'source.html').write_bytes(raw_path.read_bytes())
            save(target / 'packet.json', packet)
            save(target / 'supplement.json', supplement)
            save(target / 'intake.json', intake)
            summary = {'isbn': isbn, 'title': books[isbn]['title'], 'orderState': intake['orderState'],
                'inventoryEntries': len(intake['contents']['entries']), 'unresolvedEntries': len(intake['contents']['unresolvedEntries']),
                'researchItems': len(intake['researchQueue'])}
            if args.model:
                result = trial.run(packet, supplement, args.model)
                save(target / 'result.json', result)
                summary['stageErrors'] = result['stageErrors']
            report.append(summary)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            error = {'isbn': isbn, 'error': str(exc)}
            save(target / 'error.json', error)
            report.append(error)
    save(folder / 'report.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
