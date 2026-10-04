"""Command-level failure and provenance checks, with no network or model calls."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import order_research as research


class PipelineTests(unittest.TestCase):
    def run_fixture(self, first_fetch):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'scripts').mkdir()
            script=root/'scripts/order_research.py';script.write_text('fixture',encoding='utf-8')
            (root/'data/local-ai-trials').mkdir(parents=True)
            edition=root/'editions/9781234567890';edition.mkdir(parents=True)
            (edition/'packet.json').write_text(json.dumps({'book':{'isbn':'9781234567890','title':'Example'},
                                                           'seriesIdentityReferences':[]}),encoding='utf-8')
            (edition/'result.json').write_text(json.dumps({'contents':{'entries':[]}}),encoding='utf-8')
            raw=b'<h1>Annihilation</h1><button role="tab" aria-controls="issues">Single Issues</button><div role="tabpanel" id="issues"><p>Example #1 (2020)</p><p>Unknown #2</p></div>'
            with patch.object(research,'__file__',str(script)), patch('sys.argv',[
                    'order_research.py','--event','annihilation','--edition-run',str(root/'editions'),'--name','fixture']), \
                 patch.object(research.guide_order,'download',side_effect=first_fetch), \
                 patch.object(research.cbro_order,'download',side_effect=lambda url:(raw,url,'utf-8')), \
                 contextlib.redirect_stdout(io.StringIO()):
                research.main()
            folder=root/'data/local-ai-trials/fixture'
            return {p.relative_to(folder).as_posix():json.loads(p.read_text(encoding='utf-8'))
                    for p in folder.rglob('*.json')}

    def test_unavailable_source_does_not_stop_other_host_or_claim_agreement(self):
        def fail(url):raise HTTPError(url,429,'sensitive-provider-message',{},None)
        output=self.run_fixture(fail)
        report=output['report.json']
        self.assertEqual(report['acquiredSources'],1)
        self.assertEqual(report['state'],'needs_review')
        self.assertEqual(report['comparisons'],[])
        self.assertEqual(report['failures'][0]['stage'],'download')
        self.assertNotIn('sensitive-provider-message',json.dumps(output))
        self.assertEqual(output['source-2/collection-path.json']['unresolvedSourcePositions'],[2])
        self.assertFalse(output['source-2/collection-path.json']['coversAllSourceListedIssues'])
        self.assertEqual(output['research-tasks.json'][0]['sourceLabel'],'Unknown')

    def test_downloaded_but_unparseable_page_is_not_a_network_error(self):
        output=self.run_fixture(lambda url:(b'<h1>Unrecognized layout</h1>',url,'utf-8'))
        first=output['source-1/acquisition.json']
        self.assertTrue(first['downloaded'])
        self.assertEqual(first['stage'],'parse')
        self.assertEqual(first['state'],'failed')
        self.assertIn('sha256',first)
        self.assertEqual(output['report.json']['failures'][0]['stage'],'parse')


if __name__ == '__main__':unittest.main()
