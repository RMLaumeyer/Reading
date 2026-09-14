import copy
import unittest
from auto_enrich import annotate, issue_index, normalize

class ExtractionSafety(unittest.TestCase):
    def test_years_and_partial_issues_do_not_create_false_overlap(self):
        aliases={(normalize('Uncanny X-Men'),2013):'Uncanny X-Men'}
        self.assertEqual(issue_index('Collects Uncanny X-Men #1-5.',aliases),[])
        self.assertEqual(issue_index('Collects Uncanny X-Men (2011) #1-5.',aliases),[])
        self.assertEqual(issue_index('Collects material from Uncanny X-Men (2013) #1-5.',aliases),[])
        self.assertEqual(issue_index('Uncanny X-Men (2013) #15.INH',aliases),[])
        # A sentence-ending period is punctuation, not a decimal issue suffix.
        self.assertEqual(issue_index('Uncanny X-Men (2013) #1-3;',aliases),[f'Uncanny X-Men (2013) #{n}' for n in range(1,4)])
        self.assertEqual(len(issue_index('Collects Uncanny X-Men (2013) #1-3.',aliases)),3)

    def test_mentions_and_guessed_issues_never_become_verified(self):
        original=dict(summary='Saved text',pages=100,issueKeys=[],characters=[],sources=[],readingPath={},level='basic')
        snapshot=copy.deepcopy(original)
        result,reasons=annotate(dict(title='Uncanny X-Men Vol. 2',author='Bendis'),original,'Spider-Man remembers Uncanny X-Men (2013) #1-3;',['Spider-Man'],{(normalize('Uncanny X-Men'),2013):'Uncanny X-Men'},{})
        self.assertEqual(original,snapshot)
        self.assertEqual(result['characters'],[])
        self.assertEqual(result['issueKeys'],[])
        self.assertEqual(result['automation']['characterMentions'],['Spider-Man'])
        self.assertEqual(len(result['automation']['suggestedIssues']),3)
        self.assertNotIn('review',result)
        self.assertTrue(reasons)

if __name__=='__main__': unittest.main()
