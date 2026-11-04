# Sustained Qwen enrichment run — October 30, 2026

Processed 100 previously unused cached ISBN editions in four sequential batches of 25 using Qwen3.5-4B. The worker had zero failures. Published 32 source-reviewed synopsis improvements to the local Panel site, held 55 editions for research, and retained 13 existing editorial summaries. There are now 60 approved synopsis overlays.

Nine published summaries retain the worker selection unchanged; 23 are source-backed Codex revisions. This is a supervised enrichment workflow. These outcomes do not establish that Qwen is ready to publish autonomously. Delegated decision events retain the user authorization and identify Codex as assessor; they are not independent human adjudications or gold labels.

| Batch | Editions | Worker failures | Published | Unchanged drafts | Revised drafts | Held | Retained | Worker seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25c | 25 | 0 | 5 | 2 | 3 | 16 | 4 | 136.31 |
| 25d | 25 | 0 | 8 | 4 | 4 | 13 | 4 | 141.22 |
| 25e | 25 | 0 | 12 | 1 | 11 | 11 | 2 | 132.14 |
| 25f | 25 | 0 | 7 | 2 | 5 | 15 | 3 | 148.02 |

Worker times exclude source research, editorial review, testing and browser verification. All 220 model evidence quotations match their original source packets. Frozen packet hashes, Python code hashes, publication chain, exact backups and final production data hashes passed the saved audit. Staged differences preserve every unrelated record and every field other than synopsis, synopsis review provenance and source links.

## Source research and scope

Fresh public distributor evidence resolved nine provisional series identities for synopsis-only decisions: Thunderbolts (2006), Moon Girl and Devil Dinosaur (2015), Chaos War (2010), Maestro (2022), Illuminati (2015), The Totally Awesome Hulk (2015), Miles Morales: Spider-Man (2018), King In Black: Namor (2020), and Venom (2003). Each resolution preserves exact-ISBN identifier paths, source hashes and corroboration of the original bibliographic series year. No global alias, collected-issue completeness or appearance claim was added.

Additional evidence holds cover a Wolverine description contaminated by Spider-Man copy, a Shadowland Power Man record describing Moon Knight, a New Avengers record describing Amazing Spider-Man, and Iron Man 2020 satire that would mislead if extracted literally. Existing parser, inventory, partial-material, missing-description and unresolved edition flags continue to block publication. Failed distributor lookups do not count as corroboration.

## Verification

All 32 new summaries were verified in browser search results. Groot: Uprooted required All imported records because its borrowing availability remains unconfirmed; publication did not alter that availability. Exact ISBN search avoids pagination when common title words return many books.

The detail panel now distinguishes saved reviewed summaries from basic publisher excerpts and labels delegated or assistant review as AI review. This does not upgrade automatic character mentions, issue membership or reading order. Typecheck, 34 Python worker/review/staging/promotion tests, 18 catalog tests and whitespace validation passed.

The local rebuild initially skipped the home page, then exposed a blocked loopback fetch during prerendering. The page now explicitly declares force-static, matching this browser-loaded catalog and static local server. The final build succeeded with local loopback access, generated the home page, and was verified in the browser. Post-build target hashes still match the last publication receipt. Final verification and the Dawn of X screenshot are saved beside the cumulative audit.

## Audit and recovery

The four directories are data/local-ai-trials/worker-batch-25c-20261030 through worker-batch-25f-20261030. Each preserves frozen packets, raw attempts, model results, original and resolved review queues, review-spec.json, immutable delegated-decisions, approved-staging, edition-research where applicable, and publish-receipt with exact backups. The cumulative audit is worker-batch-25c-20261030/sustained-audit-cdef.json. Rollback must use the newest active receipt first; older receipts deliberately refuse to overwrite later publication changes.

No remote deployment was performed. Approved summaries are stored in data/approved-synopses.json and applied over later collector rebuilds.

## Edition decisions

