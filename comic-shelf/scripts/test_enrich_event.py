import unittest
import enrich_event


class EventSelectionTests(unittest.TestCase):
    def test_bounded_deduplicated_selection_includes_named_tie_in(self):
        books=[{'isbn':'9781302471590','title':'Nova Vol. 4: Original Sin: Issues #17-22'},
               {'isbn':'9781302406240','title':'Original Sin: Hulk vs. Iron Man: Issues #1-4'},
               {'isbn':'9781302406240','title':'Original Sin duplicate'},
               {'isbn':'9780000000000','title':'Unoriginal Sin'},
               {'isbn':'../unsafe','title':'Original Sin'}]
        result=enrich_event.select(books,'original-sin',1)
        self.assertEqual([b['isbn'] for b in result['selected']],['9781302406240'])
        self.assertEqual([b['isbn'] for b in result['omitted']],['9781302471590'])
        self.assertIn('neither membership',result['scope'])

    def test_no_candidates_and_invalid_budget(self):
        self.assertEqual(enrich_event.select([],'original-sin',8)['selected'],[])
        for limit in (0,9):
            with self.assertRaises(ValueError):enrich_event.select([],'original-sin',limit)


if __name__=='__main__':unittest.main()
