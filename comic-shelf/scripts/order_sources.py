"""Bounded ISBN-based identity research from catalog candidates, never membership."""
import datetime
import hashlib
import json
import re

import edition_sources
import edition_trial
from series_references import name_key


def lookup_name(name):
    # Volume suffix removal is only a query expansion, never an accepted alias.
    return re.sub(r'\s+Vol\.\s*\d+$', '', name, flags=re.I).strip()


def plan(paths, books, excluded_isbns=(), max_pages=6, event_label=''):
    if not 0 <= max_pages <= 12: raise ValueError('Use an identity-page budget from zero to twelve')
    wanted = {}
    for path in paths:
        for slot in path.get('sourceSequence', []):
            issue = slot.get('issue')
            if not issue or slot.get('identityState') not in ('unresolved','conflict'): continue
            label = lookup_name(issue['series'])
            group = wanted.setdefault(name_key(label), {'lookupLabel': label, 'sourceLabels': [], 'numbers': set()})
            if issue['series'] not in group['sourceLabels']: group['sourceLabels'].append(issue['series'])
            group['numbers'].add(issue['number'])
    groups = []
    for key, target in sorted(wanted.items()):
        candidates = []
        seen = set()
        for book in books:
            isbn = book.get('isbn','')
            if not re.fullmatch(r'\d{13}',isbn) or isbn in excluded_isbns or isbn in seen: continue
            title = book.get('title','')
            title_series = re.split(r'\s+Vol\.\s*\d+', title, maxsplit=1, flags=re.I)[0]
            if name_key(title_series) != key: continue
            match = re.search(r'Issues\s+#(\d+)(?:-(\d+))?',title,re.I)
            if not match: continue
            first,last = int(match[1]),int(match[2] or match[1])
            if last<first: continue
            distance = min(max(first-number,number-last,0) for number in target['numbers'])
            candidates.append({'isbn':isbn,'title':title,'catalogRange':[first,last],'distance':distance})
            seen.add(isbn)
        candidates.sort(key=lambda c:(c['distance'],c['isbn']))
        groups.append({**target,'numbers':sorted(target['numbers']),'candidates':candidates})
    groups.sort(key=lambda g:(not any(name_key(s)==name_key(g['lookupLabel']) for s in g['sourceLabels']), name_key(g['lookupLabel'])))
    selected, selected_isbns = [], set()
    # Breadth first: one candidate per label before a second; never unlimited crawling.
    for rank in range(2):
        for group in groups:
            if len(selected) >= max_pages: break
            if rank >= len(group['candidates']): continue
            candidate = group['candidates'][rank]
            if candidate['isbn'] in selected_isbns: continue
            selected.append({**candidate,'lookupLabel':group['lookupLabel'],'sourceLabels':group['sourceLabels']})
            selected_isbns.add(candidate['isbn'])
    return {'groups':groups,'selected':selected,'maxPages':max_pages,'eventLabel':event_label,
            'scope':'Candidate discovery only. Title/range matching and volume stripping do not prove series identity.'}


def acquire(plan_data, books, folder, fetch=edition_sources.download_edition):
    selected = plan_data['selected']
    if (not 0 <= plan_data['maxPages'] <= 12 or len(selected)>plan_data['maxPages']
            or len({c['isbn'] for c in selected}) != len(selected)
            or any(not re.fullmatch(r'\d{13}',c['isbn']) for c in selected)):
        raise ValueError('Invalid bounded identity acquisition plan')
    folder.mkdir(exist_ok=False)
    by_isbn = {b['isbn']:b for b in books if b.get('isbn')}
    sources, audit = [], []
    def save(path,data):
        with path.open('x',encoding='utf-8') as stream: json.dump(data,stream,indent=2,ensure_ascii=False)
    save(folder/'plan.json',plan_data)
    for candidate in plan_data['selected']:
        isbn = candidate['isbn']
        row = {'isbn':isbn,'state':'attempted','retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        audit.append(row)
        target = folder/isbn; target.mkdir()
        try:
            body,url,encoding = fetch(isbn)
            (target/'source.html').write_bytes(body)
            packet = edition_sources.packet_from_html(by_isbn[isbn],body.decode(encoding))
            save(target/'packet.json',packet)
            if not packet['constraints'].get('isbnMatched') or packet['constraints'].get('contentsConflict'):
                row['state']='isbn_or_contents_unverified'; continue
            event_words = re.findall(r'[a-z0-9]+',plan_data.get('eventLabel','').casefold())
            synopsis = packet['sources'][0]['text'].partition('Bibliographic information:')[0]
            synopsis_words = ' '.join(re.findall(r'[a-z0-9]+',synopsis.casefold()))
            event_phrase = ' '.join(event_words)
            if not event_phrase or not re.search(r'(?<!\w)'+re.escape(event_phrase)+r'(?!\w)',synopsis_words):
                row['state']='event_context_unverified'; continue
            contents = edition_trial.inventory(packet)
            entries = [e for e in contents['entries'] if not e.get('identityResolution')
                       and name_key(e['series']) == name_key(candidate['lookupLabel'])]
            evidence = {'isbn':isbn,'url':url,'sha256':hashlib.sha256(body).hexdigest(),'entries':entries,
                        'sourceLabels':candidate['sourceLabels'],
                        'eventContext':{'label':plan_data['eventLabel'],'quote':synopsis},
                        'scope':'Other-edition series identity evidence only; no target-edition membership or volume alias established.'}
            save(target/'identity-evidence.json',evidence)
            if entries: sources.append(evidence)
            row.update(state='explicit_identity_evidence' if entries else 'no_explicit_dated_range',entries=len(entries))
        except (OSError,ValueError,TypeError,LookupError) as exc:
            row.update(state='failed',errorType=type(exc).__name__,httpStatus=getattr(exc,'code',None))
            if row['httpStatus'] in (403,429,503): break
        finally:
            save(target/'acquisition.json',row)
    save(folder/'report.json',audit)
    save(folder/'evidence.json',sources)
    return sources
