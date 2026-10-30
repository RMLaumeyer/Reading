"""Bounded ISBN acquisition for unresolved event decimal issues."""
import datetime
import json
import re
import edition_sources
import overdrive_sources


def plan(paths, books, event, excluded=(), budget=2):
    if not 0 <= budget <= 2:
        raise ValueError('Decimal discovery budget must be zero to two ISBNs')
    unresolved = [s for p in paths for s in p.get('sourceSequence', [])
                  if s.get('unsupportedIssueDesignation') and s.get('identityState') != 'resolved']
    if not unresolved:
        return []
    event_words=re.findall(r'[a-z0-9]+',event.casefold())
    if not event_words:
        raise ValueError('Missing event context')
    candidates=[]
    for book in books:
        isbn=book.get('isbn','')
        title_words=re.findall(r'[a-z0-9]+',book.get('title','').casefold())
        if (not re.fullmatch(r'\d{13}',isbn) or isbn in excluded
                or title_words[:len(event_words)] != event_words):
            continue
        if isbn not in {c['isbn'] for c in candidates}:
            candidates.append(book)
    return sorted(candidates,key=lambda b:b['isbn'])[:budget]


def acquire(candidates, folder, google=edition_sources.download_edition,
            distributor=overdrive_sources.acquire):
    if (len(candidates)>2 or len({b['isbn'] for b in candidates})!=len(candidates)
            or any(not re.fullmatch(r'\d{13}',b.get('isbn','')) for b in candidates)):
        raise ValueError('Unbounded or duplicate decimal candidate plan')
    folder.mkdir(exist_ok=False)
    def save(path,value):
        with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,indent=2)
    save(folder/'plan.json',[{'isbn':b['isbn'],'title':b.get('title')} for b in candidates])
    packets=[];audit=[]
    for book in candidates:
        target=folder/book['isbn'];target.mkdir()
        row={'isbn':book['isbn'],'state':'attempted','retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            body,url,encoding=google(book['isbn'])
            (target/'source.html').write_bytes(body)
            extra=distributor(book['isbn'],target/'overdrive')
            packet,_,_=edition_sources.prepare(book,body.decode(encoding),[extra] if extra else [])
            if not packet['constraints'].get('isbnMatched'):
                row['state']='google_isbn_unverified'
            else:
                packets.append(packet);save(target/'packet.json',packet)
                row['state']='packet_acquired'
        except (OSError,ValueError,LookupError,TypeError) as exc:
            row.update(state='failed',errorType=type(exc).__name__,httpStatus=getattr(exc,'code',None))
        audit.append(row);save(target/'acquisition.json',row)
        if row.get('httpStatus') in (403,429,503):break
    save(folder/'report.json',audit)
    return packets
