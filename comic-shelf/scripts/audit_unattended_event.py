"""Audit the completed event smoke run; write a new review artifact only."""
import hashlib
import argparse
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',choices=('checks.json','checks-corrected.json'),default='checks.json')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1];trials=root/'data/local-ai-trials'
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    run=trials/'original-sin-unattended-v2';manifest=read(run/'manifest.json')
    assert all(sha(root/'scripts'/name)==h for name,h in manifest['codeSha256'].items())
    assert sha(root/'public/catalog.json')==manifest['catalogSha256']
    stage_report=read(run/'report.json')
    assert len(stage_report['stages'])==2 and all(s['exitCode']==0 for s in stage_report['stages'])
    editions=[]
    for isbn in (b['isbn'] for b in manifest['selection']['selected']):
        folder=trials/manifest['editionRun']/isbn
        result=read(folder/'result.json');packet=read(folder/'packet.json')
        assert result['characters']['state']=='not_requested'
        assert not result['readyForPublication']
        assert packet['constraints']['isbnMatched']
        entries=result['contents']['entries']
        editions.append({'isbn':isbn,'inventoryUnits':sum(e['last']-e['first']+1 for e in entries),
            'contentsConflict':bool(result['contents'].get('conflict')),
            'stageErrorNames':list(result['stageErrors']),
            'unresolvedInventoryEntries':len(result['contents'].get('unresolvedEntries',[])),
            'namedStories':len(result.get('namedStories',[])),
            'editionStoryHighlights':len(result.get('featuredStoryHighlights',[]))})
    orders=trials/manifest['orderRun'];order_manifest=read(orders/'manifest.json')
    assert all(sha(Path(p))==h for p,h in order_manifest['inputs'].items())
    assert all(sha(root/'scripts'/p)==h for p,h in order_manifest['codeSha256'].items())
    paths=[]
    for source in sorted(orders.glob('source-*')):
        path=read(source/'path.json');mapped=read(source/'collection-path.json')
        assert not mapped['eligibleForPublication'] and not mapped['completeReadingOrder']
        paths.append({'source':source.name,'coverage':mapped['coverage'],
                      'decimalDraftPlacements':sum(n['issue'].get('numberKind')=='decimal' for n in mapped['nodes']),
                      'unresolvedSourcePositions':mapped['unresolvedSourcePositions']})
    comparison=read(orders/'report.json')['comparisons'][0]
    tasks=read(orders/'research-tasks.json')
    conflicts=[t for t in tasks if t['kind']=='reading_order_disagreement']
    assert comparison['commonIssueCount']==13 and len(comparison['orderConflicts'])==len(conflicts)==4
    prior=read(trials/'typed-decimal-v2-validation/freeze.json')['priorFileSha256']
    changed=[p for p,h in prior.items() if not (root/p).is_file() or sha(root/p)!=h]
    assert not changed
    result={'editionCount':len(editions),'editions':editions,'readingPaths':paths,
            'sharedIdentities':13,'orderConflicts':4,'orderConflictResearchTasks':len(conflicts),
            'preservation':{'checked':len(prior),'changed':changed},
            'scope':'Unattended acquisition smoke and development evidence matching; no independent accuracy score.',
            'unaidedEnrichmentReady':False,'eligibleForPublication':False}
    with (run/args.output).open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('editions','readingPaths')},indent=2))


if __name__=='__main__':main()
