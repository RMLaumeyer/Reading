import unittest
from unittest.mock import patch
import edition_sources as sources


class IntakeTests(unittest.TestCase):
    def raw(self, rows):
        return '<div id="toc"><table>' + ''.join('<tr><td class="toc_entry"><div><span>'+r+'</span></div></td><td class="toc_number">99</td></tr>' for r in rows) + '</table></div>'

    def packet(self, text='Collects Example (2020) #1-2.'):
        return {'book': {'isbn': '9781302507046'}, 'constraints': {}, 'sources': [{
            'id': 'S1', 'url': 'https://books.google.com/books?id=example',
            'text': text+'\nBibliographic information: ISBN 9781302507046'}]}

    def prepare(self, rows, packet=None):
        with patch.object(sources, 'packet_from_html', return_value=packet or self.packet()):
            return sources.prepare({'isbn': '9781302507046'}, self.raw(rows))

    def test_only_toc_cells_in_dom_order(self):
        raw = '<td class="toc_entry">Fake 8</td><script>Fake 9</script>' + self.raw(['Example 2', 'Example 1'])
        self.assertEqual(sources.ContentsParser(raw).rows, ['Example 2', 'Example 1'])

    def test_preparation_gets_order_and_queue_without_inventing_titles(self):
        packet, supplement, intake = self.prepare(['Example 2', 'Example 1', 'Copyright'])
        self.assertEqual(supplement['editionContentsOrder']['rows'], ['Example 2', 'Example 1'])
        self.assertEqual(supplement['sources'], [])
        self.assertEqual(len(intake['researchQueue']), 2)
        self.assertEqual(intake['omittedNonStoryRows'], ['Copyright'])

    def test_unknown_row_is_not_silently_dropped(self):
        _, supplement, intake = self.prepare(['Example 1', 'Special Bonus Story', 'Example 2'])
        self.assertNotIn('editionContentsOrder', supplement)
        self.assertEqual(intake['orderState'], 'needs_review')
        self.assertIn('Special Bonus Story', intake['tocRows'])

    def test_wrong_isbn_missing_year_and_partial_contents_block_order(self):
        packets = [self.packet('Collects Example #1-2.'), self.packet('Collects Example (2020) #1 (D story), Example (2020) #2.')]
        wrong = self.packet()
        wrong['sources'][0]['text'] = wrong['sources'][0]['text'].replace('ISBN 9781302507046', 'ISBN 9781302507047')
        packets.append(wrong)
        for packet in packets:
            _, supplement, intake = self.prepare(['Example 1', 'Example 2'], packet)
            self.assertNotIn('editionContentsOrder', supplement)
            self.assertEqual(intake['orderState'], 'needs_review')

    def test_no_toc_keeps_explicit_missing_state(self):
        _, supplement, intake = self.prepare([])
        self.assertEqual(intake['orderState'], 'missing_evidence')
        self.assertNotIn('editionContentsOrder', supplement)

    def test_absent_contents_and_conflicting_contents_get_distinct_tasks(self):
        _, _, intake = self.prepare([], self.packet('Synopsis: A story premise.'))
        self.assertEqual(intake['researchQueue'][0]['kind'], 'edition_contents')
        packet = self.packet()
        packet['constraints']['contentsConflict'] = True
        _, _, intake = self.prepare([], packet)
        self.assertTrue(intake['contents']['conflict'])
        self.assertEqual([q['kind'] for q in intake['researchQueue']], ['edition_conflict'])

    def test_unresolved_identity_gets_a_research_task_even_without_accepted_issues(self):
        _, _, intake = self.prepare([], self.packet('Collects Example #1-2.'))
        self.assertEqual(intake['researchQueue'][0]['kind'], 'series_identity')
        self.assertEqual(len(intake['researchQueue']), 1)

    def test_fallback_cannot_clear_existing_or_new_range_conflict(self):
        book = {'isbn': '9781302507046', 'title': 'Example: Issues #1-3'}
        extra = {'id': 'OD1', 'url': 'https://knoxcounty.overdrive.com/media/123',
                 'kind': 'OverDrive public edition metadata', 'editionIsbn': book['isbn'],
                 'description': 'Collects Example (2020) #1-3.',
                 'text': 'Synopsis: Collects Example (2020) #1-3.'}
        packet = self.packet('Collects Example (2020) #1-2.')
        packet['constraints']['contentsConflict'] = True
        with patch.object(sources, 'packet_from_html', return_value=packet):
            _, _, intake = sources.prepare(book, self.raw([]), [extra])
        self.assertTrue(intake['contents']['conflict'])
        self.assertEqual(intake['contents']['entries'], [])
        packet = self.packet('No contents supplied.')
        extra['description'] = 'Collects Example (2020) #1-5.'
        with patch.object(sources, 'packet_from_html', return_value=packet):
            _, _, intake = sources.prepare(book, self.raw([]), [extra])
        self.assertTrue(intake['contents']['conflict'])


if __name__ == '__main__':
    unittest.main()
