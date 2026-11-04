# Second ten-edition enrichment batch — November 1, 2026

Reviewed ten new ISBN editions and published six synopses locally, bringing the approved overlay to 133 editions. Hidden Empire was accepted as an unchanged Qwen selection. Five published synopses required explicit source-backed Codex revisions. Four editions remain held.

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302938444 | Symbiote Spider-Man: King in Black | Revised to remove promotion/speculative alliance wording and retain the shadow-creature threat and earlier Knull context |
| 9781302513283 | Killmonger: By Any Means | Revised using intact exact-ISBN source text to avoid damaged names/contractions and preserve the pre-throne-bid revenge premise |
| 9781302534417 | Wolverine: The Death and Life of Sabretooth | Revised to restore the later Victor Creed/Romulus thread without claiming a permanent death or naming the mysterious woman |
| 9780785182870 | Cable & Deadpool: Paved with Good Intentions | Revised to restore Civil War and Cable's secret Captain America meeting without asserting genuine neutrality |
| 9781302525033 | Star Wars: Hidden Empire | Unchanged Qwen draft covering Qi'ra, Crimson Dawn, Palpatine's response and the threatened Fermata Cage plan |
| 9781302367886 | FF by Jonathan Hickman Vol. 2 | Recovered missing plot from an exact-ISBN source, then revised to include the omitted Kree Supreme Intelligence threat |

## Worker and editorial results

The original ten cases completed without worker failures. FF's original source contained only a collecting statement, so the worker appropriately abstained without making a model request. Source research supplied plot text, and one separate immutable FF retry was made. This is ten unique new editions, eleven worker case executions and ten model requests, not eleven fresh editions.

Total worker processing took 59.78 seconds, excluding research and review. All 21 selected evidence quotations across both runs are literal source text. The first pass had two editorial passes, seven drafts needing revision and one appropriate abstention. Hidden Empire published unchanged; the other passing draft, Jessica Jones: Avenger, remains blocked by edition evidence. The recovered FF draft still needed a coverage revision. These are Codex development judgments under user authorization, not independent human gold labels or a general model-accuracy estimate.

Only the original sentence-selection policy was used. No extra audit pass, block mode or free-form model rewrite ran. Production worker/parser code did not change.

## Source and manual contents review

Killmonger's two cached exact-ISBN distributor records agree on the 2018 label, #1–5 contents and substantive description. Ellipsis typography differs, so the strict aggregate acquisition remains failed. One intact record supplied complete name/punctuation evidence for review; no merged description was created or passed to the model.

Cable & Deadpool's accepted exact-ISBN distributor metadata uses the spelling Cable/Deadpool (2004), with matching #30–36 contents. Manual punctuation/name assessment corroborates the original 2004 identity for this edition only. No global alias or issue expansion was added.

FF's two exact-ISBN distributor records have identical plot descriptions and #6–11 contents but disagree on the year label: FF (2011) versus FF (2010-2012). Both labels and the failed aggregate check remain preserved. The source-recovery packet explicitly retained an external-series-year-conflict hold. Post-run review preferred Marvel's [explicitly dated FF (2011) collecting statement](https://www.marvel.com/comics/collection/89990/) and [FF (2011) #6 metadata](https://www.marvel.com/comics/discover/679/black-bolt), consistent with the original Google identity and one exact-ISBN record. These publisher references are indexed excerpts returned by web search, not cached full-page publisher downloads. The different publisher collection establishes only the namespace; it does not expand this edition beyond #6–11. The original abstention, new source record, retained hold and explicit resolution are all preserved.

Wolverine's original source explicitly collects Wolverine (2003) #50–55 and Wolverine (2010) #310–#313. The parser recognizes the first range and holds the second because of the redundant hash marker. Manual review verified the exact literal clause, dated original-series identities and whole-issue endpoints. That resolution applies only to synopsis eligibility. The raw parser output, source, website issue fields and mappings were not rewritten; there is no inferred gap filling or global parser relaxation. The explicit review is in manual-contents-review.json.

## Held editions

| ISBN | Edition | Reason |
| --- | --- | --- |
| 9781302530389 | What If…? Venom | Title punctuation truncates the collecting parser; namespace/membership need review, and the draft repeats promotional framing |
| 9781302489366 | Squirrel Girl & the Great Lakes Avengers | Unresolved extras, missing years and partial material; question-only draft also remains flagged |
| 9781302489953 | Jessica Jones: Avenger | Usable limited plot overview, but unnumbered extras and partial contributions remain unresolved |
| 9781302522568 | Dawn of X Vol. 8 | Unparsed Giant-Size syntax plus a source plot/contents alignment concern |

Dawn of X's description names New Mutants, Crucible and Excalibur threads that are absent from its explicit collecting list. That is recorded as a research concern, not proof that the book is contaminated or permission to add those issues. The selected New Mutants thread was not published. Unspecified partial material in the other collections was not promoted to whole-issue scope.

## Publication verification

All 18 catalog tests passed. The preceding 355-test Python validation remains applicable because production code was unchanged; the full suite was not rerun for this data-only batch. Verified frozen code, packet and source hashes, actual prompt hashes, literal citations and manual-resolution evidence hashes. Current candidate ISBNs do not overlap prior run manifests, excluding this batch's explicit FF follow-up.

Only six intended records changed, limited to synopsis, review provenance and source fields. Other records and fields were preserved. Exact backups and final production hashes passed verification, and localhost:5173/enrichment.json serves the exact staged payload. No remote deployment occurred. The actual promotion uses approved-staging-final; the earlier unpromoted package and superseded citation-completeness decisions remain available for audit.

Artifacts are in data/local-ai-trials/enrichment-ten-b-20261101: frozen inputs/code, original results, source research/audits, manual-contents-review.json, ff-publisher-reference.json, resolved-review-queue.json, immutable decisions, approved-staging-final, publish-receipt and verification.json. The separate FF source-recovery run is enrichment-ff-followup-20261101. new-held.json contains four newly held editions; known-held.json combines them with the preceding backlog for 156 reviewed holds. This count excludes books not yet reviewed.
