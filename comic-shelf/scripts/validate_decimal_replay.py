"""Exclusive saved-source regression audit; never modifies prior results."""
import hashlib
import json
from pathlib import Path
import guide_order
import cbro_order


def main():
    root = Path(__file__).resolve().parents[1]
    trials = root / 'data/local-ai-trials'
    output = trials / 'decimal-designators-v1-validation'
    output.mkdir(exist_ok=False)
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    baseline = read(trials / 'order-evidence-v2-validation/preservation-before.json')
    rows = []
    for name in ('original-sin-discovery-v2-orders', 'order-evidence-v6-black-vortex', 'order-evidence-v4-annihilation'):
        for source in sorted((trials / name).glob('source-*')):
            old = read(source / 'extracted-path.json')
            raw = (source / 'source.html').read_text(encoding='utf-8')
            # These extraction stages used no publisher identity reference rows.
            references = []
            manifest = read(trials / name / 'manifest.json')
            for filename in manifest['inputs']:
                if Path(filename).name == 'packet.json':
                    references.extend(read(Path(filename)).get('seriesIdentityReferences', []))
            new = (guide_order.parse(raw, old['sourceUrl'], old['selectedSections'], references)
                   if 'marvelguides.com' in old['sourceUrl'] else cbro_order.parse(raw, old['sourceUrl']))
            assert new['orderedIssues'] == old['orderedIssues']
            assert len(new['sourceSequence']) == len(old['sourceSequence'])
            decimals = [s for s in new['sourceSequence'] if s.get('unsupportedIssueDesignation')]
            assert all(s['issue'] is None and s['identityState'] == 'unsupported' for s in decimals)
            (output / (name + '-' + source.name + '.json')).write_text(json.dumps(new, indent=2), encoding='utf-8')
            rows.append({'run': name, 'source': source.name, 'sourcePositions': len(new['sourceSequence']),
                         'decimalPositionsCaptured': len(decimals), 'resolvedSequenceUnchanged': True})
    changed = [n for n,h in baseline.items() if not (root/n).is_file() or sha(root/n) != h]
    assert not changed
    result = {'replays': rows, 'preservation': {'checked': len(baseline), 'changed': changed},
              'codeSha256': {p.name: sha(p) for p in (root/'scripts').glob('*.py') if not p.name.startswith('test_')},
              'scope': 'Structured capture and regression only; no new resolved identities or accuracy claims.'}
    (output/'checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'replays': rows, 'preservation': result['preservation']}, indent=2))


if __name__ == '__main__':
    main()
