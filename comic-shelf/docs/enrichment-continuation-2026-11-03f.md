# Source recovery and saved-case edition review — November 3, 2026, sixth block

Published **two source-reviewed editorial synopses**, increasing the local approved total from **340 to 342**. One came from a new source-recovery request; the other came from formal edition review of an existing prospective case. Five saved cases received formal decisions without repeated inference: three previously generated baseline drafts and two prior empty-input abstentions. Four remain held. Production code, selector and settings are unchanged.

## Ultimate X-Men: World Tour

The guarded exact-ISBN lookup for Ultimate X-Men Vol. 3: World Tour (9780785171270) succeeded. The source adds a collecting statement for #13–20. Its literal collecting line uses 2000, while its series label and the older bibliographic label use 2001. [The publisher’s original #13](https://www.marvel.com/comics/issue/15703/ultimate_x-men_2001_13) identifies the 2001 run and connects the issue to World Tour. The disagreement is recorded explicitly for synopsis-only review; no year, alias, issue key or ordering metadata changed.

That original included issue also describes a Gambit setup absent from both book blurbs: a girl seeks his help. Rather than claim the world-tour paragraph covers all the book’s threads, the reviewed revision now covers that setup alongside the X-Men’s peace/trust mission, hostility toward mutants and exposure of Xavier’s secret. It does not identify the girl, reveal the secret or claim a successful rescue or tour outcome.

Two short, noncontiguous literal publisher excerpts are preserved in a separate source record and explicitly marked **added after inference**. They are not represented as Qwen input or output. Target exact-ISBN collecting evidence establishes that original #13 belongs to the book; plot was not transferred from a different collection. The correction cites the older book description, new library description and those included-issue excerpts. The second staging package completes the citation to the library’s trust objective; the earlier staging and immutable decision history remain preserved.

One new Qwen request completed in **6.98 seconds**, selecting **three literal quotations**, with zero production worker failures. The published wording is an explicit editorial revision, not an unchanged model draft. Both original packets/results and the new source/parent hashes remain intact.

The Venom vs. Carnage lookup (9780785171317) failed. Its downloaded search page, acquisition audit and hash are preserved and attached to the backlog. The identical lookup should not be repeated without changed evidence or a new source strategy. All downloaded page hashes for both attempts verified.

## Formal review of the five saved prospective cases

Used the original **60-word baseline** results and full frozen ISBN descriptions. The 90-word treatment outputs were not silently substituted. Raw proposals remain unchanged; current inventory checks and explicit manual findings were added to a new review queue. Two cases have prior no-call abstentions and are not counted as model-generated drafts.

| Case | Decision | Reason |
| --- | --- | --- |
| Sgt. Fury: Berlin Breakout | Hold | Collecting parser truncates SGT. at the abbreviation; original namespace and annual scope still need review |
| Ultimates: Homeland Security | Hold | No collecting evidence; source grammar/setup and excluded long passage require editorial review |
| Art of Marvel Studios: Thor | Hold | Art-book format and movie casting/director promotion do not establish a suitable book synopsis |
| Mighty Avengers by Dan Slott | Hold | Original-series identity plus unspecified material from Secret Invasion: Requiem remain unresolved |
| Phases of the Moon Knight | Revised and published | Publisher evidence distinguishes original-series identity from collection-year labeling; full target description supports anthology scope |

For Phases of the Moon Knight (9781302532000), the target source labels its collection 2025 and lists #1–4. [The original publisher series](https://www.marvel.com/comics/series/39624/phases_of_the_moon_knight_2024_-_present) enumerates #1–4 under 2024, and [an original #1 variant](https://www.marvel.com/comics/issue/120975/phases_of_the_moon_knight_2024_1_variant) is dated August 2024. [The publisher’s collection catalog](https://prhcomics.com/wp-content/uploads/2024/12/PREVIEWS2021040_March_2025_FINAL.pdf) places the same-title collection in 2025, with MacKay/Garcia among multiple contributors. Another format’s ISBN and supplemental contents are not assigned to the target.

The revision covers past, present and future Fists of Khonshu: a Moon Knight’s violent vision of justice, the Old Crusades incarnation, a crime-ridden version of the Marvel Universe, and additional Marc Spector/Khonshu tales. It removes creator advertising and superlatives. It does **not** equate the source’s unnamed familiar Moon Knight with Marc Spector or supply another incarnation’s identity from memory. Every scope claim comes from the full frozen target description, including text not available to the default selector because of its length filter. Publisher references establish identity; they do not supply extra plot to the correction.

Sgt. Fury’s annual issue list is not assumed to mean complete annual contents. [A review of a different format](https://aiptcomics.com/2023/05/31/sgt-fury-epic-collection-berlin-breakout-review/) reports missing companion stories. That is a research question for the target edition, not evidence to add or remove target material automatically. Even a future abbreviation fix must preserve the namespace and scope holds. Mighty Avengers’ unspecified partial special likewise cannot become a whole issue through parsing alone.

## Verification and counts

Both guarded publications passed exact receipt/backup checks and actual HTTP-served payload verification. The final audit connects both transactions to the 340-synopsis baseline. Only two intended book records changed, limited to summary, citations and review provenance. Prior approvals, unrelated fields, top-level metadata and the initialized Atlantis Rising record remain intact. Canonical approved data, public data, built data and the served response agree at **342**.

The known production-review backlog is **427 editions**: 424 before, minus one recovered prior hold, plus four newly formalized holds from the saved research cohort. Phases was a saved research candidate outside that earlier backlog, so it is not counted as a second recovered prior hold. The saved-case review involved **five cases, three prior drafts and two prior no-call outcomes**, with zero new inference requests. This block’s only new model response is the World Tour recovery; the earlier prospective requests and earlier harness error were not repeated or counted again.

All 78 current Python script hashes match the frozen manifests. Parser version 25, the 60-word candidate allowance, original three-passage selector, opening-reference warning and guarded initialization behavior are unchanged. No test-suite rerun is claimed for this artifact/data-only block; prior validation remains 385 Python tests and 18 catalog tests. The collector stays paused and no remote deployment occurred.

## Next work

Seek exact-ISBN collecting evidence for the newly formalized Ultimates case and Wolverine: Old Man Logan, checking acquisition history first. Investigate the bounded SGT. abbreviation parsing defect with regression fixtures and frozen-input replay before changing the parser; a parser repair alone must not clear unknown series identity or annual/partial-material scope. Continue source/edition review rather than repeat the same word-limit experiment.

Artifacts are in data/local-ai-trials/continued-20261103f, source-recovery-one-20261103f and namespace-review-prospective-five-20261103f. Current source audits, publisher excerpt provenance, saved-case decisions, both publication receipts, final-verification.json, known-held.json and next-session-priorities.json preserve the distinction between model outputs, no-call outcomes and later editorial evidence.
