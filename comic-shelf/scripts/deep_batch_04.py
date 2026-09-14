"""One hundred individually researched X-Men collections, September 2026."""
import copy
import datetime
import json
import msvcrt
from enrich_catalog import ROOT, write_json
from build_pilot import group, run

ROWS='''Beast brings the original teenage X-Men into a present they scarcely recognize. Seeing the people they become forces the young team to question both its mission and whether it can return home.|Yesterday's X-Men / Here to Stay|Beast, Jean Grey, Cyclops
The displaced original team clashes with present-day heroes and struggles over whom to trust. After Battle of the Atom, a new alliance changes where the students belong.|Out of Their Depth / All-Different|Kitty Pryde, Jean Grey
The Shi'ar put young Jean on trial for the future Phoenix's crimes, drawing in the Guardians. Back on Earth, the team's conflict with the future Brotherhood continues.|The Trial of Jean Grey / One Down|Jean Grey, Guardians of the Galaxy
A journey into the Ultimate universe brings the original team into unfamiliar territory. The collection continues through the Utopians chapters, with Black Vortex material embedded in the larger run.|The Ultimate Adventure / The Utopians|Miles Morales, Jean Grey
Cyclops and Emma Frost launch a public-facing X-Men team while a supposed cure threatens mutant identity. A second crisis turns the school's training system into a dangerous adversary.|Gifted / Dangerous|Cyclops, Emma Frost, Kitty Pryde
Psychological attacks fracture the team before its confrontation with Breakworld. The closing Whedon stories turn a prophecy and a weapon aimed at Earth into a personal crisis for Kitty.|Torn / Unstoppable|Kitty Pryde, Colossus, Emma Frost
The Phoenix's return divides the Avengers and X-Men over Hope Summers and mutantkind's future. Attempts to control the force escalate a rescue dispute into a world-changing conflict.|Avengers vs. X-Men|Avengers, Hope Summers, Cyclops
The Chaos King's assault releases dead mutants back into the world. Thunderbird, Banshee and fallen allies face a threat that reaches beyond death; companion chapters expand the event's supernatural conflict.|Chaos War: resurrected X-Men and companion tie-ins|Thunderbird, Banshee, Moira MacTaggert
Cyclops and Emma's new school policies divide the students into rival squads. Hauntings, dangerous powers, a forbidden relationship and the Hellions' vacation test friendships and loyalties.|Choosing Sides / Haunted / X-Posed / Hellions|Cyclops, Emma Frost, Dani Moonstar, New Mutants, Hellions, Prodigy
Cable's arrival shatters Xavier's plans, and Bishop builds a new team as Apocalypse approaches. These late Ultimate stories lead into Magneto's disaster in Ultimatum, with Wolverine's Hulk confrontation also collected.|Cable / Sentinels / Apocalypse / Ultimatum|Cable, Bishop, Apocalypse, Magneto, Wolverine, Hulk
The Ultimate X-Men and Fantastic Four meet in a crossover involving threats to both teams. The companion handbook material introduces the people and organizations of their shared universe.|Ultimate X-Men / Fantastic Four crossover|Fantastic Four
Cyclops's outlaw school faces Sentinels, Dormammu and S.H.I.E.L.D. The full Bendis collection includes Xavier's will and the Battle of the Atom crossover that brings future mutants into the dispute.|Revolution / Broken / Battle of the Atom / Xavier's will|Cyclops, Emma Frost, Magneto, Magik, Dormammu
Beast and Abigail Brand defend S.W.O.R.D. before Gillen's X-Men confront Breakworld and an empowered Juggernaut. The Extinction Team era then leads through Tabula Rasa and the Phoenix war into its consequences.|S.W.O.R.D. / Fear Itself / Extinction Team / AVX: Consequences|Beast, Abigail Brand, Cyclops, Magneto, Magik, Juggernaut
Wolverine's loss leaves the school facing questions about how to carry on his work. The students and faculty must decide what his legacy means for their own futures.|Death of Wolverine: school aftermath|Wolverine
Kid Omega challenges Wolverine's authority by trapping him in a mental prison. The struggle over the Jean Grey School becomes a fight inside Logan's own mind.|Alpha & Omega|Wolverine, Kid Omega
After Schism, Wolverine opens a new school in Westchester. The young Hellfire Club attacks almost immediately, testing whether the staff can protect its students through even the first days.|Opening the Jean Grey School|Wolverine, Hellfire Club
An apparent pregnancy sends a miniature rescue team into Kitty's bloodstream. Meanwhile, Wolverine and Quentin gamble for the school's finances as Brood trouble threatens everyone back home.|School troubles / Brood invasion / space casino|Kitty Pryde, Beast, Iceman, Rachel Summers, Wolverine, Kid Omega, Broo, Sabretooth, Angel
The Avengers conflict divides Wolverine's loyalties and the school's students. Cosmic attacks and a confrontation between Iceman and Red Hulk accompany the faculty's difficult choice of sides.|Avengers vs. X-Men: divided loyalties|Wolverine, Cyclops, Iceman, Red Hulk, Kid Gladiator, Warbird
As Phoenix power corrupts Cyclops's allies, Wolverine's role in the war becomes clearer. Kitty must still keep a school running with much of its faculty absent and danger on the doorstep.|Avengers vs. X-Men: school under siege|Wolverine, Kitty Pryde, Doop, Toad, Husk
A critically injured student draws the faculty into a search for the attacker. Storm joins the school before Frankenstein's Murder Circus turns the teachers against the children they protect.|Frankenstein's Murder Circus|Storm, Wolverine, Iceman, Rachel Summers
A field trip to the Savage Land goes wrong when Dog Logan takes control. The students must cope without their teacher, while a future-looking chapter explores what the school could become.|Savage Land / Dog Logan / school of the future|Wolverine, Dog Logan
Missing students push Wolverine and Rachel toward the new Hellfire Club. Beast seeks help for Broo as the school's long-running conflict with its enemies erupts into the Hellfire Saga.|The Hellfire Saga|Wolverine, Rachel Summers, Beast, Broo, Hellfire Club
The Jean Grey School reaches a turning point as students and teachers consider life beyond their familiar routines. These final Aaron chapters close this version of the school's story.|School year finale / graduation|Wolverine
Cyclops prepares to stop an out-of-control Wolverine, backed by Magneto and Namor. A birthday celebration adds another dangerous encounter to Logan's already troubled life.|Wolverine vs. the X-Men / birthday trouble|Wolverine, Cyclops, Magneto, Namor, Avengers
The original team searches for Cyclops's missing son as Madelyne Pryor becomes the Goblin Queen. Inferno reunites X-Factor with the X-Men, while Sinister threatens the family at the center of the crisis.|X-Factor / Inferno / aftermath|X-Factor, Cyclops, Jean Grey, Beast, Madelyne Pryor, Mister Sinister
The animated-era team investigates a rehabilitation project that conceals a threat to mutants. Baron Kelly's Battleworld domain becomes the setting for this Secret Wars reinterpretation.|Warzones! / Clear Mountain|X-Men
The school reopens to a crowded new student body after Cassandra Nova's defeat. Omega Red, the Fenris twins and Dracula bring fresh trouble to this cartoon-inspired world.|The World Is a Vampire|Omega Red, Dracula, Fenris
The X-Men provide security at Lila Cheney's music festival and become targets themselves. Mutant threats intrude on a concert intended to bring people together.|Lilapalooza|Lila Cheney
The nineties team establishes Krakoa decades ahead of its familiar history. A secret resurrection power and the founders' hidden knowledge reshape this alternate version of the mutant nation.|House of XCII|Professor X, Magneto
Battleworld adventures give way to a reopened school, a music festival and an early Krakoan nation. This larger collection combines the three smaller X-Men '92 phases.|Warzones! / The World Is a Vampire / Lilapalooza / House of XCII|Professor X, Cyclops, Storm, Wolverine, Rogue, Gambit, Jubilee, Lila Cheney, X-Force
The animated team faces new threats while Scott and Jean prepare for a major change in their lives. Sabretooth's attack and a concealed enemy set the stage for the television continuation.|X-Men '97 prelude: Great X-Pectations|Cyclops, Storm, Jean Grey, Beast, Jubilee, Rogue, Gambit, Bishop, Morph, Wolverine, Sabretooth
Jean leads the time-displaced original team under Magneto's mentorship. Old distrust complicates the mission to protect mutants and bring criminals to justice.|Strangest|Jean Grey, Cyclops, Iceman, Angel, Beast, Magneto
Hydra's rise changes the political landscape around the young team. Jean and her allies navigate Secret Empire while Magneto pursues his own plans.|Toil and Trouble / Secret Empire|Jean Grey, Cyclops, Beast, Angel, Iceman, Magneto
Krakoa's elected heroes defend Earth against Stasis, the Children of the Vault and the Brood. The run progresses from public superheroics through the Hellfire Gala catastrophe into the struggle against Orchis.|Elected X-Men / Judgment Day / Lord of the Brood / Fall of X|Cyclops, Jean Grey, Rogue, Synch, Polaris, Sunfire, Kitty Pryde
Krakoa elects a team to protect the planet it shares with humanity. New threats include the High Evolutionary, Cordyceps Jones and Doctor Stasis, while Captain Krakoa poses a mystery of his own.|Krakoa's elected X-Men|Cyclops, Jean Grey, Sunfire, Rogue, Synch, Polaris, High Evolutionary
Doctor Stasis escalates his attack as Captain Krakoa's secrets come into focus. M.O.D.O.K. and a visit to Gameworld complicate the team's efforts to serve as Earth's heroes.|Captain Krakoa / Gameworld|Doctor Stasis, M.O.D.O.K.
Judgment Day tests the elected X-Men's choices and identities. The Children of the Vault return with another evolutionary advantage as Forge undertakes a secret mission.|Judgment Day / Children of the Vault|Eternals, Forge, Children of the Vault
A distress call reveals that the Brood are killing again despite Broo's control. Meanwhile, Feilong turns Stark technology toward a new generation of Sentinels for Orchis.|Lord of the Brood / Orchis preparations|Broo, Feilong
The Hellfire Gala's destruction drives Kitty into her Shadowkat identity. Emma's marriage, Cyclops's captivity and a Latverian rival team unfold as the remaining mutants fight to survive.|Fall of X / Shadowkat|Kitty Pryde, Emma Frost, Iron Man, Cyclops, Juggernaut, Firestar, Doctor Doom
Synch and Talon face the High Evolutionary as Orchis presses its campaign. Nimrod's threat and the alliance of Kate and Illyana form part of the closing battle for Krakoa's heroes.|Fall of the House of X companion chapters|Synch, Talon, High Evolutionary, Nimrod, Kitty Pryde, Magik
Cyclops leads a new team from a factory in Alaska after Krakoa's fall. An alien attack, the headquarters' history and the returning Upstarts test their place in the new world.|Homecoming|Cyclops, Beast, Magneto, Psylocke, Kid Omega, Temper, Magik, Juggernaut, Trevor Fitzroy
Doug Ramsey's new role as Revelation brings a difficult choice to Cyclops's team. Young mutants pursue the Upstarts while a Hellfire Vigil commemorates the destruction of Krakoa's dream.|The Hellfire Vigil / Revelation's rise|Doug Ramsey, Cyclops, Upstarts
The aftermath of Revelation leaves a displaced X-Man and a question about a switched identity. A revived 3K, O.N.E. and the Creationist create further dangers in the present.|Age of Revelation aftermath / Creationist|Creationist
The Summers family establishes a lunar home while Krakoa meets new threats and rival powers. Diplomacy, an unusual island and Mystique's personal demands shape the new era.|Dawn of X / Summer House / mutant diplomacy|Cyclops, Jean Grey, Mystique
The Crucible raises difficult questions about resurrection and identity. Brood conflict and Empyre's consequences bring spacefaring allies and unwanted visitors into the mutants' world.|Crucible / Brood conflict / Empyre|New Mutants, Starjammers, Shi'ar Imperial Guard
After X of Swords, Krakoa faces new decisions and a request for help from the Shi'ar. The Vault and Nimrod return as threats before the transition to an elected team.|Reign of X / Children of the Vault / Nimrod|Cyclops, Storm, Jean Grey, Nimrod
With mutants facing extinction after M-Day, Apocalypse offers a brutal vision of survival. Cable and Deadpool investigate the warning signs as new Horsemen emerge.|Blood of Apocalypse / Decimation|Apocalypse, Cable, Deadpool
Storm's Lifedeath accompanies relationship crises, Morlock trouble and Rachel's arrival. A separate Japan adventure transforms Kitty and Wolverine's partnership.|Lifedeath / Kitty Pryde and Wolverine|Storm, Cyclops, Madelyne Pryor, Wolverine, Kitty Pryde, Rogue, Colossus, Mystique, Rachel Summers
The newly divided blue and gold teams encounter Omega Red, violent attacks and Bishop's arrival from the future. Ghost Rider joins the New Orleans Brood chapters in this broad Epic edition.|Bishop's Crossing / Omega Red / Brood in New Orleans|Bishop, Wolverine, Colossus, Ghost Rider, Gambit
The Legacy virus spreads as Magneto returns with an offer of sanctuary. The confrontation changes Wolverine's life, while Gambit's solo story explores New Orleans' rival guilds.|Fatal Attractions / Gambit's guilds|Magneto, Wolverine, Professor X, Gambit, Forge
The Morlocks' arrival and Rogue's recruitment accompany major changes in the team's relationships. God Loves, Man Kills and Wolverine's Japan miniseries provide two central companion stories.|God Loves, Man Kills / Wolverine in Japan / Morlocks|Kitty Pryde, Colossus, Rogue, Callisto, Cyclops, Madelyne Pryor, Wolverine
Arcade, Doctor Doom and Magneto challenge the team as Kitty's Fairy Tale supplies a very different adventure. Rogue's debut, a Fantastic Four team-up and Savage Land material broaden the collection.|I, Magneto / Kitty's Fairy Tale / Rogue's debut|Magneto, Kitty Pryde, Rogue, Fantastic Four, Spider-Woman, Dazzler, Doctor Doom
Colossus's family becomes entangled with the Soul Skinner while the Acolytes renew Magneto's shadow. Betsy's identity and a spreading mutant illness lead toward further upheaval.|Legacies / Soul Skinner / Legacy virus|Colossus, Magik, Psylocke, Mastermind
The original team and current X-Men unite against the Shadow King after Cyclops makes a painful sacrifice for his son. The reunited roster launches a new era with Magneto and his Acolytes.|Muir Island Saga / Mutant Genesis|X-Factor, Cyclops, Professor X, Shadow King, Magneto
The Marauders slaughter Morlocks and leave the X-Men badly wounded. The collection follows the team's recovery and confrontations with the Fantastic Four and Avengers, plus a Spider-Man/Wolverine adventure.|Mutant Massacre: X-Men chapters / superhero confrontations|Marauders, Morlocks, Psylocke, Longshot, Wolverine, Sabretooth, Fantastic Four, Avengers, Spider-Man
Xavier recruits an international team to rescue his original students. The new X-Men's early missions lead toward Phoenix and a wider cosmic world, with additional guest adventures collected alongside.|Second Genesis / Phoenix emergence / early adventures|Professor X, Wolverine, Storm, Colossus, Nightcrawler, Banshee, Sunfire, Starjammers
The X-Men face parasitic aliens across a long space adventure with the Starjammers and Shi'ar. Dracula, Limbo and the shared past of Xavier and Magneto add darker chapters.|The Brood Saga / Limbo / Xavier and Magneto|Starjammers, Dracula, Professor X, Magneto
Jean's transformation into Dark Phoenix leads to a cosmic tragedy, followed by the threatened future of Days of Future Past. Wolverine's Wendigo encounter and related extras complete this larger edition.|Dark Phoenix Saga / Days of Future Past|Jean Grey, Wolverine
Storm and Forge reach a turning point before an apparent attack by Cable throws the mutant teams into conflict. Sinister's plans and Stryfe's secrets drive the X-Cutioner's Song crossover.|X-Cutioner's Song / preceding team chapters|Storm, Forge, Cyclops, Jean Grey, Cable, Professor X, Mister Sinister, Apocalypse, Stryfe, X-Factor, X-Force
Magneto's trial, Xavier's departure and the Storm/Cyclops leadership contest reshape the team. Asgard, Lady Deathstrike and Nimrod provide major challenges before the Mutant Massacre era.|Wounded Wolf / Asgardian Wars / leadership changes|Rachel Summers, Magneto, Professor X, Cyclops, Storm, Lady Deathstrike, Wolverine, New Mutants, Loki
Kitty returns to lead a familiar team after the Inhumans conflict. A new Brotherhood threatens New York as the X-Men recommit to protecting the public.|Back to the Basics|Kitty Pryde, Storm, Colossus, Nightcrawler, Rachel Summers, Old Man Logan
Hydra's takeover draws Kitty's team into the changing world of Secret Empire. Their public mission becomes more difficult as hostile forces control the country.|Evil Empires / Secret Empire|Kitty Pryde, Storm, Colossus, Nightcrawler, Rachel Summers, Old Man Logan
Rogue leads a rescue mission for Rachel, Havok and Polaris in an extraterrestrial war. After Schism, she and her allies face unfinished business and a choice of allegiance.|Five Miles South of the Universe / Schism aftermath|Rogue, Rachel Summers, Havok, Polaris, Magneto, Gambit
Something dangerous follows the mutants out of Age of X. Rogue and Magneto assemble a team to hunt the escaped threat after returning to Utopia.|Lost Legions / Age of X aftermath|Rogue, Magneto
Returning creators revisit gaps in earlier runs: the Summers family mystery, Apocalypse and the original X-Factor, and an embassy crisis for Havok's later team.|The Missing Links: Summers family / X-Factor stories|Cyclops, Havok, Adam-X, X-Factor, Apocalypse, Polaris, Wolfsbane, Strong Guy, Quicksilver, Multiple Man
Wolverine and Jubilee return to Japan, Sinister gathers mutant experts, and other chapters revisit the New Mutants and the road toward Excalibur. These are new stories set in earlier periods.|Mutant Mayhem: Japan / Sinister / Excalibur prelude|Wolverine, Jubilee, Lady Deathstrike, Mister Sinister, New Mutants, Apocalypse, Nightcrawler, Kitty Pryde
Wolverine's pre-X-Men missions, a return to Mojoworld and Bishop's time-travel mission revisit three different corners of mutant history. Publication order does not make these one continuous present-day adventure.|Past Meets Future: Wolverine / Mojoworld / Bishop|Wolverine, Hulk, Longshot, Kitty Pryde, Bishop
Jean Grey's cosmic power spirals into a danger to the universe. Her teammates must face the possible cost of saving someone they love in the central Dark Phoenix storyline.|Dark Phoenix Saga|Jean Grey
Three separate mutant teams endure defining losses and transformations. Apocalypse changes Angel's fate while the X-Men and New Mutants face their own sacrifices.|Fall of the Mutants|X-Factor, New Mutants, Angel, Apocalypse
Limbo's demons exploit Illyana and Madelyne Pryor to invade New York. Family secrets and Sinister's schemes compound the fight to prevent Earth and Limbo from merging.|Inferno|Magik, Madelyne Pryor, Cyclops, Mister Sinister, X-Factor, New Mutants
The first mutant birth since M-Day sparks a struggle over the child's future. Rival factions pursue the baby as the X-teams race to protect mutantkind's possible hope.|Messiah Complex|X-Factor, New X-Men
Cable protects Hope in the future while Bishop pursues them. Cyclops sends X-Force to help, only for the rescue team to encounter a trap of its own.|Messiah War|Cable, Hope Summers, Bishop, Cyclops, X-Force
Onslaught's hidden campaign becomes an open assault on the mutant teams and Earth's other heroes. The conflict brings the Avengers and Fantastic Four into a crisis with lasting consequences.|Onslaught|Avengers, Fantastic Four, Onslaught
An apparent assassination by Cable and the kidnapping of Cyclops and Jean drive three mutant teams against each other. Stryfe and Sinister manipulate the conflict toward a confrontation with Apocalypse.|X-Cutioner's Song|Cable, Cyclops, Jean Grey, Professor X, Stryfe, Mister Sinister, Apocalypse, X-Factor, X-Force
Genosha retaliates against the mutants with kidnapping, depowering and forced combat. Cameron Hodge directs the conflict as X-Men, X-Factor and New Mutants struggle to escape.|X-Tinction Agenda / earlier Genosha chapters|Cameron Hodge, X-Factor, New Mutants
Six origin spotlights revisit the formative experiences of major heroes and villains. Each chapter focuses on an individual's past rather than advancing one team storyline.|Origins: Colossus / Beast / Jean Grey / Sabretooth / Wolverine / Gambit|Colossus, Beast, Jean Grey, Sabretooth, Wolverine, Gambit
Five more origin stories explore the difficult paths toward mutant identity. These character portraits are companions to the first Origins collection, not a single chronological sequel.|Origins: Deadpool / Emma Frost / Nightcrawler / Cyclops / Iceman|Deadpool, Emma Frost, Nightcrawler, Cyclops, Iceman
Storm seeks a future for Arakko beyond permanent war. Magneto, Sunspot, Brand and Cable pursue competing plans as Vulcan's instability threatens the planet's fragile balance.|Arakko / Brotherhood / Great Ring politics|Storm, Magneto, Sunspot, Abigail Brand, Cable, Vulcan, Tarn
The Eternals' assault forces Arakko to defend itself during Judgment Day. Cable then moves against Brand's wider scheme while the Great Ring confronts Isca's place among its rulers.|Judgment Day / Brand's conspiracy|Cable, Abigail Brand, Isca, Eternals
Storm faces Xavier's questions after Magneto's death while new threats approach Arakko. The companion Heralds chapter explores Genesis, Apocalypse and the nation's older history.|Heralds of Apocalypse / Genesis War prelude|Storm, Professor X, Apocalypse, Genesis, White Sword
Genesis uses the Hellfire Gala catastrophe to launch a war on Arakko. Storm and the Brotherhood defend the planet while the Fisher King's secrets offer a possible advantage.|Genesis War / Fall of X|Storm, Genesis, Fisher King, Apocalypse, Brotherhood
Jean Grey assembles a new team in a world increasingly hostile to mutants. A rescue mission and growing public hatred push her allies into an international struggle.|The Hate Machine|Jean Grey, Nightcrawler, Namor, X-23, Gambit
An assault on Atlantis leads Jean's team toward the enemy manufacturing anti-mutant hatred. Jean confronts Cassandra Nova in the conclusion to this Red series.|Waging Peace|Jean Grey, Namor, Cassandra Nova
Apocalypse gathers the Twelve, powerful mutants whose abilities he plans to steal. The X-Men ally with Magneto in a desperate attempt to prevent his ascension.|The Twelve|Apocalypse, Professor X, Cyclops, Jean Grey, Storm, Iceman, Sunfire, Polaris, Cable, Bishop, Mikhail Rasputin, Magneto
Distorted timelines follow the Twelve crisis as Apocalypse seeks a reality that suits him. The collection continues into the search for Cyclops and the struggle over his identity.|Ages of Apocalypse / The Search for Cyclops|Apocalypse, Cyclops, Cable, Wolverine, Hulk, Machine Man, Deathlok
Wedding chapters mark major relationships across several eras: Scott and Jean, Northstar and Kyle, Storm and T'Challa, and the surprise-filled Gold ceremony. These are selected celebration issues, not complete surrounding runs.|X-Men weddings|Cyclops, Jean Grey, Northstar, Storm, Black Panther, Kitty Pryde, Colossus
Stories revisit the earlier history of Apocalypse's alternate world, then follow its survivors across other adventures. Magneto, Rogue and Weapon X's relationships receive particular attention.|Age of Apocalypse: historical and companion stories|Magneto, Rogue, Gambit, Cyclops, Havok, Blink, Colossus, Sabretooth, Wolverine, Mariko Yashida, X-Man
A defeated mutant resistance gives way to the X-Terminated in the Age of Apocalypse. The conflict with Weapon X eventually draws multiple universes into X-Termination.|Age of Apocalypse revival / X-Termination|Jean Grey, Sabretooth, Wolverine, Cyclops, X-Terminated
Return visits explore Apocalypse's world after its original ending. Sinister, Exiles adventures and alternate possibilities complicate what victory meant for its survivors.|Age of Apocalypse: returns and alternate outcomes|Magneto, Mister Sinister, Blink, Sabretooth, Exiles, X-Man
Xavier's death in the past creates a world dominated by Apocalypse. Bishop's memories offer Magneto's resistance a chance to restore history as the many parallel missions begin.|Legion Quest / Age of Apocalypse: Alpha|Professor X, Apocalypse, Bishop, Magneto
The resistance's missions continue across Apocalypse's empire. Nightcrawler seeks Destiny, the Summers brothers clash and Nate Grey confronts the forces behind his creation.|Age of Apocalypse: Reign|Nightcrawler, Destiny, Cyclops, Havok, Dark Beast, X-Man
The parallel missions of Magneto's resistance reach their closing chapters. X-Men Omega brings the original Age of Apocalypse event to its final confrontation.|Age of Apocalypse: Omega|Magneto
Krakoa's early line-wide stories continue across the X-Men, satellite teams and the Fantastic Four dispute. Empyre, Giant-Size character chapters and the opening Hellions material accompany the second Dawn of X phase.|Dawn of X / X-Men–Fantastic Four / Empyre|Fantastic Four, New Mutants, Marauders, Cable, X-Force, Excalibur, Hellions, Wolverine, X-Factor, Nightcrawler, Magneto, Fantomex, Storm
Doug Ramsey's Revelation rules a transformed future that the surviving X-Men hope to change. Opening chapters follow Emma and Tony, Laura's new identity, Binary and Cloak or Dagger through this alternate world.|Age of Revelation: opening / Amazing X-Men / companion series|Doug Ramsey, Emma Frost, Iron Man, X-23, Binary, Cloak, Dagger
Revelation's court and rivalries develop alongside stories of displaced mutants. A radioactive Spider-Man, Rogue and Storm's conflict, the Expatriates and the Last Wolverine reveal different parts of this future.|Book of Revelation / Radioactive Spider-Man / companion series|Doug Ramsey, Fabian Cortez, Spider-Man, Rogue, Storm, Ms. Marvel, Bronze, Melee, Rift
The remaining Haven House mutants, Undeadpool and transformed Avengers face Revelation's world. Sinister's strike team and Quentin's spy network lead into the event's collected finale.|World of Revelation / Unbreakable X-Men / Age of Revelation Finale|Deadpool, Avengers, Mister Sinister, Kid Omega
Rescue missions in Weirdworld and Nightcrawler's mind lead into a journey to a future ruled by Apocalypse. This edition collects the Extraordinary team's part of Apocalypse Wars.|Apocalypse Wars: Extraordinary X-Men|Old Man Logan, Colossus, Iceman, Magik, Storm, Jean Grey, Nightcrawler, Apocalypse
Apocalypse and Dracula renew an ancient feud in nineteenth-century London. This historical villain confrontation does not establish an appearance by the modern X-Men team.|Apocalypse vs. Dracula|Apocalypse, Dracula
Future mutants arrive with a warning about the displaced original X-Men. Multiple generations and rival teams collide over whether the young heroes should remain in the present.|Battle of the Atom|X-Men
Bishop pursues escaped convicts into the present and meets the heroes he grew up idolizing. The gold team's early missions also explore Colossus's family and Storm and Forge's relationship.|Bishop's Crossing: extended gold-team chapters|Bishop, Gambit, Colossus, Storm, Forge, Cyclops, Jean Grey'''

