import json
from pathlib import Path
import tempfile
import unittest
import review_decisions as review


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.queue = Path(self.tmp.name)/'queue.json'
        self.decisions = Path(self.tmp.name)/'decisions'
        self.queue.write_text(json.dumps([{'isbn': '123', 'proposedSynopsis': {'value': 'Old text'},
            'fullDescriptions': [{'source': 'S1', 'description': 'Alpha fights Beta.'}],
            'reviewReasons': ['edition_conflict']}]), encoding='utf-8')

    def record(self, action='accept', **kwargs):
        return review.record(self.queue, self.decisions, '123', action, 'Test assistant', 'assistant', 'Source review', **kwargs)

    def test_history_is_append_only_and_source_unchanged(self):
        before = self.queue.read_bytes()
        self.record()
        self.record('reject')
        result = review.report(self.queue, self.decisions)
        self.assertEqual(result['decisionEvents'], 2)
        self.assertEqual(result['latestActions'], {'reject': 1})
        self.assertEqual(result['decisions'][0]['sequence'], 2)
        self.assertEqual(self.queue.read_bytes(), before)
        self.assertEqual(result['decisions'][0]['retainedReviewReasons'], ['edition_conflict'])
        self.assertFalse(result['readyForPublication'])

    def test_revision_requires_exact_evidence(self):
        with self.assertRaises(ValueError):
            self.record('revise', correction='Changed', evidence=[{'source': 'S1', 'quote': 'invented'}])
        event = self.record('revise', correction='Alpha fights.', evidence=[{'source': 'S1', 'quote': 'Alpha fights'}])
        self.assertEqual(event['correctedSynopsis'], 'Alpha fights.')

    def test_changed_queue_rejects_existing_decisions(self):
        self.record()
        self.queue.write_text(self.queue.read_text()+'\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            review.report(self.queue, self.decisions)

    def test_empty_proposal_cannot_be_accepted(self):
        rows = json.loads(self.queue.read_text())
        rows[0]['proposedSynopsis']['value'] = None
        self.queue.write_text(json.dumps(rows), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.record()


if __name__ == '__main__':
    unittest.main()
