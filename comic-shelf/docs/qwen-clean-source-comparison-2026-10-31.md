# Clean-source comparison — October 31, 2026

Tested whether intact exact-ISBN distributor descriptions improve Qwen's selections on difficult cases from the preceding fixed ten-edition cohort. Cleaner text removed punctuation/spelling damage, but both retried editions selected the same passage positions and still needed editorial work. No new synopsis was published; the approved total remains 123.

| Edition | Source result | Model/review result |
| --- | --- | --- |
| Shuri: The Search for Black Panther | Reused the intact, individually verified exact-ISBN distributor record already cached in the preceding pass | Same three selected positions; names/contractions now intact, but the explicit search-for-her-brother setup is still omitted. Existing approved revision preserved. |
| Miles Morales: Beyond | New accepted exact-ISBN distributor record fixes the broken metamorphic token | Same two selected positions; the distinct Amulet/monster thread is still omitted. Partial annual material remains held. |
| Hunt for Wolverine | New accepted exact-ISBN distributor description | Candidate IDs and text are identical to the old input, so another model call was skipped. The new collecting list also includes additional material requiring reconciliation. |
| Annihilation: Complete Collection Vol. 2 | Exact-ISBN replacement lookup failed | Original unresolved inventory hold preserved; no model call. |
| Kanan: The Last Padawan | Exact-ISBN replacement lookup failed | Original inventory and character-name research holds preserved; no model call. |

Four new source lookups produced two accepted records and two failed acquisitions. Shuri reused a previously cached record, with the original aggregate-label failure still preserved. Two model requests completed without worker failures in 15.58 worker seconds. All five selected evidence quotes are literal source text. The model, original prompt, selection mode and production code were unchanged. Only the primary source record changed; no publisher prose was manually edited or merged before inference.

This is a tiny targeted development comparison. The original run preceded the retry, there is no independent adjudication or randomized order, and the same selected IDs describe these two observations rather than a guarantee of deterministic behavior. Neither new draft passed unchanged under the existing coverage assessments. Correct source text is useful, but these results do not show improved selection coverage or support scaling unattended publication.

## Source and publication holds

Hunt for Wolverine's new exact-ISBN collecting statement adds Hunt for Wolverine: Dead Ends #1 and material from Marvel Legacy #1, absent from the original list. It also includes the Where's Wolverine pages. The difference is now an explicit source-contents reconciliation hold, alongside the original unresolved inventory. An incomplete old list and a longer new list do not establish which material can safely be mapped to full issues. No material was silently added to the site or treated as a whole issue.

Miles Morales still collects unspecified material from an annual. Cleaner narrative text does not establish that portion's identity or make the full annual part of the edition. Kanan's failed replacement lookup does not resolve the Caleb Dune/Dume discrepancy or its two-title inventory. Annihilation's failed lookup does not resolve the undated/unnumbered entries.

All four unpublished cases received new immutable needs-research decisions with the current findings. Their staging package contains zero changes and excludes all four. Shuri was a comparison control with an explicit existing-approved-synopsis hold and received no replacement publication decision. No previously approved editorial work was overwritten.

## Verification and artifacts

Verified all frozen code, packet, parent-packet, selected source-record, downloaded-page, prompt and quotation hashes. The existing 348-test Python validation remains applicable because production code did not change; no broad test suite was rerun for this data-only comparison. Exact before/after hashes confirm that canonical, public and built enrichment files are unchanged. Known held editions remain 146.

Artifacts are in data/local-ai-trials/clean-source-comparison-20261031: source acquisition audits/pages, candidate-comparison.json, frozen manifest/packets/code, raw results, comparison-review.json, held-review-queue.json, immutable decisions, held-staging, verification.json and known-held.json. The preceding original inputs/results remain in selection-check-fresh-ten-20261031.

## Next experiment

Test a small comparison using coherent adjacent sentence blocks so setup and dependent follow-ups can be selected together. Freeze the current cohort and evaluate both coverage and extra promotion/repetition before adopting that change. The existing checks and manual source/edition review must remain in place; larger excerpt blocks would not themselves establish factual accuracy or completeness.

Completed in [the adjacent-passage block comparison](qwen-block-comparison-2026-10-31.md): three block passes versus four sentence passes, with two regressions. The default remains sentence selection.