def main():
    lock=(ROOT/'data/enrichment.lock').open('a+b');lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    ids=json.loads((ROOT/'data/deep-batch-04.json').read_text());rows=ROWS.splitlines();assert len(ids)==len(rows)==100
    catalog=json.loads((ROOT/'public/catalog.json').read_text(encoding='utf-8'))['books'];by={b['isbn']:b for b in catalog}
    payload=json.loads((ROOT/'public/enrichment.json').read_text(encoding='utf-8'));before=copy.deepcopy(payload['books'])
    path=ROOT/'data/editorial-enrichment.json';editorial=json.loads(path.read_text(encoding='utf-8'));notes={}
    for i,(isbn,row) in enumerate(zip(ids,rows),1):
        b=by[isbn];d=copy.deepcopy(before.get(b['id'],{}));source=d.get('pagesSource') or b['catalogUrl'];summary,story,guests=row.split('|')
        for key in ['level','automation','review']:d.pop(key,None)
        d.update(summary=summary,pages=d.get('pages'),pagesSource=source,coverSource=d.get('coverSource',source),checkedAt=datetime.date.today().isoformat(),editorialBatch='deep-04',stories=[dict(title=story,coverage='Story highlights; see edition and reading notes')],characters=[dict(name=n,role='Featured in cited synopsis; not a complete cameo index',source=source) for n in dict.fromkeys(['X-Men']+[g.strip() for g in guests.split(',') if g.strip()])],issueKeys=[],startingPoint=False)
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
    report=dict(batch='deep-04',records=100,reviews=sum(bool(d.get('review')) for d in notes.values()),missingPages=sum(not d.get('pages') for d in notes.values()),remainingXMen=sum('x-men' in b['title'].lower() and (b['id'] not in payload['books'] or payload['books'][b['id']].get('level')=='basic') for b in catalog),notes='100 researched records; previous work preserved. Edition uncertainties and missing ratings remain explicit.')
    write_json(ROOT/'data/deep-batch-04-audit.json',report);print(json.dumps(report))

