"""Local, resumable enrichment. Conservative extraction; ambiguity stays in a queue."""
import argparse
import copy
import datetime
import html
import json
import msvcrt
import os
import re
import time
import urllib.error
import urllib.request
from enrich_catalog import ROOT, CACHE, AUTO, parse_metadata, write_json
from parse_sources import Page

VERSION = 2
STATE = ROOT/'data/auto-enrichment-state.json'
PAUSE = ROOT/'data/pause-auto-enrichment'

def read(path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default

def normalize(value):
    return re.sub(r'[^a-z0-9]', '', value.lower())

def issue_index(text, aliases):
    """Require an explicit series year, not the export's edition date."""
    keys = []
    for match in re.finditer(r'([A-Za-z][A-Za-z0-9 &.:’\'-]{1,90}?)\s*\((19\d{2}|20\d{2})\)\s*#?\s*(\d+)(?:\s*[-–]\s*(\d+))?', text):
        raw, year, first, last = match.groups()
        raw = re.sub(r'^.*?\b(?:collects|collecting|and|from)\s+', '', raw, flags=re.I).strip()
        candidates=[(name,canonical) for (name,y),canonical in aliases.items() if y==int(year) and normalize(raw).endswith(name)]
        canonical = max(candidates,key=lambda pair:len(pair[0]))[1] if candidates else None
        if not canonical: continue
        # Decimal/suffixed issues and partial material require a person.
        if re.match(r'(?:\.[A-Za-z0-9]|[A-Za-z])', text[match.end():]): continue
        if 'material from' in text[max(0,match.start()-20):match.start()+len(raw)+20].lower(): continue
        a, b = int(first), int(last or first)
        if a > b or b-a > 150: continue
        keys.extend(f'{canonical} ({year}) #{n}' for n in range(a,b+1))
    return sorted(set(keys))

def annotate(book, detail, description, names, aliases, reviews):
    d = copy.deepcopy(detail)
    mentions = [name for name in names if len(name)>3 and re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)', description, re.I)]
    keys = issue_index(description, aliases)
    # These are suggestions, never inserted into the verified appearance or overlap index.
    volume = re.search(r'\bVol(?:ume)?\.?\s*(\d+)\b', book['title'], re.I)
    proposal = None
    if volume:
        prefix = book['title'][:volume.start()].strip(' :,.')
        proposal = dict(name=prefix+' · '+book['author'], position=int(volume[1]), note='Numbered-volume suggestion only. Series identity and crossover gaps need checking.')
    reasons=[]
    if not description: reasons.append('No usable publisher synopsis')
    if not d.get('pages'): reasons.append('Page count missing')
    reasons.append('Story names and character appearances need review')
    if keys: reasons.append('Extracted issue ranges need edition confirmation')
    else: reasons.append('Collected issues could not be matched safely')
    reasons.append('Reading order needs review')
    # Only transfer an existing checked review when both ISBNs have the same
    # complete verified issue index. Automatic issue guesses never qualify.
    signature=tuple(sorted(d.get('issueKeys',[])))
    if not d.get('review') and signature in reviews:
        d['review']=copy.deepcopy(reviews[signature])
        d['review']['match']='Same verified issue set as an already reviewed collection; edition extras may differ.'
    if not d.get('review'): reasons.append('Review score needs an exact collection match')
    candidate=reviews.get(tuple(sorted(keys))) if keys else None
    d['automation']=dict(version=VERSION, characterMentions=mentions, suggestedIssues=keys, suggestedReadingPath=proposal, reviewCandidate=candidate, reasons=reasons)
    return d, reasons

def request(url):
    for attempt in range(2):
        try:
            time.sleep(3)
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PanelPersonalCatalog/1.0 (local personal catalog)'}),timeout=15) as response:
                return response.read().decode('utf-8',errors='replace')
        except urllib.error.HTTPError as exc:
            if exc.code not in (500,502,503,504) or attempt: raise
        except (urllib.error.URLError,TimeoutError,ConnectionError):
            if attempt: raise
        if PAUSE.exists(): raise InterruptedError('Paused')
        time.sleep(3)

def main():
    args=argparse.ArgumentParser(); args.add_argument('--cached-only',action='store_true'); args.add_argument('--retry',action='store_true'); opts=args.parse_args()
    lock=(ROOT/'data/enrichment.lock').open('a+b'); lock.seek(0)
    try: msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:
        print('Another collector is already running.',flush=True); return 2
    catalog=read(ROOT/'public/catalog.json',{})['books']
    payload=read(ROOT/'public/enrichment.json',{}); original=payload['books']
    automatic=read(AUTO,{})
    state=read(STATE,dict(version=VERSION,records={}))
    if state.get('version')!=VERSION: state=dict(version=VERSION,records={})
    records=state['records']
    names=sorted({c['name'] for d in original.values() if d.get('level')!='basic' for c in d.get('characters',[])})
    aliases={}
    reviews={}
    for d in original.values():
        if d.get('level')=='basic': continue
        for key in d.get('issueKeys',[]):
            m=re.match(r'(.+) \((\d{4})\) #',key)
            if m: aliases[(normalize(m[1]),int(m[2]))]=m[1]
        if d.get('review') and d.get('issueKeys'): reviews[tuple(sorted(d['issueKeys']))]=d['review']
    def save(status,message,current=''):
        # State and derived data are saved together in one authoritative checkpoint.
        state['status']=dict(status=status,message=message,current=current,total=len(catalog),processed=len(records),pid=os.getpid(),updatedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
        write_json(STATE,state)
        merged=dict(original)
        for key,record in records.items():
            if original.get(key,{}).get('level')!='basic' and key in original: continue
            if record.get('detail'): merged[key]=record['detail']; automatic[key]=record['detail']
        queue=[dict(id=b['id'],title=b['title'],reasons=records[b['id']]['reasons'],status=records[b['id']]['status']) for b in catalog if b['id'] in records and records[b['id']].get('reasons')]
        import approved_synopses
        merged = approved_synopses.apply(merged, ROOT/'data/approved-synopses.json')
        counts=dict(state['status'],reviewCount=len(queue),pendingLookups=sum(r['status'] in ('pending','error') for r in records.values()),automatic=sum(bool(d.get('automation')) for d in merged.values()),editorial=sum(d.get('level')!='basic' for d in merged.values()))
        write_json(AUTO,automatic)
        for directory in [ROOT/'public',ROOT/'dist/client']:
            if directory.exists():
                write_json(directory/'enrichment.json',dict(updatedAt=datetime.date.today().isoformat(),books=merged))
                write_json(directory/'auto-enrichment-status.json',counts)
                write_json(directory/'review-queue.json',dict(records=queue))
        print(json.dumps(counts),flush=True)
    save('running','Checking saved descriptions first.')
    try:
        # Cache pass always comes first, so remote timeouts cannot delay thousands
        # of records whose source material is already saved locally.
        for index,b in enumerate(catalog):
            if PAUSE.exists(): save('paused','Paused. Saved work will be reused.'); return 0
            key=b['id']; d=original.get(key)
            if d and d.get('level')!='basic':
                reasons=[]
                if not d.get('review'): reasons.append('Review score needs an exact collection match')
                if not d.get('pages'): reasons.append('Page count missing')
                if re.search(r'disput|unconfirmed|excluded|mismatch',d.get('contentsNote',''),re.I): reasons.append('Edition discrepancy needs checking; see collected-issue notes')
                records[key]=dict(status='editorial',reasons=reasons); continue
            if key in records and records[key].get('status')!='pending' and not (opts.retry and records[key].get('status')=='error'): continue
            cached=CACHE/f"google-{b['isbn']}.html"; description=''
            if cached.exists():
                raw=cached.read_text(encoding='utf-8'); matched=parse_metadata(b,raw)
                if matched:
                    d=d or matched; description=html.unescape(Page(raw).meta.get('description',''))
            if d:
                result,reasons=annotate(b,d,description,names,aliases,reviews)
                records[key]=dict(status='processed',detail=result,reasons=reasons)
            else: records[key]=dict(status='pending',reasons=['No exact ISBN metadata match'])
            if index%50==0: save('running','Checking saved descriptions.',b['title'])
        save('running','Saved descriptions checked; looking up missing editions.')
        if not opts.cached_only:
            for b in catalog:
                key=b['id']; record=records[key]
                if record['status']!='pending' and not (opts.retry and record['status']=='error'): continue
                if PAUSE.exists(): save('paused','Paused. Resume to continue missing-edition lookups.'); return 0
                save('running','Looking up missing editions; each result is saved.',b['title'])
                isbn=b['isbn']; errors=[]; d=None; description=''
                if not re.fullmatch(r'\d{13}',isbn):
                    records[key]=dict(status='unmatched',reasons=['No single ISBN-13 in the catalog']); continue
                for source in ('google','openlibrary'):
                    try:
                        if source=='google':
                            cache=CACHE/f'google-{isbn}.html'
                            raw=cache.read_text(encoding='utf-8') if cache.exists() else request('https://books.google.com/books?vid=ISBN'+isbn)
                            if any(s in raw.lower() for s in ('unusual traffic','captcha')):
                                save('paused','Source requested a traffic check. Resume later.'); return 0
                            d=parse_metadata(b,raw)
                            if d: description=html.unescape(Page(raw).meta.get('description','')); cache.write_text(raw,encoding='utf-8')
                        else:
                            cache=CACHE/f'openlibrary-{isbn}.json'; bib='ISBN:'+isbn
                            data=read(cache,None)
                            if data is None:
                                data=json.loads(request('https://openlibrary.org/api/books?bibkeys='+bib+'&format=json&jscmd=data')); write_json(cache,data)
                            item=data.get(bib,{})
                            if isbn in item.get('identifiers',{}).get('isbn_13',[]):
                                url=item.get('url','').replace('http:','https:',1)
                                if not url.startswith('https://openlibrary.org/'): raise ValueError('Unexpected source URL')
                                pages=item.get('number_of_pages'); pages=pages if isinstance(pages,int) and pages>0 else None
                                d=dict(level='basic',summary='Exact ISBN edition matched in Open Library; a story synopsis still needs checking.',pages=pages,pagesSource=url,coverSource=url,checkedAt=datetime.date.today().isoformat(),sources=[dict(label='Open Library · exact ISBN match',url=url)],characters=[],stories=[],issueKeys=[],startingPoint=False,readingPath=dict(name='',position=0,alternative=False,note='Reading order needs checking.'),contentsNote='Edition metadata; story details need review.')
                        if d: break
                    except urllib.error.HTTPError as exc:
                        if exc.code in (401,403,429): save('paused',f'{source} returned HTTP {exc.code}. Resume later; progress is saved.'); return 0
                        if exc.code!=404: errors.append(f'{source}: HTTP {exc.code}')
                    except (OSError,ValueError) as exc: errors.append(f'{source}: {str(exc)[:180]}')
                if d:
                    result,reasons=annotate(b,d,description,names,aliases,reviews); records[key]=dict(status='processed',detail=result,reasons=reasons)
                else: records[key]=dict(status='error' if errors else 'unmatched',reasons=['No exact ISBN metadata match']+errors)
                save('running','Lookup saved.',b['title'])
        save('finished','Automatic pass complete. Items in Needs review still require checking.' if not opts.cached_only else 'Saved-data pass complete. Start enrichment to look up remaining editions.')
        return 0
    except Exception:
        save('paused','Worker stopped unexpectedly. Saved results are safe; resume to continue.')
        raise

if __name__=='__main__': raise SystemExit(main())
