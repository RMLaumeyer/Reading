# Qwen enrichment session — November 2, 2026

Published **59 reviewed synopses**, increasing the approved total from **202 to 261** on the local site. Qwen processed **150 previously unused editions** plus **6 source-recovery executions**. 5 publications use unchanged Qwen selections; 54 are explicit source-backed editorial revisions.

Two additional historical Qwen drafts were reviewed and revised without new inference: Deadpool: Operation Annihilation and Gwenpool: All-New, All-Deadly. Their original packets, model outputs and editorial findings were hash-verified; they are excluded from the new worker-execution and response counts.

The 156 worker executions completed with zero failures and 149 recorded model responses. Cases without eligible plot excerpts did not request inference. All 359 selected quotations match their frozen sources. Qwen used the original sentence-selection policy, temperature zero and thinking off. This is delegated Codex source/editorial assessment, not independent human gold labels or a general accuracy estimate.

## Publication passes

| Pass | Cases | Published | Unchanged | Revised | Held at that pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| sustained-25h-20261102 | 25 | 9 | 1 | 8 | 16 |
| sustained-25i-20261102 | 25 | 10 | 2 | 8 | 15 |
| sustained-25j-20261102 | 25 | 8 | 0 | 8 | 17 |
| source-recovery-two-20261102 | 2 | 1 | 0 | 1 | 1 |
| sustained-25k-20261102 | 25 | 11 | 1 | 10 | 14 |
| sustained-25l-20261102 | 25 | 6 | 0 | 6 | 19 |
| source-recovery-four-20261102 | 4 | 4 | 0 | 4 | 0 |
| sustained-25m-20261102 | 25 | 8 | 1 | 7 | 17 |
| legacy-editorial-two-20261102 | 0 | 2 | 0 | 2 | 0 |

Cases in source-recovery passes repeat ISBNs; they are not additional fresh editions. Four initially held editions from this session were subsequently recovered, alongside three editions from the earlier backlog.

## Source recovery and holds

Sixteen exact-ISBN public library lookups retained ten validated records and six failed acquisitions. Every accepted record preserves raw downloaded pages, exact format-ISBN evidence and hashes. Daredevil: The Man Without Fear gained its missing origin description. Daredevil: Reborn, Avengers: Solo and Deadpool vs. Thanos gained missing collecting statements. Dawn of X Vol. 15 gained the complete ending of its truncated description, allowing a revision covering the Marauders and Fantomex alongside its other three threads. The old truncated source and original drafts remain unchanged.

Incredible Hulk: Transfer of Power stays held because its new source says 1999 in the collecting statement and 2000 in the series label. Kanan gained contents but its differently named series label does not resolve the collecting title automatically. Mighty Thor and Deadpool Kills Deadpool repeated insufficient blurbs, so no model retry was requested. Thor by Simonson and X-23 also retain explicit plot-context holds; creator praise or an origin teaser alone did not become a story synopsis.

Additional manual holds preserve the Old Man Logan #1–4 versus #1–6 disagreement, Weapon X anthology-feature scope and the Guardians of the Galaxy production art book. The latter requires treatment appropriate to an art book. Partial stories, unnumbered specials, annuals and conflicting collections remain held.

