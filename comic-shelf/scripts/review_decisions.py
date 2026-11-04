"""Append immutable synopsis-review decisions; never publish or rewrite model output."""
import argparse
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import uuid


def load_queue(path):
    raw = path.read_bytes()
    rows = json.loads(raw.decode('utf-8-sig'))
    records = {row['isbn']: row for row in rows}
    if len(records) != len(rows):
        raise ValueError('Duplicate ISBNs in queue')
    return hashlib.sha256(raw).hexdigest(), records


def record(queue, decisions, isbn, action, reviewer, reviewer_kind, reason, correction=None, evidence=None, authorization=None):
    digest, rows = load_queue(queue)
    sequence = 1
    if decisions.exists():
        report(queue, decisions)  # Refuse to mix events from different queue versions.
        sequence = max((json.loads(p.read_text(encoding='utf-8')).get('sequence', 0)
                        for p in decisions.glob('*.json')), default=0) + 1
    if isbn not in rows or action not in ('accept', 'revise', 'reject', 'needs_research'):
        raise ValueError('Unknown ISBN or decision')
    if reviewer_kind not in ('human', 'assistant', 'delegated') or not reviewer.strip() or not reason.strip():
        raise ValueError('Reviewer identity, kind and rationale required')
    if reviewer_kind == 'delegated' and not authorization:
        raise ValueError('Delegated review requires explicit user authorization provenance')
    original = rows[isbn]
    proposal = original.get('proposedSynopsis') or {}
    if action == 'accept' and not proposal.get('value'):
        raise ValueError('Cannot accept an empty synopsis')
    evidence = evidence or []
    if action == 'revise':
        if not correction or not correction.strip() or not evidence:
            raise ValueError('Revision needs corrected text and evidence')
        sources = {source['source']: source['description'] for source in original['fullDescriptions']}
        for item in evidence:
            if not item.get('quote') or item.get('source') not in sources or item['quote'] not in sources[item['source']]:
                raise ValueError('Correction evidence must match an exact source passage')
    elif correction is not None or evidence:
        raise ValueError('Only revisions may supply correction evidence')
    event = {'id': uuid.uuid4().hex, 'sequence': sequence,
             'createdAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'queueSha256': digest, 'isbn': isbn, 'scope': 'synopsis_only', 'action': action,
             'reviewer': reviewer, 'reviewerKind': reviewer_kind, 'reason': reason,
             'authorization': authorization,
             'originalSynopsis': proposal, 'correctedSynopsis': correction, 'evidence': evidence,
             'retainedReviewReasons': original['reviewReasons'], 'readyForPublication': False,
             'limitation': 'Exact citation checks do not verify semantic entailment or edition identity.'}
    decisions.mkdir(parents=True, exist_ok=True)
    path = decisions/(event['createdAt'].replace(':', '-')+'-'+event['id']+'.json')
    with path.open('x', encoding='utf-8') as stream:
        json.dump(event, stream, indent=2, ensure_ascii=False)
    return event


def report(queue, decisions):
    digest, rows = load_queue(queue)
    latest = {}
    history = []
    for path in decisions.glob('*.json'):
        event = json.loads(path.read_text(encoding='utf-8'))
        if event['queueSha256'] != digest:
            raise ValueError('Decisions belong to a different queue; use a separate directory')
        if event['isbn'] not in rows:
            raise ValueError('Decision ISBN absent from queue')
        history.append(event)
    for event in sorted(history, key=lambda item: (item.get('sequence', 0), item['createdAt'], item['id'])):
        latest[event['isbn']] = event
    return {'queueSha256': digest, 'total': len(rows), 'decisionEvents': len(history),
            'unreviewed': len(rows)-len(latest), 'latestActions': dict(Counter(e['action'] for e in latest.values())),
            'latestReviewerKinds': dict(Counter(e['reviewerKind'] for e in latest.values())),
            'decisions': list(latest.values()), 'readyForPublication': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--queue', type=Path, required=True)
    parser.add_argument('--decisions', type=Path, required=True)
    parser.add_argument('--input', type=Path, help='JSON decision with isbn, action, reviewer, reviewer_kind, reason; optional correction/evidence')
    args = parser.parse_args()
    if args.input:
        event = record(args.queue, args.decisions, **json.loads(args.input.read_text(encoding='utf-8-sig')))
        print(json.dumps({'recorded': event['id'], 'action': event['action']}))
    else:
        print(json.dumps(report(args.queue, args.decisions), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
