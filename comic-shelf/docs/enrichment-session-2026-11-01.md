# Timed enrichment session — November 1, 2026

Published 25 reviewed synopses, increasing the approved total from 133 to 158. Two were recovered from the held backlog; 23 came from 50 new ISBN editions. Seven publications are unchanged Qwen selections and 18 are explicit source-backed Codex revisions. Publication occurred in three guarded packages, each with exact rollback backups and served-byte verification.

| Work | New ISBNs | Published | Unchanged Qwen | Revised | Still held in that review |
| --- | ---: | ---: | ---: | ---: | ---: |
| Parser recovery | 0 | 2 | 0 | 2 | 1 reviewed range mismatch |
| First sustained batch | 25 | 11 | 4 | 7 | 14 |
| Second sustained batch | 25 | 12 | 3 | 9 | 13 |

The first batch includes one extra Deadpool source-recovery execution. Across both batches there were 51 worker executions, 50 model requests and zero worker failures. The two held-edition recoveries reused their immutable original Qwen proposals because candidate inputs were unchanged; no redundant model requests were made. All 115 selected model quotations are literal source text.

These are Codex editorial/source assessments under user delegation, not independent human gold labels or a general accuracy estimate. Publication counts include corrected drafts. Source-blocked drafts were not uniformly scored for prose quality, so the publication ratio is not an overall Qwen acceptance rate. The original single-pass sentence-selection policy remains the default; no experimental block, rewriting or audit policy was enabled.

## Parser fixes and safety gates

The parser now handles a redundant hash on a range endpoint, such as #310–#313, without changing the literal evidence or filling gaps. The same grammar applies to shorthand and disjoint ranges. Missing years remain unresolved; partial scope stays partial; decimals, variants, reversed ranges and oversized ranges remain blocked.

Question marks inside a title before an explicit issue introducer no longer truncate collecting statements such as What If…? Venom #1–5. The punctuation mask is reversible and does not invent missing years or issue numbers. This recovered What If? Age of Ultron and What If…? Venom for explicit source/edition review. Both were revised and published after independent namespace corroboration. Uncanny Inhumans also became parseable, revealing #11–13 against a catalog title saying #11–14. A new range-disagreement gate keeps that discrepancy held instead of treating successful parsing as approval.

Source review of New X-Men Companion exposed a separate safety bug: And Material From was interpreted as part of a series name, causing partial contributions to appear whole. The final parser, version 23, recognizes that conjoined scope marker and preserves subsequent partial entries and inherited gaps. Regression tests cover both the corrected series identity and its extent. A search of saved raw results found the same artificial prefix in three editions: New X-Men Companion, Ant-Man/Giant-Man: Ant-Man No More and Ms. Marvel: The Woman Who Fell to Earth. All three remain unpublished and now retain correct partial scope under the current parser.

The final partial-scope fix was added after the model batches. Their version-22 code archives and original results remain unchanged. Only edition_trial.py and its test file differ from those frozen archives. Final verification confirms that every inventory associated with the 23 newly published batch synopses is unaffected by this later fix; the three affected editions stayed held throughout. No published issue keys, appearances or reading-order mappings were rewritten.

## Source findings

What If? Age of Ultron gained an accepted exact-ISBN distributor corroboration of the 2014 series and #1–5 range. What If…? Venom's failed distributor lookup remains failed; [Marvel's original 2024 issue metadata](https://www.marvel.com/comics/issue/114867/what_if_venom_2024_1_variant/variant), returned as a short web-indexed excerpt, corroborates the namespace only. The original exact-ISBN collecting statement establishes membership. Revisions distinguish the alternate-history/alternate-host premises from canonical introductory copy and promotional language.

Captain Marvel: Down remains held after two distributor records sharing the requested ISBN described incompatible editions: one matches the Monica Rambeau/weakening-powers #7–12 description, while another describes the 2014 #12–15 Haffensye/Black Vortex storyline. Matching an ISBN was not treated as sufficient proof. Both downloaded records, their identifier evidence and the failed aggregate reconciliation remain preserved. Publisher collection metadata also presents a range that needs reconciliation; no issue was silently added or removed.

Deadpool: World's Greatest Vol. 5 gained a better exact-ISBN description that explicitly describes team hostility, Madcap's revenge and the future daughters' contest. One additional Qwen request used that intact replacement source. Its draft still omitted a distinct thread and needed revision; the final synopsis preserves the conflict instead of reading the earlier ironic assurances of teamwork literally. This is source recovery, not evidence that the original model became more accurate.

Other unresolved source conflicts, missing inventories, unspecified partial material and edition mismatches remain in the backlog. The known reviewed backlog is now 181 editions: the previous 156, minus two recoveries, plus 27 new holds. This excludes books not yet reviewed. Uncanny Inhumans retains its newly surfaced range discrepancy, and New X-Men Companion is explicitly blocked despite the older raw parser's clean status.

