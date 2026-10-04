import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError

import issue_fetch as fetcher


class FetchTests(unittest.TestCase):
    issue = {'series': 'Example', 'year': 2020, 'number': 1}
    url = 'https://comicvine.gamespot.com/example/4000-1/'

    def packet(self, text='Collects Example (2020) #1-2.'):
        return {'book': {'isbn': '123'}, 'sources': [{'id': 'S1', 'text': text}], 'constraints': {}}

    def plan(self):
        return {'isbn': '123', 'sources': [{'id': 'I1', 'url': self.url, 'issue': self.issue}]}

    def test_exact_title_with_year_and_site_suffix(self):
        headings = ['Example #1', 'Example (2020) #1 - A Story (Issue) - Comic Vine']
        self.assertEqual(fetcher.title_from_headings(headings, self.issue)['title'], 'A Story')

    def test_missing_title_wrong_year_and_wrong_number_abstain(self):
        for heading in ['Example #1', 'Example (2016) #1 - A Story', 'Example #10 - A Story', 'Other Example #1 - A Story']:
            self.assertIsNone(fetcher.title_from_headings([heading], self.issue))

    def test_conflicting_headings_fail(self):
        with self.assertRaises(ValueError):
            fetcher.title_from_headings(['Example #1 - First', 'Example #1 - Second'], self.issue)

    def test_autonomous_plan_requires_year_again_on_downloaded_page(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = self.plan()
            plan['sources'][0]['identityMode'] = 'explicit_year'
            supplement, report = fetcher.acquire(plan, self.packet(), Path(temp), Path(temp),
                lambda url: (b'<title>Example #1 - Wrong Run Maybe (Issue)</title>', url, 'utf-8'))
            self.assertEqual(supplement['sources'], [])
            self.assertEqual(report[0]['state'], 'no_explicit_title')

    def test_local_urls_and_redirects_are_rejected(self):
        for url in ['http://comicvine.gamespot.com/x', 'https://127.0.0.1/x', 'https://comicvine.gamespot.com.evil.test/x', 'https://user@www.marvel.com/x']:
            with self.assertRaises(ValueError):
                fetcher.check_url(url)

    def test_partial_issue_does_not_trigger_fetch(self):
        with tempfile.TemporaryDirectory() as temp:
            def request(url):
                self.fail('Partial issue must not be fetched for whole-story mapping')
            supplement, report = fetcher.acquire(self.plan(), self.packet('Collects Example (2020) #1 (D story).'), Path(temp), Path(temp), request)
            self.assertEqual(supplement['sources'], [])
            self.assertEqual(report[0]['state'], 'needs_review')

    def test_downloaded_heading_preserves_raw_bytes(self):
        body = b'<title>Example #1 - A Story (Issue)</title><h1>Example #1</h1>'
        with tempfile.TemporaryDirectory() as temp:
            supplement, report = fetcher.acquire(self.plan(), self.packet(), Path(temp), Path(temp), lambda url: (body, url, 'utf-8'))
            self.assertEqual(supplement['sources'][0]['text'], 'A Story')
            self.assertEqual((Path(temp) / 'I1.html').read_bytes(), body)
            self.assertEqual(report[0]['provenance'], 'downloaded_html')

    def test_blocked_download_uses_only_explicit_attributed_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'snapshot.json').write_text(json.dumps({'url': self.url, 'provider': 'web_search', 'retrievedAt': '2026-09-25', 'heading': 'Example #1 - A Story (Issue)'}))
            plan = self.plan()
            plan['sources'][0]['snapshot'] = 'snapshot.json'
            def blocked(url):
                raise HTTPError(url, 403, 'Forbidden', {}, None)
            supplement, report = fetcher.acquire(plan, self.packet(), path, path, blocked)
            self.assertEqual(report[0]['httpStatus'], 403)
            self.assertEqual(supplement['sources'][0]['provenance'], 'imported_search_snapshot')
            accepted = fetcher.trial.supported_titles({'stories': [{'source': 'I1', 'title': 'A Story'}]},
                supplement['sources'], fetcher.trial.inventory(self.packet()))
            self.assertIn('imported_search_snapshot', accepted[0]['mappingNote'])
            self.assertFalse((path / 'I1.html').exists())

    def test_snapshot_mismatch_is_not_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'snapshot.json').write_text(json.dumps({'url': 'wrong', 'provider': 'web_search', 'retrievedAt': '2026-09-25', 'heading': 'Example #1 - A Story'}))
            plan = self.plan()
            plan['sources'][0]['snapshot'] = 'snapshot.json'
            def blocked(url):
                raise OSError('offline')
            supplement, report = fetcher.acquire(plan, self.packet(), path, path, blocked)
            self.assertEqual(report[0]['state'], 'snapshot_failed')
            self.assertEqual(supplement['sources'], [])


if __name__ == '__main__':
    unittest.main()
