import unittest
import cbro_order as cb
import order_research as research


class ResearchTests(unittest.TestCase):
    url = 'https://comicbookreadingorders.com/marvel/events/example-reading-order/'

    def page(self, content):
        return ('<h1>Example</h1><button role="tab" aria-controls="issues">Single Issues</button>'
                '<button role="tab" aria-controls="books">TPBs</button>'
                '<div role="tabpanel" id="issues">'+content+'</div>'
                '<div role="tabpanel" id="books"><p>Wrong #1 (2020)</p></div>')

    def path(self, numbers, series='Example'):
        return cb.parse(self.page('<p>'+ '<br>'.join(f'{series} #{n} (2020)' for n in numbers)+'</p>'), self.url)

    def test_same_series_year_in_paragraph_and_tab_isolation(self):
        path = cb.parse(self.page('<p>Example #1 (2020)<br>Example #2</p>'), self.url)
        self.assertEqual([n['issue']['year'] for n in path['orderedIssues']], [2020,2020])
        self.assertTrue(path['orderedIssues'][1]['identityRequiresReview'])

    def test_same_tab_year_crosses_paragraphs_but_never_series(self):
        path = cb.parse(self.page('<p>Example #1 (2020)<br>Other #2</p><p>Example #3</p>'), self.url)
        self.assertEqual(len(path['orderedIssues']), 2)
        self.assertEqual(len(path['problems']), 1)

    def test_conflict_in_another_paragraph_vetoes_year_inference(self):
        result = cb.parse(self.page('<p>Example #1 (2020)</p><p>Example #2 (2021)</p>'), self.url)
        self.assertEqual(result['orderedIssues'], [])
        self.assertEqual(len(result['sourceSequence']), 2)

    def test_conflicting_years_empty_and_missing_panel_fail(self):
        for html in (self.page(''), '<h1>Blocked</h1>'):
            with self.assertRaises(ValueError): cb.parse(html, self.url)

    def test_scripts_duplicates_and_unsupported_numbers(self):
        path = cb.parse(self.page('<script><p>Fake #1 (2000)</p></script><p>Example #1 (2020)<br>Example #1<br>Example #1.A</p>'), self.url)
        self.assertEqual(len(path['orderedIssues']), 1)
        self.assertEqual(len(path['problems']), 2)

    def test_added_issues_are_scope_differences_not_order_conflicts(self):
        result = research.compare(self.path([1,2]), self.path([1,3,2]))
        self.assertTrue(result['sameRelativeOrderOnSharedIssues'])
        self.assertEqual(len(result['onlyRight']), 1)
        self.assertEqual(result['orderConflicts'], [])
        self.assertEqual(result['state'], 'needs_review')
        self.assertFalse(result['requiredReadingEstablished'])

    def test_inverted_order_and_no_overlap_never_claim_agreement(self):
        result = research.compare(self.path([1,2]), self.path([2,1]))
        self.assertEqual(len(result['orderConflicts']), 1)
        self.assertFalse(result['sameRelativeOrderOnSharedIssues'])
        result = research.compare(self.path([1]), self.path([2]))
        self.assertFalse(result['sameRelativeOrderOnSharedIssues'])

    def test_punctuation_normalization_never_drops_series_prefix(self):
        self.assertEqual(research.compare(self.path([1], 'Event: Example'), self.path([1], 'Event Example'))['commonIssueCount'], 1)
        self.assertEqual(research.compare(self.path([1], 'Event: Example'), self.path([1], 'Example'))['commonIssueCount'], 0)

    def test_source_problems_block_agreement(self):
        a, b = self.path([1]), self.path([1])
        b['problems'] = [{'reason': 'unparsed row'}]
        self.assertFalse(research.compare(a,b)['sameRelativeOrderOnSharedIssues'])

    def test_year_disagreements_are_distinct_from_scope_differences(self):
        a,b=self.path([1]),self.path([1])
        b['orderedIssues'][0]['issue']['year']=2019
        result=research.compare(a,b)
        self.assertEqual(len(result['identityDisagreements']),1)
        self.assertEqual(result['state'],'needs_review')

    def test_research_tasks_group_unresolved_identity_without_losing_positions(self):
        a=self.path([1]);b=self.path([1]);b['sourceUrl']='https://other.example'
        for p in (a,b):
            p['sourceSequence'][0].update(identityState='unresolved')
            p['sourceSequence'][0]['issue']['year']=None
        tasks=research.research_tasks([a,b],[])
        self.assertEqual(len(tasks),1)
        self.assertEqual(len(tasks[0]['evidence']),2)

    def test_url_boundary(self):
        for url in (self.url.replace('https:', 'http:'), self.url+'?secret=1', self.url.replace('comicbookreadingorders.com', 'evil.test')):
            with self.assertRaises(ValueError): cb.check_url(url)

    def test_wrong_event_page_cannot_supply_a_plausible_list(self):
        raw=self.page('<p>Example #1 (2020)</p>').replace('<h1>Example</h1>','<h1>Other Event</h1>')
        with self.assertRaises(ValueError):cb.parse(raw,self.url)


if __name__ == '__main__': unittest.main()
