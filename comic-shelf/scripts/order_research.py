"""Acquire registered reading guides, map editions, and report disagreements."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import datetime

import cbro_order
import collection_path
import guide_order
import series_references
import order_identity
import order_sources
import order_discovery

REGISTRY = {'annihilation': [
    {'adapter': 'marvelguides', 'url': 'https://marvelguides.com/annihilation-reading-order',
     'sections': ['Part 5.2: Road to Annihilation', 'Part 5.3: Annihilation']},
    {'adapter': 'cbro', 'url': 'https://comicbookreadingorders.com/marvel/events/annihilation-reading-order/'}],
    'black-vortex': [
    {'adapter':'marvelguides','url':'https://marvelguides.com/black-vortex-reading-order',
     'sections':['Part 9.2: The Black Vortex']},
    {'adapter':'cbro','url':'https://comicbookreadingorders.com/marvel/events/black-vortex-reading-order/'}]}


def identity(node):
    issue = node['issue']
    return series_references.name_key(issue['series']), issue['year'], issue['number']


def compare(left, right):
    a, b = [identity(n) for n in left['orderedIssues']], [identity(n) for n in right['orderedIssues']]
    if len(a) != len(set(a)) or len(b) != len(set(b)): raise ValueError('Ambiguous repeated identity')
    common = set(a) & set(b)
    a_shared, b_shared = [k for k in a if k in common], [k for k in b if k in common]
    rank = {k: i for i, k in enumerate(b_shared)}
    conflicts = [{'first': x, 'second': y} for i, x in enumerate(a_shared)
                 for y in a_shared[i+1:] if rank[x] > rank[y]]
    identity_disagreements = [{'left':x,'right':y} for x in a for y in b
                              if x[0]==y[0] and x[2]==y[2] and x[1]!=y[1]]
    source_problems = bool(left.get('problems') or right.get('problems')
                           or left['state'] != 'draft' or right['state'] != 'draft')
    return {'sources': [left['sourceUrl'], right['sourceUrl']], 'commonIssueCount': len(common),
            'sameRelativeOrderOnSharedIssues': bool(common) and not conflicts and not source_problems,
            'orderConflicts': conflicts,
            'identityDisagreements':identity_disagreements,
            'onlyLeft': [n for n in left['orderedIssues'] if identity(n) not in common],
            'onlyRight': [n for n in right['orderedIssues'] if identity(n) not in common],
            'sourceProblemsPresent': source_problems,
            'state': 'needs_review' if conflicts or source_problems or set(a) != set(b) or not common else 'agreement_on_listed_issues',
            'completeReadingOrder': False, 'requiredReadingEstablished': False,
            'note': 'Agreement does not establish source independence, completeness, or required prerequisites. Differences remain evidence; no automatic merged order.'}


def research_tasks(paths, edition_warnings):
    """Keep a finite, evidence-linked work list without inventing identity answers."""
    tasks = [{'kind':'edition_identity_disagreement','priority':1,'evidence':warning,
              'action':'Find dated original-series evidence and verify target ISBN contents; do not pick a year by majority.'}
             for warning in edition_warnings]
    grouped = {}
    for path in paths:
        for slot in path.get('sourceSequence',[]):
            if slot.get('identityState')=='resolved':continue
            issue=slot.get('issue')
            label=issue['series'] if issue else slot['quote']
            key=(series_references.name_key(label),issue['number'] if issue else None)
            task=grouped.setdefault(key,{'kind':'series_identity' if issue else 'unsupported_source_row',
                'priority':2 if issue else 3,'sourceLabel':label,'issueNumber':issue['number'] if issue else None,
                'evidence':[],'action':'Acquire explicit dated identity or alias evidence; retain original source position.'})
            task['evidence'].append({'url':path['sourceUrl'],'position':slot['position'],
                                     'quote':slot['quote'],'state':slot['identityState']})
    tasks.extend(grouped.values())
    return tasks


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--event', required=True)
    cli.add_argument('--edition-run', type=Path, required=True)
    cli.add_argument('--name', required=True)
    cli.add_argument('--discover-identities',action='store_true',help='Bounded live ISBN research using related local catalog entries')
    cli.add_argument('--max-identity-pages',type=int,default=6)
    cli.add_argument('--discover-guides',action='store_true',help='Look up exact event pages in public indexes; Marvel Guides uses full-page scope')
    args = cli.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,60}', args.name): cli.error('Use a unique safe run name')
    if not 0 <= args.max_identity_pages <= 12: cli.error('Use an identity-page budget from zero to twelve')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.event) or len(args.event)>80:cli.error('Use a lowercase event slug')
    if not args.discover_guides and args.event not in REGISTRY:cli.error('Unregistered event; use --discover-guides')
    root = Path(__file__).resolve().parents[1]
    folder = root/'data/local-ai-trials'/args.name
    folder.mkdir(exist_ok=False)
    def save(path, data):
        with path.open('x', encoding='utf-8') as f: json.dump(data, f, indent=2, ensure_ascii=False)
    editions, references, hashes = [], [], {}
    for file in sorted(args.edition_run.glob('*/result.json')):
        packet_file = file.parent/'packet.json'
        packet = json.loads(packet_file.read_text(encoding='utf-8'))
        references.extend(packet.get('seriesIdentityReferences', []))
        editions.append({'isbn': packet['book']['isbn'], 'title': packet['book']['title'],
                         'result': json.loads(file.read_text(encoding='utf-8'))})
        for p in (file, packet_file): hashes[str(p.resolve())] = hashlib.sha256(p.read_bytes()).hexdigest()
    if not editions: raise ValueError('No saved edition drafts')
    editions, identity_warnings = order_identity.audit_editions(editions)
    save(folder/'edition-identity-audit.json', {'warnings': identity_warnings,
         'note': 'Scoped cross-edition discrepancies; no year corrected and no original edition result modified.'})
    discovery_report=[]
    if args.discover_guides:
        sources,discovery_report=order_discovery.acquire(args.event,folder/'guide-discovery')
    else:
        sources=REGISTRY[args.event]
    save(folder/'manifest.json', {'event': args.event, 'sources': sources, 'inputs': hashes,
         'codeSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),
             Path(cbro_order.__file__), Path(guide_order.__file__), Path(collection_path.__file__), Path(series_references.__file__), Path(order_identity.__file__),
             Path(order_sources.__file__),Path(order_sources.edition_sources.__file__),Path(order_sources.edition_trial.__file__),Path(order_discovery.__file__)]},
         'identityDiscoveryRequested':args.discover_identities,'maxIdentityPages':args.max_identity_pages,
         'discoveryMode': 'Exact event lookup in public indexes' if args.discover_guides else 'Registered public sources; no general web discovery'})
    paths, failures, extracted = [], [], []
    for index, source in enumerate(sources, 1):
        target = folder/f'source-{index}'; target.mkdir()
        adapter = guide_order if source['adapter'] == 'marvelguides' else cbro_order
        acquisition = {'url':source['url'],'stage':'download','state':'attempted',
                       'retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            body, url, encoding = adapter.download(source['url'])
            (target/'source.html').write_bytes(body)
            acquisition.update(stage='parse',downloaded=True,sha256=hashlib.sha256(body).hexdigest(),finalUrl=url)
            raw=body.decode(encoding)
            sections=(adapter.sections_with_lists(raw) if source.get('sectionSelection')=='all_explicit_reading_lists'
                      else source.get('sections'))
            path = (adapter.parse(raw, url, sections, references)
                    if adapter is guide_order else adapter.parse(body.decode(encoding), url))
            path['selectionMode']=source.get('sectionSelection','registered_source_scope')
            path['sha256'] = hashlib.sha256(body).hexdigest()
            save(target/'extracted-path.json', path)
            extracted.append((target,path))
            acquisition.update(state='parsed',observedPositions=len(path.get('sourceSequence',path['orderedIssues'])))
        except (OSError, ValueError, LookupError) as exc:
            failure = {'url': source['url'], 'stage':acquisition['stage'],'errorType': type(exc).__name__, 'httpStatus': getattr(exc, 'code', None)}
            failures.append(failure); save(target/'error.json', failure)
            acquisition.update(state='failed',errorType=type(exc).__name__,httpStatus=getattr(exc,'code',None))
        finally:
            save(target/'acquisition.json',acquisition)
    identity_sources = []
    if args.discover_identities:
        catalog_file = root/'public/catalog.json'
        books = json.loads(catalog_file.read_text(encoding='utf-8'))['books']
        save(folder/'catalog-input.json',{'sha256':hashlib.sha256(catalog_file.read_bytes()).hexdigest()})
        unresolved_paths = [order_identity.resolve(p,editions) for _,p in extracted]
        plan = order_sources.plan(unresolved_paths,books,[e['isbn'] for e in editions],args.max_identity_pages,
                                  event_label=args.event.replace('-',' '))
        identity_sources = order_sources.acquire(plan,books,folder/'identity-discovery')
    for target, path in extracted:
        try:
            path = order_identity.resolve(path, editions, identity_sources)
            save(target/'path.json',path)
            save(target/'collection-path.json',collection_path.build(path,editions))
            paths.append(path)
        except (ValueError,KeyError,TypeError) as exc:
            failure={'url':path['sourceUrl'],'stage':'identity_mapping','errorType':type(exc).__name__}
            failures.append(failure);save(target/'mapping-error.json',failure)
    comparisons = [compare(a, b) for i, a in enumerate(paths) for b in paths[i+1:]]
    tasks = research_tasks(paths,identity_warnings)
    save(folder/'research-tasks.json',tasks)
    report = {'acquiredSources': len(paths), 'failures': failures, 'comparisons': comparisons,
              'guideDiscovery':discovery_report,
              'editionIdentityWarnings': identity_warnings,
              'researchTaskCount':len(tasks),
              'state': 'needs_review' if identity_warnings or failures or not comparisons or any(c['state'] == 'needs_review' for c in comparisons) else 'agreement_on_listed_issues',
              'eligibleForPublication': False}
    save(folder/'report.json', report)
    print(json.dumps({'acquiredSources': len(paths), 'failures': failures, 'state': report['state'],
                     'comparisons': [{'shared': c['commonIssueCount'], 'orderConflicts': len(c['orderConflicts']),
                                      'onlyLeft': len(c['onlyLeft']), 'onlyRight': len(c['onlyRight'])} for c in comparisons]}))


if __name__ == '__main__': main()