The last pass also identified a source/publisher year disagreement for Obi-Wan and Anakin: the collecting statement says 2015, while [Marvel’s original first issue identifies 2016](https://www.marvel.com/comics/issue/57730/obi-wan_and_anakin_2016_1?mobile-app=true&theme=false). No year was silently changed. Captain America: The Man With No Face retains a contributor-metadata concern in addition to its original namespace hold.

## Parser correction

Parser version 25 rejects an embedded “material from” scope transition inside an unsplit collecting title. An unnumbered special followed by partial material can no longer become a made-up whole-issue series. The original clause stays available for review, and later issue numbers cannot inherit that ambiguous context. Valid leading material markers and existing title grammar retain their previous behavior. Uppercase VS abbreviation recovery remains deferred.

A replay of **820 frozen packets** changed 7 inventories, all for held editions, with **no approved inventory changes**. The final replay is parser-replay-final.json; an earlier exploratory replay is retained separately. Two regression tests cover compound partial-material scope and disjoint ranges. All **372 Python tests and 18 catalog tests passed**. The earlier seven publication passes used frozen parser version 24; the last fresh pass used tested version 25. Archived code and packets remain hash-verified.

## Publication verification

The audit follows every publication receipt from the initial 202-synopsis baseline to the final 261-synopsis overlay, validates exact backups, and compares the full before/after enrichment payload. Exactly 59 intended records changed, limited to summary, source citations and review provenance. All prior approvals, other book fields and top-level metadata are preserved. The canonical overlay, public file, built preview and actual local served bytes agree. The preview was initially stopped; it was restarted, and the served-payload checks then passed. The automatic collector remains paused. No remote deployment or commit occurred.

The known reviewed backlog is **353 editions**: 262 before, minus 3 prior recoveries, plus 94 remaining fresh holds. This is a reviewed-hold inventory, not all unenriched books.

Artifacts: data/local-ai-trials/timed-session-20261102 contains final-verification.json, published-editions.json, known-held.json, source acquisition records, test logs and parser replay evidence. Each named pass retains its frozen inputs/code, raw Qwen outputs, explicit decisions, staging, publication receipt and verification.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302506735 | Deadpool: Assassin: Issues #1-6 | Source-backed revision |
| 9780785180142 | Guardians Of The Galaxy Vol. 1: Legacy: Issues #1-6 | Source-backed revision |
| 9781302942045 | Iron Man Vol. 3: Books of Korvac III: Cosmic Iron Man: Issues #12-19 | Source-backed revision |
| 9781302368449 | Uncanny X-Force Vol. 7: Final Execution Part 2: Issues #30-35 | Source-backed revision |
| 9781302935788 | Marvel-Verse: Captain Marvel | Source-backed revision |
| 9781302524036 | Star Wars: The Mandalorian: Season One, Part Two: Issues #5-8 | Source-backed revision |
| 9780785179344 | New Avengers Vol. 11: Search For The Sorceror Supreme: Issues #51-54 | Source-backed revision |
| 9781302515195 | Black Panther by Ta-Nehisi Coates Vol. 7: The Intergalactic Empire of Wakanda Part Two: Issues #7-12 | Source-backed revision |
| 9781302523695 | New Mutants Vol. 4: Issues #29-33 | Unchanged selection |
| 9781302526306 | Ghost Rider Vol. 3: Dragged Out Of Hell: Issues #11-16 | Source-backed revision |
| 9781302498887 | Gamora: Memento Mori: Issues #1-5 | Source-backed revision |
| 9781302488383 | Shadowland: Blood on the Streets: Issues #1-4 | Source-backed revision |
| 9781302497897 | The Unworthy Thor: Issues #1-5 | Unchanged selection |
| 9781302523435 | Genis-Vell: Captain Marvel: Issues #1-5 | Unchanged selection |
| 9781302497798 | Moon Knight Vol. 2: Reincarnations: Issues #6-9 | Source-backed revision |
| 9781302528553 | Spider-Man: India - Seva: Issues #1-5 | Source-backed revision |
| 9781302940140 | X-Men By Peter Milligan: Blood of Apocalypse | Source-backed revision |
| 9781302502010 | Venom Vol. 3: Lethal Protector - Blood In The Water: Issues #154-158 | Source-backed revision |
| 9781302520243 | Ms. Marvel By Saladin Ahmed Vol. 2: Stormranger: Issues #7-12 | Source-backed revision |
| 9781302367671 | New X-Men by Grant Morrison Vol. 5: Assault on Weapon Plus: Issues #139-145 | Source-backed revision |
| 9781302494612 | Moon Knight Vol. 1: Lunatic: Issues #1-5 | Source-backed revision |
| 9781302531614 | The Spectacular Spider-Men Vol. 2: Elementary: Issues #6-10 | Source-backed revision |
| 9781302478964 | Black Widow: Itsy-Bitsy Spider | Source-backed revision |
| 9781302528799 | Realm of X: Issues #1-4 | Source-backed revision |
| 9781302525415 | Spider-Man 2099: Dark Genesis: Issues #1-5 | Source-backed revision |
| 9781302940768 | X-Force by Benjamin Percy Vol. 4: Issues #21-26 | Source-backed revision |
| 9781302525903 | Cosmic Ghost Rider: Duel Identity: Issues #1-5 | Source-backed revision |
| 9781302377052 | Daredevil: The Man Without Fear: Issues #1-5 | Source-backed revision |
| 9781302524906 | Deadpool Epic Collection: Dead Reckoning | Source-backed revision |
| 9780785171393 | Hulk: World War Hulk: Issues #1-5 | Source-backed revision |
| 9781302935757 | Incredible Hulk Epic Collection: Who Will Judge The Hulk?: Issues #138-156 | Source-backed revision |
| 9781302939595 | Amazing Spider-Man Epic Collection: Lifetheft: Issues #381-393 | Source-backed revision |
| 9781302480660 | Avengers West Coast: Darker Than Scarlet | Source-backed revision |
| 9781302507787 | Moon Knight: Legacy Vol. 2 – Phases: Issues #194-200 | Source-backed revision |
| 9781302531669 | X-Men by Jed Mackay Vol. 1: Homecoming: Issues #1-7 | Source-backed revision |
| 9781302482381 | Iron Man: Legacy of Doom: Issues #1-4 | Unchanged selection |
| 9781302938949 | Wolverine By Benjamin Percy Vol. 2: Issues #8-12 | Source-backed revision |
| 9781302938116 | Spider-Woman Vol. 2: King In Black: Issues #6-10 | Source-backed revision |
| 9780785179313 | Marvel Universe vs. Wolverine: Issues #1-4 | Source-backed revision |
| 9781302516390 | Ms. Marvel by Saladin Ahmed Vol. 1: Destined: Issues #1-6 | Source-backed revision |
| 9781302527129 | Venom: Lethal Protector: Life And Deaths: Issues #1-5 | Source-backed revision |
| 9781302505431 | Old Man Hawkeye Vol. 1: An Eye For An Eye: Issues #1-6 | Source-backed revision |
| 9781302535032 | Deadpool Modern Era Epic Collection: X X Baby: Issues #13-31 | Source-backed revision |
| 9781302483227 | Punisher By Greg Rucka Vol. 3: Issues #11-16 | Source-backed revision |
| 9781302937997 | Avengers Epic Collection: A Traitor Stalks Within Us | Source-backed revision |
| 9781302482664 | Daredevil: Reborn: Issues #1-4 | Source-backed revision |
| 9781302370268 | Avengers Hawkeye Solo: Issues #1-5 | Source-backed revision |
| 9781302482978 | Deadpool Vs. Thanos: Issues #1-4 | Source-backed revision |
| 9781302936921 | Dawn of X Vol. 15 | Source-backed revision |
| 9781302368180 | Marvel Zombies 5: Issues #1-5 | Source-backed revision |
| 9780785182672 | Invincible Iron Man Vol. 6: Stark Resilient Part 2: Issues #29-33 | Source-backed revision |
| 9781302499044 | The Punisher Vol. 2: End Of The Line: Issues #7-12 | Source-backed revision |
| 9781302940461 | Winter Guard: Operation Snowblind: Issues #1-4 | Unchanged selection |
| 9781302520410 | Amazing Spider-Man by Nick Spencer Vol. 7: 2099: Issues #32-36 | Source-backed revision |
| 9781302535940 | Ultimates by Deniz Camp Vol. 3: Rescue Mission | Source-backed revision |
| 9781302527006 | Marvel-Verse: Spider-Man & Madame Web | Source-backed revision |
| 9781302522117 | Venom: Rex Marvel Select: Issues #1-6 | Source-backed revision |
| 9780785182191 | Deadpool Vol. 8: Operation Annihilation: Issues #36-39 | Source-backed revision |
| 9781302535179 | Gwenpool: All-New, All-Deadly: Issues #1-5 | Source-backed revision |

## Continuation queue

The 353 held editions are grouped into 205 collecting-statement cases, 49 edition-evidence reconciliations, 48 feature-scope cases, 41 plot-evidence cases, five namespace-focused cases, three art books and two other editorial reviews. These are mutually exclusive research-priority groups, not approval categories. Counts of individual flags overlap.

next-session-priorities.json identifies the five namespace-focused cases and preserves their other editorial conditions. continuation-research.json records six primary-source checks. Marvel Zombies Return gained an explicit source-label 2010 versus publisher-original 2009 disagreement; its earlier rewritten-draft hold remains. Spider-Gwen: Predators has publisher support for #19–23 in the 2015B series, but the target source only says 2015, so no A/B identifier or fuller plot was inferred. The Luke Cage damaged-text and Sabretooth rewritten-claim assessments also remain required. No continuation research cleared a hold or changed the published payload.
