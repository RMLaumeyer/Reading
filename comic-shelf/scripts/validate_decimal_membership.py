"""Audit the isolated live decimal-membership trial without altering its inputs."""
import hashlib
import argparse
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    trials = root/'data/local-ai-trials'
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',default='original-sin-decimal-membership-v1',choices=['original-sin-decimal-membership-v1','original-sin-decimal-reconciliation-v1'])
    args=parser.parse_args()
    run = trials/args.run
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = read(run/'manifest.json')
    assert all(sha(Path(p)) == h for p,h in manifest['inputs'].items())
    assert all(sha(root/'scripts'/p) == h for p,h in manifest['codeSha256'].items())
    baseline = read(trials/'order-evidence-v2-validation/preservation-before.json')
    changed = [p for p,h in baseline.items() if not (root/p).is_file() or sha(root/p) != h]
    assert not changed
    report = read(run/'decimal-membership.json')
    matched = [m for m in report['matches'] if m['membershipCandidates']]
    assert [m['designation']['designator'] for m in matched] == ['3.1','3.2','3.3','3.4']
    assert all(c['existingContentsConflict'] for m in matched for c in m['membershipCandidates'])
    assert report['contentsConflictsCleared'] == report['resolvedIdentitiesAdded'] == 0
    sequences=[]
    for source in sorted(run.glob('source-*')):
        path=read(source/'path.json')
        old=read(trials/'original-sin-discovery-v2-orders'/source.name/'path.json')
        assert [n['issue'] for n in path['orderedIssues']] == [n['issue'] for n in old['orderedIssues']]
        sequences.append({'source':source.name,'positions':len(path['sourceSequence']),
                          'resolved':len(path['orderedIssues']),'sameResolvedSequence':True})
    checks={'decimalPositions':len(report['matches']),'candidatePositions':len(matched),
            'equivalentNumberingSupported':report.get('positionsWithSupportedEquivalentNumbering',0),
            'sequences':sequences,'preservation':{'checked':len(baseline),'changed':changed},
            'scope':'Development evidence matching, no new accepted accuracy or autonomy claim.'}
    with (run/'checks.json').open('x',encoding='utf-8') as stream:
        json.dump(checks,stream,indent=2)
    print(json.dumps(checks,indent=2))


if __name__ == '__main__': main()
