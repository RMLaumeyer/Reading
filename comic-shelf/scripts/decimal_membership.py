"""Extract explicit publisher decimal aliases as reviewable membership candidates."""
import re
from copy import deepcopy
from series_references import name_key


def reconcile(packet, row):
    """Explain a numbering mismatch only when every supplied synopsis agrees.

    This is scoped evidence reconciliation, not permission to clear the packet's
    global conflict or replace the established integer inventory schema.
    """
    isbn = packet['book']['isbn']
    alias = row['explicitAlias']
    title = re.fullmatch(r'(.+?): Issues #(\d+)-(\d+)', packet['book'].get('title', ''))
    if (not title or name_key(title[1]) != name_key(alias['series'])
            or [int(title[2]), int(title[3])] != [alias['numbers'][0], alias['numbers'][-1]]
            or packet.get('constraints', {}).get('catalogRange') != [alias['numbers'][0], alias['numbers'][-1]]):
        return {'state': 'unreconciled', 'reason': 'Catalog title and range do not match explicit alias'}
    quotes = []
    for source in packet.get('sources', []):
        text = source.get('text', '')
        synopsis, _, bib = text.partition('Bibliographic information:')
        direct = re.fullmatch(r'Synopsis:\s*Collects (.+?) #(\d+\.\d+)[-–](\d+\.\d+)\.\s*', synopsis)
        if source.get('id') == row['evidence']['source']:
            # Reject a later collecting claim hidden after the alias sentence.
            remainder = source.get('description', '')[len(row['evidence']['quote']):]
            if re.search(r'\bcollect(?:s|ing)\b', remainder, re.I):
                return {'state': 'unreconciled', 'reason': 'Additional collecting claim'}
            quotes.append({'source': source['id'], 'quote': row['evidence']['quote']})
        elif (direct and name_key(direct[1]) == name_key(row['series'])
              and [direct[2], direct[3]] == [row['designators'][0], row['designators'][-1]]
              and re.search(r'\bISBN\s+[\d,\sXx-]*\b'+re.escape(isbn)+r'\b', bib)):
            quotes.append({'source': source['id'], 'quote': direct[0].strip()})
        else:
            return {'state': 'unreconciled', 'reason': 'Additional source lacks matching exact-ISBN collecting evidence'}
    if len(quotes) < 2 or len({q['source'] for q in quotes}) != len(quotes):
        return {'state': 'unreconciled', 'reason': 'Need distinct alias and decimal collecting evidence'}
    return {'state': 'equivalent_numbering_supported', 'evidence': quotes,
            'scope': 'Only the explicit decimal range and its stated integer alias',
            'globalConflictCleared': False, 'identityRequiresReview': True}


def evidence(packet):
    isbn = packet['book']['isbn']
    rows = []
    for source in packet.get('sources', []):
        # Require source-specific exact-edition evidence, not another source's ISBN.
        if source.get('editionIsbn') != isbn or not any(
                row.get('identifier') == isbn for row in source.get('isbnEvidence', [])):
            continue
        description = source.get('description', '')
        match = re.match(r'^Collects (.+?) #(\d+)[-–](\d+) \(aka (.+?) #(\d+)\.(\d+)[-–](\d+)\.(\d+)\)\.', description)
        if not match:
            continue
        primary, first, last, secondary, major, low, end_major, high = match.groups()
        first, last, low, high = map(int, (first, last, low, high))
        year = re.fullmatch(r'(.+?) \((\d{4})\)', source.get('seriesLabel', ''))
        if (major != end_major or not 0 <= last-first <= 50 or high-low != last-first
                or not year or name_key(year[1]) != name_key(secondary)
                or not 1900 <= int(year[2]) <= 2100):
            continue
        # Leading zero suffixes are distinct strings; do not normalize them.
        if str(low) != match[6] or str(high) != match[8]:
            continue
        rows.append({'isbn': isbn, 'series': secondary, 'year': int(year[2]),
                     'designators': [major+'.'+str(n) for n in range(low, high+1)],
                     'explicitAlias': {'series': primary, 'numbers': list(range(first, last+1))},
                     'evidence': {'source': source['id'], 'url': source['url'], 'quote': match[0],
                                  'isbnEvidence': source['isbnEvidence'],
                                  'seriesLabel': source['seriesLabel'],
                                  'sha256': source.get('cacheSha256')},
                     'state': 'requires_review', 'existingContentsConflict': bool(packet.get('constraints', {}).get('contentsConflict'))})
    return rows


