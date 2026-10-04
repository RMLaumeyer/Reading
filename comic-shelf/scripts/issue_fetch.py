"""Fetch selected issue metadata into new draft-only experiment folders.

URLs and series years are curated inputs. Never scrapes search engines or bypasses
blocked pages. Explicit imported search snapshots are separately labelled fallbacks.
"""
import argparse
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
from urllib.parse import urlsplit

import edition_trial as trial
import local_ai_trial as legacy

HOSTS = {'comicvine.gamespot.com', 'www.marvel.com', 'marvel.fandom.com', 'www.comics.org', 'my.comics.org'}
MAX_BYTES = 3_000_000


def check_url(url):
    p = urlsplit(url)
    if p.scheme != 'https' or p.hostname not in HOSTS or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Use an HTTPS issue URL on a supported source host')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    check_url(url)
    request = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1 (personal metadata research)', 'Accept': 'text/html'})
    with urllib.request.build_opener(Redirects).open(request, timeout=25) as response:
        check_url(response.url)
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected an HTML metadata page')
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('Source exceeds metadata download limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


class Headings(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.headings, self.tag, self.parts = [], None, []
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        if tag in ('title', 'h1'):
            self.tag, self.parts = tag, []

    def handle_data(self, data):
        if self.tag:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.tag:
            self.headings.append(' '.join(''.join(self.parts).split()))
            self.tag = None


def title_from_headings(headings, issue, require_year=False):
    # An issue heading without a story subtitle is not a named story. Series year
    # may be absent (curated in plan), but an explicitly different year must fail.
    year = r'\s+\(' + str(issue['year']) + r'\)'
    prefix = re.escape(issue['series']) + (year if require_year else '(?:' + year + ')?') + r'\s+#' + str(issue['number'])
    pattern = prefix + r'\s+[-–]\s+(.+?)(?:\s+\(Issue\)(?:\s+-\s+Comic Vine)?)?'
    found = []
    for heading in headings:
        if not isinstance(heading, str) or len(heading) > 450:
            continue
        match = re.fullmatch(pattern, heading)
        if match and match[1].strip() and match[1] not in [x['title'] for x in found]:
            found.append({'title': match[1], 'heading': heading})
    if len(found) > 1:
        raise ValueError('Conflicting story subtitles in page headings')
    return found[0] if found else None


def validate_plan(plan, packet):
    if not isinstance(plan, dict) or plan.get('isbn') != packet['book']['isbn']:
        raise ValueError('Fetch plan must match packet ISBN')
    sources = plan.get('sources')
    if not isinstance(sources, list) or not 1 <= len(sources) <= 20:
        raise ValueError('Select one to twenty issue sources per run')
    ids = set()
    for s in sources:
        check_url(s['url'])
        if s.get('identityMode', 'curated_year') not in ('curated_year', 'explicit_year'):
            raise ValueError('Unknown issue identity verification mode')
        # Reuse identity validation before any requests. Dummy excerpt is not evidence.
        trial.validate_sources([{**s, 'text': 'plan validation only'}])
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,40}', s['id']) or s['id'] in ids:
            raise ValueError('Source IDs must be unique safe filenames')
        ids.add(s['id'])


def acquire(plan, packet, folder, plan_dir, fetch=download):
    validate_plan(plan, packet)
    contents = trial.inventory(packet)
    supplement = {'isbn': plan['isbn'], 'sources': [],
        'curationNote': 'Automatically extracted issue-heading subtitles. URLs and series years are curated; all mappings require review.'}
    report = []
    def save(name, value):
        with (folder / name).open('x', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
    for s in plan['sources']:
        item = {'id': s['id'], 'url': s['url'], 'issue': s['issue'], 'state': 'pending',
                'retrievedAt': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        report.append(item)
        issue = s['issue']
        if not any(e['extent'] == 'whole' and e['series'] == issue['series'] and e['year'] == issue['year']
                   and e['first'] <= issue['number'] <= e['last'] for e in contents['entries']):
            item.update(state='needs_review', reason='No accepted whole-issue membership; no request made')
            continue
        headings = []
        try:
            body, final_url, encoding = fetch(s['url'])
            (folder / (s['id'] + '.html')).write_bytes(body)
            item.update(provenance='downloaded_html', finalUrl=final_url, sha256=hashlib.sha256(body).hexdigest())
            headings = Headings(body.decode(encoding, errors='replace')).headings
        except (OSError, ValueError, LookupError) as exc:
            item['downloadError'] = str(exc)
            item['httpStatus'] = getattr(exc, 'code', None)
            item['state'] = 'download_failed'
        if not headings and s.get('snapshot'):
            try:
                path = (plan_dir / s['snapshot']).resolve()
                if not path.is_relative_to(plan_dir.resolve()):
                    raise ValueError('Snapshot must be inside the plan directory')
                snapshot = json.loads(path.read_text(encoding='utf-8-sig'))
                if (snapshot.get('url') != s['url'] or snapshot.get('provider') != 'web_search'
                        or not snapshot.get('retrievedAt') or not isinstance(snapshot.get('heading'), str)):
                    raise ValueError('Snapshot needs matching URL, provider, date and heading')
                headings = [snapshot['heading']]
                save(s['id'] + '-snapshot.json', snapshot)
                item.update(provenance='imported_search_snapshot', snapshotRetrievedAt=snapshot['retrievedAt'],
                            snapshotSha256=hashlib.sha256(path.read_bytes()).hexdigest())
            except (OSError, ValueError, TypeError) as exc:
                item.update(state='snapshot_failed', reason=str(exc))
                continue
        if not headings:
            item.setdefault('reason', 'No usable headings available')
            if item['state'] == 'pending':
                item['state'] = 'no_heading'
            continue
        try:
            found = title_from_headings(headings, issue, require_year=s.get('identityMode') == 'explicit_year')
            if not found:
                item.update(state='no_explicit_title', reason='No exact matching issue heading with a story subtitle')
                continue
            item.update(state='draft_title', title=found['title'], heading=found['heading'])
            supplement['sources'].append({'id': s['id'], 'url': s['url'], 'kind': 'story_title',
                'issue': issue, 'text': found['title'], 'headingQuote': found['heading'],
                'provenance': item['provenance'], 'retrievedAt': item['retrievedAt'],
                'identityMode': s.get('identityMode', 'curated_year'),
                'mappingNote': 'Evidence channel: ' + item['provenance'] + '. ' +
                    ('Series name, year and issue number explicitly matched in heading. ' if s.get('identityMode') == 'explicit_year'
                     else 'Series name and issue number matched in heading; series-start year supplied by curated fetch plan, not independently verified. ') +
                    'Not a completeness claim.'})
        except ValueError as exc:
            item.update(state='needs_review', reason=str(exc))
    save('supplement.json', supplement)
    save('fetch-report.json', report)
    return supplement, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--model')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', args.name):
        parser.error('Invalid run name')
    packet = json.loads(args.packet.read_text(encoding='utf-8-sig'))
    plan = json.loads(args.plan.read_text(encoding='utf-8-sig'))
    validate_plan(plan, packet)
    folder = legacy.OUT / args.name
    folder.mkdir(exist_ok=False)
    def save(name, value):
        with (folder / name).open('x', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
    save('inputs.json', {'packet': packet, 'plan': plan})
    save('run.json', {'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'model': args.model,
        'codeSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [Path(__file__), Path(trial.__file__), Path(legacy.__file__), Path(__file__).with_name('local_ai_quality.py')]}})
    supplement, report = acquire(plan, packet, folder, args.plan.parent)
    if args.model:
        result = trial.run(packet, supplement, args.model)
        save('result.json', result)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
