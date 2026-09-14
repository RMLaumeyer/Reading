"""Fifty editorial records based on ISBN-matched publisher synopses."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT,write_json
from build_pilot import group,run

# Rows correspond to the frozen ISBN manifest, not a changing catalog sort.
# Summary | named story/collection | characters explicitly supported by synopsis
ROWS='''Loki's scheme sends unfamiliar villains against Spider-Man and the mutant teams. A cosmic change for Spider-Man and a confrontation involving Psylocke sit among several separate event tie-ins.|Acts of Vengeance|Spider-Man, Wolverine, Psylocke, Magneto, Doctor Doom, Loki, New Mutants, Alpha Flight
A seemingly ideal mutant society treats the X-Men as perfect heroes, but rebellion challenges its enforced harmony. The collection includes the Alpha and Omega framing chapters as well as the central team miniseries.|Age of X-Man|Jean Grey, Colossus, Storm, X-23, Magneto, Nightcrawler, Apocalypse
The original five X-Men arrive in a present very different from the future they expected. Meeting the consequences of their older selves' choices forces them to reconsider Xavier's dream.|Yesterday’s X-Men|
The young time travelers keep adjusting to modern life as Mystique targets them. Young Cyclops becomes a particular focus of a threat that makes their unfamiliar surroundings still more dangerous.|Here to Stay|Cyclops, Mystique
Jean's growing powers unsettle the team while one young member considers joining adult Cyclops. A confrontation with Mastermind and an encounter with the Uncanny Avengers make their future feel increasingly uncertain.|Out of Their Depth|Jean Grey, Cyclops, Uncanny Avengers
This volume continues the young team's adventures in All-Different and adds X-Men: Gold material. The ISBN source confirms contents but supplies no plot synopsis; a detailed plot summary still needs verification.|All-Different|
The future Brotherhood returns to threaten the time-displaced team while Beast questions the consequences of bringing them forward. Jean's experiences during her interstellar trial add another complication to their uncertain future.|One Down|Beast, Jean Grey
The young X-Men cross into the Ultimate universe and encounter Miles Morales. This is a dimension-crossing adventure within their ongoing run, rather than a starting volume for the Ultimate X-Men.|The Ultimate Adventure|Miles Morales, Spider-Man
The team's space adventure becomes entangled with the Black Vortex and a kidnapping by Mr. Knife. Back on Earth, the mysterious Utopians introduce another challenge to the young mutants' future.|The Utopians / Black Vortex tie-in|Beast, Kitty Pryde, Storm
An apparently returned Doctor Octopus creates a paradox for Superior Spider-Man and the young X-Men. Bruce Banner joins the investigation as the Abomination's appearance deepens the mystery.|The Arms of the Octopus|Hulk, Spider-Man, Doctor Octopus, Abomination
Young Cyclops and his friends take to the road, determined to choose their futures despite the reputations of their older counterparts. Their attempted fresh start runs into the Blob.|Ghosts of Cyclops|Cyclops, Beast, Iceman, Angel, X-23, Oya, Kid Apocalypse, Blob
The young mutants confront the lives they fear becoming. Beast seeks help from Doctor Strange, while Evan's connection to Apocalypse makes the coming conflict especially personal.|Apocalypse Wars|Beast, Doctor Strange, Kid Apocalypse, Cyclops
Romantic tensions and the Terrigen threat test the team. The Goblin Queen's return turns their personal demons into an immediate danger, while Genesis continues to struggle with his possible future.|Hell Hath So Much Fury|Angel, X-23, Cyclops, Beast, Goblin Queen, Kid Apocalypse
The mutant-Inhuman conflict reaches a crisis as the Terrigen cloud threatens mutant survival. This collection brings together the run's final issues, an annual and X-Men Prime, rather than the main event series.|Inhumans vs. X-Men tie-in|Jean Grey, Fantomex, Karnak, Inhumans
A psychic assault draws an improvised team into the astral plane to confront the Shadow King. Familiar rules of reality become unreliable as the mutants try to keep the attack from spreading.|Life of X|Psylocke, Old Man Logan, Bishop, Archangel, Fantomex, Rogue, Gambit, Shadow King
The mysterious X proposes a rescue for the world, but Proteus returns with the power to reshape it. Psylocke must weigh her trust in X as a reality storm threatens London.|A Man Called X|Professor X, Psylocke, Proteus
Havok assembles an uneasy team to confront the Reavers and prove he can be trusted again. An accompanying annual reunites Jean Grey with old friends and the changed figure of their former mentor.|Until Our Heart Stops|Havok, Beast, Warpath, Colossus, Dazzler, Jean Grey, Angel, Iceman, Professor X
Cyclops and Emma Frost's rebuilt team faces a proposed mutant cure, followed by a dangerous enemy emerging from inside the school. This larger edition combines Gifted and Dangerous.|Gifted / Dangerous|Cyclops, Emma Frost, Wolverine, Kitty Pryde, Beast, Professor X
Emma's behavior and the Hellfire Club's plans destabilize the team before the conflict expands to Breakworld. This larger edition combines Torn and Unstoppable, including the Giant-Size conclusion.|Torn / Unstoppable|Emma Frost, Wolverine, Cyclops, Beast, Kitty Pryde
Cyclops and Emma Frost set out to reshape the team's public role, but news of a mutant cure disrupts their plans. Their confrontation with Ord produces unexpected allies and opposition.|Gifted|Cyclops, Emma Frost, Ord
A death at the school exposes an enemy the team never suspected was living among them. The X-Men must confront a threat that undermines their confidence in each other and their home.|Dangerous|
Emma Frost's unsettling behavior leaves the team vulnerable as the Hellfire Club makes its move. The question of which mutant threatens Breakworld brings their internal crisis into a much larger conflict.|Torn|Emma Frost, Hellfire Club
The team travels to face the threat from Breakworld and prevent Earth's destruction. The oversized concluding issue completes the story begun in the numbered issues.|Unstoppable|
A new base and a new direction bring the X-Men an unfamiliar mystery. This collection begins Warren Ellis's period on the title and includes the separate Ghost Boxes miniseries.|Ghost Box|
A psychic attack turns Northstar against people closest to him as the X-Men investigate the Marauders. His relationship with Kyle leads toward their wedding; earlier Northstar material supplies additional context.|Northstar / wedding storyline|Northstar, Wolverine, Karma, Marauders
Red Onslaught's psychic campaign turns the heroes' moral identities upside down. Avengers and X-Men confront former allies while villains take on unexpected roles in the struggle to stop the crisis.|AXIS|Avengers, Magneto, Scarlet Witch, Doctor Doom, Iron Man
The wider consequences of Avengers vs. X-Men unfold across team books, schools and battles in space. This companion also includes aftermath material; it supplements the main confrontation rather than replacing it.|Avengers vs. X-Men companion|Avengers, Captain America, Iron Fist, Hope Summers, Wolverine
The Avengers and X-Men go to war, with extended Versus battles collected alongside the central conflict. Conflicting issue listings for this edition mean its final numbered issue needs checking.|Avengers vs. X-Men|Avengers, Iron Man, Magneto, Spider-Man, Colossus, Captain America, Gambit
Expanded fights spotlight individual matchups from Avengers vs. X-Men. The collection focuses on the clashes themselves and includes a separate playful A-Babies vs. X-Babies story.|AVX: VS|Avengers, Cyclops, Captain America, Thing, Namor, Iron Man, Magneto, Black Panther, Storm
Civil war in Genosha draws both teams into a crisis inflamed by Exodus and Cortez. This collection assembles chapters from multiple Avengers and X-Men titles with an additional Exodus story.|Bloodties|Avengers, Exodus
Alien powers turn Earth into a prison for dangerous extraterrestrials. The Avengers, X-Men and Fantastic Four confront the resulting attacks and the forces behind the scheme.|Maximum Security|Avengers, Fantastic Four, Ronan the Accuser
Norman Osborn establishes his own mutant team as loyalties surrounding Emma Frost and Cyclops come under pressure. The collection combines the main Utopia crossover with Dark X-Men background material.|Utopia|Dark Avengers, Emma Frost, Cyclops, Norman Osborn, Namor, Cloak, Dagger, Professor X
Civil War divides X-Factor over government cooperation while Cable and Deadpool find themselves on opposing sides. These are related mutant-book tie-ins, not the Civil War: X-Men miniseries.|Civil War: X-Men Universe|X-Factor, Cable, Deadpool, Quicksilver
Tensions among the X-Men, the remaining mutants known as the 198 and their government overseers reach breaking point. The larger Civil War intensifies an already unstable situation around the mutant community.|Civil War: X-Men|
After the Hellfire Gala disaster, Madelyne Pryor forms an unsettling mutant rescue team. Infighting, Limbo and an Orchis weapon turn its mission into a struggle over who will wield the Goblin Queen's power.|The Mercy Crown|Madelyne Pryor, Havok, Gambit, Gimmick, Chasm
Five mutants who died after the attack on Krakoa undertake a mission across time and space. Their attempt to avert catastrophe attracts another traveler whose objective threatens everything they are trying to preserve.|Dead X-Men|
After House of M, Xavier's school becomes a refuge for the remaining mutants. The question is whether this apparent sanctuary offers protection or exposes its residents to a new form of danger.|The 198|
Emma Frost's history with Wilson Fisk threatens to resurface during his campaign against superheroes. A separate Winter Soldier chapter follows Bucky's attempt to recover information about his own past.|Devil’s Reign: X-Men / Winter Soldier|Emma Frost, Kingpin, Winter Soldier
An alien plant invasion coincides with the resurrection of dead mutants on Genosha. The X-Men must handle both disasters in an event tie-in that mixes a cosmic attack with supernatural chaos.|Empyre: X-Men|
Kate Pryde tries to build an ordinary life after Krakoa, but encounters with young mutants pull her back toward mentoring. Emma Frost's involvement makes staying out of mutant affairs increasingly difficult.|Duty Calls|Kitty Pryde, Emma Frost
Axo's work for a charismatic technology entrepreneur entangles him in a dangerous mystery. Emma and Kitty must understand what is happening before their student is overwhelmed; Ironheart also crosses the team's path.|The Deep End|Axo, Emma Frost, Kitty Pryde, Ironheart
Storm gathers a team to protect mutants facing another threat to their survival. X-Haven begins a new group's effort to provide safety in an increasingly hostile world.|X-Haven|Storm
Rescue missions and a journey into Nightcrawler's mind lead toward a perilous future ruled by Apocalypse. The team must confront his Horsemen to protect mutantkind in the present.|Apocalypse Wars|Storm, Jean Grey, Nightcrawler, Old Man Logan, Colossus, Iceman, Magik, Apocalypse
Magik's refuge faces a World-Eater while Colossus remains under Apocalypse's influence. Additional stories follow threatened mutant prisoners and Moon Girl's attempt to address the Terrigen crisis.|Kingdom Falls|Magik, Colossus, Nightcrawler, Iceman, Moon Girl
Storm confronts the decision to wage war against the Inhumans as Terrigen threatens to make Earth uninhabitable for mutants. This volume closes the team's run and adds the transition issue X-Men Prime.|Inhumans vs. X-Men tie-in|Storm, Forge, Old Man Logan, Magik, Jean Grey, Inhumans
Character-focused missions follow Krakoa's prominent mutants into psychic danger, isolated habitats and the artificial World. Storm's threatened life provides one of the collection's central problems.|Giant-Size character missions|Jean Grey, Emma Frost, Nightcrawler, Magneto, Fantomex, Storm
Kamala Khan is pulled into key moments in mutant history, including encounters with Krakoa, Dark Phoenix and altered realities. These new revisitations do not reprint the complete classic events whose names they invoke.|Second Genesis Revisited|Ms. Marvel
Artists recreate the landmark 1975 team's debut one page at a time. The original issue appears alongside the tribute, letting readers compare the new interpretations with the story that inspired them.|Second Genesis / Wein & Cockrum tribute|Storm, Nightcrawler, Colossus, Wolverine
Star-Lord seeks help recovering an immensely powerful artifact from Mr. Knife. The assembled crossover follows its effects across the Guardians' adventures and several mutant and cosmic titles.|The Black Vortex|Guardians of the Galaxy, Star-Lord
An alien power puts the young Jean Grey on trial for the crimes associated with Dark Phoenix. The Guardians join the time-displaced X-Men in trying to save her from punishment for her older self's history.|The Trial of Jean Grey|Guardians of the Galaxy, Jean Grey'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/xmen-batch-01.json').read_text())
    rows=ROWS.splitlines();assert len(ids)==len(rows)==50
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books']
    by_isbn={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))
    path=ROOT/'data/editorial-enrichment.json'
    editorial=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        summary,story,guests=row.split('|')
        b=by_isbn[isbn];d=copy.deepcopy(payload['books'][b['id']]);source=d['pagesSource']
        d.pop('level',None)
        d.update(summary=summary,stories=[dict(title=story,coverage='Collection; see reading and edition notes')],characters=[dict(name='X-Men',role='Featured team / X-Men collection',source=source)]+[dict(name=n.strip(),role='Featured in source synopsis',source=source) for n in guests.split(',') if n.strip()],issueKeys=[],startingPoint=False,editorialBatch='xmen-01',checkedAt=datetime.date.today().isoformat())
        d['sources']=[dict(label='Google Books · exact ISBN publisher synopsis and contents',url=source)]
        d['readingPath']=run('X-Men — '+story,1,'Read as a separate collection; no universal X-Men chronology is implied.')
        d['contentsNote']='Only explicitly verified issues appear in the overlap index; unindexed material may also overlap other collections.'
        d['checks']=dict(edition='ISBN matched',story='Synopsis reviewed',characters='Source-supported featured characters; not an exhaustive cameo index',readingOrder='Collection or run guidance, not universal chronology',review='No verified collection review attached')
        notes[i]=d
    def sequence(indices,name,series,year,ranges):
        for pos,(i,(first,last)) in enumerate(zip(indices,ranges),1):
            d=notes[i];d['readingPath']=run(name,pos,'Follow this run’s volume sequence. Event tie-ins may require the main event for wider context.')
            d['issueKeys']=group(series,year,first,last)
            d['startingPoint']=pos==1
    sequence([3,4,5,6,7,8,9],'All-New X-Men — Bendis (2012)','All-New X-Men',2012,[(1,5),(6,10),(11,15),(18,21),(25,29),(31,36),(37,41)])
    notes[6]['summary']='Battle of the Atom leaves Kitty questioning her school’s direction. X-23 joins the young team, creating new tensions with Cyclops and Jean before the two young women must work together against another threat.'
    notes[6]['checks']['story']='Publisher collection synopsis reviewed; bonus contents may differ by edition'
    for name in ['Kitty Pryde','X-23','Cyclops','Jean Grey']:
        notes[6]['characters'].append(dict(name=name,role='Featured in publisher synopsis',source='https://www.marvel.com/comics/collection/48247/all-new_x-men_vol_4_all-different_premiere_hc_hardcover'))
    notes[6]['readingPath']['note']='After Out of Their Depth, issues 16–17 are absent from these numbered volumes. This book begins at 18; seek the intervening crossover separately.'
    notes[7]['contentsNote']='Catalog and Marvel paperback list 25–30; this digital ISBN synopsis lists 25–29. Issue 30 is not indexed as confirmed for this edition.'
    notes[7]['readingPath']['note']='Read The Trial of Jean Grey (All-New X-Men 22–24) between All-Different and One Down. Issue 30 coverage remains uncertain.'
    notes[9]['readingPath']['note']='Follows The Ultimate Adventure. Includes Black Vortex chapters 38–39; use the complete crossover collection for its surrounding chapters.'
    sequence([11,12,13,14],'All-New X-Men — Inevitable (2015)','All-New X-Men',2015,[(1,6),(7,11),(12,16),(17,19)])
    sequence([15,16,17],'Astonishing X-Men (2017)','Astonishing X-Men',2017,[(1,6),(7,12),(13,17)])
    notes[17]['readingPath']['note']='Rosenberg follows Soule’s two volumes with a changed team. Also includes the 2018 annual.'
    sequence([20,21,22,23],'Astonishing X-Men — Whedon & Cassaday (2004)','Astonishing X-Men',2004,[(1,6),(7,12),(13,18),(19,24)])
    finale=group('Giant-Size Astonishing X-Men',2008,1,1)
    notes[23]['issueKeys']+=finale
    for i,pos,start,end in [(18,1,1,12),(19,3,13,24)]:
        notes[i]['readingPath']=run('Astonishing X-Men — Whedon & Cassaday (2004)',pos,'Larger alternative edition; overlaps the corresponding two smaller volumes.',True)
        notes[i]['issueKeys']=group('Astonishing X-Men',2004,start,end)+(finale if i==19 else [])
    notes[18]['startingPoint']=True
    notes[24]['issueKeys']=group('Astonishing X-Men',2004,25,30)
    notes[24]['readingPath']['note']='Ellis follows the Whedon/Cassaday run. Publisher lists Astonishing 25–30 plus Ghost Boxes 1–2; the catalog’s 1–2 label only describes the latter.'
    notes[25]['issueKeys']=group('Astonishing X-Men',2004,48,51)
    notes[25]['readingPath']['note']='Later in the 2004 series; not immediately after Ghost Box. Also contains Alpha Flight 106 and Nation X 2.'
    sequence([40,41],'Exceptional X-Men — Eve L. Ewing','Exceptional X-Men',2024,[(1,5),(6,13)])
    sequence([42,43,44,45],'Extraordinary X-Men (2015)','Extraordinary X-Men',2015,[(1,5),(6,12),(13,16),(17,20)])
    notes[45]['contentsNote']='Catalog says 17–21; publisher lists 17–20 plus X-Men Prime (2017) #1. No Extraordinary #21 is indexed.'
    for i in [14,45]:
        notes[i]['issueKeys']+=group('X-Men Prime',2017,1,1)
        notes[i]['stories'][0]['coverage']='Event tie-in, not the main Inhumans vs. X-Men series'
    for i in [1,27,29,33,34,38,39]:notes[i]['stories'][0]['coverage']='Event tie-in / companion material'
    notes[27]['readingPath']['note']='Read alongside or after the main Avengers vs. X-Men story. Includes AVX: Consequences aftermath; the malformed Avengers Academy range is not indexed.'
    notes[28]['contentsNote']='Digital synopsis says Avengers vs. X-Men 0–13; catalog says 0–12. Final issue numbering needs verification. AVX: VS 1–6 is confirmed and overlaps the separate VS book.'
    for i in [28,29]:notes[i]['issueKeys']=group('AVX: VS',2012,1,6)
    notes[29]['readingPath']['note']='Optional expanded battles alongside Avengers vs. X-Men. Overlaps the VS material included in the larger event edition.'
    notes[33]['characters']=[c for c in notes[33]['characters'] if c['name']!='X-Men']
    notes[33]['contentsNote']='Publisher confirms X-Factor (2005) 8–9 and Cable/Deadpool 30–32. Title branding alone is not treated as a verified X-Men team appearance.'
    notes[33]['issueKeys']=group('X-Factor',2005,8,9)
    notes[34]['readingPath']['note']='Read after House of M and The 198 for mutant-community context; this is a Civil War tie-in.'
    notes[37]['readingPath']['note']='House of M aftermath; precedes the situation described in Civil War: X-Men.'
    notes[35]['readingPath']['note']='Follows the Hellfire Gala disaster of the Fall of X period; not a standalone introduction to Krakoa.'
    notes[36]['readingPath']['note']='Late-Krakoa story. Wider event placement has not yet been verified; avoid treating this as a starting point.'
    notes[47]['readingPath']['note']='A new revisitation of classic events, not the original Dark Phoenix Saga, House of M or Age of Apocalypse collections.'
    notes[48]['issueKeys']=group('Giant-Size X-Men',1975,1,1)+group('Giant-Size X-Men: Tribute to Wein & Cockrum',2020,1,1)
    notes[48]['startingPoint']=True
    notes[49]['issueKeys']=group('All-New X-Men',2012,38,39)
    notes[49]['readingPath']['note']='Assembles the Black Vortex crossover across multiple titles. All-New X-Men 38–39 overlaps The Utopians; other crossover chapters are not yet indexed.'
    notes[50]['issueKeys']=group('All-New X-Men',2012,22,24)
    notes[50]['readingPath']=run('All-New X-Men — Bendis (2012)',4.5,'Read between All-Different (18–21) and One Down (25 onward). Also includes Guardians of the Galaxy 11–13.')
    extras={5:('Marvel · collection synopsis','https://www.marvel.com/comics/collection/45776/all-new_x-men_vol_3_out_of_their_depth_trade_paperback'),7:('Marvel · paperback synopsis; edition range differs','https://www.marvel.com/comics/collection/48722/all-new_x-men_vol_5_one_down_trade_paperback'),8:('Marvel publisher catalog · Ultimate Adventure synopsis','https://images.abovethetreeline.com/ea/TW/pdfs/MARBKPREVIEWSept-Dec15%20%28reduced%29.pdf')}
    for i,(label,url) in extras.items():
        notes[i]['sources'].append(dict(label=label,url=url))
        for c in notes[i]['characters']:c['source']=url
    notes[6]['sources'].append(dict(label='Marvel · matching main storyline, hardcover bonus material may differ',url='https://www.marvel.com/comics/collection/48247/all-new_x-men_vol_4_all-different_premiere_hc_hardcover'))
    reviews={
      3:(8.1,152,8.1,8,'all-new-x-men-%282012%29'),4:(8.3,125,7.5,5,'all-new-x-men-%282012%29'),5:(8.1,87,7.5,5,'all-new-x-men-%282012%29'),6:(7.2,62,7.5,4,'all-new-x-men-%282012%29'),7:(7.9,83,7.4,4,'all-new-x-men-%282012%29'),9:(7.6,42,7.2,4,'all-new-x-men-%282012%29'),
      11:(7.0,43,7.8,2,'all-new-x-men-%282015%29'),12:(6.5,19,5.5,2,'all-new-x-men-%282015%29'),13:(7.6,17,8.0,2,'all-new-x-men-%282015%29'),14:(7.9,42,6.0,2,'all-new-x-men-%282015%29'),
      15:(7.9,67,8.2,5,'astonishing-x-men-%282017%29'),16:(6.9,43,6.2,3,'astonishing-x-men-%282017%29'),17:(8.0,34,8.2,3,'astonishing-x-men-%282017%29'),
      42:(7.1,65,6.5,4,'extraordinary-x-men'),43:(6.6,50,5.7,3,'extraordinary-x-men'),44:(7.3,14,7.0,1,'extraordinary-x-men'),45:(7.8,13,8.0,1,'extraordinary-x-men')}
    for i,(critic,count,user,user_count,slug) in reviews.items():
        d=notes[i];url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
        d['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=user_count,url=url,checkedAt=d['checkedAt'],title=by_isbn[ids[i-1]]['title'],match='Specific trade row matched by title, volume and collected issue count; not by ISBN.',scope='Aggregate for reviewed issues in this trade, not the overall series. Bonus material may be excluded. Until Our Heart Stops excludes the annual; Extraordinary IvX excludes X-Men Prime.')
        d['checks']['review']='Verified trade-row score; bonus coverage may differ'
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row in Trades section',url=url))
    notes[8]['checks']['review']='Withheld: review row lists five issues, while digital contents list six; range needs confirmation'
    for i,isbn in enumerate(ids,1):
        b=by_isbn[isbn];editorial[b['id']]=notes[i];payload['books'][b['id']]=notes[i]
    write_json(path,editorial)
    payload['updatedAt']=datetime.date.today().isoformat()
    for directory in [ROOT/'public',ROOT/'dist/client']:write_json(directory/'enrichment.json',payload)
    report=dict(batch='xmen-01',records=50,storySynopses=50,contentsOnly=[],reviewMatches=len(reviews),notes='Unmatched reviews remain blank. Ultimate Adventure score withheld for issue-count mismatch. Character tags are source-supported, not exhaustive.')
    write_json(ROOT/'data/xmen-batch-01-audit.json',report)
    print(json.dumps(report))

if __name__=='__main__':main()
