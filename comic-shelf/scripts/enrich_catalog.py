"""Resumable ISBN metadata pass. Keeps editorial annotations separate and intact."""
import argparse
import datetime
import html
import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from parse_sources import Page

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data/cache'
STATE = ROOT / 'data/enrichment-progress.json'
AUTO = ROOT / 'data/automatic-enrichment.json'

def write_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    # Windows readers can briefly prevent replacement while the site refreshes.
    for attempt in range(20):
        try:
            temp.replace(path)
            break
        except PermissionError:
            if attempt == 19: raise
            time.sleep(0.1)

def parse_metadata(book, raw):
    page = Page(raw)
    bib = page.plain.partition('Bibliographic information')[2]
    isbn_section = re.search(r'\bISBN\s+([\d,\sXx-]+)', bib)
    if not isbn_section or book['isbn'] not in re.findall(r'\b\d{13}\b', isbn_section[1]):
        return None
    length = re.search(r'\bLength\s+(\d+)\s+pages', bib)
    url = page.meta.get('og:url', '')
    if not url.startswith('https://books.google.com/'): return None
    description = html.unescape(page.meta.get('description', ''))
    words = description.split()
    excerpt = ' '.join(words[:25]) + (' …' if len(words) > 25 else '')
    if not length and not excerpt: return None
    return dict(
        level='basic', summary=excerpt or 'No synopsis was available for this ISBN.',
        pages=int(length[1]) if length else None, pagesSource=url,
        coverUrl=page.meta.get('og:image'), coverSource=url,
        checkedAt=datetime.date.today().isoformat(),
        sources=[dict(label='Google Books · exact ISBN match; open for full synopsis', url=url)],
        characters=[], stories=[], issueKeys=[], startingPoint=False,
        readingPath=dict(name='', position=0, alternative=False, note='Reading order has not been checked for this book.'),
        contentsNote='Basic ISBN metadata only. Story arcs, appearances, collected issues, and review matches still need checking.',
    )

def publish(automatic, state):
    existing = json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))
    editorial = {k:v for k,v in existing['books'].items() if v.get('level') != 'basic'}
    books = {**automatic, **editorial}
    status = dict(state['summary'], enriched=len(books), fullyChecked=len(editorial), basic=len(automatic))
    write_json(AUTO, automatic)
    write_json(STATE, state)
    payload = dict(updatedAt=datetime.date.today().isoformat(), books=books)
    for directory in [ROOT/'public', ROOT/'dist/client']:
        if directory.exists():
            write_json(directory/'enrichment.json', payload)
            write_json(directory/'enrichment-status.json', status)

def main():
    import msvcrt
    lock = (ROOT/'data/enrichment.lock').open('a+b')
    lock.seek(0)
    try: msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print('Enrichment is already running.'); return
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=4000)
    parser.add_argument('--retry', action='store_true')
    args = parser.parse_args()
    state = json.loads(STATE.read_text()) if STATE.exists() else dict(records={}, summary={})
    automatic = json.loads(AUTO.read_text(encoding='utf-8')) if AUTO.exists() else {}
    catalog = json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books']
    editorial = json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))['books']
    priority = lambda b: bool(re.search(r'spider.man|moon knight|avengers|x.men', b['title'], re.I))
    catalog.sort(key=lambda b: (b['id'] in state['records'], not priority(b), b['title']))
    for b in catalog:
        if b['id'] in editorial and editorial[b['id']].get('level') != 'basic':
            state['records'][b['id']] = dict(status='editorial')
    count = 0
    def save(status, message=''):
        state['summary'] = dict(status=status, message=message, total=len(catalog),
            processed=len(state['records']), priorityTotal=sum(priority(b) for b in catalog),
            priorityProcessed=sum(priority(b) and b['id'] in state['records'] for b in catalog),
            unmatched=sum(v['status']=='unmatched' for v in state['records'].values()),
            errors=sum(v['status']=='error' for v in state['records'].values()),
            updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
        publish(automatic, state)
    save('running')
    try:
        for book in catalog:
            if (ROOT/'data/pause-enrichment').exists():
                save('paused', 'Paused by you. Resume to continue from saved progress.')
                return
            previous = state['records'].get(book['id'])
            if previous and (not args.retry or previous['status'] not in ('error','unmatched')): continue
            if count >= args.limit: break
            cache = CACHE / ('google-' + book['isbn'] + '.html')
            try:
                if not re.fullmatch(r'\d{13}', book['isbn']):
                    state['records'][book['id']] = dict(status='unmatched', reason='No single ISBN-13')
                    continue
                if not cache.exists():
                    time.sleep(3)
                    req = urllib.request.Request('https://books.google.com/books?vid=ISBN'+book['isbn'], headers={'User-Agent':'PanelPersonalCatalog/1.0'})
                    with urllib.request.urlopen(req, timeout=30) as response:
                        raw = response.read().decode('utf-8', errors='replace')
                    if 'unusual traffic' in raw.lower() or 'captcha' in raw.lower():
                        save('paused', 'Source requested a traffic check. No further requests were made.')
                        return
                    cache.write_text(raw, encoding='utf-8')
                detail = parse_metadata(book, cache.read_text(encoding='utf-8'))
                if detail: automatic[book['id']] = detail
                state['records'][book['id']] = dict(status='matched' if detail else 'unmatched')
            except urllib.error.HTTPError as exc:
                if exc.code in (401,403,429):
                    save('paused', f'Source returned HTTP {exc.code}. Resume later; completed work is saved.')
                    return
                state['records'][book['id']] = dict(status='error', reason=str(exc))
            except (OSError, ValueError) as exc:
                state['records'][book['id']] = dict(status='error', reason=str(exc))
            count += 1
            save('running')
            print(f"{len(state['records'])}/{len(catalog)} checked; {len(automatic)} new ISBN matches", flush=True)
        save('finished' if len(state['records']) == len(catalog) else 'paused', 'ISBN pass only; editorial checks remain.')
    except KeyboardInterrupt:
        save('paused', 'Stopped; resume to continue from saved progress.')
    except Exception:
        import traceback
        with (ROOT/'enrichment-error.log').open('a', encoding='utf-8') as log:
            traceback.print_exc(file=log)
        try:
            save('paused', 'Worker stopped unexpectedly. Details saved in enrichment-error.log; resume to continue.')
        except Exception:
            pass
        raise

if __name__ == '__main__': main()
