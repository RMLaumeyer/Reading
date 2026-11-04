# Source research, Qwen retest and reviewed publication

October 30, 2026. The user authorized a deeper assessment and publication of results judged useful. Work used the existing local Panel site, not public hosting. Decisions are labeled `delegated` with the exact user instruction and Codex as assessor; they are not presented as independent human adjudication.

## Published to the local site

Three synopsis changes passed review and were promoted with guarded backups:

- Captain America and the Falcon: Two Americas, ISBN 9781302482275 — retained Qwen's source-grounded Falcon pursuit/deadline synopsis.
- Strange Academy: Finals, ISBN 9781302525040 — published the source-backed editorial correction naming the students, mission and stakes. This is an assistant correction of Qwen's selection, not raw model output.
- Avengers Inc., ISBN 9781302527969 — retained the original Qwen premise after corroborating its provisional series year against a newly fetched exact-ISBN OverDrive record. No edition/issue completeness claim was added.

Ultimate X-Men Vol. 4 was retained unchanged: its existing editorial synopsis is already useful. The original Blade/Doom/Doctor Strange pilot is also unchanged. Six synopsis records now have canonical approved overlays in total.

## Seven held editions investigated

The existing bounded collector attempted public OverDrive ISBN lookups. Six returned validated exact-ISBN metadata; Galactus produced no validated source. Raw search/media pages, acquisition audits, identifiers and hashes are preserved under `data/local-ai-trials/deep-review-20261030/`.

| Edition | Research result | Disposition |
| --- | --- | --- |
| Avengers Inc. | OverDrive ISBN 9781302527969 identifies Avengers Inc. (2023), corroborating the earlier Google Books series label. Description agrees on the principal premise. | Provisional series-year review resolved for this synopsis-only staging decision, with evidence retained in a new queue. Published original premise. |
| Hulk: Visionaries — Peter David Vol. 7 | OverDrive supplies Incredible Hulk (1968) #383–389 plus Annual #17; cached Google metadata contains only the annual in its collecting statement. | Apparent incomplete metadata, not a basis to silently overwrite inventory. Held for source reconciliation and annual identity. |
| Ghost Rider: The Salvation Run | New exact-ISBN description repeats mixed-series contents and partial Marvel Tales material. | Missing/ambiguous identities and partial-scope review persist. Held. |
| Oz: The Emerald City of Oz | Two accepted distributor records agree on synopsis and The Emerald City of Oz (2013), while collecting text omits “The” and year. | Promising explicit alias/year research, but no automatic alias change or inventory acceptance performed. Held. |
| Galactus the Devourer | No validated OverDrive result; original packet lacks plot text. Search leads were insufficient to approve missing edition evidence. | Held; no invented synopsis or new record. |
| Deadpool Team-Up: Good Buddies | New exact-ISBN source lists #899–894 and series (2009). | Descending numbering requires explicit parser support without silently reversing publication order. Held. |
| A Year of Marvels | Distributor list uses A Year of Marvels: January Infinite Comic, while original metadata lists Marvel New Year's Eve Special; issue-level identity/scope remains unresolved. | Held; no automatic equivalence asserted. |

The source files contain the URLs and precise ISBN identifier paths. Distributor agreement may share upstream publisher data and is not independent ground truth.

## Qwen retest and worker repairs

Six newly sourced packets were frozen before local Qwen3.5-4B inference. All six model calls completed without exceptions; outputs remain development drafts. Added sources did not consistently improve selection: Avengers Inc. lost protagonist context, and Oz selected identical text from two sites. Neither result was promoted. Original attempts and packets remain in `source-retest/`.

A generic worker fix now deduplicates identical passages before model selection so copies of the same publisher text cannot consume multiple slots. A regression test covers it. The six-source retest predates that fix; it was not rerun or relabeled as an improved accuracy result. Semantic generalization and review time savings remain unproven.

Maintenance review also found `build_pilot.py` did not merge approved synopsis overlays. It now uses the same overlay helper as the automatic and ISBN/Open Library publishing paths. An actual full pilot rebuild was not run because it would rewrite unrelated existing research; merge behavior is covered in temporary promotion/overlay tests.

## Publication and validation

The reviewed queue preserves the original queue and adds source evidence plus the explicit Avengers identity-resolution rationale. Delegated approvals carry the user's authorization in both decision events and published synopsis provenance. Unresolved edition flags still block staging. The three-record staging package is in `approved-staging/`; exact backups, hashes and transaction state are in `publish-receipt/`.

Validation passed: 18 catalog tests; 16 staging/promotion test executions (including inherited fixtures); five review-decision tests; eight worker tests; TypeScript typecheck; whitespace checks. Earlier in this assessment the two metadata-enrichment tests also passed. Temporary-fixture tests exercise rollback and write-failure restoration without rolling back approved live changes.

Post-publication checks verify exactly three changed records, unchanged unrelated fields, preserved original pilot, matching target/backup hashes and correct canonical overlay merging. All three new synopses were verified in the running browser. The Avengers detail panel also shows the source link. Generic “needs review” labels remain because other enrichment fields are not approved. The screenshot is `published-avengers.png`; the structured audit is `verification.json`.

The local server was started for verification and remains available at http://localhost:5173/. No remote site was created or deployed. No commits or pushes were made.

## Next useful work

Work on evidence/identity reconciliation rather than another broad synopsis prompt patch: descending issue ranges, explicit title aliases, annual identity and conflicting collecting statements. Evaluate each change on fresh cases before using it to clear production blockers. Qwen remains a supervised draft selector; automated source collection and deterministic validation are doing distinct parts of the work.
