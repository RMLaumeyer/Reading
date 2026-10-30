"""Freeze and run isolated decimal mapping and integer regression checks."""
import hashlib
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    root=Path(__file__).resolve().parents[1]
    trials=root/'data/local-ai-trials'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version',type=int,choices=(1,2),default=1)
    args=parser.parse_args()
    suffix='v'+str(args.version)
    folder=trials/('typed-decimal-'+suffix+'-validation')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    snapshot={str(p.relative_to(root)):sha(p) for parent in (root/'public',root/'data')
              for p in parent.rglob('*') if p.is_file()}
    folder.mkdir(exist_ok=False)
    def save(name,data):
        with (folder/name).open('x',encoding='utf-8') as stream:json.dump(data,stream,indent=2)
    code={p.name:sha(p) for p in (root/'scripts').glob('*.py') if not p.name.startswith('test_')}
    save('freeze.json',{'codeSha256':code,'priorFileSha256':snapshot,
         'expectedDecimalDesignators':['3.1','3.2','3.3','3.4'],
         'scope':'Development regression; expectations derived from saved explicit source evidence, not independent human adjudication.'})
    for event,inputs,name,discover in (
        ('original-sin','original-sin-discovery-v1-three','original-sin-typed-decimal-'+suffix,True),
        ('annihilation','evidence-v3-annihilation-three','annihilation-typed-decimal-regression-'+suffix,False)):
        command=[sys.executable,str(root/'scripts/order_research.py'),'--event',event,
                 '--edition-run',str(trials/inputs),'--name',name]
        if discover:command.append('--discover-guides')
        if discover and args.version==2:command.extend(['--discover-identities','--max-identity-pages','6'])
        subprocess.run(command,cwd=root,check=True)
    findings=[]
    for source in sorted((trials/('original-sin-typed-decimal-'+suffix)).glob('source-*')):
        path=read(source/'path.json');mapped=read(source/'collection-path.json')
        old=read(trials/'original-sin-discovery-v2-orders'/source.name/'path.json')
        decimals=[n for n in path['orderedIssues'] if n['issue'].get('numberKind')=='decimal']
        integers=[n['issue'] for n in path['orderedIssues'] if not n['issue'].get('numberKind')]
        assert integers==[n['issue'] for n in old['orderedIssues']]
        expected=['3.1','3.2','3.3','3.4'] if source.name=='source-1' or args.version==2 else []
        assert [n['issue']['number'] for n in decimals]==expected
        placements=[n for n in mapped['nodes'] if n['issue'].get('numberKind')=='decimal']
        assert all(n['coverageState']=='identity_review' for n in placements)
        assert not mapped['completeReadingOrder'] and not mapped['eligibleForPublication']
        findings.append({'source':source.name,'sourcePositions':len(path['sourceSequence']),
                         'resolved':len(path['orderedIssues']),'typedDecimalDrafts':len(decimals),
                         'decimalDraftPlacements':len(placements),'coverage':mapped['coverage']})
    regression=[]
    for source in sorted((trials/('annihilation-typed-decimal-regression-'+suffix)).glob('source-*')):
        new=read(source/'path.json');old=read(trials/'order-evidence-v4-annihilation'/source.name/'path.json')
        assert [n['issue'] for n in new['orderedIssues']]==[n['issue'] for n in old['orderedIssues']]
        regression.append({'source':source.name,'resolved':len(new['orderedIssues']),'sameSequence':True})
    changed=[p for p,h in snapshot.items() if not (root/p).is_file() or sha(root/p)!=h]
    assert not changed
    assert all(sha(root/'scripts'/p)==h for p,h in code.items())
    if args.version==2:
        original=trials/('original-sin-typed-decimal-'+suffix)
        comparisons=read(original/'report.json')['comparisons']
        assert comparisons[0]['commonIssueCount']==13 and len(comparisons[0]['orderConflicts'])==4
        tasks=read(original/'research-tasks.json')
        assert len([t for t in tasks if t['kind']=='reading_order_disagreement'])==4
    report={'originalSin':findings,'annihilation':regression,
            'preservation':{'checked':len(snapshot),'changed':changed},
            'completeReadingOrderEstablished':False,'unaidedAccuracyEstablished':False}
    save('checks.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
