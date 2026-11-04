# Source recovery and input-length comparison — November 3, 2026, fourth block

Published **two reviewed source recoveries**, increasing the local approved total from **337 to 339**. Both required explicit source-backed revisions. The reviewed held backlog decreased from **427 to 425**. Separately tested whether a modest input-length allowance restores plot passages hidden from Qwen. It did restore coverage in several cases, but did not produce a synopsis suitable for unchanged publication. Production code and settings remain unchanged.

## Source recoveries

The acquisition-history guard permitted two previously untried exact-ISBN public-library lookups. Both succeeded. Raw search/media pages, acquisition audits, source JSON, format-specific ISBN evidence and hashes are retained. Every downloaded page hash and each selected source cache hash passed closing verification. New packets append the source while preserving their earlier packets and parent hashes.

She-Hulk Vol. 2: Disorderly Conduct (9781302479312) previously supplied only She-Hulk (2014) #7–12. Its new exact-ISBN source provides three plot threads. Qwen selected only the Captain America case. The reviewed revision restores the officemate rescue with Hellcat/Giant-Man and the uncertain Hank Pym agenda, the legal confrontation with Matt Murdock, and the Blue File/Titania thread. Captain America’s guilt, Hank’s intentions and Angie Huang’s fate remain uncertain. No lost character name or outcome was supplied from memory.

Hulk: Visionaries — Peter David Vol. 2 (9781302483449) gained a collecting statement for #340–348. Its older bibliographic label uses Incredible Hulk (1968), while the new exact-ISBN statement uses 1962. [Publisher creator metadata](https://www.marvel.com/comics/creators/1250/jeff_purves) groups high-numbered issues under its 1962–1999 umbrella namespace. The assessment records that distinction for synopsis-only review: the #366 reference does not establish target membership, no alias between dates is created, and no year, issue key or ordering is published. The target source supplies its own membership; both sources agree on the gray Hulk/Leader/Las Vegas plot. The revision removes invincibility hype and retains the source-stated conflict and transition without inventing a mechanism, final winner or specific death.

The two recovery requests completed with zero worker failures, five literal selected quotations and 12.00 worker seconds. Both local publications passed guarded staging, exact backup/receipt checks, parent/source/packet hashes and actual served-byte verification. Earlier approvals and unrelated metadata remain intact. The minimal Atlantis Rising record and its canonical initialization marker were preserved.

## Isolated comparison: 60 versus 90 words

The existing candidate filter rejects source passages above 60 words even when they fit its separate 450-character bound. The experiment changes only that word allowance to 90 inside an isolated runner. It retains the 450-character bound, original prompt, temperature zero, thinking-off setting, three-passage cap, 200-token response budget and complete literal source excerpts. No production script or frozen original result was edited.

Selected five saved development cases whose candidate inputs change under that rule and whose current baseline candidates exactly match their original recorded request. Every old candidate remains available; each treatment adds a source passage previously excluded by length. The manifest, criteria, exact filter implementations, packet/result hashes and treatment inputs were saved before inference. Candidate IDs can shift when a passage is inserted, so comparisons use source quotations and meaning rather than matching numeric IDs.

| Saved case | Observed change | Remaining limitation |
| --- | --- | --- |
| Champions: No Time for Losers | Selects the compound threat passage after baseline abstention | Opens with “Their” without the named team and includes creator advertising |
| Warhammer 40,000: Marneus Calgar | Adds origin/history, Black Altar and the returning threat | Creator credits and promotional wording remain |
| Guardians by Jim Valentino Vol. 1 | Restores the shield quest and Stark/Force opponents while retaining later material | Reader invitation and long cast list still need tightening |
| Marvel’s Voices: Identity | Adds broader anthology coverage after baseline abstention | Praise and creator/reader advertising remain; source detail is limited |
| Cult of Carnage: Misery | Restores Alchemax and Norman/family context | Drops the explicit stolen-Toxin setup, leaving the closing connector dependent on omitted context |

All five requests completed without failure in **27.53 seconds**. All **ten selected quotes** match their frozen sources, and all five outputs select a newly available passage. Delegated review found three coverage gains still requiring editing and two mixed tradeoffs. Neither input policy produced a clean unchanged synopsis under the saved cohort criteria; two baselines were abstentions, not fabricated drafts. These observations are not an accuracy or failure-rate estimate.

Two additional offline checks used the recovery packets as input controls: the 90-word allowance produces exactly the same candidate inputs there. No extra model requests were made for those controls. The experiment outputs were not staged or published, and Misery’s existing approved editorial synopsis was preserved.

Some splitter-produced candidates contain more than one sentence around quoted punctuation. The runner preserves those existing groups and exact bytes; it does not shorten clauses, remove advertising or repair text. More available plot evidence therefore does not itself establish less editorial work. The production limit stays at **60 words**. A future prospective comparison on previously unused editions is needed before considering a general change.

## Verification and handoff

Across both recovery and experiment work there were **seven model requests**, **fifteen literal selected quotations** and zero worker failures. The five experiment cases are historical comparisons and are not five additional newly enriched editions. The two recoveries are previously held ISBNs; no fresh batch was added in this block.

All 78 current Python script hashes match the frozen manifests. Parser version 25, original selector, opening-reference warning and explicit initialization behavior remain unchanged. The earlier 385-Python-test and 18-catalog-test validation remains applicable; those suites were not rerun for this artifact/data-only block. Publication files were unchanged during experiment assessment, then changed only through the two reviewed recoveries. Final public, built and actually served bytes agree. The legacy collector remains paused and no remote deployment occurred.

Next source candidates are Siege: Embedded and New X-Men by Grant Morrison Vol. 2: Imperial, both currently lacking inventory evidence. No prior acquisition audit was found for either at handoff; check again before lookup. Preserve existing failed-lookup histories. A next model-development step can freeze an untouched, input-affected cohort before comparing 60/90-word policies with the same editorial criteria, while treating source identity and publication eligibility separately.

Artifacts: data/local-ai-trials/continued-20261103d and source-recovery-two-20261103d. The continuation folder includes the five-case manifest, exact requests/responses, isolated filter, assessment, source acquisition verification, final-verification.json, known-held.json and next-session-priorities.json.
