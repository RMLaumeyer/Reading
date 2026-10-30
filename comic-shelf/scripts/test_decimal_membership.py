from copy import deepcopy
import unittest
import decimal_membership as dm
import collection_path
import order_research


class DecimalMembershipTests(unittest.TestCase):
    def packet(self):
        return {'book': {'isbn': '9781302406240'}, 'constraints': {'contentsConflict': True},
                'sources': [{'id': 'OD1', 'url': 'https://example.test/edition',
                    'editionIsbn': '9781302406240', 'isbnEvidence': [{'identifier': '9781302406240'}],
                    'description': 'Collects Original Sin: Hulk vs. Iron Man #1-4 (aka Original Sin #3.1-3.4).',
                    'seriesLabel': 'Original Sin (2014)'}]}

    def test_explicit_equal_length_alias_preserves_conflict(self):
        packet = self.packet(); original = deepcopy(packet)
        row = dm.evidence(packet)[0]
        self.assertEqual(row['designators'], ['3.1', '3.2', '3.3', '3.4'])
        self.assertEqual(row['explicitAlias']['numbers'], [1,2,3,4])
        self.assertTrue(row['existingContentsConflict'])
        self.assertEqual(packet, original)

    def test_wrong_isbn_year_count_or_missing_explicit_alias_abstains(self):
        for key,value in [('editionIsbn','other'), ('isbnEvidence',[]), ('isbnEvidence',[{'identifier':'other'}]), ('seriesLabel','Other (2014)'),
                          ('description','Collects Original Sin #3.1-3.4.'),
                          ('description','Collects Hulk #1-5 (aka Original Sin #3.1-3.4).'),
                          ('description','Collects Hulk #1-4 (aka Original Sin #3.01-3.04).')]:
            packet=self.packet();packet['sources'][0][key]=value
            self.assertEqual(dm.evidence(packet), [])

    def test_exact_designator_and_year_matching_without_identity_promotion(self):
        slots=[{'position': i+1, 'unsupportedIssueDesignation': {'series':'Original Sin', 'year':year,
                'designator':number}} for i,(year,number) in enumerate([(2014,'3.1'),(2015,'3.1'),(2014,'3.10')])]
        result=dm.match_paths([{'sourceUrl':'guide','sourceSequence':slots}], [self.packet()])
        self.assertEqual([len(m['membershipCandidates']) for m in result['matches']], [1,0,0])
        self.assertEqual(result['resolvedIdentitiesAdded'],0)
        self.assertFalse(result['eligibleForPublication'])

    def reconciliable_packet(self):
        packet=self.packet()
        packet['book']['title']='Original Sin: Hulk vs. Iron Man: Issues #1-4'
        packet['constraints']['catalogRange']=[1,4]
        packet['sources'].append({'id':'S1','text':'Synopsis: Collects Original Sin #3.1-3.4.\nBibliographic information: ISBN 1302406248, 9781302406240'})
        return packet

    def test_reconciliation_explains_exact_range_without_clearing_conflict(self):
        packet=self.reconciliable_packet();original=deepcopy(packet)
        result=dm.reconcile(packet,dm.evidence(packet)[0])
        self.assertEqual(result['state'],'equivalent_numbering_supported')
        self.assertFalse(result['globalConflictCleared'])
        self.assertTrue(result['identityRequiresReview'])
        self.assertEqual(packet,original)

    def test_reconciliation_vetoes_every_extra_or_mismatched_source(self):
        for text in ('Synopsis: Collects Original Sin #3.1-3.5.\nBibliographic information: ISBN 9781302406240',
                     'Synopsis: Collects Original Sin #3.1-3.4.\nBibliographic information: ISBN 9780000000000',
                     'Synopsis: Collects Other #3.1-3.4.\nBibliographic information: ISBN 9781302406240'):
            packet=self.reconciliable_packet();packet['sources'][1]['text']=text
            self.assertEqual(dm.reconcile(packet,dm.evidence(packet)[0])['state'],'unreconciled')
        packet=self.reconciliable_packet();packet['sources'].append({'id':'extra','text':'Collects Other #1.'})
        self.assertEqual(dm.reconcile(packet,dm.evidence(packet)[0])['state'],'unreconciled')

    def test_reconciliation_requires_catalog_and_two_sources(self):
        for mutation in ('title','range','single','later'):
            packet=self.reconciliable_packet()
            if mutation=='title':packet['book']['title']='Other: Issues #1-4'
            if mutation=='range':packet['constraints']['catalogRange']=[1,5]
            if mutation=='single':packet['sources']=packet['sources'][:1]
            if mutation=='later':packet['sources'][0]['description']+=' Collects Other #1.'
            self.assertEqual(dm.reconcile(packet,dm.evidence(packet)[0])['state'],'unreconciled')

    def decimal_path(self, numbers=('3.1','3.2','3.3','3.4','3.10')):
        return {'sourceUrl':'guide', 'title':'Example','state':'needs_review','sourceKind':'independent_editorial',
                'orderedIssues':[], 'problems':[{'reason':'unsupported decimal'}],
                'sourceSequence':[{'position':i+1,'quote':'Original Sin #'+n,'issue':None,
                    'identityState':'unsupported','unsupportedIssueDesignation':{
                        'series':'Original Sin','year':None,'designator':n}}
                    for i,n in enumerate(numbers)]}

    def test_typed_decimal_inventory_and_mapping_stays_reviewed_and_exact(self):
        packet=self.reconciliable_packet();path=self.decimal_path()
        editions=[{'isbn':packet['book']['isbn'],'result':{'contents':{
            'entries':[],'unresolvedEntries':[],'conflict':True}}}]
        original=deepcopy((path,editions))
        report=dm.match_paths([path],[packet])
        drafts=dm.draft_inventory(editions,report)
        resolved=dm.resolve_path(path,report)
        self.assertEqual([n['issue']['number'] for n in resolved['orderedIssues']],['3.1','3.2','3.3','3.4'])
        self.assertEqual(resolved['sourceSequence'][-1]['identityState'],'unsupported')
        mapped=collection_path.build(resolved,drafts)
        self.assertEqual(mapped['coverage']['identityReview'],4)
        self.assertEqual(mapped['coverage']['wholeIssueMatches'],0)
        self.assertEqual(mapped['draftEditionPositions'],{packet['book']['isbn']:[1,2,3,4]})
        self.assertTrue(drafts[0]['result']['contents']['conflict'])
        self.assertFalse(mapped['completeReadingOrder'])
        self.assertFalse(mapped['eligibleForPublication'])
        self.assertEqual((path,editions),original)

    def test_conflicting_candidate_year_and_duplicates_veto_typed_nodes(self):
        path=self.decimal_path(('3.1',));report=dm.match_paths([path],[self.reconciliable_packet()])
        conflicting=deepcopy(report['matches'][0]['membershipCandidates'][0]);conflicting['year']=2015
        report['matches'][0]['membershipCandidates'].append(conflicting)
        self.assertEqual(dm.resolve_path(path,report)['orderedIssues'],[])
        path=self.decimal_path(('3.1','3.1'));report=dm.match_paths([path],[self.reconciliable_packet()])
        result=dm.resolve_path(path,report)
        self.assertEqual(result['orderedIssues'],[])
        self.assertTrue(all(s['identityState']=='duplicate' for s in result['sourceSequence']))

    def test_decimal_order_comparison_does_not_collapse_designators(self):
        path=self.decimal_path(('3.1','3.2'));report=dm.match_paths([path],[self.reconciliable_packet()])
        resolved=dm.resolve_path(path,report)
        other=deepcopy(resolved);other['orderedIssues'][0]['issue']['number']='3.10'
        comparison=order_research.compare(resolved,other)
        self.assertEqual(comparison['commonIssueCount'],1)
        self.assertFalse(comparison['completeReadingOrder'])

    def test_explicit_integer_alias_maps_to_decimal_without_inventing_primary_year(self):
        path=self.decimal_path(())
        path['sourceSequence']=[{'position':n,'identityState':'unresolved','quote':'alias',
            'issue':{'series':'Original Sin: Hulk vs. Iron Man','year':None,'number':n}} for n in range(1,5)]
        report=dm.match_paths([path],[self.reconciliable_packet()])
        result=dm.resolve_path(path,report)
        self.assertEqual([n['issue']['number'] for n in result['orderedIssues']],['3.1','3.2','3.3','3.4'])
        self.assertTrue(all(n['sourceIssue']['year'] is None for n in result['orderedIssues']))
        self.assertTrue(all(n['identityRequiresReview'] for n in result['orderedIssues']))
        path['sourceSequence'][0]['issue']['year']=2015
        self.assertEqual(len(dm.resolve_path(path,report)['orderedIssues']),3)

    def test_unstated_alias_is_not_matched(self):
        path=self.decimal_path(())
        path['sourceSequence']=[{'position':1,'identityState':'unresolved','quote':'alias',
            'issue':{'series':'Hulk vs. Iron Man','year':None,'number':1}}]
        report=dm.match_paths([path],[self.reconciliable_packet()])
        self.assertEqual(dm.resolve_path(path,report)['orderedIssues'],[])

    def test_unlisted_decimal_inventory_is_retained_without_scope_inference(self):
        packet=self.reconciliable_packet();path=self.decimal_path(('3.1',))
        editions=[{'isbn':packet['book']['isbn'],'result':{'contents':{'entries':[],'conflict':True}}}]
        report=dm.match_paths([path],[packet])
        mapped=collection_path.build(dm.resolve_path(path,report),dm.draft_inventory(editions,report))
        self.assertEqual([e['issue']['number'] for e in mapped['editionIssuesOutsideSource']],['3.2','3.3','3.4'])
        self.assertTrue(all(e['identityRequiresReview'] for e in mapped['editionIssuesOutsideSource']))


if __name__ == '__main__': unittest.main()
