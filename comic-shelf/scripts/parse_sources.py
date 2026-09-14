"""Small HTML parser for public metadata; never executes page scripts."""
from html.parser import HTMLParser
import json
import re

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.meta = {}; self.links = []; self.images = []; self.text = []
        self.jsonld = []; self._script = None; self._skip = 0; self._anchor = None
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta': self.meta[a.get('property', a.get('name',''))] = a.get('content','')
        if tag == 'img': self.images.append(a)
        if tag == 'a': self._anchor = {'url':a.get('href',''), 'text':''}; self.links.append(self._anchor)
        if tag in ('script','style'):
            self._skip += 1
            if tag == 'script' and a.get('type') == 'application/ld+json': self._script = ''
    def handle_endtag(self, tag):
        if tag == 'a': self._anchor = None
        if tag in ('script','style'):
            self._skip = max(0, self._skip-1)
            if self._script is not None:
                try: self.jsonld.append(json.loads(self._script))
                except ValueError: pass
                self._script = None
    def handle_data(self, data):
        if self._script is not None: self._script += data
        if not self._skip and data.strip():
            self.text.append(data.strip())
            if self._anchor is not None: self._anchor['text'] += data.strip() + ' '
    @property
    def plain(self): return ' '.join(self.text)

def parse_catalog(html):
    p = Page(html)
    ids = list(dict.fromkeys(re.findall(r'^/Hoopla/(\d+)$', a['url'])[0] for a in p.links if re.match(r'^/Hoopla/\d+$',a['url'])))
    return {'description':p.meta.get('og:description',''), 'hooplaIds':ids,
            'sourceTitle':p.meta.get('og:title','')}

def parse_review(html):
    p = Page(html)
    scores = re.search(r'(\d+(?:\.\d+)?|N/A)\s+Critic Rating\s*(?:(\d+) Reviews)?\s*(\d+(?:\.\d+)?|N/A)\s+User Rating\s*(?:(\d+) Reviews)?',p.plain)
    current = next((im.get('src') for im in p.images if 'current' in im.get('class','').split()),None)
    return {'title':p.meta.get('og:title',''), 'coverUrl':current,
            'criticScore':float(scores[1]) if scores and scores[1]!='N/A' else None,
            'criticCount':int(scores[2]) if scores and scores[2] else None,
            'userScore':float(scores[3]) if scores and scores[3]!='N/A' else None,
            'userCount':int(scores[4]) if scores and scores[4] else None,
            'trades':[a for a in p.links if a['url'].startswith('/comic-books/trades/')],
            'issues':[a for a in p.links if re.search(r'/comic-books/reviews/.+/\d+$',a['url'])]}
