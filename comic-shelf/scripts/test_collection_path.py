import unittest
import collection_path as paths


class CollectionPathTests(unittest.TestCase):
    def path(self, numbers=(1, 2, 3)):
        return {'state': 'draft', 'sourceUrl': 'https://example.org/list', 'title': 'Example',
                'orderedIssues': [{'issue': {'series': 'Example', 'year': 2020, 'number': n},
                                   'position': p, 'quote': f'Example (2020) #{n}'} for p, n in enumerate(numbers, 1)]}

    def edition(self, isbn='A', first=1, last=1, **changes):
        entry = {'series': 'Example', 'year': 2020, 'first': first, 'last': last,
                 'extent': 'whole', 'portion': None, 'evidence': {'source': 'S1', 'quote': 'fixture'}, **changes}
        return {'isbn': isbn, 'title': isbn, 'result': {'contents': {'entries': [entry], 'unresolvedEntries': []}}}

    def test_source_sequence_and_gaps_survive_mapping(self):
        result = paths.build(self.path((3, 1, 2)), [self.edition(first=1, last=2)])
        self.assertEqual([n['issue']['number'] for n in result['nodes']], [3, 1, 2])
        self.assertEqual(result['uncoveredSourcePositions'], [1])
        self.assertEqual(result['coverage']['wholeIssueMatches'], 2)
        self.assertFalse(result['coversAllPublisherListedIssues'])

    def test_complete_source_coverage_is_not_a_complete_reading_order(self):
        result = paths.build(self.path(), [self.edition(first=1, last=3)])
        self.assertTrue(result['coversAllPublisherListedIssues'])
        self.assertFalse(result['completeReadingOrder'])
        self.assertFalse(result['eligibleForPublication'])
        self.assertTrue(all(n['requiredReading'] is None for n in result['nodes']))

    def test_collected_issues_absent_from_source_stay_visible(self):
        result = paths.build(self.path((1, 3)), [self.edition(first=1, last=3)])
        self.assertTrue(result['coversAllPublisherListedIssues'])
        self.assertEqual([n['issue']['number'] for n in result['editionIssuesOutsideSource']], [2])
        self.assertFalse(result['completeReadingOrder'])

    def test_overlapping_editions_are_alternatives_not_double_coverage(self):
        result = paths.build(self.path(), [self.edition('A', 1, 2), self.edition('B', 2, 3)])
        self.assertEqual(result['coverage']['wholeIssueMatches'], 3)
        self.assertEqual(result['alternativeEditionPositions'], [2])
        self.assertEqual(result['overlappingEditionSpans'][0]['isbns'], ['A', 'B'])

    def test_partial_and_inferred_identity_do_not_fill_whole_issue_gaps(self):
        result = paths.build(self.path(), [self.edition('A', 1, 1, extent='partial', portion='D story'),
            self.edition('B', 2, 2, identityResolution={'state': 'draft'})])
        self.assertEqual([n['coverageState'] for n in result['nodes']], ['partial_only', 'identity_review', 'uncovered'])
        self.assertEqual(result['coverage']['wholeIssueMatches'], 0)
        self.assertEqual(result['nodes'][0]['editionOptions'][0]['portions'], ['D story'])

    def test_unresolved_identity_stays_a_candidate_and_wrong_year_is_not_matched(self):
        edition = self.edition(year=2019)
        edition['result']['contents']['unresolvedEntries'] = [{'series': 'Example', 'year': None, 'first': 2, 'last': 2}]
        result = paths.build(self.path(), [edition])
        self.assertEqual([n['coverageState'] for n in result['nodes']], ['uncovered', 'identity_review', 'uncovered'])

    def test_issue_stories_do_not_leak_to_adjacent_issues(self):
        edition = self.edition(first=1, last=3)
        story = {'issue': {'series': 'Example', 'year': 2020, 'number': 2}, 'title': 'Story'}
        edition['result']['namedStories'] = [story]
        result = paths.build(self.path(), [edition])
        self.assertEqual([len(n['editionOptions'][0]['namedStories']) for n in result['nodes']], [0, 1, 0])

    def test_source_problems_and_no_nodes_cannot_earn_full_coverage(self):
        for path in (self.path(()), {**self.path(), 'state': 'needs_review'}):
            self.assertFalse(paths.build(path, [self.edition(first=1, last=3)])['coversAllPublisherListedIssues'])

    def test_failed_editions_stay_visible_and_duplicates_are_rejected(self):
        result = paths.build(self.path(), [], [{'isbn': 'failed', 'status': 'failed'}])
        self.assertEqual(len(result['unavailableEditions']), 1)
        self.assertEqual(result['coverage']['uncovered'], 3)
        with self.assertRaises(ValueError):
            paths.build(self.path(), [self.edition(), self.edition()])


if __name__ == '__main__':
    unittest.main()