def match_paths(paths, packets):
    records = []
    for packet in packets:
        for row in evidence(packet):
            row['numberingReconciliation'] = reconcile(packet, row)
            records.append(row)
    matches = []
    for path in paths:
        for slot in path.get('sourceSequence', []):
            designation = slot.get('unsupportedIssueDesignation')
            if not designation:
                continue
            candidates = [row for row in records
                          if name_key(row['series']) == name_key(designation['series'])
                          and designation['designator'] in row['designators']
                          and designation.get('year') in (None, row['year'])]
            matches.append({'sourceUrl': path['sourceUrl'], 'position': slot['position'],
                            'designation': designation, 'membershipCandidates': candidates,
                            'state': 'requires_review' if candidates else 'missing_evidence',
                            'eligibleForPublication': False})
    return {'matches': matches, 'explicitAliasEvidence': records,
            'positionsWithSupportedEquivalentNumbering': sum(any(
                c['numberingReconciliation']['state'] == 'equivalent_numbering_supported'
                for c in m['membershipCandidates']) for m in matches),
            'resolvedIdentitiesAdded': 0, 'contentsConflictsCleared': 0,
            'eligibleForPublication': False}


def draft_inventory(editions, report):
    """Attach scoped decimal evidence to copies; preserve the global conflict."""
    result = deepcopy(editions)
    by_isbn = {e['isbn']: e for e in result}
    for row in report['explicitAliasEvidence']:
        if row['numberingReconciliation']['state'] != 'equivalent_numbering_supported':
            continue
        edition = by_isbn.get(row['isbn'])
        if edition is None:
            continue
        entries = edition['result']['contents'].setdefault('decimalEntries', [])
        for index, designator in enumerate(row['designators']):
            entry = {'series': row['series'], 'year': row['year'], 'designator': designator,
                     'extent': 'whole', 'portion': None, 'evidence': row['evidence'],
                     'identityResolution': {'state': 'draft', 'method': 'Explicit equivalent numbering and matching ISBN collecting statements'},
                     'numberingReconciliation': row['numberingReconciliation'],
                     'aliasIssue': {'series': row['explicitAlias']['series'],
                                    'number': row['explicitAlias']['numbers'][index]},
                     'globalConflictRetained': row['existingContentsConflict']}
            if entry not in entries:
                entries.append(entry)
    return result


def resolve_path(path, report):
    """Add typed decimal draft nodes only with unique reconciled evidence.

    Decimal numbers remain strings, never floats or integer-range members.
    Original parser problems remain visible and all new identities require review.
    """
    result = deepcopy(path)
    nodes = {n['position']: n for n in result['orderedIssues']}
    added = False
    for slot in result.get('sourceSequence', []):
        source_issue = slot.get('issue')
        if not source_issue or slot.get('identityState') != 'unresolved' or source_issue.get('year') is not None:
            continue
        candidates = [row for row in report['explicitAliasEvidence']
                      if row['numberingReconciliation']['state'] == 'equivalent_numbering_supported'
                      and name_key(row['explicitAlias']['series']) == name_key(source_issue['series'])
                      and source_issue['number'] in row['explicitAlias']['numbers']]
        identities = {(name_key(row['series']),row['year'],row['designators'][
            row['explicitAlias']['numbers'].index(source_issue['number'])]) for row in candidates}
        if len(identities) != 1:
            continue
        row=candidates[0]
        designator=row['designators'][row['explicitAlias']['numbers'].index(source_issue['number'])]
        node={**slot,'sourceIssue':deepcopy(source_issue),
              'issue':{'series':row['series'],'year':row['year'],'number':designator,'numberKind':'decimal'},
              'identityState':'resolved','identityRequiresReview':True,
              'identityEvidence':{'method':'Explicit source numbering alias to decimal identity','candidates':candidates}}
        slot.update(node);nodes[slot['position']]=node;added=True
    for match in report['matches']:
        if match['sourceUrl'] != result['sourceUrl']:
            continue
        candidates = match['membershipCandidates']
        # A conflicting year in any candidate vetoes promotion, even if another
        # candidate's numbering reconciliation passed.
        years = {c['year'] for c in candidates}
        supported = [c for c in candidates if c['numberingReconciliation']['state'] == 'equivalent_numbering_supported']
        if len(years) != 1 or not supported:
            continue
        slot = next((s for s in result['sourceSequence'] if s['position'] == match['position']), None)
        if not slot or slot.get('identityState') != 'unsupported' or not slot.get('unsupportedIssueDesignation'):
            continue
        designation = slot['unsupportedIssueDesignation']
        issue = {'series': designation['series'], 'year': next(iter(years)),
                 'number': designation['designator'], 'numberKind': 'decimal'}
        node = {**slot, 'issue': issue, 'identityState': 'resolved',
                'identityRequiresReview': True,
                'identityEvidence': {'method': 'Reconciled explicit decimal membership', 'candidates': supported}}
        slot.update(node)
        nodes[slot['position']] = node
        added = True
    groups = {}
    for position,node in nodes.items():
        issue=node['issue']
        groups.setdefault((name_key(issue['series']),issue['year'],issue['number']),[]).append(position)
    for positions in groups.values():
        if len(positions)>1:
            for position in positions:
                del nodes[position]
                next(s for s in result['sourceSequence'] if s['position']==position)['identityState']='duplicate'
    result['orderedIssues'] = [nodes[p] for p in sorted(nodes)]
    if added:
        result['state'] = 'needs_review'
    return result
