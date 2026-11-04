import json
from pathlib import Path
import tempfile
import unittest
import review_decisions as review
import stage_enrichment as stage
import enrichment_worker as worker
from unittest.mock import patch


class StagingTests(unittest.TestCase):
    def test_missing_record_requires_explicit_isbn_and_creates_only_unknown_metadata(self):
        baseline = json.loads(self.base.read_text())
        del baseline['books']['book']
        self.base.write_text(json.dumps(baseline))
        review.record(self.queue, self.decisions, '123', 'accept', 'Reviewer', 'human', 'Fixture source review')
        ordinary = stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'ordinary')
        self.assertEqual(ordinary['changes'], [])
        self.assertIn('missing_existing_enrichment', ordinary['excluded'][0]['reasons'])
        result = stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'initialized', initialize_isbns=['123'])
        change = result['changes'][0]
        self.assertIsNone(change['before'])
        self.assertEqual(change['after']['summary'], 'Alpha fights.')
        self.assertIsNone(change['after']['pages'])
        for field in ('characters', 'stories', 'issueKeys'):
            self.assertEqual(change['after'][field], [])
        self.assertEqual(change['after']['readingPath']['name'], '')
        self.assertFalse(change['after']['startingPoint'])
        self.assertEqual(result['initializeIsbns'], ['123'])
        self.assertEqual(json.loads(self.base.read_text()), baseline)

    def test_initialization_does_not_bypass_flags_or_ambiguous_catalog_identity(self):
        baseline = json.loads(self.base.read_text());del baseline['books']['book'];self.base.write_text(json.dumps(baseline))
        rows = json.loads(self.queue.read_text());rows[0]['reviewReasons'] = ['contents_conflict'];self.queue.write_text(json.dumps(rows))
        catalog = json.loads(self.catalog.read_text());catalog['books'].append({'isbn':'123','id':'duplicate'});self.catalog.write_text(json.dumps(catalog))
        review.record(self.queue, self.decisions, '123', 'accept', 'Reviewer', 'human', 'Fixture')
        result = stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'blocked-init', initialize_isbns=['123'])
        self.assertEqual(result['changes'], [])
        self.assertIn('contents_conflict', result['excluded'][0]['reasons'])
        self.assertIn('catalog_identity_not_unique', result['excluded'][0]['reasons'])
        with self.assertRaises(ValueError):
            stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'unknown-init', initialize_isbns=['missing'])

    def test_accept_cannot_bypass_selection_warning_holds(self):
        cases = [
            ('Who controls the invaders?', 'Who controls the invaders?', 'question_only_synopsis_requires_context_review'),
            ('Alpha controls the machine! Or does he?', 'Alpha controls the machine!', 'omitted_immediate_qualifier_requires_review'),
            ('The heroes haven t escaped from the city.', 'The heroes haven t escaped from the city.', 'damaged_source_text_requires_review'),
            ('The king is imprisoned. For if he wants answers, he must fight.',
             'For if he wants answers, he must fight.', 'opening_reference_requires_context_review')]
        for index, (text, quote, reason) in enumerate(cases):
            with self.subTest(reason=reason):
                packet = {'book': {'isbn': '123', 'title': 'Alpha'}, 'sources': [{'id': 'S1', 'text': text}]}
                synopsis = {'value': quote, 'evidence': [{'source': 'S1', 'quote': quote}]}
                with patch.object(worker, 'premise_excerpts', return_value={}):
                    row = worker.review_record(packet, {'synopsis': synopsis})
                self.queue.write_text(json.dumps([row]))
                decisions = self.root / f'decisions-{index}'
                review.record(self.queue, decisions, '123', 'accept', 'Reviewer', 'delegated', 'Synthetic fixture', authorization='Synthetic test authorization')
                result = stage.build(self.queue, decisions, self.catalog, self.base, self.root / f'stage-{index}')
                self.assertEqual(result['changes'], [])
                self.assertIn(reason, result['excluded'][0]['reasons'])
                # A corrected string with valid citations also cannot silently
                # discard a queue's unresolved source/context warning.
                review.record(self.queue, decisions, '123', 'revise', 'Reviewer', 'delegated',
                              'Synthetic fixture correction', correction='A reviewed fixture synopsis.',
                              evidence=[{'source': 'S1', 'quote': quote}], authorization='Synthetic test authorization')
                revised = stage.build(self.queue, decisions, self.catalog, self.base, self.root / f'revised-stage-{index}')
                self.assertEqual(revised['changes'], [])
                self.assertIn(reason, revised['excluded'][0]['reasons'])

    def test_accepting_cited_rewrite_cannot_skip_entailment_review(self):
        rows = json.loads(self.queue.read_text())
        rows[0]['reviewReasons'] = ['rewritten_synopsis_requires_entailment_review']
        self.queue.write_text(json.dumps(rows))
        review.record(self.queue, self.decisions, '123', 'accept', 'Assistant', 'delegated', 'Citations present',
                      authorization='Synthetic authorization')
        result = stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'stage')
        self.assertEqual(result['changes'], [])
        self.assertIn('rewritten_synopsis_requires_entailment_review', result['excluded'][0]['reasons'])

    def test_user_delegated_assessment_retains_authorization(self):
        review.record(self.queue, self.decisions, '123', 'accept', 'Assistant', 'delegated', 'Reviewed fixture',
                      authorization='Synthetic user authorization for fixture publication')
        result = stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'stage')
        self.assertEqual(len(result['changes']), 1)
        provenance = result['changes'][0]['after']['synopsisReview']
        self.assertEqual(provenance['reviewerKind'], 'delegated')
        self.assertTrue(provenance['authorization'])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.queue = self.root/'queue.json'
        self.decisions = self.root/'decisions'
        self.catalog = self.root/'catalog.json'
        self.base = self.root/'enrichment.json'
        self.queue.write_text(json.dumps([{'isbn': '123', 'title': 'Test', 'reviewReasons': [],
            'fullDescriptions': [{'source': 'S1', 'description': 'Alpha fights.', 'url': 'https://example.com'}],
            'proposedSynopsis': {'value': 'Alpha fights.', 'evidence': [{'source': 'S1', 'quote': 'Alpha fights.'}]}}]))
        self.catalog.write_text(json.dumps({'books': [{'isbn': '123', 'id': 'book'}]}))
        self.base.write_text(json.dumps({'books': {'book': {'summary': 'Old', 'pages': 100}, 'other': {'summary': 'Untouched'}}}))

    def run_stage(self, kind='human', preview=False):
        review.record(self.queue, self.decisions, '123', 'accept', 'Reviewer', kind, 'Checked source')
        return stage.build(self.queue, self.decisions, self.catalog, self.base, self.root/'stage', preview)

    def test_approved_patch_preserves_fields_live_bytes_and_backup(self):
        before = self.base.read_bytes()
        result = self.run_stage()
        self.assertEqual(len(result['changes']), 1)
        self.assertEqual(self.base.read_bytes(), before)
        self.assertEqual((self.root/'stage/enrichment.before.json').read_bytes(), before)
        after = json.loads((self.root/'stage/enrichment.staged.json').read_text())
        self.assertEqual(after['books']['book']['pages'], 100)
        self.assertEqual(after['books']['other'], {'summary': 'Untouched'})

    def test_assistant_cannot_stage_by_default(self):
        self.assertEqual(len(self.run_stage('assistant')['changes']), 0)

    def test_preview_is_explicit(self):
        result = self.run_stage('assistant', True)
        self.assertTrue(result['previewOnly'])
        self.assertFalse(result['livePublicationEnabled'])

    def test_conflict_blocks_even_human_approval(self):
        rows = json.loads(self.queue.read_text())
        rows[0]['reviewReasons'] = ['contents_conflict']
        self.queue.write_text(json.dumps(rows))
        self.assertEqual(len(self.run_stage()['changes']), 0)


if __name__ == '__main__':
    unittest.main()