def configure(n,by,ids,before):
    def cite(i,url,label='Additional synopsis / collection contents; not used for this ISBN page count'):
        if url not in [s['url'] for s in n[i]['sources']]:n[i]['sources'].append(dict(label=label,url=url))
        for c in n[i]['characters']:c['source']=url
    def prior(i,isbns):
        for isbn in isbns:
            for source in before[by[isbn]['id']]['sources']:
                if 'roundup' not in source['url']:cite(i,source['url'],'Publisher source for included storyline; edition extras may differ')
    def issues(i,*specs):
        n[i]['issueKeys']=[key for series,year,a,b in specs for key in group(series,year,a,b)]
    def seq(indices,name,series,year,ranges,positions=None):
        for p,(i,(a,b)) in enumerate(zip(indices,ranges),1):
            pos=positions[p-1] if positions else p
            issues(i,(series,year,a,b));n[i]['readingPath']=run(name,pos,'Follow this series in volume order. Crossovers and omitted issues may need separate collections.');n[i]['startingPoint']=pos==1
    def note(i,text):n[i]['readingPath']['note']=text
    def caution(i,text):n[i]['contentsNote']=text;n[i]['checks']['edition']=text
    seq([1,2,3,4],'All-New X-Men — Bendis (2012)','All-New X-Men',2012,[(1,10),(11,15),(22,30),(31,41)],[1,3,4.5,6])
    n[2]['issueKeys']+=group('All-New X-Men',2012,18,21)
    n[3]['issueKeys']+=group('Guardians of the Galaxy',2013,11,13)
    for i in range(1,5):n[i]['readingPath']['alternative']=True
    prior(1,['9781302013608','9781302013615']);prior(2,['9781302368654','9781302377571']);prior(3,['9780785168300','9781302392925']);prior(4,['9781302478865','9781302480783'])
    cite(3,'https://www.marvel.com/comics/collection/53307/all-new_x-men_vol_3_hc_hardcover')
    note(2,'Larger alternative to Out of Their Depth and All-Different. Omits 16–17; use Battle of the Atom between 15 and 18.')
    note(3,'Larger edition includes The Trial of Jean Grey and One Down. Publisher confirms 22–30 and Guardians 11–13; do not infer this range for the smaller One Down edition.')
    note(4,'Combines later run chapters. Issues 38–39 are Black Vortex tie-ins; the complete event requires other titles.')
    seq([5,6],'Astonishing X-Men — Whedon & Cassaday (2004)','Astonishing X-Men',2004,[(1,12),(13,24)],[1,3])
    for i in [5,6]:n[i]['readingPath']['alternative']=True
    prior(5,['9780785170037','9780785170044']);prior(6,['9780785170051','9780785170068'])
    n[6]['issueKeys']+=group('Giant-Size Astonishing X-Men',2008,1,1)
    cite(6,'https://www.marvel.com/comics/collection/40928/')
    note(6,'Larger alternative covering Torn and Unstoppable, with the Giant-Size conclusion. Not the 1995 Age of Apocalypse series.')
    prior(7,['9780785179948']);issues(7,('Avengers vs. X-Men',2012,0,12));note(7,'Main Avengers vs. X-Men event. Companion and VS books add tie-ins rather than replacing it.')
    cite(8,'https://marvel.fandom.com/wiki/Chaos_War%3A_X-Men_TPB_Vol_1_1','Marvel Database · collection contents and publisher solicitation')
    cite(8,'https://uncannyxmen.net/comics/issue/chaos-war-x-men-1','UncannyXMen.net · issue synopsis and appearances')
    issues(8,('Chaos War: X-Men',2010,1,2),('Chaos War: Alpha Flight',2010,1,1),('Chaos War: God Squad',2010,1,1),('Chaos War: Chaos King',2010,1,1));note(8,'Tie-in anthology to Chaos War, not the main event miniseries. Characters include returned dead mutants.')
    cite(9,'https://www.hoopladigital.com/comic/19714672','Hoopla · digital collection synopsis and contents')
    issues(9,('New X-Men',2004,1,15),('New X-Men: Hellions',2005,1,4));n[9]['readingPath']=run('New X-Men — Academy X (2004)',1,'Alternative to Choosing Sides, Haunted and X-Posed, plus Yearbook and Hellions. Childhood’s End follows.',True)
    cite(10,'https://prhcomics.com/book/?isbn=9781302963620');note(10,'Third original-universe omnibus. Includes late Ultimate X-Men, Ultimatum and companion stories; not Peach Momoko’s universe.')
    issues(10,('Ultimate X-Men',2001,75,100),('Ultimate Wolverine vs. Hulk',2005,1,6),('Ultimatum',2008,1,5),('Ultimatum: X-Men Requiem',2009,1,1))
    caution(10,'Synopsis and contents checked against the matching-title print omnibus; this digital ISBN’s extras and page count are not independently confirmed. Crossover annuals are not indexed.')
    cite(11,'https://uncannyxmen.net/comics/issue/ultimate-x4-1','UncannyXMen.net · crossover synopsis and placement')
    cite(11,'https://www.comics.org/issue/304240/','Grand Comics Database · crossover part 2 and reprints')
    n[11]['summary']='The theft of Cerebro brings the Ultimate X-Men and Fantastic Four together against Rhona Burchill, the Mad Thinker. Her attempt to expand her intelligence creates a threat that neither team can ignore.'
    issues(11,('Ultimate X-Men/Fantastic Four',2006,1,1),('Ultimate Fantastic Four/X-Men',2006,1,1));note(11,'Ultimate X4 crossover after Ultimate X-Men 65. Separate from the 2008 crossover annuals and Ultimatum tie-ins. Handbook extras are not indexed.')
    cite(12,'https://prhcomics.com/book/?isbn=9781302966454')
    issues(12,('Uncanny X-Men',2013,1,14),('Uncanny X-Men',2013,16,35),('Uncanny X-Men',2013,600,600),('All-New X-Men',2012,16,17),('Wolverine & the X-Men',2011,36,37),('X-Men: Battle of the Atom',2013,1,2),('X-Men',2013,5,6),('Uncanny X-Men Annual',2014,1,1),('All-New X-Men Annual',2014,1,1))
    n[12]['issueKeys']+=['Uncanny X-Men (2013) #15.INH'];n[12]['readingPath']=run('Uncanny X-Men — Brian Michael Bendis (2013)',1,'Omnibus alternative to six smaller volumes; includes Battle of the Atom and the otherwise missing issue 25.',True)
    caution(12,'Matching-title publisher omnibus contents checked; digital ISBN page count remains unavailable. Includes 15.INH, not an ordinary issue 15.')
    cite(13,'https://www.penguinrandomhouse.com/books/802681/uncanny-x-men-by-kieron-gillen-omnibus-by-kieron-gillen/')
    prior(13,['9781302508715','9781302519797'])
    issues(13,('S.W.O.R.D.',2009,1,5),('Uncanny X-Men',1963,535,544),('Uncanny X-Men',2011,1,20),('AVX: Consequences',2012,1,5));n[13]['issueKeys']+=['Uncanny X-Men (1963) #534.1']
    n[13]['readingPath']=run('Uncanny X-Men — Gillen Complete Collection',1,'Omnibus alternative spanning both Complete Collection volumes. Includes the full main Gillen series, not the entire Avengers vs. X-Men event.',True)
    caution(13,'Matching-title publisher omnibus and smaller collected editions checked. Digital page count and additional extras remain unconfirmed.')
    cite(14,'https://www.marvel.com/comics/collection/48948/')
    n[14]['summary']='Melita’s return and Quentin’s birthday complicate life at the school before Wolverine’s death. After the tragedy, his will and the stories his friends tell force the community to consider how to preserve his legacy.'
    seq([14],'Wolverine & the X-Men — Jason Latour (2014)','Wolverine & the X-Men',2014,[(7,12)],[2]);note(14,'After Tomorrow Never Learns. Includes Death of Wolverine aftermath, not the four-issue main event. Review row lists only three issues, so its score is withheld.')
    issues(15,('Wolverine & the X-Men: Alpha & Omega',2012,1,5));note(15,'Optional early Jean Grey School companion miniseries; not a numbered volume of Aaron’s main series.')
    seq(list(range(16,24)),'Wolverine & the X-Men — Jason Aaron (2011)','Wolverine & the X-Men',2011,[(1,4),(5,8),(9,13),(14,18),(19,24),(25,29),(30,35),(38,42)])
    n[23]['issueKeys']+=group('Wolverine & the X-Men Annual',2013,1,1)
    cite(23,'https://www.marvunapp.com/Appendix8/anole.htm','Marvel Appendix · issue 42 graduation reference')
    for i in [18,19]:note(i,'Avengers vs. X-Men period. Follow the main event alongside these school-focused tie-ins.')
    note(23,'Final Aaron volume. Issues 36–37 are in Battle of the Atom, between volumes 7 and 8. The 2014 Latour series follows separately.')
    issues(24,('Wolverine',2010,6,9));n[24]['issueKeys']+=['Wolverine (2010) #5.1'];note(24,'Continuation of Wolverine’s 2010 solo run; not a school-series volume.')
    cite(25,'https://prhcomics.com/book/?isbn=9781302966096')
    issues(25,('X-Factor',1986,27,50),('X-Factor Annual',1986,3,4),('X-Terminators',1988,1,4),('Uncanny X-Men',1963,240,243),('New Mutants',1983,76,76),('Fantastic Four',1961,342,342))
    note(25,'Second Original X-Men omnibus: issues 27–50 and Inferno-era material. Not the later 51–70 collection. Overlaps Inferno Milestones; partial backups are not indexed.')
    caution(25,'Matching-title publisher edition contents confirmed; exact digital page count remains unconfirmed.')
    seq([26,27,28,29],'X-Men ’92 — cartoon-inspired alternate continuity','X-Men ’92',2016,[(1,4),(1,5),(6,10),(1,5)],[0,1,2,3])
    issues(26,("X-Men '92",2015,1,4));issues(27,("X-Men '92",2016,1,5));issues(28,("X-Men '92",2016,6,10));issues(29,("X-Men '92: House of XCII",2022,1,5))
    note(26,'Secret Wars Battleworld miniseries, followed by the 2016 series. Separate from the animated television continuity.');note(29,'A later alternate Krakoa take; not the original House of X/Powers of X event.')
    n[30]['issueKeys']=n[26]['issueKeys']+n[27]['issueKeys']+n[28]['issueKeys']+n[29]['issueKeys'];n[30]['readingPath']=run('X-Men ’92 — cartoon-inspired alternate continuity',0,'Alternative collecting the 2015 miniseries, the 2016 run and House of XCII.',True)
    issues(31,("X-Men '97",2024,1,4));note(31,'Official prelude to the animated X-Men ’97 series; not a sequel volume of the X-Men ’92 comics.')
    seq([32,33],'X-Men Blue — Cullen Bunn (2017)','X-Men: Blue',2017,[(1,6),(7,12)])
    note(33,'Secret Empire tie-in period. Main Secret Empire and later Blue volumes are separate collections.')
    cite(34,'https://www.comicexpress.de/kataloge/Marvel%20Previews%20April%202025.pdf','Marvel publisher catalog · matching-title omnibus contents')
    issues(34,('X-Men',2021,1,34),('X-Men Annual',2022,1,1),('Planet-Size X-Men',2021,1,1),('X-Men: Hellfire Gala',2022,1,1),('X-Men: Hellfire Gala',2023,1,1),('X-Men Unlimited: X-Men Green',2022,1,2))
    n[34]['readingPath']=run('X-Men — Gerry Duggan (2021)',1,'Omnibus alternative to volumes 1–6, adding Galas and companion material. The wider Krakoa finale requires other series.',True)
    caution(34,'Matching-title publisher print omnibus contents checked; exact digital extras/page count still need confirmation. Review row lists 40 issues rather than this 41-issue listing, so no omnibus score is attached.')
    seq(list(range(35,41)),'X-Men — Gerry Duggan (2021)','X-Men',2021,[(1,6),(7,12),(13,18),(19,24),(25,29),(30,34)])
    note(35,'After the 2021 Hellfire Gala and Planet-Size X-Men; the elected team begins here.');note(37,'Judgment Day tie-ins plus the Vault mission; read the main event separately.');note(39,'After the 2023 Hellfire Gala attack. Companion Invincible Iron Man chapters tell more of the wedding storyline.');note(40,'Read alongside Fall of the House of X/Rise of the Powers of X. This is the Duggan run’s final volume, not the whole Krakoa conclusion.')
    seq([41,42,43],'X-Men — Jed MacKay (2024)','X-Men',2024,[(1,7),(19,22),(23,25)],[1,3,4])
    n[42]['issueKeys']+=group('X-Men: Hellfire Vigil',2025,1,1);n[43]['issueKeys']+=group('X-Men Annual',2026,1,1)
    caution(41,'ISBN source says issues 1–7; review collection row says six issues. Score withheld rather than mixing editions.')
    note(42,'Volume 3; issues 8–18 and Raid on Graymalkin occur before this collection. Leads toward Age of Revelation.');note(43,'After the Age of Revelation event, whose story does not simply run through X-Men 22–23. Includes Annual 2026.')
    seq([44,45,46],'X-Men — Jonathan Hickman (2019)','X-Men',2019,[(1,6),(7,11),(16,20)])
    note(44,'Start with House of X/Powers of X for Krakoa’s foundation. This volume begins the ongoing series.');note(45,'Includes Empyre-era chapters; the event and Empyre: X-Men tie-in are separate.');note(46,'Issues 12–15 are in X of Swords. Read that crossover between volumes 2 and 3; the Hellfire Gala follows this run.')
    issues(47,('X-Men',1991,177,187),('Cable & Deadpool',2004,26,27));note(47,'After House of M/M-Day. Includes Decimation aftermath and the Blood of Apocalypse conclusion to Milligan’s run.')
    classic={48:(176,188),49:(281,288),50:(301,306),51:(168,175),52:(144,153),53:(297,300),54:(278,280),55:(211,219),56:(94,110),57:(154,167),58:(129,143),59:(289,296),60:(199,210),68:(129,137),69:(225,227),70:(239,243),73:(333,337),74:(294,297),75:(270,272),100:(281,293)}
    for i,(a,b) in classic.items():
        issues(i,('Uncanny X-Men',1963,a,b));n[i]['readingPath']=run('X-Men — classic era collections',a,'Ordered by main Uncanny chapter. These editions overlap and do not form a complete continuous run.',True)
    n[48]['issueKeys']+=group('Kitty Pryde and Wolverine',1984,1,6)
    n[49]['issueKeys']+=group('X-Men',1991,4,9)+group('Ghost Rider',1990,26,27)+group('X-Men Annual',1970,16,16)+group('X-Men Annual',1992,1,1)
    n[50]['issueKeys']+=group('X-Men',1991,24,25)+group('X-Men Unlimited',1993,2,2)+group('Wolverine',1988,75,75)+group('Gambit',1993,1,4)
    note(50,'Fatal Attractions chapters and surrounding stories. This Epic omits some event tie-ins, including X-Factor 92, X-Force 25 and Excalibur 71; it is not the complete event checklist.')
    n[51]['issueKeys']+=group('X-Men Annual',1970,7,7)+group('Wolverine',1982,1,4)+['Marvel Graphic Novel (1982) #5']
    note(51,'Overlaps Uncanny Masterworks Volume 9, including God Loves, Man Kills and the Wolverine miniseries. Choose an edition rather than reading both as successive steps.')
    n[52]['issueKeys']+=group('X-Men Annual',1970,5,5)+group('Avengers Annual',1967,10,10)+group('Bizarre Adventures',1981,27,27)
    n[53]['issueKeys']+=group('X-Men',1991,17,23)+group('X-Men Annual',1970,17,17)+group('X-Men Unlimited',1993,1,1)+group("Stryfe's Strike File",1993,1,1)
    n[54]['issueKeys']+=group('X-Factor',1986,65,70)+group('X-Men',1991,1,3)+group('X-Men Annual',1970,15,15)
    n[55]['issueKeys']+=group('Spider-Man versus Wolverine',1987,1,1)+group('Fantastic Four vs. X-Men',1987,1,4)+group('X-Men vs. Avengers',1987,1,4)
    note(55,'Collects the Uncanny side of Mutant Massacre and later mini-series, not every X-Factor, Thor or Power Pack crossover chapter.')
    n[56]['issueKeys']+=group('Giant-Size X-Men',1975,1,1)+group('Marvel Team-Up',1972,53,53)+group('Marvel Team-Up',1972,69,70)+group('Marvel Team-Up Annual',1976,1,1)+group('Iron Fist',1975,14,15)
    caution(56,'Publisher blurb mistakenly names Warpath among the 1975 recruits; that appearance is not asserted. Contents follow the explicitly listed issues.')
    n[57]['issueKeys']+=group('X-Men Annual',1970,6,6)+group('Special Edition X-Men',1983,1,1)
    note(57,'Spans the Brood story across Masterworks 7–8 and explicitly includes issue 160, absent from the checked Masterworks 8 listing.')
    n[58]['issueKeys']+=group('X-Men Annual',1970,4,4)+group('Marvel Treasury Edition',1974,26,27)+group('Phoenix: The Untold Story',1984,1,1)
    note(58,'Larger alternative containing both Dark Phoenix 129–137 and Days of Future Past 141–142. Includes surrounding chapters and extras.')
    n[59]['issueKeys']+=group('X-Men',1991,10,16)+group('X-Factor',1986,84,86)+group('X-Force',1991,16,18)
    n[60]['issueKeys']+=group('X-Men Annual',1970,9,10)+group('New Mutants Special Edition',1985,1,1)+group('Marvel Fanfare',1982,33,33)
    seq([61,62],'X-Men Gold — Marc Guggenheim (2017)','X-Men Gold',2017,[(1,6),(7,12)]);note(62,'Secret Empire period. This team’s tie-ins do not replace the main event.')
    seq([64,63],'X-Men Legacy — Mike Carey (2008)','X-Men Legacy',2008,[(250,253),(254,260)],[250,254]);note(64,'After Age of X. Continue with Five Miles South of the Universe.');note(63,'Follows Lost Legions and reaches the Schism-era choice of teams.')
    seq([65,66],'X-Men Legends — 2021 anthology','X-Men Legends',2021,[(1,6),(7,12)])
    for i in [65,66]:note(i,'Publication-volume order only. Separate stories revisit different historical runs; not a single timeline.')
    issues(67,('X-Men Legends',2022,1,6));note(67,'The 2022 relaunch, separate from 2021 issues 1–12. Individual stories belong to different historical periods.')
    n[68]['startingPoint']=True;note(68,'Self-contained central Dark Phoenix arc, 129–137. Larger Fate of the Phoenix and Masterworks editions overlap.')
    n[69]['issueKeys']+=group('New Mutants',1983,59,61)+group('X-Factor',1986,24,26);note(69,'Three parallel team stories grouped as Fall of the Mutants, not a chapter-by-chapter team crossover.')
    n[70]['issueKeys']+=group('X-Terminators',1988,1,4)+group('X-Factor',1986,35,39)+group('New Mutants',1983,71,73);note(70,'Main mutant Inferno stories; other Marvel tie-ins and earlier setup are outside this collection.')
    issues(71,('X-Men: Messiah Complex',2007,1,1),('Uncanny X-Men',1963,492,494),('X-Men',1991,205,207),('New X-Men',2004,44,46),('X-Factor',2005,25,27))
    n[71]['readingPath']=run('X-Men — Messiah storyline',1,'Messiah Complex precedes Cable’s protection of Hope, Messiah War and eventually Second Coming.')
    issues(72,('X-Force/Cable: Messiah War',2009,1,1),('Cable',2008,13,15),('X-Force',2008,14,16));n[72]['readingPath']=run('X-Men — Messiah storyline',2,'After Messiah Complex and early Cable (2008); Second Coming concludes the wider Hope storyline later.')
    n[73]['issueKeys']+=group('X-Men',1991,53,57)+group('Cable',1993,35,35)
    caution(73,'Publisher listing has corrupted Avengers, Fantastic Four and Wolverine issue numbers. Those issues and ambiguously named Onslaught one-shots are not indexed; main Uncanny/X-Men/Cable ranges are clear.')
    n[74]['issueKeys']+=group('X-Men',1991,14,16)+group('X-Factor',1986,84,86)+group('X-Force',1991,16,18)+group("Stryfe's Strike File",1993,1,1)
    note(74,'Overlaps the X-Cutioner’s Song Epic but adds Uncanny 297 and Strike File instead of the Epic’s earlier setup chapters.')
    n[75]['issueKeys']+=group('Uncanny X-Men',1963,235,238)+group('New Mutants',1983,95,97)+group('X-Factor',1986,60,62);note(75,'The event is the 270–272-era crossover; 235–238 supplies the earlier Genosha story rather than consecutive event chapters.')
    for i in [76,77]:note(i,'Independent character-origin spotlights; read by interest. One-shot years are not indexed without edition-by-edition confirmation.')
    seq([78,79,80,81],'X-Men Red — Al Ewing (2022)','X-Men Red',2022,[(1,5),(6,10),(11,13),(14,18)])
    n[80]['issueKeys']+=group('X-Men: Before the Fall - Heralds of Apocalypse',2023,1,1)
    note(78,'Arakko-era series following the terraforming of Mars; separate from Tom Taylor’s 2018 Jean Grey team.');note(79,'Judgment Day and its aftermath. Read the main A.X.E. event separately.');note(80,'Genesis War setup, with Heralds of Apocalypse included.');note(81,'Concludes the Genesis War during Fall of X; follows the Hellfire Gala catastrophe.')
    seq([82,83],'X-Men Red — Tom Taylor (2018)','X-Men Red',2018,[(1,5),(6,11)])
    n[82]['issueKeys']+=group('X-Men Red Annual',2018,1,1);note(82,'After Phoenix Resurrection. Separate from Ewing’s 2022 Arakko series.');note(83,'Concludes the 2018 Jean Grey team’s conflict with Cassandra Nova.')
    issues(84,('Uncanny X-Men',1963,376,377),('Cable',1993,73,76),('X-Men',1991,96,97),('Wolverine',1988,145,147));n[84]['readingPath']=run('X-Men — The Twelve / Ages of Apocalypse',1,'The Twelve begins here; continue into Ages of Apocalypse.')
    issues(85,('X-51',1999,8,8),('Uncanny X-Men',1963,378,378),('Cable',1993,77,77),('Wolverine',1988,148,148),('X-Men Unlimited',1993,26,26),('X-Men',1991,98,98),('X-Men: The Search for Cyclops',2000,1,4));n[85]['readingPath']=run('X-Men — The Twelve / Ages of Apocalypse',2,'After The Twelve. Different event from the 1995 Age of Apocalypse alternate universe.')
    cite(86,'https://catalog.ocls.org/Author/Home?author=%22Nicieza%2C+Fabian.%22&basicSearchType=Author&filter%5B%5D=authorStr%3A%22Nicieza%2C+Fabian%22&sort=relevance&view=list','OCLS · X-Men Weddings publisher synopsis and issue list')
    issues(86,('X-Men',1991,30,30),('Astonishing X-Men',2004,51,51),('X-Men Gold',2017,30,30),('Black Panther',2005,18,18));note(86,'Selected wedding issues across unrelated runs. The source’s X-Men year 1990 is normalized to the 1991 series.')
    issues(87,('X-Men Chronicles',1995,1,2),('X-Man',1995,1,1),('Blink',2001,1,4));n[87]['readingPath']=run('X-Men — Age of Apocalypse',4,'Companion/prequel material best read after Alpha, Reign and Omega. Overlaps X-Man 1 in Alpha.')
    issues(88,('Age of Apocalypse',2012,1,14),('X-Treme X-Men',2012,12,13),('X-Termination',2013,1,2),('Astonishing X-Men',2004,60,61));n[88]['issueKeys']+=['Uncanny X-Force (2010) #19.1'];n[88]['readingPath']=run('X-Men — Age of Apocalypse',6,'Much later revival and X-Termination, after the original event and Uncanny X-Force’s return to that world.')
    issues(89,('X-Man',1995,53,54),('X-Men: Age of Apocalypse',2005,1,6),('Exiles',2001,60,61),('What If?',1989,77,77),('What If?',1989,81,81));n[89]['readingPath']=run('X-Men — Age of Apocalypse',5,'Later return stories and alternate possibilities. Read after the original Alpha/Reign/Omega ending.')
    titles=['Generation Next','Astonishing X-Men','Gambit and the X-Ternals','Weapon X','Factor X','X-Man','X-Calibre','Amazing X-Men']
    issues(90,('Uncanny X-Men',1963,320,321),('X-Men',1991,40,41),('Cable',1993,20,20),('X-Men Alpha',1995,1,1))
    for title in titles:n[90]['issueKeys']+=group(title,1995,1,1)
    for title in ['Astonishing X-Men','Amazing X-Men','X-Calibre','Factor X','X-Man']:n[91]['issueKeys']+=group(title,1995,2,3)
    for title in ['Gambit and the X-Ternals','Generation Next','Weapon X']:n[91]['issueKeys']+=group(title,1995,2,2)
    n[91]['issueKeys']+=group('X-Universe',1995,1,1)
    for title in ['Weapon X','Generation Next','Gambit and the X-Ternals']:n[92]['issueKeys']+=group(title,1995,3,4)
    for title in ['Astonishing X-Men','X-Man','X-Calibre','Factor X','Amazing X-Men']:n[92]['issueKeys']+=group(title,1995,4,4)
    n[92]['issueKeys']+=group('X-Universe',1995,2,2)+group('X-Men Omega',1995,1,1)+group('Age of Apocalypse: The Chosen',1995,1,1)
    for i,p in [(90,1),(91,2),(92,3)]:n[i]['readingPath']=run('X-Men — Age of Apocalypse',p,'Read Alpha, Reign, then Omega. The 1995 series here are separate from later titles with identical names.')
    cite(92,'https://share.marvel.com/comics/discover/2519/the-x-mens-major-alternate-timelines','Marvel · Age of Apocalypse event context')
    cite(93,'https://prhcomics.com/book/?isbn=9781302966553')
    issues(93,('New Mutants',2019,8,12),('Marauders',2019,9,12),('X-Men/Fantastic Four',2020,1,4),('Cable',2020,1,4),('X-Men',2019,8,11),('X-Force',2019,9,12),('Excalibur',2019,9,12),('Hellions',2020,1,4),('Wolverine',2020,4,5),('X-Factor',2020,1,3),('Empyre: X-Men',2020,1,4))
    for character in ['Nightcrawler','Magneto','Fantomex','Storm']:n[93]['issueKeys']+=group('Giant-Size X-Men: '+character,2020,1,1)
    n[93]['readingPath']=run('X-Men — Dawn of X omnibuses',2,'After Dawn of X Omnibus 1, before X of Swords. Alternative to the corresponding individual team volumes.',True)
    caution(93,'Matching-title publisher print contents checked, but digital page count is unconfirmed. Wolverine 1 is partial material and is excluded from whole-issue overlaps.')
    issues(94,('X-Men: Age of Revelation',2025,0,0),('X-Men: Age of Revelation Overture',2025,1,1),('Amazing X-Men',2025,1,3),('Binary',2025,1,3),('Cloak or Dagger',2025,1,3),('Iron & Frost',2025,1,3),('Laura Kinney: Sabretooth',2025,1,3))
    issues(95,('X-Men: Book of Revelation',2025,1,3),('Longshots',2025,1,3),('Radioactive Spider-Man',2025,1,3),('Rogue Storm',2025,1,3),('Expatriate X-Men',2025,1,3),('The Last Wolverine',2025,1,3))
    issues(96,('World of Revelation',2025,1,1),('Unbreakable X-Men',2025,1,3),('Undeadpool',2025,1,3),('Omega Kids',2025,1,3),('X-Vengers',2025,1,3),("Sinister's Six",2025,1,3),('X-Men: Age of Revelation Finale',2025,1,1))
    for i,p in [(94,1),(95,2),(96,3)]:n[i]['readingPath']=run('X-Men — Age of Revelation collections',p,'Collection order, not strict chronology: companion miniseries occur in parallel. Start with Overture; World of Revelation contains the Finale.')
    issues(97,('Extraordinary X-Men',2015,6,12));n[97]['readingPath']=run('Extraordinary X-Men (2015)',2,'Same main issue range as Extraordinary X-Men Volume 2: Apocalypse Wars; not an omnibus of all three Apocalypse Wars titles.',True)
    issues(98,('X-Men: Apocalypse/Dracula',2006,1,4));n[98]['characters']=[c for c in n[98]['characters'] if c['name']!='X-Men'];note(98,'Historical Apocalypse/Dracula story. The X-Men title branding does not establish a modern-team appearance.')
    issues(99,('All-New X-Men',2012,16,17),('Uncanny X-Men',2013,12,13),('Wolverine & the X-Men',2011,36,37),('X-Men: Battle of the Atom',2013,1,2),('X-Men',2013,5,6));cite(99,'https://share.marvel.com/comics/discover/2519/the-x-mens-major-alternate-timelines','Marvel · Battle of the Atom event premise')
    note(99,'Fills the crossover gaps in Bendis All-New/Uncanny and Aaron Wolverine & the X-Men. Also included in the Bendis Uncanny omnibus.')
    n[100]['issueKeys']+=group('X-Men',1991,8,8);note(100,'Different from the Bishop’s Crossing Epic: more Uncanny chapters (281–293), fewer blue-team chapters and no indexed Ghost Rider issues. Neither is a wholly new sequel to the other.')
    # Explicitly matching trade rows from live Comic Book Roundup source pages.
    scores={}
    def review(slug,rows):
        for i,critic,count,user,ucount in rows:scores[i]=(slug,critic,count,user,ucount)
    review('wolverine-and-the-x-men-(2011)',[(16,8.3,57,9.2,2),(17,8.3,38,8.8,2),(18,7.4,46,8.5,1),(19,7.7,43,7.2,2),(20,7.4,58,7,2),(21,7.4,55,7,2),(22,7.8,57,7.2,2),(23,8.1,55,7,2)])
    review('x-men-blue-(2017)',[(32,7.8,77,7.6,8),(33,8.1,32,6.5,6)])
    review('x-men-gold-(2017)',[(61,6.9,76,6.3,5),(62,6.3,32,6.1,5)])
    review('x-men-red-(2018)',[(82,8.2,99,6.5,4),(83,8.5,57,5.7,3)])
    review('x-men-(2021)',[(35,7.8,76,8,3),(36,7.8,56,5,2),(37,7.5,48,8,1),(38,7.4,51,7.5,1),(39,7.5,39,7.5,1),(40,7.2,37,7,1)])
    review('x-men-(2019)',[(44,8.6,107,9,5),(45,8.3,66,9.3,3),(46,8.2,71,10,2)])
    review('x-men-red-(2022)',[(78,8.6,60,9.3,5),(79,8.6,40,9.5,4),(80,8,26,9,1),(81,8.4,27,8.8,2)])
    review('x-men-92-(2016)',[(27,7.2,18,None,None),(28,8.4,2,None,None)])
    review('x-men-legends-(2021)',[(65,7,41,None,None),(66,6.7,19,None,None)])
    review('x-men-(2024)',[(42,7.8,32,8,1),(43,8.2,32,None,None)])
    for i,(slug,critic,count,user,ucount) in scores.items():
        url='https://comicbookroundup.com/comic-books/reviews/marvel-comics/'+slug;d=n[i]
        d['review']=dict(criticScore=critic,criticCount=count,userScore=user,userCount=ucount,url=url,checkedAt=d['checkedAt'],title=by[ids[i-1]]['title'],match='Trade row matched by series, volume and collected issue count; not ISBN.',scope='Aggregate of reviewed issues in this collection, not the entire series; bonus material may be excluded.')
        d['sources'].append(dict(label='Comic Book Roundup · matching trade row',url=url));d['checks']['review']='Verified matching collection row'
    for i in [14,34,41]:n[i]['checks']['review']='Score withheld: review collection issue count differs from publisher listing'
    for i in n:n[i]['issueKeys']=list(dict.fromkeys(n[i]['issueKeys']))

if __name__=='__main__': main()
