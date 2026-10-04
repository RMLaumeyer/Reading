import tempfile
from pathlib import Path
from unittest.mock import patch
import unittest
import order_sources as sources
import order_identity


class DiscoveryTests(unittest.TestCase):
    def path(self,series='Example',number=3):
        return {'sourceSequence':[{'position':1,'issue':{'series':series,'year':None,'number':number},
                                  'identityState':'unresolved','quote':series+' #3'}],
                'orderedIssues':[],'problems':[{'reason':'missing year'}],'state':'needs_review'}

    def books(self):
        return [{'isbn':'9781234567890','title':'Example Vol. 1: Title: Issues #1-5'},
                {'isbn':'9781234567891','title':'Example Vol. 2: Title: Issues #6-10'},
                {'isbn':'9781234567892','title':'Example Classic Vol. 1: Issues #1-5'}]

    def test_candidates_bounded_ranked_and_volume_only_expands_lookup(self):
        plan=sources.plan([self.path('Example Vol. 2')],self.books(),max_pages=1)
        self.assertEqual([c['isbn'] for c in plan['selected']],['9781234567890'])
        self.assertEqual(plan['selected'][0]['sourceLabels'],['Example Vol. 2'])
        self.assertEqual(len(plan['groups'][0]['candidates']),2)
        self.assertEqual(sources.plan([self.path()],self.books(),max_pages=0)['selected'],[])

    def test_wrong_isbn_never_supplies_identity(self):
        plan=sources.plan([self.path()],self.books(),max_pages=1)
        with tempfile.TemporaryDirectory() as temp, patch.object(sources.edition_sources,'packet_from_html',return_value={'constraints':{'isbnMatched':False}}):
            result=sources.acquire(plan,self.books(),Path(temp)/'out',lambda isbn:(b'page','https://books.google.com','utf-8'))
            self.assertEqual(result,[])

    def test_rate_limit_stops_batch(self):
        from urllib.error import HTTPError
        calls=[]
        def fetch(isbn):
            calls.append(isbn);raise HTTPError('https://books.google.com',429,'sensitive',{},None)
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)/'out'
            self.assertEqual(sources.acquire(sources.plan([self.path()],self.books()),self.books(),folder,fetch),[])
            self.assertEqual(len(calls),1)
            self.assertNotIn('sensitive',(folder/'report.json').read_text())

    def test_explicit_evidence_proposes_year_without_membership_or_alias(self):
        evidence={'isbn':'reference','url':'https://books.google.com','sha256':'test','scope':'identity only',
                  'entries':[{'series':'Example','year':2020,'first':1,'last':5,'evidence':{'quote':'Example (2020) #1-5'}}]}
        resolved=order_identity.resolve(self.path(),[],[evidence])
        self.assertEqual(resolved['orderedIssues'][0]['issue']['year'],2020)
        self.assertTrue(resolved['orderedIssues'][0]['identityRequiresReview'])
        self.assertEqual(order_identity.resolve(self.path('Example Vol. 2'),[],[evidence])['orderedIssues'],[])
        self.assertEqual(order_identity.resolve(self.path(number=6),[],[evidence])['orderedIssues'],[])

    def test_unsafe_plan_rejected_before_fetch(self):
        with tempfile.TemporaryDirectory() as temp:
            for plan in ({'maxPages':1,'selected':[{'isbn':'../escape'}]}, {'maxPages':0,'selected':[{'isbn':'9781234567890'}]}):
                with self.assertRaises(ValueError):sources.acquire(plan,[],Path(temp)/'out')

    def test_unrelated_event_context_cannot_supply_year(self):
        plan=sources.plan([self.path()],self.books(),max_pages=1,event_label='Black Vortex')
        packet={'book':{'isbn':'9781234567890'},'constraints':{'isbnMatched':True},
                'sources':[{'id':'S1','text':'Synopsis: An unrelated adventure. Collects Example (2020) #1-5.'}]}
        with tempfile.TemporaryDirectory() as temp, patch.object(sources.edition_sources,'packet_from_html',return_value=packet):
            self.assertEqual(sources.acquire(plan,self.books(),Path(temp)/'out',lambda isbn:(b'page','https://books.google.com','utf-8')),[])
        packet['sources'][0]['text']='Synopsis: The Black Vortex arrives. Collects Example (2020) #1-5.'
        with tempfile.TemporaryDirectory() as temp, patch.object(sources.edition_sources,'packet_from_html',return_value=packet):
            result=sources.acquire(plan,self.books(),Path(temp)/'out',lambda isbn:(b'page','https://books.google.com','utf-8'))
            self.assertEqual(result[0]['entries'][0]['year'],2020)
            self.assertEqual(result[0]['eventContext']['label'],'Black Vortex')

    def test_volume_lookup_evidence_does_not_leak_into_another_source_label(self):
        evidence={'isbn':'other','url':'https://books.google.com','sha256':'test','scope':'identity only',
                  'sourceLabels':['Example Vol. 2'],
                  'entries':[{'series':'Example','year':2000,'first':1,'last':5,'evidence':{}}]}
        self.assertEqual(order_identity.resolve(self.path(),[],[evidence])['orderedIssues'],[])
