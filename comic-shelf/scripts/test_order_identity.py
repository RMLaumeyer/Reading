import unittest
import order_identity
import test_order_research
import cbro_order

class IdentityTests(unittest.TestCase):
    def path(self):
        fixture = test_order_research.ResearchTests()
        return cbro_order.parse(fixture.page('<p>Alpha #1 (2020)</p><p>Middle #2</p><p>Omega #1 (2020)</p>'), fixture.url)

    def edition(self, year=2019):
        return {'isbn': str(year), 'result': {'contents': {'entries': [
            {'series': 'Middle', 'year': year, 'first': 1, 'last': 3, 'extent': 'whole', 'evidence': {'quote': 'Middle'}}]}}}

    def test_positions_preserved_and_exact_evidence_resolves(self):
        path = self.path()
        self.assertEqual([n['position'] for n in path['orderedIssues']], [1,3])
        result = order_identity.resolve(path, [self.edition()])
        self.assertEqual([n['position'] for n in result['orderedIssues']], [1,2,3])
        self.assertEqual(result['orderedIssues'][1]['issue']['year'], 2019)
        self.assertTrue(result['orderedIssues'][1]['identityRequiresReview'])
        self.assertIsNone(path['sourceSequence'][1]['issue']['year'])

    def test_conflicting_evidence_never_resolves(self):
        result = order_identity.resolve(self.path(), [self.edition(),self.edition(2000)])
        self.assertEqual(len(result['orderedIssues']),2)
        self.assertEqual(result['identityDiagnostics'][0]['state'],'conflict')

    def test_explicit_conflict_and_alias_not_overridden(self):
        path = self.path(); path['sourceSequence'][1]['identityState']='conflict'
        self.assertEqual(len(order_identity.resolve(path,[self.edition()])['orderedIssues']),2)
        path = self.path(); path['sourceSequence'][1]['issue']['series']='Middle Vol. 2'
        self.assertEqual(len(order_identity.resolve(path,[self.edition()])['orderedIssues']),2)

    def test_duplicate_resolved_proposals_are_withheld(self):
        path = self.path()
        from copy import deepcopy
        slot = deepcopy(path['sourceSequence'][1]);slot['position']=4
        path['sourceSequence'].append(slot)
        result=order_identity.resolve(path,[self.edition()])
        self.assertEqual(len(result['orderedIssues']),2)
        self.assertEqual(result['identityDiagnostics'][-1]['state'],'duplicate_identity')

    def test_audit_flags_dated_entries_without_mutating_or_correcting_them(self):
        editions = [self.edition(),self.edition(2000)]
        audited, warnings = order_identity.audit_editions(editions)
        self.assertEqual(len(warnings),1)
        self.assertTrue(warnings[0]['doesNotEstablishWhichEditionIsWrong'])
        self.assertEqual(audited[0]['result']['contents']['entries'][0]['year'],2019)
        self.assertNotIn('identityConflicts', editions[0]['result']['contents']['entries'][0])
        self.assertTrue(audited[1]['result']['contents']['entries'][0]['identityConflicts'])

    def test_nonoverlapping_ranges_and_other_series_are_not_conflicts(self):
        a,b = self.edition(),self.edition(2000)
        b['result']['contents']['entries'][0].update(first=4,last=5)
        self.assertEqual(order_identity.audit_editions([a,b])[1],[])
        b['result']['contents']['entries'][0].update(first=1,last=3,series='Other')
        self.assertEqual(order_identity.audit_editions([a,b])[1],[])
