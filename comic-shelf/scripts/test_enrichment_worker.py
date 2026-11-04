import json
import unittest
from unittest.mock import patch
import enrichment_worker as worker


class WorkerTests(unittest.TestCase):
    def test_opening_reference_reports_skipped_literal_setup(self):
        setup = 'The king has been imprisoned!'
        for opening in ['For if he is to learn the truth, he must fight.',
                        'Yet her greatest battle is against a personal foe.',
                        'But they must escape.', 'His enemy returns.']:
            with self.subTest(opening=opening):
                warnings = self.warnings(setup + ' ' + opening, [opening])
                hint = next(w for w in warnings if w['reason'] == 'opening_reference_requires_context_review')
                self.assertEqual(hint['omittedContext'], {'source': 'S1', 'quote': setup})
                self.assertEqual(hint['contextPosition'], 'before_selection')

    def test_selected_setup_and_named_or_hyphenated_openings_are_not_flagged(self):
        for opening in ['He-Man fights Skeletor.', 'She-Hulk investigates.',
                        'Wolverine investigates the theft.', 'The king is imprisoned.']:
            self.assertEqual(self.warnings('Earlier source text. ' + opening, [opening]), [])
        quotes = ['Jane Foster becomes Thor.', 'Yet her greatest battle is personal.']
        self.assertEqual(self.warnings(' '.join(quotes), quotes), [])

    def test_opening_reference_requires_earlier_text_from_same_source(self):
        quote = 'They search for a missing friend.'
        self.assertEqual(self.warnings('Synopsis: ' + quote, [quote]), [])
        packet = {'sources': [{'id': 'S1', 'text': 'Earlier source text.'},
                              {'id': 'S2', 'text': 'Synopsis: ' + quote}]}
        self.assertEqual(worker.selection_warnings(packet, {'value': quote,
            'evidence': [{'source': 'S2', 'quote': quote}]}), [])

    def test_self_introduction_and_contents_only_prefix_are_not_skipped_setup(self):
        for quote in ["Her name is Janet, and she's hunting a killer.",
                      "Her name's Gwen Stacy, and she has her sights set on Peter Parker!",
                      'His name is Victor Shade.']:
            self.assertEqual(self.warnings('Earlier source text. ' + quote, [quote]), [])
        quote = "She's the deadliest spy, but Black Widow remembers her training."
        self.assertEqual(self.warnings('Collects Black Widow #1-4. ' + quote, [quote]), [])

    def test_opening_context_warning_reaches_queue_without_changing_proposal(self):
        quote = 'For if he is to learn the truth, he must fight.'
        text = 'The king has been imprisoned! ' + quote
        packet = {'book': {'isbn': '123', 'title': 'A prisoner'},
                  'sources': [{'id': 'S1', 'text': text}]}
        synopsis = {'value': quote, 'evidence': [{'source': 'S1', 'quote': quote}]}
        with patch.object(worker, 'premise_excerpts', return_value={}):
            row = worker.review_record(packet, {'synopsis': synopsis})
        self.assertIs(row['proposedSynopsis'], synopsis)
        self.assertIn('opening_reference_requires_context_review', row['reviewReasons'])
        self.assertIn('Earlier source context: S1: The king has been imprisoned!', worker.render_review([row]))

    def test_catalog_range_disagreement_remains_a_review_hold(self):
        contents={'entries':[{'extent':'whole'}], 'catalogRangeDisagreement':{'catalogRange':[11,14],'sourceRange':[11,13]}}
        self.assertIn('catalog_description_issue_range_disagreement',worker.contents_review(contents))
    def warnings(self, text, quotes, **extra):
        packet = {'sources': [{'id': 'S1', 'text': text}]}
        synopsis = {'value': ' '.join(quotes), 'evidence': [{'source': 'S1', 'quote': q} for q in quotes], **extra}
        return worker.selection_warnings(packet, synopsis)

    def test_questions_without_a_protagonist_setup_are_held(self):
        quotes = ['Who controls the invaders?', 'How can they be stopped?']
        warnings = self.warnings('Alpha fights invaders. ' + ' '.join(quotes), quotes)
        self.assertEqual([w['reason'] for w in warnings], ['question_only_synopsis_requires_context_review'])

    def test_a_question_with_narrative_setup_is_not_question_only(self):
        quotes = ['Alpha fights invaders.', 'Who controls them?']
        self.assertEqual(self.warnings(' '.join(quotes), quotes), [])
        self.assertEqual(self.warnings('Alpha wonders who controls them?', ['Alpha wonders who controls them?']), [])

    def test_selected_damaged_contractions_and_replacement_characters_are_held(self):
        for quote in ['They haven t escaped.', 'Alpha can t leave.', 'The city is \ufffd.']:
            with self.subTest(quote=quote):
                self.assertEqual(self.warnings(quote, [quote])[0]['reason'], 'damaged_source_text_requires_review')
        for quote in ["They haven't escaped.", 'They haven’t escaped.', 'Alpha cannot leave.']:
            self.assertEqual(self.warnings(quote, [quote]), [])

    def test_unselected_damage_does_not_hold_clean_selection(self):
        self.assertEqual(self.warnings('They haven t escaped. Alpha searches for them.', ['Alpha searches for them.']), [])

    def test_omitted_immediate_qualifier_is_reported_with_literal_context(self):
        warnings = self.warnings('Alpha controls the machine! Or does he?', ['Alpha controls the machine!'])
        self.assertEqual(warnings[0]['reason'], 'omitted_immediate_qualifier_requires_review')
        self.assertEqual(warnings[0]['omittedContext'], {'source': 'S1', 'quote': 'Or does he?'})

    def test_including_qualifier_separately_or_in_same_quote_clears_that_check(self):
        text = 'Alpha controls the machine! Or does he?'
        self.assertEqual(self.warnings(text, ['Alpha controls the machine!', 'Or does he?']), [])
        self.assertEqual(self.warnings(text, [text]), [])

    def test_qualifier_must_be_immediate_and_from_same_source(self):
        text = 'Alpha controls the machine! Beta leaves. Or does he?'
        self.assertEqual(self.warnings(text, ['Alpha controls the machine!']), [])
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha controls the machine! Or does he?'},
                              {'id': 'S2', 'text': 'Or does he?'}]}
        result = {'value': 'Alpha controls the machine! Or does he?',
                  'evidence': [{'source': 'S1', 'quote': 'Alpha controls the machine!'}, {'source': 'S2', 'quote': 'Or does he?'}]}
        self.assertIn('omitted_immediate_qualifier_requires_review', [w['reason'] for w in worker.selection_warnings(packet, result)])

    def test_following_topic_question_and_hyphenated_name_are_not_qualifiers(self):
        for following in ['But is she ready to face her past?', 'But is She-Hulk the greatest hero?', 'But will she marry Alpha?']:
            text = 'Alpha controls the machine! ' + following
            self.assertEqual(self.warnings(text, ['Alpha controls the machine!']), [])
        text = 'Alpha controls the machine! Or does he really?'
        self.assertEqual(self.warnings(text, ['Alpha controls the machine!'])[0]['omittedContext']['quote'], 'Or does he really?')

    def test_rewrite_remains_subject_to_separate_entailment_review(self):
        self.assertEqual(self.warnings('Who controls them?', ['Who controls them?'], mode='rewrite'), [])

    def test_review_exports_context_and_does_not_change_model_selection(self):
        text = 'Alpha controls the machine! Or does he?'
        packet = {'book': {'isbn': '123', 'title': 'Alpha'}, 'sources': [{'id': 'S1', 'text': text}]}
        synopsis = {'value': 'Alpha controls the machine!', 'evidence': [{'source': 'S1', 'quote': 'Alpha controls the machine!'}]}
        with patch.object(worker, 'premise_excerpts', return_value={}):
            row = worker.review_record(packet, {'synopsis': synopsis})
        self.assertIs(row['proposedSynopsis'], synopsis)
        self.assertIn('omitted_immediate_qualifier_requires_review', row['reviewReasons'])
        self.assertIn('Immediate source context: S1: Or does he?', worker.render_review([row]))
        self.assertFalse(row['readyForPublication'])

    def test_recovery_cannot_drop_inherited_manual_source_holds(self):
        packet={'book':{'isbn':'123','title':'Alpha'},
                'sources':[{'id':'S1','text':'Alpha fights Beta.'}],
                'retainedReviewReasons':['editorial_source_integrity_requires_research','source_catalog_contents_disagreement']}
        result={'synopsis':{'value':'Alpha fights Beta in a struggle for the city.','evidence':[]},'reviewReasons':[]}
        with patch.object(worker,'premise_excerpts',return_value={}):
            row=worker.review_record(packet,result)
        self.assertIn('editorial_source_integrity_requires_research',row['reviewReasons'])
        self.assertIn('source_catalog_contents_disagreement',row['reviewReasons'])
        self.assertFalse(row['readyForPublication'])

    def rewrite(self, sentences, finish='stop', source='Alpha escapes. Beta pursues Alpha.'):
        packet = {'book': {'isbn': '123', 'title': 'Alpha'}, 'sources': [{'id': 'S1', 'text': source}]}
        excerpts = {'E1': {'source': 'S1', 'quote': 'Alpha escapes.'},
                    'E2': {'source': 'S1', 'quote': 'Beta pursues Alpha.'}}
        response = {'choices': [{'finish_reason': finish, 'message': {'content': json.dumps({'sentences': sentences})}}]}
        with patch.object(worker, 'premise_excerpts', return_value=excerpts):
            return worker.rewritten_synopsis(packet, 'test', [], lambda *args: response)

    def test_rewrite_retains_per_sentence_citations_and_deduplicates_flat_evidence(self):
        result = self.rewrite([{'text': 'Alpha flees Beta.', 'evidenceIds': ['E1', 'E2']},
                               {'text': 'Beta follows Alpha.', 'evidenceIds': ['E2']}])
        self.assertEqual(result['value'], 'Alpha flees Beta. Beta follows Alpha.')
        self.assertEqual(len(result['claims'][0]['evidence']), 2)
        self.assertEqual(len(result['evidence']), 2)
        self.assertEqual(result['passages'], ['Alpha escapes.', 'Beta pursues Alpha.'])

    def test_rewrite_rejects_missing_unknown_duplicate_and_empty_citations(self):
        for ids in ([], ['E99'], ['E1', 'E1']):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                self.rewrite([{'text': 'Alpha flees.', 'evidenceIds': ids}])
        with self.assertRaises(ValueError):
            self.rewrite([{'text': ' ', 'evidenceIds': ['E1']}])

    def test_rewrite_rejects_truncation_excess_claims_and_word_limit(self):
        claim = {'text': 'Alpha flees.', 'evidenceIds': ['E1']}
        with self.assertRaises(ValueError):
            self.rewrite([claim], finish='length')
        with self.assertRaises(ValueError):
            self.rewrite([claim] * 4)
        with self.assertRaises(ValueError):
            self.rewrite([{'text': 'word ' * 81, 'evidenceIds': ['E1']}])

    def test_rewrite_rejects_evidence_not_present_in_actual_source(self):
        with self.assertRaises(ValueError):
            self.rewrite([{'text': 'Alpha flees.', 'evidenceIds': ['E1']}], source='Unrelated text.')

    def test_rewrite_abstention_does_not_require_claims(self):
        result = self.rewrite([])
        self.assertIsNone(result['value'])
        self.assertEqual(result['claims'], [])

    def test_valid_citation_does_not_prove_entailment_or_clear_review_gate(self):
        # An ID can be valid while the claimed outcome is unsupported.
        result = self.rewrite([{'text': 'Alpha defeats Beta in battle.', 'evidenceIds': ['E1']}])
        packet = {'book': {'isbn': '123', 'title': 'Alpha'}, 'sources': [{'id': 'S1', 'text': 'Alpha escapes.'}]}
        with patch.object(worker, 'premise_excerpts', return_value={}):
            row = worker.review_record(packet, {'synopsis': result})
        self.assertIn('rewritten_synopsis_requires_entailment_review', row['reviewReasons'])
        self.assertFalse(row['readyForPublication'])
        self.assertIn('Alpha defeats Beta in battle.', worker.render_review([row]))

    def test_experimental_prompt_keeps_schema_grounding_and_abstention(self):
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha fights.'}]}
        attempts = []
        requests = []
        def request(base, path, body):
            requests.append(body)
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"ids":[]}'}}]}
        excerpts = {'E1': {'source': 'S1', 'quote': 'Alpha fights.'}}
        with patch.object(worker, 'premise_excerpts', return_value=excerpts):
            result = worker.synopsis(packet, 'test', attempts, request, prompt=worker.REVISED_PREMISE_PROMPT)
        self.assertIsNone(result['value'])
        self.assertEqual(requests[0]['messages'][0]['content'], worker.REVISED_PREMISE_PROMPT)
        self.assertEqual(requests[0]['response_format']['json_schema']['schema']['properties']['ids']['items']['enum'], ['E1'])
        self.assertEqual(requests[0]['temperature'], 0)
        self.assertEqual(requests[0]['reasoning_effort'], 'none')
        self.assertTrue(attempts[0]['promptSha256'])

    def test_identical_copy_from_two_sources_is_one_candidate(self):
        excerpts = {'E1': {'source': 'S1', 'quote': 'Alpha fights.'},
                    'E2': {'source': 'OD1', 'quote': 'Alpha fights.'}}
        packet = {'sources': [{'id': 'S1', 'text': 'Alpha fights.'}, {'id': 'OD1', 'text': 'Alpha fights.'}]}
        with patch.object(worker.edition_highlights, 'excerpts_for', return_value=excerpts):
            self.assertEqual(list(worker.premise_excerpts(packet)), ['E1'])

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
