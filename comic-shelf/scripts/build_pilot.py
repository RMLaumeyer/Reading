"""Build a sourced pilot from cached public pages and explicit editorial annotations."""
import json
import re
from html import unescape
from pathlib import Path
from parse_sources import Page, parse_catalog, parse_review
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT/'data/cache'
DATE = '2026-09-08'

def run(name, pos, note='', alternative=False):
    return dict(name=name, position=pos, note=note, alternative=alternative)

def group(series, year, first, last):
    return [f'{series} ({year}) #{i}' for i in range(first,last+1)]

def entry(summary, stories, path, issues, guests=(), starting=False, coverage='Part of a run'):
    return dict(summary=summary, stories=[dict(title=s,coverage=coverage) for s in stories], readingPath=path, issueKeys=issues, guests=list(guests), startingPoint=starting)

MK14='Moon Knight (2014)'; MK16='Moon Knight — Lemire & Smallwood (2016)'; MK21='Moon Knight — Jed MacKay (2021)'; ASM='Amazing Spider-Man — Nick Spencer (2018)'; USM='Ultimate Spider-Man — Brian Michael Bendis (2000)'
NOTES = {
 '9781302392055':entry('Marc Spector investigates strange threats across New York in six compact adventures. Ghosts, disturbing experiments, and a rescue through a building full of criminals give this collection an episodic detective-horror feel.', ['From the Dead'],run(MK14,1,'Begin this three-volume series here.'),group('Moon Knight',2014,1,6),starting=True),
 '9781302479961':entry('A citywide blackout and a high-rise hostage crisis put Moon Knight under public scrutiny. His relationship with his psychiatrist takes a dangerous turn as his investigations leave him increasingly isolated.', ['Dead Will Rise'],run(MK14,2,'Read after From the Dead.'),group('Moon Knight',2014,7,12)),
 '9781302482169':entry('As Marc tries to rebuild his life, supernatural predators threaten New York. Wolves, a creature preying on children, and dangers tied to Khonshu bring this series to a horror-focused conclusion.', ['In the Night'],run(MK14,3,'Read after Dead Will Rise. Final volume of this series.'),group('Moon Knight',2014,13,17)),
 '9781302494612':entry('Marc wakes in a psychiatric institution with records that challenge his memories of being Moon Knight. Familiar faces may be allies, enemies, or something stranger as he searches for an escape and a reliable version of reality.', ['Lunatic'],run(MK16,1,'Start the three-volume Lemire story here, or choose the Complete Collection.'),group('Moon Knight',2016,1,5),starting=True),
 '9781302497798':entry('The story shifts among Marc Spector, Steven Grant, and Jake Lockley. Their competing lives blur the boundary between escape and another trap, continuing the identity mystery begun in Lunatic.', ['Reincarnations'],run(MK16,2,'Read after Lunatic. Includes a bonus classic issue.'),group('Moon Knight',2016,6,9)+group('Moon Knight',1980,2,2)),
 '9781302499839':entry('The final chapter explores Marc’s past and his relationship with Khonshu. Questions about where his identities began build toward a confrontation over who controls his future.', ['Birth and Death'],run(MK16,3,'Read after Reincarnations. Concludes the Lemire story.'),group('Moon Knight',2016,10,14)),
 '9781302940973':entry('The full Lemire and Smallwood story follows Marc from a disorienting institutional confinement through competing identities and an examination of his past. This is an alternative to reading the three smaller volumes.', ['Lunatic','Reincarnations','Birth and Death'],run(MK16,1,'Alternative to volumes 1–3; do not read it as an additional sequel.',True),group('Moon Knight',2016,1,14),starting=True,coverage='Complete run'),
 '9781302940669':entry('Marc opens the Midnight Mission to protect people who travel after dark. With Khonshu imprisoned, he must define his own duty while a series of strange attacks tests his new sanctuary.', ['The Midnight Mission'],run(MK21,1,'Start MacKay’s 2021 series here.'),group('Moon Knight',2021,1,6),starting=True),
 '9781302943509':entry('The hunt for Zodiac draws Marc deeper into a hostile underworld while enemies threaten his mission from multiple directions. A separate Devil’s Reign tie-in sends him into a prison populated by criminals he helped capture.', ['Too Tough to Die','Devil’s Reign: Moon Knight'],run(MK21,2,'Read after The Midnight Mission. The Devil’s Reign material is a tie-in, not the full event.'),group('Moon Knight',2021,7,12)+group('Devil’s Reign: Moon Knight',2022,1,1)),
 '9781302523671':entry('Moon Knight takes on the vampire organization called the Structure while confronting secrets within his own circle. Hunter’s Moon follows his own approach to justice, and the collection includes a Werewolf by Night encounter.', ['Halfway to Sanity'],run(MK21,3,'Read after Too Tough to Die. Includes the 2022 annual.'),group('Moon Knight',2021,13,18)+group('Moon Knight Annual',2022,1,1),['Hunter’s Moon','Werewolf by Night']),
 '9781302525651':entry('Assassins target people from Marc’s past as the Midnight Mission faces dangers that cross into dreams. Tigra pursues the Midnight Man, and Venom arrives seeking help.', ['Road to Ruin'],run(MK21,4,'Read after Halfway to Sanity.'),group('Moon Knight',2021,19,24),['Tigra','Venom']),
 '9781302527624':entry('Marc’s mercenary past returns as he and Hunter’s Moon pursue the Black Spectre. The threat to Manhattan raises the stakes for the Midnight Mission in the concluding volume of the 2021 series.', ['The Last Days of Moon Knight'],run(MK21,5,'Read after Road to Ruin. The story continues in Vengeance of the Moon Knight (2024), outside this pilot.'),group('Moon Knight',2021,25,30),['Hunter’s Moon']),
 '9781302527334':entry('To save a young victim of death cultists, Moon Knight travels into the underworld. Layla El-Faouly, the Scarlet Scarab, becomes an unlikely ally as enemies from his past stand in the way.', ['City of the Dead'],run('Moon Knight — City of the Dead (2023)',1,'A separate miniseries using the Midnight Mission setting.'),group('Moon Knight: City of the Dead',2023,1,5),['Scarlet Scarab'],coverage='Complete miniseries'),
 '9781302498139':entry('This larger collection combines Peter and Mary Jane’s wedding, an encounter with Wolverine, and Kraven’s attempt to prove himself superior to Spider-Man. It contains the same central Kraven story as the shorter Marvel Select edition, plus surrounding adventures.', ["Kraven’s Last Hunt",'Peter and Mary Jane’s wedding','Spider-Man versus Wolverine'],run('Spider-Man — Kraven’s Last Hunt',1,'Choose this for the central arc plus surrounding stories; Marvel Select is the shorter alternative.',True),group('Amazing Spider-Man',1963,289,294)+group('Amazing Spider-Man Annual',1964,20,21)+group('Spider-Man versus Wolverine',1987,1,1)+group('Web of Spider-Man',1985,29,32)+group('Peter Parker, The Spectacular Spider-Man',1976,131,132),['Wolverine','Kraven the Hunter'],coverage='Complete arc + extras'),
 '9781302935818':entry('Kraven sets out to prove that he can surpass Spider-Man by taking his place. This focused edition collects the central six-part psychological confrontation without the extra wedding and Wolverine stories in the Epic Collection.', ['Kraven’s Last Hunt'],run('Spider-Man — Kraven’s Last Hunt',1,'Choose this for the focused six-part arc, or the Epic Collection for extra context.'),group('Web of Spider-Man',1985,31,32)+group('Amazing Spider-Man',1963,293,294)+group('Peter Parker, The Spectacular Spider-Man',1976,131,132),['Kraven the Hunter'],starting=True,coverage='Complete arc'),
 '9781302516468':entry('An alternate version of Peter Parker ages in real time through decades of history. Familiar Spider-Man milestones are reimagined around an entire lifetime, making this a self-contained take on the character rather than a main-continuity reading guide.', ['Life Story'],run('Spider-Man — Life Story (2019)',1,'Standalone alternate history. This edition collects the original six issues.'),group('Spider-Man: Life Story',2019,1,6),starting=True,coverage='Complete miniseries'),
 '9781302939359':entry('What if Peter never gave up the alien costume? This alternate story follows a darker Spider-Man as the symbiote changes his response to enemies and threatens the people around him.', ['Spider’s Shadow'],run('Spider-Man — Spider’s Shadow (2021)',1,'Standalone alternate scenario, separate from the main Spider-Man timeline.'),group('Spider-Man: Spider’s Shadow',2021,1,5),coverage='Complete miniseries'),
 '9781302524708':entry('A powerless Peter and Mary Jane attempt a civilian life in Portland while someone from Kraven’s past pursues them. The miniseries explores the hunter’s legacy and the consequences of that history.', ['The Lost Hunt'],run('Spider-Man — Kraven’s Last Hunt',2,'Suggested after Kraven’s Last Hunt for context. Set after Spider-Man: The Final Adventure, not immediately after Last Hunt.'),group('Spider-Man: The Lost Hunt',2022,1,5),['Kraven the Hunter'],coverage='Complete miniseries'),
 '9781302507206':entry('Peter’s work and relationships are upended as a new era begins. An alien invasion, a villainous roommate, and an unusual Peter-versus-Spider-Man problem reset the stakes for Nick Spencer’s run.', ['Back to Basics'],run(ASM,1,'Start Nick Spencer’s run here. Includes material from Free Comic Book Day 2018.'),group('Amazing Spider-Man',2018,1,5),starting=True),
 '9781302508647':entry('Living with Boomerang pulls Peter into a bar full of villains. A theft by New York’s Thieves Guild draws Black Cat into the story while Peter struggles to keep his rebuilt life from falling apart.', ['Friends and Foes'],run(ASM,2,'Read after Back to Basics.'),group('Amazing Spider-Man',2018,6,10),['Black Cat','Boomerang']),
 '9781302513276':entry('J. Jonah Jameson’s public support for Spider-Man creates fresh complications. Threats to Jonah and Aunt May collide with the Enforcers, Taskmaster, and Black Ant as Peter tries to protect his family and allies.', ['Lifetime Achievement'],run(ASM,3,'Read after Friends and Foes.'),group('Amazing Spider-Man',2018,11,15)),
 '9781302514587':entry('Kraven’s plans bring animal-themed superhumans together for a hunt in Central Park. Spider-Man and the Lizard are caught in a dangerous contest where the hunters and prey are not as straightforward as they appear.', ['Hunted'],run(ASM,4,'Read after Lifetime Achievement. This is a later Kraven story, distinct from Kraven’s Last Hunt.'),group('Amazing Spider-Man',2018,16,23),['Kraven the Hunter','Lizard']),
 '9780785171188':entry('Early in his career, Ultimate Peter Parker takes on Wilson Fisk, the Kingpin. The young hero’s pursuit of revenge puts him up against an established criminal empire.', ['Learning Curve'],run(USM,2,'Volume 1 is not enriched in this pilot. Start with it before this volume.'),group('Ultimate Spider-Man',2000,8,13),['Kingpin']),
 '9780785171195':entry('The Ultimate version of Doctor Octopus hunts people linked to the accident that transformed him. Peter faces a dangerous new opponent while still learning how to be Spider-Man.', ['Double Trouble'],run(USM,3,'Read after Learning Curve.'),group('Ultimate Spider-Man',2000,14,21),['Doctor Octopus']),
 '9780785171201':entry('The Green Goblin returns while New York’s criminals put pressure on Spider-Man. Peter’s early superhero life grows more dangerous as an old enemy re-enters the picture.', ['Legacy'],run(USM,4,'Read after Double Trouble.'),group('Ultimate Spider-Man',2000,22,27),['Green Goblin']),
 '9780785180012':entry('The X-Men confront a future ruled by mutant-hunting Sentinels. This edition includes the original two-part Days of Future Past story, surrounding team adventures, and an annual; the whole book is broader than the title arc.', ['Days of Future Past'],run('X-Men — Days of Future Past',1,'The title arc is issues 141–142. This edition also includes 138–140, 143, and Annual 4.'),group('Uncanny X-Men',1963,138,143)+group('X-Men Annual',1970,4,4),starting=True,coverage='Complete arc + extras'),
}

