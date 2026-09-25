import copy
import json
import unittest
from unittest.mock import patch
import edition_trial as trial


class EditionTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
