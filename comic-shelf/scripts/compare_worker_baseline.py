"""Offline diagnostic comparison; never changes worker outputs or served data.

Reference cues below are editorial labels for already reviewed development cases,
not independent gold. Literal matching measures retention, not semantic accuracy.
"""
import argparse
import hashlib
import json
from pathlib import Path


CUES = {
    '9781302529567': [('Dracula teaches Blade', ['teach Blade']), ('Adana confrontation', ['Adana']), ('Banner help', ['Bruce Banner', "Hulk's aid"])],
    '9781302367749': [('Clint identity', ['Clint']), ('Kate partnership', ['Kate Bishop']), ('Evidence mission', ['incriminating evidence'])],
    '9780785170761': [('New York setting', ['New York']), ('Ordinary and fantastic', ['ordinary and fantastic'])],
    '9781302481964': [('Moon Knight return', ['Moon Knight']), ('Registration controversy', ['Registration Card']), ('Stark pressure', ['Stark'])],
    '9781302485603': [('Strange identity', ['Doctor Strange']), ('Supernatural threat', ['trying to kill you', 'forces of darkness']), ('Cost of magic', ['magic has a cost'])],
    '9781302939304': [('Enemy targets loved ones', ['enemy from her past']), ('Bruno Wakanda thread', ['Wakanda']), ('Friendship conflict', ['best friends']), ('Power disruption', ['powers to fritz'])],
    '9781302483005': [('Alternate Kitty identity', ['Age of Apocalypse']), ('Battleworld survival', ['Battleworld'])],
    '9780785179658': [('Shield succession', ['Steve Rogers or Bucky Barnes']), ('1950s threat', ['1950s'])],
    '9781302368616': [('Soul mission', ['damned souls']), ('Iron Man flashback', ['Iron Man']), ('Spider-Man team-up', ['Spider-Man'])],
    '9781302530907': [('Valeria partner', ['Valeria Richards']), ('Galactus threat', ['Galactus'])],
}


def retained(text, cues):
    return [label for label, alternatives in cues if any(cue.casefold() in text.casefold() for cue in alternatives)]


def compare(folder, output):
    output.mkdir(exist_ok=False)
    manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    rows, details = [], []
    for case in manifest['cases']:
        packet_path = folder/case['packet']
        packet = json.loads(packet_path.read_text(encoding='utf-8'))
        source = next(s for s in packet['sources'] if s['id'] == 'S1')
        # Baseline preserves the whole description, including marketing and contents.
        baseline = source['text'].partition('Bibliographic information:')[0].removeprefix('Synopsis:').strip()
        result_path = folder/f"{case['isbn']}-result.json"
        result = json.loads(result_path.read_text(encoding='utf-8'))
        selected = result['synopsis']['value'] or ''
        cues = CUES[case['isbn']]
        full_cues, selected_cues = retained(baseline, cues), retained(selected, cues)
        rows.append({'isbn': case['isbn'], 'title': case['title'], 'expectedCues': len(cues),
                     'baselineCues': full_cues, 'qwenCues': selected_cues,
                     'omittedCues': [label for label in full_cues if label not in selected_cues],
                     'baselineWords': len(baseline.split()), 'qwenWords': len(selected.split()),
                     'baseline': baseline, 'qwen': selected, 'reviewReasons': result['reviewReasons'],
                     'packetSha256': hashlib.sha256(packet_path.read_bytes()).hexdigest(),
                     'resultSha256': hashlib.sha256(result_path.read_bytes()).hexdigest()})
        details.extend([f"## {case['title']}", '', f"ISBN {case['isbn']}", '', '**Full publisher description**', '', baseline, '',
                        '**Qwen selection**', '', selected or '(abstention)', '',
                        '**Omitted review cues:** '+(', '.join(rows[-1]['omittedCues']) or 'none'), ''])
    summary = {'editions': len(rows), 'referenceCues': sum(r['expectedCues'] for r in rows),
               'baselineCuesRetained': sum(len(r['baselineCues']) for r in rows),
               'qwenCuesRetained': sum(len(r['qwenCues']) for r in rows),
               'baselineWords': sum(r['baselineWords'] for r in rows), 'qwenWords': sum(r['qwenWords'] for r in rows),
               'casesWithOmissions': sum(bool(r['omittedCues']) for r in rows),
               'limitations': 'Post-hoc assistant labels on known cases; literal cue retention, not accuracy. No human timing or independent gold.'}
    (output/'comparison.json').write_text(json.dumps({'summary': summary, 'cases': rows}, indent=2), encoding='utf-8')
    header = ['# Publisher description versus Qwen selection', '', summary['limitations'], '',
              '| Edition | Full-description cues | Qwen cues | Full/Qwen words |', '| --- | ---: | ---: | ---: |']
    header.extend(f"| {r['title']} | {len(r['baselineCues'])}/{r['expectedCues']} | {len(r['qwenCues'])}/{r['expectedCues']} | {r['baselineWords']}/{r['qwenWords']} |" for r in rows)
    (output/'comparison.md').write_text('\n'.join(header+['']+details), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    compare(args.run, args.output)
