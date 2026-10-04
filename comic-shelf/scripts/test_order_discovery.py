from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError
import order_discovery as discovery
import guide_order


class IndexTests(unittest.TestCase):
    def test_exact_event_index_ignores_sequel_foreign_link_and_script(self):
        raw='''<a href="/marvel/events/example-reading-order/">Example (2020)</a>
        <a href="/marvel/events/example-conquest-reading-order/">Example Conquest (2021)</a>
        <a href="https://evil.test/marvel/events/example-reading-order/">Example (2020)</a>
        <script><a href="/marvel/events/example-reading-order/">Example</a></script>'''
        matches=discovery.candidates(raw,'cbro','example')
        self.assertEqual(len(matches),1)
        self.assertTrue(matches[0]['url'].endswith('/example-reading-order/'))
        self.assertEqual(discovery.candidates(raw,'cbro','unregistered'),[])

    def test_index_label_cannot_redirect_selection_to_another_event(self):
        self.assertEqual(discovery.candidates('<a href="/marvel/events/other-reading-order/">Example</a>','cbro','example'),[])

    def test_sitemap_uses_page_locations_not_image_metadata(self):
        raw='''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="https://example.test/image">
        <url><loc>https://marvelguides.com/example-reading-order</loc><image:loc>https://evil.test/example-reading-order</image:loc></url>
        <url><loc>https://marvelguides.com/example-conquest-reading-order</loc></url></urlset>'''
        result=discovery.candidates(raw,'marvelguides','example')
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['sectionSelection'],'all_explicit_reading_lists')

    def test_dtd_and_unrecognized_sitemap_fail_closed(self):
        for raw in ('<!DOCTYPE root><urlset/>','<!ENTITY x "foo"><urlset/>','<sitemapindex/>'):
            with self.assertRaises(ValueError):discovery.candidates(raw,'marvelguides','example')

    def test_missing_index_retains_other_source_and_failure(self):
        def fetch(url):
            if url.endswith('sitemap.xml'):raise HTTPError(url,403,'sensitive',{},None)
            return b'<a href="/marvel/events/example-reading-order/">Example (2020)</a>','utf-8'
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'new'
            sources,report=discovery.acquire('example',folder,fetch)
            self.assertEqual(len(sources),1)
            self.assertEqual(report[1]['httpStatus'],403)
            self.assertNotIn('sensitive',(folder/'report.json').read_text())

    def test_full_page_section_selection_is_explicit_not_a_core_guess(self):
        raw='<p>Part 1: Event</p><p>Part 1.1: Before</p><p>Reading Order:</p><li>A #1</li><p>Collected Editions:</p><li>Book</li><p>Part 1.2: Core</p><p>Reading Order:</p><li>B #1</li>'
        self.assertEqual(guide_order.sections_with_lists(raw),['Part 1.1: Before','Part 1.2: Core'])
        with self.assertRaises(ValueError):guide_order.sections_with_lists('<p>No list here</p>')
