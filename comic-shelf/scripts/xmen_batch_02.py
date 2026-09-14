"""Second frozen batch of fifty source-reviewed X-Men collections."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT,write_json
from build_pilot import group,run

ROWS='''In the altered House of M world, the Hellions receive an assassination order against a human resistance leader. The New Mutants intervene, hoping to prevent a mission with potentially disastrous international consequences.|House of M: New X-Men|Hellions, New Mutants
Captain Britain returns from his wider responsibilities to confront a major threat. Meanwhile, Psylocke and Rachel are caught in a predicament within the altered House of M setting.|House of M: Uncanny X-Men|Captain Britain, Psylocke, Rachel Summers
Hulk's return sends shockwaves through the mutant school and several other corners of the superhero world. This collection combines the X-Men confrontation with Ant-Man, Initiative, Ghost Rider and Iron Man tie-ins.|World War Hulk tie-ins|Hulk, Wolverine, Ghost Rider, Iron Man, Ant-Man
The Quiet Council struggles to govern Krakoa after Inferno. Filling Magneto's vacant seat, Destiny's prophecies and preparations for another Hellfire Gala expose competing ambitions behind the nation's apparent unity.|Quiet Council / Immortal X-Men Volume 1|Magneto, Destiny, Emma Frost, Selene
Judgment Day puts the Quiet Council under fresh pressure. Nightcrawler considers extreme measures as the rulers of Krakoa confront a crisis that tests both their political choices and their convictions.|Judgment Day / Immortal X-Men Volume 2|Nightcrawler
The aftermath of Sins of Sinister forces Storm and the Council to reckon with what happened. A decision over another Council vacancy runs alongside revelations about Nathaniel Essex's surviving clones.|Sins of Sinister aftermath / Sinister Four|Storm, Colossus, Mister Sinister
After Orchis attacks the Hellfire Gala, Xavier confronts the collapse of his dream while displaced mutants seek safety. Exodus, Sebastian Shaw and Jean Grey follow very different paths through the catastrophe.|Fall of X / Immortal X-Men Volume 4|Professor X, Exodus, Sebastian Shaw, Jean Grey
The mysteries running through Immortal X-Men converge with the final struggle over Krakoa. The White Hot Room, the Phoenix and the question of Hope's future become central to this concluding chapter.|X-Men Forever / end of Krakoa|Hope Summers, Phoenix
Beast discovers that the Terrigen threat leaves mutants little time before Earth becomes uninhabitable for them. The resulting confrontation brings the Inhumans and X-Men into open war.|Inhumans vs. X-Men|Beast, Inhumans
Kitty's trouble in Japan draws Wolverine into a life-changing adventure. Back in New York, the team faces the Hellfire Club and Kulan Gath, while additional stories bring Alpha Flight into the collection.|Kitty Pryde and Wolverine / Kulan Gath|Kitty Pryde, Wolverine, Hellfire Club, Alpha Flight
Storm's journey through Africa accompanies rising tension around Xavier's health. The X-Men and New Mutants travel to Asgard, Magneto faces an international tribunal, and Nightcrawler stars in a separate adventure.|Lifedeath II / Asgardian Wars / Magneto’s trial|Storm, Professor X, Nightcrawler, Magneto, Juggernaut, New Mutants, Loki
Storm and Cyclops contest leadership as family changes and the Beyonder's shadow unsettle the team. Encounters involving Rachel, Wolverine and the Hellfire Club accompany the miniseries introducing Longshot.|Leadership challenge / Longshot|Storm, Cyclops, Rachel Summers, Wolverine, Nightcrawler, Longshot, Hellfire Club
Cyclops and Emma reorganize the school into competing student squads. Friends face separation and new loyalties as the young mutants discover that changes in school policy can have deeply personal consequences.|Choosing Sides|Cyclops, Emma Frost
The destruction of Genosha opens Morrison's run with a catastrophe that reshapes the team's world. The collection establishes the new direction for Xavier's school and includes the accompanying annual.|E Is for Extinction|
The U-Men's harvesting of mutant body parts creates a new danger while tensions at home grow. Jean's powers and the crisis surrounding Xavier complicate the team's efforts to respond.|Imperial|Cyclops, Jean Grey, Professor X, U-Men
This collection continues Morrison's run with New Worlds. Its ISBN-matched listing confirms issues 127–133, but the supplied plot text appears to repeat earlier Cassandra Nova material; a corrected synopsis still needs verification.|New Worlds|
A student adopts the name Kid Omega and leads a revolt inside Xavier's school. The institution's promise of safety is tested when conflict erupts between the very mutants it exists to protect.|Riot at Xavier’s|Kid Omega
Wolverine, Cyclops and Fantomex investigate the weapons program connected to Logan's past. Their search extends beyond familiar territory and exposes disturbing secrets about the forces that created living weapons.|Assault on Weapon Plus|Wolverine, Cyclops, Fantomex
Magneto's apparent return turns a long-hidden threat into a direct attack on the X-Men. This is the late-run Planet X storyline, following the team's investigation of Weapon Plus.|Planet X|Magneto
A jump 150 years into the future introduces a changed mutant world and new versions of familiar figures. The crisis there becomes part of the conclusion to Morrison's present-day story.|Here Comes Tomorrow|
Character-focused stories explore the mutant community around the Morrison era. Heroes and enemies take turns in the spotlight, with adventures involving grief, rescue missions, family and the team's public image.|New X-Men companion stories|Phoenix, Wolverine, Beast, Storm, Psylocke, Cyclops, Rogue, Nightcrawler, Professor X, Emma Frost, Kitty Pryde, Magneto, Sabretooth, Juggernaut
Cassandra Nova's assault on mutantkind begins with Genosha and expands into a personal attack on Xavier and his team. This larger edition combines the opening Morrison collections, including the U-Men threat and annual.|E Is for Extinction / Imperial|Cassandra Nova, Emma Frost, Xorn, Jean Grey, Beast, Professor X
The closing Morrison stories move from Weapon Plus to Magneto's attack and a distant future. This edition starts partway through the smaller Weapon Plus collection and continues through the run's finale.|Weapon Plus / Planet X / Here Comes Tomorrow|Wolverine, Cyclops, Fantomex, Magneto, Phoenix
A haunting at the school puts the students on an investigation of their own. Prodigy's ability to absorb knowledge raises a second question: whether permanently retaining it would be a gift or a danger.|Haunted|Prodigy, New Mutants
An exposed relationship, grief for a teacher and preparations for a school dance test the students' friendships. A villain chooses the adults' absence as an opportunity to strike.|X-Posed / Campfire / Year’s End|New Mutants
House of M gives way to widespread depowering and increasingly lethal attacks on the school. The remaining students form a new squad as X-23 arrives and Reverend Stryker's campaign threatens their survival.|House of M / Childhood’s End|New Mutants, Hellions, X-23, Reverend Stryker
The Skrulls invade San Francisco and discover the X-Men at their new home. Cyclops and his team must defend the city against an enemy that has made special preparations for mutant resistance.|Secret Invasion: X-Men|Cyclops, Skrulls
Daken joins the assault on Asgard while his true loyalties remain uncertain. A separate New Mutants chapter follows Dani Moonstar's responsibilities toward the dead during the siege.|Siege: mutant tie-ins|Daken, Dani Moonstar, New Mutants
Spider-Man takes a guidance-counselor job at the Jean Grey Academy and forms a special student class. His work at the mutant school brings him into conflict with Sauron and Stegron.|Spider-Man & the X-Men|Spider-Man, Sauron, Stegron
Hisako wants an ordinary school life, but manifestations of urban legends draw her toward unexpected powers. Armor and Maystorm begin a new mutant story set in the reimagined Ultimate universe.|Fears and Hates|Armor, Maystorm
The young mutants seek guidance from Kanon while investigating a concealed murder and the origins of their powers. The Children of the Atom and the Shadow King's schemes deepen the danger around them.|Children of the Atom|Armor, Maystorm, Psylocke, Surge, Shadow King, Viper
Conflict with the Children of the Atom spills into the mutants' relationships and the Astral Plane. Hisako's struggle with the Shadow King threatens both her friends and their surrounding reality.|The Realm of the Mind|Armor, Maystorm, Shadow King
Armor's confrontation with the Shadow King reaches its climax as the group's enemies regroup. The consequences of her journey into the Astral Plane shape the team's final struggle in this series.|Children’s Whereabouts|Armor, Shadow King
The original Ultimate X-Men begin their battle against Sentinels and Magneto before falling into the hands of Weapon X. This larger edition combines the material of the first two smaller collections.|The Tomorrow People / Return to Weapon X|Professor X, Magneto, Wolverine
Professor Xavier recruits young mutants to stand between anti-mutant violence and Magneto's campaign against humanity. This opens the original Ultimate team's story, separate from Peach Momoko's later universe.|The Tomorrow People|Professor X, Magneto
Gambit's return creates a new problem for the team. The thief's intentions and the object of his interest gradually emerge as the X-Men try to work out what he is planning.|Cry Wolf|Gambit
An attempt to rescue Longshot from a televised hunt turns the X-Men into participants. Mojo holds one of their teammates captive and demands that they surrender the fugitive.|The Most Dangerous Game|Longshot, Mojo, Angel
Storm and Wolverine encounter Lady Deathstrike on a trip north. A separate annual adventure brings Juggernaut into conflict with Rogue and Gambit.|Hard Lessons|Storm, Wolverine, Lady Deathstrike, Juggernaut, Rogue, Gambit
Lorna Dane's involvement in a terrible incident forces the team to decide whether to protect her from S.H.I.E.L.D. Emma Frost and Alex Summers become part of the resulting crisis.|Magnetic North|Lorna Dane, Emma Frost, Havok
After the confrontation of Magnetic North, the team's attempt at a normal night out is disrupted by the mysterious Magician. Wolverine also encounters a former teammate seeking revenge.|Phoenix?|Wolverine, Magician
The Magician's rising popularity conceals more than the team understands about its newest member. Jean struggles with the results of Shi'ar testing while Dazzler begins to stir.|Magical|Magician, Jean Grey, Dazzler
Cable arrives from a tragic future and disrupts Xavier's carefully managed world. His secrets threaten the team, while an additional story explores Emma Frost's rival school.|Cable|Cable, Professor X, Emma Frost
Bishop builds a new team to carry forward Xavier's work. Their immediate challenge is a renewed wave of Sentinel attacks against mutants, backed by a hidden adversary.|Sentinels|Bishop
This volume is titled Apocalypse and confirms issues 89–93. The publisher's plot text instead describes a Shadow King and Storm story, so a reliable arc-specific synopsis remains pending rather than repeating that possible mismatch.|Apocalypse|
In the aftermath of the battle with Apocalypse, a new adversary pushes the team toward dangerous choices. The young mutants must decide how much they are willing to change in order to win.|Absolute Power|
The X-Men are captured and pressed into service by Weapon X. Their prospects of escape depend on Wolverine and whether he can overcome the program that helped make him a weapon.|Return to Weapon X|Wolverine
An international trip intended to spread Xavier's message exposes a secret from his past. The students discover that fear and hostility toward mutants extend well beyond their home country.|World Tour|Professor X
The Hellfire Club invites the X-Men into its circle, concealing a plan that has been developing for years. The invitation draws the team toward a threat hidden behind apparent hospitality.|Hellfire & Brimstone|Hellfire Club
The government sends the Ultimates against the X-Men, setting two young superhuman teams on a collision course. Xavier's students must face Captain America, Iron Man, Thor and their allies.|Ultimate War|Ultimates, Captain America, Iron Man, Thor, Professor X
Magneto returns while the X-Men are still recovering from their confrontations with Weapon X and the Ultimates. His renewed threat tests whether Xavier's team can withstand another major assault.|Return of the King|Magneto, Professor X'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/xmen-batch-02.json').read_text());rows=ROWS.splitlines();assert len(ids)==len(rows)==50
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books'];by_isbn={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))
    path=ROOT/'data/editorial-enrichment.json';editorial=json.loads(path.read_text(encoding='utf-8'))
    notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        summary,story,guests=row.split('|');b=by_isbn[isbn];d=copy.deepcopy(payload['books'][b['id']]);source=d['pagesSource'];d.pop('level',None)
        d.update(summary=summary,stories=[dict(title=story,coverage='Collection; see edition and reading notes')],characters=[dict(name='X-Men',role='Featured team / incarnation',source=source)]+[dict(name=n.strip(),role='Featured in publisher synopsis',source=source) for n in guests.split(',') if n.strip()],issueKeys=[],startingPoint=False,editorialBatch='xmen-02',checkedAt=datetime.date.today().isoformat())
        d['sources']=[dict(label='Google Books · exact ISBN publisher synopsis and contents',url=source)]
        d['readingPath']=run('X-Men — '+story,1,'Separate collection. No universal X-Men chronology is implied.')
        d['contentsNote']='Only explicitly indexed issues are used for overlap matching; additional or partial material may overlap other collections.'
        d['checks']=dict(edition='ISBN matched',story='Publisher synopsis reviewed',characters='Featured characters only; cameo coverage incomplete',readingOrder='Volume or collection guidance',review='No verified collection score attached')
        notes[i]=d
    def seq(indices,name,series,year,ranges,positions=None):
        for pos,(i,(first,last)) in enumerate(zip(indices,ranges),1):
            p=positions[pos-1] if positions else pos
            notes[i]['readingPath']=run(name,p,'Follow numbered volumes within this series; gaps and crossovers may require other books.')
            notes[i]['issueKeys']=group(series,year,first,last);notes[i]['startingPoint']=p==1
    seq([4,5,6,7],'Immortal X-Men — Gillen (2022)','Immortal X-Men',2022,[(1,5),(7,10),(11,13),(14,18)])
    notes[4]['startingPoint']=False;notes[4]['readingPath']['note']='Run opening, but assumes Krakoa and Inferno context. Not a general X-Men introduction.'
    notes[5]['readingPath']['note']='Judgment Day period. This edition starts at issue 7, leaving issue 6 outside these first two volumes.'
    notes[6]['readingPath']['note']='After Sins of Sinister. Includes X-Men: Before the Fall — Sinister Four #1, not the complete Sins of Sinister event.'
    notes[7]['readingPath']['note']='Fall of X: follows the Hellfire Gala attack.'
    notes[8]['readingPath']=run('Immortal X-Men — Gillen (2022)',5,'X-Men Forever (2024), not Immortal issues 19 onward. Read with Fall of the House of X / Rise of the Powers of X for the wider ending.')
    notes[8]['issueKeys']=group('X-Men: Forever',2024,1,4)
    seq([10,11,12],'Uncanny X-Men — Masterworks','Uncanny X-Men',1963,[(189,193),(194,200),(201,209)],[11,12,13])
    notes[10]['issueKeys']+=group('Kitty Pryde and Wolverine',1984,1,6)
    notes[11]['issueKeys']+=group('Nightcrawler',1985,1,4)
    notes[12]['issueKeys']+=group('Longshot',1985,1,6)
    seq([14,15,16,17,18,19,20],'New X-Men — Grant Morrison (2001)','New X-Men',2001,[(114,117),(118,126),(127,133),(134,138),(139,145),(146,150),(151,154)])
    notes[14]['issueKeys']+=group('New X-Men Annual',2001,1,1)
    notes[16]['checks']['story']='Plot synopsis withheld: source appears to repeat earlier material'
    notes[16]['contentsNote']='Both the cached ISBN listing and Marvel collection page repeat a Cassandra Nova synopsis associated with earlier material. Issue range is confirmed; plot needs checking.'
    notes[21]['readingPath']['note']='Optional character stories around Morrison’s era; not an eighth volume of the main run.'
    for i,pos,first,last in [(22,1,114,126),(23,5.5,142,154)]:
        notes[i]['readingPath']=run('New X-Men — Grant Morrison (2001)',pos,'Larger alternative edition. Compare included issues before reading alongside the smaller volumes.',True)
        notes[i]['issueKeys']=group('New X-Men',2001,first,last)
    notes[22]['issueKeys']+=group('New X-Men Annual',2001,1,1);notes[22]['startingPoint']=True
    notes[23]['readingPath']['note']='Begins at 142, overlapping only the latter part of Assault on Weapon Plus, then all of Planet X and Here Comes Tomorrow. Does not bridge 127–141 from the first Epic in this batch.'
    seq([13,24,25],'New X-Men — Academy X (2004)','New X-Men',2004,[(1,6),(7,11),(12,15)])
    notes[24]['contentsNote']='Catalog lists 7–11, but digital synopsis says 7–12. Issue 12 is disputed and excluded from this edition’s overlap index.'
    notes[25]['contentsNote']='Publisher confirms 12–15 plus the Yearbook Special. Haunted may also contain 12, but that overlap is disputed.'
    notes[1]['readingPath']=run('New X-Men — Academy X (2004)',4,'House of M alternate-reality chapters; overlaps the opening of Childhood’s End.')
    notes[1]['issueKeys']=group('New X-Men',2004,16,19)
    notes[26]['readingPath']=run('New X-Men — Academy X (2004)',4,'Collects the House of M chapters followed by the depowering aftermath. Overlaps the separate House of M volume.',True)
    notes[26]['issueKeys']=group('New X-Men',2004,16,32)
    notes[2]['issueKeys']=group('Uncanny X-Men',1963,462,465)
    notes[9]['issueKeys']=group('IvX',2016,0,6);notes[9]['readingPath']['note']='Main event. Read alongside the All-New and Extraordinary IvX tie-in volumes from batch 1, which do not replace this series.'
    for i in [1,2,3,27,28]:notes[i]['stories'][0]['coverage']='Event tie-in; not the full event'
    notes[3]['issueKeys']=group('World War Hulk: X-Men',2007,1,3)
    notes[27]['issueKeys']=group('Secret Invasion: X-Men',2008,1,4)
    notes[28]['characters']=[c for c in notes[28]['characters'] if c['name']!='X-Men']
    notes[28]['contentsNote']='Dark Wolverine 82–84 and New Mutants (2009) 11 plus handbook material. X-Men branding does not verify a main-team appearance.'
    notes[29]['issueKeys']=group('Spider-Man & the X-Men',2015,1,6)
    seq([30,31,32,33],'Ultimate X-Men — Peach Momoko (2024)','Ultimate X-Men',2024,[(1,6),(7,12),(13,18),(19,24)])
    for i in [30,31,32,33]:notes[i]['readingPath']['note']+=' This is a separate universe from Ultimate X-Men (2001).'
    notes[30]['contentsNote']='Also includes Ultimate Universe #1; no score attached because the review trade row lists only four issues, unlike this edition’s six plus the special.'
    old=[35,46,47,48,50,36,37,38,39,40,41,42,43,44,45]
    ranges=[(1,6),(7,12),(13,20),(21,25),(26,33),(50,53),(54,57),(58,60),(61,65),(66,71),(72,74),(75,80),(81,86),(89,93),(94,97)]
    seq(old,'Ultimate X-Men — original universe (2001)','Ultimate X-Men',2001,ranges,[1,2,3,4,6,10,11,12,13,14,15,16,17,18,19])
    notes[49]['readingPath']=run('Ultimate X-Men — original universe (2001)',5,'Ultimate War crossover miniseries, between Hellfire & Brimstone and Return of the King; not Ultimate X-Men issues 1–4.')
    notes[49]['issueKeys']=group('Ultimate War',2002,1,4)
    notes[36]['readingPath']['note']='Volume 10. Volumes 7–9 (issues 34–49) are outside this batch; do not jump directly from Volume 6.'
    notes[34]['readingPath']=run('Ultimate X-Men — original universe (2001)',1,'Alternative to Volumes 1 and 2; also contains issue 1/2, which is not indexed.',True)
    notes[34]['issueKeys']=group('Ultimate X-Men',2001,1,12);notes[34]['startingPoint']=True
    notes[38]['issueKeys']+=group('Ultimate X-Men Annual',2005,1,1)
    notes[41]['issueKeys']+=group('Ultimate X-Men Annual',2005,2,2)
    notes[43]['contentsNote']='Digital source lists 81–86; review row lists eight issues. Score withheld until the range is reconciled. Issues 87–88 are not covered by these indexed volumes.'
    notes[44]['checks']['story']='Plot synopsis withheld: title and publisher blurb appear inconsistent'
    notes[44]['readingPath']['note']='After Sentinels, with issues 87–88 unconfirmed in these editions. Issues 89–93 are confirmed, but the publisher plot text needs review.'
    for i,url in [(16,'https://www.marvel.com/comics/collection/1324/new_x-men_new_worlds_trade_paperback'),(40,'https://www.marvel.com/comics/collection/5057/ultimate_x-men_vol_14_phoenix_2006'),(44,'https://www.marvel.com/comics/collection/21608/ultimate_x-men_vol_18_apocalypse_trade_paperback'),(48,'https://www.marvel.com/comics/collection/42599/ultimate_x-men_vol_4_hellfire_brimstone_trade_paperback')]:
        notes[i]['sources'].append(dict(label='Marvel · collection synopsis and contents',url=url))
        if i in [40,48]:
            for c in notes[i]['characters']:c['source']=url
    reviews={}
    def scores(slug,values):
        for i,critic,count,user,ucount in values:reviews[i]=(critic,count,user,ucount,slug)
    scores('immortal-x-men-%282022%29',[(4,8.8,57,9.6,4),(5,8.9,26,10,2),(6,8.7,25,9.5,1),(7,8.5,27,9,1)])
    scores('new-x-men-%282001%29',[(16,5,8,8.4,5),(17,7.5,5,8.8,6),(18,7.1,19,8.4,5),(19,8.1,14,8.8,5),(20,6.6,11,8,6)])
    scores('ultimate-x-men-%282024%29',[(31,7.6,17,None,None),(32,7.1,9,None,None),(33,8.6,22,None,None)])
    scores('ultimate-x-men',[(35,9,1,8.5,4),(36,7.4,5,7.5,3),(37,8,4,8,3),(38,8,5,7.2,3),(39,8,2,7.5,3),(40,5.2,7,5,3),(41,6,2,5.7,3),(42,5.4,8,5.9,4),(44,4,11,5.1,4),(45,6.7,9,3.2,4),(47,5,2,7.3,3),(48,7.2,5,7.3,3),(49,6,4,7.3,3),(50,6.6,9,7.7,3)])
    for i,(critic,count,user,ucount,slug) in reviews.items():
        d=notes[i];url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
        d['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=ucount,url=url,checkedAt=d['checkedAt'],title=by_isbn[ids[i-1]]['title'],match='Specific trade row matched by title, volume and issue count; not by ISBN.',scope='Aggregate for reviewed issues in this collection, not the entire series. Unreviewed issues and bonus material may be excluded.')
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row in Trades section',url=url));d['checks']['review']='Verified collection-row score'
    for i in [14,15,46]:notes[i]['checks']['review']='Source has reader ratings but no critic score; not fitted to the current combined-score schema'
    for i in [30,43]:notes[i]['checks']['review']='Withheld due to collected-issue count mismatch'
    notes[16]['summary']='The team’s work expands beyond the school into international mutant crises. A return to devastated Genosha brings the X-Men face to face with Polaris and a recorded message from Magneto, confronting the human cost of the destruction.'
    notes[16]['checks']['story']='Replaced questionable collection blurb using distributor context and Marvel issue 132; synopsis highlights selected contents'
    notes[16]['sources'] += [dict(label='PRH / Marvel · broader New Worlds collection, not this edition’s page count',url='https://prhcomics.com/book/?isbn=9781302961268'),dict(label='Marvel · verified Genosha chapter, issue 132',url='https://www.marvel.com/comics/issue/14951/new_x-men_2001_132/aggregate')]
    notes[16]['characters'].append(dict(name='Lorna Dane',role='Polaris; featured in issue 132',source='https://www.marvel.com/comics/issue/14951/new_x-men_2001_132/aggregate'))
    notes[16]['contentsNote']='Original collection blurb appears to repeat earlier material. Replacement summary uses publisher context and confirmed issue 132; no page count or later storyline from the larger Epic edition was imported.'
    notes[44]['summary']='Sinister’s return leads into the arrival of Apocalypse and an escalating threat to the Ultimate X-Men. The confrontation culminates in a struggle whose possible solution carries dangers of its own.'
    notes[44]['checks']['story']='Corrected against Marvel synopses for included issues 91 and 93'
    notes[44]['sources'] += [dict(label='Marvel · Apocalypse chapter, issue 91',url='https://www.marvel.com/comics/issue/20638/ultimate_x-men_2000_91'),dict(label='Marvel · Apocalypse conclusion, issue 93',url='https://www.marvel.com/comics/issue/20967/ultimate_x-men_2000_93')]
    notes[44]['characters'].append(dict(name='Apocalypse',role='Featured in verified issue synopsis',source='https://www.marvel.com/comics/issue/20638/ultimate_x-men_2000_91'))
    notes[44]['readingPath']['note']='After Sentinels, with issues 87–88 unconfirmed in these editions. Main plot checked against included issues 91 and 93 rather than the questionable collection blurb.'
    for i,isbn in enumerate(ids,1):
        b=by_isbn[isbn];editorial[b['id']]=notes[i];payload['books'][b['id']]=notes[i]
    write_json(path,editorial);payload['updatedAt']=datetime.date.today().isoformat()
    for directory in [ROOT/'public',ROOT/'dist/client']:write_json(directory/'enrichment.json',payload)
    report=dict(batch='xmen-02',records=50,storySynopses=50,correctedPlotSources=[ids[15],ids[43]],reviewMatches=len(reviews),notes='Two misleading collection blurbs corrected using additional sources. Unverified scores and disputed issues remain unfilled. Previous batches preserved.')
    write_json(ROOT/'data/xmen-batch-02-audit.json',report);print(json.dumps(report))

if __name__=='__main__':main()
