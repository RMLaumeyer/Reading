"""Try failed ISBN lookups against Open Library without fuzzy edition matches."""
import datetime
import json
import msvcrt
import time
import urllib.request
import urllib.error
from enrich_catalog import ROOT, STATE, AUTO, CACHE, publish, write_json

def fetch_json(req, report, opener=urllib.request.urlopen, sleep=time.sleep):
    for attempt in range(3):
        try:
            with opener(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code not in (500, 502, 503, 504) or attempt == 2: raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == 2: raise
        delay = 10 * (attempt + 1)
        report(f'Open Library connection interrupted. Retrying in {delay} seconds (retry {attempt + 1}/2).')
        sleep(delay)

def main():
    lock = (ROOT/'data/enrichment.lock').open('a+b')
    try: msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print('Another collector is running. Wait for it to finish.', flush=True)
        return
    state = json.loads(STATE.read_text(encoding='utf-8'))
    automatic = json.loads(AUTO.read_text(encoding='utf-8'))
    books = json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books']
    queue = [b for b in books if state['records'].get(b['id'],{}).get('status')=='error'
             and not state['records'][b['id']].get('openLibraryChecked')]
    recovered = 0
    def save(status, message):
        records = state['records'].values()
        state['summary'].update(status=status, message=message,
            errors=sum(r['status']=='error' for r in records),
            updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
        publish(automatic,state)
    try:
        for i,b in enumerate(queue):
            if (ROOT/'data/pause-enrichment').exists():
                save('paused','Open Library pass paused by you.'); return
            save('running',f'Open Library fallback: {i}/{len(queue)} checked; {recovered} recovered this pass.')
            isbn = b['isbn']
            key = 'ISBN:'+isbn
            cache = CACHE/f'openlibrary-{isbn}.json'
            if cache.exists(): data=json.loads(cache.read_text(encoding='utf-8'))
            else:
                time.sleep(2)
                url='https://openlibrary.org/api/books?bibkeys='+key+'&format=json&jscmd=data'
                req=urllib.request.Request(url,headers={'User-Agent':'PanelPersonalCatalog/1.0'})
                data=fetch_json(req, lambda message: save('running',message))
                write_json(cache,data)
            item=data.get(key,{})
            identifiers=item.get('identifiers',{}).get('isbn_13',[])
            if isbn in identifiers:
                source=item.get('url','')
                if source.startswith('http://openlibrary.org/'): source=source.replace('http:','https:',1)
                if not source.startswith('https://openlibrary.org/'): raise ValueError('Unexpected edition source URL')
                pages=item.get('number_of_pages')
                if not isinstance(pages,int) or pages <= 0: pages=None
                automatic[b['id']]=dict(level='basic',summary='Edition matched in Open Library. A story synopsis has not been checked; open the source below for its record.',
                    pages=pages,pagesSource=source,coverUrl=item.get('cover',{}).get('large'),coverSource=source,
                    checkedAt=datetime.date.today().isoformat(),sources=[dict(label='Open Library · exact ISBN edition match',url=source)],
                    characters=[],stories=[],issueKeys=[],startingPoint=False,
                    readingPath=dict(name='',position=0,alternative=False,note='Reading order has not been checked for this book.'),
                    contentsNote='Open Library edition metadata. Story arcs, appearances, reviews and collected issues still need checking.')
                state['records'][b['id']]=dict(status='matched',openLibraryChecked=True,source='Open Library')
                recovered+=1
            else: state['records'][b['id']]['openLibraryChecked']=True
            save('running',f'Open Library fallback: {i+1}/{len(queue)} checked; {recovered} recovered this pass.')
            print(state['summary']['message'],flush=True)
        save('finished',f'Open Library fallback finished: {len(queue)} checked; {recovered} recovered this pass. Unresolved books need another source or manual matching.')
    except Exception as exc:
        save('paused',f'Open Library pass paused: {exc}. Completed results are saved.')
        raise

if __name__=='__main__': main()
