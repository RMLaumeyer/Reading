import tempfile
from pathlib import Path
import unittest
from unittest.mock import Mock
import decimal_research as research


class DecimalDiscoveryTests(unittest.TestCase):
    def paths(self):
        return [{'sourceSequence':[{'identityState':'unsupported',
                                    'unsupportedIssueDesignation':{'designator':'5.1'}}]}]

    def test_event_prefix_budget_exclusions_and_no_range_requirement(self):
        books=[{'isbn':'9780785191698','title':'Original sin: Thor & Loki : the tenth realm'},
               {'isbn':'9781302406240','title':'Original Sin: Hulk vs. Iron Man: Issues #1-4'},
               {'isbn':'9780000000000','title':'Other Original Sin'},
               {'isbn':'bad','title':'Original Sin'}]
        result=research.plan(self.paths(),books,'original sin',['9781302406240'],1)
        self.assertEqual([b['isbn'] for b in result],['9780785191698'])
        self.assertEqual(research.plan([],books,'original sin'),[])
        self.assertEqual(research.plan(self.paths(),books,'original sin',budget=0),[])

    def test_unsafe_acquisition_is_rejected_before_files_or_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'output';fetch=Mock()
            with self.assertRaises(ValueError):
                research.acquire([{'isbn':'../escape'}],folder,google=fetch)
            self.assertFalse(folder.exists());fetch.assert_not_called()

    def test_rate_limit_is_recorded_and_stops_same_provider_batch(self):
        import urllib.error
        fetch=Mock(side_effect=urllib.error.HTTPError('https://books.google.com',429,'limited',{},None))
        books=[{'isbn':'9780785191698'},{'isbn':'9781302406240'}]
        with tempfile.TemporaryDirectory() as tmp:
            result=research.acquire(books,Path(tmp)/'output',google=fetch)
            self.assertEqual(result,[]);self.assertEqual(fetch.call_count,1)


if __name__=='__main__':unittest.main()
