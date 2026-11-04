# Second twenty-five-edition enrichment batch

October 30, 2026. Processed 25 new cached ISBN editions sequentially with Qwen3.5-4B. Zero worker failures; total per-edition processing time 141.05 seconds, excluding review/research. All 63 model-selected evidence quotations match their source packets. Inputs and worker code were frozen; no prompt, model or parser changes occurred during this batch.

## Outcome

Eight synopsis improvements published locally; twelve editions held for research; five existing editorial summaries retained. There are now 28 approved synopsis overlays total. Two publications retain Qwen selections and six are source-backed assistant corrections. Decisions record the user's delegated authorization and Codex as assessor, not independent human review.

| Published edition | Treatment |
| --- | --- |
| West Coast Avengers: Best Coast / 9781302508722 | Corrected fragment-led selection to name Kate Bishop, Clint Barton and the giant-Tigra threat. |
| Superior Iron Man: Infamous / 9781302480066 | Corrected context to establish San Francisco, Extremis and Daredevil's opposition. |
| Deadpool vs. the Marvel Universe / 9781302013936 | Corroborated provisional series identity and corrected the source's broken trailing character in a concise synopsis. |
| Star Wars: Quests of the Force / 9781302525712 | Retained Qwen's self-contained lost-Rebels/Luke quest selection. |
| Invincible Iron Man: Civil War II / 9781302496180 | Corrected synopsis to include Riri's armor transition and the collected Mighty Avengers/Doom material. |
| Luke Cage: The Fire This Time / 9781302527259 | Replaced pronoun-led selection with explicit Luke Cage, 1970s setting, threats and Bill Foster context. |
| Marvel-Verse: Wonder Man / 9781302527600 | Neutral synopsis of Simon Williams' powers, Avengers conflict, Hollywood and Beast friendship; removed publisher superlatives. |
| Star Wars: The Destiny Path / 9781302523282 | Retained Qwen's Han/Luke/Rebel-reunion premise. |

All changes apply to synopsis/provenance/source fields only. No new issue membership, character index, reading-order completeness, borrowing availability or continuity mapping was asserted.

## Source investigations and disagreements

Three public OverDrive ISBN lookups attempted. Black Widow and the Marvel Girls returned no validated record. Ultimate New Ultimates and Deadpool returned exact-ISBN metadata, preserved with raw pages, hashes and identifier paths.

Deadpool's source explicitly collects Cable & Deadpool #43–50 and labels the series Cable/Deadpool (2004), corroborating Google Books year 2004 for the same ISBN. The title-format variation is documented for this edition; no global alias rule was added. Only its provisional series-review reason was resolved in a new queue.

Ultimate New Ultimates still has unresolved year/title formatting and no accepted inventory; a distributor match alone did not clear its blockers.

Editorial review also identified two explicit catalog/source scope disagreements: Agents of S.H.I.E.L.D. says #1–6 in the catalog versus #1–5 plus Point One material in the source; Carnage says #6–10 versus #6–11. Both were held with explicit added flags in the resolved review queue. The automatic range comparison misses the no-hash Carnage collecting statement. No gate was bypassed and no range silently reconciled; improving range detection remains future work requiring regression tests.

## Held and retained editions

| Edition | Disposition |
| --- | --- |
| Agents of S.H.I.E.L.D.: The Coulson Protocols | Held: scope disagreement and unresolved/partial contents |
| Carnage: World Tour | Held: #6–10 versus #6–11 disagreement and provisional identity |
| Thor: The World Eaters | Held: unparsed contents |
| Rom Epic Collection Vol. 2 | Held: unparsed/unresolved contents |
| New X-Men: Planet X | Retained existing editorial synopsis |
| Dawn of X Vol. 11 | Held: partial material |
| New Ultimates: Thor Reborn | Held: unresolved inventory despite matched distributor evidence |
| Generation X: Emplate's Revenge | Held: unparsed annual/preview contents |
| X-Men Legends: Mutant Mayhem | Retained existing editorial synopsis |
| Black Widow and the Marvel Girls | Held: unresolved inventory and unsuccessful fresh acquisition |
| Uncanny X-Men Masterworks Vol. 3 | Retained existing editorial synopsis |
| Predator: The Theta Saga | Held: unparsed/unresolved multi-series contents |
| Deadpool Classic: Killogy | Held: unparsed/unresolved inventory |
| Uncanny X-Men: Waking from the Dream | Retained existing editorial synopsis |
| X-Men Red Vol. 2 | Retained existing editorial synopsis |
| Deadpool vs. Wolverine | Held: unparsed/unresolved mixed contents |
| Spider-Island: Warzones! | Held: no accepted inventory |

## Verification

All eighteen catalog tests pass. Exactly eight records changed; all unrelated records, earlier publications and other fields within changed records are preserved. Target, rollback-backup and original packet hashes pass. All eight published summaries were checked in the running browser. Needs-review labels remain because other enrichment fields remain unapproved.

Artifacts in `data/local-ai-trials/worker-batch-25b-20261030/`: frozen inputs and full attempts; original/resolved review queues; source acquisition evidence; delegated decisions; staging preview/diff; publication receipt and backups; `publication-audit.json`; `published-destiny-path.png`. The update is local at http://localhost:5173/ only. No remote deployment or automatic schedule was created.
