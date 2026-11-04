# Longer enrichment and publication-path improvement — November 3, 2026, third block

Published **12 reviewed synopses**, increasing the local approved total from **325 to 337**. Ten came from 25 fresh editions, Daredevil came from a new source-recovery run, and Atlantis Rising came from an existing reviewed draft after implementing a guarded missing-record path. All twelve publications are source-backed editorial revisions. The block improves the pipeline and fills the site; it does not show improved Qwen writing or readiness for autonomous publication.

## Missing-record publication path

Normal staging still rejects missing enrichment records. The new explicit --initialize-isbn option allows only specified, reviewed catalog ISBNs to receive a minimal synopsis-only record. Unique catalog identity, remaining review flags, citations and reviewer authorization still apply. Pages remain unknown; characters, stories and issue keys stay empty; reading order and starting-point status are not inferred. All required display fields are present and the record remains marked basic.

Promotion rebuilds the staged package with the recorded initialization list and verifies the actual change entries as well as payload/input hashes. It writes canonical approved data, public data and preview data through the existing transactional backup path. The canonical patch retains an initialization marker so collector rebuilds can restore the minimal record. If a collector later supplies fuller metadata, approved synopsis fields merge into it without overwriting those other fields. Later synopsis revisions retain the marker.

Tests cover default rejection, explicit initialization, unresolved flags, ambiguous/unknown identity, tampering with initialization and before-state entries, partial write failure, a subsequent ordinary synopsis edit, canonical rebuild and exact rollback. **All 385 Python tests and 18 catalog tests passed.** Five Python files changed: approved_synopses.py, stage_enrichment.py, promote_enrichment.py and the staging/promotion tests. The Qwen worker, original prompt, three-passage limit and parser version 25 are unchanged. Focused before/after hashes and diff are saved; all inference runs were frozen after these changes. See also [operator notes](enrichment-record-initialization.md).

## Atlantis Rising recovered

Rechecked the previously saved exact-ISBN source, original Qwen output, reviewed correction and publisher namespace resolutions. The new explicitly enabled staging package adds exactly one record, for ISBN 9781302500351, instead of bypassing the former exclusion. Its synopsis restores Morgan Le Fay raising Atlantis and the resulting crisis for Namor and the Atlanteans. No chapter, page, character-appearance or ordering annotations were invented.

The record was published locally with exact backups. The audit verifies both its HTTP-served bytes and reconstruction through the canonical approved overlay. The old held package and its zero-change verification remain historical. This was one historical draft review with **zero new inference requests**, not another freshly enriched ISBN.

## Fresh 25-edition review

The fresh Qwen batch completed all 25 cases without worker failures, with 24 recorded model responses, 49 literal selected quotations and 165.06 worker seconds. One issue-only source had no eligible plot excerpts. Ten source-backed revisions were published and fifteen editions remain held. None of the published fresh drafts passed unchanged.

Reviews restore Vision’s family crisis and the reason the Avengers intervene; the Mob’s failed attempt to use Fisk as a trap for Frank Castle; both the Haunted Mansion and Museum of the Weird stories; Kate Bishop’s case, client and fake-Kate mystery; Emma Frost’s club position, investigation and framing; Miles Morales’s Avengers and everyday challenges; Shadow Base’s objective; and the Avengers’ transformation and allies in Mech Strike. They do not assert final victories, identify an unnamed traitor or turn possible dates/study sessions into completed events.

