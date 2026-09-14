"""Fifty individually researched X-Men collections, September 2026."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT, write_json
from build_pilot import group, run

ROWS='''Rogue's team is attacked from within as a coordinated campaign targets mutants with knowledge of the future. The survivors must uncover the attackers' objective before their dwindling allies are eliminated.|Blinded by the Light|Rogue, Iceman, Cannonball, Marauders
Jubilee confronts her vampire past, Magik defends Russia, and Psylocke's Japanese vacation becomes a supernatural fight. Laura frees captive mutants while Logan battles the vampire invasion in his own companion miniseries.|Blood Hunt: mutant tie-ins|Jubilee, Magik, Psylocke, X-23, Wolverine
Xarus brings a vampire army to San Francisco, forcing the mutants to seek a cure and consider an alliance with Dracula. These companion stories follow the science team, Storm, Gambit and Blade through the crisis.|Curse of the Mutants: companion battles|Storm, Gambit, Blade, Dracula, Xarus
Scott and Jean spend their honeymoon in a distant future raising the child who becomes Cable under Apocalypse's shadow. A second journey takes them to Victorian England and Nathaniel Essex's transformation into Mister Sinister.|The Adventures of Cyclops and Phoenix / The Further Adventures|Cyclops, Jean Grey, Cable, Apocalypse, Mister Sinister, Stryfe
Jean Grey's growing Phoenix power becomes a cosmic catastrophe. Her teammates face a choice between saving someone they love and protecting the lives threatened by that power; this edition adds aftermath and archival material.|The Dark Phoenix Saga / aftermath|Jean Grey, Professor X
The Phoenix's corruption turns Jean Grey's extraordinary power against the universe. The X-Men struggle to reach their friend as the crisis becomes a reckoning beyond Earth.|The Dark Phoenix Saga|Jean Grey, Professor X
This prequel traces the decades that turn an anti-mutant political backlash into the Sentinel dystopia of Days of Future Past. Kate Pryde and her allies struggle to survive a future closing around them.|Days of Future Past: the road to dystopia|Kitty Pryde, Wolverine, Colossus, Storm, Banshee, Angel, Cyclops, Professor X, Magneto
Havok leads the Starjammers against his brother Vulcan, now emperor of the Shi'ar. Their family conflict becomes a struggle over the empire's future and the lives of its subjects.|Emperor Vulcan|Havok, Vulcan, Starjammers
Teenage mutants balance Bayville High with Xavier's training in this animated-series universe. Established teachers guide a growing class through rival students, Mimic and the mystery behind their enemies.|X-Men Evolution: Bayville adventures|Cyclops, Jean Grey, Nightcrawler, Rogue, Kitty Pryde, Spyke, Professor X, Wolverine, Storm, Beast, Iceman
After injuring a friend, Sunspot leaves the school with Warlock and joins a strange teenage gang. Their adventures take the runaways beyond the familiar world of Xavier's students.|Fallen Angels: Sunspot's runaway adventure|Sunspot, Warlock, Fallen Angels
Magneto's Acolytes escalate their attacks while a deadly illness spreads through mutantkind. This edition brings together selected Fatal Attractions chapters and surrounding Uncanny stories about the mounting cost of the conflict.|Fatal Attractions / Acolytes / Legacy Virus|Magneto, Acolytes
Xavier's original five students learn how to be heroes through encounters with the Lizard, Doctor Strange and alien intruders. These later-written early adventures mix school life, unusual field trips and superhero guest stars.|First Class: Mutants 101|Cyclops, Jean Grey, Angel, Beast, Iceman, Professor X, Lizard, Doctor Strange, Thor, Gorilla-Man
The young original team heads beyond the classroom for Monster Island, road trips and encounters with other heroes. When Sentinels threaten Quicksilver and Scarlet Witch, the students must help without their usual powers.|First Class: Road Trips|Cyclops, Jean Grey, Angel, Beast, Iceman, Invisible Woman, Quicksilver, Scarlet Witch, Man-Thing, Black Widow
After Krakoa's fall, Scott and Jean confront a mystery before her departure for space, while Sally Floyd investigates Xavier. Other stories follow Havok, Madelyne, Omega Red, Beast and Magneto as they try to build lives after the mutant nation.|From the Ashes: post-Krakoa character stories|Cyclops, Jean Grey, Professor X, Havok, Madelyne Pryor, Omega Red, Beast, Magneto
Kitty befriends Lockheed, Storm confronts Callisto, and Rogue's arrival unsettles the team. Wolverine's plans with Mariko and Cyclops's relationship with Madelyne Pryor unfold under the lingering shadow of Phoenix.|From the Ashes: Morlocks / Rogue joins / Madelyne Pryor|Kitty Pryde, Lockheed, Storm, Callisto, Rogue, Wolverine, Mariko Yashida, Cyclops, Madelyne Pryor
Gambit's solo adventures take him through thefts, old relationships and clashes with X-Cutioner. Stories of young Remy and his father's wartime exploits accompany missions involving Rogue, Storm and Sabretooth.|Gambit: solo missions and family history|Gambit, Rogue, Storm, Sabretooth, X-Cutioner, Hydro-Man
Time travel exposes the Thieves Guild's history as Gambit's changing powers offer both romance and danger. Becoming a leader draws Remy into an assassination contest and the mystery of his patron, the New Son.|Gambit: Thieves Guild / Assassination Game / New Son|Gambit, Rogue, Mister Sinister, Bullseye, Archangel, X-Cutioner, Ego
Gambit returns to New Orleans after learning that Bella Donna may still live. Two solo miniseries explore the lovers' complicated histories, with rival guilds, family obligations and old enemies standing in their way.|Gambit and Rogue: the early solo miniseries|Gambit, Rogue, Bella Donna
Ed Piskor retells the arrival of the international X-Men and their expanding cosmic adventures. The compressed history moves through the Shi'ar, Phoenix and Brood eras with a new visual interpretation of familiar stories.|Grand Design: Second Genesis|Wolverine, Storm, Colossus, Nightcrawler, Sunfire, Thunderbird, Banshee, Kitty Pryde, Carol Danvers, Starjammers
The final Grand Design installment reworks the mutant crises of the eighties into a connected history. Mutant Massacre, Fall of the Mutants, Inferno and X-Tinction Agenda lead toward the blue-and-gold era.|Grand Design: X-Tinction|Jubilee, Gambit, Psylocke, Mister Sinister
Piskor's complete six-part retelling connects Xavier's founding team, the international recruits, Phoenix and the upheavals of the eighties. This is a compressed reinterpretation of X-Men history rather than a reprint of all the original events.|Grand Design trilogy|Professor X, Jean Grey
The opening Grand Design chapters weave the origins and early history of Xavier's team into one continuous account. Piskor's retelling provides context for the later Second Genesis and X-Tinction installments.|Grand Design: the original team|Professor X, Cyclops, Jean Grey, Angel, Beast, Iceman
Apocalypse chooses twelve mutants to compete for the responsibility of testing Earth's mutantkind. Rival heroes and villains face a brutal tournament while Archangel tries to stop another generation from suffering under the same philosophy.|Heir of Apocalypse|Apocalypse, Cable, Exodus, Emma Frost, Forge, Dani Moonstar, Mister Sinister, Archangel
Krakoa invites the world to a night of diplomacy and spectacle. The first elected X-Men team is unveiled, and a planet-sized surprise changes mutantkind's place in the solar system.|Hellfire Gala 2021: election and planetary transformation|X-Men
The first Hellfire Gala unfolds across a dozen team books, revealing the conversations and conflicts around Krakoa's grand announcement. This expanded edition includes the central election and planetary transformation alongside the night's companion stories.|Hellfire Gala 2021: Red Carpet Collection|X-Men, Marauders, Excalibur, X-Force, New Mutants, X-Factor, Hellions
Orchis turns Krakoa's annual celebration into a catastrophe that launches Fall of X. Companion stories follow the losing election candidates, Rogue and Captain America's emerging alliance, and Iron Man's fight against Stark Sentinels.|Hellfire Gala 2023 / Fall of X begins|Rogue, Captain America, Iron Man, Orchis
Emma tries to hold the second Gala together as revelations disrupt the party. Wolverine and Spider-Man pursue a dangerous intruder, while the Secret X-Men embark on a separate mission involving the Shi'ar.|Hellfire Gala 2022 / Secret X-Men|Emma Frost, Wolverine, Spider-Man, Cannonball, Sunspot
Three annual celebrations chart Krakoa's changing fortunes: a planetary triumph, a disrupted second election, and the Orchis assault that starts Fall of X. This combined edition includes companion adventures and election-candidate stories.|Hellfire Galas 2021–2023|Spider-Man, Wolverine, Iron Man, Orchis
Bobby Drake's visit home becomes a time-travel adventure involving his family and the mysterious Oblivion. The solo tale explores what Iceman can do when removed from the safety of his usual team.|Iceman: family, time travel and Oblivion|Iceman, Oblivion
Kitty's trip to Japan exposes her to Ogun, who wants to turn her into an assassin. Wolverine confronts his former teacher to help Kitty reclaim herself from the training forced upon her.|Kitty Pryde and Wolverine: Ogun|Kitty Pryde, Wolverine, Ogun
Following Xavier's death, Legion tries to control his fractured mind and choose how to honor his father. Helping exploited mutant twins and entering the Jean Grey School expose threats both outside him and inside his own psyche.|Prodigal: Legion's new direction|Legion
Storm searches for purpose after losing her powers, first through her relationship with Forge and then on a journey in Africa. Other Barry Windsor-Smith stories bring Wolverine into conflict with Lady Deathstrike and follow a threat to Dazzler.|Lifedeath I and II / Wounded Wolf / Dazzler|Storm, Forge, Wolverine, Lady Deathstrike, Spiral, Dazzler
The first mutant birth since M-Day triggers a race among the X-Men, Marauders and Purifiers. Protecting the child becomes a battle over mutantkind's future and begins the wider Hope storyline.|Messiah Complex|Marauders, Purifiers, Hope Summers
Magneto's renewed confrontation with the X-Men launches the blue-team era. The opening adventures then bring Omega Red into the conflict, giving the newly reorganized team another dangerous enemy.|Mutant Genesis / Omega Red|Magneto, Omega Red
Bastion leads a government-backed campaign to eradicate mutants. Multiple teams and solo heroes struggle through the assault as Operation Zero Tolerance reaches across the X-Men's world.|Operation Zero Tolerance|Bastion, X-Force, Wolverine, Cable
The Stepford Cuckoos show disturbing signs of a Phoenix connection. The X-Men investigate the sisters' link to Weapon Plus as the apparent return of the cosmic force raises questions about what they really are.|Phoenix Warsong|Stepford Cuckoos
The Phoenix returns to Earth searching for Jean Grey, only to find that she is dead. Its attempt to reunite with its former host forces the X-Men into another painful confrontation with the cosmic force.|Phoenix Endsong|Jean Grey
Morrison's final New X-Men stories bring the apparent return of Magneto and a devastating attack on New York. The story then jumps into a possible future where the Phoenix becomes central to mutantkind's fate.|Planet X / Here Comes Tomorrow|Jean Grey, Magneto, Professor X
The Avengers and Fantastic Four uncover the mystery behind Jean Grey's return. Her resurrection leads into the original team's reunion as X-Factor and reexamines what happened during the Phoenix tragedy.|Phoenix Rising / the original X-Factor forms|Jean Grey, Avengers, Fantastic Four, X-Factor, She-Hulk, Hercules
A reality-warping child linked to one of the team's allies threatens the X-Men in body and mind. The Proteus battle tests the team's courage immediately before the Dark Phoenix era.|Proteus|Proteus
Hickman's early Krakoan stories follow the new mutant nation's place in the world and trouble involving the Brood and Shi'ar. Giant-Size chapters send Jean and Emma to help Storm and give Nightcrawler his own mystery.|Krakoa's early missions / Giant-Size X-Men|Jean Grey, Emma Frost, Storm, Nightcrawler, Starjammers
The later Hickman chapters revisit the Vault, confront Nimrod and bring the elected X-Men team to the Hellfire Gala. Giant-Size stories add missions for Magneto, Fantomex and Storm.|The Vault / Nimrod / Hellfire Gala / Giant-Size X-Men|Cyclops, Jean Grey, Storm, Magneto, Fantomex, Nimrod
Onslaught's approach is felt through Post, Psylocke's grave injuries and Dark Beast's schemes. The collection combines late pre-event missions with historical stories about Sinister and Apocalypse.|Road to Onslaught: Post / Dark Beast / historical origins|Psylocke, Archangel, Wolverine, Doctor Strange, Dark Beast, Mister Sinister, Apocalypse
Abigail Brand must share control of S.W.O.R.D. with Henry Gyrich after Secret Invasion. Beast's arrival complicates an already tense workplace as Gyrich moves to expel every alien from Earth.|S.W.O.R.D.: No Time to Breathe|Abigail Brand, Beast, Henry Peter Gyrich
A surge in anti-mutant hostility exposes an irreconcilable difference between Cyclops and Wolverine over how to protect their people. The confrontation divides the X-Men and sets up separate futures for the school and Utopia.|Schism: Cyclops and Wolverine divide|Cyclops, Wolverine
Cable brings Hope back to the present, where an organized campaign to eradicate mutants makes her its central target. The X-Men suffer mounting losses while trying to protect the child at the heart of Cyclops's hopes.|Second Coming: Hope returns|Cable, Hope Summers, Cyclops
Mojoworld's struggle for freedom entangles several mutant teams before the collection moves to Colossus's family crisis in Russia. Psylocke's identity mystery and Rogue and Gambit's relationship continue in the surrounding blue-team chapters.|Shattershot / Soul Skinner / Psylocke identity crisis|Colossus, Magik, Psylocke, Gambit, Rogue, Longshot, Shatterstar, X-Factor, X-Force
A visit to Colossus's family becomes a crisis when Soul Skinner and the Russian government threaten Illyana. The team then seeks answers to Psylocke's identity mystery in Japan while Rogue and Gambit confront their feelings.|Skinning of Souls / Psylocke identity crisis|Colossus, Magik, Psylocke, Silver Samurai, Gambit, Rogue
The Starjammers aid the X-Men against threats to the Shi'ar and the parasitic Brood. Corsair's family connection and Carol Danvers's changing future accompany a separate quest starring the space pirates themselves.|Starjammers: Shi'ar adventures / Brood / solo quest|Starjammers, Corsair, Hepzibah, Ch'od, Raza, Carol Danvers, Lilandra
Hope grieves Cable after Extermination, while another story explains Cyclops's return. A holiday anthology brings lighter moments for Rogue, Gambit, Magneto and Jubilee alongside the Summers family's losses and reunions.|Cable's aftermath / Cyclops returns / mutant holidays|Hope Summers, Cable, Jean Grey, Cyclops, Rogue, Gambit, Magneto, Jubilee'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/deep-batch-05.json').read_text());rows=ROWS.splitlines();assert len(ids)==len(rows)==50
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books'];by={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'));before=copy.deepcopy(payload['books'])
    path=ROOT/'data/editorial-enrichment.json';editorial=json.loads(path.read_text(encoding='utf-8'));notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        b=by[isbn];d=copy.deepcopy(before.get(b['id'],{}));source=d.get('pagesSource') or b['catalogUrl'];summary,story,guests=row.split('|')
        for key in ['level','automation','review']:d.pop(key,None)
        d.update(summary=summary,pages=d.get('pages'),pagesSource=source,coverSource=d.get('coverSource',source),checkedAt=datetime.date.today().isoformat(),editorialBatch='deep-05',stories=[dict(title=story,coverage='Story highlights; see edition and reading notes')],characters=[dict(name=n,role='Featured in cited synopsis; not a complete cameo index',source=source) for n in dict.fromkeys(['X-Men']+[g.strip() for g in guests.split(',') if g.strip()])],issueKeys=[],startingPoint=False)
        d['sources']=[dict(label='ISBN metadata / publisher synopsis' if d.get('pages') else 'OCLS · imported edition record',url=source)]
        d['readingPath']=run('X-Men — '+story,1,'Separate collection. No universal chronology is implied.')
        d['contentsNote']='Only confirmed whole issues are indexed. Partial material, annuals or extras not explicitly indexed may also overlap.'
        d['checks']=dict(story='Individually reviewed synopsis',characters='Featured appearances; cameos incomplete',edition='ISBN metadata retained where available',review='No reliable score matched',readingOrder='Collection sequence and crossover guidance reviewed')
        notes[i]=d
    configure(notes,by,ids,before)
    for i,isbn in enumerate(ids,1):editorial[by[isbn]['id']]=notes[i];payload['books'][by[isbn]['id']]=notes[i]
    targets={by[isbn]['id'] for isbn in ids};assert all(payload['books'][k]==v for k,v in before.items() if k not in targets)
    write_json(path,editorial);payload['updatedAt']=datetime.date.today().isoformat()
    for directory in [ROOT/'public',ROOT/'dist/client']:write_json(directory/'enrichment.json',payload)
    # Refresh only these books' review-queue reasons; retain the collector's state.
    queuepath=ROOT/'public/review-queue.json'
    if queuepath.exists():
        q=json.loads(queuepath.read_text(encoding='utf-8'));entries={v['id']:v for v in q['records']}
        for i,isbn in enumerate(ids,1):
            b=by[isbn];d=notes[i];reasons=[]
            if not d.get('review'):reasons.append('Review score needs an exact collection match')
            if not d.get('pages'):reasons.append('Page count missing')
            if d['checks'].get('edition')!='ISBN metadata retained where available':reasons.append(d['checks']['edition'])
            entries.pop(b['id'],None)
            if reasons:entries[b['id']]=dict(id=b['id'],title=b['title'],status='editorial',reasons=reasons)
        q['records']=list(entries.values())
        for directory in [ROOT/'public',ROOT/'dist/client']:write_json(directory/'review-queue.json',q)
        for directory in [ROOT/'public',ROOT/'dist/client']:
            sp=directory/'auto-enrichment-status.json'
            if sp.exists():
                status=json.loads(sp.read_text(encoding="utf-8"));status.update(editorial=sum(d.get('level')!='basic' for d in payload['books'].values()),automatic=sum(bool(d.get('automation')) for d in payload['books'].values()),reviewCount=len(entries));write_json(sp,status)
    report=dict(batch='deep-05',records=50,reviews=sum(bool(d.get('review')) for d in notes.values()),missingPages=sum(not d.get('pages') for d in notes.values()),remainingXMen=sum('x-men' in b['title'].lower() and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog),notes='50 researched records; previous work preserved. Edition uncertainties and missing ratings remain explicit.')
    write_json(ROOT/'data/deep-batch-05-audit.json',report);print(json.dumps(report))

def configure(n,by,ids,before):
    def cite(i,url,label='Additional story / contents source; print page count not imported'):
        n[i]['sources'].append(dict(label=label,url=url))
    def issues(i,*specs):
        n[i]['issueKeys']=[key for series,year,a,b in specs for key in group(series,year,a,b)]
    def path(i,name,pos,note,alternative=False):n[i]['readingPath']=run(name,pos,note,alternative)
    def note(i,text):n[i]['readingPath']['note']=text
    def caution(i,text):n[i]['contentsNote']=text;n[i]['checks']['edition']=text
    issues(1,('X-Men',1991,200,204))
    cite(1,'https://marvel.fandom.com/wiki/X-Men_Vol_2_202','Issue index · appearances and Marauders storyline')
    for c in n[1]['characters']:c['source']='https://marvel.fandom.com/wiki/X-Men_Vol_2_202'
    note(1,'Follows the Supernovas-era Rogue team and leads directly into Messiah Complex, which begins the next X-Men issue range.')
    issues(2,('Wolverine: Blood Hunt',2024,1,4))
    for title in ['Jubilee','Magik','Psylocke','Laura Kinney the Wolverine']:n[2]['issueKeys']+=group('X-Men: Blood Hunt - '+title,2024,1,1)
    note(2,'Companion stories to Blood Hunt, after Fall of X. The main Blood Hunt miniseries is not in this collection; the title range 1–4 refers only to Wolverine’s portion.')
    issues(3,('X-Men: Curse of the Mutants - Storm & Gambit',2010,1,1),('X-Men: Curse of the Mutants - Smoke & Blood',2010,1,1),('X-Men: Curse of the Mutants - Blade',2010,1,1),('X-Men vs. Vampires',2010,1,2),('Uncanny X-Men',1963,159,159))
    note(3,'Companion material to Curse of the Mutants in X-Men (2010), not the later Blood Hunt event. The main six-part X-Men story is separate.')
    issues(4,('The Adventures of Cyclops and Phoenix',1994,1,4),('The Further Adventures of Cyclops and Phoenix',1996,1,4))
    note(4,'Read Adventures before Further Adventures in publication order, despite the second story traveling farther into the past. Partial Valentine material is not indexed.')
    for i in [5,6]:
        issues(i,('Uncanny X-Men',1963,129,138));path(i,'X-Men — classic era collections',129,'Alternative Dark Phoenix edition; overlaps the Milestones and Fate of the Phoenix collections.',True)
    caution(6,'Catalog title says 129–137 but the ISBN metadata says 129–138. Index follows the metadata; exact final chapter needs digital-edition confirmation.')
    cite(6,'https://www.marvel.com/comics/discover/1930/chris-claremont','Marvel · classic X-Men storyline context')
    # The identical core story was checked in the previous batch; carry its source, not its page count.
    prior=before[by['9781302514440']['id']]
    n[6]['sources']+=copy.deepcopy(prior['sources'])
    for c in n[6]['characters']:c['source']=prior['sources'][0]['url']
    issues(7,('X-Men: Days of Future Past - Doomsday',2023,1,4))
    note(7,'A later-written prequel to the alternate future of Days of Future Past. Read the original Uncanny 141–142 first; these are not those issues.')
    issues(8,('X-Men: Emperor Vulcan',2007,1,5));note(8,'Follows Rise and Fall of the Shi’ar Empire. The Vulcan/Starjammers conflict continues beyond this miniseries.')
    issues(9,('X-Men: Evolution',2001,1,9));n[9]['startingPoint']=True
    note(9,'Separate animated-series continuity, not main-universe X-Men chronology. This volume collects the nine-issue comic series.')
    issues(10,('Fallen Angels',1987,1,8))
    cite(10,'https://www.marvel.com/comics/series/23621/fallen_angels_%281987%29','Marvel · eight-issue Fallen Angels series')
    cite(10,'https://www.marvel.com/characters/sunspot','Marvel · Sunspot’s Fallen Angels adventure')
    cite(10,'https://marvel.fandom.com/wiki/X-Men%3A_Fallen_Angels_Vol_1_1','Collection index · original Fallen Angels 1–8')
    for c in n[10]['characters']:c['source']='https://www.marvel.com/characters/sunspot'
    caution(10,'Matching-title Jo Duffy collection and original 1987 series checked; this digital ISBN’s exact extras and page count remain unconfirmed. Eight core issues indexed; bonus contents not inferred.')
    note(10,'Original 1987 runaways, not the 2019 Krakoa series of the same name. A New Mutants companion adventure.')
    issues(11,('Uncanny X-Men',1963,298,300),('Uncanny X-Men',1963,303,304),('Uncanny X-Men',1963,315,315),('X-Factor',1986,92,92),('X-Force',1991,25,25),('X-Men Unlimited',1993,2,2),('X-Men',1991,25,25))
    path(11,'X-Men — classic era collections',298,'Compare the listed chapters with the Fatal Attractions Epic. Editions differ; do not treat these as successive books.',True)
    caution(11,'Imported publisher copy calls this the entire saga, but its listed contents omit important chapters found in other event editions. Only the explicitly listed ranges are indexed.')
    issues(12,('X-Men: First Class',2006,1,8),('X-Men: First Class Special',2007,1,1));issues(13,('X-Men: First Class',2007,1,9))
    for i,p in [(12,1),(13,2)]:path(i,'X-Men — First Class (2006–2007)',p,'Later-written early-team adventures. Read the 2006 miniseries before the 2007 ongoing series.');n[i]['startingPoint']=p==1
    for title in ["X-Men: Xavier's Secret",'X-Men: Demons and Death','X-Men: Tooth and Claw','X-Men: The Undertow']:n[14]['issueKeys']+=group(title,2025,1,1)
    note(14,'Post-Krakoa Infinity Comic stories reprinted as four 2025 one-shots. Completely different from the classic Claremont From the Ashes collection; Infinity chapter equivalences are not inferred.')
    issues(15,('Uncanny X-Men',1963,168,176));path(15,'X-Men — classic era collections',168,'Overlaps the 168–175 portion of God Loves, Man Kills Epic and adds 176; does not include that Epic’s graphic novel or Wolverine miniseries.',True)
    issues(16,('Gambit',1999,1,11));n[16]['issueKeys']+=['Gambit (1999) #1/2','Gambit Annual (1999) #1']
    issues(17,('Gambit',1999,12,25));n[17]['issueKeys']+=['Gambit Annual (2000) #1']
    for i,p in [(16,1),(17,2)]:path(i,'Gambit — 1999 complete collections',p,'Read Volume 1 before Volume 2; these collect the 1999 solo series. Partial bonus stories are not indexed.');n[i]['startingPoint']=p==1
    issues(18,('Gambit',1993,1,4),('Rogue',1995,1,4));note(18,'Earlier solo miniseries, before the 1999 Gambit collections. Not the later Mr. and Mrs. X marriage-era series.')
    issues(19,('X-Men: Grand Design - Second Genesis',2018,1,2))
    issues(20,('X-Men: Grand Design - X-Tinction',2019,1,2),('Uncanny X-Men',1963,268,268))
    issues(21,('X-Men: Grand Design',2017,1,2),('X-Men: Grand Design - Second Genesis',2018,1,2),('X-Men: Grand Design - X-Tinction',2019,1,2))
    issues(22,('X-Men: Grand Design',2017,1,2),('Uncanny X-Men',1963,1,1))
    for i,p in [(22,1),(19,2),(20,3),(21,1)]:path(i,'X-Men — Grand Design',p,'Read Grand Design, Second Genesis, then X-Tinction. Trilogy is the combined alternative. Retellings do not count as the original event issues.',i==21);n[i]['startingPoint']=p==1
    caution(19,'Publisher mentions a Giant-Size X-Men reprint without its year/number. That bonus is not included in the overlap index.')
    issues(23,('X-Men: Heir of Apocalypse',2024,1,4));note(23,'After the Krakoa era. Establishes Apocalypse’s successor before the later Age of Revelation storyline; not part of the original Age of Apocalypse.')
    base=[('Marauders',2019,21,21),('X-Men',2019,21,21),('Planet-Size X-Men',2021,1,1),('S.W.O.R.D.',2020,6,6)]
    issues(24,*base);issues(25,*base,('Excalibur',2019,21,21),('X-Force',2019,20,20),('New Mutants',2019,19,19),('X-Factor',2020,10,10),('Hellions',2020,12,12),('Way of X',2021,3,3),('X-Corp',2021,2,2),('Wolverine',2020,13,13))
    issues(26,('X-Men: Hellfire Gala',2023,1,1),('X-Men Unlimited Infinity Comic',2021,100,105),('Invincible Iron Man',2022,8,8))
    issues(27,('X-Men: Hellfire Gala',2022,1,1),('Secret X-Men',2022,1,1),('X-Men Unlimited Infinity Comic',2021,50,55),('Amazing Spider-Man',2022,9,9))
    n[28]['issueKeys']=n[24]['issueKeys']+n[26]['issueKeys']+n[27]['issueKeys']
    for i,p in [(24,1),(25,1),(27,2),(26,3),(28,1)]:path(i,'X-Men — Hellfire Galas (2021–2023)',p,'2021 first, 2022 second, 2023 third. Ongoing team stories occur between the annual Galas; these are not consecutive nights.',i in [25,28])
    note(25,'Expanded alternative to the four-issue 2021 Gala edition, including eight more team chapters. Does not include the 2022 or 2023 Galas.')
    note(28,'Combines the central 2021 Gala with 2022 and 2023 collections. It does not include every extra 2021 team issue in Red Carpet. Partial FCBD and Classic material are not indexed.')
    issues(29,('Iceman',1984,1,4));note(29,'The original Iceman solo miniseries, not his later 2017 or Astonishing Iceman runs. Partial Bizarre Adventures material is not a whole-issue overlap.')
    issues(30,('Kitty Pryde and Wolverine',1984,1,6));note(30,'Also included in the Lifedeath Epic Collection, but not the smaller Barry Windsor-Smith Lifedeath book. Read as a complete six-part adventure.');n[30]['startingPoint']=True
    issues(31,('X-Men Legacy',2012,1,6));path(31,'X-Men Legacy — Si Spurrier (2012)',1,'Legion-centered relaunch after Xavier’s death. Separate from Mike Carey’s earlier X-Men Legacy numbering.');n[31]['startingPoint']=True
    for num in [186,198,205,214]:n[32]['issueKeys']+=group('Uncanny X-Men',1963,num,num)
    cite(32,'https://www.marvel.com/articles/podcasts/complete-storm-episode-transcript-women-of-marvel-podcast','Marvel · Lifedeath I and II: Storm without powers')
    caution(32,'Imported synopsis describes a different Storm/Forge adventure. Replaced with the Lifedeath plot supported by Marvel; issue list retained. Partial issue 53 is not indexed.')
    note(32,'Artist-focused selection of separate stories, not the larger Lifedeath Epic. Lifedeath I and II are 186 and 198; intervening chapters are not included.')
    issues(33,('X-Men: Messiah Complex',2007,1,1),('Uncanny X-Men',1963,492,494),('X-Men',1991,205,207),('New X-Men',2004,44,46),('X-Factor',2005,25,27))
    path(33,'X-Men — Messiah storyline',1,'Same central crossover as the Milestones edition. Messiah War follows and Second Coming concludes the wider Hope story.',True)
    issues(34,('X-Men',1991,1,7));path(34,'X-Men — 1991 blue team',1,'Starts the 1991 series. Larger Epics combine some of these chapters with other teams; compare overlap before reading both.')
    issues(35,('Generation X',1994,26,31),('X-Force',1991,67,70),('X-Men',1991,65,70),('Uncanny X-Men',1963,346,346),('Wolverine',1988,115,118),('Cable',1993,45,47),('X-Man',1995,30,30));note(35,'The 1997 Bastion crossover, long before Messiah Complex and Second Coming. Event collection rather than a single-team numbered volume.')
    issues(36,('X-Men: Phoenix - Warsong',2006,1,5));issues(37,('X-Men: Phoenix - Endsong',2005,1,5))
    for i,p in [(37,1),(36,2)]:path(i,'X-Men — Phoenix Endsong / Warsong',p,'Read Endsong before Warsong. These follow Morrison’s New X-Men and are distinct from the original Dark Phoenix Saga.')
    issues(38,('New X-Men',2001,146,154));path(38,'New X-Men — Grant Morrison (2001)',6,'Alternative collecting Planet X and Here Comes Tomorrow, overlapping the final two smaller Morrison volumes. Starts late in the run.',True)
    issues(39,('Avengers',1963,263,263),('Fantastic Four',1961,286,286),('X-Factor',1986,1,1));note(39,'Jean’s return after Dark Phoenix and the original X-Factor launch. Not the later Phoenix Resurrection miniseries; partial Classic material is not indexed.')
    issues(40,('Uncanny X-Men',1963,125,128));caution(40,'Classic X-Men 32–33 and 36 contain reprint/backup material; excluded from whole-issue overlaps to avoid counting duplicated main chapters twice.')
    path(40,'X-Men — classic era collections',125,'Proteus immediately precedes Dark Phoenix at issue 129. Extra Classic material accompanies the core four-part arc.',True)
    issues(41,('X-Men',2019,1,9),('Giant-Size X-Men: Jean Grey and Emma Frost',2020,1,1),('Giant-Size X-Men: Nightcrawler',2020,1,1))
    issues(42,('X-Men',2019,10,12),('X-Men',2019,16,21),('Giant-Size X-Men: Magneto',2020,1,1),('Giant-Size X-Men: Fantomex',2020,1,1),('Giant-Size X-Men: Storm',2020,1,1))
    path(41,'X-Men — Jonathan Hickman (2019)',1,'Larger alternative beginning at issue 1 despite the Reign of X title. Start with House of X/Powers of X. Includes two Giant-Size stories.',True)
    path(42,'X-Men — Jonathan Hickman (2019)',2.5,'Larger alternative finishing Hickman’s run; issues 13–15 are absent and belong to X of Swords. Issue 21 overlaps the 2021 Hellfire Gala.',True)
    cite(43,'https://prhcomics.com/book/?isbn=9781302965488','Publisher · matching-title print omnibus contents and synopsis')
    issues(43,('X-Men',1991,48,52),('Uncanny X-Men',1963,329,332),('Archangel',1996,1,1),('X-Men/Brood',1996,1,2),('X-Men & ClanDestine',1996,1,2),('X-Men Unlimited',1993,10,10),('Wolverine',1988,101,101),('Storm',1996,1,4),('The Further Adventures of Cyclops and Phoenix',1996,1,4),('Rise of Apocalypse',1996,1,4),('Black Knight: Exodus',1996,1,1),('Fantastic Four',1961,19,19))
    caution(43,'Matching-title print omnibus checked; exact digital ISBN contents/page count remain unconfirmed. Yearbook extras omitted from the whole-story overlap index.')
    path(43,'X-Men — Road to Onslaught omnibuses',2,'After omnibus 1 and before Onslaught. Not the smaller Road to Onslaught Volume 2 paperback; includes historical miniseries.',True)
    issues(44,('S.W.O.R.D.',2009,1,5));note(44,'Gillen’s 2009 series after Secret Invasion, not the 2020 Krakoa S.W.O.R.D. relaunch. Also overlaps the Gillen Uncanny omnibus.')
    issues(45,('X-Men: Schism',2011,1,5));cite(45,'https://www.marvel.com/comics/collection/39382/x-schism_hardcover','Marvel · Schism context; print edition has additional chapters')
    caution(45,'Core Schism 1–5 indexed. Publisher print and review collections include differing extras, unconfirmed for this digital ISBN; no collection score attached.')
    note(45,'Leads into Wolverine & the X-Men (2011) and Gillen’s Uncanny X-Men (2011). Regenesis and other companion chapters may require separate reading.')
    issues(46,('X-Men: Second Coming',2010,1,2),('Uncanny X-Men',1963,523,525),('New Mutants',2009,12,14),('X-Men Legacy',2008,235,237),('X-Force',2008,26,28))
    cite(46,'https://www.marvel.com/comics/collection/29519/','Marvel · Second Coming plot and core collected chapters')
    for c in n[46]['characters']:c['source']='https://www.marvel.com/comics/collection/29519/'
    caution(46,'Imported description incorrectly described Age of X. Replaced using Marvel’s Second Coming listing; core event contents checked against matching-title print edition, digital extras unconfirmed.')
    n[46]['pages']=None
    n[46]['checks']['edition']+=' Page count withheld because the imported metadata conflicts with the book’s identity.'
    path(46,'X-Men — Messiah storyline',3,'After Messiah Complex, Cable’s travels and Messiah War. This is the main Second Coming event, not the Revelations companion.')
    issues(47,('X-Men',1991,17,24),('X-Men Annual',1992,1,2),('X-Men Annual',1970,16,16));issues(48,('X-Men',1991,17,24))
    path(47,'X-Men — 1991 blue team',17,'Larger alternative to Skinning of Souls with Shattershot annual material. Partial X-Factor/X-Force annual content is not indexed.',True)
    path(48,'X-Men — 1991 blue team',17,'Follows X-Cutioner’s Song (14–16). Same main chapters as Shattershot, without that edition’s annuals and extras.',True)
    issues(49,('Uncanny X-Men',1963,107,108),('Uncanny X-Men',1963,154,158),('Uncanny X-Men',1963,161,167),('X-Men: Spotlight on Starjammers',1990,1,2));note(49,'Creator/character collection across different periods. Overlaps classic Phoenix/Brood-era collections; it is not a continuous Uncanny run.')
    issues(50,('Uncanny X-Men Annual',2019,1,1),('X-Men: The Exterminated',2018,1,1),('Merry X-Men Holiday Special',2018,1,1));note(50,'After Extermination (2018), leading toward the 2019 Uncanny era. Holiday stories are an anthology, not a single chronological chapter.')
    # Solo-character branding alone does not establish the team's appearance.
    for i in [4,10,16,17,18,29,30,44]:n[i]['characters']=[c for c in n[i]['characters'] if c['name']!='X-Men']
    scores=[(19,'x-men-grand-design',8.9,12,None,None),(20,'x-men-grand-design',9,11,8,1),(22,'x-men-grand-design',8.8,18,None,None),(31,'x-men-legacy-(2012)',6.9,31,10,1)]
    for i,slug,critic,count,user,ucount in scores:
        url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
        n[i]['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=ucount,url=url,checkedAt=n[i]['checkedAt'],title=by[ids[i-1]]['title'],match='Matching trade row: series, story and core issue range; not ISBN.',scope='Aggregate of the reviewed core issues. Recolored reprints and other bonus material are not scored.')
        cite(i,url,'Comic Book Roundup · matching trade row');n[i]['checks']['review']='Matching core collection reviewed'
    i=23;url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/x-men-heir-of-apocalypse-(2024)'
    n[i]['review']=dict(criticScore=7.0,criticCount=19,userScore=7.4,userCount=55,url=url,checkedAt=n[i]['checkedAt'],title=by[ids[i-1]]['title'],match='All four issues of the completed miniseries match this collection.',scope='Completed four-issue series aggregate, not a separately reviewed trade edition.')
    cite(i,url,'Comic Book Roundup · completed four-issue series');n[i]['checks']['review']='Complete matching miniseries aggregate'
    n[21]['checks']['review']='Omnibus review row not attached to differently titled Trilogy edition'
    for i in n:n[i]['issueKeys']=list(dict.fromkeys(n[i]['issueKeys']))

if __name__=='__main__':main()