def main():
    catalog = json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))
    review_matches = json.loads((ROOT/'data/review-matches.json').read_text())
    enriched = {}
    for book in catalog['books']:
        isbn=book['isbn']
        if isbn not in NOTES: continue
        note=NOTES[isbn].copy()
        google_file=CACHE/f'google-{isbn}.html'
        if not google_file.exists(): continue
        google=Page(google_file.read_text(encoding='utf-8'))
        bib=google.plain.partition('Bibliographic information')[2]
        if isbn not in bib: raise ValueError(f'ISBN not confirmed on Google Books: {isbn}')
        length=re.search(r'\bLength\s+(\d+)\s+pages',bib)
        source_url=google.meta.get('og:url','')
        note.update(pages=int(length[1]) if length else None,pagesSource=source_url, checkedAt=DATE,
                    sources=[{'label':'Google Books · edition, contents, and synopsis','url':source_url}],
                    coverUrl=google.meta.get('og:image'), coverSource=source_url)
        primary='Moon Knight' if 'moon knight' in book['title'].lower() else ('X-Men' if book['title'].lower().startswith('x-men') else 'Spider-Man')
        note['characters']=[{'name':primary,'role':'Lead / team','source':source_url}]+[{'name':name,'role':'Featured in source synopsis','source':source_url} for name in note.pop('guests')]
        note['contentsNote']='Issue list shows verified primary contents; bonus pages and supplemental material may not be fully indexed.'
        if isbn=='9781302943509': note['stories'][1]['coverage']='Event tie-in only'
        if isbn=='9781302514587': note['contentsNote']='Also includes Hunted supplemental issues. The publisher lists one suffix as 16.HH; this discrepancy is not used for overlap matching.'
        if isbn=='9780785180012': note['sources'].append({'label':'Marvel · original Days of Future Past arc','url':'https://www.marvel.com/comics/issue/107703/x-men_days_of_future'})
        catalog_file=CACHE/f'{isbn}.html'
        if catalog_file.exists():
            cp=parse_catalog(catalog_file.read_text(encoding='utf-8'))
            if cp['sourceTitle'] != book['title']: raise ValueError(f'Catalog title mismatch: {isbn}')
            note['hooplaUrls']=[f'https://www.hoopladigital.com/title/{i}' for i in cp['hooplaIds']]
            note['sources'].append({'label':'OCLS · catalog and Hoopla edition link','url':book['catalogUrl']})
        review_file=CACHE/f'review-{isbn}.html'
        if isbn in review_matches and review_file.exists():
            rp=parse_review(review_file.read_text(encoding='utf-8'))
            assert rp['criticScore'] is not None and rp['criticCount'], f'Review parse failed: {isbn}'
            url='https://comicbookroundup.com/comic-books/trades/marvel-comics/'+review_matches[isbn]
            note['review']={k:rp[k] for k in ['title','criticScore','criticCount','userScore','userCount']}
            note['review'].update(url=url,checkedAt=DATE,scope='Critic aggregate for reviewed issues in this collection; bonus material may not be covered.',match='Matched by collection title, creators, series, and issue range; not by ISBN.')
            note['coverUrl']=rp['coverUrl'] or note['coverUrl']; note['coverSource']=url
            note['sources'].append({'label':'Comic Book Roundup · scores and reviewed issues','url':url})
        enriched[book['id']]=note
    automatic_file=ROOT/'data/automatic-enrichment.json'
    if automatic_file.exists():
        enriched={**json.loads(automatic_file.read_text(encoding='utf-8')), **enriched}
    editorial_file=ROOT/'data/editorial-enrichment.json'
    if editorial_file.exists():
        enriched.update(json.loads(editorial_file.read_text(encoding='utf-8')))
    out={'updatedAt':DATE,'books':enriched}
    (ROOT/'public/enrichment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    report={'catalogRecords':len(catalog['books']),'hooplaListed':sum(b['hooplaListed'] for b in catalog['books']),
            'enriched':len(enriched),'pages':sum(b['pages'] is not None for b in enriched.values()),
            'reviews':sum('review' in b for b in enriched.values()),'hooplaLinks':sum(bool(b.get('hooplaUrls')) for b in enriched.values())}
    (ROOT/'data/audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__': main()
