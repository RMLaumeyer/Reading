import copy
import json
import unittest
from unittest.mock import patch
import edition_trial as trial


class EditionTests(unittest.TestCase):
    def test_sergeant_abbreviation_keeps_list_without_resolving_year_or_annual(self):
        for title in ('SGT. FURY', 'Sgt. Fury', 'sgt. Fury'):
            packet=self.packet('Collecting '+title+' #20-36 and ANNUAL #1-2. A separate story begins.')
            packet['book']={'isbn':'9781302524357'}
            packet['sources'][0]['text']+=' Bibliographic information: Volume 3 of Sgt. Fury Epic Collection (2019). ISBN 9781302524357'
            result=trial.inventory(packet)
            self.assertEqual(result['entries'],[])
            self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['unresolvedEntries']],
                             [(title,None,20,36),('ANNUAL',None,1,2)])
            self.assertEqual([e['quote'] for e in result['unparsed']],
                             [title+' #20-36','ANNUAL #1-2'])
            self.assertFalse(result['complete'])

    def test_sergeant_abbreviation_does_not_hide_real_sentence_or_variant_boundaries(self):
        quote='Sgt. Fury (1963) #20-36'
        result=trial.inventory(self.packet('Collects '+quote+'. Sgt. Fury faces another threat.'))
        self.assertEqual([e['evidence']['quote'] for e in result['entries']],[quote])
        self.assertEqual(result['unparsed'],[])
        for suffix in ('#20.1','#20.AU','#36-20'):
            malformed=trial.inventory(self.packet('Collects SGT. FURY (1963) '+suffix))
            self.assertEqual(malformed['entries'],[])
            self.assertTrue(malformed['unparsed'])

    def test_versus_abbreviation_keeps_entire_collecting_title(self):
        for title in ('Black Panther vs. Deadpool','Black Panther Vs. Deadpool'):
            quote=title+' (2018) #1-5'
            result=trial.inventory(self.packet('Collects '+quote+'. A separate story begins.'))
            self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['entries']],[(title,2018,1,5)])
            self.assertEqual(result['entries'][0]['evidence']['quote'],quote)
            self.assertEqual(result['unparsed'],[])

    def test_versus_title_without_year_stays_unresolved(self):
        result=trial.inventory(self.packet('Collects Black Panther vs. Deadpool #1-5. A plot begins.'))
        self.assertEqual(result['entries'],[])
        self.assertEqual(result['unresolvedEntries'][0]['series'],'Black Panther vs. Deadpool')
        self.assertIsNone(result['unresolvedEntries'][0]['year'])

    def test_unnumbered_special_and_embedded_material_scope_stay_unparsed(self):
        for conjunction in ('and material from','And Material From','AND MATERIAL FROM'):
            compound='Anniversary Special '+conjunction+' Beta (2023) #1'
            result=trial.inventory(self.packet('Collects Alpha (2020) #1, '+compound+', #3.'))
            self.assertEqual([(e['series'],e['extent']) for e in result['entries']],[('Alpha','whole')])
            self.assertEqual([e['quote'] for e in result['unparsed']],[compound,'#3'])
            self.assertEqual(result['unresolvedEntries'],[])

    def test_embedded_material_scope_cannot_become_a_disjoint_series(self):
        result=trial.inventory(self.packet('Collects Anniversary Special and material from Beta (2023) #1 & #3.'))
        self.assertEqual(result['entries'],[])
        self.assertEqual(result['unresolvedEntries'],[])
        self.assertTrue(result['unparsed'])

    def test_space_before_period_separates_two_word_prose_name(self):
        result=trial.inventory(self.packet('Collects Legion (2018) #1-5 .David Haller, the son of Charles Xavier, has a problem.'))
        self.assertEqual([(e['series'],e['first'],e['last']) for e in result['entries']],[('Legion',1,5)])
        self.assertEqual(result['entries'][0]['evidence']['quote'],'Legion (2018) #1-5')
        self.assertEqual(result['unparsed'],[])
        missing=trial.inventory(self.packet('Collects Legion #1-5 .David Haller, the son of Charles Xavier, has a problem.'))
        self.assertEqual(missing['entries'],[])
        self.assertEqual(missing['unresolvedEntries'][0]['series'],'Legion')

    def test_proper_name_boundary_never_truncates_variants_or_decimals(self):
        for suffix in ('#1.1','#1.AU','#1.David Haller','#1 .AU','#1 .David'):
            result=trial.inventory(self.packet('Collects Alpha (2020) '+suffix))
            self.assertEqual(result['entries'],[])
            self.assertTrue(result['unparsed'])

    def test_conjoined_material_clause_never_becomes_a_whole_issue_series(self):
        result=trial.inventory(self.packet('Collects Alpha (1993) #35; And Material From Alpha (1993) #34, #36, #40-43, #48.'))
        self.assertEqual([e['series'] for e in result['entries']],['Alpha']*5)
        self.assertEqual([e['extent'] for e in result['entries']],['whole']+['partial']*4)
        self.assertEqual(result['entries'][1]['evidence']['quote'],'And Material From Alpha (1993) #34')
        self.assertTrue(all(e['portion']=='unspecified material' for e in result['entries'][1:]))

    def test_conjoined_partial_clause_preserves_missing_year_and_source_boundary(self):
        packet=self.packet('Collects Alpha (2020) #1; and material from Beta #2, #4.')
        packet['sources'].append({'id':'S2','text':'Collects Gamma (2021) #1.'})
        result=trial.inventory(packet)
        self.assertEqual([(e['series'],e['extent']) for e in result['entries']],[('Alpha','whole'),('Gamma','whole')])
        self.assertTrue(all(e['extent']=='partial' and e['year'] is None for e in result['unresolvedEntries']))
        self.assertEqual(len(result['unresolvedEntries']),2)

    def test_recovered_hash_range_cannot_hide_catalog_disagreement(self):
        packet=self.packet('Collects Alpha (2020) #11-#13.')
        packet['constraints']={'isbnMatched':True,'catalogRange':[11,14],'contentsConflict':False}
        result=trial.inventory(packet)
        self.assertEqual(result['catalogRangeDisagreement']['sourceRange'],[11,13])
        self.assertEqual(result['catalogRangeDisagreement']['catalogRange'],[11,14])
        packet['sources'].append({'id':'OD1','text':'Collects Alpha (2020) #11-13.'})
        self.assertIn('catalogRangeDisagreement',trial.inventory(packet))

    def test_matching_range_and_complex_or_partial_lists_do_not_trigger_single_range_check(self):
        for text in ('Collects Alpha (2020) #11-14.',
                     'Collects Alpha (2020) #11-13, Beta (2021) #1.',
                     'Collects material from Alpha (2020) #11-13.'):
            packet=self.packet(text)
            packet['constraints']={'isbnMatched':True,'catalogRange':[11,14]}
            self.assertNotIn('catalogRangeDisagreement',trial.inventory(packet))
    def test_range_endpoint_hash_keeps_original_evidence_and_gaps(self):
        text='Collects Alpha (2020) #1-#3, #8-#9 and Beta (2021) #4–#6.'
        result=trial.inventory(self.packet(text))
        self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['entries']],
                         [('Alpha',2020,1,3),('Alpha',2020,8,9),('Beta',2021,4,6)])
        self.assertEqual([e['evidence']['quote'] for e in result['entries']],
                         ['Alpha (2020) #1-#3','#8-#9','Beta (2021) #4–#6'])
        self.assertEqual(result['unparsed'],[])

    def test_endpoint_hash_preserves_partial_scope_and_missing_year(self):
        result=trial.inventory(self.packet('Collects material from Alpha (2020) #1-#3, #8-#9.'))
        self.assertTrue(all(e['extent']=='partial' for e in result['entries']))
        missing=trial.inventory(self.packet('Collects Alpha #1-#3 & #8-#9.'))
        self.assertEqual(missing['entries'],[])
        self.assertEqual([(e['first'],e['last']) for e in missing['unresolvedEntries']],[(1,3),(8,9)])

    def test_endpoint_hash_never_truncates_variants_decimals_or_reversed_ranges(self):
        for issue in ('#1-#3.1','#1-#3A','#1-##3','#9-#2','#1-#999'):
            with self.subTest(issue=issue):
                result=trial.inventory(self.packet('Collects Alpha (2020) '+issue))
                self.assertEqual(result['entries'],[])
                self.assertTrue(result['unparsed'])

    def test_question_mark_title_before_issue_number_is_not_a_plot_boundary(self):
        for title in ('What If…? Venom','What If...? Venom','Who Do You Trust?'):
            quote=title+' (2024) #1-5'
            result=trial.inventory(self.packet('Collects '+quote+'. A separate plot begins.'))
            self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['entries']],[(title,2024,1,5)])
            self.assertEqual(result['entries'][0]['evidence']['quote'],quote)
            self.assertEqual(result['unparsed'],[])

    def test_question_mark_title_missing_year_still_requires_identity_review(self):
        result=trial.inventory(self.packet('Collects What If…? Venom #1-5. A plot begins.'))
        self.assertEqual(result['entries'],[])
        self.assertEqual(result['unresolvedEntries'][0]['series'],'What If…? Venom')
        self.assertIsNone(result['unresolvedEntries'][0]['year'])

    def test_title_question_protection_does_not_swallow_plot_or_unknown_suffix(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1-3. Who rules the city? Ask Alpha #4.'))
        self.assertEqual([(e['first'],e['last']) for e in result['entries']],[(1,3)])
        self.assertEqual(result['unparsed'],[])
        malformed=trial.inventory(self.packet('Collects What If…? Venom (2024) #1-#5.AU'))
        self.assertEqual(malformed['entries'],[])

    def test_thousands_in_titles_or_numbers_never_create_phantom_issues(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #46-62, Avengers 1,000,000 BC #1'))
        self.assertEqual([(e['series'],e['first'],e['last']) for e in result['entries']],[('Alpha',46,62)])
        self.assertEqual(result['unparsed'][0]['quote'],'Avengers 1,000,000 BC #1')
        self.assertEqual(trial.inventory(self.packet('Collects Alpha (2020) #1,100'))['entries'],[])
        spaced=trial.inventory(self.packet('Collects Alpha (2020) #1, #100'))
        self.assertEqual([e['first'] for e in spaced['entries']],[1,100])

    def test_comma_shorthand_and_following_series_do_not_merge(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1, #4 and #7, #9 and material from Beta (2021) #2, #5.'))
        self.assertEqual([(e['series'],e['first']) for e in result['entries']],
                         [('Alpha',1),('Alpha',4),('Alpha',7),('Alpha',9),('Beta',2),('Beta',5)])
        self.assertEqual([e['extent'] for e in result['entries']],['whole']*4+['partial']*2)
        self.assertEqual(result['unparsed'],[])

    def test_malformed_equals_title_does_not_become_a_new_series(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1, #4 and = Beta (2021) #2'))
        self.assertEqual([(e['series'],e['first']) for e in result['entries']],[('Alpha',1),('Alpha',4)])
        self.assertEqual(result['unparsed'][0]['quote'],'= Beta (2021) #2')

    def test_abbreviated_series_names_keep_literal_collecting_evidence(self):
        for name in ('Ms. Marvel', 'Mr. Fantastic', 'Dr. Strange', 'Agents of S.H.I.E.L.D.'):
            with self.subTest(name=name):
                quote=name+' (2020) #1-5'
                result=trial.inventory(self.packet('Synopsis: Collects '+quote+'. A plot begins.'))
                self.assertEqual([(e['series'],e['year'],e['first'],e['last']) for e in result['entries']],[(name,2020,1,5)])
                self.assertEqual(result['entries'][0]['evidence']['quote'],quote)
                self.assertEqual(result['unparsed'],[])

    def test_comma_issue_shorthand_retains_gap_and_context_evidence(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1-3, #7-8, 11. A story.'))
        self.assertEqual([(e['first'],e['last']) for e in result['entries']],[(1,3),(7,8),(11,11)])
        self.assertEqual([e['evidence']['quote'] for e in result['entries']],['Alpha (2020) #1-3','#7-8','11'])
        self.assertEqual(result['entries'][1]['seriesContext'],{'source':'S1','quote':'Alpha (2020) #1-3'})
        self.assertEqual(result['entries'][2]['seriesContext'],result['entries'][1]['seriesContext'])
        self.assertEqual(result['unparsed'],[])
        self.assertFalse(result['complete'])

    def test_shorthand_preserves_partial_scope_and_missing_year(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1, material from #4-5, #8'))
        self.assertEqual([e['extent'] for e in result['entries']],['whole','partial','partial'])
        unresolved=trial.inventory(self.packet('Collects Alpha #1, #4-5'))
        self.assertEqual(unresolved['entries'],[])
        self.assertEqual(len(unresolved['unresolvedEntries']),2)
        self.assertTrue(all(e['year'] is None for e in unresolved['unresolvedEntries']))

    def test_shorthand_never_inherits_across_unknown_text_or_sources(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1, epilogue, #4'))
        self.assertEqual([(e['first'],e['last']) for e in result['entries']],[(1,1)])
        self.assertEqual([e['quote'] for e in result['unparsed']],['epilogue','#4'])
        packet=self.packet('Collects Alpha (2020) #1')
        packet['sources'].append({'id':'S2','text':'Collects #4-5'})
        self.assertEqual(len(trial.inventory(packet)['entries']),1)

    def test_shorthand_rejects_variants_reversed_ranges_and_unknown_qualifiers(self):
        for tail in ('#2.1','#2.AU','#5-3','#2 (cover)'):
            with self.subTest(tail=tail):
                result=trial.inventory(self.packet('Collects Alpha (2020) #1, '+tail+', #9'))
                self.assertEqual(len(result['entries']),1)
                self.assertEqual(len(result['unparsed']),2)

    def test_bare_annual_is_not_a_same_series_numeric_continuation(self):
        result=trial.inventory(self.packet('Collects Alpha (2020) #1-5, Annual #1, #3'))
        self.assertEqual(len(result['entries']),1)
        self.assertEqual([e['series'] for e in result['unresolvedEntries']],['Annual','Annual'])
        self.assertTrue(all(e['year'] is None for e in result['unresolvedEntries']))

    def test_undated_ampersand_ranges_stay_unresolved_and_keep_gaps(self):
        result=trial.inventory(self.packet('Collects Alpha #1-3 & #8-9'))
        self.assertEqual(result['entries'],[])
        self.assertEqual([(e['first'],e['last']) for e in result['unresolvedEntries']],[(1,3),(8,9)])

    def test_who_and_quoted_plot_openers_do_not_get_swallowed(self):
        for ending in ('.Who is the hero?', '. "A new adventure begins!"'):
            result=trial.inventory(self.packet('Collects Alpha (2020) #1-5'+ending))
            self.assertEqual([(e['first'],e['last']) for e in result['entries']],[(1,5)])
            self.assertEqual(result['unparsed'],[])
        for tail in ('.Who','.WHO','.A','.AU'):
            self.assertEqual(trial.inventory(self.packet('Collects Alpha (2020) #1'+tail))['entries'],[])

    def test_formal_collecting_label_wins_over_casual_prose_but_not_two_lists(self):
        text='A volume collecting many early adventures. Collecting Alpha (2020) #1-5.'
        result=trial.inventory(self.packet(text))
        self.assertEqual([(e['series'],e['last']) for e in result['entries']],[('Alpha',5)])
        two=trial.inventory(self.packet('Collects Alpha (2020) #1-5. A plot. Collects Beta (2021) #1-5.'))
        self.assertEqual(two['entries'],[])
        self.assertTrue(two['unparsed'])

    def test_generic_giant_size_label_requires_series_identity(self):
        bad=trial.inventory(self.packet('Collects Alpha (2020) #1, Giant-Size (1974) #1, #3'))
        self.assertEqual(len(bad['entries']),1)
        self.assertEqual(len(bad['unparsed']),2)
        good=trial.inventory(self.packet('Collects Giant-Size Alpha (1974) #1'))
        self.assertEqual(good['entries'][0]['series'],'Giant-Size Alpha')

    def test_ampersand_between_series_preserves_title_and_disjoint_ranges(self):
        text = 'Alpha & Omega (2000) #1-4 & Beta (2001) #2-3'
        result = trial.inventory(self.packet('Collects '+text))
        self.assertEqual([(e['series'], e['first'], e['last']) for e in result['entries']],
                         [('Alpha & Omega', 1, 4), ('Beta', 2, 3)])
        self.assertEqual(trial.collecting_chunks('Alpha (2000) #1-3 & #5-6'), ['Alpha (2000) #1-3 & #5-6'])

    def packet(self, text='Collecting Example (2020) #1-4, Annual (2024) 1 (D story)'):
        return {'book': {'isbn': '123'}, 'sources': [{'id': 'S1', 'text': text}], 'constraints': {}}

    def source(self):
        return {'id': 'P1', 'url': 'https://example.org/issue',
                'issue': {'series': 'Example', 'year': 2020, 'number': 1},
                'text': 'TEST ARC - PART ONE!'}

    def claim(self):
        return {'source': 'P1', 'arc': 'TEST ARC', 'part': 1}

    def test_original_unicode_evidence_is_attached_without_model_retyping(self):
        source = self.source()
        source['text'] = '“TEST ARC” - PART ONE!'
        result = trial.supported_parts({'parts': [self.claim()]}, [source], trial.inventory(self.packet()))
        self.assertEqual(result[0]['quote'], source['text'])

    def test_partial_story_retained_without_becoming_whole_issue(self):
        result = trial.inventory(self.packet())
        self.assertEqual(result['entries'][1]['extent'], 'partial')
        self.assertEqual(result['entries'][1]['portion'], 'D story')
        self.assertFalse(result['complete'])

    def test_collecting_sentence_excludes_following_plot_and_creator_prose(self):
        result = trial.inventory(self.packet('Synopsis: Collects Example (2020) #1-4. A villain attacks, then a hero responds. Writer Jane Smith returns.'))
        self.assertEqual(len(result['entries']), 1)
        self.assertEqual(result['entries'][0]['last'], 4)
        self.assertEqual(result['unparsed'], [])

    def test_missing_space_after_collecting_sentence_does_not_swallow_plot(self):
        result = trial.inventory(self.packet('Collects Example (2020) #1-4.The story starts here, with danger.'))
        self.assertEqual([(e['first'], e['last']) for e in result['entries']], [(1, 4)])
        self.assertEqual(result['unparsed'], [])

    def test_decimal_issue_and_variant_suffix_are_not_sentence_boundaries(self):
        for text in ('Example (2020) #1.1', 'Example (2020) #1.A', 'Example (2020) #1.AU'):
            result = trial.inventory(self.packet('Collects '+text))
            self.assertEqual(result['entries'], [])
            self.assertTrue(result['unparsed'])

    def test_material_scope_and_unknown_entries_preserved(self):
        result = trial.inventory(self.packet('Collects Example (2020) #1-4, material from Annual (2024) #1, Mystery #2'))
        self.assertEqual(result['entries'][1]['extent'], 'partial')
        self.assertEqual(result['unparsed'][0]['quote'], 'Mystery #2')

    def test_conflict_withholds_dependent_inventory(self):
        packet = self.packet()
        packet['constraints']['contentsConflict'] = True
        self.assertEqual(trial.inventory(packet)['entries'], [])

    def test_material_from_conjunction_keeps_two_distinct_partial_issues(self):
        result = trial.inventory(self.packet('Collects Miles Morales: Spider-Man (2022) #27-29, material from Miles Morales: Spider-Man Annual (2024) #1 and Miles Morales: Spider-Man (2022) #25.'))
        self.assertEqual([e['series'] for e in result['entries']], ['Miles Morales: Spider-Man', 'Miles Morales: Spider-Man Annual', 'Miles Morales: Spider-Man'])
        self.assertEqual([e['extent'] for e in result['entries']], ['whole', 'partial', 'partial'])
        self.assertEqual(result['unparsed'], [])

    def test_series_conjunction_is_not_a_separator(self):
        result = trial.inventory(self.packet('Collects Ant-Man and the Wasp (2018) #1-5 and Example (2020) #1-2'))
        self.assertEqual([e['series'] for e in result['entries']], ['Ant-Man and the Wasp', 'Example'])

    def test_disjoint_dated_ranges_preserve_gaps_and_source_quote(self):
        quote = 'Fantastic Four (1961) #300 & #357-358'
        result = trial.inventory(self.packet('Collects ' + quote))
        self.assertEqual([(e['first'], e['last']) for e in result['entries']], [(300, 300), (357, 358)])
        self.assertTrue(all(e['evidence']['quote'] == quote for e in result['entries']))
        self.assertEqual(result['unparsed'], [])

    def test_disjoint_ranges_keep_partial_scope_and_do_not_guess_bad_ranges(self):
        result = trial.inventory(self.packet('Collects material from Example (2020) #1 & #3-4'))
        self.assertEqual([e['extent'] for e in result['entries']], ['partial', 'partial'])
        for text in ('Example (2020) #1 & #5-3', 'Example (2020) #1 & epilogue',
                     'Example (2020) #1 & #2 (cover)', 'Example #1 & #3'):
            result = trial.inventory(self.packet('Collects ' + text))
            self.assertEqual(result['entries'], [])
            self.assertTrue(result['unparsed'])

    def test_markerless_list_recovers_known_year_but_preserves_unknown_identity(self):
        result = trial.inventory(self.packet('Synopsis: Spider-Man 2099 (2014) 1-5, Amazing Spider-Man 1 (2099 story)\nBibliographic information: other text'))
        self.assertEqual(result['entries'][0]['series'], 'Spider-Man 2099')
        unresolved = result['unresolvedEntries'][0]
        self.assertIsNone(unresolved['year'])
        self.assertEqual(unresolved['portion'], '2099 story')
        self.assertEqual(unresolved['extent'], 'partial')

    def test_markerless_plot_prose_is_not_collected_contents(self):
        result = trial.inventory(self.packet('Synopsis: Example (2020) #1-4. A hero meets a villain.'))
        self.assertEqual(result['entries'], [])

    def test_embedded_issue_cannot_be_part_of_a_series_name(self):
        result = trial.inventory(self.packet('Collects First (2020) #1 plus Second (2021) #2'))
        self.assertEqual(result['entries'], [])
        self.assertEqual(len(result['unparsed']), 1)

    def test_coverage_exposes_gaps_partial_material_and_unmapped_issues(self):
        contents = trial.inventory(self.packet())
        part = {**self.claim(), 'part': 3, 'issue': self.source()['issue']}
        coverage = trial.story_coverage(contents, [part], [self.source()])
        self.assertEqual(coverage['arcs'][0]['missingPartNumbers'], [1, 2])
        self.assertEqual([i['number'] for i in coverage['unmappedWholeIssues']], [2, 3, 4])
        self.assertEqual(coverage['partialStoriesNeedingIdentification'][0]['portion'], 'D story')
        self.assertFalse(coverage['complete'])

    def test_model_cannot_invent_part_or_title(self):
        for key, value in [('part', 2), ('arc', 'Invented arc')]:
            claim = self.claim()
            claim[key] = value
            with self.assertRaises(ValueError):
                trial.supported_parts({'parts': [claim]}, [self.source()], trial.inventory(self.packet()))

    def bounded_part(self, part, total=5, arc='TEST ARC'):
        return {**self.claim(), 'part': part, 'arc': arc, 'issue': {**self.source()['issue'], 'number': part},
                'quote': f'{arc} Part {part} of {total}'}

    def test_explicit_total_exposes_missing_tail(self):
        coverage = trial.story_coverage(trial.inventory(self.packet()), [self.bounded_part(1), self.bounded_part(2)], [])
        arc = coverage['arcs'][0]
        self.assertEqual(arc['missingPartNumbers'], [3, 4, 5])
        self.assertTrue(arc['endingEstablished'])
        self.assertFalse(arc['numberedSequenceComplete'])

    def test_complete_numbered_arc_is_not_complete_edition(self):
        coverage = trial.story_coverage(trial.inventory(self.packet()), [self.bounded_part(n, 4) for n in range(1, 5)], [])
        self.assertTrue(coverage['arcs'][0]['numberedSequenceComplete'])
        self.assertFalse(coverage['complete'])
        self.assertEqual(len(coverage['partialStoriesNeedingIdentification']), 1)

    def test_conflicting_totals_never_establish_complete_sequence(self):
        for parts in ([self.bounded_part(1, 4), self.bounded_part(2, 5)],
                      [self.bounded_part(1, 2), {**self.bounded_part(3), 'quote': 'TEST ARC Part 3'}]):
            arc = trial.story_coverage(trial.inventory(self.packet()), parts, [])['arcs'][0]
            self.assertTrue(arc['boundaryConflict'])
            self.assertFalse(arc['numberedSequenceComplete'])

    def test_unrelated_totals_and_issue_counts_do_not_set_arc_length(self):
        for text in ['TEST ARC Part 1. OTHER ARC Part 1 of 5', 'TEST ARC Part 1. Issue 1 of 5', 'TEST ARC Part 1 of 10000']:
            self.assertIsNone(trial.explicit_boundary({**self.claim(), 'quote': text}))

    def test_word_number_boundaries_keep_exact_evidence(self):
        boundary = trial.explicit_boundary({**self.claim(), 'quote': 'TEST ARC - Part One of Five'})
        self.assertEqual(boundary['totalParts'], 5)
        self.assertEqual(boundary['quote'], 'TEST ARC - Part One of Five')

    def test_different_arcs_do_not_become_one_reading_sequence(self):
        parts = [self.bounded_part(1, 1, 'FIRST'), self.bounded_part(2, 2, 'SECOND')]
        with patch.object(trial, 'extract_parts', return_value=parts), patch.object(trial.legacy, 'generate_stage', return_value={'summary': {'value': None, 'evidence': []}}):
            result = trial.run(self.packet(), None, 'fake')
        self.assertEqual(result['readingOrder']['orderedParts'], [])
        self.assertEqual(len(result['readingOrder']['arcs']), 2)
        self.assertEqual(result['readingOrder']['orderBetweenArcs'], 'unknown')

    def test_invalid_supplement_cannot_discard_independent_contents(self):
        invalid = [[self.source(), self.source()], [{'id': 'broken'}], None]
        for sources in invalid:
            with self.subTest(sources=sources), patch.object(trial.legacy, 'generate_stage', return_value={'summary': {'value': None, 'evidence': []}}), patch.object(trial.legacy, 'local_request') as request:
                result = trial.run(self.packet(), {'isbn': '123', 'sources': sources}, 'fake', request=request)
                request.assert_not_called()
                self.assertEqual(len(result['contents']['entries']), 2)
                self.assertEqual(result['readingOrder']['state'], 'failed')
                self.assertEqual(result['status'], 'partial')

    def test_partial_issue_cannot_support_whole_arc_part(self):
        contents = trial.inventory(self.packet('Collects Example (2020) #1 (D story)'))
        with self.assertRaises(ValueError):
            trial.supported_parts({'parts': [self.claim()]}, [self.source()], contents)

    def test_conflicting_part_mapping_is_rejected(self):
        source2 = copy.deepcopy(self.source())
        source2['id'] = 'P2'
        source2['issue']['number'] = 2
        claim2 = {**self.claim(), 'source': 'P2'}
        with self.assertRaises(ValueError):
            trial.supported_parts({'parts': [self.claim(), claim2]}, [self.source(), source2], trial.inventory(self.packet()))

    def test_duplicate_mapping_cannot_hide_contradictory_boundaries(self):
        first = {**self.source(), 'text': 'TEST ARC Part 1 of 4'}
        second = {**self.source(), 'id': 'P2', 'text': 'TEST ARC Part 1 of 5'}
        with self.assertRaises(ValueError):
            trial.supported_parts({'parts': [self.claim(), {**self.claim(), 'source': 'P2'}]}, [first, second], trial.inventory(self.packet()))

    def test_core_contents_survive_model_failure_and_synopsis_still_runs(self):
        supplement = {'isbn': '123', 'sources': [self.source()]}
        with patch.object(trial.legacy, 'generate_stage', return_value={'summary': {'value': None, 'evidence': []}}) as summary:
            result = trial.run(self.packet(), supplement, 'fake', request=lambda *a: (_ for _ in ()).throw(OSError('offline')))
        self.assertEqual(len(result['contents']['entries']), 2)
        self.assertEqual(result['status'], 'partial')
        self.assertIn('synopsis', result)
        self.assertIsNone(summary.call_args.kwargs['named_characters'])
        self.assertEqual(result['characters']['state'], 'not_requested')

    def test_gapless_prefix_does_not_claim_complete_order(self):
        response = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({'parts': [self.claim()]})}}]}
        with patch.object(trial.legacy, 'generate_stage', return_value={'summary': {'value': None, 'evidence': []}}):
            result = trial.run(self.packet(), {'isbn': '123', 'sources': [self.source()]}, 'fake', request=lambda *a: response)
        self.assertEqual(len(result['readingOrder']['orderedParts']), 1)
        self.assertFalse(result['readingOrder']['complete'])

    def bibliography_packet(self, bibliography='Volume 2 of Example (2020) ISBN 9781302507046'):
        packet = self.packet('Collects Example #0-4.\nBibliographic information: '+bibliography)
        packet['book']['isbn'] = '9781302507046'
        return packet

    def test_bibliographic_identity_preserves_both_source_spans(self):
        result = trial.inventory(self.bibliography_packet())
        entry = result['entries'][0]
        self.assertEqual((entry['year'], entry['first'], entry['last']), (2020, 0, 4))
        self.assertEqual(entry['evidence']['quote'], 'Example #0-4')
        evidence = entry['identityResolution']['evidence'][0]
        self.assertEqual(evidence['quote'], 'Volume 2 of Example (2020)')
        self.assertEqual(evidence['isbnQuote'], 'ISBN 9781302507046')
        self.assertEqual(result['unresolvedEntries'], [])
        self.assertEqual(result['unparsed'], [])
        self.assertFalse(result['complete'])

    def test_bibliographic_year_requires_exact_series_and_isbn(self):
        for bib in ['Volume 2 of Other Example (2020) ISBN 9781302507046',
                    'Volume 2 of Example Extra (2020) ISBN 9781302507046',
                    'Publisher Example, 2020 ISBN 9781302507046',
                    'Volume 2 of Example (2020) ISBN 9781302507047',
                    'Volume 2 of Example (2020) ISBN 1302507044',
                    'Volume 2 of Example (2020)',
                    'Volume 2 of Example (1800) ISBN 9781302507046']:
            with self.subTest(bib=bib):
                result = trial.inventory(self.bibliography_packet(bib))
                self.assertEqual(result['entries'], [])
                self.assertEqual(len(result['unresolvedEntries']), 1)

    def test_publisher_year_conflict_withholds_bibliographic_identity_without_substitution(self):
        packet = self.bibliography_packet()
        packet['constraints']['publisherYearConflicts'] = [{'issue': {'series': 'Example', 'year': 2019, 'number': 1},
                                                          'quote': 'Example (2019) #1', 'sourceUrl': 'https://example.org/list'}]
        result = trial.inventory(packet)
        self.assertEqual(result['entries'], [])
        self.assertIsNone(result['unresolvedEntries'][0]['year'])
        self.assertEqual(result['unresolvedEntries'][0]['identityConflicts'][0]['issue']['year'], 2019)
        packet['sources'][0]['text'] = 'Collects Example (2020) #1.'
        self.assertEqual(trial.inventory(packet)['entries'][0]['year'], 2020)

    def test_conflicting_bibliographic_years_abstain(self):
        packet = self.bibliography_packet('Volume 2 of Example (2020) Volume 1 of Example (1990) ISBN 9781302507046')
        self.assertEqual(trial.inventory(packet)['entries'], [])
        packet = self.bibliography_packet()
        packet['sources'].append({'id': 'S2', 'text': 'Bibliographic information: Volume 1 of Example (1990) ISBN 9781302507046'})
        self.assertEqual(trial.inventory(packet)['entries'], [])

    def test_identity_cannot_be_borrowed_from_other_source(self):
        packet = self.bibliography_packet('ISBN 9781302507046')
        packet['sources'].append({'id': 'S2', 'text': 'Bibliographic information: Volume 2 of Example (2020) ISBN 9781302507046'})
        self.assertEqual(trial.inventory(packet)['entries'], [])

    def test_wrong_edition_bibliography_does_not_override_matching_one(self):
        packet = self.bibliography_packet()
        packet['sources'].append({'id': 'S2', 'text': 'Bibliographic information: Volume 1 of Example (1990) ISBN 9781302507047'})
        self.assertEqual(trial.inventory(packet)['entries'][0]['year'], 2020)

    def test_bibliography_does_not_overwrite_explicit_year_or_conflict_gate(self):
        packet = self.bibliography_packet()
        packet['sources'][0]['text'] = packet['sources'][0]['text'].replace('Example #0-4', 'Example (1990) #0-4')
        result = trial.inventory(packet)
        self.assertEqual(result['entries'][0]['year'], 1990)
        self.assertNotIn('identityResolution', result['entries'][0])
        packet['constraints']['contentsConflict'] = True
        self.assertEqual(trial.inventory(packet)['entries'], [])

    def test_identity_resolution_keeps_partial_scope_and_other_gaps(self):
        packet = self.bibliography_packet()
        packet['sources'][0]['text'] = packet['sources'][0]['text'].replace('Example #0-4', 'Example #1 (D story), Missing #2')
        result = trial.inventory(packet)
        self.assertEqual(result['entries'][0]['extent'], 'partial')
        self.assertEqual(result['entries'][0]['portion'], 'D story')
        self.assertEqual(result['unresolvedEntries'][0]['series'], 'Missing')
        self.assertEqual(len(result['unparsed']), 1)

    def toc(self):
        return {'kind': 'table_of_contents', 'isbn': '123', 'url': 'https://example.org/book',
                'isbnQuote': 'ISBN 9781302507046', 'rows': ['Example 2', 'Example 1']}

    def toc_packet(self):
        packet = self.packet('Collects Example (2020) #1-2')
        packet['book']['isbn'] = '9781302507046'
        return packet

    def toc_evidence(self):
        return {**self.toc(), 'isbn': '9781302507046'}

    def test_toc_preserves_source_order_without_inventing_chronology(self):
        packet = self.toc_packet()
        result = trial.edition_contents_order(self.toc_evidence(), packet, trial.inventory(packet), [])
        self.assertEqual([x['issue']['number'] for x in result['orderedIssues']], [2, 1])
        self.assertTrue(result['coversAllInventoriedWholeIssues'])
        self.assertFalse(result['chronologyEstablished'])
        self.assertFalse(result['complete'])

    def test_toc_rejects_wrong_edition_and_missing_provenance(self):
        packet = self.toc_packet()
        for field, value in [('isbn', 'wrong'), ('isbnQuote', 'ISBN 9781302507047'),
                             ('kind', 'collecting_range'), ('url', ''), ('rows', ['Example 1-2']),
                             ('rows', ['Example 1', 'Example 1']), ('rows', ['Example 3'])]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                trial.edition_contents_order({**self.toc_evidence(), field: value}, packet, trial.inventory(packet), [])

    def test_toc_cannot_expand_partial_or_choose_ambiguous_series(self):
        for text in ['Collects Example (2020) #1 (D story), Example (2020) #2',
                     'Collects Example (2020) #1-2, Example (1990) #1-2']:
            packet = self.toc_packet()
            packet['sources'][0]['text'] = text
            with self.assertRaises(ValueError):
                trial.edition_contents_order(self.toc_evidence(), packet, trial.inventory(packet), [])

    def test_incomplete_toc_does_not_claim_inventory_coverage(self):
        packet = self.toc_packet()
        result = trial.edition_contents_order({**self.toc_evidence(), 'rows': ['Example 1']}, packet, trial.inventory(packet), [])
        self.assertFalse(result['coversAllInventoriedWholeIssues'])

    def test_without_toc_no_issue_number_sort_is_invented(self):
        packet = self.toc_packet()
        self.assertEqual(trial.edition_contents_order(None, packet, trial.inventory(packet), [])['orderedIssues'], [])

    def test_invalid_toc_keeps_independent_named_stories(self):
        titles = [{'title': 'Story', 'issue': self.source()['issue'], 'extent': 'whole'}]
        with patch.object(trial, 'extract_titles', return_value=titles), \
                patch.object(trial.legacy, 'generate_stage', return_value={'summary': {}}):
            result = trial.run(self.toc_packet(), {'isbn': '9781302507046', 'sources': [],
                'editionContentsOrder': self.toc()}, 'fake')
        self.assertEqual(result['namedStories'], titles)
        self.assertIn('editionContentsOrder', result['stageErrors'])
        self.assertIn('synopsis', result)

    def title_source(self):
        return {**self.source(), 'kind': 'story_title', 'text': 'Example #1 - A New Beginning'}

    def test_title_cleanup_removes_only_declared_footnote(self):
        source = {**self.title_source(), 'text': '4. "Prelude[ 1 ]"', 'titleFootnotes': ['[ 1 ]']}
        result = trial.supported_titles({'stories': [{'source': 'P1', 'title': '"Prelude[ 1 ]"'}]},
            [source], trial.inventory(self.packet()))[0]
        self.assertEqual(result['title'], 'Prelude')
        self.assertEqual(result['modelTitle'], '"Prelude[ 1 ]"')
        self.assertEqual(result['quote'], source['text'])
        self.assertEqual(trial.clean_story_title('Prelude[ 1 ]', {**source, 'titleFootnotes': []}), 'Prelude[ 1 ]')
        with self.assertRaises(ValueError):
            trial.clean_story_title('Prelude[ 1 ]', {**source, 'titleFootnotes': ['Prelude']})

    def test_matching_issue_heading_prefix_is_removed_and_audited(self):
        source = self.title_source()
        result = trial.supported_titles({'stories': [{'source': 'P1', 'title': source['text']}]},
            [source], trial.inventory(self.packet()))[0]
        self.assertEqual(result['title'], 'A New Beginning')
        self.assertEqual(result['modelTitle'], source['text'])
        self.assertEqual(result['quote'], source['text'])

    def test_title_cleanup_does_not_strip_arbitrary_hyphens(self):
        source = {**self.title_source(), 'text': 'Beginning - The End'}
        self.assertEqual(trial.clean_story_title(source['text'], source), source['text'])

    def test_named_story_needs_no_invented_part_number(self):
        stories = trial.supported_titles({'stories': [{'source': 'P1', 'title': 'A New Beginning'}]},
            [self.title_source()], trial.inventory(self.packet()))
        self.assertEqual(stories[0]['title'], 'A New Beginning')
        self.assertNotIn('part', stories[0])
        self.assertEqual(stories[0]['placement'], 'unknown')

    def test_partial_title_requires_exact_scope(self):
        source = {**self.title_source(), 'portion': 'D story'}
        claim = {'stories': [{'source': 'P1', 'title': 'A New Beginning'}]}
        contents = trial.inventory(self.packet('Collects Example (2020) #1 (D story)'))
        self.assertEqual(trial.supported_titles(claim, [source], contents)[0]['extent'], 'partial')
        for portion in [None, 'C story', 'unspecified material']:
            with self.assertRaises(ValueError):
                trial.supported_titles(claim, [{**source, 'portion': portion}], contents)

    def test_title_rejects_invention_unknown_source_and_unresolved_issue(self):
        for claim in [{'source': 'P1', 'title': 'Invented'}, {'source': 'unknown', 'title': 'A New Beginning'}]:
            with self.assertRaises(ValueError):
                trial.supported_titles({'stories': [claim]}, [self.title_source()], trial.inventory(self.packet()))
        with self.assertRaises(ValueError):
            trial.supported_titles({'stories': [{'source': 'P1', 'title': 'A New Beginning'}]},
                [self.title_source()], trial.inventory(self.packet('Collects Example #1')))

    def test_prelude_relation_requires_explicit_separate_evidence(self):
        claim = {'stories': [{'source': 'P1', 'title': 'A New Beginning'}]}
        source = {**self.title_source(), 'preludeTo': 'TEST ARC', 'relationText': 'Prelude to TEST ARC .'}
        story = trial.supported_titles(claim, [source], trial.inventory(self.packet()))[0]
        self.assertEqual(story['preludeTo'], 'TEST ARC')
        for relation in [None, 'Not a Prelude to TEST ARC', 'Prelude to OTHER ARC']:
            with self.assertRaises(ValueError):
                trial.supported_titles(claim, [{**source, 'relationText': relation}], trial.inventory(self.packet()))

    def test_title_sources_bypass_numbered_part_inference(self):
        with patch.object(trial.legacy, 'local_request') as request:
            self.assertEqual(trial.extract_parts('fake', [self.title_source()], trial.inventory(self.packet()), [], request), [])
            request.assert_not_called()

    def test_title_failure_keeps_numbered_sequence_and_synopsis(self):
        with patch.object(trial, 'extract_parts', return_value=[self.bounded_part(1)]), \
                patch.object(trial, 'extract_titles', side_effect=ValueError('invalid title')), \
                patch.object(trial.legacy, 'generate_stage', return_value={'summary': {'value': None, 'evidence': []}}):
            result = trial.run(self.packet(), None, 'fake')
        self.assertEqual(len(result['readingOrder']['orderedParts']), 1)
        self.assertIn('namedStories', result['stageErrors'])
        self.assertIn('synopsis', result)

    def test_partial_candidate_does_not_claim_complete_story_coverage(self):
        source = {**self.title_source(), 'portion': 'D story', 'preludeTo': 'TEST ARC',
                  'relationText': 'Prelude to TEST ARC'}
        packet = self.packet('Collects Example (2020) #1 (D story)')
        titles = trial.supported_titles({'stories': [{'source': 'P1', 'title': 'A New Beginning'}]}, [source], trial.inventory(packet))
        with patch.object(trial, 'extract_parts', return_value=[self.bounded_part(1)]), \
                patch.object(trial, 'extract_titles', return_value=titles), \
                patch.object(trial.legacy, 'generate_stage', return_value={'summary': {}}):
            result = trial.run(packet, None, 'fake')
        self.assertEqual(len(result['readingOrder']['preludeCandidates']), 1)
        self.assertEqual(len(result['storyCoverage']['partialStoriesNeedingIdentification']), 1)
        self.assertFalse(result['readingOrder']['complete'])


if __name__ == '__main__':
    unittest.main()
