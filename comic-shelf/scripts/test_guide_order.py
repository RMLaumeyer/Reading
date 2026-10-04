import unittest
import guide_order as guide
import collection_path
import series_references


class GuideTests(unittest.TestCase):
    url = 'https://marvelguides.com/example-reading-order'
    section = 'Part 1.2: Example'

    def page(self, rows):
        return '<h3>Example Reading Order</h3><p>'+self.section+'</p><p>Reading Order:</p><ul>'+''.join('<li><p>'+r+'</p></li>' for r in rows)+'</ul><p>Collected Editions:</p><li>Wrong #9</li>'

    def reference(self, text='COLLECTING: Example (2020) 1-5'):
        return series_references.parse('<p>'+text+'</p>', 'https://prhcomics.com/book/?isbn=9781234567890')

    def parse(self, rows, references=None):
        return guide.parse(self.page(rows), self.url, [self.section], references or [self.reference()])

    def test_source_order_range_expansion_and_scope(self):
        result = self.parse(['Example #3 – #4', 'Example #1'])
        self.assertEqual([n['issue']['number'] for n in result['orderedIssues']], [3,4,1])
        self.assertEqual(result['sourceKind'], 'independent_editorial')
        self.assertFalse(result['requiredReadingEstablished'])
        self.assertTrue(all(n['identityRequiresReview'] for n in result['orderedIssues']))

    def test_unknown_year_bad_range_and_duplicates_flag_problems(self):
        result = self.parse(['Example #1', 'Example #1', 'Unknown #2', 'Example #4-2'])
        self.assertEqual(len(result['orderedIssues']), 1)
        self.assertEqual(len(result['problems']), 3)
        self.assertEqual(result['state'], 'needs_review')

    def test_conflicting_year_does_not_silently_match(self):
        result = self.parse(['Example #1'], [self.reference(), self.reference('COLLECTING: Example (2000) 1-5')])
        self.assertEqual(result['orderedIssues'], [])
        self.assertEqual(result['sourceSequence'][0]['identityState'], 'conflict')

    def test_section_selection_is_exact_and_page_order_wins(self):
        raw = self.page(['Example #1'])+'<p>Part 1.3: Next</p><p>Reading Order:</p><li>Example #2</li>'
        result = guide.parse(raw, self.url, ['Part 1.3: Next', self.section], [self.reference()])
        self.assertEqual([n['issue']['number'] for n in result['orderedIssues']], [1,2])
        with self.assertRaises(ValueError):
            guide.parse(raw, self.url, ['Part 9: Missing'], [self.reference()])

    def test_scripts_and_navigation_do_not_supply_sequence(self):
        raw = self.page(['Example #1'])+'<script><li>Fake #2</li></script><nav><li>Fake #3</li></nav>'
        result = guide.parse(raw, self.url, [self.section], [self.reference()])
        self.assertEqual(len(result['orderedIssues']), 1)

    def test_editorial_mapping_cannot_become_publisher_or_required_claim(self):
        path = self.parse(['Example #1'])
        edition = {'isbn': 'test', 'result': {'contents': {'entries': [
            {'series': 'Example', 'year': 2020, 'first': 1, 'last': 1, 'extent': 'whole', 'portion': None, 'evidence': {}}]}}}
        result = collection_path.build(path, [edition])
        self.assertEqual(result['coverage']['identityReview'], 1)
        self.assertEqual(result['draftEditionPositions'], {'test': [1]})
        self.assertFalse(result['coversAllPublisherListedIssues'])
        self.assertFalse(result['completeReadingOrder'])
        self.assertIsNone(result['nodes'][0]['requiredReading'])

    def test_url_boundaries(self):
        for url in ['http://marvelguides.com/example-reading-order', self.url+'?key=x', 'https://evil.test/example-reading-order']:
            with self.assertRaises(ValueError): guide.check_url(url)

    def test_empty_selected_section_and_invalid_year_fail_closed(self):
        raw = self.page(['Example #1'])+'<p>Part 1.3: Empty</p><p>Reading Order:</p>'
        with self.assertRaises(ValueError):
            guide.parse(raw, self.url, [self.section, 'Part 1.3: Empty'], [self.reference()])
        self.assertEqual(self.parse(['Other (9999) #1'])['orderedIssues'], [])

    def test_draft_spans_expose_book_interleaving(self):
        path = self.parse(['Example #1', 'Example #2', 'Example #3'])
        def edition(isbn, numbers):
            return {'isbn': isbn, 'result': {'contents': {'entries': [
                {'series': 'Example', 'year': 2020, 'first': n, 'last': n, 'extent': 'whole', 'portion': None, 'evidence': {}}
                for n in numbers]}}}
        result = collection_path.build(path, [edition('A', [1,3]), edition('B', [2])])
        self.assertEqual(result['overlappingDraftEditionSpans'][0]['isbns'], ['A', 'B'])

    def test_document_title_supports_layout_without_matching_heading(self):
        raw=self.page(['Example #1']).replace('<h3>Example Reading Order</h3>',
            '<title>Example Reading Order — Marvel Guides</title><h1>Marvel Guides</h1>')
        result=guide.parse(raw,self.url,[self.section],[self.reference()])
        self.assertEqual(result['title'],'Example Reading Order')
        self.assertEqual(len(result['orderedIssues']),1)

    def test_document_title_mismatch_or_duplicates_fail_closed(self):
        for prefix in ('<title>Other Reading Order — Marvel Guides</title>',
                       '<title>Example Reading Order — Marvel Guides</title>'*2):
            with self.assertRaises(ValueError):guide.parse(prefix+self.page(['Example #1']),self.url,[self.section],[self.reference()])


if __name__ == '__main__': unittest.main()
