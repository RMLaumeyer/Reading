# Held-edition recovery — October 31, 2026

Audited 166 previously held ISBN editions, fixed recurring deterministic parsing problems, and re-ran 25 held editions with Qwen3.5-4B using the original sentence-selection prompt. Eleven editions cleared source review and were published locally: six unchanged Qwen selections and five explicit source-backed Codex revisions. Fourteen retry editions remain held. There are now 104 approved synopsis overlays; 155 of the original 166 held editions remain unpublished.

This is a targeted development recovery cohort, not 25 fresh books or independent gold adjudication. Codex designed the changes and assessed the sources under the user's delegated authorization. Parser recovery and new source evidence improved eligibility; no improvement in Qwen's autonomous factual accuracy is inferred.

## Parser changes and safeguards

Abbreviated names such as Ms. Marvel and Agents of S.H.I.E.L.D. no longer end collecting statements early. Reversible punctuation masking preserves exact evidence. Supported no-space prose openers and quoted plot introductions no longer swallow the issue list. Formal collecting labels take precedence over casual collecting prose; multiple formal lists remain blocked for edition review.

Comma-separated numeric ranges inherit only the immediately preceding explicit series in the same collecting clause. Evidence retains both the numeric fragment and its series context. Missing years stay unresolved, gaps stay gaps, partial-material scope stays partial, and unknown text resets the context. Annuals do not acquire another series' year. Decimal/suffixed issues, reversed ranges, unknown qualifiers and malformed equals-prefixed titles remain unparsed.

Bare Giant-Size is now rejected as an incomplete series name. Multiple collecting statements withdraw the contaminated Wolverine source's dependent inventory. A final safeguard also prevents thousands punctuation in Avengers 1,000,000 BC from producing phantom issues. That guard was added after inference: all 77 frozen Python files were hash-verified and archived first. Published memberships were rechecked under final parser version 20 and are identical to their run-time memberships. The historical raw results were not rewritten.

The recovery packets explicitly retain prior manual source/edition holds. Parser-produced flags are recomputed; old proposal-only flags are assessed on the new proposal. Unsupported source/catalog disagreements and contamination do not disappear merely because a new draft is longer. Regression tests cover this separation and the numeric/partial/identity boundaries.

## Corpus-level replay

| Parser blocker (overlapping counts) | Before | Final |
| --- | ---: | ---: |
| contents_unparsed | 101 | 87 |
| no_inventory | 72 | 64 |
| contents_unresolvedEntries | 52 | 51 |
| bibliographic_series_identity_requires_review | 34 | 36 |
| partial_material_requires_review | 12 | 14 |
| contents_conflict | 11 | 11 |

These counts replay the same original 166 packets with the final parser, before considering new distributor supplements. More visible provisional identities or partial material are additional safeguards, not reasons to approve. The retry cohort contains 23 formatting-improvement cases plus contaminated Wolverine and ambiguous Giant-Size safety cases. The first cohort-size preflight was corrected before inference; its failed preflight log is retained. Earlier exploratory replay metrics are preserved; the final table and verification.json supersede them.

## Source research

Seven exact-ISBN distributor lookups returned five accepted records and two failed validations. Generation Why gained a missing plot synopsis. Ultimate Spider-Man (2000), Alias (2001) and Sensational She-Hulk (1989) received independent matching year/issue evidence. Their publication decisions resolve only the provisional identity reason; no global alias or completeness claim was added. Alias's inherited truncated-name hold was resolved only through an explicit revision that uses complete source passages and omits the broken peripheral name.

Doomquest exposed a conflict: Google says Iron Man (1968), while the exact-ISBN distributor says Iron Man (1981). Both sources remain attached, the conflict is explicit, and the edition was not published. The two Ms. Marvel aggregate distributor validations initially failed, as did the publisher-catalog attempts. Subsequent review of the cached individual distributor records recovered both identities, as described below. Failed lookup results themselves were not treated as evidence. Partial-material, annual, malformed-title and source-integrity holds remain in force.


