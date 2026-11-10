# Enrichment and parser continuation — November 5, 2026

Published **28 source-reviewed synopses**, increasing the local approved total from **342 to 370**, after reviewing **50 previously unused editions** in two frozen 25-edition batches. Twenty-six publications are explicit editorial revisions, and two retain Qwen's selected text. Twenty-two new editions remain held; the known backlog is **449**. No remote deployment occurred.

## Parser improvement

Parser version 26 protects the Sgt. abbreviation, including uppercase SGT., while finding a collecting-sentence boundary. The original literal quote is preserved. The saved Sgt. Fury: Berlin Breakout packet now retains SGT. FURY #20–36 and ANNUAL #1–2 as separate unresolved entries. It does not infer an original year from the Epic Collection's 2019 label, identify the annual run, or claim complete annual contents. The edition remains held.

Two regression tests cover abbreviation casing, unchanged quotes, yearless/annual holds, true sentence boundaries, decimals, variants and reversed ranges. **387 Python tests and 18 catalog tests passed**. A frozen replay of **921 unique source packets** changed only the intended Sgt. Fury case. Only edition_trial.py and test_edition_trial.py changed among the 78 production Python scripts; both inference batches were frozen afterward.

## Qwen and editorial review

The 50 cases produced **49 model responses, one empty-input no-call abstention, 112 literal selected quotes and zero worker failures**. Worker time was **316.99 seconds**. The 60-word/450-character candidate bounds, original prompt, three-passage limit, temperature zero, thinking off and 200-token output limit remain unchanged.

Full-source review restored major omitted strands: Vision's family setup, Strikeforce's hospital and Angela stories, the Phoenix future era, Ghost Rider's separate What If story, Siege's Unit material, the Fantastic Four's changed reality, She-Hulk's Fight Club and the Mandalorian's journey episodes. Explicit revisions repaired unambiguous grammar damage without overwriting raw source text or inventing missing names or outcomes. The America revision uses the source's campus-queen role without guessing a correction for X Andria. The Doctor Strange revision leaves an unnamed assistant unnamed.

Namespace review used exact-ISBN collecting/bibliographic evidence alongside publisher metadata. Some publisher pages returned 403; where only publisher search-index headings were available, source-assessment.json explicitly records that limited access. They were used only for namespace corroboration, never as full issue text or extra plot. Examples include [Vision](https://www.marvel.com/comics/issue/57306/read), [Avengers Arena](https://www.marvel.com/comics/series/16875/avengers_arena_%282012_-_2013%29), [Moon Knight](https://www.marvel.com/comics/issue/4042/moon-knight-2006-1) and [Death of X](https://www.marvel.com/comics/series/22313/death_of_x_2016). The [publisher's Secret Invasion list](https://share.marvel.com/comics/discover/133/secret-invasion-the-complete-event) was fully readable and corroborated the Initiative namespace. Every published plot claim comes from the full frozen target description. No original-year aliases, issue keys, ordering, page counts or other-format contents were published.

Held cases include unresolved annuals and unnumbered specials, unspecified partial stories, missing inventories, empty descriptions and collecting-range conflicts. Additional full-source review caught an unspecified Giant-Size X-Men issue outside Grand Design's formal collecting sentence; its supplemental scope remains held. Saved parser diagnostics also expose a false compound title around Minimum Carnage/Scarlet Spider and a comma-split Doctor Strange, Sorcerer Supreme title. No broad parser fix was improvised during frozen inference.

## Source recovery

Both guarded ISBN lookups failed reconciliation and remain held. Ultimates: Homeland Security (9780785171300) has two ISBN-matched records with different quotation punctuation; both collect #7–13, disagreeing with the catalog's #7–14. Wolverine: Old Man Logan (9780785171355) has descriptions differing in ellipsis typography; both add an unnumbered Giant-Size special. All downloaded HTML hashes and format-level ISBN matches verified. No record was cherry-picked, silently normalized or passed to Qwen. Failures and findings are attached to the held map to prevent identical retries.

## Publication verification

Each package passed staging checks, immutable review-decision/citation checks, transactional promotion, receipt/backup checks and actual HTTP-served payload verification. The final audit chains both transactions to the 342-synopsis baseline. Only the 28 intended records changed, limited to summary, citations and review provenance; earlier approvals and unrelated metadata remain intact. Public, built and HTTP-served enrichment match canonical approvals at **370**.

Localhost was initially down and was restarted at http://127.0.0.1:5173/. Both the home page and enrichment response were verified. The legacy collector remains paused. A one-off review preparation script initially read the compact worker queue instead of the exported full review queue; its invalid pre-staging artifact and v1 script were preserved, corrected before any decisions/publication, and no model request was repeated. This was a review-harness error, not a production worker failure.

Artifacts: data/local-ai-trials/continued-20261105, sustained-25a-20261105 and sustained-25b-20261105. The final verification, known-held map, source acquisition audits, frozen-code snapshots, raw results, review decisions and publication receipts remain available. Current handoff: continued-20261105/next-session-priorities.json.
