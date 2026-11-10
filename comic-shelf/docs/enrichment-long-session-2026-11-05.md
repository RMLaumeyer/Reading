# Long enrichment session — November 5, 2026

Published **35 new reviewed synopses**, raising the local approved total **342 → 377**. Reviewed **75 previously unused editions** across three 25-edition batches and performed **one additional source-recovery execution** for an edition from the first batch. The final backlog is **467 held editions**, up from 427: 41 fresh cases were initially held and one was subsequently recovered. No remote deployment occurred.

## Results and model limits

Across 76 worker case executions, Qwen returned **71 responses**, with **five empty-input no-call outcomes**, **164 literal selected quotes**, **459.29 worker seconds** and **zero worker failures**. The source recovery is not counted as a 76th fresh ISBN. Publications comprise **33 explicit editorial revisions and two unchanged model selections**. Three later fidelity corrections tightened already published wording and do not increase the publication or model-request counts.

| Pass | Cases | New publications | Held at that review |
| --- | ---: | ---: | ---: |
| First fresh batch | 25 | 14 | 11 |
| Second fresh batch | 25 | 14 | 11 |
| Hawkeye source recovery | 1 reused ISBN | 1 | 0 |
| Third fresh batch | 25 | 6 | 19 |

The third batch had more empty/thin descriptions, conflicting ranges and unknown supplemental contents. Its lower yield was retained. An issue-list fragment is not a synopsis, and a literal quotation is not proof of useful coverage. The 60-word/450-character candidate bounds, original prompt, three-passage selector, temperature zero, thinking off and 200-token output limit are unchanged. These results continue to support a supervised drafting worker; they do not justify automatic publishing without review.

## Pipeline improvement

Parser **version 26** preserves the Sgt. abbreviation, including uppercase SGT., while locating the collecting-sentence boundary. Two regression tests cover casing, exact quotes, true sentence boundaries, missing-year/annual holds and invalid issue suffixes/ranges. **387 Python tests and 18 catalog tests passed**. A replay of **921 unique frozen source packets** changed only the intended Sgt. Fury: Berlin Breakout case.

That case still has two unresolved yearless entries, SGT. FURY #20–36 and ANNUAL #1–2. No original year is inferred from an Epic Collection year, and annual completeness remains unknown. Only edition_trial.py and test_edition_trial.py changed among the 78 core Python files. All model runs were frozen after that change and still match their snapshots. No later test-suite rerun is claimed for artifact-only work.

Full-source review also documented future parser candidates: comma-containing All-New, All-Different Avengers and Doctor Strange, Sorcerer Supreme titles, and an unnumbered Minimum Carnage title that fuses with Scarlet Spider into a false compound. Negative issue -1, year-suffixed labels and unknown partial material remain held. No broad fix was made during inference.

## Source recovery and review

Four guarded ISBN lookups produced one accepted source and three preserved failures. Ultimates: Homeland Security's two records differ in punctuation and both collect #7–13 instead of the catalog's #7–14. Wolverine: Old Man Logan's records differ in ellipsis typography and both add an unnumbered Giant-Size special. Black Widow: Deadly Origin yielded no bounded public ISBN result. All downloaded HTML hashes verified. Failed lookup paths/hashes are attached to the held map to prevent unchanged retries.

