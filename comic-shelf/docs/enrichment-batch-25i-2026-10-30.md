# Qwen enrichment batch 25i — October 30, 2026

Reviewed 25 fresh cached ISBN editions using the unchanged original Qwen3.5-4B sentence selector. Seven synopsis improvements were published locally: two unchanged Qwen selections and five source-backed Codex revisions. Four stronger existing editorials were retained; fourteen editions remain held. There are now 93 approved synopsis overlays.

The worker, prompt, parser and model settings were unchanged. This batch still needed substantial editorial correction; it does not demonstrate improved autonomous drafting. Decisions identify Codex as the source assessor under user delegation, not independent human adjudication. No correction is counted as an unchanged Qwen pass.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302379810 | Guardians of the Galaxy by Jim Valentino Vol. 2: Issues #8-20 | Unchanged Qwen selection |
| 9781302482527 | Magneto Vol. 4: Last Days: Issues #18-21 | Unchanged Qwen selection |
| 9781302503826 | Runaways by Rainbow Rowell & Kris Anka Vol. 1: Find Your Way Home: Issues #1-6 | Source-backed Codex revision |
| 9781302938796 | Heroes Reborn: America's Mightiest Heroes Companion Vol. 2 | Source-backed Codex revision |
| 9781302013707 | Iron Man Vol. 1: Believe: Issues #1-5 | Source-backed Codex revision |
| 9781302490461 | Marvel Masterworks: Captain America Vol. 3: Issues #101-113 | Source-backed Codex revision |
| 9781302514709 | Hawkeye: Private Eye: Issues #1-12 | Source-backed Codex revision |

Runaways was revised to describe the return of a member and unresolved relationships without assigning the return to a named character or inventing its mechanism. Heroes Reborn Companion now represents all five one-shot threads. Iron Man names Tony and the Extremis mission without attributing an invention to him. Captain America removes creator praise and avoids treating a death/return teaser as a permanent outcome. Hawkeye replaces reader-directed praise with Kate Bishop, the setting and the unresolved crime/past challenges.

## Research and unresolved findings

Fresh public OverDrive records were accepted for three exact ISBNs. Guardians originally supplied only a 1990 #8–20 contents list. Its distributor record confirms exactly the same year and issue set and supplies the World of Mutants/Rancor, Dark Phoenix and later cosmic encounters. A separate one-edition frozen Qwen follow-up added that source and produced the published selection unchanged. The original contents-only result remains intact. This is one additional processing case, not a twenty-sixth fresh edition.

Avengers/Defenders War remains held: both the Google source and exact-ISBN distributor say Giant-Size (1974) #1 without identifying a particular series. The mechanical parser admitted that generic label; source review added an explicit identity hold rather than guessing which series was intended. Its draft also omitted the primary Avengers/Defenders conflict.

The Marvels remains held despite an exact-ISBN match because the fresh source repeats genre/cast promotion and Kevin Schumer/Threadneedle/KSHOOM teasers without supplying a concrete central mission or conflict. No Siancong plot was inferred from the edition title. Spider-Gwen also retains a draft-context hold for its plot-light Gwenom/mash-up promotion, as well as the unresolved series identity. Other contents, partial-material, annual, suffix and identity blockers were preserved.

## Verification

The 25 fresh editions and one Guardians follow-up completed as 26 cases with zero worker failures and 24 model requests. Worker time totaled 164.76 seconds, excluding review, research and publication. All 53 selected quotations match their frozen sources. Both runs passed packet, Python code and actual request prompt hash checks.

Only the seven intended records and synopsis/provenance/source fields changed. Target summaries still matched the pre-review snapshot at staging; stronger editorials were preserved. Exact backups and final production hashes passed, and localhost:5173/enrichment.json serves byte-for-byte the published payload. All 18 catalog tests and git diff --check passed. No UI build or remote deployment was performed, and unrelated checkout work was preserved.

No new issue membership, character appearances, reading-order completeness or borrowing-availability claims were asserted. Publication updated public and saved-build enrichment JSON plus the canonical approved overlay.

## Artifacts and recovery

data/local-ai-trials/worker-batch-25i-20261030 contains original frozen inputs, results/attempts, source review, edition-research raw pages and acquisition audits, resolved-review-queue.json, review-spec.json, immutable delegated-decisions, approved-staging, publish-receipt and verification.json. worker-25i-guardians-research-20261030 preserves the augmented packet, parent/source hashes, raw model response and review output. data/approved-synopses.json retains the approved overlay. The latest receipt holds exact pre-publication backups and refuses rollback over newer publication changes.

## All edition decisions

