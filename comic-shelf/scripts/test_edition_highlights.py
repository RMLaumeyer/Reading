import json
import unittest
from unittest.mock import Mock, patch
import edition_highlights as highlights


class HighlightTests(unittest.TestCase):
    def packet(self):
        return {'book': {'isbn': '9781302518585'}, 'constraints': {'isbnMatched': True},
                'sources': [{'id': 'S1', 'url': 'https://books.google.com/', 'text': 'Synopsis: '},
                            {'id': 'OD1', 'url': 'https://knoxcounty.overdrive.com/media/123',
                             'kind': 'OverDrive public edition metadata', 'editionIsbn': '9781302518585',
                             'isbnEvidence': [{'identifier': '9781302518585'}],
                             'text': 'Synopsis: Collects Example #1-3. A hero fights a dangerous invader to protect the town.'}]}

    def response(self, groups):
        return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'groups': groups})}}]}

    def test_fallback_premise_keeps_actual_source_and_unknown_story_scope(self):
        result = highlights.extract(self.packet(), 'fake', [], lambda *args: self.response([['E1']]))
        self.assertEqual(result[0]['source'], 'OD1')
        self.assertEqual(result[0]['description'], 'A hero fights a dangerous invader to protect the town.')
        self.assertEqual(result[0]['coveredIssues'], [])
        self.assertIsNone(result[0]['officialStoryTitle'])
        self.assertFalse(result[0]['completeStoryScopeEstablished'])

    def test_wrong_isbn_cannot_supply_highlights(self):
        packet = self.packet()
        packet['sources'][1]['editionIsbn'] = '9780000000000'
        request = Mock()
        self.assertEqual(highlights.extract(packet, 'fake', [], request), [])
        request.assert_not_called()

    def test_number_abbreviation_preserves_actor_and_complete_sentence(self):
        packet = self.packet()
        quote = 'Speedball is public enemy No. 1, jailed and blamed for the disaster.'
        packet['sources'][1]['text'] = 'Synopsis: '+quote
        excerpts = highlights.excerpts_for(packet)
        self.assertEqual([e['quote'] for e in excerpts.values()], [quote])

    def test_source_placeholder_is_not_a_highlight_candidate(self):
        packet = self.packet()
        packet['sources'][1]['text'] = 'Synopsis: [Author] will describe the battle.'
        self.assertEqual(highlights.excerpts_for(packet), {})

    def test_collecting_sentence_alone_is_not_a_story_premise(self):
        packet = self.packet()
        packet['sources'][1]['text'] = 'Synopsis: Collects Example #1-3.'
        request = Mock()
        self.assertEqual(highlights.extract(packet, 'fake', [], request), [])
        request.assert_not_called()

    def classified_response(self, decisions):
        return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(decisions)}}]}

    def test_omitted_plan_gets_reviewed_without_replacing_existing_selection(self):
        packet = self.packet()
        packet['sources'][1]['text'] = 'Synopsis: A hero fights an invader. Discover the regent\'s scheme.'
        request = Mock(side_effect=[self.response([['E1']]), self.classified_response({'E2': 'premise'})])
        result = highlights.extract(packet, 'fake', [], request)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['quote'], 'A hero fights an invader.')
        self.assertEqual(result[1]['quote'], "Discover the regent's scheme.")
        self.assertEqual(result[1]['coveredIssues'], [])
        self.assertEqual(request.call_count, 2)

    def test_planning_review_can_abstain_and_filters_promotion_and_pronouns(self):
        excerpts = {f'E{i}': {'source': 'S1', 'quote': q} for i, q in enumerate([
            'The greatest plan ever unfolds.', 'The writer plans a book.', 'His scheme begins.',
            "Discover the regent's scheme."], 1)}
        request = Mock(return_value=self.classified_response({'E4': 'other'}))
        self.assertEqual(highlights.select_planning(excerpts, 'fake', [], request), [])
        sent = json.loads(request.call_args.args[2]['messages'][1]['content'])
        self.assertEqual(list(sent), ['E4'])

    def test_planning_review_rejects_missing_unknown_invalid_or_duplicate_keys(self):
        excerpts = {'E1': {'source': 'S1', 'quote': "Discover the regent's plan."}}
        for raw in ['{}', '{"invented":"premise"}', '{"E1":"invented"}',
                    '{"E1":"other","E1":"premise"}']:
            response = {'choices': [{'finish_reason': 'stop', 'message': {'content': raw}}]}
            with self.assertRaises(ValueError):
                highlights.select_planning(excerpts, 'fake', [], Mock(return_value=response))

    def test_full_primary_selection_does_not_trigger_more_model_requests(self):
        excerpts = {f'E{i}': {'source': 'S1', 'quote': q} for i, q in enumerate([
            'A hero fights an invader.', 'A spy uncovers a secret.', 'A pirate rescues the crew.',
            'Discover the regent\'s plan.'], 1)}
        request = Mock(return_value=self.response([['E1'], ['E2'], ['E3']]))
        self.assertEqual(len(highlights.select(excerpts, 'fake', [], request)), 3)
        self.assertEqual(request.call_count, 1)

    def test_unknown_or_repeated_evidence_id_is_rejected(self):
        for groups in ([['invented']], [['E1'], ['E1']]):
            with self.assertRaises(ValueError):
                highlights.extract(self.packet(), 'fake', [], lambda *args: self.response(groups))

    def test_no_matching_primary_isbn_does_not_supply_primary_prose(self):
        packet = self.packet()
        packet['sources'] = [{'id': 'S1', 'text': 'Synopsis: A hero fights an invader.', 'url': 'https://books.google.com/'}]
        packet['constraints']['isbnMatched'] = False
        self.assertEqual(highlights.excerpts_for(packet), {})

    def test_highlight_failure_does_not_erase_inventory(self):
        import edition_trial
        packet = self.packet()
        packet['sources'][0]['text'] = 'Synopsis: Collects Example (2020) #1-3.'
        with patch.object(edition_trial.legacy, 'generate_stage', return_value={'summary': {}}):
            result = edition_trial.run(packet, None, 'fake', request=lambda *args: self.response([['invented']]))
        self.assertIn('featuredStoryHighlights', result['stageErrors'])
        self.assertEqual(result['contents']['entries'][0]['last'], 3)
        self.assertEqual(result['featuredStoryHighlights'], [])


if __name__ == '__main__':
    unittest.main()