The cached Beyond the Limit records agree on exact ISBN, 2021 series identity and #1-5 membership; their capitalization and ellipsis formatting differ. The unchanged original Qwen synopsis was approved using the original plot evidence. Super Famous's two exact-ISBN records both explicitly collect Ms. Marvel (2015) #1-6, matching the original source, while their broader category label says 2014. That conflicting label remains preserved. The specific dated collecting statements establish the issue namespace for this edition only; no global year alias was added. Its synopsis was revised to restore the development-company conflict and remove hype. This review-only follow-up made no additional model requests and published two more of the same 25 retry cases.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302493462 | Captain America: Serpents Unite! | Unchanged Qwen selection |
| 9781302479268 | Ms. Marvel Vol. 2: Generation Why: Issues #6-11 | Unchanged Qwen selection |
| 9781302501631 | Ms. Marvel Vol. 8: Mecca: Issues #19-24 | Source-backed Codex revision |
| 9781302532192 | Fantastic Four vs. Galactus: Issues #48-50, 242-244 | Source-backed Codex revision |
| 9781302936174 | Ms. Marvel: Army Of One: Issues #1-12 | Unchanged Qwen selection |
| 9781302944049 | Iron Fist: The Shattered Sword: Issues #1-5 | Unchanged Qwen selection |
| 9781302383398 | Ultimate Spider-Man Vol. 20: And His Amazing Friends: Issues #118-123 | Unchanged Qwen selection |
| 9781302482695 | Jessica Jones: Alias Vol. 3: Issues #10, 16-21 | Source-backed Codex revision |
| 9781302494643 | Sensational She-Hulk by John Byrne: The Return | Source-backed Codex revision |
| 9781302488567 | Ms. Marvel Vol. 5: Super Famous | Source-backed Codex revision |
| 9781302942137 | Ms. Marvel: Beyond the Limit | Unchanged Qwen selection |

The first four revisions restore Mecca's main conflict, cover both Galactus encounters, distinguish the three women in Alias, and remove duplicated/promotional She-Hulk passages. All citation text is checked against full descriptions. Unchanged selections are not conflated with corrected drafts. One rationale-only correction was appended as a superseding immutable decision; the earlier unpromoted staging package is preserved.

## Verification and recovery

All 25 retry cases completed without worker failures using 25 model requests in 175.99 worker seconds, excluding research/review. All 57 selected evidence quotations are literal source text. Packet, parent-packet, actual prompt and archived run-code hashes passed.

All 335 Python test executions and 18 catalog tests passed, as did whitespace validation. Publication checks verify that only the eleven intended records across two promotions and synopsis/provenance/source fields changed, that current target summaries matched the pre-review snapshot, and that exact backups and final production hashes match. localhost:5173/enrichment.json serves exactly the staged payload. No issue keys, appearances, reading-order completeness, borrowing availability or unrelated checkout work changed. No UI build or remote deployment was needed.

Artifacts: data/local-ai-trials/held-recovery-20261031 contains the original held baseline, exploratory and final parser replays, research pages/audits, inherited-hold packets, original run results, frozen-code, source review, resolved-review-queue.json, review-spec.json, immutable decisions, approved-staging-final, publish-receipt and verification.json. The canonical approved overlay is data/approved-synopses.json. The follow-up is in data/local-ai-trials/held-recovery-identity-followup-20261031, including the two-row review queue, decisions, approved-staging, publish-receipt, final verification.json and remaining-held.json. The first verification records the intermediate nine-publication/102-overlay state; the follow-up verification records the final eleven-publication/104-overlay state and verifies both receipt hashes as one chain. The latest receipt contains exact backups and refuses rollback over newer edits.

## Retry decisions

