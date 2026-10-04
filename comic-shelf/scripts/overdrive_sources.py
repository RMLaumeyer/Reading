"""Two-step public ISBN lookup; no login, private API or search-engine scraping."""
import datetime
import hashlib
import json
import re
import urllib.request
from urllib.parse import urlsplit, parse_qs, urljoin
from html.parser import HTMLParser

from parse_sources import Page


def check_url(url):
    p = urlsplit(url)
    if (p.scheme != 'https' or p.hostname not in ('www.overdrive.com', 'knoxcounty.overdrive.com')
            or p.username or p.password or p.port not in (None, 443) or p.fragment):
        raise ValueError('Unsupported public catalog URL')
    if re.fullmatch(r'/media/\d+(?:/[a-z0-9-]+)?/?', p.path) and not p.query:
        return url
    if p.hostname == 'www.overdrive.com' and p.path == '/search':
        q = parse_qs(p.query)
        if set(q) == {'q'} and len(q['q']) == 1 and re.fullmatch(r'\d{13}', q['q'][0]):
            return url
    raise ValueError('Only public ISBN search and media pages are supported')


class Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 3

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    check_url(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'ComicShelfResearch/0.1 (personal metadata research)'})
    with urllib.request.build_opener(Redirects).open(req, timeout=25) as response:
        check_url(response.url)
        if response.headers.get_content_type() != 'text/html':
            raise ValueError('Expected public catalog HTML')
        body = response.read(3_000_001)
        if len(body) > 3_000_000:
            raise ValueError('Public catalog page exceeds limit')
        return body, response.url, response.headers.get_content_charset() or 'utf-8'


def parse_record(raw, url, isbn):
    check_url(url)
    media = re.fullmatch(r'/media/(\d+)(?:/[a-z0-9-]+)?/?', urlsplit(url).path)
    matches = list(re.finditer(r'window\.OverDrive\.mediaItems\s*=\s*', raw))
    if not media or len(matches) != 1:
        raise ValueError('Missing unique public media record')
    # Parse JSON data only. Never execute scripts or consume site API keys.
    records, _ = json.JSONDecoder().raw_decode(raw[matches[0].end():])
    record = records.get(media[1]) if isinstance(records, dict) else None
    if not isinstance(record, dict) or str(record.get('id')) != media[1]:
        raise ValueError('Page and media identity differ')
    formats = record.get('formats', [])
    evidence = []
    for index, fmt in enumerate(formats):
        if not isinstance(fmt, dict):
            continue
        for identifier in fmt.get('identifiers', []):
            if isinstance(identifier, dict) and identifier.get('type') == 'ISBN' and identifier.get('value') == isbn:
                evidence.append({'path': f'mediaItems.{media[1]}.formats[{index}].identifiers', 'identifier': isbn})
    if not evidence:
        raise ValueError('Requested ISBN is not in this media record formats')
    description, series = record.get('description'), record.get('series', '')
    if not isinstance(description, str) or not 1 <= len(description) <= 12000 or not isinstance(series, str) or len(series) > 300:
        raise ValueError('Missing or oversized description')
    clean = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', description, flags=re.S | re.I)
    text = ' '.join(Page(clean).plain.split())
    if not text or len(text) > 7000:
        raise ValueError('No bounded description text')
    return {'id': 'OD1', 'url': url, 'kind': 'OverDrive public edition metadata',
            'text': 'Synopsis: '+text+'\nBibliographic information: ISBN '+isbn+' Series '+series,
            'description': text, 'editionIsbn': isbn, 'isbnEvidence': evidence, 'seriesLabel': series,
            'seriesEvidencePath': f'mediaItems.{media[1]}.series',
            'cacheSha256': hashlib.sha256(raw.encode('utf-8')).hexdigest()}


