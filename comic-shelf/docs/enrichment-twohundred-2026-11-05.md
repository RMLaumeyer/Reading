# Enrichment — additional 200 editions, November 5, 2026

Processed **200 new, unique ISBN cases** with local **qwen3.5-4b**, followed by source/edition review and eight guarded local publication transactions. **77 synopses published; 123 held for research.** Approved coverage rose from **430/4,000 (10.75%)** to **507/4,000 (12.675%, rounded 12.68%)**. The known reviewed hold backlog is now **637**, up from 514. These figures count approved narrative synopses, not completion of every enrichment field.

| Batch | Reviewed | Published | Held |
| --- | ---: | ---: | ---: |
| 25a | 25 | 8 | 17 |
| 25b | 25 | 11 | 14 |
| 25c | 25 | 9 | 16 |
| 25d | 25 | 12 | 13 |
| 25e | 25 | 7 | 18 |
| 25f | 25 | 11 | 14 |
| 25g | 25 | 10 | 15 |
| 25h | 25 | 9 | 16 |
| Total | 200 | 77 | 123 |

## Model work and editorial limits

The local model produced **188 responses**; **12 cases made no inference call**. All 200 cases completed with **zero worker failures**, retaining **435 literal selected evidence quotations**. Summed worker execution time was **1,324.74 seconds** (not the full session's elapsed time). Five original selections were accepted unchanged; 72 published selections required source-backed editorial revision. The model continues to draft or abstain; it does not approve or publish autonomously.

Production settings stayed unchanged: thinking off, temperature zero, original prompt, sentence selection, at most three passages, a 60-word/450-character model synopsis limit and 200 output tokens. Editorial publication decisions remain separate from frozen model responses. No new source text was inserted into model packets after inference. Publisher metadata was consulted to resolve original-series namespaces and investigate source conflicts; it did not supply unrecorded extra plot to published summaries.

## Findings retained for follow-up

- ISBN **9780785179832** maps to two catalog records. The older preparation audit stopped at this ambiguity before inference. A session-only artifact auditor retained both candidates, and the case received an explicit identity hold. No target was selected arbitrarily. This was a preparation guard, separate from the zero inference failures.
- **X-Cellent Vol. 2** carries an X-23: Deadly Regenesis collecting line, and **Fantastic Four by Hickman Vol. 5** disagrees between catalog #600–604 and source #600–605. Both remain held.
- **Silk: Threats and Menaces** pairs a 2021 collecting label with a narrative/creator set inconsistent with the original 2021 issue metadata. The publisher collection repeats the suspect text, so repetition does not clear the conflict. Compare the [publisher collection](https://www.marvel.com/comics/issue/82673/silk_vol_1_threats_and_menaces_trade_paperback) with [original 2021 #1](https://www.marvel.com/comics/issue/82672/silk_2021_1). No replacement plot was published.
- **She-Hulk: Secret Invasion** has an explicit 2004 collecting-year label versus 2005 bibliographic label. The [publisher index](https://www.marvel.com/comics/creators/10197/barbara_ciardo) lists #31–33 under 2005. This remains an edition namespace hold.
- Generic introductions, bare character names, film art-book pitches and unresolved supplemental stories were held. Partial-material scope, annuals, unparsed titles and malformed inventory entries were preserved for research rather than guessed.

New held-case flag counts overlap because an edition can have several flags:

- `contents_unparsed`: 67
- `no_inventory`: 47
- `contents_unresolvedEntries`: 47
- `bibliographic_series_identity_requires_review`: 23
- `partial_material_requires_review`: 15
- `no_synopsis`: 12
- `contents_conflict`: 6
- `short_synopsis_requires_context_review`: 5
- `no_concrete_plot_evidence`: 3
- `question_only_synopsis_requires_context_review`: 2
- `opening_reference_requires_context_review`: 2
- `volume_specific_plot_evidence_requires_review`: 2
- `supplemental_story_scope_requires_review`: 2
- `catalog_identity_not_unique`: 1
- `catalog_description_issue_range_disagreement`: 1
- `source_bibliographic_year_conflict`: 1
- `damaged_source_text_requires_review`: 1
- `edition_type_requires_review`: 1
- `source_collecting_title_conflict`: 1
- `source_plot_edition_conflict`: 1

## Verification and artifacts

All 78 production Python hashes matched their frozen copies across all eight runs. Packet hashes, prompt hashes, literal quotations, review-resolution evidence, decisions, staging changes, receipt chains and exact backups verified. Existing 430 approvals and unrelated enrichment fields were preserved. No records were initialized, catalog IDs were unchanged, and parser v26/settings were unchanged. No production code changed during this block; the earlier test-suite results were not rerun or counted as new validation.

Local HTTP checks passed for the root, health endpoint, catalog, enrichment payload and six compiled assets. The served enrichment bytes match both public and built copies. Final payload SHA-256: `7d23ea7507e88fc79da9309cf73752c9b4dabf65f17bcf43b21366016f116a9e`. The localhost server remains running, and the legacy automatic collector remains paused. No remote deployment was performed.

Artifact root: `data/local-ai-trials/twohundred-20261105`. Each `twohundred-25[a-h]-20261105` run retains frozen inputs/code, raw outputs, source assessments, append-only decisions, staging, backups, receipt and verification. Consolidated results are `final-verification.json`, `published-editions.json`, `known-held.json`, `localhost-final-check.json` and `next-session-priorities.json`.

The next improvement should target source/edition reliability before unattended publication: resolve duplicate identity and contradictory descriptions, then test narrow parser changes against frozen held cases. Five unchanged publications out of 200 reviewed cases do not establish an autonomous publishing success rate.
