"""Offline guardrail checks only: no server, inference, or trial output."""
import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import local_ai_trial as trial


def empty_result():
    result = {key: {'value': None, 'evidence': []} for key in ['summary', 'pages', 'readingOrder', 'review']}
    result.update(stories=[], characters=[], issues=[], uncertainties=['Insufficient evidence'])
    return result


class TrialTests(unittest.TestCase):
    def test_descriptive_labels_are_withheld_but_named_people_and_teams_survive(self):
        names=["Marvel's silver-screen icons",'web-head','Mercs','Daughter','Peter Parker','Deadpool & Daughter','Heroes for Hire']
        part={'characters':[{'value':n,'evidence':[{'source':'S1','quote':n}]} for n in names]}
        logs=[]
        kept=trial.quarantine_character_roles({'sources':[]},part,logs)
        self.assertEqual([c['value'] for c in kept['characters']],names[4:])
        self.assertEqual([c['claim']['value'] for c in logs[0]['withheldCharacters']],names[:4])

    def test_suggestions_use_role_gate_even_when_model_misclassifies_every_name(self):
        text='Ben Reilly meets Peter Parker in faraway Wakanda. Writer Jane Smith explores the Spider-Verse.'
        packet={'sources':[{'id':'S1','text':'Synopsis: '+text}]}
        excerpts=trial.narrative_input(packet)
        first={'characters':[{'value':'Ben Reilly','evidence':[excerpts['E1']]}]}
        def request(base,path,payload):
            candidates=json.loads(payload['messages'][1]['content'])
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps({key:'character' for key in candidates})}}]}
        logs=[]
        result=trial.recover_characters('unused','fake',packet,excerpts,first,logs,request)
        self.assertEqual(result,first)
        quality=trial.quality_report(result,packet,logs,'draft')
        self.assertEqual(quality['suggestedNames'],['Peter Parker'])
        self.assertEqual(set(quality['withheldNames']),{'Wakanda','Jane Smith','Spider-Verse'})
        self.assertIn('not verified on-page',quality['characterScope'])

    def test_candidates_do_not_repeat_normalized_apostrophe_names(self):
        excerpts={'E1':{'source':'S1','quote':'Miguel O’Hara meets Peter Parker.'}}
        names=[c['name'] for c in trial.name_candidates(excerpts,["Miguel O'Hara"]).values()]
        self.assertEqual(names,['Peter Parker'])

    def test_optional_audit_failure_preserves_validated_characters_and_reports_warning(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Ben Reilly meets Peter Parker.'}]}
        first={'characters':[{'value':'Ben Reilly','evidence':[{'source':'S1','quote':'Ben Reilly meets Peter Parker.'}]}]}
        failures=[ValueError('Malformed response'),OSError('Connection failed'),KeyError('choices')]
        for failure in failures:
            with self.subTest(failure=str(failure)):
                logs=[]
                with patch.object(trial,'extract_characters',return_value=copy.deepcopy(first)),\
                     patch.object(trial,'recover_characters',side_effect=failure):
                    result=trial.generate_stage('unused','fake',packet,('characters',),logs,narrative_mode='extractive',audit_coverage=True)
                self.assertEqual(result,first)
                quality=trial.quality_report(result,packet,logs,'draft')
                self.assertIn(str(failure),quality['auditWarnings'][0])
                self.assertEqual(quality['suggestedNames'],[])
                self.assertFalse(quality['readyForPublication'])

    def test_primary_extraction_failure_still_fails_character_stage(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Ben Reilly returns.'}]}
        with patch.object(trial,'extract_characters',side_effect=ValueError('Invalid primary extraction')):
            with self.assertRaisesRegex(ValueError,'Invalid primary'):
                trial.generate_stage('unused','fake',packet,('characters',),[],narrative_mode='extractive',audit_coverage=True)

    def test_group_names_are_not_flagged_as_person_aliases(self):
        names=['Deadpool','Deadpool & Daughter','Peter','Peter Parker','Peter and Friends']
        result={'characters':[{'value':n,'evidence':[]} for n in names]}
        self.assertEqual(trial.quality_report(result,{},[],'draft')['possibleAliases'],
                         [{'short':'Peter','possibleFullNames':['Peter Parker']}])

    def test_contraction_prefix_is_not_part_of_candidate_name(self):
        for prefix in ["It's",'It’s']:
            excerpts={'E1':{'source':'S1','quote':prefix+' Spidey vs. the Deadpools!'}}
            names=[c['name'] for c in trial.name_candidates(excerpts,[]).values()]
            self.assertEqual(names,['Spidey','Deadpools'])

    def test_abbreviations_do_not_split_source_sentences(self):
        sentences=["It's Spidey vs. the Deadpools -- and even if Miles can survive a battle with two murderous Mercs, he'll have to face the terrifying threat pulling all these strings!",
                   'Dr. Strange meets Mr. Knight.']
        packet={'sources':[{'id':'S1','text':'Synopsis: '+' '.join(sentences)}]}
        excerpts=trial.narrative_input(packet)
        self.assertEqual([e['quote'] for e in excerpts.values()],sentences)
        self.assertEqual(trial.evidence_errors({'stories':[{'value':s,'evidence':[e]} for s,e in zip(sentences,excerpts.values())]},packet),[])

    def test_name_normalization_merges_surface_forms_not_identities(self):
        def c(name): return {'value':name,'evidence':[{'source':'S1','quote':name}]}
        names,changes=trial.normalize_characters([c('the Hobgoblin'),c('Hobgoblin'),c('Miguel O’Hara'),c("Miguel O'Hara"),c('Peter'),c('Peter Parker')])
        self.assertEqual([x['value'] for x in names],['Hobgoblin',"Miguel O'Hara",'Peter','Peter Parker'])
        self.assertEqual(len(names[0]['evidence']),2)
        self.assertTrue(changes)
        self.assertTrue(trial.literal_name("Miguel O'Hara",'Miguel O’Hara returns.'))

    def test_cast_above_ten_is_valid_and_never_truncated(self):
        claims=[{'value':f'Hero {i}','evidence':[{'source':'S1','quote':f'Hero {i}'}]} for i in range(12)]
        self.assertEqual(trial.validate_schema(claims,trial.SCHEMA['properties']['characters']),[])
        self.assertEqual(len(trial.normalize_characters(claims)[0]),12)

    def test_mixed_collecting_ranges_exclude_partial_story_and_preserve_exact_evidence(self):
        text='COLLECTING: Example (2020) 1-5, Other (2021) 11-12, Annual (2022) 1 (D story)'
        packet={'constraints':{},'sources':[{'id':'S1','text':'Synopsis: '+text}]}
        result=trial.structured_contents(packet)
        self.assertEqual([c['value'] for c in result['issues']],['Example (2020) #1-5','Other (2021) #11-12'])
        self.assertEqual(trial.issue_errors(result,packet),[])
        self.assertEqual(trial.evidence_errors(result,packet),[])
        self.assertTrue(any('Partial' in s for s in result['uncertainties']))

    def test_full_range_before_material_from_is_retained(self):
        text='Collects Example (2022) #27-29 and material from Annual (2024) #1 and Example (2022) #25.'
        packet={'constraints':{},'sources':[{'id':'S1','text':'Synopsis: '+text}]}
        self.assertEqual([c['value'] for c in trial.structured_contents(packet)['issues']],['Example (2022) #27-29'])

    def test_missing_series_year_is_not_borrowed_from_neighbor(self):
        text='Collecting Example (2008) #1-4, Other #1-4, Edge (2014) #1.'
        self.assertEqual([r['value'] for r in trial.contents_ranges(text)],['Example (2008) #1-4','Edge (2014) #1'])

    def test_summary_uses_specific_plot_over_long_vague_teaser(self):
        excerpts={'E1':{'source':'S1','quote':"But as heroes make their stand, Morlun isn't their only problem and things get worse."},
                  'E2':{'source':'S1','quote':'Shathra is back, even more powerful than the last time she nearly killed Peter and Ezekiel!'}}
        def request(base,path,payload):
            self.assertEqual(list(json.loads(payload['messages'][1]['content'])),['E2'])
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E2"]]}'}}]}
        trial.select_evidence('unused','fake',excerpts,'summary',[],request)

    def test_quality_distinguishes_conflict_missing_evidence_and_unfinished_fields(self):
        part={'issues':[],'review':{'value':None,'evidence':[]},'readingOrder':{'value':None,'evidence':[]},
              'characters':[{'value':'Peter','evidence':[]},{'value':'Peter Parker','evidence':[]}]}
        q=trial.quality_report(part,{'constraints':{'contentsConflict':True}},[],'error')
        self.assertIn('Conflicting',q['fields']['issues']['reason'])
        self.assertIn('No supported',q['fields']['readingOrder']['reason'])
        self.assertEqual(q['fields']['summary']['state'],'not_completed')
        self.assertEqual(q['possibleAliases'],[{'short':'Peter','possibleFullNames':['Peter Parker']}])
        self.assertFalse(q['readyForPublication'])

    def test_cli_failure_preserves_successful_fields_and_quality_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            trial.save(root/'config.json',{'books':[{'isbn':'1'}]})
            trial.save(root/'public/catalog.json',{'books':[{'isbn':'1','id':'b','title':'Test'}]})
            packet={'book':{'isbn':'1','title':'Test'},'sources':[],'constraints':{}}
            first={'issues':[],'pages':{'value':112,'evidence':[]},'uncertainties':[]}
            with patch.object(trial,'ROOT',root),patch.object(trial,'CONFIG',root/'config.json'),patch.object(trial,'OUT',root/'runs'),\
                 patch.object(trial,'source_packet',return_value=packet),patch.object(trial,'reference_snapshot',return_value={}),\
                 patch.object(trial,'local_request',return_value={'data':[{'id':'fake'}]}),patch.object(trial,'report'),\
                 patch.object(trial,'generate_stage',side_effect=[first,ValueError('Review stage failed')]),\
                 patch.object(sys,'argv',['local_ai_trial.py','run','--model','fake','--name','failure']),contextlib.redirect_stdout(io.StringIO()):
                trial.main()
            record=trial.read(root/'runs/failure/1.json')
            self.assertEqual(record['status'],'error')
            self.assertEqual(record['partialResult']['pages']['value'],112)
            self.assertEqual(record['quality']['fields']['summary']['state'],'not_completed')

    def test_role_quarantine_uses_context_and_preserves_supported_people(self):
        text="Spider-Man travels to faraway Wakanda. Writer Dan Slott and artist Mark Bagley tell the story."
        names=['Spider-Man','Wakanda','Dan Slott','Mark Bagley','Doctor Octopus']
        part={'characters':[{'value':n,'evidence':[{'source':'S1','quote':text}]} for n in names]}
        logs=[]
        result=trial.quarantine_character_roles({'sources':[{'id':'S1','text':text}]},part,logs)
        self.assertEqual([c['value'] for c in result['characters']],['Spider-Man','Doctor Octopus'])
        self.assertEqual(len(logs[0]['withheldCharacters']),3)
        self.assertIn('writer',logs[0]['withheldCharacters'][1]['roleEvidence']['quote'].lower())

    def test_setting_and_organization_names_are_withheld_not_deleted(self):
        names=['Spider-Verse','PARKER INDUSTRIES',"Miguel O'Hara"]
        part={'characters':[{'value':n,'evidence':[{'source':'S1','quote':n}]} for n in names]}
        logs=[]
        result=trial.quarantine_character_roles({'sources':[]},part,logs)
        self.assertEqual([c['value'] for c in result['characters']],["Miguel O'Hara"])
        self.assertEqual([c['claim']['value'] for c in logs[0]['withheldCharacters']],names[:2])

    def test_summary_prefers_substantial_passage_without_rewriting_it(self):
        excerpts={'E1':{'source':'S1','quote':'Morlun is back!'},
                  'E2':{'source':'S1','quote':'Morlun returns with a new ally who threatens Peter Parker and all his friends.'}}
        def request(base,path,payload):
            self.assertEqual(list(json.loads(payload['messages'][1]['content'])),['E2'])
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E2"]]}'}}]}
        self.assertEqual(trial.select_evidence('unused','fake',excerpts,'summary',[],request,named_characters=['Morlun']),[{'E2':excerpts['E2']}])

    def test_short_summary_remains_available_when_no_longer_source_exists(self):
        excerpts={'E1':{'source':'S1','quote':'Aunt May has a secret.'}}
        def request(*args): return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E1"]]}'}}]}
        self.assertEqual(trial.select_evidence('unused','fake',excerpts,'summary',[],request),[excerpts])

    def test_coverage_recovers_secondary_names_but_excludes_creators_and_places(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Ben Reilly meets Peter Parker in Manhattan. Artist Jane Smith draws the story.'}]}
        excerpts=trial.narrative_input(packet)
        first={'characters':[{'value':'Ben Reilly','evidence':[excerpts['E1']]}]}
        def request(base,path,payload):
            candidates=json.loads(payload['messages'][1]['content'])
            kinds={'Peter Parker':'character','Manhattan':'place','Jane Smith':'creator'}
            response={key:kinds.get(c['name'],'other') for key,c in candidates.items()}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(response)}}]}
        logs=[]
        result=trial.recover_characters('unused','fake',packet,excerpts,first,logs,request)
        self.assertEqual([c['value'] for c in result['characters']],['Ben Reilly'])
        self.assertEqual([c['value'] for c in logs[-1]['suggestedCharacters']],['Peter Parker'])
        self.assertFalse(logs[-1]['autoApplied'])

    def test_name_candidates_preserve_apostrophes_and_split_conjunctions(self):
        excerpts={'E1':{'source':'S1','quote':"First Rabble meets Miguel O'Hara, T'Challa, Hightail and the Cape Killers."}}
        names=[c['name'] for c in trial.name_candidates(excerpts,[]).values()]
        self.assertEqual(names,['Rabble',"Miguel O'Hara","T'Challa",'Hightail','Cape Killers'])

    def test_contents_only_without_hash_marks_is_not_a_synopsis(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Spider-Man 2099 (2014) 1-5, Amazing Spider-Man 1 (2099 story)'}]}
        self.assertEqual(trial.narrative_input(packet),{})

    def test_candidate_audit_missing_keys_is_rejected(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Aunt May has a secret.'}]}
        def request(*args):
            return {'choices':[{'finish_reason':'stop','message':{'content':'{}'}}]}
        with self.assertRaises(ValueError):
            trial.recover_characters('unused','fake',packet,trial.narrative_input(packet),{'characters':[]},[],request)

    def test_prose_selection_requires_known_name_and_excludes_credits_and_bad_encoding(self):
        excerpts={'E1':{'source':'S1','quote':'That property damage keeps rents down.'},
                  'E2':{'source':'S1','quote':'Artist Jones brings Ben Reilly back.'},
                  'E3':{'source':'S1','quote':'Ben Reilly meets a mysterious foe.'},
                  'E4':{'source':'S1','quote':'Ben Reilly meets an unknown \ufffd figure.'}}
        def request(base,path,payload):
            self.assertEqual(list(json.loads(payload['messages'][1]['content'])),['E3'])
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E3"]]}'}}]}
        self.assertEqual(trial.select_evidence('unused','fake',excerpts,'summary',[],request,named_characters=['Ben Reilly']),[{'E3':excerpts['E3']}])

    def test_structured_contents_extracts_range_and_exact_isbn_pages(self):
        packet={'constraints':{'contentsConflict':False,'isbnMatched':True},'sources':[{'id':'S1',
                'text':'Synopsis: Collects Example (2022) #1-5. A hero helps. Bibliographic information: ISBN 9781234567890 Length 112 pages'}]}
        def request(*args): self.fail('No inference needed for explicit bibliography')
        result=trial.generate_stage('unused','fake',packet,trial.STAGES[0],[],request)
        self.assertEqual(result['issues'][0]['value'],'Example (2022) #1-5')
        self.assertEqual(result['pages']['value'],112)
        self.assertEqual(result['uncertainties'],[])

    def test_structured_contents_withholds_partial_and_conflicting_page_counts(self):
        packet={'constraints':{'contentsConflict':False,'isbnMatched':True},'sources':[{'id':'S1',
                'text':'Synopsis: Collects material from Example (2022) #1-5. Bibliographic information: Length 112 pages Length 120 pages'}]}
        result=trial.structured_contents(packet)
        self.assertEqual(result['issues'],[])
        self.assertIsNone(result['pages']['value'])

    def test_structured_pages_require_bibliographic_section_and_isbn(self):
        for text,matched in [('Synopsis: Length 112 pages',True),
                             ('Synopsis: A hero helps. Bibliographic information: Length 112 pages',False)]:
            packet={'constraints':{'isbnMatched':matched},'sources':[{'id':'S1','text':text}]}
            self.assertIsNone(trial.structured_contents(packet)['pages']['value'])

    def test_extractive_summary_preserves_source_without_generated_actions(self):
        quote='Aunt May has a secret that could affect Peter and his family.'
        packet={'sources':[{'id':'S1','text':'Synopsis: '+quote}]}
        calls=[];logs=[]
        def request(base,path,payload):
            calls.append(payload)
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E1"]]}'}}]}
        result=trial.generate_stage('unused','fake',packet,['summary'],logs,request,narrative_mode='extractive')
        self.assertEqual(result['summary']['value'],quote)
        self.assertEqual(result['summary']['evidence'],[{'source':'S1','quote':quote}])
        self.assertEqual(len(calls),1)
        self.assertEqual(logs[-1]['method'],'verbatim source excerpt')

    def test_extractive_selection_cannot_merge_two_sources_into_one_claim(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: A hero travels. A relative has a secret.'}]}
        def request(*args):
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E1","E2"]]}'}}]}
        with self.assertRaisesRegex(ValueError,'too many entries'):
            trial.generate_stage('unused','fake',packet,['summary'],[],request,narrative_mode='extractive')

    def test_per_excerpt_names_repair_missing_last_excerpt_and_merge(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Spider-Man helps. Aunt May meets Spider-Man.'}]}
        calls=[];logs=[]
        def request(base,path,payload):
            calls.append(payload)
            result={'E1':['Spider-Man']} if len(calls)==1 else {'E1':['Spider-Man'],'E2':['Aunt May','Spider-Man']}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        result=trial.generate_stage('unused','fake',packet,['characters'],logs,request,narrative_mode='extractive')
        self.assertEqual([c['value'] for c in result['characters']],['Spider-Man','Aunt May'])
        self.assertEqual(len(result['characters'][0]['evidence']),2)
        self.assertEqual(len(calls),2)
        self.assertIn('missing or extra',logs[0]['errors'][0])

    def test_per_excerpt_names_reject_inferred_aliases(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Spider-Man helps.'}]}
        def request(*args):
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"E1":["Peter Parker"]}'}}]}
        with self.assertRaisesRegex(ValueError,'literally'):
            trial.generate_stage('unused','fake',packet,['characters'],[],request,narrative_mode='extractive')

    def test_pronoun_only_excerpt_not_selected_for_standalone_prose(self):
        excerpts={'E1':{'source':'S1','quote':'And he repairs the damage.'}}
        def request(*args): self.fail('No self-contained evidence to select')
        self.assertEqual(trial.select_evidence('unused','fake',excerpts,'summary',[],request),[])

    def test_support_review_sees_only_selected_evidence_and_rejects_uncertainty(self):
        part={'summary':{'value':'The universe is threatened.','evidence':[{'source':'S1','quote':'His neighbors are threatened.'}]}}
        calls=[];log={}
        def request(base,path,payload):
            calls.append(payload)
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(
                {'summary_0':{'verdict':'uncertain','reason':'Threat scope is not established.'}})}}]}
        self.assertTrue(trial.check_support('unused','fake',part,log,request))
        sent=json.loads(calls[0]['messages'][1]['content'])
        self.assertEqual(sent['summary_0']['evidence'],['His neighbors are threatened.'])
        self.assertIn('supportCheck',log)

    def test_support_review_missing_or_invalid_verdict_fails_closed(self):
        part={'summary':{'value':'A hero helps.','evidence':[{'source':'S1','quote':'A hero helps.'}]}}
        for result in [{},{'summary_0':{'verdict':'maybe','reason':'Unknown'}}]:
            def request(*args):
                return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
            with self.assertRaises(ValueError): trial.check_support('unused','fake',part,{},request)

    def test_semantic_failure_requests_repair_then_rechecks(self):
        calls=[];logs=[]
        replies=[{'summary':{'value':'The universe is threatened.','evidence':['E1']}},
                 {'summary_0':{'verdict':'unsupported','reason':'Only the neighborhood is threatened.'}},
                 {'summary':{'value':'The neighborhood is threatened.','evidence':['E1']}},
                 {'summary_0':{'verdict':'supported','reason':'Matches the evidence.'}}]
        def request(base,path,payload):
            calls.append(copy.deepcopy(payload))
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(replies[len(calls)-1])}}]}
        packet={'sources':[{'id':'S1','text':'Synopsis: The neighborhood is threatened.'}]}
        result=trial.generate_stage('unused','fake',packet,['summary'],logs,request,trial.narrative_input(packet))
        self.assertEqual(result['summary']['value'],'The neighborhood is threatened.')
        self.assertEqual(len(calls),4)
        self.assertIn('Only the neighborhood',calls[2]['messages'][-1]['content'])
        self.assertEqual(logs[1]['errors'],[])

    def test_long_claims_and_uncited_character_names_rejected(self):
        self.assertTrue(trial.narrative_errors({'stories':[{'value':'word '*21,'evidence':[]}]}))
        self.assertTrue(trial.narrative_errors({'characters':[{'value':'May','evidence':[{'source':'S1','quote':'Maybe Peter will help.'}]}]}))
        self.assertEqual(trial.narrative_errors({'characters':[{'value':'Aunt May','evidence':[{'source':'S1','quote':'Aunt May’s secret.'}]}]}),[])

    def test_generation_isolated_to_selected_evidence(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Aunt May has a secret. A galaxy is destroyed.'}]}
        calls=[]
        replies=[{'groups':[['E1']]},
                 {'summary':{'value':'Aunt May has a secret.','evidence':['E1']}},
                 {'summary_0':{'verdict':'supported','reason':'Exact statement.'}}]
        def request(base,path,payload):
            calls.append(copy.deepcopy(payload))
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(replies[len(calls)-1])}}]}
        result=trial.generate_stage('unused','fake',packet,['summary'],[],request)
        self.assertEqual(result['summary']['value'],'Aunt May has a secret.')
        self.assertNotIn('galaxy',calls[1]['messages'][1]['content'])
        self.assertNotIn('galaxy',calls[2]['messages'][1]['content'])

    def test_invalid_evidence_selection_is_rejected(self):
        excerpts={'E1':{'source':'S1','quote':'A hero helps.'}}
        for groups in [[['E9']],[['E1'],['E1']]]:
            def request(*args):
                return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'groups':groups})}}]}
            with self.assertRaises(ValueError): trial.select_evidence('unused','fake',excerpts,'stories',[],request)

    def test_conflict_in_prose_is_rejected_but_story_is_allowed(self):
        packet={'constraints':{'contentsConflict':True},'sources':[]}
        for value in ['Example #1-5 follows a hero.', 'Collects five issues.', 'A 136 page story.']:
            self.assertTrue(trial.factual_errors({'summary':{'value':value,'evidence':[]}},packet))
        self.assertEqual(trial.factual_errors({'summary':{'value':'A hero helps his neighbors.','evidence':[]}},packet),[])

    def test_excerpt_ids_preserve_quotes_and_hide_bibliography(self):
        packet={'sources':[{'id':'S1','text':"Synopsis: Collects Example (2020) #1-5. Aunt May’s secret changes Peter’s life. Bibliographic information: Length 136 pages"}]}
        excerpts=trial.narrative_input(packet)
        self.assertEqual(excerpts,{'E1':{'source':'S1','quote':'Aunt May’s secret changes Peter’s life.'}})
        calls=[]
        def request(base,path,payload):
            calls.append(copy.deepcopy(payload))
            result={'characters':[{'value':'Aunt May','evidence':['E1']}]}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        result=trial.generate_stage('unused','fake',packet,['characters'],[],request)
        self.assertEqual(result['characters'][0]['evidence'],[excerpts['E1']])
        self.assertEqual(trial.evidence_errors(result,packet),[])
        self.assertNotIn('136',calls[0]['messages'][1]['content'])
        self.assertEqual(calls[0]['reasoning_effort'],'none')

    def test_unknown_excerpt_rejected_and_retry_keeps_previous_claim(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Aunt May has a secret.'}]}
        calls=[]; logs=[]
        def request(base,path,payload):
            calls.append(copy.deepcopy(payload))
            result={'characters':[{'value':'Aunt May','evidence':['E999' if len(calls)==1 else 'E1']}]}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        result=trial.generate_stage('unused','fake',packet,['characters'],logs,request)
        self.assertEqual(result['characters'][0]['value'],'Aunt May')
        self.assertIn('Unknown evidence ID',logs[0]['errors'][0])
        self.assertEqual(calls[1]['messages'][2]['role'],'assistant')
        self.assertIn('Aunt May',calls[1]['messages'][2]['content'])

    def test_conflict_gate_does_not_call_model(self):
        packet={'constraints':{'contentsConflict':True,'catalogRange':[1,6],'sourceRange':[1,5]}}
        def request(*args): self.fail('Known conflict should not need inference')
        logs=[]
        result=trial.generate_stage('unused','fake',packet,trial.STAGES[0],logs,request)
        result.update(trial.generate_stage('unused','fake',packet,['review'],logs,request))
        self.assertEqual(result['issues'],[])
        self.assertIsNone(result['pages']['value'])
        self.assertIsNone(result['review']['value'])
        self.assertEqual(len(logs),2)

    def test_overlong_sentences_are_omitted_not_truncated(self):
        text=' '.join('word'+str(i) for i in range(90))
        packet={'sources':[{'id':'S1','text':'Synopsis: '+text}]}
        excerpts=trial.narrative_input(packet)
        self.assertEqual(excerpts,{})

    def test_complete_sentence_preserves_threat_target_and_modality(self):
        text=('A threat could destroy the hero and all his neighbors, and it may force '
              'him to travel far from home to a previously unseen place.')
        packet={'sources':[{'id':'S1','text':'Synopsis: '+text}]}
        excerpts=trial.narrative_input(packet)
        self.assertEqual(excerpts['E1']['quote'],text)
        self.assertEqual(trial.evidence_errors({'summary':{'value':'A threat could destroy the neighborhood.','evidence':[excerpts['E1']]}},packet),[])

    def test_promotional_superlatives_not_available_for_prose_selection(self):
        excerpts={'E1':{'source':'S1','quote':'The greatest hero ever!'},
                  'E2':{'source':'S1','quote':'Aunt May has a secret.'}}
        def request(base,path,payload):
            self.assertNotIn('greatest',payload['messages'][1]['content'])
            return {'choices':[{'finish_reason':'stop','message':{'content':'{"groups":[["E2"]]}'}}]}
        self.assertEqual(trial.select_evidence('unused','fake',excerpts,'summary',[],request),[{'E2':excerpts['E2']}])

    def test_narrative_missing_evidence_never_accepted(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: A hero rescues a neighbor.'}]}
        def request(*args):
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(
                {'stories':[{'value':'A hero rescues a neighbor.','evidence':[]}]})}}]}
        logs=[]
        with self.assertRaisesRegex(ValueError,'too few entries'):
            trial.generate_stage('unused','fake',packet,['stories'],logs,request,trial.narrative_input(packet))
        self.assertEqual(len(logs),2)

    def test_no_narrative_source_abstains_without_inference(self):
        packet={'sources':[{'id':'S1','text':'Synopsis: Collects Example (2020) #1-5. Bibliographic information: Length 136 pages'}]}
        def request(*args): self.fail('No narrative evidence to interpret')
        self.assertEqual(trial.generate_stage('unused','fake',packet,['summary','readingOrder'],[],request),
                         {'summary':{'value':None,'evidence':[]},'readingOrder':{'value':None,'evidence':[]}})

    def test_conflict_requires_abstention_even_with_real_quote(self):
        book={'isbn':'9781302515041','title':'Friendly Neighborhood Spider-Man: Issues #1-6'}
        description='Collects Friendly Neighborhood Spider-Man (2019) #1-5.'
        constraints=trial.constraints_for(book,description,'ISBN 9781302515041 Length 136 pages')
        self.assertTrue(constraints['contentsConflict']);self.assertTrue(constraints['isbnMatched'])
        packet={'book':book,'constraints':constraints,'sources':[{'id':'S1','text':description+' Length 136 pages'}]}
        part={'issues':[{'value':'Friendly Neighborhood Spider-Man (2019) #1-5','evidence':[{'source':'S1','quote':description}]}],
              'pages':{'value':136,'evidence':[]}}
        self.assertEqual(len(trial.factual_errors(part,packet)),2)
        self.assertEqual(trial.factual_errors({'issues':[],'pages':{'value':None,'evidence':[]}},packet),[])

    def test_score_rows_keep_critic_and_user_separate(self):
        raw='''<div id="trades"><table><tr><td><div class="critic-rating"><span>8.5</span><div>53 Reviews</div></div>
        <div class="user-rating"><span>8.4</span><div>4 Reviews</div></div></td>
        <td><a href="/comic-books/trades/example/vol-1">Vol. 1: Secrets</a></td><td>5</td></tr></table></div>'''
        rows=trial.parse_trade_rows(raw)
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['criticScore'],rows[0]['criticCount'],rows[0]['userScore'],rows[0]['userCount']),(8.5,53,8.4,4))
        packet={'book':{'title':'Vol. 1: Secrets'},'constraints':{'sourceRange':[1,5]},'sources':[{'id':'S2','rows':rows}]}
        review={'value':{'collection':'Vol. 1: Secrets','criticScore':8.4,'criticCount':4,'scope':'trade'},'evidence':[{'source':'S2','quote':'irrelevant'}]}
        self.assertTrue(trial.factual_errors({'review':review},packet))
        review['value'].update(criticScore=8.5,criticCount=53)
        self.assertEqual(trial.factual_errors({'review':review},packet),[])
        self.assertEqual(trial.parse_trade_rows('<table>unrecognized markup</table>'),[])

    def test_issue_prefix_and_hidden_partial_material_rejected(self):
        for source,value in [('Collects Example (2020) #1-50.','Example (2020) #1-5'),
                             ('Collects material from Example (2020) #1-5.','Example (2020) #1-5')]:
            quote=source if 'material' not in source else 'Example (2020) #1-5.'
            self.assertTrue(trial.issue_errors({'issues':[{'value':value,'evidence':[{'source':'S1','quote':quote}]}]},
                                               {'sources':[{'id':'S1','text':source}]}))

    def test_bounded_retry_passes_specific_feedback(self):
        packet={'book':{},'constraints':{'contentsConflict':True},'sources':[{'id':'S1','text':'Length 136 pages'}]}
        bad={'pages':{'value':136,'evidence':[{'source':'S1','quote':'Length 136 pages'}]}}
        good={'pages':{'value':None,'evidence':[]}}
        calls=[];logs=[]
        def request(base,path,payload):
            calls.append(copy.deepcopy(payload))
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(bad if len(calls)==1 else good)}}]}
        self.assertEqual(trial.generate_stage('unused','fake',packet,['pages'],logs,request),good)
        self.assertEqual(len(calls),2)
        self.assertIn('unresolved contents conflict',calls[1]['messages'][-1]['content'])
        self.assertTrue(logs[0]['errors']);self.assertEqual(logs[1]['errors'],[])
        def always_bad(*args): return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(bad)}}]}
        logs=[]
        with self.assertRaises(ValueError): trial.generate_stage('unused','fake',packet,['pages'],logs,always_bad)
        self.assertEqual(len(logs),2)

    def test_runaway_issue_numbers_are_rejected(self):
        quote = 'Collects Friendly Neighborhood Spider-Man (2019) #1-5.'
        packet = {'sources':[{'id':'S1','text':quote}]}
        def claims(value): return {'issues':[{'value':value,'evidence':[{'source':'S1','quote':quote}]}]}
        self.assertTrue(trial.issue_errors(claims('Friendly Neighborhood Spider-Man (2019) #1-47'),packet))
        valid = claims('Friendly Neighborhood Spider-Man (2019) #1-5')
        self.assertEqual(trial.issue_errors(valid,packet),[])
        self.assertEqual(len(trial.expanded_issues(valid['issues'])),5)
        self.assertTrue(trial.validate_schema([1,2],{'type':'array','maxItems':1,'items':{'type':'integer'}}))

    def test_cloud_endpoints_and_redirects_rejected(self):
        for url in ['https://example.com/v1', 'http://127.0.0.1.example.com/v1',
                    'http://user:secret@localhost:1234/v1', 'http://localhost/v1?x=1']:
            with self.assertRaises(ValueError): trial.endpoint(url)
        self.assertEqual(trial.endpoint('http://127.0.0.1:1234/v1/'), 'http://127.0.0.1:1234/v1')
        with self.assertRaises(ValueError):
            trial.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com')

    def test_validation_and_evidence_are_not_trusted_blindly(self):
        result = empty_result()
        self.assertEqual(trial.validate_schema(result, trial.SCHEMA), [])
        result['pages']['value'] = True
        self.assertTrue(trial.validate_schema(result, trial.SCHEMA))
        result['pages']['value'] = None
        result['summary'] = {'value': 'An unsupported assertion', 'evidence': [{'source': 'S1', 'quote': 'invented quote'}]}
        self.assertTrue(trial.evidence_errors(result, {'sources': [{'id': 'S1', 'text': 'Actual source.'}]}))
        result['summary']['evidence'] = []
        self.assertTrue(trial.evidence_errors(result, {'sources': []}))

    def test_packet_excludes_editorial_answers_and_page_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); cache = root/'data/cache'; cache.mkdir(parents=True)
            (cache/'google-123.html').write_text('<meta name="description" content="Publisher text"><script>EVIL_SCRIPT</script>Bibliographic information ISBN 123 Length 100 pages')
            (root/'public').mkdir()
            (root/'public/enrichment.json').write_text('SECRET_BASELINE')
            with patch.object(trial, 'ROOT', root):
                packet = trial.source_packet({'isbn': '123', 'title': 'Title', 'summary': 'SECRET_ANSWER', 'detail': 'SECRET_DETAIL'}, {})
            rendered = str(packet)
            for sentinel in ['SECRET_BASELINE', 'SECRET_ANSWER', 'SECRET_DETAIL', 'EVIL_SCRIPT']:
                self.assertNotIn(sentinel, rendered)
            self.assertIn('Publisher text', rendered)


if __name__ == '__main__': unittest.main()
