# Qwen cited-rewrite comparison — October 30, 2026

Implemented an experimental sentence-cited rewrite mode and compared it with original sentence selection on the same 25 fresh ISBN editions. Keep selection as the default. Ten selection drafts passed their applicable source/editorial checks unchanged, compared with two fully cited rewrites. Eleven rewrite drafts were conservatively held for unsupported or distorted claims, eight needed editing or citation repairs, two appropriately abstained, and two failed the deterministic 80-word limit. This is a development assessment by Codex, not independent human adjudication or a general model-accuracy estimate.

| Outcome | Selection | Cited rewrite |
| --- | ---: | ---: |
| Pass unchanged under applicable review requirements | 10 | 2 |
| Needs editing or citation repair | 13 | 8 |
| Unsupported/distorted-claim hold | 0 | 11 |
| Appropriate abstention | 2 | 2 |
| Deterministic output-validation rejection | 0 | 2 |
| Model requests | 24 | 24 |
| Worker processing seconds | 154.77 | 329.42 |

There were 48 model requests rather than 50 because Devil Dinosaur had no eligible synopsis excerpts and both modes abstained without inference. Every completed response ended normally; the two failed results were overlong rewrites, not transport errors. No automatic retry, shortening or silent correction was performed. Raw responses remain available. Times exclude editorial review, tests and publication.

## Implementation

scripts/enrichment_worker.py now accepts --synopsis-mode select|rewrite, default select. Preparation freezes the mode and actual prompt; prepared execution uses the manifest. Historical manifests without a mode still use selection. Rewriting receives edition-title context and the same eligible source excerpts, emits at most three text/evidenceIds objects, and has a 700-token response budget instead of the selection mode's 200. Model qwen3.5-4b, temperature zero, thinking-off request setting, source bytes and parser are shared. This compares output modes, not an isolated prompt-only intervention.

The worker validates response completion, strict fields, evidence IDs, duplicates, nonempty text, citation membership in the frozen source, claim count and total word count. Every sentence retains its own cited passages. Review Markdown shows each claim and evidence beside the full descriptions. Nonempty rewrites always receive rewritten_synopsis_requires_entailment_review. Merely accepting such a draft cannot stage it; a dedicated regression test verifies that block. A separate source assessment must resolve that flag, and unresolved edition/inventory flags still block publication.

Exact citations establish where words came from; they do not establish that the rewritten sentence follows from them. Tests explicitly exercise a valid citation attached to an unsupported battle outcome and confirm the review gate remains in place. No new automatic semantic-accuracy guarantee is claimed.

## What review caught

Thor & Loki changed sons of Odin into brothers of Odin. Doctor Strange: Herald made Strange the banished figure where the source identifies Galactus, and described an alliance with a feast. Doctor Strange Vol. 1 changed a companion helping when Super-Skrull arrives into Super-Skrull himself helping. X-Men Legends turned writer Peter David into a team leader. These are meaningful changes to agents and relationships despite genuine source IDs.

Other holds concern missing citation coverage, hypothetical outcomes, inferred intentions, omitted anthology material, or promotional prose. Some are conservative interpretation/uncertainty judgments rather than provable contradictions. Moon Knight had names in the full source that were absent from its cited excerpts. Black Panther omitted the discovery passage from its first sentence's citations. Wastelands omitted survival text after the sentence splitter stopped at Hulk Jr. These distinctions are recorded per edition; no citation repair is counted as a raw fully cited model pass.

The two unchanged rewrite passes were Strange Academy and Ultimate X-Men: Cable. Strange Academy retains an unresolved edition-identity flag; Cable already has a stronger editorial. Neither was published from this experiment.

## Published locally

| Edition | ISBN | Treatment |
| --- | --- | --- |
| Godzilla Destroys the Marvel Universe | 9781302535162 | Original Qwen sentence selection, unchanged |
| Thor & Loki: Double Trouble | 9781302939106 | Original Qwen sentence selection, unchanged |
| Doctor Strange by Mark Waid Vol. 1 | 9781302526580 | Original Qwen sentence selection, unchanged |
| Doctor Strange by Mark Waid Vol. 3: Herald | 9781302515737 | Original Qwen sentence selection, unchanged |
| Avengers of the Wastelands | 9781302521981 | Qwen rewrite text unchanged; Codex repaired sentence citation coverage |
| Black Panther: The Intergalactic Empire of Wakanda Part One | 9781302508111 | Qwen rewrite text unchanged; Codex repaired sentence citation coverage |

