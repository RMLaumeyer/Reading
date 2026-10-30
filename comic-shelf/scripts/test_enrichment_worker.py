import json
import unittest
from unittest.mock import patch
import enrichment_worker as worker


class WorkerTests(unittest.TestCase):
    def test_review_preserves_full_context_and_surfaces_short_draft(self):
        packet = {'book': {'isbn': '123', 'title': 'Example'},
                  'sources': [{'id': 'S1', 'text': 'Synopsis: Full evidence. More context. Bibliographic information: credits'}]}
        result = {'synopsis': {'value': 'Example, of course.', 'evidence': []}, 'reviewReasons': []}
        with patch.object(worker, 'premise_excerpts', return_value={'E1': {'source': 'S1', 'quote': 'More context.'}}):
            record = worker.review_record(packet, result)
        self.assertEqual(record['fullDescriptions'][0]['description'], 'Full evidence. More context.')
        self.assertIn('short_synopsis_requires_context_review', record['reviewReasons'])
        self.assertEqual(record['editorialStatus'], 'unreviewed')
        self.assertIn('More context.', worker.render_review([record]))

    def test_initialisms_keep_subject_and_action_together(self):
        text = 'Synopsis: M.O.D.O.K. takes aim at the X-Men. Wade sells S.H.I.E.L.D. tech on the black market.'
        packet = {'constraints': {'isbnMatched': True}, 'sources': [{'id': 'S1', 'text': text}]}
        quotes = [item['quote'] for item in worker.premise_excerpts(packet).values()]
        self.assertEqual(quotes, ['M.O.D.O.K. takes aim at the X-Men.', 'Wade sells S.H.I.E.L.D. tech on the black market.'])

    def select(self, ids, finish='stop'):
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha fights. Beta escapes.'}]}
        excerpts = {'E1': {'source': 'S1', 'quote': 'Alpha fights.'},
                    'E2': {'source': 'S1', 'quote': 'Beta escapes.'}}
        response = {'choices': [{'finish_reason': finish, 'message': {'content': json.dumps({'ids': ids})}}]}
        with patch.object(worker.edition_highlights, 'excerpts_for', return_value=excerpts):
            return worker.synopsis(packet, 'test', [], lambda *args: response)

    def test_rejects_invented_duplicate_and_excessive_ids(self):
        for ids in [['E9'], ['E1', 'E1'], ['E1'] * 4]:
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                self.select(ids)

    def test_keeps_verbatim_passages_in_source_order(self):
        result = self.select(['E2', 'E1'])
        self.assertEqual(result['passages'], ['Alpha fights.', 'Beta escapes.'])
        self.assertEqual(len(result['evidence']), 2)

    def test_truncation_is_not_accepted(self):
        with self.assertRaises(ValueError):
            self.select(['E1'], 'length')

    def test_empty_selection_abstains(self):
        self.assertIsNone(self.select([])['value'])

    def test_flags_provisional_identity_and_partial_material(self):
        reasons = worker.contents_review({'entries': [{'identityResolution': {'state': 'draft'}, 'extent': 'partial'}]})
        self.assertIn('bibliographic_series_identity_requires_review', reasons)
        self.assertIn('partial_material_requires_review', reasons)


if __name__ == '__main__':
    unittest.main()