def acquire(isbn, folder, fetch=download):
    if not re.fullmatch(r'\d{13}', isbn):
        raise ValueError('Use a 13-digit ISBN')
    folder.mkdir(exist_ok=False)
    audit = {'isbn': isbn, 'retrievedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'requests': []}
    try:
        url = 'https://www.overdrive.com/search?q='+isbn
        audit['requests'].append({'url': url, 'state': 'attempted'})
        body, final, encoding = fetch(url)
        check_url(final)
        (folder / 'search.html').write_bytes(body)
        audit['requests'][-1].update(state='downloaded', finalUrl=final, sha256=hashlib.sha256(body).hexdigest())
        media = re.fullmatch(r'/media/(\d+)(?:/[a-z0-9-]+)?/?', urlsplit(final).path)
        ids = [media[1]] if media else candidate_ids(body.decode(encoding), final)
        accepted = []
        for media_id in ids:
            url = 'https://knoxcounty.overdrive.com/media/'+media_id
            audit['requests'].append({'url': url, 'state': 'attempted'})
            body, final, encoding = fetch(url)
            check_url(final)
            if urlsplit(final).path.rstrip('/') != '/media/'+media_id:
                raise ValueError('Media lookup redirected to a different record')
            filename = 'media.html' if len(ids) == 1 else f'media-{media_id}.html'
            (folder / filename).write_bytes(body)
            audit['requests'][-1].update(state='downloaded', finalUrl=final, sha256=hashlib.sha256(body).hexdigest())
            try:
                accepted.append(parse_record(body.decode(encoding), final, isbn))
            except (ValueError, TypeError, LookupError):
                audit['requests'][-1]['recordValidation'] = 'rejected'
            else:
                audit['requests'][-1]['recordValidation'] = 'isbn_matched'
        source = reconcile_records(accepted)
        audit['state'] = 'accepted'
        return source
    except (OSError, ValueError, LookupError, TypeError) as exc:
        audit.update(state='failed', errorType=type(exc).__name__, httpStatus=getattr(exc, 'code', None))
        return None
    finally:
        with (folder / 'acquisition.json').open('x', encoding='utf-8') as stream:
            json.dump(audit, stream, indent=2)


def reconcile_records(records):
    """Collapse duplicate ISBN records only when their substantive text agrees."""
    if not records:
        raise ValueError('No validated ISBN record')
    ordered = sorted(records, key=lambda source: len(source['description']))
    source = dict(ordered[0])
    for other in ordered[1:]:
        if other['seriesLabel'] != source['seriesLabel'] or other['editionIsbn'] != source['editionIsbn']:
            raise ValueError('Conflicting ISBN metadata')
        base, extended = source['description'], other['description']
        if extended == base:
            continue
        # Some distributor records append credits/legal boilerplate. Require an
        # exact shared synopsis and recognizable credits, never fuzzy similarity.
        tail = extended[len(base):] if extended.startswith(base) else ''
        if not (tail.startswith(' Author: ') and ' Illustrator: ' in tail
                and 'All rights reserved.' in tail and not re.search(r'\bcollects?\b|#\d', tail, re.I)):
            raise ValueError('Conflicting ISBN descriptions')
    if len(ordered) > 1:
        source['equivalentRecords'] = [
            {key: item[key] for key in ('url', 'cacheSha256', 'isbnEvidence')}
            for item in ordered]
        source['recordAgreement'] = 'Exact synopsis and series; optional trailing credits/legal text'
    return source


def candidate_ids(raw, url):
    """Read a bounded public catalog result list; titles alone never select a book."""
    if urlsplit(url).hostname != 'www.overdrive.com' or urlsplit(url).path != '/search':
        raise ValueError('Expected public ISBN result list')
    check_url(url)
    class Links(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.ids = []

        def handle_starttag(self, tag, attrs):
            if tag != 'a':
                return
            target = urljoin(url, dict(attrs).get('href', ''))
            try:
                check_url(target)
            except ValueError:
                return
            match = re.fullmatch(r'/media/(\d+)(?:/[a-z0-9-]+)?/?', urlsplit(target).path)
            if match and match[1] not in self.ids:
                self.ids.append(match[1])
    parser = Links()
    parser.feed(raw)
    if not 1 <= len(parser.ids) <= 3:
        raise ValueError('No bounded unambiguous candidate set; manual discovery required')
    return parser.ids