There are now 69 approved synopsis overlays. Seven existing editorials were retained and twelve unique editions remain held. The two citation repairs are explicit revise decisions, with original claims/IDs, corrected sentence evidence, queue resolution provenance and unchanged generated-text checks. Codex checked every clause of those two texts against the full original source before resolving only the entailment-review flag. No edition or inventory blocker was cleared.

The served synopsis provenance contains the corrected evidence; the complete original per-sentence mapping and repaired mapping remain in the immutable decision/queue artifacts. No Qwen prose in the two published rewrites was rewritten by Codex. Publication did not add issue membership, character appearances, reading-order completeness or borrowing-availability claims. No remote deployment occurred.

## Verification and recovery

The paired audit verified identical packet manifests, frozen Python code hashes and actual prompt hashes on every model attempt. All 165 citation references (57 selection, 108 rewrite, including repeated references and rejected overlong responses) resolve to exact source passages. That is a mechanical integrity check, not 165 independently verified factual claims.

Both publication packages preserve unrelated records and fields. Exact backups, the selection-to-rewrite publication chain and final target hashes passed. The local Panel server serves byte-for-byte the published enrichment JSON. Tests passed: 15 worker executions, six staging executions, five decision executions, 18 promotion/staging executions including inherited staging cases, and 18 catalog tests. Some staging cases are intentionally exercised by more than one suite; these totals are test executions, not unique cases. git diff --check passed. No UI code changed and no static rebuild was needed.

Artifacts live in data/local-ai-trials/rewrite-v1-control-25-20261030 and rewrite-v1-candidate-25-20261030. The control directory contains the assessment plan, source checklist, both assessments, paired-assessment.json, comparison-summary.json, selection staging/receipt and publication-verification.json. The candidate preserves every result and raw response, sentence-citation-repairs.json, resolved-review-queue.json, delegated decisions and its staging/receipt. Roll back the candidate receipt first; older receipts refuse to overwrite later publications.

## Operating decision

Keep original selection as the normal enrichment mode and use rewrite only for explicitly supervised experiments. This sample does not support autonomous rewriting with the loaded 4B model. The next productive enrichment run can continue source selection and edition research while the unsupported-claim examples form a regression set for any later, narrower rewrite design.

## Per-edition results