## Validation and runtime

All 366 Python tests and 18 catalog tests passed. The final audit checked source packets, original model inputs, prompt hashes, literal quotations, frozen code archives, current parser behavior and publication receipts. The three publication backup chains link exactly. A full comparison against the 133-overlay starting payload confirms that only the 25 intended records changed, limited to summary, review provenance and source fields. Other records and fields are unchanged. The local server serves the exact final payload; no remote deployment occurred.

Total worker processing was 1,202.47 seconds, excluding research and review. Median case processing was 6.25 seconds. One Ant-Man/Giant-Man case took 891.28 seconds despite a small 364-token prompt, eight completion tokens and thinking off. It completed successfully, but its cause is not established. That outlier accounts for most of the second batch's runtime and must not be described as normal throughput or attributed to a large context without evidence.

## Reviewable artifacts

The aggregate audit is data/local-ai-trials/timed-session-20261101/final-verification.json. That directory also contains published-editions.json, published-table.md, scope-fix-audit.json, latency-note.json, backlog-summary.json and the latest known-held.json. The backlog records both historical manual holds and current parser flags; it does not silently approve entries whose syntax changed. Overlapping flag counts are triage aids, not independent edition counts or automatic clearance rules.

Parser replay, the preserved version-20 baseline, source research and the two recovery decisions are in parser-recovery-20261101. The raw inference and immutable review histories are in sustained-25a-20261101 and sustained-25b-20261101. The source-only Deadpool retry is sustained-deadpool-followup-20261101. The second batch was restaged after the first publication so its payload includes the first batch's new synopses; the older unpromoted package remains preserved.

Each promoted package has a publish-receipt directory with exact backups. Old receipts are historical: rollback must not overwrite a later publication. All model outputs remain drafts until explicit review. The next productive work is targeted source research and bounded drafting, with separate tracking of unchanged selections, editorial revisions and source eligibility.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302480486 | What If? Age Of Ultron: Issues #1-5 | Source-backed revision |
| 9781302530389 | What If…? Venom: Issues #1-5 | Source-backed revision |
| 9781302523114 | Black Panther by Ta-Nehisi Coates Vol. 3: The Intergalactic Empire of Wakanda Part One: Issues #1-12 | Unchanged Qwen selection |
| 9781302535407 | New Avengers Vol. 1: Killuminati: Issues #1-5 | Source-backed revision |
| 9781302529109 | Doctor Strange By Mark Waid Vol. 2 | Source-backed revision |
| 9781302938246 | Generation X Epic Collection: Back to School | Unchanged Qwen selection |
| 9781302485351 | Figment 2: Legacy of Imagination: Issues #1-5 | Source-backed revision |
| 9781302936112 | Luke Cage Epic Collection: Retribution: Issues #1-16 | Source-backed revision |
| 9781302520359 | Death of Wolverine Prelude: Three Months to Die: Issues #1-12 | Unchanged Qwen selection |
| 9781302520106 | Star Wars Vol. 13: Rogues and Rebels: Issues #73-75 | Source-backed revision |
| 9781302526139 | X-Men by Gerry Duggan Vol. 4: Issues #19-24 | Unchanged Qwen selection |
| 9781302526351 | Iron Man Epic Collection: The War of the Super Villains | Source-backed revision |
| 9781302494803 | Deadpool: World's Greatest Vol. 5: Civil War II: Issues #14-19 | Source-backed revision |
| 9781302510084 | Fantastic Four Vol. 1: Fourever: Issues #1-4 | Source-backed revision |
| 9781302520762 | Punisher: Soviet: Issues #1-6 | Source-backed revision |
| 9781302502003 | Doctor Strange Vol. 5: Secret Empire: Issues #21-26 | Source-backed revision |
| 9781302377328 | She-Hulk Vol. 2: Superhuman Law: Issues #7-12 | Source-backed revision |
| 9781302498184 | Fantastic Four Epic Collection: The Master Plan of Doctor Doom: Issues #19-32 | Unchanged Qwen selection |
| 9781302499150 | Captain America: Sam Wilson Vol. 5: End Of The Line: Issues #18-21 | Source-backed revision |
| 9781302938475 | Captain America Epic Collection: The Captain | Unchanged Qwen selection |
| 9781302495534 | The Thing Classic Vol. 1: Issues #1-10 | Source-backed revision |
| 9781302536015 | Wolverine and Kitty Pryde: Issues #1-5 | Unchanged Qwen selection |
| 9781302930349 | King in black: Avengers | Source-backed revision |
| 9781302505943 | Amazing Spider-Man: Red Goblin: Issues #794-801 | Source-backed revision |
| 9780785170181 | Captain America: The Death Of Captain America Vol. 1: The Death Of The Dream: Issues #25-30 | Source-backed revision |
