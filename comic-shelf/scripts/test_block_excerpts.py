import json
import unittest
from unittest.mock import patch
import enrichment_worker as worker


class BlockTests(unittest.TestCase):
    def blocks(self, text, quotes, other=None):
        packet = {'sources': [{'id': 'S1', 'text': text}] + (other or [])}
        excerpts = {f'E{i}': {'source': 'S1', 'quote': q} for i, q in enumerate(quotes, 1)}
        with patch.object(worker, 'premise_excerpts', return_value=excerpts):
            return worker.block_excerpts(packet)

    def test_pairs_are_nonoverlapping_and_preserve_literal_whitespace(self):
        text = 'Alpha fights.  Beta flees. Gamma returns.'
        blocks = self.blocks(text, ['Alpha fights.', 'Beta flees.', 'Gamma returns.'])
        self.assertEqual([b['quote'] for b in blocks.values()], ['Alpha fights.  Beta flees.', 'Gamma returns.'])
        self.assertTrue(all(b['quote'] in text for b in blocks.values()))

    def test_cannot_bridge_filtered_promotion_or_paragraph_boundary(self):
        for separator in [' Buy it now! ', '\n\n']:
            blocks = self.blocks('Alpha fights.' + separator + 'Beta flees.', ['Alpha fights.', 'Beta flees.'])
            self.assertEqual(len(blocks), 2)

    def test_does_not_cross_source_or_bibliographic_boundary(self):
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha fights. Bibliographic information: Beta flees.'},
                              {'id': 'OD1', 'text': 'Beta flees.'}]}
        excerpts = {'E1': {'source': 'S1', 'quote': 'Alpha fights.'}, 'E2': {'source': 'OD1', 'quote': 'Beta flees.'}}
        with patch.object(worker, 'premise_excerpts', return_value=excerpts):
            self.assertEqual(len(worker.block_excerpts(packet)), 2)

    def test_long_pairs_are_kept_as_singletons_without_truncation(self):
        for quote in ['word ' * 101 + '.', 'x' * 1201 + '.']:
            blocks = self.blocks(quote + ' Beta flees.', [quote, 'Beta flees.'])
            self.assertEqual([b['quote'] for b in blocks.values()], [quote, 'Beta flees.'])

    def test_model_still_selects_three_ids_with_same_prompt_and_exact_quotes(self):
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha fights. Beta flees.'}]}
        requests = []
        def request(base, path, body):
            requests.append(body)
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"ids":["B1"]}'}}]}
        singles = {'E1': {'source': 'S1', 'quote': 'Alpha fights.'}, 'E2': {'source': 'S1', 'quote': 'Beta flees.'}}
        with patch.object(worker, 'premise_excerpts', return_value=singles):
            result = worker.synopsis(packet, 'test', [], request, excerpt_mode='blocks')
        self.assertEqual(result['value'], packet['sources'][0]['text'])
        self.assertEqual(result['excerptMode'], 'blocks')
        self.assertEqual(requests[0]['messages'][0]['content'], worker.PREMISE_PROMPT)
        self.assertEqual(requests[0]['response_format']['json_schema']['schema']['properties']['ids']['maxItems'], 3)

    def test_review_omissions_use_blocks_and_keep_manual_holds(self):
        packet = {'book': {'isbn': '123', 'title': 'Alpha'}, 'sources': [{'id': 'S1', 'text': 'Alpha fights. Beta flees. Gamma returns.'}],
                  'retainedReviewReasons': ['source_integrity_requires_review']}
        singles = {f'E{i}': {'source': 'S1', 'quote': q} for i, q in enumerate(['Alpha fights.', 'Beta flees.', 'Gamma returns.'])}
        synopsis = {'value': 'Alpha fights. Beta flees.', 'evidence': [{'source': 'S1', 'quote': 'Alpha fights. Beta flees.'}], 'excerptMode': 'blocks'}
        with patch.object(worker, 'premise_excerpts', return_value=singles):
            row = worker.review_record(packet, {'synopsis': synopsis})
        self.assertEqual(row['unselectedPassages'], [{'source': 'S1', 'quote': 'Gamma returns.'}])
        self.assertIn('source_integrity_requires_review', row['reviewReasons'])
        self.assertFalse(row['readyForPublication'])

    def test_unknown_mode_fails_before_model_request(self):
        with self.assertRaises(ValueError):
            worker.synopsis({'sources': []}, 'test', [], lambda *args: self.fail('Unexpected model call'), excerpt_mode='unknown')


if __name__ == '__main__':
    unittest.main()
