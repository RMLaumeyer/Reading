"""Ninety individually researched Spider-Man collections, September 2026."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT, write_json
from build_pilot import group, run

ROWS = """Peter's team-ups range from a Moloid battle with Red Hulk to the Omega Drive crossover with Daredevil and Punisher. Savage Land adventures, vampire hunting and a world without Spider-Man round out this broad collection.|Omega Effect; Savage Land; superhero team-ups|Red Hulk,Daredevil,Punisher,Captain America,Hawkeye,She-Hulk,Captain Marvel,Deadpool,Blade,Thing,Devil Dinosaur
Peter visits the Savage Land, confronts a mind-controlled Thing and finds a world where he never became Spider-Man. Blade joins a vampire-fighting adventure in this shorter companion collection.|Savage Land; a world without Spider-Man; vampire fights|Thing,Blade,Devil Dinosaur,Moon Boy
Ben Reilly faces a mystery connected to Ravencroft while trying to live up to the Spider-Man name. These newly written adventures revisit his first stint in the costume during the 1990s Clone Saga era.|Ben Reilly's first Spider-Man era; Ravencroft mystery|Ben Reilly
Peter's support for Tony Stark brings his private life into the superhero registration conflict. His choices and their consequences form Spider-Man's side of Civil War, rather than the entire event.|Civil War: Peter Parker's registration crisis|Iron Man
Peter's public unmasking exposes the people around him to danger. These Sensational Spider-Man chapters explore the personal fallout of Civil War alongside the main Amazing Spider-Man tie-in.|Civil War: the cost of unmasking|
Norman Osborn's supposed Spider-Man is actually Mac Gargan wearing the Venom symbiote. This dark comedy follows an impostor using a hero's public image while indulging very unheroic appetites.|Dark Reign: Mac Gargan's impostor Spider-Man|Venom,Mac Gargan,Norman Osborn
A visit to Los Angeles draws Peter into a nightmare where science and the supernatural collide. Demon Bear turns an unfamiliar neighborhood into a horror story.|Demon Bear; Los Angeles nightmare|Demon Bear
A laboratory accident strands Spider-Man, Deadpool and Hulk in another reality. Peter discovers a wildly successful counterpart, but the apparent wish fulfillment hides an ugly price.|Identity Wars: alternate-world counterparts|Deadpool,Hulk
Early encounters with Marvel's other heroes chart Spider-Man's place in the expanding 1960s universe. Team-ups and misunderstandings bring him into contact with the Avengers, Daredevil, Doctor Strange, Fantastic Four and X-Men.|1960s first meetings and team-ups|Avengers,Daredevil,Doctor Strange,Fantastic Four,X-Men
As Fear Itself spreads panic through New York, Peter tries to keep frightened people alive. Companion material broadens the crisis to the Fantastic Four and the threat of the Worthy.|Fear Itself: street-level panic; the Worthy|Fantastic Four,Thing
Peter's neighbors need help with problems that reach beyond ordinary supervillain fights. Aunt May's situation and the people in his own building make this a personal, community-focused Spider-Man story.|Secrets and Rumors: neighborhood mysteries|Aunt May
An attack linked to the Prowler threatens F.E.A.S.T., while Aunt May's work and the Rumor's past draw Peter into a larger struggle. Mary Jane and the Fantastic Four join a run built around protecting a community.|Hostile Takeovers: F.E.A.S.T. and the Rumor|Prowler,Aunt May,Mary Jane Watson,Fantastic Four,Rumor
In the altered House of M reality, Peter has fame, family and a seemingly ideal life. Secrets threaten that success in a self-contained view of a world reshaped by the event.|House of M: Peter's alternate life|
Anniversary one-shots revisit Spider-Man through short adventures and celebrations, including a fresh take on the black-costume concept. A Power Pack reunion adds a separate family-team story.|Self-Improvement; Going Big; Power Pack Grow Up|Power Pack
Teenage Peter, Miles and Gwen meet through a Daily Bugle internship and learn to work together when strange attacks threaten the city. This is an accessible alternate-continuity introduction to the three young heroes.|A New Beginning: the Spider-team forms|Miles Morales,Gwen Stacy
Black Cat's arrival brings bad luck and tension to Peter, Miles and Gwen's partnership. Their friendship matters as much as catching the new troublemaker.|Bad Luck: Black Cat tests the team|Miles Morales,Gwen Stacy,Black Cat
Miles and Gwen face an important school exam while Shocker disrupts the team's lives. The heroes must balance the pressure of their futures with an immediate supervillain problem.|Shock to the System: exams and Shocker|Miles Morales,Gwen Stacy,Shocker
Peter, Miles and Gwen juggle school and their internship while Kraven turns the young heroes into targets. Their new partnership faces a hunter who wants to control the chase.|Spider-Chase: Kraven hunts the team|Miles Morales,Gwen Stacy,Kraven the Hunter
A black-suited Spider-Man brings new trouble to the young team's city. Peter, Miles and Gwen face the arrival of Venom in this all-ages continuity.|Venom: a new black-suited threat|Miles Morales,Gwen Stacy,Venom
Lighthearted team adventures pair Spider-Man and other heroes with unusual threats, including a robotic dog and a robbery mystery. She-Hulk, Tigra, Hawkeye and more share the spotlight in these Marvel Adventures stories.|Marvel Adventures superhero team-ups|Avengers,She-Hulk,Tigra,Hawkeye,Hulk,Mysterio,Spider-Woman,Beast,Hercules
An all-ages take on Peter's early superhero career brings together six familiar enemies. Doctor Octopus, Vulture, Electro, Kraven, Sandman and Mysterio challenge a young Spider-Man, with Human Torch also appearing.|All-ages Sinister Six; early Spider-Man|Doctor Octopus,Vulture,Electro,Kraven the Hunter,Sandman,Mysterio,Human Torch
Peter returns to New York with a mysterious black costume and faces the Rose, Puma and Hobgoblin while his relationships shift. This Gallery collection reproduces the opening black-costume year with period presentation material.|Black costume year one; Rose and Puma|Black Cat,Mary Jane Watson,Hobgoblin,Puma,Fantastic Four
Gangland conflict, the Hobgoblin and the Sinister Syndicate fill this stretch of classic Amazing Spider-Man. Flash Thompson's troubles and appearances by Silver Sable and other heroes widen Peter's problems.|Sinister Syndicate; Hobgoblin; gang war|Silver Sable,Daredevil,Black Cat,Falcon,Punisher,X-Factor,Iron Man 2020,Hobgoblin
Short, playful adventures introduce younger readers to Spider-Man and fellow spider-heroes. The emphasis is on approachable team-ups and colorful problems rather than the main comics' event chronology.|Super Hero Adventures: young-reader Spider-team stories|Miles Morales,Gwen Stacy,Anya Corazon
Animated-continuity Spider-Man and Avengers stories share this collection. It is a cartoon companion, separate from both the original Ultimate comics universe and the main Avengers ongoing series.|Animated Spider-Man and Avengers adventures|Avengers
Doctor Octopus and Arnim Zola threaten the animated Spider-Man's world as Hydra puts his allies under pressure. Scarlet Spider, Doctor Strange and Miles enter a story tied to the television series.|Animated Sinister Six: Hydra and new allies|Doctor Octopus,Arnim Zola,Scarlet Spider,Doctor Strange,Miles Morales
A possible mole complicates Spider-Man's S.H.I.E.L.D. connections while familiar enemies return. Vulture, Lizard and Kraven join this continuation of the animated Sinister Six storyline.|Animated Sinister Six: a mole and returning enemies|Vulture,Agent Venom,Lizard,Kraven the Hunter
The search for Nick Fury leads the animated Spider-Man into fresh dangers involving Hydro-Man and the Inhumans' city of Attilan. This continues the television-based adventure sequence.|Animated Sinister Six: Nick Fury and Attilan|Nick Fury,Hydro-Man,Inhumans
Goblin's travel between worlds brings the animated Spider-Man into contact with other spider-heroes. This is the television version of Spider-Verse, distinct from the main comics crossover.|Animated Spider-Verse: Goblin's dimensional chase|Green Goblin
Miles's early Ultimate-universe adventures introduce his powers and responsibilities, followed by a taste of his later life in the main Marvel universe. This sampler spans two periods rather than one uninterrupted arc.|Miles Morales introduction; Blackheart|Miles Morales,Blackheart
Peter's first encounter with Cassandra Webb introduces Madame Web, followed by the classic Juggernaut struggle. Later chapters feature Julia Carpenter's prophetic role and a race against a threatened future.|Madame Web; Nothing Can Stop the Juggernaut; Tomorrow Dies Today|Madame Web,Cassandra Webb,Julia Carpenter,Juggernaut
An origin retelling, the classic Master Planner crisis and all-ages adventures offer different entry points into Spider-Man. These selections come from separate series and are not a continuous modern run.|Origin; If This Be My Destiny; all-ages adventures|
This adaptation follows the first Insomniac Spider-Man game's struggle for New York as criminal power shifts after Kingpin. Peter's personal connections intersect with Mister Negative and a widening city crisis.|Gamerverse: City at War|Kingpin,Mister Negative,Mary Jane Watson,Aunt May,Norman Osborn,Doctor Octopus,Miles Morales
Black Cat pulls the game's Peter Parker into a conflict involving the Maggia and Hammerhead. The story adapts the game's DLC-era adventures and follows the main City at War storyline.|Gamerverse: Black Cat and the Maggia|Black Cat,Hammerhead,Silver Sable,Mary Jane Watson
An original Gamerverse adventure explores Peter's Velocity suit while Mary Jane investigates a strange case with Ben Urich. Superhero action and an apparent haunting expand the game setting.|Gamerverse: Velocity suit and a haunting|Mary Jane Watson,Ben Urich,Swarm
Peter's earliest Amazing adventures introduce the responsibilities, rivalries and mistakes that shape Spider-Man. The collection pairs the opening ten issues with selected origin material.|Early Spider-Man: origin and first villains|
Miles struggles to balance everyday life with hero work as Rabble targets him personally. Misty Knight's involvement adds a mentor figure to a demanding new chapter.|Trial by Spider: Rabble's attack|Miles Morales,Rabble,Misty Knight,Scorpion
After the Carnage Reigns crossover, Miles faces Hobgoblin and the pressure of anti-vigilante forces. Hightail and the Cape Killers complicate a run already testing his endurance.|Bad Blood: Hobgoblin and Cape Killers|Miles Morales,Hobgoblin,Hightail,Blade,Bloodline
New York's gang conflict pulls Miles into battles involving Hobgoblin and uneasy allies. A separate Giant-Size chapter adds a confrontation with Dylan Brock's Venom.|Gang War: Miles's frontline; Venom clash|Miles Morales,Hobgoblin,Prowler,Ms. Marvel,Scorpion,Venom,Dylan Brock
Rabble renews her campaign against Miles as upgraded threats close in. A family responsibility involving his little sister adds a more personal counterpoint to the attacks.|Retribution: Rabble returns|Miles Morales,Rabble,Billie Morales
The vampire crisis of Blood Hunt draws Miles into a mission with Blade and leaves lasting consequences. Family ties and a trip to Puerto Rico carry the story beyond the immediate event.|Blood Hunt: Miles's transformation and aftermath|Miles Morales,Blade,Vulture
Miles travels to Wakanda seeking help with his vampiric condition. Black Panther and divine trials make this a supernatural test, while trouble with his Spider-Man identity continues back home.|Webs of Wakanda: a cure and divine trials|Miles Morales,Black Panther,Bast
After Pools of Blood, Miles becomes involved in a contest among gods. Anansi, Ares and other powerful figures turn his struggle into a mythic adventure.|God War: a contest of deities|Miles Morales,Anansi,Ares,Thor,Hercules,War-Cry
Rabble's return collides with new thieves and the influence of the Assessor. Black Cat becomes an ally as Miles deals with threats reaching beyond one familiar enemy.|Revenge of Rabble: thieves and the Assessor|Miles Morales,Rabble,Black Cat,Assessor,Inari,White Cat
Miles gains powers in the original Ultimate universe and learns how his family, especially his uncle Aaron, complicates heroism. Spider-Men then brings him face to face with another world's Peter Parker.|Miles's origin; Prowler; Spider-Men|Miles Morales,Prowler,Aaron Davis,Scorpion
Galactus's invasion leads into a new phase for Miles, including a surprising Peter Parker mystery, Green Goblin and difficult family revelations. This larger edition covers the Cataclysm-to-Revelations sequence.|Cataclysm; Revival; Revelations|Miles Morales,Galactus,Green Goblin,Doctor Doom
An offer from the Ultimates, a devastating Venom encounter and a crisis of commitment test Miles. Cloak, Dagger and Taskmaster enter the story as he considers giving up the costume.|United We Stand; Venom War; Spider-Man No More|Miles Morales,Ultimates,Venom,Cloak,Dagger,Taskmaster
Deadpool and his daughter Ellie take an assignment that puts Miles in their sights. This crossover interrupts Miles's regular volume sequence between Webs of Wakanda and God War.|Pools of Blood: Deadpool versus Miles|Miles Morales,Deadpool,Ellie Camacho
Miles faces Galactus's invasion and then a new set of personal shocks involving Peter Parker, Green Goblin and his own father. This complete collection overlaps the later Revivals and Revelations Epic edition.|Cataclysm; Revival; Revelations|Miles Morales,Galactus,Green Goblin,Doctor Doom
The Ultimate Spider-Man legacy is revisited before Miles confronts a mystery involving Peter Parker's apparent return. This opens the 2014 series after Cataclysm.|Revival: Peter Parker's return mystery|Miles Morales,Green Goblin
Miles's relationships become tangled with secrets about his father and girlfriend Katie Bishop. S.H.I.E.L.D. connections and the Human Flies push the 2014 run toward its conclusion.|Revelations: family secrets and Katie Bishop|Miles Morales,Katie Bishop
A mystery at Empire State University sends Peter into a fast-moving international adventure. The story's escalating physical danger leads into the later Savage Spider-Man miniseries.|Non-Stop Spider-Man: campus mystery and global chase|
Norman Osborn attacks Peter through the people he cares about. This focused Green Goblin story closes the Paul Jenkins stretch represented by these Peter Parker: Spider-Man chapters.|A Death in the Family: Green Goblin's attack|Green Goblin,Norman Osborn
A dangerous Predator called Skinner reaches New York during a heat wave and blackout. Spider-Man becomes part of an urban hunt in this standalone crossover continuity.|Predator versus Spider-Man: Skinner's hunt|Predator,Skinner
Following Non-Stop Spider-Man, Peter's transformation into a spider-creature strands him in a brutal jungle conflict. Baron Zemo and the Immaculatum turn the adventure toward body horror.|Savage Spider-Man: monstrous transformation|Baron Zemo,Immaculatum
The Skrull invasion reaches New York while Jackpot and other supporting figures face the danger around Spider-Man's world. This is a Secret Invasion companion, not the event's central story.|Secret Invasion: New York and Jackpot|Jackpot,Skrulls
Curt Connors's struggle with the Lizard turns dangerous while Morbius adds another kind of monster to Peter's problems. These chapters precede the Queen storyline in Disassembled.|Here There Be Monsters: Lizard and Morbius|Lizard,Curt Connors,Morbius
The Queen threatens Peter with a disturbing transformation, and Captain America becomes involved in the crisis. These Spider-Man chapters accompany the Avengers Disassembled period.|Disassembled: the Queen's transformation plot|Queen,Captain America
The 1990s animated Spider-Man returns in a continuation featuring Peter and Mary Jane, with Kaine and Morlun entering that show's world. This is a sequel to the cartoon rather than a 1994 comic reprint.|Spider-Man '94: continuation of the animated series|Mary Jane Watson,Kaine,Morlun
The original Secret Wars is revisited through an approachable Spider-Man-centered adventure. Battleworld and the heroes' struggle against overwhelming odds provide the setting.|Original Secret Wars retelling; Battleworld|Hulk
Spider-Man and Venom share an unruly, comedic adventure that includes a body swap. The playful presentation makes this a separate entry from the darker symbiote event books.|Double Trouble: Spider-Man and Venom body swap|Venom
Peter and Wolverine follow a shared mystery into a globe-spanning adventure, including the Savage Land. The Janus Directory and Dreadshadow connect the enemies targeting them.|The Janus Directory: Spider-Man and Wolverine team-up|Wolverine,Dreadshadow
The team-up continues with the Shadow Coven and Arachnix raising the stakes around Dreadshadow. Read after The Janus Directory for the ongoing conflict and choices facing the two heroes.|Life, Death and Other Choices: Shadow Coven|Wolverine,Dreadshadow,Arachnix
Miguel O'Hara's future-born Spider-Man operates in the present day. This opens Peter David's revived 2099 sequence, establishing the situation before its Spider-Verse crossover chapters.|Out of Time: Miguel in the present|Spider-Man 2099,Miguel O'Hara
Spider-Verse pulls Miguel into a multiversal struggle involving Lady Spider and the Inheritors. The volume continues beyond that crisis toward an encounter with Maestro.|Spider-Verse; Lady Spider; Maestro|Spider-Man 2099,Miguel O'Hara,Lady Spider,Daemos,Morlun,Maestro
Miguel tries to build a life around Parker Industries, but new danger disrupts any hope of leaving hero work behind. This is the opening of the 2015 relaunch despite being labeled Volume 3.|Smack to the Future: a new start disrupted|Spider-Man 2099,Miguel O'Hara
F.I.S.T. and its connections draw Miguel deeper into a conspiracy involving future technology and present threats. Alchemax and Lash complicate his effort to protect the timeline.|Gods and Women: F.I.S.T. and Alchemax|Spider-Man 2099,Miguel O'Hara,Lash
An altered 2099 and its superhero conflict bring Miguel into contact with Roberta Mendez and a future Sinister Six. This is his series' Civil War II-era storyline, not the main event miniseries.|Civil War II: an altered 2099|Spider-Man 2099,Miguel O'Hara,Roberta Mendez,Sinister Six 2099
Miguel's pursuit of F.I.S.T. connects with Elektra, the Hand and an ancient threat. The run moves toward its final attempt to repair the future.|Apocalypse Soon: F.I.S.T. and the Hand|Spider-Man 2099,Miguel O'Hara,Elektra,Hand
Miguel and Sonny Frisco confront the consequences of the damaged future as the modern run concludes. A reprinted 1990s meeting between the two Spider-Men adds a separate earlier adventure.|Back to the Future, Shock: fixing 2099|Spider-Man 2099,Miguel O'Hara,Sonny Frisco,Electro
The original 1990s Spider-Man 2099 faces Venom 2099 and the upheaval surrounding Doom and Tyler Stone. The collection also includes a time-crossing meeting with Peter Parker.|Original 2099: Venom and a Spider-Man meeting|Spider-Man 2099,Miguel O'Hara,Venom 2099,Doctor Doom,Tyler Stone
Carnage 2099 drives a crisis that brings together an expanded future cast. Miguel joins new versions of familiar heroes in a bloody adventure following Exodus.|Dark Genesis: Carnage 2099|Spider-Man 2099,Miguel O'Hara,Carnage 2099,Blade 2099,Punisher 2099,Daredevil 2099,Moon Knight 2099,Spider-Woman 2099,Ghost Rider 2099
A new Garden of Eden and the Cabal's ambitions draw Miguel across the future Marvel landscape. Winter Soldier 13, Loki 2099 and future teams broaden this tour of 2099.|Exodus: Garden of Eden and the Cabal|Spider-Man 2099,Miguel O'Hara,Winter Soldier 13,Loki 2099
Miguel encounters the horror side of 2099 through future vampires, monsters and supernatural heroes. These are future versions of familiar characters, not assumed appearances by their present-day counterparts.|2099 horror: vampires, monsters and supernatural threats|Spider-Man 2099,Miguel O'Hara,Blade 2099,Moon Knight 2099,Dracula 2099,Werewolf 2099,Man-Thing 2099
Someone who knows Peter's identity kidnaps Aunt May, forcing him through a dangerous network of villains. Mark Millar's complete Marvel Knights arc turns his personal life into the pressure point.|Down Among the Dead Men; Venomous; The Last Stand|Aunt May,Mary Jane Watson
Todd McFarlane's Spider-Man run moves from the Lizard's Torment to encounters with Ghost Rider, Wolverine and Morbius. The X-Force crossover adds a Juggernaut battle to this artist-led collection.|Torment; Masques; Perceptions; Sub-City; Sabotage|Lizard,Ghost Rider,Hobgoblin,Wolverine,Wendigo,Morbius,X-Force,Juggernaut
Tom Taylor's full neighborhood-focused run follows Peter helping the people around him while Aunt May and F.E.A.S.T. face serious challenges. The Rumor, Mary Jane, Miles and Fantastic Four connect intimate stories with superhero action.|Secrets and Rumors; Hostile Takeovers|Aunt May,Rumor,Mary Jane Watson,Miles Morales,Fantastic Four,Prowler
Mary Jane's school life, friendships and crush on Spider-Man take center stage in this alternate high-school romance. Peter's secret identity complicates a story told largely from outside the costume.|Super Crush: Mary Jane's high-school romance|Mary Jane Watson
Gwen Stacy's arrival changes the social balance around Mary Jane and Peter. Romantic uncertainty and friendship carry this continuation of the high-school series.|The New Girl: Gwen joins the cast|Mary Jane Watson,Gwen Stacy
Peter's superhero responsibilities and the teenagers' private feelings make relationships harder to navigate. This middle stretch continues the romance and identity tensions of the same school setting.|My Secret Life: romance and hidden identities|Mary Jane Watson
The first twenty-issue romance series reaches its closing stretch as friendships and relationships are tested. Mary Jane and Peter must deal with feelings that are harder to manage than a simple crush.|Still Friends: relationship crossroads|Mary Jane Watson
Depression-era Spider-Man Noir confronts crime and brutality in his origin and Eyes Without a Face sequel. Later multiverse material adds short appearances to the two central noir mysteries.|Spider-Man Noir origin; Eyes Without a Face|Spider-Man Noir
A 1930s Peter Parker faces a corrupt city dominated by the Goblin. This alternate-world origin trades the usual bright superhero setting for a Depression-era crime story.|Spider-Man Noir: Depression-era origin|Spider-Man Noir,Green Goblin
Private investigator Peter Parker takes a case involving Gwen Stacy and her father George. Hardboil and Plasma-Man enter a new Spider-Man Noir mystery.|The Gwen Stacy Affair: Noir detective case|Spider-Man Noir,Gwen Stacy,George Stacy,Hardboil,Plasma-Man
A murder connected with the Black Cat nightclub leads Noir into a 1939 adventure across Europe. The investigation opens onto Nazi threats and ancient evil.|Twilight in Babylon: Noir's European mystery|Spider-Man Noir,Black Cat
Shathra threatens the spider-heroes across the multiverse, forcing Peter into another Spider-Verse crisis. Morlun's role adds complications to a conflict centered on the web connecting these worlds.|End of the Spider-Verse: Shathra's attack|Shathra,Morlun
Spider-Boy's arrival raises questions about Peter's forgotten connections while new powers create their own complications. This follows End of the Spider-Verse in the 2022 Spider-Man series.|Who Is Spider-Boy?; Peter's changing powers|Spider-Boy,Electro,Norman Osborn
Black Cat's debut and early returns establish her changing relationship with Spider-Man. Three classic pairs of issues chart the beginning of the rivalry and attraction.|Black Cat's debut and early encounters|Black Cat,Felicia Hardy
The mystery of a new Green Goblin intersects with an underworld struggle. These late-1970s chapters form a focused slice of classic Amazing Spider-Man.|The New Goblin: identity mystery and gangland conflict|Green Goblin,Silvermane
Eddie Brock attempts a different kind of mission as Anti-Venom, crossing paths with Punisher during Dark Reign. This is an Eddie-focused redemption story rather than a Peter Parker solo adventure.|New Ways to Live: Anti-Venom and Punisher|Anti-Venom,Eddie Brock,Punisher"""

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/deep-batch-07.json').read_text());rows=ROWS.splitlines();assert len(ids)==len(rows)==90
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books'];by={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'));before=copy.deepcopy(payload['books'])
    path=ROOT/'data/editorial-enrichment.json';editorial=json.loads(path.read_text(encoding='utf-8'));notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        b=by[isbn];d=copy.deepcopy(before.get(b['id'],{}));source=d.get('pagesSource') or b['catalogUrl'];summary,story,guests=row.split('|')
        for key in ['level','automation','review']:d.pop(key,None)
        d.update(summary=summary,pages=d.get('pages'),pagesSource=source,coverSource=d.get('coverSource',source),checkedAt=datetime.date.today().isoformat(),editorialBatch='deep-07',stories=[dict(title=story,coverage='Story highlights; see edition and reading notes')],characters=[dict(name=n,role='Featured in cited synopsis; not a complete cameo index',source=source) for n in dict.fromkeys(['Spider-Man']+[g.strip() for g in guests.split(',') if g.strip()])],issueKeys=[],startingPoint=False)
        d['sources']=[dict(label='ISBN metadata / publisher synopsis' if d.get('pages') else 'OCLS · imported edition record',url=source)]
        d['readingPath']=run('Spider-Man — '+story,1,'Separate collection. No universal chronology is implied.')
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
    report=dict(batch='deep-07',records=90,reviews=sum(bool(d.get('review')) for d in notes.values()),missingPages=sum(not d.get('pages') for d in notes.values()),remainingXMen=sum('x-men' in b['title'].lower() and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog),notes='90 researched records; previous work preserved. Edition uncertainties and missing ratings remain explicit.')
    report['xMenRecords']=0;report['spiderManRecords']=90
    report['remainingSpiderMan']=sum(any(t in b['title'].lower() for t in ['spider-man','spiderman']) and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog)
    write_json(ROOT/'data/deep-batch-07-audit.json',report);print(json.dumps(report))

def configure(n,by,ids,before):
    def issues(i,*ranges):
        n[i]['issueKeys']=[key for args in ranges for key in group(*args)]
    def path(i,name,pos,note='',alt=False):n[i]['readingPath']=run(name,pos,note,alt)
    def note(i,text):n[i]['readingPath']['note']+=' '+text
    def cite(i,url,label='Additional edition / story evidence'):
        n[i]['sources'].append(dict(label=label,url=url))
    def caution(i,text):
        n[i]['checks']['edition']=text;n[i]['contentsNote']+=' '+text
    def seq(indices,name,series,year,ranges):
        for pos,(i,(a,b)) in enumerate(zip(indices,ranges),1):
            issues(i,(series,year,a,b));path(i,name,pos,'Read within this series and continuity; numbering follows the collected chapters.')
    for i in [6,90]:
        n[i]['characters'][0]['role']='Spider-Man-related title; the lead is '+('Mac Gargan as an impostor Spider-Man, not Peter Parker' if i==6 else 'Eddie Brock as Anti-Venom')
    issues(1,('Avenging Spider-Man',2011,1,15),('Avenging Spider-Man Annual',2012,1,1),('Punisher',2011,10,10),('Daredevil',2011,11,11),('Amazing Spider-Man Annual',1964,39,39),('Spider-Man vs. Vampires',2010,1,1))
    issues(2,('Avenging Spider-Man',2011,14,15),('Avenging Spider-Man Annual',2012,1,1),('Amazing Spider-Man Annual',1964,39,39),('Spider-Man vs. Vampires',2010,1,1))
    cite(2,'https://www.marvel.com/comics/collection/42948/avenging_spider-man_threats_menaces')
    cite(2,'https://books.apple.com/ca/book/avenging-spider-man/id949852694','Marvel publisher copy · collected contents')
    for c in n[2]['characters']:c['source']=n[2]['sources'][1]['url']
    for i,pos in [(1,1),(2,14)]:path(i,'Avenging Spider-Man (2011)',pos,'Complete collection and smaller Threats & Menaces overlap. Material from Amazing 692 is partial and not indexed as a whole issue.',True)
    n[1]['startingPoint']=True
    issues(3,('Ben Reilly: Spider-Man',2022,1,5));note(3,'Retrospective 1990s setting, not a sequel to Beyond or Dark Web.')
    issues(4,('Amazing Spider-Man',1999,532,538));issues(5,('Sensational Spider-Man',2006,28,34))
    cite(4,'https://yvl.overdrive.com/library/comics/media/5902039','ISBN-matched publisher copy · Civil War 532–538')
    caution(4,'Imported synopsis says 532–536; the catalog and ISBN-matched library publisher copy list 532–538. Conflicting length metadata is withheld.');n[4]['pages']=None
    for i in [4,5]:path(i,'Spider-Man — Civil War companions',1,'Parallel tie-ins to Civil War (2006); read with the main event rather than treating these two titles as consecutive volumes.',True)
    issues(6,('Dark Reign: Sinister Spider-Man',2009,1,4),('Amazing Spider-Man Family',2008,8,8));note(6,'Dark Avengers-era Mac Gargan story. Spider-Man branding does not identify Peter as the lead.')
    issues(7,('Deadly Neighborhood Spider-Man',2022,1,5));n[7]['startingPoint']=True
    issues(8,('Amazing Spider-Man Annual',1964,38,38),('Deadpool Annual',2011,1,1),('Incredible Hulks Annual',2011,1,1));n[8]['startingPoint']=True
    issues(9,('Amazing Spider-Man',1963,16,16),('Amazing Spider-Man Annual',1964,2,3),('Strange Tales Annual',1962,2,2),('Avengers',1963,11,11),('Daredevil',1964,16,17),('Daredevil',1964,27,27),('Uncanny X-Men',1963,35,35),('Fantastic Four',1961,73,73));note(9,'Themed sampler, not a continuous arc. Other listed excerpts are partial and excluded from whole-issue overlap matching.')
    issues(10,('Fear Itself: Spider-Man',2011,1,3),('Fear Itself: FF',2011,1,1),('Fear Itself: The Worthy',2011,1,1));note(10,'Companion to Fear Itself; the main event is separate.')
    seq([11,12],'Friendly Neighborhood Spider-Man — Tom Taylor (2019)','Friendly Neighborhood Spider-Man',2019,[(1,5),(7,14)])
    caution(11,'Catalog says 1–6 but cached publisher copy says 1–5. Only uncontested 1–5 indexed; issue 6, length and review score withheld pending contents verification.');n[11]['pages']=None
    caution(12,'Imported title has malformed issue range 2–14; publisher synopsis confirms 7–14.');note(12,'The earlier volume has a disputed issue 6 listing. The complete collection explicitly contains 1–14.')
    issues(13,('Spider-Man: House of M',2005,1,5));note(13,'Alternate House of M reality; read alongside that event, not as Peter’s main-universe biography.')
    issues(14,('Sensational Spider-Man: Self-Improvement',2019,1,1),('Amazing Spider-Man: Going Big',2019,1,1),('Power Pack: Grow Up',2019,1,1));note(14,'Anniversary anthology; its one-shots do not form a numbered ongoing arc.')
    seq([15,18,16,19],'Marvel Action: Spider-Man — young Peter, Miles and Gwen','Marvel Action Spider-Man',2018,[(1,3),(4,6),(7,9),(10,12)])
    issues(17,('Marvel Action Spider-Man',2020,1,3));path(17,'Marvel Action: Spider-Man — young Peter, Miles and Gwen',5,'Fifth collected book, but the underlying comic restarts numbering in 2020. Separate from main Marvel continuity.')
    for i in [15,16,17,18,19]:
        cite(i,'https://www.comics.org/series/147896/','Grand Comics Database · collection mapping');note(i,'All-ages alternate continuity with teenage Peter, Miles and Gwen as peers.')
    cite(15,'https://goodcomicsforkids.slj.com/2019/07/09/review-marvel-action-spider-man-a-new-beginning/','School Library Journal · collection review and story context')
    cite(16,'https://marvel.fandom.com/wiki/Marvel_Action%3A_Spider-Man_TPB_Vol_1_3%3A_Bad_Luck','Reproduced publisher synopsis')
    cite(18,'https://marvel.fandom.com/wiki/Marvel_Action%3A_Spider-Man_TPB_Vol_1_2%3A_Spider-Chase','Reproduced publisher synopsis')
    cite(17,'https://www.marvel.com/comics/collection/93746/','Marvel · Shock to the System synopsis and contents')
    cite(19,'https://prhinternationalsales.com/wp-content/uploads/2020/06/GN-Manga-June-2020.pdf','Publisher distributor catalog · Marvel Action Venom')
    for i in [15,16,17,18,19]:
        for c in n[i]['characters']:c['source']=n[i]['sources'][-1]['url']
    n[15]['startingPoint']=True
    issues(20,('Marvel Adventures Super Heroes',2008,13,16));note(20,'Different all-ages series from the Avengers main universe and television adaptations.')
    issues(21,('Marvel Adventures Spider-Man',2005,1,4));n[21]['startingPoint']=True
    issues(22,('Amazing Spider-Man',1963,252,263));path(22,'Amazing Spider-Man — classic era collections',252,'Gallery/facsimile presentation of the black-costume year; overlaps ordinary collections of these issues.',True)
    issues(23,('Amazing Spider-Man',1963,279,288));path(23,'Amazing Spider-Man — classic era collections',279,'Masterworks edition of this classic stretch; overlapping Epic editions are alternatives.',True)
    caution(24,'Four named Super Hero Adventures one-shots are listed, but their exact series/year keys are not independently resolved; no speculative issue keys added.');n[24]['startingPoint']=True
    issues(25,('Marvel Universe Ultimate Spider-Man',2012,29,31),('Marvel Universe Avengers Assemble',2013,13,13));note(25,'Television continuity, not the Brian Michael Bendis Ultimate comics. Plot detail remains limited because the cached source provides contents only.')
    seq([26,27,28],'Marvel Universe Ultimate Spider-Man vs. the Sinister Six — animated','Marvel Universe Ultimate Spider-Man vs. the Sinister Six',2016,[(1,4),(5,8),(9,12)])
    caution(28,'Title says 9–11; publisher synopsis says 9–12. Only uncontested 9–11 indexed until the edition contents are confirmed.');n[28]['issueKeys']=group('Marvel Universe Ultimate Spider-Man vs. the Sinister Six',2016,9,11);n[28]['pages']=None
    cite(29,'https://www.marvel.com/comics/collection/57008/marvel_universe_ultimate_spider-man_spider-verse_trade_paperback')
    caution(29,'Catalog says 1–4; Marvel publisher listing says 13–16 under an ambiguous Spider-Verse series label. Issue keys and length withheld to avoid matching the wrong Spider-Verse series.');n[29]['pages']=None;note(29,'Animated adaptation; not the 2014 main-comics event or Edge of Spider-Verse anthology.')
    issues(30,('Ultimate Comics Spider-Man',2011,1,2),('Ultimate Comics Spider-Man',2011,5,5),('Spider-Man',2016,1,2));note(30,'Sampler crosses the original Ultimate and later main-universe eras. It skips early chapters; choose Hero in Training for a longer origin sequence.')
    issues(31,('Amazing Spider-Man',1963,210,210),('Amazing Spider-Man',1963,229,230),('Amazing Spider-Man',1999,678,679));note(31,'Selected Madame Web stories spanning decades, not a single continuous arc.')
    issues(32,('Mythos: Spider-Man',2007,1,1),('Amazing Spider-Man',1963,32,33),('Marvel Adventures Spider-Man',2005,2,3));n[32]['startingPoint']=True
    for i,series,pos in [(33,'Marvel’s Spider-Man: City at War',1),(35,'Marvel’s Spider-Man: Velocity',2),(34,'Marvel’s Spider-Man: The Black Cat Strikes',3)]:
        issues(i,(series,2020 if i==34 else 2019,1,5 if i!=33 else 6));path(i,'Marvel’s Spider-Man — Insomniac Gamerverse',pos,'Game continuity. Suggested sequence: main-game adaptation, original Velocity adventure, then DLC adaptation. Not a claim about every mission’s chronology.')
    n[33]['startingPoint']=True
    issues(36,('Amazing Spider-Man',1963,1,10));path(36,'Amazing Spider-Man — classic era collections',1,'Alternative early-issue edition. Only partial Amazing Fantasy 15 is listed, so it is not indexed as a complete issue.',True);n[36]['startingPoint']=True
    seq(list(range(37,45)),'Miles Morales — Cody Ziglar (2022)','Miles Morales: Spider-Man',2022,[(1,5),(8,12),(13,16),(17,20),(21,24),(27,29),(32,36),(37,42)])
    n[39]['issueKeys']+=group('Giant-Size Spider-Man',2024,1,1)
    n[41]['issueKeys']+=group('Miles Morales: Spider-Man',2022,26,26)
    n[37]['startingPoint']=True
    note(37,'Issues 6–7 are in Carnage Reigns between this book and Bad Blood.');note(38,'Read Carnage Reigns for intervening 6–7; the jump is intentional, not missing numbering in this volume.')
    note(39,'Miles’s Gang War chapters plus the Giant-Size Venom encounter; other heroes’ Gang War books are separate.')
    note(40,'Partial Web of Spider-Man (2024) material is not a whole-issue overlap.')
    for i in [41,42]:note(i,'Publisher lists selected material from issue 25 and the 2024 annual. Neither is indexed as a whole issue; partial-content overlap is not quantified.')
    note(41,'Blood Hunt’s main miniseries remains separate. Miles 21–22 also overlap the Amazing Spider-Man: Blood Hunt companion.')
    note(42,'Read Pools of Blood for Miles 30–31 before God War.');note(43,'Follows the Pools of Blood crossover, not directly issue 29.')
    issues(45,('Ultimate Comics Spider-Man',2011,1,12),('Spider-Men',2012,1,5));path(45,'Miles Morales — original Ultimate universe',1,'Origin and Spider-Men crossover; partial Ultimate Fallout 4 omitted from whole-issue indexing.',True);n[45]['startingPoint']=True
    for i in [46,49]:
        issues(i,('Cataclysm: Ultimate Spider-Man',2013,1,3),('Ultimate Spider-Man',2014,200,200),('Miles Morales: Ultimate Spider-Man',2014,1,12));path(i,'Miles Morales — original Ultimate universe',3,'Alternative larger editions covering Cataclysm, Revival and Revelations. Choose one; both share the sixteen core issues.',True)
    issues(47,('Ultimate Comics Spider-Man',2011,13,28));n[47]['issueKeys']+=['Ultimate Comics Spider-Man (2011) #16.1'];path(47,'Miles Morales — original Ultimate universe',2,'After Hero in Training and before Cataclysm / Revivals and Revelations.',True)
    issues(48,('Miles Morales: Spider-Man',2022,30,31),('Deadpool',2024,11,12));path(48,'Miles Morales — Cody Ziglar (2022)',6.5,'Crossover between Webs of Wakanda and God War. Selected annual material is not indexed as a whole annual.')
    issues(50,('Ultimate Spider-Man',2014,200,200),('Miles Morales: Ultimate Spider-Man',2014,1,5));issues(51,('Miles Morales: Ultimate Spider-Man',2014,6,12))
    path(50,'Miles Morales — original Ultimate universe',3.1,'Smaller Revival volume after Cataclysm; overlaps both larger complete/Epic collections.',True);path(51,'Miles Morales — original Ultimate universe',3.2,'After Revival; overlaps both larger complete/Epic collections. Later main-universe Miles stories belong to a different era.',True)
    issues(52,('Non-Stop Spider-Man',2021,1,5));issues(55,('Savage Spider-Man',2022,1,5))
    path(52,'Spider-Man — Joe Kelly and Chris Bachalo',1,'Read Non-Stop before Savage Spider-Man.');path(55,'Spider-Man — Joe Kelly and Chris Bachalo',2,'Direct follow-up to Non-Stop Spider-Man.');n[52]['startingPoint']=True
    issues(53,('Peter Parker: Spider-Man',1999,44,47));note(53,'Later Paul Jenkins-era story; not the 1970s New Goblin arc.')
    issues(54,('Predator vs. Spider-Man',2025,1,4));n[54]['startingPoint']=True;note(54,'Standalone Predator crossover, separate from regular Amazing continuity.')
    issues(56,('Secret Invasion: The Amazing Spider-Man',2008,1,3));caution(56,'Imported bonus number 35 is ambiguous; the main three issues are indexed, but the annual alias is withheld until edition confirmation.');note(56,'Supporting-cast Secret Invasion story. Spider-Man’s name on the cover does not mean he leads every chapter.')
    seq([57,58],'Spectacular Spider-Man — Paul Jenkins (2003)','Spectacular Spider-Man',2003,[(11,14),(15,20)])
    note(58,'Spider-Man tie-in to the Disassembled period; does not contain the main Avengers story.')
    issues(59,("Spider-Man '94",2025,1,5));note(59,'Sequel to the 1990s animated show. The publication year is 2025 despite the 94 in the title.')
    issues(60,('Spider-Man & the Secret Wars',2009,1,4));note(60,'Retelling of the original 1984 Battleworld event; not the 2015 Secret Wars crossover.');n[60]['startingPoint']=True
    issues(61,('Spider-Man & Venom: Double Trouble',2019,1,4));n[61]['startingPoint']=True
    seq([62,63],'Spider-Man & Wolverine (2025)','Spider-Man & Wolverine',2025,[(1,5),(6,10)])
    seq([64,65],'Spider-Man 2099 — Peter David modern return','Spider-Man 2099',2014,[(1,5),(6,12)])
    for pos,(i,(a,b)) in enumerate(zip(range(66,71),[(1,5),(6,10),(11,16),(17,21),(22,25)]),3):
        issues(i,('Spider-Man 2099',2015,a,b));path(i,'Spider-Man 2099 — Peter David modern return',pos,'The 2015 relaunch restarts issue numbering; collected volume numbering continues from the 2014 run.')
    note(65,'Spider-Verse tie-in chapters; the main event is separate.');n[64]['startingPoint']=True
    n[70]['issueKeys']+=group('Spider-Man 2099 Meets Spider-Man',1995,1,1);note(70,'The 1995 bonus one-shot also appears in the original-era Venom 2099 collection.')
    issues(71,('Spider-Man 2099',1992,34,38),('Spider-Man 2099 Special',1995,1,1),('Spider-Man 2099 Meets Spider-Man',1995,1,1));path(71,'Spider-Man 2099 — original 1992 series',34,'Original 1990s run, not the 2014/2015 relaunch. Partial 2099 Unlimited material is excluded.')
    issues(72,('Spider-Man 2099: Dark Genesis',2023,1,5));issues(73,('Spider-Man 2099: Exodus Alpha',2022,1,1),('Spider-Man 2099: Exodus',2022,1,5),('Spider-Man 2099: Exodus Omega',2022,1,1));issues(74,('Miguel O’Hara: Spider-Man 2099',2024,1,5))
    for pos,i in enumerate([73,72,74],1):path(i,'Spider-Man 2099 — Steve Orlando future adventures',pos,'Suggested sequence: Exodus, Dark Genesis, then Miguel O’Hara. Separate from the Peter David volume numbering.')
    for i in [72,73,74]:note(i,'Future variants have distinct character tags; Moon Knight 2099 is not assumed to be Marc Spector, for example.')
    issues(75,('Marvel Knights Spider-Man',2004,1,12));n[75]['startingPoint']=True;note(75,'Complete Mark Millar arc; Ultimate Collection is an edition label, not the Ultimate universe.')
    issues(76,('Spider-Man',1990,1,14),('Spider-Man',1990,16,16),('X-Force',1991,4,4));note(76,'Creator collection intentionally skips Spider-Man 15. Sabotage crosses into X-Force 4; the missing number is not silently filled.')
    issues(77,('Friendly Neighborhood Spider-Man',2019,1,14));path(77,'Friendly Neighborhood Spider-Man — Tom Taylor (2019)',1,'Complete alternative to the smaller Secrets and Rumors / Hostile Takeovers volumes; includes the disputed issue 6. Partial FCBD material excluded.',True);n[77]['startingPoint']=True
    seq([78,79,80,81],'Spider-Man Loves Mary Jane — Sean McKeever (2005)','Spider-Man Loves Mary Jane',2005,[(1,5),(6,10),(11,15),(16,20)])
    for i in [78,79,80,81]:
        cite(i,'https://www.marvel.com/comics/series/969/spider-man_loves_mary_jane_%282005_-_2007%29','Marvel · original series identity');note(i,'Alternate high-school romance continuity. The earlier Mary Jane and Mary Jane: Homecoming miniseries provide optional background; the later 2008 series is separate.')
    n[78]['startingPoint']=True
    issues(82,('Spider-Man Noir',2008,1,4),('Spider-Man Noir: Eyes Without a Face',2009,1,4),('Edge of Spider-Verse',2014,1,1));note(82,'Larger alternative containing the original miniseries and its sequel plus multiverse extras. Video-comic and partial Team-Up material are not indexed.')
    cite(82,'https://www.marvel.com/comics/series/8304/spider-man_noir%3A_eyes_without_a_face_%282009_-_2010%29','Marvel · Eyes Without a Face series identity')
    issues(83,('Spider-Man Noir',2008,1,4));issues(84,('Spider-Man Noir',2025,1,5));issues(85,('Spider-Man Noir',2020,1,5))
    for i,pos in [(82,1),(83,1),(85,3),(84,4)]:path(i,'Spider-Man Noir — collection sequence',pos,'Publication sequence of separate Noir adventures; historical settings are not publication dates. Hard-Boiled Origins includes the first story plus Eyes Without a Face.',i in [82,83])
    n[82]['startingPoint']=True;n[83]['startingPoint']=True
    seq([86,87],'Spider-Man — Dan Slott (2022)','Spider-Man',2022,[(1,7),(8,11)]);note(86,'Separate Spider-Man ongoing alongside Amazing; familiarity with earlier Spider-Verse helps.')
    issues(88,('Amazing Spider-Man',1963,194,195),('Amazing Spider-Man',1963,204,205),('Amazing Spider-Man',1963,226,227));path(88,'Amazing Spider-Man — classic era collections',194,'Black Cat-themed selections with gaps, not a complete issue sequence.',True)
    issues(89,('Amazing Spider-Man',1963,176,180));path(89,'Amazing Spider-Man — classic era collections',176,'The 1970s Goblin mystery; overlaps broader Epic editions of this period.',True)
    issues(90,('Amazing Spider-Man Presents: Anti-Venom - New Ways to Live',2009,1,3));note(90,'Eddie Brock and Punisher story during Dark Reign; partial Amazing Spider-Man Extra 2 is not a whole issue.')
    for i in n:n[i]['issueKeys']=list(dict.fromkeys(n[i]['issueKeys']))
    reviews(n,by,ids)

def reviews(n,by,ids):
    scores=[]
    def add(slug,rows):
        for row in rows:scores.append((slug,*row))
    add('friendly-neighborhood-spider-man-(2019)',[(12,8.1,42,9.5,2),(77,8.4,105,None,None)])
    add('spider-man-2099-(2014)',[(64,7,54,7,4),(65,7.5,32,7.1,4)])
    add('spider-man-2099-(2015)',[(66,7.7,28,8,1),(67,7.1,7,7.5,1),(68,7.1,14,7,1),(69,6.5,7,6,1)])
    add('miles-morales-ultimate-spider-man',[(49,8.1,154,8.2,3),(50,8.4,84,7.9,8),(51,8.1,53,7.8,8)])
    add('miles-morales-spider-man-(2023)',[(37,9.1,28,6.5,2),(38,7.6,16,6.5,2),(39,8.5,22,7.2,2),(40,9,11,7.5,1),(43,9.3,8,6,1),(44,9,7,None,None)])
    add('spider-man-(2022)',[(86,7.4,47,8.2,5),(87,7.7,24,7.5,1)])
    add('spider-man-noir-(2020)',[(85,7.2,20,5,1)])
    add('ben-reilly-spider-man-(2022)',[(3,8.3,26,6.5,1)])
    add('deadly-neighborhood-spider-man-(2022)',[(7,7,16,9,1)])
    add('non-stop-spider-man-(2021)',[(52,7.7,31,None,None)])
    add('savage-spider-man-(2022)',[(55,5.2,11,6,1)])
    for slug,i,critic,count,user,ucount in scores:
        d=n[i];url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
        d['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=ucount,url=url,checkedAt=d['checkedAt'],title=by[ids[i-1]]['title'],match='Trade row matched by series, volume/story and collected issue count; not ISBN.',scope='Aggregate for the reviewed issues in the matching collection; bonus stories and partial material may be excluded.')
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row',url=url));d['checks']['review']='Matching collection row checked'
    for i in [11,41,42,46,48,70]:n[i]['checks']['review']='Withheld: edition title, issue count or bonus material does not securely match the review row'

if __name__=='__main__':main()