| ISBN | Edition | Decision | Rationale |
| --- | --- | --- | --- |
| 9781302379810 | Guardians of the Galaxy by Jim Valentino Vol. 2: Issues #8-20 | accept | Fresh exact-ISBN source recovered missing plot; unchanged follow-up Qwen selection covers the original Guardians, Rancor/Dark Phoenix and later cosmic encounters. Original and fresh sources agree on 1990 #8-20. |
| 9781302939335 | Silk: Out Of The Spider-Verse Vol. 3: Issues #9-19 | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, no_inventory |
| 9781302940195 | Amazing Spider-Man: Beyond Vol. 1 | reject | Retain the existing useful editorial or previously approved synopsis; the new selection is not a clear improvement. |
| 9781302485511 | Black Panther By Christopher Priest: The Complete Collection Vol. 3: Issues #36-49, 57-58 | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, contents_unresolvedEntries |
| 9781302530211 | Amazing Spider-Man: Blood Hunt: Issues #1-3 | reject | Retain the existing useful editorial or previously approved synopsis; the new selection is not a clear improvement. |
| 9781302378554 | Indestructible Hulk Vol. 4: Humanity Bomb | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, contents_unresolvedEntries, no_inventory, no_synopsis |
| 9781302482527 | Magneto Vol. 4: Last Days: Issues #18-21 | accept | Unchanged Qwen selection clearly names Magneto, his extinction-prevention mission and Sugar Man/Polaris conflict while preserving the source question about salvation. |
| 9781302503710 | Avengers Epic Collection: The Avengers/Defenders War | needs_research | Hold unresolved edition/source/draft blockers: ambiguous_collected_series_identity |
| 9781302520335 | X-Men by Jonathan Hickman Vol. 1: Issues #1-6 | reject | Retain the existing useful editorial or previously approved synopsis; the new selection is not a clear improvement. |
| 9781302941710 | Jane Foster: The Saga of the Mighty Thor | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, partial_material_requires_review |
| 9781302500153 | Spider-Gwen Vol. 4: Predators: Issues #19-23 | needs_research | Hold unresolved edition/source/draft blockers: bibliographic_series_identity_requires_review, draft_context_requires_review |
| 9781302944049 | Iron Fist: The Shattered Sword: Issues #1-5 | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, no_inventory |
| 9781302480646 | Avengers: Hawkeye: Issues #1-4 | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, contents_unresolvedEntries |
| 9781302940430 | The Marvels Vol. 1: The War In Siancong: Issues #1-6 | needs_research | Hold unresolved edition/source/draft blockers: source_plot_context_requires_research |
| 9780785179030 | What If? Secret Invasion | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, no_inventory |
| 9781302503826 | Runaways by Rainbow Rowell & Kris Anka Vol. 1: Find Your Way Home: Issues #1-6 | revise | Replace unintroduced she, reader hype and isolated romance questions with a neutral source-backed premise. Do not identify the returning member, explain the return mechanism, or resolve either relationship. |
| 9781302938796 | Heroes Reborn: America's Mightiest Heroes Companion Vol. 2 | revise | Represent all five one-shot threads rather than only Elektra/Luke Cage; remove sales language and add no cause of death, victory or reunion. |
| 9781302504083 | Black Widow: The Sting of the Widow: Issues #1-8 | needs_research | Hold unresolved edition/source/draft blockers: contents_conflict, no_inventory |
| 9781302532642 | Moon Knight: Fist of Khonshu Vol. 1 - Leave Home: Issues #0-5 | reject | Retain the existing useful editorial or previously approved synopsis; the new selection is not a clear improvement. |
| 9781302508678 | Captain America by Ta-Nahesi Coates Vol. 1: Winter in America: Issues #1-6 | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed |
| 9781302013707 | Iron Man Vol. 1: Believe: Issues #1-5 | revise | Replace the unclear his-greatest-invention opening with an explicit Tony Stark/Iron Man subject, the rogue-Extremis mission and armor objective. Do not infer who invented Extremis or claim the mission succeeds. |
| 9781302516987 | Silver Surfer Epic Collection: When Calls Galactus | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed |
| 9781302535971 | Venom Modern Era Epic Collection: Sting of the Scorpion | needs_research | Hold unresolved edition/source/draft blockers: contents_unparsed, no_inventory |
| 9781302490461 | Marvel Masterworks: Captain America Vol. 3: Issues #101-113 | revise | Retain the Red Skull/nuclear dilemma and major battles/personal history while removing creator advertising. Do not convert the death/return teaser into a definite permanent outcome. |
| 9781302514709 | Hawkeye: Private Eye: Issues #1-12 | revise | Replace reader-directed favorite-character praise with the named protagonist, setting and unresolved crime/past challenges. Add no unmentioned case, villain, job title or resolution. |