| ISBN | Edition | Selection | Rewrite | Rewrite assessment |
| --- | --- | --- | --- | --- |
| 9781302520557 | Young Avengers By Gillen & Mckelvie: The Complete Collection: Issues #1-15 | needs_edit | needs_edit | The cast sentence includes Loki without citing his excerpt; Young Avengers are unnamed and the third sentence repeats the first threat. |
| 9781302521981 | Avengers of the Wastelands: Issues #1-5 | pass | needs_edit | Text is source-supported, but survival in sentence one needs the omitted continuation after Hulk Jr. Repair citations without changing wording. |
| 9781302502386 | Avengers: West Coast Avengers: Zodiac Attack: Issues #25-30 | pass | needs_edit | Archery dominance interprets rather than explains the source's puzzling also-Hawkeye conflict; meta narrative wording needs clarification. |
| 9781302377717 | Uncanny X-Men Vol. 3: The Good, The Bad, The Inhuman: Issues #14-15 | needs_edit | needs_edit | Mostly copies source sentences, retaining malformed apostrophes and Magneto repetition while omitting Inhumanity and the stranded-students thread. |
| 9780785178859 | Marvel Zombies Return: Issues #1-5 | needs_edit | unsupported_claim | Asserts a disappearance in Marvel Zombies 2 where the description asks what happened at its end; the first sentence does not cite the transport excerpts that might supply context. |
| 9781302529611 | Deadly Hands of Kung Fu: Gang War: Issues #1-3 | needs_edit | needs_edit | Makes the doubts about Shang-Chi's intentions ambiguous and leaves out the collected Mister Negative and Spider-Man training tales. |
| 9781302524579 | Generation X Epic Collection: The Secret of M: Issues #24-32 | pass | unsupported_claim | Groups the truth about M as a threat to Emma's students; the cited source only says the truth comes to light, not that it is a threat. |
| 9781302508111 | Black Panther by Ta-Nehisi Coates Vol. 6: The Intergalactic Empire of Wakanda Part One: Issues #1-6 | needs_edit | needs_edit | Both sentences are supported by the full description, but the discovery clause needs the omitted kingdom-discovery excerpt. Repair evidence without changing wording. |
| 9781302503680 | X-Men: Grand Design: Issues #1-2 | appropriate_abstention | appropriate_abstention | No specific plot beyond publication-history marketing; retain existing editorial. |
| 9781302482541 | Moon Knight Epic Collection: Shadows of the Moon: Issues #5-23 | pass | needs_edit | Marc, Steven, Jake, Midnight Man and Bushman are in the full source but absent from the sentence's cited E1-E4; requires corrected citations and retains a stronger editorial. |
| 9781302523688 | Moon Knight: Black, White & Blood: Issues #1-4 | needs_edit | unsupported_claim | Turns a Spider-Man adventure and separate Strange favor into a joint mission to seek Strange; literalizes blood-moon promotional framing and omits future/reverse anthology threads. |
| 9781302535162 | Godzilla Destroys the Marvel Universe: Issues #1-5 | pass | worker_failure | Rejected deterministically for exceeding the 80-word bound. Raw response retained; no retry or silent shortening. |
| 9781302942205 | Strange Academy: First Class Collection: Issues #1-6 | needs_edit | pass | Both school/teacher setup and threatening field-trip sentence are directly entailed by E2/E4. Identity review still blocks publication. |
| 9781302939861 | X-Men Legends Vol. 1: The Missing Links: Issues #1-6 | needs_edit | unsupported_claim | Makes the Summers brothers the hunters instead of the Shi'ar and turns writer Peter David into a team leader; also embeds evidence IDs in prose. |
| 9780785192244 | Avengers: Time runs out : Vol. 4 | pass | needs_edit | Copies reader hype and a long writer-credit sentence rather than a neutral synopsis, dropping the final-incursion alliance question. |
| 9781302939106 | Thor & Loki: Double Trouble: Issues #1-4 | pass | unsupported_claim | Calls Thor and Loki brothers of Odin rather than sons and assigns serpent cleanup to both siblings where the source assigns it to Thor. |
| 9781302520007 | Rocket Raccoon and Groot: Tall Tails: Issues #1-10 | needs_edit | unsupported_claim | Adds intent by saying Groot refuses to discuss the mystery despite the source's correction that he is talking; also omits the distinct mentor-grief thread. |
| 9781302518998 | Dark Reign: Accept Change | needs_edit | unsupported_claim | Declares the groups' identities unconfirmed from a teaser asking who the Dark Avengers are; the book description makes no such confirmation-status claim. |
| 9781302494476 | Civil War II: Choosing Sides: Issues #1-6 | needs_edit | unsupported_claim | Says a major loss causes the division, whereas the source attributes division to the preventive-action question and the loss to later reconsideration. Nick Fury is also absent from that sentence's citations. |
| 9781302526580 | Doctor Strange by Mark Waid Vol. 1: Issues #1-11 | pass | unsupported_claim | Changes the source's new companion helping when Super-Skrull arrives into Super-Skrull himself helping Strange; invents a helper relationship. |
| 9781302480554 | Devil Dinosaur by Jack Kirby: The Complete Collection: Issues #1-9 | appropriate_abstention | appropriate_abstention | No source synopsis; no claims generated from title alone. |
| 9781302515737 | Doctor Strange by Mark Waid Vol. 3: Herald: Issues #12-17 | pass | unsupported_claim | Makes Strange the banished figure instead of Galactus and describes an alliance with a feast rather than an unspecified ally; rescue objective becomes unclear. |
| 9781302436322 | Ultimate X-Men Vol. 16: Cable: Issues #75-80 | pass | pass | Cable/future/school premise and separate Academy of Tomorrow bonus story are entailed by cited E1/E2/E6. Keep existing stronger editorial. |
| 9781302531553 | Miles Morales: Spider-Man Modern Era Epic Collection: Hero in Training | needs_edit | worker_failure | Rejected for exceeding 80 words. Raw response preserved; no automatic retry or correction. |
| 9781302533427 | Sabretooth: The Dead Don't Talk: Issues #1-5 | needs_edit | unsupported_claim | Strengthens may affect Wolverine into a definite threat and invents Mad Dog Murphy fighting gangs including Dragonfire and a crocodile man, whose affiliations/actions are not stated. |
