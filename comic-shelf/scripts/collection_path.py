"""Map a publisher's issue sequence across edition drafts, without publication."""


def identity(issue):
    return issue['series'].casefold(), issue['year'], issue['number']


def build(path, editions, unavailable=()):
    """Retain source order, edition alternatives and gaps; do not rank editions."""
    if len({e['isbn'] for e in editions}) != len(editions):
        raise ValueError('Duplicate edition ISBN in collection path')
    nodes, spans, draft_spans = [], {}, {}
    unresolved_positions = [s['position'] for s in path.get('sourceSequence', []) if s.get('identityState') != 'resolved']
    source_identities = {identity(n['issue']) for n in path['orderedIssues']}
    outside, outside_seen = [], set()
    for edition in editions:
        for entry in edition['result']['contents']['entries']:
            for number in range(entry['first'], entry['last'] + 1):
                issue = {'series': entry['series'], 'year': entry['year'], 'number': number}
                key = (edition['isbn'], identity(issue), entry['extent'], entry.get('portion'))
                if identity(issue) not in source_identities and key not in outside_seen:
                    outside_seen.add(key)
                    outside.append({'isbn': edition['isbn'], 'issue': issue, 'extent': entry['extent'],
                                    'portion': entry.get('portion'), 'inventoryEvidence': entry['evidence'],
                                    'identityRequiresReview': bool(entry.get('identityResolution') or entry.get('identityConflicts')),
                                    'reason': 'Inventoried in this edition but not listed in this source; no event membership or reading requirement inferred.'})
        for entry in edition['result']['contents'].get('decimalEntries', []):
            issue = {'series':entry['series'],'year':entry['year'],
                     'number':entry['designator'],'numberKind':'decimal'}
            key=(edition['isbn'],identity(issue),entry['extent'],entry.get('portion'))
            if identity(issue) not in source_identities and key not in outside_seen:
                outside_seen.add(key)
                outside.append({'isbn':edition['isbn'],'issue':issue,'extent':entry['extent'],
                    'portion':entry.get('portion'),'inventoryEvidence':entry['evidence'],
                    'identityRequiresReview':True,
                    'reason':'Draft decimal inventory not listed in this source; no event membership or reading requirement inferred.'})
    for source_node in path['orderedIssues']:
        issue = source_node['issue']
        options, candidates = [], []
        for edition in editions:
            result = edition['result']
            matches = [e for e in result['contents']['entries']
                       if e['series'].casefold() == issue['series'].casefold()
                       and e['year'] == issue['year'] and isinstance(issue['number'], int)
                       and e['first'] <= issue['number'] <= e['last']]
            matches.extend(e for e in result['contents'].get('decimalEntries', [])
                           if e['series'].casefold() == issue['series'].casefold()
                           and e['year'] == issue['year'] and e['designator'] == issue['number']
                           and issue.get('numberKind') == 'decimal')
            explicit = [e for e in matches if not e.get('identityResolution') and not e.get('identityConflicts') and not source_node.get('identityRequiresReview')]
            if explicit:
                whole = any(e['extent'] == 'whole' for e in explicit)
                options.append({'isbn': edition['isbn'], 'title': edition.get('title'),
                    'extent': 'whole' if whole else 'partial',
                    'portions': sorted({e['portion'] for e in explicit if e.get('portion')}),
                    'inventoryEvidence': [e['evidence'] for e in explicit],
                    'namedStories': [s for s in result.get('namedStories', [])
                                     if identity(s['issue']) == identity(issue)
                                     and (whole or s.get('portion') in {e.get('portion') for e in explicit})],
                    'numberedParts': [s for s in result.get('storyParts', [])
                                      if whole and identity(s['issue']) == identity(issue)],
                    'publisherDescriptions': [s for s in result.get('featuredStoryEvidence', [])
                                              if whole and identity(s['issue']) == identity(issue)]})
                if whole:
                    spans.setdefault(edition['isbn'], []).append(source_node['position'])
            elif matches:
                candidates.append({'isbn': edition['isbn'], 'reason': 'Edition or reading-source identity uses corroboration; identity review required',
                                   'entries': matches})
                if any(e['extent'] == 'whole' for e in matches):
                    draft_spans.setdefault(edition['isbn'], []).append(source_node['position'])
            unresolved = [e for e in result['contents'].get('unresolvedEntries', [])
                          if e['series'].casefold() == issue['series'].casefold()
                          and isinstance(issue['number'], int) and e['first'] <= issue['number'] <= e['last']]
            if unresolved:
                candidates.append({'isbn': edition['isbn'], 'reason': 'Series identity unresolved; no automatic substitution',
                                   'entries': unresolved})
        whole_options = [e for e in options if e['extent'] == 'whole']
        state = ('covered' if whole_options else 'partial_only' if options else
                 'identity_review' if candidates else 'uncovered')
        nodes.append({**source_node, 'coverageState': state, 'editionOptions': options,
                      'identityCandidates': candidates, 'requiredReading': None})
    gaps = [n['position'] for n in nodes if n['coverageState'] != 'covered']
    overlaps = [n['position'] for n in nodes
                if sum(e['extent'] == 'whole' for e in n['editionOptions']) > 1]
    # Overlapping spans warn against sorting whole books into the source sequence.
    # They can represent alternation, nesting or shared contents, not chronology.
    overlapping_spans = []
    isbns = sorted(spans)
    for i, left in enumerate(isbns):
        for right in isbns[i+1:]:
            if max(min(spans[left]), min(spans[right])) <= min(max(spans[left]), max(spans[right])):
                overlapping_spans.append({'isbns': [left, right],
                    'reason': 'Source positions overlap; use issue-level placements and choose alternatives before ordering whole editions.'})
    draft_overlaps = []
    combined_spans = {isbn: sorted(set(spans.get(isbn, []) + draft_spans.get(isbn, [])))
                      for isbn in set(spans) | set(draft_spans)}
    combined_isbns = sorted(combined_spans)
    for i, left in enumerate(combined_isbns):
        for right in combined_isbns[i+1:]:
            if max(min(combined_spans[left]), min(combined_spans[right])) <= min(max(combined_spans[left]), max(combined_spans[right])):
                draft_overlaps.append({'isbns': [left, right],
                    'reason': 'Including draft matches, edition spans overlap; do not infer a whole-book sequence.'})
    return {'sourceUrl': path['sourceUrl'], 'sourceTitle': path['title'],
            'sourceSequence': path.get('sourceSequence', []), 'unresolvedSourcePositions': unresolved_positions,
            'sourceSha256': path.get('sha256'), 'state': path['state'],
            'sourceKind': path.get('sourceKind', 'publisher'),
            'selectedSections': path.get('selectedSections', []),
            'scope': 'This source list, evaluated against only the supplied edition drafts',
            'nodes': nodes, 'uncoveredSourcePositions': gaps, 'alternativeEditionPositions': overlaps,
            'editionIssuesOutsideSource': outside,
            'editionPositions': spans, 'draftEditionPositions': draft_spans, 'overlappingEditionSpans': overlapping_spans,
            'overlappingDraftEditionSpans': draft_overlaps,
            'unavailableEditions': list(unavailable),
            'editionDiagnostics': [{'isbn': e['isbn'],
                'contentsConflict': e['result']['contents'].get('conflict', False),
                'identityReviewWarnings': [warning for entry in e['result']['contents']['entries']
                                           for warning in entry.get('identityConflicts', [])],
                'acceptedInventoryEntries': len(e['result']['contents']['entries']),
                'draftDecimalInventoryEntries': len(e['result']['contents'].get('decimalEntries',[])),
                'unresolvedEntries': len(e['result']['contents'].get('unresolvedEntries', [])),
                'unparsedContents': len(e['result']['contents'].get('unparsed', [])),
                'inventoryNote': e['result']['contents'].get('reason'),
                'stageErrors': e['result'].get('stageErrors', {})} for e in editions],
            'coverage': {'sourceIssues': len(nodes), 'wholeIssueMatches': len(nodes)-len(gaps),
                         'observedSourcePositions': len(path.get('sourceSequence', path['orderedIssues'])),
                         'unresolvedSourcePositions': len(unresolved_positions),
                         'partialOnly': sum(n['coverageState'] == 'partial_only' for n in nodes),
                         'identityReview': sum(n['coverageState'] == 'identity_review' for n in nodes),
                         'uncovered': sum(n['coverageState'] == 'uncovered' for n in nodes)},
            'coversAllPublisherListedIssues': path.get('sourceKind', 'publisher') == 'publisher' and bool(nodes) and not gaps and not unresolved_positions and path['state'] == 'draft',
            'coversAllSourceListedIssues': bool(nodes) and not gaps and not unresolved_positions and path['state'] == 'draft',
            'completeReadingOrder': False, 'requiredReadingEstablished': False,
            'eligibleForPublication': False,
            'note': 'Source-list coverage is not proof of a complete event or story inventory. Uncovered nodes are research gaps, not automatically required purchases or prerequisites.'}
