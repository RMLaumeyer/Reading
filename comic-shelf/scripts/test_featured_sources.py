import unittest
import featured_sources as features


class FeaturedTests(unittest.TestCase):
    url = 'https://share.marvel.com/comics/discover/1233/start-here-fantastic-four'

    def row(self, title='Example (2020) #1', description='A story premise.', link='/comics/issue/1/example'):
        return (f'<div class="DiscoverList__Item"><div><a class="DiscoverList__Item-Url" href="{link}">image</a></div>'
                f'<div><h3 class="DiscoverList__Item-Title">{title}</h3>'
                f'<span class="DiscoverList__Item-Description">{description}</span></div></div>')

    def page(self, rows):
        return '<title>Start Here | Reading Lists | Marvel Comics</title>' + rows

    def contents(self, **kwargs):
        return {'entries': [{'series': 'Example', 'year': 2020, 'first': 1, 'last': 3,
                             'extent': 'whole', 'portion': None, **kwargs}]}

    def test_description_stays_bound_to_its_own_issue(self):
        raw = self.page(self.row(description='First <span>nested</span> ending.') +
                        self.row('Example (2020) #2', 'Second story.', '/comics/issue/2/example'))
        page = features.parse_features(raw, self.url)
        self.assertEqual([f['descriptionQuote'] for f in page['features']], ['First nested ending.', 'Second story.'])
        evidence, sources = features.edition_evidence([page], self.contents())
        self.assertEqual(len(evidence), 2)
        self.assertEqual(sources, [])
        self.assertIsNone(evidence[0]['officialStoryTitle'])
        self.assertFalse(page['readingOrderEstablished'])

    def test_unrelated_scripts_and_links_do_not_supply_evidence(self):
        page = features.parse_features(self.page('<script>'+self.row('Fake (2020) #9')+'</script>'+self.row()), self.url)
        self.assertEqual(len(page['features']), 1)
        self.assertEqual(page['features'][0]['issue']['series'], 'Example')

    def test_wrong_year_partial_and_inferred_identity_do_not_attach(self):
        page = features.parse_features(self.page(self.row()), self.url)
        for changes in ({'year': 2008}, {'extent': 'partial'}, {'identityResolution': {'state': 'draft'}}, {'series': 'Other'}):
            self.assertEqual(features.edition_evidence([page], self.contents(**changes)), ([], []))

    def test_explicit_part_evidence_is_not_a_story_title_or_complete_arc(self):
        page = features.parse_features(self.page(self.row(description='EXAMPLE ARC PART ONE! A premise.')), self.url)
        evidence, sources = features.edition_evidence([page], self.contents())
        self.assertEqual(sources[0]['kind'], 'publisher_issue_description')
        self.assertEqual(sources[0]['text'], 'EXAMPLE ARC PART ONE! A premise.')
        self.assertFalse(evidence[0]['completeStoryScopeEstablished'])

    def test_duplicate_unsafe_or_missing_description_blocks_automatic_use(self):
        for rows in (self.row()+self.row(), self.row(description=''),
                     self.row(link='https://evil.test/comics/issue/1/example'), self.row(title='Example #1')):
            page = features.parse_features(self.page(rows), self.url)
            self.assertEqual(page['state'], 'needs_review')
            self.assertEqual(features.edition_evidence([page], self.contents()), ([], []))

    def test_unclosed_or_unrecognized_page_is_rejected(self):
        for raw in (self.page('<div class="DiscoverList__Item">'), '<h3>Example (2020) #1</h3>'):
            with self.assertRaises(ValueError):
                features.parse_features(raw, self.url)

    def test_duplicate_page_cannot_inflate_description_count(self):
        page = features.parse_features(self.page(self.row()), self.url)
        self.assertEqual(len(features.edition_evidence([page, page], self.contents())[0]), 1)


if __name__ == '__main__':
    unittest.main()