| Batch | ISBN | Edition | Decision | Rationale |
| --- | --- | --- | --- | --- |
| 25c | 9781302369903 | The Fearless Defenders Vol. 1: Doom Maidens: Issues #1-6 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review |
| 25c | 9781302535148 | Fantastic Four Vol. 1: Save Everyone: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed |
| 25c | 9781302527334 | Moon Knight: City of the Dead: Issues #1-5 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25c | 9780785171317 | Venom Vs. Carnage: Issues #1-4 | needs_research | Retain unresolved evidence/edition blockers: no_inventory |
| 25c | 9781302476366 | Civil War: Thunderbolts: Issues #101-105 | revise | Source-backed correction names the protagonist and restores the central conflict omitted or obscured by the model selection. No issue or reading-order changes. |
| 25c | 9781302367572 | X-Men: The End Book Three: Issues #1-6 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25c | 9781302527754 | Wolverine Epic Collection: The Return of Weapon X | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, editorial_source_integrity_requires_research |
| 25c | 9781302488437 | Avengers Standoff: Assault on Pleasant Hill: Issue #1 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25c | 9781302496333 | Spider-Man Loves Mary Jane Vol. 2: The New Girl: Issues #6-10 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25c | 9781302388058 | Inhumanity: Issues #1-2 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, bibliographic_series_identity_requires_review |
| 25c | 9781302510480 | The Road to Marvel's Avengers: Endgame: The Art of the Marvel Cinematic Universe | needs_research | Retain unresolved evidence/edition blockers: no_inventory, no_synopsis |
| 25c | 9781302940706 | The Darkhold | accept | Source-grounded premise improves truncated basic metadata and retains the central source-described conflict; no stronger existing editorial synopsis. |
| 25c | 9781302530723 | Star Wars: Darth Vader Modern Era Epic Collection: Shadows and Secrets | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed |
| 25c | 9781302532857 | Spider-Boy Vol. 3: The Dragon's Challenge: Issues #11-16 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review |
| 25c | 9781302527549 | Fantastic Four Epic Collection: Atlantis Rising: Issues  #393-402 | accept | Source-grounded premise improves truncated basic metadata and retains the central source-described conflict; no stronger existing editorial synopsis. |
| 25c | 9781302378479 | Wolverine and the X-Men by Jason Aaron Vol. 7: Issues #30-35 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25c | 9781302494377 | Eternals: To Slay a God: Issues #1-6 | revise | Source-backed correction names the protagonist and restores the central conflict omitted or obscured by the model selection. No issue or reading-order changes. |
| 25c | 9781302520571 | Marvel Action Avengers Vol. 3: The Fear Eaters: Issues #7-9 | needs_research | Retain unresolved evidence/edition blockers: no_inventory, no_synopsis |
| 25c | 9781302943486 | Moon Girl and Devil Dinosaur: Place in the World: Issues #37-47 | revise | Source-backed correction names the protagonist and restores the central conflict omitted or obscured by the model selection. No issue or reading-order changes. |
| 25c | 9781302497033 | Captain America: Steve Rogers Vol. 2: The Trial Of Maria Hill: Issues #7-11 | needs_research | Retain unresolved evidence/edition blockers: no_inventory |
| 25c | 9781302483173 | X-Factor Visionaries By Peter David Vol. 2: Issues #76-78 | needs_research | Retain unresolved evidence/edition blockers: contents_conflict, no_inventory |
| 25c | 9781302528232 | Avengers by Jason Aaron Vol. 5: Issues #46-62 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, bibliographic_series_identity_requires_review |
| 25c | 9781302515973 | Marvel Zombies: The Complete Collection Vol. 2 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25c | 9781302498276 | Spider-Gwen Vol. 3: Long-Distance: Issues #14-15 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25c | 9781302514297 | Ms. Marvel: Metamorphosis: Issues #12-19 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25d | 9781302942182 | Star Wars: Darth Vader by Greg Pak Vol. 4: Crimson Reign: Issues #18-22 | revise | Source-backed editorial correction restores explicit protagonists and central conflict while removing promotional or context-dependent fragments. Synopsis only. |
| 25d | 9781302935016 | U.S.Agent: The Good Fight: Issues #1-4 | needs_research | Retain unresolved evidence/edition blockers: contents_conflict, no_inventory |
| 25d | 9781302935832 | Sword Master Vol. 2: God of War: Issues #7-12 | accept | Self-contained source-grounded selection improves a truncated basic snippet; no stronger editorial synopsis exists. |
| 25d | 9781302478568 | Hawkeye And Mockingbird/Black Widow: Widowmaker: Issues #1-4 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25d | 9781302503758 | The Unbelievable Gwenpool Vol. 5: Lost In The Plot: Issues #21-25 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25d | 9781302488406 | Shadowland: Power Man: Issues #1-3 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, editorial_source_integrity_requires_research |
| 25d | 9781302533038 | Marvel Masterworks: The Tomb of Dracula Vol. 5 | revise | Source-backed editorial correction restores explicit protagonists and central conflict while removing promotional or context-dependent fragments. Synopsis only. |
| 25d | 9781302502607 | Astonishing X-Men by Charles Soule Vol. 1: Life of X: Issues #1-6 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25d | 9781302368029 | Chaos War: Issues #1-5 | accept | Self-contained source-grounded selection improves a truncated basic snippet; no stronger editorial synopsis exists. |
| 25d | 9781302936174 | Ms. Marvel: Army Of One: Issues #1-12 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25d | 9781302478667 | The Punisher Vol. 2: Border Crossing: Issues #7-12 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review, no_synopsis |
| 25d | 9781302509811 | Beta Ray Bill: Godhunter: Issues #1-3 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, bibliographic_series_identity_requires_review |
| 25d | 9781302434120 | Fear Itself: The Fearless: Issues #1-12 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review |
| 25d | 9781302530105 | Venom Modern Era Epic Collection: Shiver: Issues #1-18 | revise | Source-backed editorial correction restores explicit protagonists and central conflict while removing promotional or context-dependent fragments. Synopsis only. |
| 25d | 9781302943738 | Marvel-Verse: Shuri | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25d | 9781302953188 | Groot: Uprooted | accept | Self-contained source-grounded selection improves a truncated basic snippet; no stronger editorial synopsis exists. |
| 25d | 9781302501631 | Ms. Marvel Vol. 8: Mecca: Issues #19-24 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25d | 9781302014148 | Captain America By Ed Brubaker Vol. 3: Issues #11-14, 328 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries |
| 25d | 9781302507961 | Astonishing X-Men by Matt Rosenberg: Until Our Heart Stops: Issues #13-17 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25d | 9781302504601 | Amazing Spider-Man: Worldwide Vol. 8: Issues #794-796 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25d | 9781302496432 | Wolverine: Origins & Endings: Issues #36-40 | needs_research | Retain unresolved evidence/edition blockers: no_inventory |
| 25d | 9781302530532 | Avengers Epic Collection: Seasons of the Witch | accept | Self-contained source-grounded selection improves a truncated basic snippet; no stronger editorial synopsis exists. |
| 25d | 9781302944292 | X-Men: First Class: Road Trips: Issues #1-9 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25d | 9781302480486 | What If? Age Of Ultron: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25d | 9780785170327 | Daredevil: Yellow: Issues #1-6 | revise | Source-backed editorial correction restores explicit protagonists and central conflict while removing promotional or context-dependent fragments. Synopsis only. |
| 25e | 9781302527211 | Cult of Carnage: Misery: Issues #1-5 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302488611 | Spider-Woman Vol. 1: Baby Talk: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review |
| 25e | 9781302943707 | Maestro: World War M: Issues #1-5 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302480189 | X-23 Vol. 3: Don't Look Back: Issues #17-21 | accept | Self-contained source-grounded X-23 babysitting/adventure premise improves truncated basic metadata. No stronger existing editorial synopsis. |
| 25e | 9781302488512 | Illuminati: Life of Crime | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302498511 | Spider-Man: Hobgoblin Lives: Issues #1-3 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25e | 9780785179719 | Deadpool Vol. 6: I Rule, You Suck: Issues #27-31 | needs_research | Retain unresolved evidence/edition blockers: no_synopsis |
| 25e | 9781302505240 | Spider-Man: Miles Morales Vol. 4: Issues #234-240 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302935993 | Amazing Spider-Man By Nick Spencer Vol. 11: Last Remains: Issues #50-55 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25e | 9780785178248 | Wolverine by Claremont & Miller: Issues #1-4 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory, no_synopsis |
| 25e | 9781302536305 | Spider-Man: The Other | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302942137 | Ms. Marvel: Beyond The Limit by Samira Ahmed: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25e | 9781302377687 | Iron Man Vol. 4: Iron Metropolitan: Issues #18-22 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed |
| 25e | 9781302525019 | Moon Girl and Devil Dinosaur: Menace on Wheels: Issues #1-5 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302499051 | The Totally Awesome Hulk Vol. 3: Big Apple Showdown: Issues #13-18 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302489403 | X-Men: The Trial of Gambit: Issues #341-350 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25e | 9781302524562 | Deadpool by Alyssa Wong Vol. 1: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: partial_material_requires_review |
| 25e | 9781302941826 | Reign of X Vol. 12 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302939090 | Savage Avengers Vol. 4: King in Black: Issues #17-22 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302479206 | Hulk: World War Hulk: Warbound: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25e | 9781302535223 | Incredible Hulk Epic Collection: Devolution | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed |
| 25e | 9781302480974 | Spider-Woman Vol. 1: Spider-Verse: Issues #1-4 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25e | 9781302944711 | Ant-Man: The Saga of Scott Lang | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries |
| 25e | 9781302483715 | Runaways: Battleworld: Issues #1-4 | needs_research | Retain unresolved evidence/edition blockers: no_inventory, no_synopsis |
| 25e | 9781302938901 | Reign of X Vol. 3 | revise | Source-backed editorial correction restores protagonist/context or central story scope omitted by Qwen; no issue, appearance-index or reading-order claims added. |
| 25f | 9781302944513 | Miles Morales Vol. 8: Empire of the Spider: Issues #37-42 | revise | Restore the protagonists and interdimensional setup, remove sales language and omit the corrupted honorific. Exact-ISBN distributor series corroborates the original 2018 bibliographic year. |
| 25f | 9781302524180 | Captain America Epic Collection: Fighting Chance | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries |
| 25f | 9780785199830 | Star Wars: Vol. 3 : Rebel jail | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25f | 9781302938260 | King In Black: Issues #1-5 | accept | Source-checked complete premise selection improves the truncated existing snippet, with exact issue inventory and no unresolved review flags. Retain the original worker draft. |
| 25f | 9781302938550 | King In Black: Namor: Issues #1-5 | revise | Replace the cast-list fragment and superlative with the mission and named threat, preserving the threatened outcome. Exact-ISBN distributor series corroborates the original 2020 bibliographic year. |
| 25f | 9781302479831 | Avengers West Coast: Vision Quest: Issues #42-50 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review |
| 25f | 9781302509859 | Captain Marvel: Earth's Mightiest Hero Vol. 4: Issues #12-15 | needs_research | Retain unresolved evidence/edition blockers: no_inventory |
| 25f | 9781302483623 | Future Imperfect: Warzones!: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: no_inventory |
| 25f | 9781302378677 | Fantastic Four Masterworks Vol. 4: Issues #31-40 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries |
| 25f | 9781302519698 | Star Wars: Doctor Aphra Vol. 7: A Rogue's End: Issues #37-40 | needs_research | Retain unresolved evidence/edition blockers: partial_material_requires_review |
| 25f | 9781302522674 | Iron Man 2020: Robot Revolution: Issues #1-6 | needs_research | Retain unresolved evidence/edition blockers: editorial_source_integrity_requires_research |
| 25f | 9781302496371 | Spider-Man/Doctor Octopus: Year One: Issues #1-5 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25f | 9781302940423 | Symbiote Spider-Man: Crossroads: Issues #1-5 | revise | Restore the period and Crossroads setting omitted by extraction; remove the dangling introduction and reader-directed advertising. |
| 25f | 9781302386498 | Daredevil By Mark Waid Vol. 7: Issues #31-36 | needs_research | Retain unresolved evidence/edition blockers: bibliographic_series_identity_requires_review, no_synopsis |
| 25f | 9781302495497 | Spectacular Spider-Man Vol. 3: Here There Be Monsters: Issues #11-14 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25f | 9781302508715 | Uncanny X-Men by Kieron Gillen: The Complete Collection Vol. 1 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
| 25f | 9781302513917 | New Avengers By Brian Michael Bendis: The Complete Collection Vol. 7: Issues #17-34 | needs_research | Retain unresolved evidence/edition blockers: contents_conflict, no_inventory, editorial_source_integrity_requires_research |
| 25f | 9781302942663 | Silk Vol. 2: Age of the Witch: Issues #1-5 | accept | Source-checked complete premise selection improves the truncated existing snippet, with exact issue inventory and no unresolved review flags. Retain the original worker draft. |
| 25f | 9781302514563 | Star Wars: Age of Rebellion - Heroes | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25f | 9781302488932 | Venom Vol. 3: Twist: Issues #14-18 | revise | Restore Spider-Man and the Fantastic Four intervention omitted by the one-sentence selection; no claims of a completed killing. Exact-ISBN distributor series corroborates the original 2003 bibliographic year. |
| 25f | 9781302525231 | Invincible Iron Man by Gerry Duggan Vol. 1: Demon in the Armor: Issues #1-6 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, no_inventory |
| 25f | 9781302519650 | Dawn of X Vol. 1 | revise | Represent the six-series opening volume rather than only three selected teams. Summarize the actual source premises without adding unmentioned locations, identities or outcomes. |
| 25f | 9781302513344 | Decades: Marvel in the '80s - Awesome Evolutions | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries |
| 25f | 9780785170785 | Mighty Avengers Vol. 1: The Ultron Initiative: Issues #1-6 | needs_research | Retain unresolved evidence/edition blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 25f | 9781302418700 | Uncanny X-Men Masterworks Vol. 4: Issues #122-131 | reject | Retain the existing useful editorial synopsis; the new draft offers no clear improvement. |
