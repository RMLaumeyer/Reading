import unittest
import series_references as refs
import edition_trial
import solo_enrich


class SeriesReferenceTests(unittest.TestCase):
    url = 'https://prhcomics.com/book/?isbn=9781234567890'

    def reference(self, text='COLLECTING: Example (2020) 1-6, Other (2019) 1-4'):
        return refs.parse('<div>'+text+'</div><script>COLLECTING: Fake (2000) 1-9</script>', self.url)

    def packet(self, text='Collects Example #1-3.', references=None):
        return {'book': {'isbn': '9780000000000'}, 'constraints': {},
                'sources': [{'id': 'S1', 'text': 'Synopsis: '+text}],
                'seriesIdentityReferences': references or [self.reference()]}

    def test_reference_corroborates_year_but_never_transfers_donor_contents(self):
        result = edition_trial.inventory(self.packet())
        self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['entries']], [('Example',2020,1,3)])
        self.assertFalse(result['complete'])
        identity = result['entries'][0]['identityResolution']
        self.assertEqual(identity['membershipEvidence']['quote'], 'Example #1-3')
        self.assertEqual(identity['state'], 'draft')

    def test_conflicting_years_veto_even_when_one_range_does_not_overlap(self):
        result = edition_trial.inventory(self.packet(references=[self.reference(
            'COLLECTING: Example (2020) 1-6, Example (2010) 20-30')]))
        self.assertEqual(result['entries'], [])

    def test_known_compound_boundary_recovers_numbered_series_without_numbering_unnumbered_work(self):
        reference = self.reference('COLLECTING: Opening (2020), Example (2020) 1-6')
        packet = self.packet('Collects Opening And Example #1-3.', [reference])
        result = edition_trial.inventory(packet)
        self.assertEqual([(e['series'], e['first'], e['last']) for e in result['entries']], [('Example', 1, 3)])
        self.assertEqual(result['unparsed'], [{'source': 'S1', 'quote': 'Opening'}])
        self.assertFalse(result['complete'])

    def test_compound_split_needs_both_names_and_preserves_partial_scope(self):
        for line in ('COLLECTING: Example (2020) 1-6', 'COLLECTING: Opening (2020)'):
            result = edition_trial.inventory(self.packet('Collects Opening and Example #1-3.', [self.reference(line)]))
            self.assertEqual(result['entries'], [])
        reference = self.reference('COLLECTING: Opening (2020), Example (2020) 1-6')
        result = edition_trial.inventory(self.packet('Collects material from Opening & Example #1-3.', [reference]))
        self.assertEqual(result['entries'][0]['extent'], 'partial')
        result = edition_trial.inventory(self.packet('Collects Opening and Example #1-3.', [
            reference, self.reference('COLLECTING: Example (2010) 1-6')]))
        self.assertEqual(result['entries'], [])

    def test_known_compound_names_do_not_split_an_ordinary_title(self):
        reference = self.reference('COLLECTING: Ant-Man (2020), Wasp (2020) 1-6')
        result = edition_trial.inventory(self.packet('Collects Ant-Man and the Wasp #1-3.', [reference]))
        self.assertEqual(result['entries'], [])
        reference = self.reference('COLLECTING: Alpha (2020), Beta (2020) 1-6, Alpha and Beta (2021) 1-3')
        result = edition_trial.inventory(self.packet('Collects Alpha and Beta #1-3.', [reference]))
        self.assertEqual([(e['series'], e['year']) for e in result['entries']], [('Alpha and Beta', 2021)])

    def test_no_prefix_invention_or_out_of_range_matching(self):
        for text in ['Collects Example #7-8.', 'Collects Short Name #1-3.']:
            result = edition_trial.inventory(self.packet(text, [self.reference(
                'COLLECTING: Example (2020) 1-6, Event: Short Name (2019) 1-4')]))
            self.assertEqual(result['entries'], [])

    def test_typography_only_normalization_and_partial_extent_survive(self):
        packet = self.packet('Collects material from Example-One #1-2.',
                             [self.reference('COLLECTING: Example One (2020) 1-3')])
        entry = edition_trial.inventory(packet)['entries'][0]
        self.assertEqual(entry['extent'], 'partial')
        self.assertEqual(entry['year'], 2020)

    def test_edition_conflict_cannot_be_overridden_by_another_book(self):
        packet = self.packet(); packet['constraints']['contentsConflict'] = True
        self.assertEqual(edition_trial.inventory(packet)['entries'], [])

    def test_scripts_and_undated_rows_never_supply_years(self):
        self.assertEqual(len(refs.rows_from_lines(self.reference()['collectingLines'])), 2)
        with self.assertRaises(ValueError):
            refs.parse('<script>COLLECTING: Example (2020) 1-3</script><div>COLLECTING: Example #1-3</div>', self.url)

    def test_arbitrary_urls_are_rejected(self):
        for url in ['http://prhcomics.com/book/?isbn=9781234567890',
                    self.url+'&secret=1', self.url.replace('prhcomics.com','evil.example'),
                    self.url.replace('/book/', '/private/')]:
            with self.assertRaises(ValueError): refs.check_url(url)

    def test_registration_selects_sources_not_similarly_named_events(self):
        self.assertEqual(len(solo_enrich.known_series_references([{'title':'Annihilation Book Two'}])),2)
        self.assertEqual(solo_enrich.known_series_references([{'title':'Annihilation: Conquest Book One'}]),[])


if __name__ == '__main__': unittest.main()