| ISBN | Edition | Decision | Rationale |
| --- | --- | --- | --- |
| 9781302493462 | Captain America: Serpents Unite! | accept | Source-reviewed unchanged Qwen selection after parser recovery. Captain America/Serpent Society conflict and the M.O.D.O.K. dilemma are source-supported and preserve the open choice. This event corrects only the wording of the earlier review rationale. |
| 9781302479268 | Ms. Marvel Vol. 2: Generation Why: Issues #6-11 | accept | Source-reviewed unchanged Qwen selection after parser/source recovery. Fresh exact-ISBN plot supports the Inventor threat and Kamala's effort to stop him; no invented identity or victory. |
| 9781302501631 | Ms. Marvel Vol. 8: Mecca: Issues #19-24 | revise | Restore the main enemy/targeting premise omitted by selection and keep the distinct Bruno/Wakanda thread. No identity or final outcome is inferred. |
| 9781302532192 | Fantastic Four vs. Galactus: Issues #48-50, 242-244 | revise | Cover both the original Silver Surfer encounter and later Terrax storyline, remove creator praise and preserve the gap between #48-50 and #242-244. No victory or sacrifice is invented. |
| 9781302936174 | Ms. Marvel: Army Of One: Issues #1-12 | accept | Source-reviewed unchanged Qwen selection after parser/source recovery. Represents development-company, automaton and Civil War II/school threads without creator credits or an invented outcome. |
| 9781302944049 | Iron Fist: The Shattered Sword: Issues #1-5 | accept | Source-reviewed unchanged Qwen selection after parser/source recovery. The new unnamed Iron Fist, K'un-Lun training and dark-god threat are explicit. Preserve the hero's identity as a mystery rather than adding it from memory. |
| 9781302383398 | Ultimate Spider-Man Vol. 20: And His Amazing Friends: Issues #118-123 | accept | Source-reviewed unchanged Qwen selection after parser/source recovery. Peter/Johnny Storm/Liz Allen and the school threat are self-contained. Exact-ISBN evidence corroborates the original Ultimate series identity. |
| 9781302941710 | Jane Foster: The Saga of the Mighty Thor | needs_research | Recovery remains blocked: partial_material_requires_review |
| 9781302482695 | Jessica Jones: Alias Vol. 3: Issues #10, 16-21 | revise | Use complete source passages and distinguish Jessica Jones, Mattie Franklin and Jessica Drew. Omit the truncated Daily Bugle name and do not claim Mattie is rescued. |
| 9781302488567 | Ms. Marvel Vol. 5: Super Famous: Issues #1-6 | revise | Restore the development-company/image conflict omitted from the selection and remove reader hype. Edition identity rests on the exact-ISBN dated collecting statements, not the conflicting category label. |
| 9781302494643 | Sensational She-Hulk by John Byrne: The Return | revise | Remove duplicated near-identical source selections and writer promotion. Keep the metafiction, named foes/body-swap premise and marriage question without inventing a completed wedding or artist-as-villain event. |
| 9781302507510 | Iron Man: Doomquest | needs_research | Recovery remains blocked: external_series_year_conflict, contents_unparsed, contents_unresolvedEntries, no_inventory |
| 9781302514297 | Ms. Marvel: Metamorphosis: Issues #12-19 | needs_research | Recovery remains blocked: partial_material_requires_review |
| 9781302532697 | Marvel Masterworks: The Man-Thing Vol. 2: Issues #2-14 | needs_research | Recovery remains blocked: partial_material_requires_review |
| 9781302942137 | Ms. Marvel: Beyond The Limit by Samira Ahmed: Issues #1-5 | accept | Original Qwen selection clearly establishes Kamala, the laboratory explosion, doppelganger and failing powers. Independent exact-ISBN series/issue metadata corroborates identity; the strict aggregate failure remains preserved. |
| 9781302485511 | Black Panther By Christopher Priest: The Complete Collection Vol. 3: Issues #36-49, 57-58 | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries |
| 9781302516239 | Man-Wolf: The Complete Collection | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries |
| 9781302527518 | Deadpool vs. Wolverine | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries |
| 9781302479916 | Deadpool Classic Companion | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries, no_synopsis |
| 9781302499037 | The A-Z of Marvel Monsters | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries, partial_material_requires_review |
| 9781302500078 | Thor vs. Hulk | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries, partial_material_requires_review |
| 9781302497804 | Silver Surfer Epic Collection: The Infinity Gauntlet | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries, partial_material_requires_review |
| 9781302528232 | Avengers by Jason Aaron Vol. 5: Issues #46-62 | needs_research | Recovery remains blocked: contents_unparsed, contents_unresolvedEntries, bibliographic_series_identity_requires_review |
| 9781302527754 | Wolverine Epic Collection: The Return of Weapon X | needs_research | Recovery remains blocked: editorial_source_integrity_requires_research, contents_unparsed, no_inventory |
| 9781302503710 | Avengers Epic Collection: The Avengers/Defenders War | needs_research | Recovery remains blocked: ambiguous_collected_series_identity, contents_unparsed |
