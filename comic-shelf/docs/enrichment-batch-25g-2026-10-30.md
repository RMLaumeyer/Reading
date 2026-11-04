# Qwen enrichment batch 25g — October 30, 2026

Reviewed 25 fresh cached ISBN editions with the original Qwen3.5-4B sentence-selection method. Six synopsis improvements were published locally, fifteen editions remain held for research, and four stronger existing editorials were retained. There are now 75 approved synopsis overlays.

Two published summaries retain Qwen selections unchanged. Four are source-backed Codex corrections, explicitly recorded as revisions. This batch does not show improved autonomous drafting reliability. The worker and publication code, prompt and model settings were unchanged. Source assessment and decisions identify Codex under user delegation, not independent human review.

| Published edition | ISBN | Treatment |
| --- | --- | --- |
| Thor By Jason Aaron: The Complete Collection Vol. 3 | 9781302938161 | Revised to establish Jane Foster, Mjolnir and the personal/wider conflicts |
| Venomverse | 9781302501723 | Original Qwen selection unchanged; edition identity corroborated |
| Star Wars: Jedi Knights Vol. 2: A Higher Path | 9781302535704 | Revised to include the antidote mission and separate Soona story |
| Daredevil By Chip Zdarsky Vol. 4: End of Hell | 9781302522124 | Original Qwen selection unchanged |
| Monica Rambeau: Photon | 9781302525644 | Revised to restore the cosmic delivery and remove advertising |
| Black Widow Vol. 2: The Tightly Tangled Web | 9781302478520 | Fresh source and separate Qwen follow-up; revised to identify the Punisher and restore collection context |

## Research and blockers

Black Widow originally had only an issue list and no model synopsis. Fresh public OverDrive metadata matched the exact ISBN, Black Widow (2014) series and the union of Black Widow #7–12 plus Punisher (2014) #9. A new, separate frozen input retained the original Google source and added this exact-ISBN description; Qwen processed it with the same selector. Its original batch result remains unchanged. The follow-up supplied plot evidence, but the selected Frank/Natasha oil-rig sentence lacked its Punisher setup, so the final summary was explicitly revised. Only the provisional identity reason was resolved manually; no-synopsis disappeared through the actual new source/model run.

Venomverse's strict distributor acquisition remained failed because its two ISBN-matched descriptions differed in apostrophe/replacement-character encoding. Individual cached records were inspected without another request. Both explicitly identify Venomverse (2017) and #1–5. Their independently parsed issue sets match the original Google inventory. Manual resolution used only unanimous ISBN/year/issue evidence; neither description was normalized, merged or selected as a plot source. The published synopsis remains the original Google-backed Qwen selection. The failed acquisition audit is preserved.

Two explicit issue-range disagreements were added as review blockers: Deadpool What Happened in Vegas says #23–26 in the catalog but #23–27 in the description, and Uncanny Inhumans Civil War II says #11–14 versus #11–13. Neither was reconciled or published. All other unresolved inventory, partial-material and identity flags remain blocking. No global series alias or parser behavior changed.

## Verification

The 25 fresh editions plus one research follow-up produced 26 processed cases and 24 model requests, with zero worker failures. This is 25 distinct editions, not 26 fresh books. Worker time totaled 161.65 seconds, excluding source research, review and publication. All 60 selected evidence quotations match their frozen source text.

Packet hashes, frozen Python code hashes and actual request prompt hashes passed for both runs. Stage comparisons confirm only the six intended records and synopsis/provenance/source fields changed. Existing summaries were checked against the pre-review snapshot, all stronger editorials remained untouched, exact backups and production hashes passed, and localhost:5173/enrichment.json served byte-for-byte the published payload. All 18 catalog tests and git diff --check passed. No UI build was required.

No new issue membership, character appearance, reading-order completeness or borrowing availability claim was asserted. Changes were local; no remote deployment occurred. Existing unrelated work in the checkout was preserved.

## Artifacts and recovery

data/local-ai-trials/worker-batch-25g-20261030 preserves the 25 frozen packets, original results, source review, research pages/acquisition audits, individual Venomverse records, resolved-review-queue.json, review-spec.json, immutable delegated-decisions, approved-staging, publish-receipt and verification.json. The separate worker-25g-widow-research-20261030 directory preserves the one-case augmented packet, parent/source hashes, raw model response and review output. Approved overlays are stored in data/approved-synopses.json. The latest receipt contains exact pre-publication backups and refuses to overwrite newer changes during rollback.

## Edition decisions

