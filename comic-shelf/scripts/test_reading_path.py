import unittest
import reading_path as path


class PathTests(unittest.TestCase):
    url = 'https://share.marvel.com/comics/discover/1707/absolute-carnage'

    def card(self, title, issue_id=1):
        return f'<a class="ComicCard__Url" href="/comics/issue/{issue_id}/slug"><p class="ComicCard__Info--title">{title}</p><div>Writer #99</div></a>'

    def page(self, cards):
        return '<title>Example | Reading Lists | Marvel Comics</title>'+cards

    def test_list_keeps_source_order_and_explicit_years(self):
        result = path.parse_list(self.page(self.card('Example (2020) #2')+self.card('Example (2020) #1', 2)), self.url)
        self.assertEqual([n['issue']['number'] for n in result['orderedIssues']], [2, 1])
        self.assertEqual(result['cardCount'], 2)
        self.assertFalse(result['complete'])
        self.assertFalse(result['chronologyEstablished'])

    def test_missing_year_duplicate_and_unsupported_number_remain_problems(self):
        for extra in ['Example #2', 'Example (2020) #1', 'Example (2020) #1.A']:
            result = path.parse_list(self.page(self.card('Example (2020) #1')+self.card(extra, 2)), self.url)
            self.assertEqual(result['state'], 'needs_review')
            self.assertEqual(len(result['problems']), 1)

    def test_unrecognized_page_never_becomes_empty_success(self):
        for raw in ['<title>Access denied</title>', self.page('<h1>No cards</h1>')]:
            with self.assertRaises(ValueError):
                path.parse_list(raw, self.url)

    def test_same_source_id_cannot_support_two_different_issues(self):
        result = path.parse_list(self.page(self.card('Example (2020) #1')+self.card('Example (2020) #2')), self.url)
        self.assertEqual(result['state'], 'needs_review')
        self.assertEqual(len(result['orderedIssues']), 1)

    def test_external_nodes_are_not_declared_required(self):
        result = path.parse_list(self.page(self.card('Example (2020) #1')+self.card('Example (2020) #2', 2)), self.url)
        contents = {'entries': [{'series': 'Example', 'year': 2020, 'first': 1, 'last': 1, 'extent': 'partial', 'portion': 'D story'}]}
        mapped = path.map_edition(result, contents)
        self.assertEqual(mapped['placements'][0]['extent'], 'partial')
        self.assertEqual(mapped['outsideEdition'][0]['issue']['number'], 2)
        self.assertIsNone(mapped['externalIssuesAreRequired'])

    def test_scripts_and_non_card_links_cannot_supply_issues(self):
        raw = self.page('<script>'+self.card('Fake (2020) #1')+'</script><a href="/comics/issue/999/slug">Other (2020) #9</a>'+self.card('Example (2020) #1'))
        result = path.parse_list(raw, self.url)
        self.assertEqual(result['cardCount'], 1)

    def test_untrusted_card_url_is_reported(self):
        raw = self.page(self.card('Example (2020) #1').replace('/comics/issue/1/slug', 'https://evil.test/comics/issue/1/slug'))
        result = path.parse_list(raw, self.url)
        self.assertEqual(result['orderedIssues'], [])
        self.assertEqual(result['state'], 'needs_review')

    def test_same_title_number_different_year_is_visible_and_not_merged(self):
        result = path.parse_list(self.page(self.card('Example (2008) #1')), self.url)
        contents = {'entries': [{'series': 'Example', 'year': 2009, 'first': 1, 'last': 3,
                                'extent': 'whole', 'portion': None}]}
        mapped = path.map_edition(result, contents)
        self.assertEqual(mapped['placements'], [])
        self.assertEqual(mapped['identityMismatches'][0]['inventoryYears'], [2009])
        self.assertEqual(mapped['identityMismatches'][0]['issue']['year'], 2008)
        self.assertEqual(len(mapped['outsideEdition']), 1)


if __name__ == '__main__':
    unittest.main()
