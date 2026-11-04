# Twenty-five-edition enrichment batch

October 30, 2026. Processed exactly 25 new cached ISBN editions using Qwen3.5-4B, source preservation, editorial assessment and guarded local publication. The worker's bounded maximum was raised from ten to 25 as requested; sequential execution and all review gates remain unchanged. Eight worker tests passed before preparation. Frozen original packets, code hashes and model attempts are preserved.

## Outcome

| Outcome | Editions |
| --- | ---: |
| Completed original batch | 25 |
| Worker failures | 0 |
| Published reviewed synopsis changes | 7 |
| Held for research | 15 |
| Existing editorial synopsis retained | 3 |

Original per-edition processing times sum to 107.62 seconds; this excludes source research, review and retesting. All 44 original selected evidence quotations match the frozen source packets. Citation matching is not an independently adjudicated semantic accuracy score.

## Published locally

| Edition / ISBN | Treatment |
| --- | --- |
| Venom: Separation Anxiety / 9781302531300 | Editorial correction covers Purple Man's escape, Venom's compromised bond and possible Fantastic Four help. |
| Doom Academy / 9781302535063 | Editorial correction adds the Latveria school setting to Zoe's fairy-tale-book rescue premise. |
| Danny Ketch: Ghost Rider — Blood & Vengeance / 9781302526214 | Editorial correction establishes the gang war and team-up against the new villain/Scarecrow. |
| Ultimate Fantastic Four: Salem's Seven / 9781302481667 | Editorial correction preserves the underground-city threat with readable punctuation and an explicit team name. |
| King Deadpool Vol. 2 / 9781302937003 | Editorial correction covers Elsa Bloodstone's predicament and the additional cult/space-god threats. |
| Wolverine: Origins — Born in Blood / 9780785171362 | Retained Qwen's clean selection from fresh exact-ISBN distributor evidence, replacing the original snippet's broken `[Author]` placeholders. |
| Deadpool's Art of War / 9781302479022 | Editorial correction from fresh distributor evidence establishes the book-sales/war scheme and Loki threat; original cached source had no plot. |

Six of the seven published synopses are assistant corrections, not raw Qwen output. User-authorized delegated review and supporting quotations are recorded explicitly. This is supervised enrichment, not autonomous model approval or independent human adjudication. Only synopsis/provenance/source fields changed; no issue-list, character-appearance or reading-order claims were added.

## Five source investigations and three retests

The bounded OverDrive collector returned validated exact-ISBN records for X-Factor, Wolverine: Origins and Deadpool's Art of War. Monsters Unleashed and Figment acquisitions returned 404. Cached search/media pages, identifiers, response states and hashes are retained in `edition-research/`.

Three source-augmented packets were separately frozen and retested with Qwen. Wolverine's clean plot passage became usable. Deadpool's new description enabled an editorial correction. X-Factor remained held: Google metadata labels its series 2005, while the fetched distributor record labels it 2006; Qwen also continued selecting an uninformative question. No year was guessed or silently reconciled.

The resolved review queue retains original proposals, fresh sources, prior model output and explicit resolution notes for the two newly evidence-sufficient cases. Resolving missing synopsis evidence does not establish complete edition contents.

## Held and retained records

| Edition | Disposition |
| --- | --- |
| Monsters Unleashed | Provisional series identity; distributor acquisition unsuccessful |
| Fear Itself: Deadpool/Fearsome Four | Missing inventory and plot evidence; no existing enrichment record |
| Figment | Provisional identity; distributor acquisition unsuccessful |
| X-Factor: Time and a Half | Conflicting series-year evidence; held |
| Uncanny X-Men Masterworks Vol. 9 | Retained already useful editorial synopsis |
| Marvel Horror: The Magazine Collection | Unparsed/unresolved and partial contents |
| Squadron Supreme | Contents conflict: cached collecting statement describes an additional Captain America issue without the main range |
| X-Men '92: House of XCII | Retained already useful alternate-continuity synopsis; unresolved inventory remains |
| Spider-Man: Kraven's First Hunt | Unparsed/unresolved inventory and backup material |
| Journey Into Mystery: Fear Itself Fallout | Decimal/supplemental-range conflict remains |
| Uncanny Avengers: Unity Vol. 2 | Provisional series identity |
| Avengers Epic Collection: Kang War | Partial material remains under review |
| The A-Z of Marvel Monsters | Partial/unresolved mixed-series material; not a complete whole-issue inventory |
| Avengers Assemble Vol. 4 | Missing inventory and plot evidence; no existing enrichment record |
| Avengers by Brian Michael Bendis Vol. 1 | No accepted source inventory |
| Man-Wolf: The Complete Collection | Unparsed/unresolved mixed-series contents |
| Spectacular Spider-Man: Disassembled | Retained already useful editorial synopsis |
| Captain America: Serpents Unite! | Disjoint contents remain unparsed |

## Publication checks

All 18 catalog tests pass. Exactly seven records changed and the other records, including the previous thirteen synopsis publications, remain unchanged. Other fields within changed editions are preserved. Target, rollback-backup and frozen-packet hashes match. There are now twenty canonical approved synopsis overlays total.

All seven published synopses were checked in the running local site. Source/proposal/review artifacts, staging diff, approvals, backups and `publication-audit.json` are under `data/local-ai-trials/worker-batch-25-20261030/`. `published-art-of-war.png` records browser proof. Generic needs-review labels remain for unreviewed fields.

Only the existing local site at http://localhost:5173/ was updated. No remote deployment, automatic schedule or new model installation occurred. Unresolved source/edition cases remain held instead of weakening the publication gate to increase throughput.
