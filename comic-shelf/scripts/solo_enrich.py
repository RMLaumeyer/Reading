"""One-command draft enrichment with bounded discovery and explicit review gates.

Optional Brave Search API uses BRAVE_SEARCH_API_KEY. No keys enter logs. Live
search must be explicitly enabled. This command never publishes website data.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlencode

import edition_sources as intake
import edition_trial as trial
import issue_fetch
import local_ai_trial as legacy
import reading_path
import featured_sources
import collection_path
import overdrive_sources
import series_references

FEATURED_LIST = 'https://share.marvel.com/comics/discover/1233/start-here-fantastic-four'

# Verified public source registrations, not invented issue/order answers. Titles
# select candidate sources only; placement still requires exact issue identities.
KNOWN_READING_LISTS = {
    'Absolute Carnage': 'https://share.marvel.com/comics/discover/1707/absolute-carnage',
    'X-Men: Messiah Complex': 'https://share.marvel.com/comics/discover/239/x-men-messiah-complex',
    'Civil War': 'https://share.marvel.com/comics/discover/114/civil-war-the-complete-event',
    'Secret Invasion': 'https://share.marvel.com/comics/discover/133/secret-invasion-the-complete-event',
}

# Source URLs only: no issue identities or edition contents are hardcoded here.
KNOWN_SERIES_REFERENCES = {
    'Annihilation': [
        'https://prhcomics.com/book/?isbn=9781302963255',
        'https://penguinrandomhouselibrary.com/book/?isbn=9781302963262',
    ],
}


def known_series_references(books):
    return [url for title, urls in KNOWN_SERIES_REFERENCES.items()
            if any(re.match(re.escape(title)+r'(?:$|\s+Book\b|\s+Modern Era\b)', b.get('title', ''), re.I)
                   for b in books) for url in urls]


def known_lists(books):
    return [url for title, url in KNOWN_READING_LISTS.items()
            if any(re.match(re.escape(title) + r'(?:$|:|\s*\[)', book.get('title', ''), re.I) for book in books)]


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Search API redirect refused')


def brave_search(query):
    key = os.environ.get('BRAVE_SEARCH_API_KEY')
    if not key:
        raise ValueError('BRAVE_SEARCH_API_KEY is not configured')
    url = 'https://api.search.brave.com/res/v1/web/search?' + urlencode({'q': query[:600], 'count': 5})
    request = urllib.request.Request(url, headers={'Accept': 'application/json', 'X-Subscription-Token': key})
    with urllib.request.build_opener(NoRedirects).open(request, timeout=25) as response:
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise ValueError('Search response exceeds limit')
        result = json.loads(body)
    if not isinstance(result, dict) or not isinstance(result.get('web', {}), dict):
        raise ValueError('Malformed search response')
    rows = result.get('web', {}).get('results', [])
    if not isinstance(rows, list):
        raise ValueError('Malformed search results')
    return [{'url': r.get('url'), 'heading': r.get('title')} for r in rows[:5] if isinstance(r, dict)]


def discover(packet, tasks, folder, budget, search):
    plan = {'isbn': packet['book']['isbn'], 'sources': []}
    report = []
    used = 0
    def checkpoint():
        # Only the current newly-created run is updated. A pending request counts
        # as spent after interruption; original response/snapshot files stay put.
        path = folder / 'discovery-checkpoint.json'
        temporary = folder / 'discovery-checkpoint.tmp'
        temporary.write_text(json.dumps({'queriesAttempted': used, 'plan': plan, 'report': report},
                                        indent=2, ensure_ascii=False), encoding='utf-8')
        temporary.replace(path)
    for task in tasks:
        if task['kind'] != 'story_evidence' or task['extent'] != 'whole':
            continue
        if used >= budget:
            report.append({'issue': task['issue'], 'state': 'budget_exhausted'})
            continue
        used += 1
        item = {'issue': task['issue'], 'query': task['query'], 'state': 'pending'}
        report.append(item)
        checkpoint()
        try:
            rows = search(task['query'])
            if not isinstance(rows, list):
                raise ValueError('Search provider must return a list')
            item['results'] = rows
            candidates = []
            unresolved_identity = False
            for row in rows:
                try:
                    issue_fetch.check_url(row.get('url', ''))
                    found = issue_fetch.title_from_headings([row.get('heading')], task['issue'], require_year=True)
                    if found:
                        candidates.append((row, found))
                    elif issue_fetch.title_from_headings([row.get('heading')], task['issue']):
                        unresolved_identity = True
                except (ValueError, TypeError, AttributeError):
                    continue
            if len({found['title'] for _, found in candidates}) > 1:
                item['state'] = 'conflicting_titles'
                continue
            if not candidates:
                item['state'] = 'identity_unverified' if unresolved_identity else 'no_matching_heading'
                continue
            # Select one explicit heading. Additional copies are not independent
            # corroboration; conflicting labels above are withheld for review.
            row, found = candidates[0]
            source_id = f'D{used}'
            snapshot = {'url': row['url'], 'heading': row['heading'], 'provider': 'web_search',
                'retrievedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'note': 'Automatically selected heading explicitly matches edition series, year and issue number. Search excerpt only, not full-page verification.'}
            save(folder / f'{source_id}-search.json', snapshot)
            plan['sources'].append({'id': source_id, 'url': row['url'], 'issue': task['issue'],
                                    'snapshot': f'{source_id}-search.json', 'identityMode': 'explicit_year'})
            item.update(state='candidate', title=found['title'], source=source_id)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            # Do not serialize provider exception objects or request headers.
            item.update(state='search_failed', errorType=type(exc).__name__)
            # Avoid repeatedly hitting an unavailable/rate-limited provider.
            break
        finally:
            checkpoint()
    checkpoint()
    save(folder / 'discovery.json', report)
    save(folder / 'fetch-plan.json', plan)
    return plan, report, used


def review_gate(result, supplement):
    """Report observable gaps; do not equate issue coverage with story completeness."""
    blockers = []
    contents = result['contents']
    if contents.get('conflict'):
        blockers.append('edition_contents_conflict')
    if result['stageErrors']:
        blockers.append('stage_errors')
    if not contents['entries']:
        blockers.append('no_accepted_inventory')
    if contents['unresolvedEntries'] or contents['unparsed']:
        blockers.append('unresolved_contents')
    if any(e['extent'] == 'partial' for e in contents['entries']):
        blockers.append('partial_material_requires_review')
    if any(e.get('identityResolution') for e in contents['entries']):
        blockers.append('bibliographic_series_identity_requires_review')
    if result.get('publisherIdentityConflicts') or any(p.get('identityMismatches') for p in result['readingOrder'].get('publisherPaths', [])):
        blockers.append('publisher_list_year_mismatch')
    coverage = result['storyCoverage']
    if coverage['issuesWithoutAnyStoryMapping']:
        blockers.append('issues_without_story_evidence')
    toc = result['readingOrder'].get('editionContentsOrder', {})
    if not toc.get('coversAllInventoriedWholeIssues'):
        blockers.append('printed_issue_order_incomplete')
    if any(s.get('provenance') == 'imported_search_snapshot' for s in supplement.get('sources', [])):
        blockers.append('search_excerpt_only')
    if any(s.get('identityMode') != 'explicit_year' for s in supplement.get('sources', [])):
        blockers.append('source_series_identity_requires_review')
    # No implemented stage establishes exhaustive story inventory or external
    # prerequisites. Explicitly retain these limitations even with zero issue gaps.
    blockers += ['exhaustive_story_coverage_unverified', 'external_reading_requirements_unverified',
                 'independent_accuracy_validation_pending']
    return {'decision': 'review_required', 'eligibleForPublication': False,
        'blockers': blockers, 'namedStoryCount': len(result.get('namedStories', [])),
        'issuesWithoutStoryMapping': coverage['issuesWithoutAnyStoryMapping'],
        'note': 'This gate routes drafts for review; it is not a semantic accuracy certificate.'}


def collection_coverage(result):
    """Unique issue evidence counts, never a completeness or accuracy score."""
    def key(issue):
        return (issue['series'].casefold(), issue['year'], issue['number'])
    contents = result['contents']
    whole = {(e['series'].casefold(), e['year'], n)
             for e in contents['entries'] if e['extent'] == 'whole' and e['year'] is not None
             for n in range(e['first'], e['last'] + 1)}
    missing = {key(i) for i in result['storyCoverage']['issuesWithoutAnyStoryMapping']}
    placed = {key(p['issue']) for path in result['readingOrder'].get('publisherPaths', [])
              if path['state'] == 'draft' for p in path['placements'] if p['extent'] == 'whole'} & whole
    return {'inventoriedWholeIssues': len(whole),
            'wholeIssuesWithAnyStoryEvidence': len(whole - missing),
            'wholeIssuesWithoutStoryEvidence': len(whole & missing),
            'wholeIssuesWithPublisherPosition': len(placed),
            'wholeIssuesWithoutPublisherPosition': len(whole - placed),
            'partialEntries': sum(e['extent'] == 'partial' for e in contents['entries']),
            'unresolvedEntries': len(contents['unresolvedEntries']),
            'unparsedContents': len(contents['unparsed']),
            'publisherIdentityMismatches': len({key(c['issue']) for c in
                result.get('publisherIdentityConflicts', []) + [c for p in result['readingOrder'].get('publisherPaths', [])
                                                               for c in p.get('identityMismatches', [])]}),
            'namedStories': len(result.get('namedStories', [])),
            'wholeIssuesWithPublisherDescription': len({key(f['issue']) for f in result.get('featuredStoryEvidence', [])} & whole),
            'complete': False,
            'note': 'Counts cover accepted inventory only. Story mapping counts require accepted titles or numbered parts; publisher descriptions are counted separately. Neither issue mapping nor description coverage establishes all contained stories or required reading.'}


def process(book, folder, model, budget=0, search=None, fetch=issue_fetch.download,
            refresh_edition=False, edition_fetch=intake.download_edition, reading_paths=(), featured_pages=(),
            fallback_fetch=overdrive_sources.download, series_identity_references=()):
    raw_path = legacy.ROOT / f'data/cache/google-{book["isbn"]}.html'
    remote = refresh_edition or not raw_path.exists()
    acquisition = {'mode': 'live_isbn_lookup' if remote else 'existing_cache',
                   'retrievedAt': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        if remote:
            body, url, encoding = edition_fetch(book['isbn'])
            acquisition['url'] = url
        else:
            body, encoding = raw_path.read_bytes(), 'utf-8'
        (folder / 'source.html').write_bytes(body)
        acquisition['sha256'] = hashlib.sha256(body).hexdigest()
        raw = body.decode(encoding)
    except (OSError, ValueError, LookupError) as exc:
        acquisition.update(state='failed', errorType=type(exc).__name__, httpStatus=getattr(exc, 'code', None))
        save(folder / 'acquisition.json', acquisition)
        raise
    packet, supplement, prepared = intake.prepare(book, raw, series_identity_references=series_identity_references)
    if remote and not packet['constraints'].get('isbnMatched'):
        acquisition['state'] = 'isbn_mismatch'
        save(folder / 'acquisition.json', acquisition)
        raise ValueError('Downloaded edition does not explicitly identify requested ISBN')
    fallback_state = 'not_needed'
    fallback_http_status = None
    if not prepared.get('contents', {}).get('entries') and 'contents' in prepared:
        extra = overdrive_sources.acquire(book['isbn'], folder / 'overdrive', fetch=fallback_fetch) if fallback_fetch else None
        fallback_state = ('accepted' if extra else 'unavailable') if fallback_fetch else 'disabled_for_batch'
        if fallback_fetch:
            fallback_http_status = json.loads((folder / 'overdrive/acquisition.json').read_text(encoding='utf-8')).get('httpStatus')
        if extra:
            packet, supplement, prepared = intake.prepare(book, raw, extra_sources=[extra],
                series_identity_references=series_identity_references)
    prepared['editionFallbackState'] = fallback_state
    conflicts = [{**c, 'sourceUrl': path['sourceUrl']}
                 for path in reading_paths if path['state'] == 'draft'
                 for c in reading_path.map_edition(path, prepared['contents'])['identityMismatches']]
    if conflicts:
        packet['constraints']['publisherYearConflicts'] = conflicts
        prepared['contents'] = trial.inventory(packet)
        # Do not spend search queries using a bibliographic year now withheld.
        unresolved = prepared['contents']['unresolvedEntries']
        prepared['researchQueue'] = [q for q in prepared['researchQueue']
            if not (q.get('issue') and any(e['series'].casefold() == q['issue']['series'].casefold()
                    and e['first'] <= q['issue']['number'] <= e['last'] for e in unresolved))]
        prepared['researchQueue'].extend({'kind': 'series_identity', 'entry': e, 'needed': e['reason']}
                                        for e in unresolved if e.get('identityConflicts'))
        prepared['publisherIdentityConflicts'] = conflicts
    if remote:
        packet['sources'][0]['kind'] = 'Downloaded Google Books publisher metadata'
    acquisition['state'] = 'accepted'
    save(folder / 'acquisition.json', acquisition)
    save(folder / 'packet.json', packet)
    save(folder / 'intake.json', prepared)
    featured_evidence, feature_sources = featured_sources.edition_evidence(featured_pages, prepared['contents']) if featured_pages else ([], [])
    supplement['sources'].extend(feature_sources)
    used = 0
    discovery_state = 'disabled'
    if search:
        plan, report, used = discover(packet, prepared['researchQueue'], folder, budget, search)
        discovery_state = ('search_failed' if any(r['state'] == 'search_failed' for r in report)
            else 'budget_exhausted' if any(r['state'] == 'budget_exhausted' for r in report) else 'completed')
        if plan['sources']:
            fetched_dir = folder / 'fetched'
            fetched_dir.mkdir()
            acquired, _ = issue_fetch.acquire(plan, packet, fetched_dir, folder, fetch)
            supplement['sources'].extend(acquired['sources'])
    save(folder / 'supplement.json', supplement)
    result = trial.run(packet, supplement, model)
    result['featuredStoryEvidence'] = featured_evidence
    result['publisherIdentityConflicts'] = conflicts
    mapped_paths = [reading_path.map_edition(path, result['contents']) for path in reading_paths]
    result['readingOrder']['publisherPaths'] = mapped_paths
    if (result['readingOrder']['state'] == 'missing_evidence'
            and any(p['state'] == 'draft' and p['placements'] for p in mapped_paths)):
        result['readingOrder'].update(state='draft', scope='Publisher-listed issue positions',
            reason='Listed positions do not establish all required prerequisites or complete edition story coverage.')
    result['collectionCoverage'] = collection_coverage(result)
    save(folder / 'result.json', result)
    gate = review_gate(result, supplement)
    gate['discoveryState'] = discovery_state
    if discovery_state != 'completed':
        gate['blockers'].append('source_discovery_unavailable_or_disabled')
    save(folder / 'review.json', gate)
    return {'isbn': book['isbn'], 'status': result['status'], 'stageErrors': result['stageErrors'],
            'decision': gate['decision'], 'blockers': gate['blockers'], 'searchQueries': used,
            'namedStories': len(result.get('namedStories', [])),
            'featuredDescriptions': len(featured_evidence),
            'editionStoryHighlights': len(result.get('featuredStoryHighlights', [])),
            'editionFallbackState': fallback_state,
            'editionFallbackHttpStatus': fallback_http_status,
            'collectionCoverage': result['collectionCoverage'],
            'publisherPathPlacements': sum(len(p['placements']) for p in mapped_paths)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--isbn', action='append', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', default='qwen3.5-4b')
    parser.add_argument('--search', action='store_true', help='Enable Brave API requests using configured key')
    parser.add_argument('--refresh-edition', action='store_true', help='Download current ISBN metadata into this run; leave existing caches untouched')
    parser.add_argument('--reading-list', action='append', default=[], help='Public Marvel reading-list URL to collect and map; at most three')
    parser.add_argument('--featured-list', action='append', default=[], help='Publisher feature-description list; at most three, separate from reading order')
    parser.add_argument('--series-reference', action='append', default=[], help='Public PRH ISBN page for series identity corroboration; at most three')
    parser.add_argument('--max-queries', type=int, default=5, help='Total search attempts across the batch, at most 20')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', args.name) or not 1 <= args.max_queries <= 20:
        parser.error('Use a valid run name and query budget 1–20')
    if any(not re.fullmatch(r'\d{13}', isbn) for isbn in args.isbn) or len(set(args.isbn)) != len(args.isbn):
        parser.error('Use unique 13-digit ISBNs')
    if len(args.reading_list) > 3 or len(set(args.reading_list)) != len(args.reading_list):
        parser.error('Use at most three distinct reading lists')
    for url in args.reading_list:
        reading_path.check_list_url(url)
    if len(args.featured_list) > 3 or len(set(args.featured_list)) != len(args.featured_list):
        parser.error('Use at most three distinct featured lists')
    for url in args.featured_list:
        reading_path.check_list_url(url)
    folder = legacy.OUT / args.name
    books = {b['isbn']: b for b in json.loads((legacy.ROOT / 'public/catalog.json').read_text(encoding='utf-8'))['books']}
    list_selection = 'explicit' if args.reading_list else 'registered_sources'
    if not args.reading_list:
        args.reading_list = known_lists([books[i] for i in args.isbn if i in books])
    if len(args.reading_list) > 3:
        parser.error('This batch selects more than three registered lists; split it into smaller batches')
    if not args.featured_list and any(re.match(r'^Fantastic Four\b', books[i].get('title', ''), re.I)
                                     for i in args.isbn if i in books):
        args.featured_list = [FEATURED_LIST]
    if not args.series_reference:
        args.series_reference = known_series_references([books[i] for i in args.isbn if i in books])
    if len(args.series_reference) > 3 or len(set(args.series_reference)) != len(args.series_reference):
        parser.error('Use at most three distinct series references')
    for url in args.series_reference:
        series_references.check_url(url)
    folder.mkdir(exist_ok=False)
    search = brave_search if args.search and os.environ.get('BRAVE_SEARCH_API_KEY') else None
    save(folder / 'run.json', {'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'model': args.model, 'searchRequested': args.search, 'searchConfigured': search is not None,
        'refreshEdition': args.refresh_edition,
        'readingLists': args.reading_list,
        'featuredLists': args.featured_list,
        'seriesReferences': args.series_reference,
        'readingListSelection': list_selection,
        'maxQueries': args.max_queries, 'isbns': args.isbn,
        'codeSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [Path(__file__), Path(intake.__file__), Path(trial.__file__), Path(issue_fetch.__file__),
             Path(legacy.__file__), Path(reading_path.__file__), Path(featured_sources.__file__), Path(collection_path.__file__), Path(overdrive_sources.__file__), Path(series_references.__file__), Path(trial.edition_highlights.__file__), Path(__file__).with_name('local_ai_quality.py'), Path(__file__).with_name('parse_sources.py')]}})
    identity_references = []
    for index, url in enumerate(args.series_reference, 1):
        target = folder/f'series-reference-{index}'
        reference = series_references.acquire(url, target)
        if reference:
            identity_references.append(reference)
        else:
            audit = json.loads((target/'acquisition.json').read_text(encoding='utf-8'))
            if audit.get('httpStatus') in (403, 429, 503):
                break
    featured_pages = []
    for index, url in enumerate(args.featured_list, 1):
        target = folder / f'featured-list-{index}'
        target.mkdir()
        try:
            body, final_url, encoding = reading_path.download_list(url)
            (target / 'source.html').write_bytes(body)
            page = featured_sources.parse_features(body.decode(encoding), final_url)
            page.update(sha256=hashlib.sha256(body).hexdigest(), retrievedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
            save(target / 'features.json', page)
            featured_pages.append(page)
        except (OSError, ValueError, LookupError) as exc:
            save(target / 'error.json', {'url': url, 'errorType': type(exc).__name__, 'httpStatus': getattr(exc, 'code', None)})
    reading_paths = []
    for index, url in enumerate(args.reading_list, 1):
        target = folder / f'reading-list-{index}'
        target.mkdir()
        try:
            body, final_url, encoding = reading_path.download_list(url)
            (target / 'source.html').write_bytes(body)
            path = reading_path.parse_list(body.decode(encoding), final_url)
            path['sha256'] = hashlib.sha256(body).hexdigest()
            path['retrievedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            save(target / 'path.json', path)
            reading_paths.append(path)
        except (OSError, ValueError, LookupError) as exc:
            save(target / 'error.json', {'url': url, 'errorType': type(exc).__name__, 'httpStatus': getattr(exc, 'code', None)})
    report, remaining = [], args.max_queries
    fallback_fetch = overdrive_sources.download
    for isbn in args.isbn:
        target = folder / isbn
        target.mkdir()
        try:
            row = process(books[isbn], target, args.model, remaining, search,
                          refresh_edition=args.refresh_edition, reading_paths=reading_paths, featured_pages=featured_pages,
                          fallback_fetch=fallback_fetch, series_identity_references=identity_references)
            if row.get('editionFallbackHttpStatus') in (403, 429, 503):
                fallback_fetch = None
            remaining -= row['searchQueries']
            if row.get('blockers') and 'source_discovery_unavailable_or_disabled' in row['blockers']:
                search = None
            report.append(row)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            # If a book fails after searches, conservatively stop further search
            # spending rather than lose its consumed budget during exception exit.
            remaining, search = 0, None
            row = {'isbn': isbn, 'status': 'failed', 'errorType': type(exc).__name__, 'eligibleForPublication': False}
            save(target / 'error.json', row)
            report.append(row)
        print(json.dumps(report[-1]), flush=True)
    save(folder / 'report.json', report)
    editions, unavailable = [], []
    for row in report:
        result_path = folder / row['isbn'] / 'result.json'
        if result_path.exists():
            editions.append({'isbn': row['isbn'], 'title': books[row['isbn']]['title'],
                             'result': json.loads(result_path.read_text(encoding='utf-8'))})
        else:
            unavailable.append({'isbn': row['isbn'], 'status': row['status']})
    save(folder / 'collection-paths.json', [collection_path.build(p, editions, unavailable) for p in reading_paths])


if __name__ == '__main__':
    main()