| ISBN | Edition | Decision | Rationale |
| --- | --- | --- | --- |
| 9781302494780 | Black Widow: Web of Intrigue | needs_research | Hold unresolved edition/source blockers: contents_unparsed, contents_unresolvedEntries |
| 9781302513306 | Gambit: King of Thieves - The Complete Collection: Issues #1-17 | needs_research | Hold unresolved edition/source blockers: contents_unparsed, contents_unresolvedEntries |
| 9781302479268 | Ms. Marvel Vol. 2: Generation Why: Issues #6-11 | needs_research | Hold unresolved edition/source blockers: contents_unparsed, no_inventory, no_synopsis |
| 9781302515522 | Spider-Gwen: Ghost-Spider Vol. 2: Impossible Year: Issues #5-10 | needs_research | Hold unresolved edition/source blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 9781302944735 | Fantastic Four by Dan Slott Vol. 3: Issues #21-30 | needs_research | Hold unresolved edition/source blockers: contents_unparsed |
| 9781302369064 | Captain America By Ed Brubaker Vol. 4: Issues #15-19 | needs_research | Hold unresolved edition/source blockers: no_inventory |
| 9781302938161 | Thor By Jason Aaron: The Complete Collection Vol. 3: Issues #1-19 | revise | Restore Jane Foster's name and Thor/Mjolnir setup absent from the selection; retain the personal and wider war conflicts without claiming an outcome. |
| 9781302949679 | Miles Morales: the avenging Avenger! | needs_research | Hold unresolved edition/source blockers: contents_unparsed |
| 9781302488536 | Infinity Watch Vol. 2: Issues #26-42 | needs_research | Hold unresolved edition/source blockers: contents_conflict, no_inventory |
| 9780785178866 | Nextwave Vol. 1: This is What They Want: Issues #1-6 | needs_research | Hold unresolved edition/source blockers: contents_unparsed, contents_unresolvedEntries, no_inventory |
| 9781302478520 | Black Widow Vol. 2: The Tightly Tangled Web: Issues #7-12 | revise | Fresh exact-ISBN source adds the missing plot. Correct follow-up selection's unintroduced Frank, restore the Winter Soldier setup and retain X-23/Howling Commandos material. Do not decide Punisher alliance or oil-rig outcome. |
| 9781302940683 | Reign of X Vol. 9 | needs_research | Hold unresolved edition/source blockers: contents_unparsed |
| 9781302523800 | X-Men by Gerry Duggan Vol. 3: Issues #13-18 | reject | Retain the existing useful editorial or previously reviewed synopsis; the new selection is not a clear improvement. |
| 9780785179580 | Deadpool Vol. 5: What Happened In Vegas: Issues #23-26 | needs_research | Hold unresolved edition/source blockers: bibliographic_series_identity_requires_review, catalog_description_issue_range_disagreement |
| 9781302496159 | Extraordinary X-Men Vol. 3: Kingdom Falls: Issues #13-16 | reject | Retain the existing useful editorial or previously reviewed synopsis; the new selection is not a clear improvement. |
| 9781302501723 | Venomverse: Issues #1-5 | accept | Source-reviewed original Qwen selection supplies a self-contained named protagonist and central conflict without adding an outcome; no unresolved edition flags. Preserve the generated text unchanged. |
| 9780785179290 | Dark Reign: The Sinister Spider-Man: Issues #1-4 | reject | Retain the existing useful editorial or previously reviewed synopsis; the new selection is not a clear improvement. |
| 9781302520977 | Heroes Reborn: Captain America: Issues #1-12 | needs_research | Hold unresolved edition/source blockers: contents_unparsed |
| 9781302495107 | Uncanny Inhumans Vol. 3: Civil War Ii: Issues #11-14 | needs_research | Hold unresolved edition/source blockers: contents_unparsed, no_inventory, catalog_description_issue_range_disagreement |
| 9781302535704 | Star Wars: Jedi Knights Vol. 2: A Higher Path: Issues #6-10 | revise | Restore the antidote mission and separate Soona storyline omitted by the three opening excerpts, while removing rhetorical and sales language. No identity of the poisoned Jedi or killer is inferred. |
| 9781302936884 | X-Men/Avengers: Onslaught Vol. 3 | reject | Retain the existing useful editorial or previously reviewed synopsis; the new selection is not a clear improvement. |
| 9781302521813 | Ruins of Ravencroft | needs_research | Hold unresolved edition/source blockers: contents_unparsed, no_inventory |
| 9781302522124 | Daredevil By Chip Zdarsky Vol. 4: End of Hell: Issues #16-20 | accept | Source-reviewed original Qwen selection supplies a self-contained named protagonist and central conflict without adding an outcome; no unresolved edition flags. Preserve the generated text unchanged. |
| 9781302525644 | Monica Rambeau: Photon: Issues #1-5 | revise | Replace biography and reader advertising with the omitted delivery mission and family/reunion conflicts; no named reunion participant or resolution is invented. |
| 9781302528270 | Captain America Epic Collection: The Man Who Sold the United States: Issues #180-200 | needs_research | Hold unresolved edition/source blockers: contents_unparsed |
