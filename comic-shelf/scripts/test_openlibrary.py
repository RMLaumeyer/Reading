import io
import unittest
import urllib.error
from enrich_openlibrary import fetch_json

class RetryTests(unittest.TestCase):
    def test_timeout_then_success(self):
        calls=[]
        def opener(*args,**kwargs):
            calls.append(1)
            if len(calls)==1: raise urllib.error.URLError('timeout')
            return io.StringIO('{}')
        delays=[]
        self.assertEqual(fetch_json(None,lambda s:None,opener,delays.append),{})
        self.assertEqual(delays,[10])

    def test_retry_limit(self):
        calls=[]
        def opener(*args,**kwargs):
            calls.append(1)
            raise urllib.error.URLError('timeout')
        with self.assertRaises(urllib.error.URLError):
            fetch_json(None,lambda s:None,opener,lambda s:None)
        self.assertEqual(len(calls),3)

    def test_no_retry_on_rate_limit(self):
        def opener(*args,**kwargs):
            raise urllib.error.HTTPError('https://openlibrary.org',429,'Limited',{},None)
        delays=[]
        with self.assertRaises(urllib.error.HTTPError):
            fetch_json(None,lambda s:None,opener,delays.append)
        self.assertEqual(delays,[])

if __name__=='__main__': unittest.main()
