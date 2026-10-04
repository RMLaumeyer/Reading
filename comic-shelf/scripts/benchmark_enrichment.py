"""Frozen-packet highlight evaluation; gold is never passed to model extraction."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import time

import edition_highlights
import local_ai_trial as legacy


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)


def score(packet, highlights, facts):
    sources = {s['id']: s['text'] for s in packet['sources']}
    grounded = [h for h in highlights if h.get('source') in sources
                and isinstance(h.get('quote'), str) and bool(h['quote'])
                and h['quote'] in sources[h['source']] and h.get('description') == h['quote']
                and h.get('editionIsbn') == packet['book']['isbn']]
    recovered = []
    for fact in facts:
        if any(all(term.casefold() in h['quote'].casefold() for term in alternative)
               for alternative in fact['alternatives'] for h in grounded):
            recovered.append(fact['id'])
    return {'emitted': len(highlights), 'grounded': len(grounded),
            'sourceGroundingPrecision': len(grounded)/len(highlights) if highlights else None,
            'centralFactsExpected': len(facts), 'centralFactsRecovered': recovered,
            'centralFactRecall': len(recovered)/len(facts) if facts else None,
            'placeholderArtifacts': sum('[Author]' in h.get('description', '') for h in highlights),
            'unestablishedScopeClaims': sum(bool(h.get('coveredIssues')) or bool(h.get('officialStoryTitle'))
                                           or h.get('completeStoryScopeEstablished') is True for h in highlights)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', type=Path, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--model', default='qwen3.5-4b')
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--extractor', type=Path, help='Optional preserved extractor version for comparison')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', args.name) or not 1 <= args.repeats <= 3:
        parser.error('Use a unique run name and one to three repetitions')
    extractor = edition_highlights
    if args.extractor:
        spec = importlib.util.spec_from_file_location('frozen_extractor', args.extractor)
        extractor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(extractor)
    suite = json.loads(args.suite.read_text(encoding='utf-8'))
    ids = [c['id'] for c in suite['cases']]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', i) for i in ids):
        parser.error('Suite needs unique safe case IDs')
    inputs = {c['id']: json.loads((args.suite.parent/c['packet']).read_text(encoding='utf-8')) for c in suite['cases']}
    folder = legacy.OUT/args.name
    folder.mkdir(exist_ok=False)
    code = [Path(__file__), Path(extractor.__file__), Path(legacy.__file__), Path(__file__).with_name('local_ai_quality.py')]
    save(folder/'manifest.json', {'suiteSha256': hashlib.sha256(args.suite.read_bytes()).hexdigest(),
        'model': args.model, 'repeats': args.repeats, 'scope': suite['scope'],
        'inputSha256': {c['id']: hashlib.sha256((args.suite.parent/c['packet']).read_bytes()).hexdigest() for c in suite['cases']},
        'codeSha256': {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in code},
        'note': 'No live retrieval during inference. Repetitions measure stability, not independent cases.'})
    report = []
    for repeat in range(1, args.repeats+1):
        for case in suite['cases']:
            packet = inputs[case['id']]
            attempts, highlights, error = [], [], None
            start = time.monotonic()
            try:
                # Deliberately pass only the packet, not case facts or scoring data.
                highlights = extractor.extract(packet, args.model, attempts, legacy.local_request)
            except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
                error = {'type': type(exc).__name__, 'message': str(exc)}
            row = {'case': case['id'], 'repeat': repeat, 'seconds': round(time.monotonic()-start, 3),
                   'error': error, **score(packet, highlights, case['centralFacts'])}
            save(folder/f'{case["id"]}-{repeat}.json', {'score': row, 'highlights': highlights, 'attempts': attempts})
            report.append(row)
            print(json.dumps(row), flush=True)
    save(folder/'report.json', report)


if __name__ == '__main__':
    main()
