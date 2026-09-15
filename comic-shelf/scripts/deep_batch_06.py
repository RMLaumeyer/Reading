"""One hundred individually researched X-Men collections, September 2026."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT, write_json
from build_pilot import group, run

ROWS='''Scott and Jean raise the future Cable in a world dominated by Apocalypse. Companion Askani stories expand the Summers family's future history rather than continuing their Victorian encounter with Sinister.|The Adventures of Cyclops and Phoenix / Askani family stories|Cyclops, Jean Grey, Cable
The animated team's opening adventures pit Xavier's students against Sentinels, Magneto and other familiar enemies. Encounters with the Morlocks and Cable bring the television show's early conflicts to comics.|Animated Series: early adaptations|Cyclops, Jean Grey, Storm, Wolverine, Rogue, Gambit, Beast, Jubilee, Morph, Professor X, Magneto, Cable
Animated-style adventures take Wolverine against the Hulk and bring Spider-Man into Beast and Gambit's fight with Sinister. Rival guilds, Apocalypse and cosmic powers expand the team's world beyond the classroom.|Adventures of the X-Men / animated-style crossovers|Wolverine, Hulk, Cyclops, Beast, Gambit, Mister Sinister, Spider-Man, Magneto, Apocalypse
Apocalypse returns to a mutant community weakened by M-Day. The X-Men confront his renewed plans as his influence threatens to draw familiar faces into the role of Horsemen.|The Blood of Apocalypse|Apocalypse
Claremont imagines a final chapter for the X-Men in an alternate future. The opening book begins a trilogy-wide crisis whose attacks and losses will reach across the extended mutant family.|The End: Dreamers and Demons|X-Men
Xavier and Magneto take the struggle into space as the trilogy reaches its final confrontation. The survivors face the forces behind the coordinated attacks in this imagined ending for the X-Men.|The End: Men and X-Men|Professor X, Magneto
After an attack devastates the Xavier Academy, Cyclops rallies the survivors. The team searches for the people orchestrating the assault on mutantkind while coping with the losses of the opening book.|The End: Heroes and Martyrs|Cyclops
Hope's birth, Cable's struggle to protect her and her return to the present form a connected mutant survival story. This omnibus combines Messiah Complex, Messiah War and Second Coming with companion material.|Messiah Complex / Messiah War / Second Coming|Hope Summers, Cable
An outcast child in ancient Egypt becomes En Sabah Nur, the future Apocalypse. Later historical adventures explore his links to Sinister, Dracula and other figures across centuries of mutant history.|Rise of Apocalypse / historical encounters|Apocalypse, Ozymandias, Rama-Tut, Cyclops, Jean Grey, Mister Sinister, Dracula
Gambit's hidden past threatens his relationship with Rogue and his place among the X-Men. An expanded collection combines the trial-era team adventures with missions for the Imperial Guard, Psylocke, Archangel and Bishop.|The Trial of Gambit / Crimson Dawn / companion miniseries|Gambit, Rogue, Psylocke, Archangel, Bishop, Imperial Guard
Rogue and Gambit's growing closeness exposes secrets that put Remy on trial. The surrounding adventures send the team into a Shi'ar conflict with the Phalanx, including Cannonball's clash with Gladiator.|The Trial of Gambit / Shi'ar Phalanx crisis|Gambit, Rogue, Cannonball, Gladiator
Wanda Maximoff's death on Krakoa makes Magneto the focus of a murder investigation. The search for the truth strains mutant law and threatens the foundations of the nation he helped build.|The Trial of Magneto: Krakoan murder mystery|Scarlet Witch, Magneto
Juggernaut accepts a place among the X-Men and forms a bond with young Sammy. New teachers, Havok's return and threats from the Church of Humanity challenge the school's ability to offer refuge.|Juggernaut joins / school upheaval / Church of Humanity|Juggernaut, Professor X, Northstar, Husk, Havok, Iceman, Archangel, Alpha Flight
Scott and Jean prepare to marry while the Legacy Virus and Sabretooth's presence darken life at the mansion. Friends and family gather for a celebration amid the team's ongoing crises.|The Wedding of Cyclops and Phoenix|Cyclops, Jean Grey, Sabretooth
A series of murders brings Logan and Remy to London with hints of Jack the Ripper's return. The uneasy partners investigate a mystery that tests how much they can trust one another.|Wolverine/Gambit: Victims|Wolverine, Gambit
An apparent attack by Cable on Xavier drives the mutant teams into conflict while Scott and Jean are abducted. Stryfe, Sinister and Apocalypse turn the crisis into a battle over the Summers family's secrets.|X-Cutioner's Song|Cyclops, Jean Grey, Cable, Professor X, Stryfe, Mister Sinister, Apocalypse, X-Factor, X-Force
Wolverine reluctantly mentors Kitty through a selection of early-style adventures. A Power Pack team-up adds a museum battle against Sauron to these glimpses of Logan as teacher and reluctant partner.|X-Verse: Wolverine and Kitty / Power Pack|Wolverine, Kitty Pryde, Professor X, Alpha Flight, Power Pack, Sauron
Selected stories spotlight Magneto's ambitions, Sabretooth's cruelty and Apocalypse's Horsemen. A Spider-Man crossover adds Sinister's cloning schemes to this sampler of mutant villains.|X-Verse: Magneto / Sabretooth / Apocalypse / Sinister|Magneto, Sabretooth, Apocalypse, Mister Sinister, Wolverine, Spider-Man, X-Factor
Jean and Storm's early lives sit alongside Kitty's solitary battle with a Christmas-time demon. Other short adventures spotlight Rogue, Mystique, Dani and Wolfsbane in this collection of mutant women.|X-Verse: X-Women origins and spotlights|Jean Grey, Storm, Kitty Pryde, Rogue, Mystique, Dani Moonstar, Wolfsbane
Kate Pryde protects her family in a Battleworld domain ruled by Sentinels. The persecuted mutants plan escape and rebellion while a long-kept secret threatens their fragile unity.|Years of Future Past: Battleworld rebellion|Kitty Pryde
An emerging psychic menace gathers followers and draws Earth's heroes into the X-Men's crisis. Cable and Nate Grey confront warnings of the coming threat as the mystery of Onslaught's identity takes shape.|Onslaught: emergence and revelation|Cable, X-Man, Juggernaut, Avengers, Fantastic Four, Professor X
Onslaught's reach spreads through Manhattan and the wider superhero community. The fight to save Franklin Richards draws in Hulk, while Ben Reilly and other city heroes face the Sentinel assault.|Onslaught: siege and escalation|Franklin Richards, Hulk, Cable, Storm, X-Factor, X-Force, Mister Sinister, Ben Reilly, Iron Man
Earth's heroes unite against Onslaught's final attack on New York. The climax and aftermath explore the cost of stopping him and Xavier's responsibility for the catastrophe.|Onslaught: final battle and aftermath|Avengers, Fantastic Four, Professor X
The X-Men want Franklin Richards to join Krakoa, but his family challenges their claim on his future. Doctor Doom complicates a dispute about identity, belonging and who gets to decide for a young hero.|4X: Franklin Richards and Krakoa|Franklin Richards, Fantastic Four, Professor X, Doctor Doom
Ogun's psychic attack on Kitty reunites the X-Treme team for a new mission. Their investigation uncovers additional anti-mutant threats in a later-written adventure set after the original run.|X-Treme X-Men: A New Beginning|Kitty Pryde, Ogun, Bishop, Sage, Gambit, Rogue, Rachel Summers, Storm, Wolverine
Animated-style Spider-Man adventures bring Kingpin's enforcers, Mysterio's illusions and the Beetle into Peter's path. Doctor Octopus and Venom then combine forces against the wall-crawler.|Spectacular Foes: animated-style villain battles|Kingpin, Enforcers, Mysterio, Beetle, Doctor Octopus, Venom
The future of 2099 faces a new upheaval across its heroes' lives. Miguel O'Hara's destiny, Alchemax's Venom project and Doom's ambitions connect a set of future-world one-shots.|2099: Alpha to Omega companion stories|Spider-Man 2099, Doctor Doom
Sin-Eater's escalating power drives Peter toward another confrontation with Norman Osborn. Other spider-heroes gather as the Order of the Web while the Kindred crisis approaches its breaking point.|Green Goblin Returns / Sin-Eater|Green Goblin, Sin-Eater, Kindred, Miles Morales, Spider-Woman, Ghost-Spider, Spider-Girl, Madame Web
Kindred steps out of the shadows and subjects Peter to a deeply personal assault. Spider-Man turns to Doctor Strange, but surviving the confrontation requires more than another superhero team-up.|Last Remains|Kindred, Doctor Strange
Peter tries to rebuild after Last Remains while Mister Negative pursues his own alter ego. The aftermath strains Peter and Mary Jane's relationship and leaves the Osborn family at the center of unresolved damage.|Shattered Web / Last Remains aftermath|Mister Negative, Mary Jane Watson, Norman Osborn, Harry Osborn
Kingpin hunts the Lifeline Tablet and makes Boomerang a target. Peter's loyalty to his roommate pulls him into a citywide criminal contest, while the Robertson and Lincoln families clash over a romance.|King's Ransom / Lifeline Tablet|Kingpin, Boomerang, Beetle, Tombstone
Peter teams up with his spy sister Teresa as Chameleon makes a major move. A conspiracy involving the Foreigner, Chance and Jack O'Lantern puts both Parkers in danger.|Chameleon Conspiracy|Teresa Parker, Chameleon, Foreigner, Chance, Jack O'Lantern
Rival villain teams led by Doctor Octopus and Vulture tear into Spider-Man's life. Kindred's plans reach their endgame as Spencer's long-running mysteries converge with Sinister War.|What Cost Victory? / Sinister War aftermath|Doctor Octopus, Vulture, Kindred
Peter and Mary Jane face threats linked to the figure manipulating events from the shadows. Boomerang's trouble with the Sinister Syndicate draws Spider-Man into his roommate's criminal past.|Behind the Scenes / Sinister Syndicate|Mary Jane Watson, Boomerang, Mysterio, Beetle, Electro, Lady Octopus, Scorpia, White Rabbit
Peter must protect Dylan Brock while Carnage hunts people carrying traces of symbiotes. Norman Osborn's Red Goblin past complicates the rescue, and an additional one-shot revisits his rampage.|Absolute Carnage tie-ins / Red Goblin stories|Carnage, Dylan Brock, Norman Osborn
Miguel O'Hara returns to the present with his future at risk. Peter's ordinary troubles collide with the 2099 crisis and draw Doctor Doom and Silver Sable into the adventure.|2099: present-day Spider-Man chapters|Spider-Man 2099, Doctor Doom, Silver Sable, J. Jonah Jameson
Jameson's new podcast and Chance's villain casino create fresh trouble for Peter. Meanwhile, Boomerang's activities bring Spider-Man's home life closer to Mayor Fisk's ambitions.|Threats and Menaces|J. Jonah Jameson, Chance, Boomerang, Kingpin
Kindred resurrects Sin-Eater and turns his crusade against sinners into a growing threat. Peter must decide how to confront a vigilante whose targets include some of the city's most dangerous criminals.|Sins Rising|Kindred, Sin-Eater
Peter begins this run estranged from people he depends on. Tombstone's criminal plans force Spider-Man into a brutal confrontation while the reasons for Peter's broken relationships remain unresolved.|World Without Love / Tombstone|Tombstone, Doctor Octopus
An enemy combines the Sinister Six's abilities into the Sinister Adaptoid. Norman Osborn's return then brings Peter new equipment and a major change in how he operates.|The New Sinister / Oscorp suit|Sinister Six, Norman Osborn
Peter faces Judgment Day, renewed Hobgoblin trouble and a dangerous mission with Wolverine after the Hellfire Gala. The volume combines those different pressures on his increasingly complicated life.|Hobgoblin / Judgment Day / Hellfire Gala|Hobgoblin, Wolverine
Wells's opening run follows Peter's estrangement, Tombstone's schemes, Norman Osborn's uneasy support and the Dark Web crisis. It continues into the revelations about Peter and Mary Jane's separation and their costly aftermath.|Wells omnibus: opening run / Dark Web / Dead Language|Tombstone, Norman Osborn, Mary Jane Watson, Ben Reilly, Madelyne Pryor
After Gang War, Peter faces the neglected parts of his personal life and new trouble from Electro. Chasm's escape, Norman's mysteries and the vampire invasion prevent any real respite.|Breathe / Gang War aftermath / Blood Hunt tie-in|Electro, Ben Reilly, Hallows' Eve, Norman Osborn
Norman's sins return and reignite the Green Goblin conflict. With the Sinister Six also back, Peter faces another violent upheaval that threatens his own identity.|Going Green|Green Goblin, Sinister Six
Tombstone seeks to cement his position as New York's crime boss by killing Spider-Man. Peter becomes the target of a kidnapping as Wells's run returns to its central street-level rivalry.|Dead Wrong / Tombstone finale|Tombstone
Ben Reilly and Madelyne Pryor unleash a demonic crisis over New York. Peter's struggle against Chasm takes him into Limbo while Spider-Man and the X-Men try to stop the Goblin Queen's plans.|Dark Web|Ben Reilly, Madelyne Pryor, X-Men, Venom, Hallows' Eve
Peter and Felicia try to escape the aftermath of Dark Web, but danger interrupts their getaway. The story then begins revealing what happened between Peter and Mary Jane before this run started.|Dead Language, part one / Black Cat getaway|Black Cat, Mary Jane Watson
The Emissary returns as the mystery of Peter's recent past reaches its costly conclusion. Annual and memorial stories add aftermath, while Hallows' Eve attempts to free Chasm.|Dead Language, part two / aftermath|Norman Osborn, Hallows' Eve, Ben Reilly
Doctor Octopus attacks with upgraded arms while Peter is still grieving. Randy and Janice's wedding then becomes an opportunity for the city's criminals to strike at Tombstone.|Armed and Dangerous / wedding crisis|Doctor Octopus, Tombstone, Beetle
A villainous alliance sends Peter into a darker kind of hunt. Its consequences linger when Rek-Rap returns, bringing a bizarre change of tone and a new danger of his own.|Spider-Man's First Hunt / Rek-Rap|Rek-Rap
New York's criminal power struggle erupts into open warfare. Spider-Man needs allies as Tombstone, Kingpin and rival crime bosses maneuver for control of the city.|Gang War|Tombstone, Kingpin, Madame Masque, Hobgoblin, Beetle, Diamondback
Jameson threatens Peter's secret while a succession of villains turns Manhattan into a battlefield. Green Goblin's return raises the personal stakes, and Peter considers a major step with Mary Jane.|Big Apple Battleground / Green Goblin / proposal|J. Jonah Jameson, Lizard, Punisher, Green Goblin, Nova, Mary Jane Watson
Firelord brings a cosmic challenge to Peter's street-level world, while a Spider-Slayer mistakes Mary Jane for Spider-Man. Encounters with Silver Sable, Black Fox and other unusual opponents round out this mid-eighties collection.|Ghosts of the Past / Firelord / Spider-Slayers|Firelord, Mary Jane Watson, Silver Sable, Black Fox, Frog-Man, Toad
Relentless Spider-Slayer attacks leave Peter hunting for their organizer. His parents' return remains suspicious, Venom faces judgment, and a Doctor Strange team-up takes the action into a demonic dimension.|Invasion of the Spider-Slayers / Trial of Venom|Electro, Scorpion, Black Cat, Venom, Doctor Strange
Peter's reunion with his parents unravels as old enemies push him toward a breakdown. Vulture's renewed life and clashes with Chameleon, Shriek and Carrion deepen the crisis.|Lifetheft / family revelations / Pursuit-era crisis|Vulture, Chameleon, Shriek, Carrion, Hulk
John Jameson's transformation into Man-Wolf and Harry Osborn's descent into the Goblin legacy darken Peter's life. Punisher and Jackal enter the picture amid increasingly dangerous personal upheavals.|Man-Wolf at Midnight / Punisher and Jackal arrive|Man-Wolf, Harry Osborn, Punisher, Jackal, Doctor Octopus, Aunt May
The return of Uncle Ben's killer forces Peter to confront the event that shaped him. Black Cat makes her entrance while Mysterio, Doctor Octopus and a gang conflict keep the pressure on.|The burglar returns / Black Cat's debut|Black Cat, Mysterio, Doctor Octopus, Punisher, Dazzler
Doctor Octopus assembles a new Sinister Six, and the aftermath leads Peter to reconsider his powers. Venom, Doctor Doom and a haunted Scottish trip complicate any hope of normal life.|Return of the Sinister Six / Spirits of the Earth|Doctor Octopus, Sinister Six, Black Cat, Venom, Avengers, Doctor Doom, Mary Jane Watson
Gwen Stacy's apparent return introduces Peter to the Jackal's cloning schemes. Later clashes with Doctor Octopus and Kingpin accompany a growing relationship with Mary Jane.|The original Clone Saga / Spider-Man or Spider-Clone?|Gwen Stacy, Jackal, Doctor Octopus, Kingpin, Mary Jane Watson
Madame Web enters Peter's world as city life brings assassinations, prison trouble and strange combinations of familiar villains. Annual adventures add Doctor Strange and Punisher to the collection.|Threat or Menace? / Madame Web's debut|Madame Web, Hydro-Man, Sandman, Doctor Strange, Punisher
Captain Stacy's death changes Peter and Gwen's lives during a confrontation with Doctor Octopus. The surrounding stories introduce Morbius and take Peter through the unsettling six-arm crisis.|The Death of Captain Stacy / Morbius / six-arm saga|Gwen Stacy, Captain Stacy, Doctor Octopus, Morbius, Black Widow, Iceman
Carnage forces Peter to seek an alliance with Venom. Other adventures bring the New Warriors into a fight and revisit the psychological aftermath of Kraven's Last Hunt.|Carnage's arrival / The Hero Killers / Soul of the Hunter|Carnage, Venom, New Warriors, Kraven the Hunter, Lizard, Taskmaster, Red Skull
Peter's discarded symbiote bonds with Eddie Brock to create Venom, threatening his new marriage. Surrounding adventures include the Mad Dog Ward story and encounters with several returning enemies.|Venom's arrival / Mad Dog Ward|Venom, Mary Jane Watson, Doctor Octopus, Silver Sable, Sandman
Peter's poisoning makes Doctor Octopus an unlikely source of help while Ben Reilly faces new enemies. Kaine and the Jackal deepen the Clone Saga's uncertainty as Peter's family confronts major changes.|Web of Life / Web of Death / Clone Saga|Ben Reilly, Doctor Octopus, Kaine, Jackal, Mary Jane Watson, Aunt May
Peter gains his powers and learns the responsibility that defines Spider-Man. His earliest adventures introduce the Daily Bugle, recurring enemies and his first encounters with other Marvel heroes.|Spider-Man's origin and first villains|J. Jonah Jameson, Doctor Octopus, Sandman, Vulture, Electro, Fantastic Four, Human Torch
Peter's early career brings the Green Goblin and the first Sinister Six showdown. Meetings with Daredevil and Hulk broaden his place in the superhero world.|Green Goblin arrives / the original Sinister Six|Green Goblin, Sinister Six, Daredevil, Hulk
Scorpion and Molten Man join Peter's growing collection of enemies. Familiar villains return while Doctor Strange and Human Torch become part of his early adventures.|Early Spider-Man: Scorpion and Molten Man|Scorpion, Molten Man, Green Goblin, Vulture, Doctor Strange, Human Torch
Peter begins college while Aunt May's illness and the Master Planner's crimes converge. The collection includes his desperate struggle beneath heavy machinery and a defining confrontation with Green Goblin.|If This Be My Destiny / Green Goblin unmasked|Doctor Octopus, Aunt May, Gwen Stacy, Green Goblin, Harry Osborn
Mary Jane finally enters Peter's social life as Rhino and Shocker arrive among his enemies. Kingpin's debut caps a period when Peter questions the burden of being Spider-Man.|Mary Jane arrives / Spider-Man No More!|Mary Jane Watson, Gwen Stacy, Harry Osborn, Rhino, Shocker, Kingpin, Lizard
A science job and new opportunities seem to put Peter on firmer ground, but Hobgoblin and Scorpion threaten that progress. His expanding responsibilities bring him toward the Future Foundation.|Big Time / Hobgoblin / Matters of Life and Death|Hobgoblin, Scorpion, J. Jonah Jameson, Fantastic Four
Peter returns to his old school as a teacher while Ezekiel challenges his understanding of his powers. Morlun becomes a deadly new enemy, and Peter's relationship with Aunt May reaches a turning point.|Coming Home / Morlun / The Conversation|Ezekiel, Morlun, Aunt May, Doctor Octopus
Ezekiel's explanation of Peter's powers complicates his view of the spider bite. Teaching, personal relationships and battles alongside other heroes connect the next phase of JMS's run through the legacy-numbered 500th issue.|The Life and Death of Spiders / Happy Birthday era|Ezekiel, Iron Man, Captain America
Peter reclaims his life and tries to restore his role as a friendly neighborhood hero. Electro's renewed threat challenges that fresh start after the Superior Spider-Man era.|The Parker Luck: Peter returns|Electro
Peter teams up with Ms. Marvel as the first warnings of Spider-Verse appear. Elsewhere, Otto encounters a hunter targeting spider-heroes and tries to gather allies against the threat.|Spider-Verse Prelude|Ms. Marvel, Superior Spider-Man, Spider-UK, Spider-Girl
The Inheritors hunt spider-powered heroes across realities, forcing Peter and Otto into an uneasy alliance. Miles and Silk join the struggle to prevent the destruction of the spider-totems.|Spider-Verse: main Amazing chapters|Superior Spider-Man, Miles Morales, Silk, Morlun
Peter returns from Spider-Verse to an attack on Parker Industries. Ghost's sabotage threatens both the company and the people whose safety Peter is responsible for.|Graveyard Shift / Ghost attacks|Ghost
Beyond Corporation installs Ben Reilly as its sponsored Spider-Man while Peter's condition leaves others worried. Ben faces classic enemies and trains with the Daughters of the Dragon as corporate expectations close around him.|Beyond: Ben Reilly takes over|Ben Reilly, Mary Jane Watson, Black Cat, Aunt May, Morbius, Kraven the Hunter, Daughters of the Dragon
Beyond sends Ben after Miles over the Spider-Man identity while Peter recovers in hospital. Mary Jane investigates a disappearance, and Aunt May seeks Doctor Octopus's help.|Beyond: rival Spider-Men / hospital mystery|Ben Reilly, Miles Morales, Mary Jane Watson, Aunt May, Doctor Octopus
Doctor Octopus's attack rattles Ben as Peter attempts to return to action. Queen Goblin emerges, and Mary Jane and Black Cat face a separate rescue mission.|Beyond: Queen Goblin / Mary Jane and Black Cat|Ben Reilly, Doctor Octopus, Captain America, Black Cat, Mary Jane Watson, Queen Goblin
The dangers hidden inside Beyond force Ben and Peter toward a showdown. Queen Goblin, the Lizard and Monica Rambeau become part of the struggle over the company's secrets.|Beyond: Door Z and finale|Ben Reilly, Black Cat, Queen Goblin, Lizard, Monica Rambeau
Peter protects New Yorkers during the vampire invasion and becomes entangled with Morbius. Miles faces a costly mission linked to Blade in the companion chapters.|Blood Hunt: Peter and Miles|Miles Morales, Morbius, Blade
Five alternate spider-heroes receive their own introductions, from Spider-Man Noir to Gwen Stacy and SP//dr. The anthology explores distinct worlds as the larger Spider-Verse threat approaches.|Edge of Spider-Verse: five alternate origins|Spider-Man Noir, Ghost-Spider, Peni Parker, Aaron Aikman
A S.H.I.E.L.D. summons sends Peter around the world in a deliberately unpredictable adventure. A mysterious prisoner keeps the mission moving through encounters with Nick Fury, Wolverine and Spider-Ham.|Full Circle|Nick Fury, Wolverine, Spider-Ham
The Order of the Web tries to help Peter survive Kindred's assault. Doctor Strange and Mary Jane become involved as the other spider-heroes experience the events surrounding Last Remains.|Last Remains: Order of the Web companion|Miles Morales, Ghost-Spider, Silk, Spider-Woman, Doctor Strange, Mary Jane Watson
Norman Osborn finds a new source of power in the Carnage symbiote and becomes the Red Goblin. The collection builds toward Slott's final confrontation and includes his closing Spider-Man story.|Red Goblin: buildup and finale|Norman Osborn, Carnage
On Battleworld, Peter and Mary Jane raise their daughter under Regent's rule. Protecting his family forces Peter back into costume, but the rest of the Parkers refuse to remain bystanders.|Renew Your Vows: Battleworld family|Mary Jane Watson, Annie Parker, Regent
The Jackal offers the return of dead loved ones in exchange for loyalty. Peter confronts a conspiracy that draws his enemies and supporting heroes into a dangerous new version of cloning.|The Clone Conspiracy: event and tie-ins|Jackal, Rhino, Lizard, Electro, Doctor Octopus, Silk, Prowler
A later-written adventure returns to Peter's college days with Gwen, MJ, Harry and Flash. Evangeline's interdimensional threat collides with Peter's relationships and a difficult personal choice.|Torn: college-era adventure|Gwen Stacy, Mary Jane Watson, Harry Osborn, Flash Thompson, Evangeline
Peter runs Parker Industries on a global scale while Zodiac expands its ambitions. Mister Negative's activities in Shanghai then bring a new international crisis to the company's doorstep.|Worldwide: Zodiac / Shanghai|Mister Negative, Zodiac
Parker Industries gives Peter resources and responsibilities around the world. Zodiac's renewed threat tests whether his corporate success can coexist with Spider-Man's mission.|Worldwide: global launch and Zodiac|Zodiac
Mister Negative's arrival in Shanghai turns Peter's international operation into a battleground. The villain's control over other heroes complicates Spider-Man's attempt to stop him.|Worldwide: Shanghai / Mister Negative|Mister Negative
Regent begins imprisoning heroes and stealing their powers. Peter, Miles and Iron Man must work through their differences, with Mary Jane potentially holding the key to stopping him.|Worldwide: Power Play|Regent, Miles Morales, Iron Man, Avengers, Mary Jane Watson
An accident at Parker Industries tests Peter's duties to his staff. Prowler encounters a new Electro, and Doctor Octopus acts as the groundwork for Dead No More is laid.|Worldwide: Before Dead No More|Prowler, Electro, Doctor Octopus
The Clone Conspiracy brings Doctor Octopus back into Peter's life and connects him to the Jackal's plans. Kaine and Carrion add further complications in these Amazing-series companion chapters.|Worldwide: Clone Conspiracy tie-ins|Doctor Octopus, Jackal, Kaine, Carrion
Peter confronts a sane Norman Osborn whose military resources pose a different threat from the Goblin. Parker Industries becomes a weapon and a target in their escalating contest.|Worldwide: Parker vs. Osborn|Norman Osborn
Superior Octopus allies with Hydra to take Parker Industries from Peter. Secret Empire's aftermath leaves Spider-Man rebuilding his life, with Mockingbird offering support.|Worldwide: Secret Empire / Fall of Parker|Superior Spider-Man, Mockingbird
Peter revisits Zodiac's threat and encounters Loki in the role of Sorcerer Supreme. Norman searches for a way back to his Goblin identity while Betty Brant investigates a message from Ned Leeds.|Worldwide: Threat Level Red buildup|Loki, Norman Osborn, Betty Brant, Ned Leeds, Clash
The Carnage symbiote gives Norman Osborn a terrifying new identity. Peter and his allies face the Red Goblin in the conclusion of Slott's run, followed by a final reflective story.|Worldwide: Go Down Swinging / Red Goblin finale|Norman Osborn, Carnage
Peter and Logan travel through strange corners of time and reality while trying to identify who is manipulating them. Their uneasy partnership is tested by bizarre enemies and their own clashing personalities.|Astonishing Spider-Man and Wolverine|Wolverine
Spider-Man and Red Hulk confront a subterranean invasion during the New York Marathon. Later team-ups bring Hawkeye and Captain America into this opening collection of Avenging Spider-Man.|My Friends Can Beat Up Your Friends|Red Hulk, Hawkeye, Captain America'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/deep-batch-06.json').read_text());rows=ROWS.splitlines();assert len(ids)==len(rows)==100
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books'];by={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'));before=copy.deepcopy(payload['books'])
    path=ROOT/'data/editorial-enrichment.json';editorial=json.loads(path.read_text(encoding='utf-8'));notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        b=by[isbn];d=copy.deepcopy(before.get(b['id'],{}));source=d.get('pagesSource') or b['catalogUrl'];summary,story,guests=row.split('|')
        for key in ['level','automation','review']:d.pop(key,None)
        d.update(summary=summary,pages=d.get('pages'),pagesSource=source,coverSource=d.get('coverSource',source),checkedAt=datetime.date.today().isoformat(),editorialBatch='deep-06',stories=[dict(title=story,coverage='Story highlights; see edition and reading notes')],characters=[dict(name=n,role='Featured in cited synopsis; not a complete cameo index',source=source) for n in dict.fromkeys((['X-Men'] if i<=25 else ['Spider-Man'])+[g.strip() for g in guests.split(',') if g.strip()])],issueKeys=[],startingPoint=False)
        d['sources']=[dict(label='ISBN metadata / publisher synopsis' if d.get('pages') else 'OCLS · imported edition record',url=source)]
        d['readingPath']=run(('X-Men — ' if i<=25 else 'Spider-Man — ')+story,1,'Separate collection. No universal chronology is implied.')
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
    report=dict(batch='deep-06',records=100,reviews=sum(bool(d.get('review')) for d in notes.values()),missingPages=sum(not d.get('pages') for d in notes.values()),remainingXMen=sum('x-men' in b['title'].lower() and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog),notes='100 researched records; previous work preserved. Edition uncertainties and missing ratings remain explicit.')
    report['xMenRecords']=25;report['spiderManRecords']=75
    report['remainingSpiderMan']=sum(any(t in b['title'].lower() for t in ['spider-man','spiderman']) and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog)
    write_json(ROOT/'data/deep-batch-06-audit.json',report);print(json.dumps(report))

def configure(n,by,ids,before):
    def cite(i,url,label='Additional publisher / contents source; page count not transferred'):
        n[i]['sources'].append(dict(label=label,url=url))
    def issues(i,*specs):n[i]['issueKeys']=[key for title,year,a,b in specs for key in group(title,year,a,b)]
    def path(i,name,pos,note,alt=False):n[i]['readingPath']=run(name,pos,note,alt)
    def note(i,text):n[i]['readingPath']['note']=text
    def caution(i,text):n[i]['checks']['edition']=text;n[i]['contentsNote']=text
    def seq(indices,name,series,year,ranges,positions=None):
        for j,(i,(a,b)) in enumerate(zip(indices,ranges)):
            pos=positions[j] if positions else j+1
            issues(i,(series,year,a,b));path(i,name,pos,'Read in this run’s volume order. Event companions and gaps are identified separately.');n[i]['startingPoint']=pos==1
    def prior(i,isbn):
        d=before[by[isbn]['id']]
        for s in d['sources']:
            if 'roundup' not in s['url']:cite(i,s['url'],'Previously checked source for shared storyline; edition extras differ')
    issues(1,('The Adventures of Cyclops and Phoenix',1994,1,4),("Askani'son",1996,1,4),('X-Men: Phoenix',1999,1,3))
    prior(1,'9781302506629');cite(1,'https://play.google.com/store/books/details/Scott_Lobdell_X_Men?id=AcVaBAAAQBAJ','Publisher edition contents')
    note(1,'Shares Adventures 1–4 with Past & Future, but adds Askani material instead of Further Adventures. Read the core honeymoon story before the future-family companions.')
    issues(2,('X-Men Adventures',1992,1,8));note(2,'Adaptations from the animated series; not the main-universe Uncanny numbering. Starts the 1992 comic adaptation.');n[2]['startingPoint']=True
    issues(3,('Adventures of the X-Men',1996,1,12),('Adventures of Spider-Man',1996,3,3));note(3,'Animated-style 1996 adventures, separate from the earlier X-Men Adventures adaptation. Partial magazine material is not indexed.')
    issues(4,('X-Men',1991,182,187));prior(4,'9781302940140');note(4,'The final Blood of Apocalypse arc of Milligan’s run. The larger Milligan collection also includes earlier Decimation chapters and Cable & Deadpool; this smaller book does not.')
    seq([5,7,6],'X-Men — The End (alternate future)','X-Men: The End - Dreamers and Demons',2004,[(1,6),(1,6),(1,6)])
    issues(7,('X-Men: The End - Heroes and Martyrs',2005,1,6));issues(6,('X-Men: The End - Men and X-Men',2006,1,6))
    cite(5,'https://www.marvel.com/comics/issue/523/x-men_the_end_-_dreamers_demons_2004_1');cite(6,'https://www.marvel.com/comics/series/739/xmen_the_end_men_and_xmen_2006')
    for i in [5,7,6]:note(i,'Dreamers and Demons, then Heroes and Martyrs, then Men and X-Men. An alternate-future ending, not the final event in main continuity.');n[i]['startingPoint']=False
    cite(8,'https://www.penguinrandomhouse.com/books/801685/x-men-the-messiah-trilogy-omnibus-david-finch-cover-by-ed-brubaker/')
    for isbn in ['9781302520120','9781302520564','9780785171485']:n[8]['issueKeys']+=before[by[isbn]['id']]['issueKeys']
    n[8]['issueKeys']+=group('X-Men: The Times and Life of Lucas Bishop',2009,1,3)
    path(8,'X-Men — Messiah storyline',1,'Combined alternative to Messiah Complex, Messiah War and Second Coming. Does not include the complete Cable ongoing series.',True)
    caution(8,'Publisher listings differ over Cable 11–12 and Hellbound/Blind Science extras. Only the shared core trilogy and Bishop miniseries are indexed; exact digital contents and page count need confirmation.')
    issues(9,('Rise of Apocalypse',1996,1,4),('The Further Adventures of Cyclops and Phoenix',1996,1,4),('X-Men: Apocalypse/Dracula',2006,1,4),('Black Knight: Exodus',1996,1,1),('Fantastic Four',1961,19,19))
    note(9,'Historical character anthology, not a contemporary X-Men arc. Overlaps Past & Future, Apocalypse/Dracula and Road to Onslaught omnibus material.')
    issues(11,('Uncanny X-Men',1963,341,350),('X-Men',1991,62,64));n[11]['issueKeys']+=['Uncanny X-Men (1963) #-1','X-Men (1991) #-1']
    n[10]['issueKeys']=n[11]['issueKeys'][:]
    for spec in [('Imperial Guard',1997,1,3),('Psylocke & Archangel: Crimson Dawn',1997,1,4),('Gambit',1997,1,4),('Bishop: Xavier Security Enforcer',1998,1,3),('Marvel Fanfare',1996,4,5),('Longshot',1998,1,1)]:n[10]['issueKeys']+=group(*spec)
    cite(10,'https://www.marvel.com/comics/collection/132321/x-men_the_trial_of_gambit_omnibus_joe_madureira_cover_hardcover')
    caution(10,'Matching-title omnibus contents checked; exact digital extras and page count unconfirmed. Partial Valentine material is excluded.')
    for i in [10,11]:path(i,'X-Men — classic era collections',341,'After Onslaught. Both editions share the main trial-era chapters; the omnibus adds companion miniseries.',True)
    issues(12,('X-Men: The Trial of Magneto',2021,1,5));note(12,'Krakoa-era story after the first Hellfire Gala. Not Magneto’s classic 1985 trial in Uncanny 200.')
    issues(13,('Uncanny X-Men',1963,410,424),('X-Men Unlimited',1993,44,45));path(13,'Uncanny X-Men — early 2000s',410,'Follows the early Chuck Austen-era chapters. Separate from Morrison’s concurrent New X-Men, and from Whedon’s Unstoppable arc.')
    issues(14,('X-Men',1991,27,30),('X-Men Annual',1992,2,2),('X-Men Unlimited',1993,3,3),('Uncanny X-Men',1963,308,310),('X-Men Annual',1970,18,18),('What If?',1989,60,60));note(14,'After Fatal Attractions; the wedding precedes the Adventures of Cyclops and Phoenix honeymoon. The What If? chapter is an alternative, not main continuity.')
    issues(15,('Wolverine/Gambit: Victims',1995,1,4));note(15,'A four-part London mystery featuring the pair, not Gambit’s solo-series volume numbering.');n[15]['characters']=[c for c in n[15]['characters'] if c['name']!='X-Men']
    issues(16,('Uncanny X-Men',1963,294,297),('X-Factor',1986,84,86),('X-Men',1991,14,16),('X-Force',1991,16,18),("Stryfe's Strike File",1993,1,1));path(16,'X-Men — classic era collections',294,'Same central contents as the X-Cutioner’s Song Milestones edition; the Epic includes different surrounding chapters.',True)
    for number in [1,5,17,21]:n[17]['issueKeys']+=group('Wolverine: First Class',2008,number,number)
    n[17]['issueKeys']+=group('Wolverine and Power Pack',2008,1,1)
    issues(18,('Uncanny X-Men',1963,150,150),('Wolverine: First Class',2008,2,2),('X-Factor',1986,24,24),('X-Men/Spider-Man',2008,4,4))
    issues(19,('Marvel Girl',2011,1,1),('Uncanny Origins',1996,9,9),('Uncanny X-Men',1963,143,143),('Uncanny X-Men: First Class',2009,4,4))
    for i in [17,18,19]:note(i,'Themed sampler of separate adventures, not a continuous run or complete event. Some chapters come from longer series; partial anthology material is not indexed.')
    issues(20,('Years of Future Past',2015,1,5));note(20,'Secret Wars Battleworld reinterpretation. Separate from original Days of Future Past and the later Doomsday prequel.')
    issues(21,('Cable',1993,32,33),('Uncanny X-Men',1963,333,335),('X-Force',1991,55,55),('X-Man',1995,15,17),('X-Men',1991,53,54),('X-Men Unlimited',1993,11,11),('Onslaught: X-Men',1996,1,1),('Avengers',1963,401,401),('Fantastic Four',1961,415,415))
    issues(22,('Cable',1993,34,35),('Incredible Hulk',1968,444,445),('Wolverine',1988,104,104),('X-Factor',1986,125,126),('Amazing Spider-Man',1963,415,415),('Green Goblin',1995,12,12),('Spider-Man',1990,72,72),('X-Man',1995,18,19),('X-Force',1991,57,58),('X-Men',1991,55,55),('Uncanny X-Men',1963,336,336),('Iron Man',1968,332,332))
    issues(23,('Avengers',1963,402,402),('Punisher',1995,11,11),('Thor',1966,502,502),('Wolverine',1988,105,105),('X-Men',1991,56,57),('Onslaught: Marvel Universe',1996,1,1),('Onslaught: Epilogue',1996,1,1),('Cable',1993,36,36),('Uncanny X-Men',1963,337,337),('X-Men: The Road to Onslaught',1996,1,1))
    for i,p in [(21,1),(22,2),(23,3)]:path(i,'X-Men/Avengers — Onslaught',p,'Read these three volumes in numerical order after Road to Onslaught. They overlap event/Milestones collections; not every bonus is indexed.')
    issues(24,('X-Men/Fantastic Four',2020,1,4));note(24,'Early Krakoa, after House of X/Powers of X. Also included in Dawn of X Omnibus 2; not the 1987 Fantastic Four vs. X-Men story.')
    issues(25,('X-Treme X-Men',2022,1,5));note(25,'A later-written continuation set just after the original 2001–2004 run. Not a Krakoa-era team despite its 2022 publication date.')
    issues(26,('Adventures of Spider-Man',1996,7,12));path(26,'Adventures of Spider-Man (1996)',7,'Later half of the animated-style twelve-issue series. Not Amazing Spider-Man’s main continuity.')
    for title in ['2099 Alpha','Spider-Man 2099','Fantastic Four 2099','Ghost Rider 2099','Punisher 2099','Venom 2099','Doom 2099','2099 Omega']:n[27]['issueKeys']+=group(title,2019,1,1)
    note(27,'Companion to Spencer’s 2099 volume; contains future-world one-shots rather than Amazing 32–36. Read alongside that volume.')
    seq([34,35,36,37,38,28,29,30,31,32,33],'Amazing Spider-Man — Nick Spencer (2018)','Amazing Spider-Man',2018,[(24,28),(29,31),(32,36),(37,43),(44,47),(48,49),(50,55),(56,60),(61,65),(66,69),(70,74)],list(range(5,16)))
    n[35]['issueKeys']+=group('Red Goblin: Red Death',2019,1,1);n[38]['issueKeys']+=group('Amazing Spider-Man: Sins Rising',2020,1,1);n[28]['issueKeys']+=group('Spider-Man: The Sins of Norman Osborn',2020,1,1)
    n[31]['issueKeys']+=group("Giant-Size Amazing Spider-Man: King's Ransom",2021,1,1);n[32]['issueKeys']+=group('Giant-Size Amazing Spider-Man: Chameleon Conspiracy',2021,1,1)
    note(35,'Absolute Carnage tie-ins, not the full event. Red Death spelling normalized from the imported typo.');note(36,'Pair with the 2099 Companion one-shots for the wider future-world event.')
    note(29,'Main Last Remains story. The .LR issues in the companion take place alongside these chapters; they are different issues.')
    note(33,'Final Spencer volume; read alongside the separate Sinister War miniseries. Beyond follows at issue 75.')
    seq([39,40,41,46,47,48,49,50,51,43,44,45],'Amazing Spider-Man — Zeb Wells (2022)','Amazing Spider-Man',2022,[(1,5),(6,8),(9,14),(15,18),(19,23),(24,26),(27,31),(32,38),(39,44),(45,49),(50,54),(55,60)])
    n[46]['issueKeys']+=group('Dark Web',2022,1,1)+group('Dark Web Finale',2023,1,1)
    n[48]['issueKeys']+=group('Amazing Spider-Man Annual',2023,1,1)+group('Fallen Friend',2023,1,1)
    n[51]['issueKeys']+=group('Amazing Spider-Man: Gang War First Strike',2023,1,1)
    issues(42,('Amazing Spider-Man',2022,1,26),('Dark Web',2022,1,1),('Dark Web Finale',2023,1,1),('Amazing Spider-Man Annual',2023,1,1),('Fallen Friend',2023,1,1))
    cite(42,'https://www.penguinrandomhouse.com/books/801970/amazing-spider-man-by-zeb-wells-omnibus-vol-1-by-zeb-wells/')
    path(42,'Amazing Spider-Man — Zeb Wells (2022)',1,'Combined alternative to volumes 1–6, with event/annual material. Does not collect the entire Wells run.',True)
    caution(42,'Matching-title publisher omnibus checked; digital extras and page count remain unconfirmed. Review listing counts 29 issues against 30 here, so no score attached.')
    note(41,'Includes 2022 Hellfire Gala and A.X.E. tie-ins before the Hobgoblin material. The main events are separate.')
    note(46,'Includes Dark Web’s opening and finale plus Peter’s chapters. X-Men, Venom and other tie-ins are not all included.')
    note(48,'Continues Dead Language directly from Volume 5 and adds annual/memorial material. These extras may be placed later than the main arc.')
    note(51,'Main Amazing chapters and First Strike; other heroes’ Gang War tie-ins are separate.');note(43,'Issue 49 overlaps the Blood Hunt collection. The main Blood Hunt event remains separate.')
    classic={52:(165,185),53:(259,272),54:(368,377),55:(381,393),56:(124,142),57:(186,206),58:(334,350),59:(143,164),60:(207,223),61:(86,104),62:(361,367),63:(295,310),64:(397,399),65:(1,10),66:(11,19),67:(20,30),68:(31,40),69:(41,50)}
    for i,(a,b) in classic.items():issues(i,('Amazing Spider-Man',1963,a,b));path(i,'Amazing Spider-Man — classic era collections',a,'Ordered by main Amazing chapter. Masterworks/Epic volumes overlap other editions and leave gaps between these selected books.',True)
    n[52]['issueKeys']+=group('Amazing Spider-Man Annual',1964,11,12)+group('Nova',1976,12,12)
    n[53]['issueKeys']+=group('Amazing Spider-Man Annual',1964,18,19)+group('Web of Spider-Man',1985,1,1)+group('Web of Spider-Man',1985,6,6)
    cite(53,'https://www.marvel.com/comics/collection/48377/amazing_spider-man_epic_collection_ghosts_of_the_past_2014')
    cite(53,'https://www.hoopladigital.com/comic/amazing-spider-man-epic-collection-ghosts-of-the-past-tom-defalco/19121370','Hoopla · matching collection synopsis')
    caution(53,'Matching-title collection story and contents checked; page count not transferred from another print/digital edition.')
    n[54]['issueKeys']+=group('Amazing Spider-Man Annual',1964,27,27)+group('Spider-Man/Doctor Strange: The Way to Dusty Death',1992,1,1)+group('Spider-Man Special Edition: The Trial of Venom',1992,1,1)
    n[55]['issueKeys']+=group('Amazing Spider-Man Annual',1964,28,28)+group('Spider-Man',1990,45,45)+group('Peter Parker, The Spectacular Spider-Man',1976,211,211)+group('Web of Spider-Man',1985,112,112)
    n[56]['issueKeys']+=group('Giant-Size Super-Heroes',1974,1,1)
    n[57]['issueKeys']+=group('Amazing Spider-Man Annual',1964,13,13)+group('Spectacular Spider-Man Annual',1979,1,1)
    n[58]['issueKeys']+=group('Spider-Man: Spirits of the Earth',1990,1,1);n[59]['issueKeys']+=group('Amazing Spider-Man Annual',1964,10,10);n[60]['issueKeys']+=group('Amazing Spider-Man Annual',1964,14,15)
    caution(61,'Imported blurb misattributes the drug-addiction subplot to Norman. That claim is omitted; listed core issues and Captain Stacy/Morbius storylines are retained.')
    n[62]['issueKeys']+=group('Amazing Spider-Man Annual',1964,26,26)+group('Amazing Spider-Man: Soul of the Hunter',1992,1,1)
    note(62,'Carnage’s first arc and other stories. Soul of the Hunter follows Kraven’s Last Hunt; partial Hero Killers annual material is not counted as whole issues.')
    n[63]['issueKeys']+=group('Amazing Spider-Man Annual',1964,22,22)+group('Web of Spider-Man',1985,33,33)+group('Peter Parker, The Spectacular Spider-Man',1976,133,133)
    n[64]['issueKeys']+=group('Web of Spider-Man',1985,120,123)+group('Spider-Man',1990,54,56)+group('Peter Parker, The Spectacular Spider-Man',1976,220,222)+group('Spider-Man Unlimited',1993,8,8)+group('Spider-Man: Funeral for an Octopus',1995,1,3)
    note(64,'A middle chapter of the 1990s Clone Saga, not its starting point. Distinct from the original 1970s clone story and 2016 Clone Conspiracy.')
    n[65]['issueKeys']+=group('Amazing Fantasy',1962,15,15);n[65]['startingPoint']=True
    n[66]['issueKeys']+=group('Amazing Spider-Man Annual',1964,1,1);n[67]['issueKeys']+=group('Amazing Spider-Man Annual',1964,2,2);n[69]['issueKeys']+=group('Amazing Spider-Man Annual',1964,3,3)
    issues(70,('Amazing Spider-Man',1999,649,662));n[70]['issueKeys']+=['Amazing Spider-Man (1999) #654.1']
    path(70,'Amazing Spider-Man — Dan Slott: Big Time',1,'Begins the Big Time era; publisher lists only partial issue 648, which is not a whole-issue overlap. Before Superior Spider-Man and the 2014 relaunch.')
    seq([71,72],'Amazing Spider-Man — J. Michael Straczynski (1999 series)','Amazing Spider-Man',1999,[(30,45),(46,58)])
    n[72]['issueKeys']+=group('Amazing Spider-Man',1999,500,502)
    note(72,'After Coming Home. The series switches to legacy numbering at 500 after 58; no missing 59–499 sequence is implied.')
    seq([73,74,75,76],'Amazing Spider-Man — Dan Slott (2014)','Amazing Spider-Man',2014,[(1,6),(7,8),(9,15),(16,18)])
    cite(73,'https://comicbookroundup.com/comic-books/reviews/marvel-comics/amazing-spider-man-(2014)/1','Opening issue publisher synopsis · Peter’s return and Electro')
    n[74]['issueKeys']+=group('Superior Spider-Man',2013,32,33);n[76]['issueKeys']+=group('Amazing Spider-Man Annual',2014,1,1)
    note(73,'Peter returns after Superior Spider-Man. This is the 2014 relaunch, not Spencer’s or Wells’s Volume 1.')
    note(74,'Before the main Spider-Verse story. Different book from Edge of Spider-Verse’s five alternate-world origins. Partial FCBD material is not indexed.')
    note(75,'Main Amazing chapters of Spider-Verse, not the omnibus of every tie-in. Read Prelude first; the alternate-origin anthology is an optional companion.')
    seq([77,78,79,80],'Amazing Spider-Man — Beyond (2021–2022)','Amazing Spider-Man',2018,[(75,80),(81,85),(86,88),(89,93)])
    for i,num in [(77,78),(78,80),(79,88),(80,92)]:n[i]['issueKeys']+=[f'Amazing Spider-Man (2018) #{num}.BEY']
    n[79]['issueKeys']+=group('Mary Jane & Black Cat: Beyond',2022,1,1)
    note(77,'After Spencer’s issue 74 finale. Contains the different 78.BEY issue, plus partial setup from 74.')
    note(80,'Beyond concludes here; Wells’s 2022 relaunch and the later Dark Web follow.')
    issues(81,('Amazing Spider-Man: Blood Hunt',2024,1,3),('Amazing Spider-Man',2022,49,49),('Miles Morales: Spider-Man',2022,21,22))
    note(81,'Blood Hunt companion featuring both Spider-Men. Amazing 49 overlaps Breathe; the main event is separate. Miles’s series began in 2022 despite the imported 2023 label.')
    issues(82,('Edge of Spider-Verse',2014,1,5))
    cite(82,'https://irvine.overdrive.com/media/5879763','ISBN-matched OverDrive publisher description · Edge 1–5')
    cite(82,'https://books.google.com/books/about/Amazing_Spider_Man.html?id=dO_tBgAAQBAJ','ISBN-matched contents table contradicts the imported synopsis')
    caution(82,'Imported synopsis belonged to Spider-Verse Prelude. Contents table and ISBN-matched library record confirm Edge of Spider-Verse 1–5. Page counts conflict, so length is withheld.')
    n[82]['pages']=None
    for c in n[82]['characters']:c['source']='https://irvine.overdrive.com/media/5879763'
    note(82,'Alternate-origin anthology before/alongside Spider-Verse. Not Amazing 7–8 or Superior 32–33; those belong to Prelude.')
    issues(83,('Amazing Spider-Man: Full Circle',2019,1,1));note(83,'Standalone collaborative adventure rather than a numbered chapter in Spencer’s ongoing story.');n[83]['startingPoint']=True
    n[84]['issueKeys']=[f'Amazing Spider-Man (2018) #{num}.LR' for num in range(50,55)]
    path(84,'Amazing Spider-Man — Nick Spencer (2018)',11,'Read alongside Last Remains. .LR companion issues are distinct from Amazing 50–54 and must not be treated as duplicates.')
    issues(85,('Amazing Spider-Man',2015,794,801));path(85,'Amazing Spider-Man — Worldwide (2015)',8,'Combined alternative covering core issues from Worldwide 8 and all of 9, without every annual/extra.',True)
    issues(86,('Amazing Spider-Man: Renew Your Vows',2015,1,5));cite(86,'https://www.marvel.com/comics/collection/54954/amazing_spider-man_renew_your_vows_trade_paperback')
    note(86,'Secret Wars Battleworld family story, separate from main-universe Peter and the later Renew Your Vows ongoing. Digital and print listings differ on bonus material; core five issues only indexed.')
    issues(87,('Amazing Spider-Man',2015,19,24),('The Clone Conspiracy',2016,1,5),('The Clone Conspiracy: Omega',2017,1,1),('Silk',2015,14,17),('Prowler',2016,1,5));note(87,'Large event collection: overlaps Worldwide 4 issue 19 and Worldwide 5 issues 20–24, adding the main event and other tie-ins. Separate from both earlier Clone Sagas.')
    caution(87,'Silk uses the late-2015 series (the publisher’s 2015B label), not the earlier 2015 run. Partial FCBD material excluded.')
    issues(88,('Amazing Spider-Man: Torn',2025,1,5));note(88,'Newly written college-era story, not the next chapter of JMS’s 2001 ongoing run despite the shared writer.')
    issues(89,('Amazing Spider-Man',2015,1,11));path(89,'Amazing Spider-Man — Worldwide (2015)',1,'Larger alternative to the first two smaller Worldwide volumes.',True)
    cite(89,'https://books.google.com/books/about/Amazing_Spider_Man.html?id=UXyPDwAAQBAJ','ISBN-matched contents table · Amazing 1–11')
    caution(89,'Imported synopsis incorrectly described issues 12–19. ISBN contents table confirms 1–11; rewritten from the matching smaller volumes’ publisher descriptions.')
    seq(list(range(90,99)),'Amazing Spider-Man — Worldwide (2015)','Amazing Spider-Man',2015,[(1,5),(6,11),(12,15),(16,19),(20,24),(25,28),(29,32),(794,796),(797,801)])
    n[92]['issueKeys']+=group('Amazing Spider-Man Annual',1964,19,19);n[94]['issueKeys']+=group('Amazing Spider-Man Annual',2016,1,1)
    n[96]['issueKeys']+=group('Amazing Spider-Man',2015,789,791);n[97]['issueKeys']+=group('Amazing Spider-Man Annual',1964,42,42)
    note(94,'Amazing-series tie-ins to The Clone Conspiracy. The larger event collection includes the central miniseries; this volume does not.')
    note(96,'Secret Empire tie-ins, then legacy numbering 789–791. The next volume begins at 794; Venom Inc. covers the intervening crossover chapters separately.')
    note(97,'Core 794–796 overlaps the larger Red Goblin collection; annual and partial material differ.')
    note(98,'Final Slott volume. Spencer’s Back to Basics (2018) follows; the larger Red Goblin collection also contains these chapters.')
    issues(99,('Astonishing Spider-Man & Wolverine',2010,1,6));note(99,'Complete six-part time-travel team-up, not a volume in either hero’s ongoing series.');n[99]['startingPoint']=True
    issues(100,('Avenging Spider-Man',2011,1,5));cite(100,'https://pnm.overdrive.com/media/4455463','ISBN-matched publisher listing · issues 1–5, Hawkeye and Captain America')
    caution(100,'Imported Google copy says 1–6; ISBN-matched OverDrive and catalog agree on 1–5. Issue 6 is not indexed and an unmatched collection rating is withheld.')
    n[100]['pages']=None
    n[100]['checks']['edition']+=' Page count withheld until the edition mismatch is resolved.'
    for c in n[100]['characters']:c['source']='https://pnm.overdrive.com/media/4455463'
    path(100,'Avenging Spider-Man (2011)',1,'Opening team-up collection. Issue 6 belongs to a later crossover; this is not the full ongoing series.');n[100]['startingPoint']=True
    for i in [1,9]:n[i]['characters']=[c for c in n[i]['characters'] if c['name']!='X-Men']
    for i in [90,91]:
        for s in n[i]['sources']:cite(89,s['url'],'Publisher synopsis for included Worldwide chapters')
    for c in n[89]['characters']:
        if c['name']=='Zodiac':c['source']=n[90]['sources'][0]['url']
        elif c['name']=='Mister Negative':c['source']=n[91]['sources'][0]['url']
    for i in n:n[i]['issueKeys']=list(dict.fromkeys(n[i]['issueKeys']))
    reviews(n,by,ids)

def reviews(n,by,ids):
    scores=[]
    def add(slug,rows):
        for row in rows:scores.append((slug,*row))
    add('x-men-the-trial-of-magneto-(2021)',[(12,6.4,61,5.5,3)])
    add('amazing-spider-man-(2018)',[(34,7.3,47,7.4,12),(35,7.6,36,7.4,11),(36,7.3,36,7.6,7),(38,7.6,40,8.4,7),(29,7.5,65,8.2,6),(30,7.2,47,7.2,7),(31,7.4,52,6.5,6),(32,7.1,34,4.6,7),(33,6.8,32,3.6,7),(84,7.2,38,8.2,5),(77,8,64,7.1,8),(78,7.8,55,6.1,6),(79,8.3,49,6.7,5),(80,7.9,47,6.1,5)])
    add('amazing-spider-man-(2022)',[(39,8.1,54,7.6,7),(40,8.1,26,7.2,6),(41,7.6,41,7.9,5),(46,7.8,42,7,8),(47,6.9,36,6.9,4),(48,6.4,39,4.8,3),(49,7.3,37,7.2,4),(50,8,39,8.5,5),(51,7.9,44,6,5),(43,7.8,24,7.8,5),(44,7.2,34,6.8,3),(45,7.6,34,5.5,3)])
    add('amazing-spider-man-(2014)',[(73,7.6,140,6.9,5),(74,8.1,59,7.4,4),(75,7.7,138,8.2,7),(76,6.2,41,6,5)])
    add('amazing-spider-man-(2015)',[(89,7.7,109,7.5,1),(90,7.8,60,7.3,7),(91,7.6,49,6.7,5),(94,7.2,38,7.2,2),(95,7.7,29,6.8,2),(96,7.7,51,7.5,2),(97,6.6,47,7,2),(98,8.2,81,7.7,3),(87,7,135,7,1)])
    for slug,i,critic,count,user,ucount in scores:
        d=n[i];url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug
        d['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=ucount,url=url,checkedAt=d['checkedAt'],title=by[ids[i-1]]['title'],match='Trade row matched by series, volume/story and collected issue count; not ISBN.',scope='Aggregate for the reviewed issues in the matching collection; bonus stories and partial material may be excluded.')
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row',url=url));d['checks']['review']='Matching collection row checked'
    for i in [28,37,42,85,92,93,100]:n[i]['checks']['review']='Withheld: listed collection issue count or extras do not securely match review row'

if __name__=='__main__':main()

