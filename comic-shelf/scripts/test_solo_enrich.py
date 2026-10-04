import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import solo_enrich as solo


class SoloTests(unittest.TestCase):
    def task(self, number=1):
        return {'kind': 'story_evidence', 'extent': 'whole', 'query': f'Example 2020 #{number}',
                'issue': {'series': 'Example', 'year': 2020, 'number': number}}

    def test_registered_source_selection_needs_no_per_issue_plan(self):
        urls = solo.known_lists([{'title': 'Absolute Carnage: Miles Morales: Issues #1-3'},
                                {'title': 'Absolute Carnage: Issues #1-5'}])
        self.assertEqual(urls, [solo.KNOWN_READING_LISTS['Absolute Carnage']])
        self.assertEqual(solo.known_lists([{'title': 'Absolute Carnageous'}, {'title': 'Other Story'}]), [])

    def packet(self):
        return {'book': {'isbn': '9781302507046'}, 'sources': [{'id': 'S1', 'text': 'Collects Example (2020) #1.'}], 'constraints': {}}

    def test_registered_event_does_not_select_sequel(self):
        self.assertEqual(solo.known_lists([{'title': 'Civil War II: Issues #0-8'}]), [])
        self.assertEqual(solo.known_lists([{'title': 'Civil War [Marvel Premier Collection]: Issues #1-7'}]),
                         [solo.KNOWN_READING_LISTS['Civil War']])

    def test_coverage_deduplicates_paths_and_separates_story_gaps(self):
        issue = {'series': 'Example', 'year': 2020, 'number': 1}
        entry = {'series': 'Example', 'year': 2020, 'first': 1, 'last': 2, 'extent': 'whole'}
        path = {'state': 'draft', 'placements': [{'issue': issue, 'extent': 'whole'}]}
        result = {'contents': {'entries': [entry, entry], 'unresolvedEntries': ['unknown'], 'unparsed': []},
                  'storyCoverage': {'issuesWithoutAnyStoryMapping': [issue, {**issue, 'number': 2}]},
                  'readingOrder': {'publisherPaths': [path, path]}}
        coverage = solo.collection_coverage(result)
        self.assertEqual(coverage['inventoriedWholeIssues'], 2)
        self.assertEqual(coverage['wholeIssuesWithPublisherPosition'], 1)
        self.assertEqual(coverage['wholeIssuesWithoutStoryEvidence'], 2)
        self.assertEqual(coverage['wholeIssuesWithAnyStoryEvidence'], 0)
        self.assertEqual(coverage['unresolvedEntries'], 1)
        self.assertFalse(coverage['complete'])
        path['state'] = 'needs_review'
        self.assertEqual(solo.collection_coverage(result)['wholeIssuesWithPublisherPosition'], 0)

    def search(self, query):
        return [{'url': 'https://comicvine.gamespot.com/example/4000-1/', 'heading': 'Example (2020) #1 - Story One (Issue)'}]

    def test_discovery_creates_plan_and_audited_snapshot(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            plan, report, used = solo.discover(self.packet(), [self.task()], p, 1, self.search)
            self.assertEqual(used, 1)
            self.assertEqual(plan['sources'][0]['issue'], self.task()['issue'])
            self.assertEqual(report[0]['state'], 'candidate')
            self.assertEqual(json.loads((p / 'D1-search.json').read_text())['provider'], 'web_search')

    def test_query_budget_and_partial_scope(self):
        calls = []
        def search(query):
            calls.append(query)
            return []
        with tempfile.TemporaryDirectory() as temp:
            plan, report, used = solo.discover(self.packet(), [{**self.task(), 'extent': 'partial'}, self.task(), self.task(2)], Path(temp), 1, search)
        self.assertEqual(len(calls), 1)
        self.assertEqual(used, 1)
        self.assertEqual(report[-1]['state'], 'budget_exhausted')

    def test_conflicting_search_titles_are_withheld(self):
        with tempfile.TemporaryDirectory() as temp:
            rows = self.search('') + [{'url': 'https://www.marvel.com/x', 'heading': 'Example (2020) #1 - Different Story'}]
            plan, report, _ = solo.discover(self.packet(), [self.task()], Path(temp), 1, lambda q: rows)
            self.assertEqual(plan['sources'], [])
            self.assertEqual(report[0]['state'], 'conflicting_titles')

    def test_wrong_year_number_and_unapproved_host_do_not_become_candidates(self):
        rows = [{'url': 'https://comicvine.gamespot.com/x', 'heading': 'Example (1990) #1 - Story'},
                {'url': 'https://comicvine.gamespot.com/x', 'heading': 'Example #2 - Story'},
                {'url': 'https://127.0.0.1/x', 'heading': 'Example #1 - Story'}]
        with tempfile.TemporaryDirectory() as temp:
            plan, report, _ = solo.discover(self.packet(), [self.task()], Path(temp), 1, lambda q: rows)
            self.assertEqual(plan['sources'], [])

    def test_yearless_same_number_is_not_automatic_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            rows = [{'url': 'https://comicvine.gamespot.com/x', 'heading': 'Example #1 - Story'}]
            plan, report, _ = solo.discover(self.packet(), [self.task()], Path(temp), 1, lambda q: rows)
            self.assertEqual(plan['sources'], [])
            self.assertEqual(report[0]['state'], 'identity_unverified')

    def test_malformed_provider_result_is_recorded_as_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            plan, report, _ = solo.discover(self.packet(), [self.task()], Path(temp), 1, lambda q: None)
            self.assertEqual(plan['sources'], [])
            self.assertEqual(report[0]['state'], 'search_failed')

    def test_checkpoint_retains_attempt_when_request_is_interrupted(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            def interrupt(query):
                raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt):
                solo.discover(self.packet(), [self.task()], folder, 1, interrupt)
            checkpoint = json.loads((folder / 'discovery-checkpoint.json').read_text())
            self.assertEqual(checkpoint['queriesAttempted'], 1)
            self.assertEqual(checkpoint['report'][0]['state'], 'pending')

    def test_failed_search_stops_and_does_not_log_exception_secrets(self):
        def fail(q):
            raise OSError('SECRET_TOKEN_IN_PROVIDER_EXCEPTION')
        with tempfile.TemporaryDirectory() as temp:
            plan, report, used = solo.discover(self.packet(), [self.task(), self.task(2)], Path(temp), 2, fail)
            self.assertEqual(used, 1)
            self.assertNotIn('SECRET_TOKEN', json.dumps(report))

    def test_missing_key_does_not_make_a_request(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(solo.urllib.request, 'build_opener') as opener:
            with self.assertRaises(ValueError):
                solo.brave_search('test')
            opener.assert_not_called()

    def test_full_issue_coverage_is_not_an_automatic_publication_certificate(self):
        r = {'stageErrors': {}, 'contents': {'entries': [{'extent': 'whole'}], 'unparsed': [], 'unresolvedEntries': []},
             'storyCoverage': {'issuesWithoutAnyStoryMapping': []}, 'namedStories': [{'title': 'Story'}],
             'readingOrder': {'editionContentsOrder': {'coversAllInventoriedWholeIssues': True}}}
        gate = solo.review_gate(r, {'sources': [{'provenance': 'imported_search_snapshot'}]})
        self.assertFalse(gate['eligibleForPublication'])
        self.assertIn('exhaustive_story_coverage_unverified', gate['blockers'])
        self.assertIn('search_excerpt_only', gate['blockers'])

    def test_bibliographic_year_and_publisher_disagreement_require_review(self):
        result = {'stageErrors': {}, 'contents': {'entries': [{'extent': 'whole',
                   'identityResolution': {'state': 'draft'}}], 'unparsed': [], 'unresolvedEntries': []},
                  'storyCoverage': {'issuesWithoutAnyStoryMapping': []},
                  'readingOrder': {'publisherPaths': [{'identityMismatches': [{'inventoryYears': [2009]}]}]}}
        gate = solo.review_gate(result, {'sources': []})
        self.assertIn('bibliographic_series_identity_requires_review', gate['blockers'])
        self.assertIn('publisher_list_year_mismatch', gate['blockers'])
        self.assertFalse(gate['eligibleForPublication'])

    def test_live_edition_mismatch_stops_before_model_or_search(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = self.packet()
            packet['constraints']['isbnMatched'] = False
            with patch.object(solo.intake, 'prepare', return_value=(packet, {}, {})), \
                    patch.object(solo.trial, 'run') as model:
                with self.assertRaises(ValueError):
                    solo.process(packet['book'], Path(temp), 'fake', refresh_edition=True,
                        edition_fetch=lambda isbn: (b'wrong edition', 'https://books.google.com/books?id=wrong', 'utf-8'))
                model.assert_not_called()
            self.assertEqual(json.loads((Path(temp) / 'acquisition.json').read_text())['state'], 'isbn_mismatch')

    def test_feature_description_does_not_become_reading_order_or_named_story(self):
        packet = self.packet()
        packet['constraints']['isbnMatched'] = True
        issue = self.task()['issue']
        prepared = {'contents': solo.trial.inventory(packet), 'researchQueue': []}
        pages = [{'state': 'draft', 'sourceUrl': solo.FEATURED_LIST, 'title': 'Start Here', 'features': [
            {'issue': issue, 'issueUrl': 'https://share.marvel.com/comics/issue/1/example',
             'identityQuote': 'Example (2020) #1', 'descriptionQuote': 'A hero escapes a time loop.', 'sourcePosition': 2}]}]
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            with patch.object(solo.intake, 'prepare', return_value=(packet, {'isbn': packet['book']['isbn'], 'sources': []}, prepared)), \
                    patch.object(solo.legacy, 'generate_stage', return_value={'summary': {}}):
                row = solo.process(packet['book'], folder, 'fake', refresh_edition=True,
                    edition_fetch=lambda isbn: (b'fixture', 'https://books.google.com/', 'utf-8'), featured_pages=pages)
            result = json.loads((folder / 'result.json').read_text())
            self.assertEqual(row['featuredDescriptions'], 1)
            self.assertEqual(row['namedStories'], 0)
            self.assertEqual(row['publisherPathPlacements'], 0)
            self.assertEqual(result['readingOrder']['state'], 'missing_evidence')
            self.assertEqual(row['collectionCoverage']['wholeIssuesWithPublisherDescription'], 1)

    def test_withheld_identity_conflicts_remain_in_coverage_counts(self):
        issue = self.task()['issue']
        result = {'contents': {'entries': [], 'unresolvedEntries': [{}], 'unparsed': [{}]},
                  'storyCoverage': {'issuesWithoutAnyStoryMapping': []}, 'readingOrder': {'publisherPaths': []},
                  'publisherIdentityConflicts': [{'issue': issue}, {'issue': issue}]}
        coverage = solo.collection_coverage(result)
        self.assertEqual(coverage['publisherIdentityMismatches'], 1)
        self.assertEqual(coverage['inventoriedWholeIssues'], 0)

    def test_missing_cache_attempts_isbn_lookup_and_records_http_failure(self):
        from urllib.error import HTTPError
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def missing(isbn):
                raise HTTPError('https://books.google.com/', 404, 'not found', {}, None)
            with patch.object(solo.legacy, 'ROOT', root):
                with self.assertRaises(HTTPError):
                    solo.process(self.packet()['book'], root, 'fake', edition_fetch=missing)
            self.assertEqual(json.loads((root / 'acquisition.json').read_text())['httpStatus'], 404)

    def test_end_to_end_automatic_discovery_fixture(self):
        packet, task = self.packet(), self.task()
        real_run = solo.trial.run
        def local_request(base, route, payload):
            return {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'stories': [{'source': 'D1', 'title': 'Story One'}]})}}]}
        def run(packet, supplement, model):
            return real_run(packet, supplement, model, request=local_request)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cache = root / 'data/cache'
            cache.mkdir(parents=True)
            (cache / 'google-9781302507046.html').write_text('fixture')
            folder = root / 'run'
            folder.mkdir()
            prepared = {'researchQueue': [task]}
            with patch.object(solo.legacy, 'ROOT', root), \
                    patch.object(solo.intake, 'prepare', return_value=(packet, {'isbn': '9781302507046', 'sources': []}, prepared)), \
                    patch.object(solo.trial, 'run', side_effect=run), \
                    patch.object(solo.legacy, 'generate_stage', return_value={'summary': {}}):
                report = solo.process(packet['book'], folder, 'fixture', 1, self.search,
                    lambda url: (b'<title>Example (2020) #1 - Story One (Issue)</title>', url, 'utf-8'))
            self.assertEqual(report['namedStories'], 1)
            self.assertEqual(report['searchQueries'], 1)
            self.assertEqual(report['decision'], 'review_required')
            self.assertTrue((folder / 'fetched/D1.html').exists())


if __name__ == '__main__':
    unittest.main()
