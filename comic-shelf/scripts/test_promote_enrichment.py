import json
import unittest
from unittest.mock import patch
from test_stage_enrichment import StagingTests as Fixtures
import stage_enrichment as stage
import review_decisions as review
import promote_enrichment as promote
import approved_synopses


class PromotionTests(Fixtures):
    def prepare(self, kind='human', preview=False):
        (self.root/'public').mkdir()
        (self.root/'data').mkdir()
        (self.root/'dist/client').mkdir(parents=True)
        self.live = self.root/'public/enrichment.json'
        self.live.write_bytes(self.base.read_bytes())
        (self.root/'public/catalog.json').write_bytes(self.catalog.read_bytes())
        (self.root/'dist/client/enrichment.json').write_bytes(self.base.read_bytes())
        review.record(self.queue, self.decisions, '123', 'accept', 'Synthetic test reviewer', kind, 'Fixture only')
        self.package = self.root/'package'
        stage.build(self.queue, self.decisions, self.root/'public/catalog.json', self.live, self.package, preview)
        self.receipt = self.root/'receipt'

    def publish(self):
        return promote.promote(self.root, self.package, self.queue, self.decisions, self.receipt)

    def test_promote_overlay_and_exact_rollback(self):
        self.prepare()
        before = self.live.read_bytes()
        self.publish()
        overlay = self.root/'data/approved-synopses.json'
        self.assertEqual(approved_synopses.apply({'book': {'summary': 'Collector overwrite', 'pages': 200}}, overlay)['book']['summary'], 'Alpha fights.')
        self.assertEqual(json.loads(self.live.read_text())['books']['other'], {'summary': 'Untouched'})
        promote.rollback(self.root, self.receipt)
        self.assertEqual(self.live.read_bytes(), before)
        self.assertEqual((self.root/'dist/client/enrichment.json').read_bytes(), before)
        self.assertFalse(overlay.exists())

    def test_changed_live_refused(self):
        self.prepare()
        self.live.write_text('{}')
        with self.assertRaises(ValueError):
            self.publish()

    def test_withdrawn_approval_refused(self):
        self.prepare()
        review.record(self.queue, self.decisions, '123', 'reject', 'Synthetic reviewer', 'human', 'Withdraw test approval')
        with self.assertRaises(ValueError):
            self.publish()

    def test_preview_refused(self):
        self.prepare('assistant', True)
        with self.assertRaises(ValueError):
            self.publish()

    def test_rollback_refuses_newer_edits(self):
        self.prepare()
        self.publish()
        self.live.write_text('{}')
        with self.assertRaises(ValueError):
            promote.rollback(self.root, self.receipt)
        self.assertEqual(self.live.read_text(), '{}')

    def test_write_failure_restores_prior_files(self):
        self.prepare()
        before = self.live.read_bytes()
        original = promote.replace
        def fail_live(path, data):
            if path == self.live:
                raise OSError('Injected fixture failure')
            return original(path, data)
        with patch.object(promote, 'replace', side_effect=fail_live), self.assertRaises(OSError):
            self.publish()
        self.assertEqual(self.live.read_bytes(), before)
        self.assertFalse((self.root/'data/approved-synopses.json').exists())


if __name__ == '__main__':
    unittest.main()
