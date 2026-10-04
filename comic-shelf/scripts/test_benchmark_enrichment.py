import unittest
from benchmark_enrichment import score


class BenchmarkTests(unittest.TestCase):
    def test_empty_predictions_do_not_get_perfect_precision(self):
        result = score({'book': {'isbn': '1'}, 'sources': []}, [], [{'id': 'fact', 'alternatives': [['plan']]}])
        self.assertIsNone(result['sourceGroundingPrecision'])
        self.assertEqual(result['centralFactRecall'], 0)

    def test_ungrounded_or_wrong_edition_prediction_cannot_cover_gold(self):
        packet = {'book': {'isbn': '1'}, 'sources': [{'id': 'S1', 'text': 'A plan.'}]}
        for change in ({'editionIsbn': '2'}, {'description': 'An invented plan.'}):
            h = {'source': 'S1', 'quote': 'A plan.', 'description': 'A plan.', 'editionIsbn': '1', **change}
            result = score(packet, [h], [{'id': 'plan', 'alternatives': [['plan']]}])
            self.assertEqual(result['grounded'], 0)
            self.assertEqual(result['centralFactsRecovered'], [])


if __name__ == '__main__':
    unittest.main()
