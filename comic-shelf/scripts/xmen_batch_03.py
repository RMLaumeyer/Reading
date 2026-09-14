"""Third frozen set of fifty X-Men editorial records; rerunnable and additive."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT, write_json
from build_pilot import group, run

ROWS='''Wolverine's hidden past catches up with him, drawing Spider-Man and Daredevil into a fight alongside the X-Men.|Blockbuster|Wolverine, Spider-Man, Daredevil
Emma Frost introduces a government-backed mutant team with the President's support. An attack on the public unveiling forces the X-Men into action.|New Mutants|Emma Frost
The team struggles with a recent death when Mister Sinister emerges as a new threat. Grief and a dangerous newcomer shape this early Brian K. Vaughan arc.|The Tempest|Mister Sinister
Magneto's catastrophe brings a tidal wave to New York and disaster across the world. These chapters follow the Ultimate X-Men and Fantastic Four through the destruction.|Ultimatum tie-ins|Magneto, Fantastic Four
After Krakoa's fall, Rogue, Gambit and Wolverine regroup in Louisiana. Four young mutants need their help against a menacing new pursuer.|Red Wave|Rogue, Gambit, Wolverine
A murderous mutant girl uses horror-film violence to fuel hostility toward mutants. New Orleans festivities and a mission in Argentina bring further trouble for the team.|Murder Me, Mutina|Wolverine, Ransom, Deadpool, Outlaw
Mutina interrupts a celebration with an unexpected request. An old promise and the Regulators' connection to Haven House bring the team's past into its present troubles.|Where Monsters Dwell|Wolverine, Mutina
After Schism, Cyclops builds a powerful new team to protect mutantkind. Mister Sinister provides an early test of the Extinction Team's strength and judgment.|Extinction Team / Mister Sinister|Cyclops, Mister Sinister
Cyclops leads an investigation of Tabula Rasa, a place transformed into an unfamiliar ecosystem. The team must navigate its strange inhabitants and dangers.|Tabula Rasa|Cyclops
The Avengers conflict reaches Cyclops's team. Colossus's Juggernaut power, a return to Tabula Rasa and Hope's flight complicate their response.|Avengers vs. X-Men tie-ins: Gillen Volume 3|Colossus, Red Hulk, Hope Summers
Mister Sinister makes his move as the Phoenix conflict escalates. Cyclops and Emma Frost face the consequences of their growing power.|Avengers vs. X-Men tie-ins: Gillen Volume 4|Mister Sinister, Cyclops, Emma Frost
Beast and Abigail Brand face a takeover at S.W.O.R.D. before the collection moves into Gillen's Uncanny run: Breakworld's return, an empowered Juggernaut and the formation of the Extinction Team.|S.W.O.R.D. / Breaking Point / Fear Itself / Extinction Team|Beast, Abigail Brand, Magneto, Colossus, Magik, Storm, Emma Frost, Namor
Tabula Rasa and Sinister's schemes lead into the Phoenix war. The collection continues beyond the main clash into the political and personal fallout of AVX: Consequences.|Tabula Rasa / Avengers vs. X-Men / Consequences|Cyclops, Mister Sinister
A new international team sets out to rescue Xavier's original students. Their earliest missions establish the larger cast and test whether these very different recruits can work together.|Second Genesis / new team's early missions|Wolverine, Storm, Colossus, Nightcrawler, Banshee, Sunfire, Professor X, Jean Grey
Personal turning points accompany threats from the Morlocks, Mystique and the Dire Wraiths. Storm's Lifedeath story shares the volume with Illyana's separate Magik miniseries.|Lifedeath / Magik / Morlock troubles|Storm, Magik, Cyclops, Madelyne Pryor, Wolverine, Kitty Pryde, Colossus, Rogue, Mystique, Rachel Summers
Jean Grey's emergence as Phoenix opens a new phase for the team. These early Claremont adventures expand the world around Xavier's students and introduce new allies and enemies.|Phoenix emergence / early Claremont adventures|Jean Grey
An extended journey takes the X-Men from Antarctic danger through the Savage Land and onward to Japan and Canada. Their troubles continue far from their usual home.|World tour: Savage Land, Japan and Canada|
Proteus, Arcade and the White Queen confront the team. The collection introduces Kitty Pryde and Dazzler and begins the Hellfire Club material that leads into Dark Phoenix.|Proteus / opening Dark Phoenix chapters|Kitty Pryde, Dazzler, Emma Frost, Hellfire Club, Spider-Man
Jean Grey's growing power becomes a cosmic threat during the Dark Phoenix confrontation. The volume carries the crisis through its conclusion and into the team's aftermath.|Dark Phoenix Saga: conclusion and aftermath|Jean Grey
Kitty Pryde becomes the link to a future ruled by Sentinels, with a chance to prevent it in the present. Further adventures bring the team against Arcade, Doctor Doom and Magneto.|Days of Future Past / subsequent adventures|Kitty Pryde, Magneto, Mystique, Spider-Woman, Dazzler, Doctor Doom
Kitty's encounter with Emma Frost leads into a mixture of fantasy, space adventure and horror. The volume includes early Brood chapters, a Dracula encounter and Rogue's debut in an Avengers annual.|Kitty's Fairy Tale / early Brood Saga / Rogue's debut|Kitty Pryde, Emma Frost, Rogue, Mystique, Dracula, Starjammers, Fantastic Four
Xavier and Magneto's shared past precedes the closing stretch of the Brood conflict. The team and its spacefaring allies face the consequences of the alien threat.|Brood Saga: concluding chapters / Xavier and Magneto's past|Professor X, Magneto, Starjammers
The Morlocks and Rogue's arrival change life for the team. Two major companion stories join these chapters: God Loves, Man Kills and Wolverine's adventure in Japan.|God Loves, Man Kills / Wolverine in Japan / Morlocks|Wolverine, Kitty Pryde, Colossus, Rogue, Callisto
Magneto investigates efforts to turn mutants into weapons and the Hellfire Club's involvement. Psylocke's growing doubts put the team's methods under scrutiny.|Waking from the Dream|Magneto, Psylocke, Hellfire Club
Cyclops, Emma Frost, Magneto and Magik recruit mutants while operating as outlaws after the Phoenix war. Sentinel attacks and questions of trust threaten the new school.|Revolution|Cyclops, Emma Frost, Magneto, Magik
Magik's connection to Limbo brings Dormammu into the team's troubles. The effects of the Phoenix conflict continue to destabilize the outcast mutants.|Broken / Limbo crisis|Magik, Dormammu
After Battle of the Atom, Kitty and the displaced original students join Cyclops's side. Magneto faces a personal reckoning while the younger mutants encounter new tests and Inhumanity's fallout.|The Good, the Bad, the Inhuman|Kitty Pryde, Magneto
Sentinel attacks push Cyclops's team toward a confrontation with S.H.I.E.L.D. Dazzler's disappearance and the discovery of Xavier's will deepen the mystery around their enemies and their former mentor.|Vs. S.H.I.E.L.D. / Xavier's will|Cyclops, Dazzler, Mystique
Xavier's legacy continues to unsettle Cyclops and the team. Magneto's return and the aftermath of AXIS force the school to reconsider what its revolution is meant to achieve.|The Omega Mutant / Xavier's legacy|Cyclops, Magneto
Cyclops reaches a crossroads while Kitty and Magik confront monsters and Mystique pursues revenge. The collection concludes Bendis's run with the milestone issue 600.|Storyville / Bendis run finale|Cyclops, Kitty Pryde, Magik, Mystique
Magneto's public image becomes a problem for the team as people from Breakworld return. Colossus and Kitty face the consequences of their earlier encounter with that world.|Breaking Point|Magneto, Colossus, Kitty Pryde
The Serpent's power turns Juggernaut into an overwhelming threat to San Francisco. The team must find a way to stop him while Sinister's return signals further danger.|Fear Itself: Uncanny X-Men|Juggernaut, Mister Sinister
Colossus struggles with Kitty's absence while a threat from his old homeland emerges. Beast and Angel help assemble a scientific group to tackle the team's problems.|Lovelorn|Colossus, Kitty Pryde, Beast, Angel
The X-Men establish themselves in San Francisco after leaving their old home. Shorter character stories accompany the team's move and explore the lives of its wider cast.|Manifest Destiny / San Francisco arrival|Dazzler, Karma, Mercury, X-23, Colossus, Emma Frost, Graymalkin, Juggernaut
An illness strips Utopia's mutants of their powers, leaving the island vulnerable. The remaining defenders face threats involving the Collective Man and Sublime Corporation.|Quarantine|Wolverine, Rockslide, Mercury, Collective Man
Vulcan pursues revenge against the Shi'ar, drawing the X-Men into an interstellar conflict. The team must try to stop his campaign before it tears the empire apart.|The Rise and Fall of the Shi'ar Empire|Vulcan
Magneto assembles a ruthless mutant team in a dangerous new climate. Their efforts to protect mutantkind put lethal methods at the center of the mission.|Survival of the Fittest|Magneto, Sabretooth, Fantomex, Mystique, Psylocke
Psylocke investigates the disturbing condition of Archangel and its connection to Apocalypse. The mystery threatens both her teammate and Magneto's wider mission.|Apocalypse Wars: Uncanny X-Men|Psylocke, Archangel, Apocalypse
The war with the Inhumans brings Magneto and Psylocke's differences to a breaking point. An annual chapter adds another perspective on the team's troubled mission.|Inhumans vs. X-Men: Uncanny tie-ins|Magneto, Psylocke, Domino
After Second Coming, signs of new mutant life offer hope for the future. The team tries to find its direction after the struggle to bring Hope Summers home.|The Birth of Generation Hope|Hope Summers
Back from space and divided by recent events, the team faces violence connected to the Morlock tunnels. Storm returns as the underground crisis unfolds.|The Extremists|Storm, Morlocks
The Sisterhood targets the X-Men while their scientific allies pursue a mission of their own. Anti-mutant politics add another threat to life in San Francisco.|Sisterhood|Sisterhood, Simon Trask
Cyclops and Wolverine return to a shattered situation after Disassembled. They try to rebuild a team while confronting the Mutant Liberation Front and unfinished problems.|Wolverine and Cyclops: rebuilding|Cyclops, Wolverine, Mutant Liberation Front
Mounting losses and a plan to erase the mutant gene push the remaining team toward a final confrontation. The Hellfire Club and O.N.E. tighten the pressure on Cyclops and Wolverine.|Wolverine and Cyclops: final struggle|Cyclops, Wolverine, Hellfire Club
A missing-person mystery escalates into a threat involving the Horsemen of Salvation. The crisis dismantles the team's familiar world and leads toward Age of X-Man.|Disassembled / Age of X-Man lead-in|
The time-displaced original X-Men join Venom in space against the Poisons. This crossover follows Venomverse and sets up further symbiote conflict.|Poison X|Venom, Jean Grey, Cyclops, Iceman, Beast, Angel
The War of the Realms reaches Queens, where the mutants try to protect people caught in the invasion. Dani Moonstar's responsibilities connect the team to the wider conflict; additional material features other heroes.|War of the Realms: Uncanny X-Men|Dani Moonstar, Sabretooth, Doctor Strange, Wiccan, Hulkling, Loki
An adventure with the original five X-Men opens a multiverse crisis that brings together different Wolverines. The unusual team, including a zombie version of Logan, faces a Phoenix-related threat.|Original X-Men / Weapon X-Men multiverse mission|Wolverine, Phoenix
Wolverine, Deadpool, Cable, Chamber and Thunderbird form a new strike team. A rescue operation brings them into conflict with Strucker and Red Ronin.|The Real Thing|Wolverine, Deadpool, Cable, Chamber, Thunderbird
The Phoenix Corporation threatens the Jean Grey School as Wolverine fights for his life. Storm and the students resist while Quentin Quire seeks help from Cyclops.|Tomorrow Never Learns|Wolverine, Storm, Kid Omega, Cyclops, Oya'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b'); msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/xmen-batch-03.json').read_text()); rows=ROWS.splitlines(); assert len(ids)==len(rows)==50
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books']; by={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'))
    path=ROOT/'data/editorial-enrichment.json'; editorial=json.loads(path.read_text(encoding='utf-8')); notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        summary,story,guests=row.split('|'); d=copy.deepcopy(payload['books'][by[isbn]['id']]); source=d['pagesSource']
        d.pop('level',None); d.pop('review',None)
        d.update(summary=summary,stories=[dict(title=story,coverage='Selected story highlights; see collection notes')],characters=[dict(name='X-Men',role='Featured team / incarnation',source=source)]+[dict(name=n.strip(),role='Featured in source synopsis',source=source) for n in guests.split(',') if n.strip()],issueKeys=[],startingPoint=False,editorialBatch='xmen-03',checkedAt=datetime.date.today().isoformat())
        d['sources']=[dict(label='Google Books · exact ISBN publisher synopsis and contents',url=source)]
        d['readingPath']=run('X-Men — '+story,1,'Separate collection; does not imply a universal X-Men chronology.')
        d['contentsNote']='Only confirmed issues are indexed. Bonus and partial material may produce additional overlaps.'
        d['checks']=dict(edition='ISBN matched',story='Source synopsis reviewed',characters='Featured characters only; cameos incomplete',readingOrder='Collection sequence with gaps noted',review='No verified collection score attached')
        notes[i]=d
    def seq(indices,name,series,year,ranges,positions=None):
        for p,(i,(a,b)) in enumerate(zip(indices,ranges),1):
            pos=positions[p-1] if positions else p
            notes[i]['issueKeys']=group(series,year,a,b)
            notes[i]['readingPath']=run(name,pos,'Follow this series in volume order; other collections may be needed for gaps or crossovers.')
            notes[i]['startingPoint']=pos==1
    seq([1,2,3,4],'Ultimate X-Men — original universe (2001)','Ultimate X-Men',2001,[(34,39),(40,45),(46,49),(98,100)],[7,8,9,20])
    notes[4]['issueKeys']+=group('Ultimate Fantastic Four',2004,58,60)
    notes[4]['readingPath']['note']='After Absolute Power; tie-ins to the separate Ultimatum event, not the event itself.'
    seq([5,6,7],'Uncanny X-Men — Gail Simone (2024)','Uncanny X-Men',2024,[(1,6),(17,21),(22,25)],[1,3,4])
    notes[6]['readingPath']['note']='Volume 3; issues 7–16 are outside these three indexed collections. Read the intervening material first.'
    notes[7]['issueKeys']+=group('Uncanny X-Men Annual',2026,1,1)
    seq([8,9,10,11],'Uncanny X-Men — Kieron Gillen (2011)','Uncanny X-Men',2011,[(1,4),(5,9),(11,14),(15,20)])
    notes[8]['contentsNote']='Catalog says 1–4; publisher blurb says 1–6. Only their common range 1–4 is indexed.'
    notes[9]['contentsNote']='Catalog says 5–10; publisher says 5–9. Issue 10 is excluded pending verification.'
    notes[10]['readingPath']['note']='Avengers vs. X-Men tie-in; issue 10 is unconfirmed in the preceding edition. Read with the main event.'
    notes[11]['readingPath']['note']='Concludes the Gillen series during Avengers vs. X-Men. The source year label is inconsistent; these are the 2011 relaunched series issues.'
    notes[12]['issueKeys']=group('S.W.O.R.D.',2009,1,5)+['Uncanny X-Men (1963) #534.1']+group('Uncanny X-Men',1963,535,544)+group('Uncanny X-Men',2011,1,3)
    notes[13]['issueKeys']=group('Uncanny X-Men',2011,4,20)+group('AVX: Consequences',2012,1,5)
    for i,p in [(12,1),(13,2)]: notes[i]['readingPath']=run('Uncanny X-Men — Gillen Complete Collection',p,'Larger alternative editions overlapping the smaller Gillen volumes; includes companion series.',True)
    seq([14,16,17,18,19,20,21,22,23,15],'Uncanny X-Men — Masterworks','Uncanny X-Men',1963,[(94,100),(101,110),(111,121),(122,131),(132,140),(141,150),(151,159),(161,167),(168,175),(176,188)])
    notes[14]['issueKeys']+=group('Giant-Size X-Men',1975,1,1)
    notes[15]['issueKeys']+=group('Magik',1983,1,4)
    notes[23]['issueKeys']+=group('Wolverine',1982,1,4)+['Marvel Graphic Novel (1982) #5']
    for i,a in [(18,3),(19,4),(21,5),(22,6),(23,7)]: notes[i]['issueKeys']+=group('X-Men Annual',1970,a,a)
    notes[21]['issueKeys']+=group('Avengers Annual',1967,10,10)
    notes[19]['readingPath']['note']='Dark Phoenix starts in the preceding Masterworks volume; this book begins at 132 and contains the conclusion plus aftermath.'
    notes[22]['contentsNote']='ISBN listing starts at 161 even though the blurb refers to Illyana in Limbo. Issue 160 is not confirmed and is excluded; summary focuses on confirmed later material.'
    seq([25,26,27,28,29,30],'Uncanny X-Men — Brian Michael Bendis (2013)','Uncanny X-Men',2013,[(1,5),(6,11),(16,18),(19,24),(26,31),(32,35)])
    notes[27]['issueKeys']+=['Uncanny X-Men (2013) #14','Uncanny X-Men (2013) #15.INH']
    notes[27]['readingPath']['note']='After Battle of the Atom; issues 12–13 belong to that crossover and are absent here. Includes 14, 15.INH and 16–18.'
    notes[29]['readingPath']['note']='Follows Vs. S.H.I.E.L.D., but issue 25 is absent from the confirmed ranges. Seek it before continuing Xavier’s will storyline.'
    notes[30]['issueKeys']+=group('Uncanny X-Men',2013,600,600)
    seq([37,38,24,39],'Uncanny X-Men — Cullen Bunn (2016)','Uncanny X-Men',2016,[(1,5),(6,10),(11,15),(16,19)])
    notes[37]['contentsNote']='Catalog says 1–5; publisher blurb says 1–6. Only 1–5 is indexed, and a review score is withheld.'
    notes[39]['issueKeys']+=group('Uncanny X-Men Annual',2016,1,1)
    notes[39]['readingPath']['note']='Final Bunn volume; tie-in to Inhumans vs. X-Men, whose main story is a separate collection.'
    seq([36,41,34,33,42,40,35,31,32],'Uncanny X-Men — pre-Schism collections','Uncanny X-Men',1963,[(475,486),(487,491),(500,503),(504,507),(508,512),(526,529),(530,534),(535,539),(540,544)],[475,487,500,504,508,526,530,535,540])
    for i in [36,41,34,33,42,40,35,31,32]: notes[i]['readingPath']['note']='Ordered by original issue number. Gaps require other collections; this is not a complete run.'
    notes[31]['issueKeys']+=['Uncanny X-Men (1963) #534.1']
    notes[40]['readingPath']['note']='After Second Coming. Utopia and intervening crossovers are not replaced by this collection.'
    seq([45,43,44],'Uncanny X-Men — Disassembled and Rosenberg (2018)','Uncanny X-Men',2018,[(1,10),(11,16),(17,22)])
    notes[45]['readingPath']['note']='Disassembled leads into the separate Age of X-Man books; Wolverine and Cyclops follows the remaining present-day team.'
    notes[46]['issueKeys']=group('X-Men: Blue',2017,21,22)+group('X-Men: Blue Annual',2018,1,1)+group('Venom',2016,162,163)
    notes[46]['readingPath']['note']='Poison X crossover after Venomverse; interleaves X-Men Blue and Venom rather than replacing either full run.'
    notes[47]['issueKeys']=group('War of the Realms: Uncanny X-Men',2019,1,3)
    notes[47]['readingPath']['note']='Companion to Rosenberg’s Uncanny run during War of the Realms; not the complete event.'
    notes[48]['issueKeys']=group('Original X-Men',2023,1,1)+group('Weapon X-Men',2024,1,4)
    notes[49]['issueKeys']=group('Weapon X-Men',2025,1,5)
    notes[49]['characters']=[c for c in notes[49]['characters'] if c['name']!='X-Men']
    notes[49]['characters'].append(dict(name='Weapon X-Men',role='Featured team',source=notes[49]['pagesSource']))
    notes[49]['readingPath']['note']='Separate 2025 team series, not Volume 2 of the 2024 multiverse miniseries.'
    notes[50]['issueKeys']=group('Wolverine & the X-Men',2014,1,6)
    notes[50]['readingPath']=run('Wolverine & the X-Men — Jason Latour (2014)',1,'A new volume following the earlier Jason Aaron series; not the 2011 first volume.')
    extra={2:'https://www.marvel.com/comics/issue/476/read',16:'https://collectededitions.com/tag/phoenix/',18:'https://www.marvel.com/comics/collection/39881/marvel_masterworks_the_uncanny_x-men_vol_4_trade_paperback',28:'https://images.abovethetreeline.com/ea/TW/pdfs/CATALOGMARVEL-Sept-Dec2014.pdf',29:'https://www.marvel.com/comics/collection/49839/uncanny_x-men_vol_5_the_omega_mutant_trade_paperback',50:'https://www.marvel.com/comics/issue/48899/wolverine_the_x-men_2014_4'}
    for i,url in extra.items():
        notes[i]['sources'].append(dict(label='Additional story synopsis source; not used for edition page count',url=url))
        for c in notes[i]['characters']: c['source']=url
    for i,score,count,user in [(1,6.8,14,8.2),(2,7,7,7.7),(3,6.8,9,8)]:
        url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/ultimate-x-men'; d=notes[i]
        d['review']=dict(criticScore=score,criticCount=count,userScore=user,userCount=3,url=url,checkedAt=d['checkedAt'],title=by[ids[i-1]]['title'],match='Trade title and collected issue count matched; not ISBN.',scope='Aggregate of reviewed issues in this collection; bonus material may be excluded.')
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row',url=url)); d['checks']['review']='Verified collection row'
    for i,isbn in enumerate(ids,1): editorial[by[isbn]['id']]=notes[i]; payload['books'][by[isbn]['id']]=notes[i]
    previous=json.loads((ROOT/'data/xmen-batch-02.json').read_text())[35]; key=by[previous]['id']
    editorial[key]['readingPath']['note']='Volume 10; follows The Tempest (Volume 9). Volumes 7–9 are now annotated in batch 3.'
    payload['books'][key]=editorial[key]
    write_json(path,editorial); payload['updatedAt']=datetime.date.today().isoformat()
    for directory in [ROOT/'public',ROOT/'dist/client']: write_json(directory/'enrichment.json',payload)
    report=dict(batch='xmen-03',records=50,storySynopses=50,reviewMatches=3,notes='Previous annotations preserved. Disputed issue ranges and reading gaps flagged; other review scores remain unverified.')
    write_json(ROOT/'data/xmen-batch-03-audit.json',report); print(json.dumps(report))

if __name__=='__main__': main()
