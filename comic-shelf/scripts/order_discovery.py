"""Discover exact event pages from two public indexes, without search APIs."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
import re
import urllib.request
from urllib.parse import urljoin,urlsplit
import xml.etree.ElementTree as ET

import cbro_order
import guide_order
from series_references import name_key

INDEXES = [('cbro','https://comicbookreadingorders.com/marvel/events/'),
           ('marvelguides','https://marvelguides.com/sitemap.xml')]


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Index redirect not supported')


def download(url):
    if url not in {u for _,u in INDEXES}:raise ValueError('Unsupported public index')
    request=urllib.request.Request(url,headers={'User-Agent':'ComicShelfResearch/0.1'})
    with urllib.request.build_opener(NoRedirects).open(request,timeout=25) as response:
        if response.headers.get_content_type() not in ('text/html','text/xml','application/xml'):
            raise ValueError('Unexpected index content type')
        body=response.read(3_000_001)
        if len(body)>3_000_000:raise ValueError('Index exceeds limit')
        return body,response.headers.get_content_charset() or 'utf-8'


class Links(HTMLParser):
    def __init__(self,raw):
        super().__init__(convert_charrefs=True)
        self.links,self.current,self.skip=[],None,0
        self.feed(raw)
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if not self.skip and tag=='a':self.current={'url':dict(attrs).get('href',''),'text':''}
    def handle_data(self,text):
        if not self.skip and self.current is not None:self.current['text']+=text
    def handle_endtag(self,tag):
        if tag in ('script','style'):
            self.skip=max(0,self.skip-1);return
        if not self.skip and tag=='a' and self.current is not None:
            self.links.append(self.current);self.current=None


def candidates(raw,adapter,event):
    expected=name_key(event)
    found={}
    if adapter=='cbro':
        for link in Links(raw).links:
            label=re.sub(r'\s*\(\d{4}\)\s*$','',' '.join(link['text'].split()))
            if name_key(label)!=expected:continue
            url=urljoin(INDEXES[0][1],link['url'])
            try:cbro_order.check_url(url)
            except ValueError:continue
            slug=urlsplit(url).path.strip('/').split('/')[-1].removesuffix('-reading-order')
            if name_key(slug)!=expected:continue
            found[url]={'adapter':adapter,'url':url,'discoveryQuote':link['text']}
    elif adapter=='marvelguides':
        if re.search(r'<!\s*(?:DOCTYPE|ENTITY)\b',raw,re.I):raise ValueError('DTD/entity declarations not accepted')
        root=ET.fromstring(raw)
        ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
        if root.tag!=ns+'urlset':raise ValueError('Expected a bounded URL sitemap')
        for element in root.findall(ns+'url/'+ns+'loc'):
            url=(element.text or '').strip()
            try:guide_order.check_url(url)
            except ValueError:continue
            slug=urlsplit(url).path.strip('/').removesuffix('-reading-order')
            if name_key(slug)==expected:
                found[url]={'adapter':adapter,'url':url,'sectionSelection':'all_explicit_reading_lists',
                            'discoveryQuote':url}
    else:raise ValueError('Unsupported index adapter')
    return list(found.values())


def acquire(event,folder,fetch=download):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',event) or len(event)>80:
        raise ValueError('Use a lowercase event slug')
    folder.mkdir(exist_ok=False)
    sources,report=[],[]
    def save(path,data):
        with path.open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,ensure_ascii=False)
    for adapter,url in INDEXES:
        item={'adapter':adapter,'url':url,'state':'attempted','retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            body,encoding=fetch(url)
            (folder/(adapter+'-index.txt')).write_bytes(body)
            item['sha256']=hashlib.sha256(body).hexdigest()
            matches=candidates(body.decode(encoding),adapter,event)
            item['candidates']=matches
            item['state']='selected' if len(matches)==1 else 'ambiguous' if matches else 'no_exact_event'
            if len(matches)==1:sources.append(matches[0])
        except (OSError,ValueError,LookupError,ET.ParseError) as exc:
            item.update(state='failed',errorType=type(exc).__name__,httpStatus=getattr(exc,'code',None))
        report.append(item)
        save(folder/(adapter+'-discovery.json'),item)
    save(folder/'sources.json',sources)
    save(folder/'report.json',report)
    return sources,report
