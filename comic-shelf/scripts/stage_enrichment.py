"""Build isolated synopsis staging packages. Never writes served catalog data."""
import argparse
import copy
import difflib
import hashlib
import json
from pathlib import Path
import review_decisions
import approved_synopses


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build(queue, decisions, catalog_path, enrichment_path, output, preview_assistant=False,
          initialize_isbns=()):
    reviewed = review_decisions.report(queue, decisions)
    _, records = review_decisions.load_queue(queue)
    if isinstance(initialize_isbns, str) or not isinstance(initialize_isbns, (list, tuple)):
        raise ValueError('Initialization requires an explicit ISBN list')
    if any(not isinstance(isbn, str) or isbn not in records for isbn in initialize_isbns):
        raise ValueError('Initialization ISBN absent from review queue')
    initialize_isbns = sorted(set(initialize_isbns))
    catalog_raw, base_raw = catalog_path.read_bytes(), enrichment_path.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig'))
    baseline = json.loads(base_raw.decode('utf-8-sig'))
    staged = copy.deepcopy(baseline)
    mapping = {}
    for book in catalog['books']:
        mapping.setdefault(book['isbn'], []).append(book['id'])
    changes, excluded = [], []
    for event in reviewed['decisions']:
        isbn = event['isbn']
        record = records[isbn]
        blockers = list(record['reviewReasons'])
        if event['action'] == 'revise':
            blockers = [flag for flag in blockers if flag != 'short_synopsis_requires_context_review']
        if event['action'] not in ('accept', 'revise'):
            blockers.append('not_approved')
        if event['reviewerKind'] not in ('human', 'delegated') and not preview_assistant:
            blockers.append('human_approval_required')
        if len(mapping.get(isbn, [])) != 1:
            blockers.append('catalog_identity_not_unique')
        key = mapping.get(isbn, [None])[0]
        if key not in baseline['books'] and isbn not in initialize_isbns:
            blockers.append('missing_existing_enrichment')
        proposal = record.get('proposedSynopsis') or {}
        text = event['correctedSynopsis'] if event['action'] == 'revise' else proposal.get('value')
        evidence = event['evidence'] if event['action'] == 'revise' else proposal.get('evidence', [])
        sources = {s['source']: s for s in record['fullDescriptions']}
        if not text or not evidence or any(not e.get('quote') or e.get('source') not in sources
            or e['quote'] not in sources[e['source']]['description'] for e in evidence):
            blockers.append('missing_or_invalid_citations')
        if blockers:
            excluded.append({'isbn': isbn, 'reasons': sorted(set(blockers))})
            continue
        before = copy.deepcopy(staged['books'].get(key))
        if before is None:
            staged['books'][key] = approved_synopses.initial_record(event['createdAt'][:10])
        target = staged['books'][key]
        target['summary'] = text
        # Preserve existing edition fields and citations; retain synopsis provenance separately.
        target['synopsisReview'] = {'decisionId': event['id'], 'reviewer': event['reviewer'],
            'reviewerKind': event['reviewerKind'], 'queueSha256': reviewed['queueSha256'],
            'authorization': event.get('authorization'),
            'evidence': [{**e, 'url': sources[e['source']].get('url')} for e in evidence]}
        for e in evidence:
            url = sources[e['source']].get('url')
            if url and not any(s.get('url') == url for s in target.get('sources', [])):
                target.setdefault('sources', []).append({'label': 'Reviewed synopsis source', 'url': url})
        changes.append({'isbn': isbn, 'catalogId': key, 'before': before, 'after': copy.deepcopy(target)})
    output.mkdir(exist_ok=False)
    (output/'enrichment.before.json').write_bytes(base_raw)
    after_raw = (json.dumps(staged, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    (output/'enrichment.staged.json').write_bytes(after_raw)
    # Diff only affected records, avoiding whole-file formatting noise.
    before_view = json.dumps({c['catalogId']: c['before'] for c in changes}, indent=2, ensure_ascii=False).splitlines(True)
    after_view = json.dumps({c['catalogId']: c['after'] for c in changes}, indent=2, ensure_ascii=False).splitlines(True)
    (output/'changes.diff').write_text(''.join(difflib.unified_diff(before_view, after_view, fromfile='before', tofile='staged')), encoding='utf-8')
    manifest = {'previewOnly': preview_assistant, 'livePublicationEnabled': False,
        'initializeIsbns': initialize_isbns,
        'queueSha256': reviewed['queueSha256'], 'catalogSha256': digest(catalog_raw),
        'beforeSha256': digest(base_raw), 'stagedSha256': digest(after_raw),
        'changes': changes, 'excluded': excluded, 'unreviewed': reviewed['unreviewed'],
        'decisionsSha256': {p.name: digest(p.read_bytes()) for p in decisions.glob('*.json')},
        'rollback': 'enrichment.before.json is the exact pre-stage snapshot; staging never modifies the live file.'}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Staging review', '', 'Assistant preview only.' if preview_assistant else 'Approved synopsis staging (see reviewer and authorization provenance).',
             'No live data was changed. Edition flags block staging; acceptance applies to synopses only.', '',
             f'{len(changes)} staged; {len(excluded)} excluded; {reviewed["unreviewed"]} unreviewed.', '']
    for c in changes:
        lines.extend(['## '+records[c['isbn']]['title'], '', '**Before:** '+((c['before'] or {}).get('summary', '') if c['before'] is not None else '(No enrichment record; explicit synopsis-only initialization)'), '',
                      '**Staged:** '+c['after']['summary'], ''])
    for item in excluded:
        lines.extend([f"- {item['isbn']}: {', '.join(item['reasons'])}"])
    (output/'preview.md').write_text('\n'.join(lines), encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('queue', 'decisions', 'catalog', 'enrichment', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--preview-assistant', action='store_true', help='Explicitly labeled preview; never eligible for live publication')
    parser.add_argument('--initialize-isbn', action='append', default=[],
                        help='Explicitly allow a reviewed synopsis-only record for this missing catalog ISBN')
    args = parser.parse_args()
    result = build(args.queue, args.decisions, args.catalog, args.enrichment, args.output,
                   args.preview_assistant, args.initialize_isbn)
    print(json.dumps({'staged': len(result['changes']), 'excluded': len(result['excluded']), 'previewOnly': result['previewOnly']}))
