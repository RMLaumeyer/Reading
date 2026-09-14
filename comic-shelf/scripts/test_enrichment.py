import unittest
from enrich_catalog import parse_metadata

class MetadataTests(unittest.TestCase):
    def test_exact_isbn_required(self):
        raw = '<meta property="og:url" content="https://books.google.com/books?id=test"><meta name="description" content="A story">Bibliographic information ISBN 9780000000002 Length 144 pages'
        self.assertIsNone(parse_metadata({'isbn':'9780000000001'},raw))
        self.assertEqual(parse_metadata({'isbn':'9780000000002'},raw)['pages'],144)

    def test_partial_does_not_invent_editorial_fields(self):
        raw = '<meta property="og:url" content="https://books.google.com/books?id=test"><meta name="description" content="' + 'word '*100 + '">Bibliographic information ISBN 9780000000002 Length 144 pages'
        d = parse_metadata({'isbn':'9780000000002'},raw)
        self.assertEqual(d['characters'],[])
        self.assertEqual(d['stories'],[])
        self.assertEqual(d['readingPath']['name'],'')
        self.assertNotIn('review',d)
        self.assertLessEqual(len(d['summary'].split()),26)

if __name__ == '__main__': unittest.main()