[The publisher’s Miles Morales collection](https://www.marvel.com/comics/collection/55694/spider-man_miles_morales_vol_1_trade_paperback) corroborates the 2016 #1–5 run. Matching Bendis/Pichelli and Miles context distinguishes it from another publisher item labeled Spider-Man (2016) #1 about Peter Parker. [The Mech Strike original #1](https://www.marvel.com/comics/issue/99736/mech_strike_monster_hunters_2022_1) corroborates Gage/Diaz, the 2022 series and the transformation setup. Publisher references establish identity; the frozen target ISBN descriptions supply published plot.

[Squirrel Girl’s same-title publisher collection](https://www.marvel.com/comics/collection/79885/the_unbeatable_squirrel_girl_powers_of_a_squirrel_trade_paperback) explicitly identifies the spaced 2015 A #1–8 statement, resolving a parser limitation without conflating the later 2015 run. The revision covers Doreen’s studies, threats and secret identity; earlier promotional claims about defeated villains are not assigned to these collected issues.

[A publisher dated collecting line](https://www.marvel.com/comics/collection/104950/marvel_masterworks_the_tomb_of_dracula_vol_3_2023) establishes the Dracula Lives 1973 namespace only. The target independently lists #1–4 alongside Tomb of Dracula #1–15. No issues, partial-material modifiers or later plots from that other collection were transferred. The revision covers the vampire hunters and historical horror tales; the source’s question about Blade staking Dracula was not converted into a definite action or successful outcome.

[The same-title Punisher collection](https://www.marvel.com/comics/collection/65944/) corroborates the target’s 2010 collecting label and Aaron/Dillon plot. Its original-series publisher index uses 2009; that label distinction is recorded explicitly, without publishing an original-year alias or issue/order mapping. Spider-Man & the X-Men retains a separate unresolved 2015 target collecting-label versus 2014 original-run hold.

The Ant-Man production art book remains held: its selected film-premise sentence does not summarize the art book. Partial Ghost Rider and Avengers material, unidentified annual/extras, Daken/X-23 contents, and other unresolved edition flags remain. No unsupported metadata was promoted merely because a plot selection was literal.

## Daredevil source recovery

The guarded exact-ISBN lookup for Daredevil: Hell to Pay Vol. 1 (9781302431693) found an intact public-library record with its 1998 #94–99 collecting statement and actual plot. The previous source was issue-only. Original packet and new source hashes, raw pages and ISBN-format evidence are retained.

One local Qwen request completed without failure in 4.81 seconds and selected two literal quotations. The revision restores the threat from Matt’s past, prison/life-on-the-run context, reunion with Milla and post-Civil War relationship pressure. It does not supply a villain, marriage, surname or relationship outcome from memory. This is a previously held ISBN, not an additional fresh edition.

## Input coverage finding for future improvement

Champions: No Time for Losers has a 71-word, 421-character source sentence describing several threats. The current 60-word candidate limit excludes that complete sentence before Qwen; only a formation/cast sentence and generic copy remain, and Qwen abstains. A saved zero-inference diagnostic separates this input limitation from model selection quality. The long sentence also contains creator praise, so admitting it would not itself prove a clean synopsis.

A future bounded experiment can test a modest complete-sentence allowance on length-limited cases, with controls for promotion and coverage. No limits or sentence splitting changed in this block. Do not describe the model’s empty proposal as proof that the full source contains no plot. The existing opening-reference warning remains enabled, with its known bounded scope.

## Closing verification and handoff

The final audit links all three receipt/backup transactions to the 325-synopsis baseline. Exactly twelve intended records changed, including one explicit addition; the other eleven changes are limited to summary, source citations and review provenance. Earlier approvals, unrelated fields and top-level metadata remain intact. Reapplying the current canonical approved overlay to the baseline records exactly reconstructs the final logical book data, including Atlantis Rising. Public, built and actually served bytes agree.

There were **26 new worker cases**, **25 recorded responses**, **51 literal selected quotes** and zero worker failures, plus one historical review without inference. The reviewed backlog is **427 editions**: 414 before, minus two recovered holds, plus fifteen fresh holds. Source/content review is delegated Codex assessment, not independent gold labeling. The legacy collector stays paused and no remote deployment occurred.

Artifacts are in data/local-ai-trials/continued-20261103c, namespace-initialize-atlantis-20261103c, sustained-25s-20261103 and source-recovery-one-20261103c. The fresh publication uses approved-staging-v2 after tightening the Dracula wording; earlier staging and immutable decision history remain preserved. Current handoff candidates and failure histories are in next-session-priorities.json.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302500351 | Fantastic Four/Inhumans: Atlantis Rising | Explicit synopsis-only initialization |
| 9781302522582 | Disney Kingdoms: Haunted Mansion: Issues #1-5 | Source-backed revision |
| 9781302494711 | Vision Vol. 2: Little Better Than A Beast: Issues #7-12 | Source-backed revision |
| 9781302502096 | Punisher MAX: The Complete Collection Vol. 7: Issues #1-22 | Source-backed revision |
| 9781302493370 | Spider-Man: Miles Morales Vol. 1: Issues #1-5 | Source-backed revision |
| 9781302500320 | Tomb Of Dracula: The Complete Collection Vol. 1: Issues #1-15 | Source-backed revision |
| 9781302535094 | Emma Frost: The White Queen - All Hail the Queen: Issues #1-5 | Source-backed revision |
| 9781302517588 | The Unbeatable Squirrel Girl: Powers of a Squirrel: Issues #1-8 | Source-backed revision |
| 9781302501570 | Hawkeye: Kate Bishop Vol. 2: Masks: Issues #7-12 | Source-backed revision |
| 9781302517267 | Immortal Hulk Vol. 5: Breaker of Worlds: Issues #21-25 | Source-backed revision |
| 9781302944506 | Mech Strike: Monster Hunters: Issues #1-5 | Source-backed revision |
| 9781302431693 | Daredevil: Hell to Pay Vol. 1: Issues #94-99 | Source-backed revision |