Hawkeye by Fraction & Aja (9781302940171) recovered from an empty target description using an exact-ISBN public library record. Its collecting statement includes the main run, annual and companion issue. [Publisher annual metadata](https://www.marvel.com/comics/issue/47398/hawkeye_annual_2013_1) corroborates the unusual annual syntax. The direct page returned 403; indexed publisher text exposed the heading/date/credits and synopsis, and that limitation is explicitly recorded. Two short, noncontiguous annual excerpts were added after inference to cover Kate's Los Angeles story; they are not presented as Qwen input or output. Target collecting evidence establishes membership, not another format's ISBN. [The recovery report](enrichment-continuation-2026-11-05b.md) records the details.

Hawkeye lacked an existing enrichment record. The first staging package correctly excluded it and remains preserved. A second package explicitly used the tested reviewed-synopsis initialization path. Pages, characters, stories, issue keys and reading order remain unknown, with no inferred cover. The initialization marker survives canonical-overlay rebuild.

Other namespace reviews used exact-ISBN bibliography and publisher metadata; limited search-index headings were explicitly distinguished from successfully fetched full pages. All ordinary book plot claims come from full frozen target descriptions. Examples include [the readable publisher Initiative list](https://share.marvel.com/comics/discover/133/secret-invasion-the-complete-event) and [publisher Iron Man issue metadata](https://www.marvel.com/comics/issue/32779/invincible_iron_man_2008_25_iron_man_by_design_variant/iron_man_by_design_variant), used only for namespace corroboration. No issue/year aliases or other-format contents were published.

## Final wording corrections

A final editorial pass caught three unnecessary expansions in my already published wording. A separate guarded transaction changed Jennifer Walters to the source's Jen, removed future from an Avengers America setting that the target description does not explicitly date, and changed Other stories involve to The collection also features for Fantastic Four's concluding subject list. These corrections add no new facts or inference. Prior drafts, decisions and receipts remain intact. A similar name expansion from Tony to Tony Stark was removed before the third batch's publication; its earlier staging and append-only decision history are preserved.

A review preparation script initially selected the compact worker queue rather than the full exported review queue. The invalid pre-staging artifact and v1 script were saved and corrected before decisions or publication; no model call was repeated. This harness error is distinct from the zero production worker failures. The initialization exclusion was a working guard, not a bypass or automatic approval.

## Final verification and local server

**Five publication transactions** form a verified receipt/backup chain from the original 342-synopsis baseline to the final 377. The audit verifies all frozen packet/code hashes, model prompts and literal selections, manual-source provenance, source acquisition HTML hashes, review citations, canonical data and intended record changes. Earlier approvals and unrelated fields remain intact. Only one new metadata record was initialized, with unknown fields preserved as unknown. The final three corrections alter only their intended summaries and review provenance.

Public, built and actual HTTP-served enrichment bytes agree. Localhost was down at session start, was restarted, and its home page, health endpoint and enrichment response were checked. The site is available at [localhost:5173](http://localhost:5173/). The legacy collector remains paused and no remote deployment occurred.

Final audit: data/local-ai-trials/continued-20261105c/final-verification.json. Current handoff: continued-20261105c/next-session-priorities.json. The earlier [50-edition checkpoint](enrichment-continuation-2026-11-05.md) remains a historical snapshot. The published-editions file records 35 unique new approvals; synopsis-fidelity-three-20261105 records three corrections without double-counting them.

## New approved editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302934989 | Strikeforce Vol. 2: Fight Me: Issues #6-9 | revise |
| 9781302527105 | Strange Academy: Year Two | revise |
| 9781302944537 | Punisher Vol. 1: The King of Killers Book One: Issues #1-6 | revise |
| 9781302936976 | Ghost Rider: Robbie Reyes - The Complete Collection: Issues #1-12 | revise |
| 9781302938062 | Marvel: Issues #1-6 | revise |
| 9781302369033 | Avengers: The Initiative Vol. 3: Secret Invasion: Issues #14-19 | accept |
| 9781302488703 | Vision Vol. 1: Little Worse Than A Man: Issues #1-6 | revise |
| 9781302368982 | Avengers Arena Vol. 1: Kill or Die: Issues #1-6 | revise |
| 9781302499198 | Deadpool: World's Greatest Vol. 8: 'Till Death Do Us…: Issues #28-29 | revise |
| 9781302506551 | X-Men: Phoenix in Darkness by Grant Morrison: Issues #146-154 | revise |
| 9781302529543 | Avengers: Twilight: Issues #1-6 | revise |
| 9781302508098 | What If? Classic: The Complete Collection Vol. 1: Issues #1-12 | revise |
| 9781302499839 | Moon Knight Vol. 3: Birth and Death: Issues #10-14 | accept |
| 9781302516208 | Cosmic Ghost Rider Destroys Marvel History: Issues #1-6 | revise |
| 9781302496531 | Death Of X: Issues #1-4 | revise |
| 9780785187400 | Fear Itself: Avengers | revise |
| 9781302503703 | America Vol. 2: Fast and Fuertona: Issues #7-12 | revise |
| 9781302484507 | Siege: Battleworld: Issues #1-4 | revise |
| 9781302479701 | Spider-Man: Nothing Can Stop The Juggernaut: Issues #224-230 | revise |
| 9780785180203 | Moon Knight Vol. 1: The Bottom: Issues #1-6 | revise |
| 9781302531980 | Fantastic Four by Ryan North Vol. 5: Aliens, Ghosts and Alternate Earths: Issues #23-28 | revise |
| 9781302526931 | Fantastic Four by Ryan North Vol. 2: Four Stories About Hope: Issues #7-11 | revise |
| 9781302936938 | Dead Man Logan: The Complete Collection: Issues #1-12 | revise |
| 9781302506537 | Doctor Strange By Donny Cates Vol. 2: City of Sin: Issues #386-390 | revise |
| 9781302526047 | She-Hulk by Rainbow Rowell Vol. 3: Girl Can't Help It: Issues #11-15 | revise |
| 9781302526498 | Star Wars: The Mandalorian: Season Two, Part One: Issues #1-4 | revise |
| 9781302535575 | Spider-Man & Wolverine Vol. 1: The Janus Directory: Issues #1-5 | revise |
| 9781302499679 | Iron Fist Vol. 1: The Trial of the Seven Masters: Issues #1-5 | revise |
| 9781302940171 | Hawkeye by Fraction & Aja: The Saga of Barton and Bishop | revise |
| 9780785178446 | The Invincible Iron Man Vol. 5: Stark Resiliant Part 1: Issues #25-28 | revise |
| 9781302510541 | The Unstoppable Wasp: G.I.R.L. Power: Issues #1-8 | revise |
| 9781302526849 | Avengers: Beyond: Issues #1-5 | revise |
| 9781302527792 | X-Men Red by Al Ewing Vol. 4: Issues #14-18 | revise |
| 9781302499921 | Wolverine: Old Man Logan Vol. 5: Past Lives: Issues #19-24 | revise |
| 9781302532543 | Storm Vol. 1: Earth's Mightiest Mutant: Issues #1-5 | revise |
