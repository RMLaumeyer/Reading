import json
from pathlib import Path
import tempfile
import unittest
import overdrive_sources as od
import edition_trial as trial


class OverDriveTests(unittest.TestCase):
    isbn = '9781302518585'
    url = 'https://knoxcounty.overdrive.com/media/123'

    def raw(self, **changes):
        record = {'id': '123', 'description': '<p>Collects Example #1-3. A story premise.</p>',
                  'series': 'Example (2020)',
                  'formats': [{'identifiers': [{'type': 'ISBN', 'value': self.isbn}]}], **changes}
        return '<script>window.OverDrive.mediaItems = '+json.dumps({'123': record})+';</script>'

    def test_isbn_bound_record_retains_field_evidence_and_draft_identity(self):
        source = od.parse_record(self.raw(), self.url, self.isbn)
        packet = {'book': {'isbn': self.isbn}, 'sources': [source], 'constraints': {}}
        result = trial.inventory(packet)
        self.assertEqual(result['entries'][0]['year'], 2020)
        self.assertEqual(result['entries'][0]['last'], 3)
        self.assertEqual(result['entries'][0]['identityResolution']['state'], 'draft')
        self.assertEqual(source['isbnEvidence'][0]['identifier'], self.isbn)

    def test_recommended_book_isbn_and_isbn_query_are_not_identity_evidence(self):
        raw = self.raw(formats=[]) + 'Recommended ISBN '+self.isbn
        with self.assertRaises(ValueError):
            od.parse_record(raw, self.url, self.isbn)

    def test_wrong_media_and_ambiguous_record_assignment_fail(self):
        for raw in (self.raw(id='456'), self.raw()+self.raw()):
            with self.assertRaises(ValueError):
                od.parse_record(raw, self.url, self.isbn)

    def test_bounded_two_request_lookup_saves_raw_evidence(self):
        calls = []
        def fetch(url):
            calls.append(url)
            if len(calls) == 1:
                return b'lookup', 'https://www.overdrive.com/media/123/example', 'utf-8'
            return self.raw().encode(), self.url, 'utf-8'
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)/'od'
            source = od.acquire(self.isbn, folder, fetch)
            self.assertEqual(len(calls), 2)
            self.assertEqual(source['editionIsbn'], self.isbn)
            self.assertTrue((folder/'search.html').exists())
            self.assertTrue((folder/'media.html').exists())
            self.assertEqual(json.loads((folder/'acquisition.json').read_text())['state'], 'accepted')

    def test_ambiguous_search_stops_before_second_request(self):
        calls = []
        def fetch(url):
            calls.append(url)
            return b'results', url, 'utf-8'
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(od.acquire(self.isbn, Path(temp)/'od', fetch))
        self.assertEqual(len(calls), 1)

    def test_candidate_list_requires_unique_record_isbn_match(self):
        for second_matches in (False, True):
            def fetch(url):
                if '/search?' in url:
                    return b'<a href="/media/123/a">A</a><a href="/media/456/b">B</a>', url, 'utf-8'
                raw = self.raw()
                if '/456' in url:
                    raw = raw.replace('123', '456')
                    if not second_matches: raw = raw.replace(self.isbn, '9780000000000')
                return raw.encode(), url, 'utf-8'
            with tempfile.TemporaryDirectory() as temp:
                result = od.acquire(self.isbn, Path(temp)/'od', fetch)
                self.assertEqual(result['url'], self.url)
                if second_matches: self.assertEqual(len(result['equivalentRecords']), 2)

    def test_duplicate_records_require_exact_agreement_except_credits(self):
        first = od.parse_record(self.raw(), self.url, self.isbn)
        for change in (' A different story.', ' Author: A. Illustrator: B. All rights reserved. Collects #4.'):
            second = {**first, 'description': first['description']+change}
            with self.assertRaises(ValueError): od.reconcile_records([first, second])
        with self.assertRaises(ValueError):
            od.reconcile_records([first, {**first, 'seriesLabel': 'Example (2021)'}])
        second = {**first, 'description': first['description']+' Author: A. Illustrator: B. All rights reserved.'}
        self.assertEqual(od.reconcile_records([second, first])['description'], first['description'])

    def test_candidate_list_bound_and_foreign_links(self):
        url = 'https://www.overdrive.com/search?q='+self.isbn
        raw = '<a href="https://evil.example/media/99">X</a><a href="/media/123/a">A</a><a href="/media/123/a">A</a>'
        self.assertEqual(od.candidate_ids(raw, url), ['123'])
        with self.assertRaises(ValueError):
            od.candidate_ids(''.join(f'<a href="/media/{i}/a">A</a>' for i in range(4)), url)

    def test_errors_are_sanitized_and_http_status_retained(self):
        from urllib.error import HTTPError
        def fetch(url):
            raise HTTPError(url, 429, 'secret_in_exception', {}, None)
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)/'od'
            self.assertIsNone(od.acquire(self.isbn, folder, fetch))
            raw = (folder/'acquisition.json').read_text()
            self.assertNotIn('secret_in_exception', raw)
            self.assertEqual(json.loads(raw)['httpStatus'], 429)

    def test_login_external_host_and_private_api_urls_are_rejected(self):
        for url in ('https://knoxcounty.overdrive.com/account/sign-in', 'https://evil.test/media/123',
                    'https://www.overdrive.com:444/media/123', 'http://www.overdrive.com/media/123',
                    'https://thunder.api.overdrive.com/v2/media/123'):
            with self.assertRaises(ValueError):
                od.check_url(url)


if __name__ == '__main__':
    unittest.main()
