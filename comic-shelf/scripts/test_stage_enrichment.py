import json
from pathlib import Path
import tempfile
import unittest
import review_decisions as review
import stage_enrichment as stage


class StagingTests(unittest.TestCase):
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
