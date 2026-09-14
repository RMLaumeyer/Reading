"""Publish reviewed story annotations without discarding ISBN metadata."""
import copy
import datetime
import json
import msvcrt
from moon_knight_notes import N
from enrich_catalog import ROOT, write_json

# Trade-specific rows observed on Comic Book Roundup; never series-wide scores.
REVIEWS={
 '9780785180203':(7.6,20,7.4,4,'moon-knight-%282006%29'),
 '9781302368203':(6.9,13,6.8,4,'moon-knight-%282006%29'),
 '9781302481964':(8.8,16,7.4,4,'moon-knight-%282006%29'),
 '9781302482626':(7.9,14,7.0,3,'moon-knight-%282006%29'),
 '9781302485924':(8.2,8,7.7,3,'moon-knight-%282006%29'),
 '9781302532642':(9.0,11,9.0,1,'moon-knight-fist-of-khonshu-%282024%29'),
 '9781302534066':(9.2,6,None,None,'moon-knight-fist-of-khonshu-%282024%29'),
 '9781302535384':(8.9,8,None,None,'moon-knight-fist-of-khonshu-%282024%29'),
}

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b')
    msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books']
    editorial={}
    for b in catalog:
        if b['isbn'] not in N: continue
        d=copy.deepcopy(payload['books'].get(b['id'],{}))
        if b['isbn']=='9781302497415':
            d.update(pages=172,pagesSource='https://lib2go.overdrive.com/addc-rogers/content/media/8612800',coverSource='')
        source=d['pagesSource']
        assert source.startswith(('https://books.google.com/','https://lib2go.overdrive.com/'))
        note=copy.deepcopy(N[b['isbn']])
        guests=note.pop('guests')
        d.update(note)
        d.pop('level',None)
        d['editorialBatch']='moon-knight'
        d['checkedAt']=datetime.date.today().isoformat()
        d['characters']=[dict(name='Moon Knight',role='Lead character / featured incarnation',source=source)]+[dict(name=name,role='Featured in publisher synopsis',source=source) for name in guests]
        d['contentsNote']=note.get('contentsNote','Overlap index includes only the explicitly indexed issues, not all bonus material. '+note['readingPath']['note'])
        d['sources']=[dict(label='Google Books · ISBN-matched publisher synopsis and contents',url=source)]
        if b['isbn']=='9781302497415':
            d['sources'][0]['label']='OverDrive · matching digital ISBN, 172 pages and publisher synopsis; not an OCLS availability claim'
        d['checks']=dict(edition='ISBN matched',story='Publisher synopsis reviewed',characters='Synopsis appearances only; cameos not exhaustive',readingOrder='Editorial sequence from series and issue coverage',review='No additional verified review score attached')
        if b['isbn'] in REVIEWS:
            critic,count,reader,reader_count,slug=REVIEWS[b['isbn']]
            url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
            d['review']=dict(criticScore=critic,criticCount=count,userScore=reader,userCount=reader_count,url=url,checkedAt=d['checkedAt'],title=b['title'],match='Matched to the specific trade row by volume, title and issue count on the series page.',scope='Trade-row aggregate of reviewed issues, not the overall series score. Supplemental material may be excluded; Leave Home excludes issue 0.')
            d['sources'].append(dict(label='Comic Book Roundup · specific collection row in Trades section',url=url))
            d['checks']['review']='Verified collection-row aggregate'
        editorial[b['id']]=d
    payload['books'].update(editorial)
    payload['updatedAt']=datetime.date.today().isoformat()
    write_json(ROOT/'data/editorial-enrichment.json',editorial)
    for directory in [ROOT/'public',ROOT/'dist/client']:
        write_json(directory/'enrichment.json',payload)
    report={'moonKnightTitles':sum('moon knight' in b['title'].lower() for b in catalog),'newStoryAnnotations':len(editorial),'newReviews':len(REVIEWS),'unresolved':['Bendis Volume 2 issue range conflict; Killed Not Dead issue 10 conflict; additional review matches and exhaustive cameo indexing remain'],'reviewStatus':'Eight new trade-specific scores; unavailable scores remain blank.'}
    write_json(ROOT/'data/moon-knight-audit.json',report)
    print(json.dumps(report))

if __name__=='__main__': main()
