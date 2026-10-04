"""Propose exact-series identities from existing edition evidence, without aliases."""
from copy import deepcopy
from series_references import name_key


def audit_editions(editions):
    """Flag overlapping same-label ranges with different years; never choose a winner.

    These may be different runs, so this is a scoped review warning, not proof
    that either edition is wrong. Input edition results are never mutated.
    """
    copies = deepcopy(editions)
    records = [(edition, entry) for edition in copies
               if not edition['result']['contents'].get('conflict')
               for entry in edition['result']['contents']['entries']]
    diagnostics = []
    for i, (left_book, left) in enumerate(records):
        for right_book, right in records[i+1:]:
            if (name_key(left['series']) != name_key(right['series'])
                    or left['year'] == right['year']
                    or max(left['first'],right['first']) > min(left['last'],right['last'])):
                continue
            warning = {'kind': 'overlapping_series_label_different_years',
                       'state': 'requires_review', 'doesNotEstablishWhichEditionIsWrong': True,
                       'evidence': [{'isbn': book['isbn'], 'series': entry['series'], 'year': entry['year'],
                                     'first': entry['first'], 'last': entry['last'], 'evidence': entry['evidence']}
                                    for book, entry in ((left_book,left),(right_book,right))]}
            diagnostics.append(warning)
            for entry in (left,right):
                if warning not in entry.setdefault('identityConflicts', []):
                    entry['identityConflicts'].append(warning)
    return copies, diagnostics


def resolve(path, editions, identity_sources=()):
    result = deepcopy(path)
    sequence = result.get('sourceSequence', [])
    resolved = {n['position']: n for n in result['orderedIssues']}
    diagnostics = []
    for slot in sequence:
        issue = slot.get('issue')
        if not issue or slot['identityState'] != 'unresolved':
            continue
        candidates = []
        for edition in editions:
            contents = edition['result']['contents']
            if contents.get('conflict'): continue
            for entry in contents['entries']:
                if name_key(entry['series']) != name_key(issue['series']): continue
                candidates.append({'isbn': edition['isbn'], 'entry': entry})
        for source in identity_sources:
            if source.get('sourceLabels') and not any(name_key(s)==name_key(issue['series']) for s in source['sourceLabels']):
                continue
            for entry in source['entries']:
                if name_key(entry['series']) == name_key(issue['series']):
                    candidates.append({'isbn':source['isbn'],'entry':entry,'url':source['url'],
                                       'sourceSha256':source['sha256'],'scope':source['scope']})
        years = {c['entry']['year'] for c in candidates}
        bounded = [c for c in candidates if c['entry']['first'] <= issue['number'] <= c['entry']['last']]
        if len(years) != 1 or not bounded:
            diagnostics.append({'position': slot['position'], 'state': 'conflict' if len(years)>1 else 'missing_evidence',
                                'candidates': candidates})
            continue
        node = {**slot, 'issue': {**issue, 'year': next(iter(years))},
                'identityState': 'resolved', 'identityRequiresReview': True,
                'identityEvidence': {'method': 'Unique exact-series identity in saved edition ranges', 'candidates': bounded}}
        slot.update(node)
        resolved[slot['position']] = node
    groups = {}
    for position, node in resolved.items():
        issue = node['issue']
        groups.setdefault((name_key(issue['series']), issue['year'], issue['number']), []).append(position)
    for positions in groups.values():
        if len(positions) > 1:
            for position in positions:
                del resolved[position]
                next(s for s in sequence if s['position'] == position)['identityState'] = 'duplicate'
            diagnostics.append({'positions': positions, 'state': 'duplicate_identity'})
            result['state'] = 'needs_review'
    result['orderedIssues'] = [resolved[p] for p in sorted(resolved)]
    result['identityDiagnostics'] = diagnostics
    # Original parser problems remain visible; proposals do not erase review gates.
    return result
