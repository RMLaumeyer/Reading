# Qwen synopsis prompt comparison — October 30, 2026

The longer revised instructions did not improve this development sample. Retain the original default prompt. Of 25 fresh editions, six original-policy drafts passed editorial review unchanged versus four revised-policy drafts. Both policies had zero worker failures. The test used 50 local model requests; eight pairs produced identical text.

| Measure | Original | Revised |
| --- | ---: | ---: |
| Editorial passes without correction | 6 | 4 |
| Needs editorial revision | 17 | 19 |
| Appropriate abstentions | 1 | 1 |
| Edition-format scope holds | 1 | 1 |
| Unblocked passing drafts without an existing stronger summary | 3 | 2 |
| Exact source quotations verified | 53 | 44 |
| Worker processing seconds | 152.35 | 142.47 |

Editorial review was performed by Codex using the saved source checklist and rubric, under user delegation. These are development judgments, not independent human gold labels or a reliable estimate of general model quality. The original ran first and revised second, once each. Editorial scoring is separate from edition eligibility; most books in this sample have unresolved contents or identity flags. Rates should not be compared directly with the prior 9/32 published-draft acceptance figure, whose denominator was different.

## What changed and what stayed fixed

Added an experimental --premise-policy original|revised switch. Preparation freezes the selected prompt in the manifest; prepared execution uses that frozen text, not the command-line default. Every request attempt now records its prompt hash. The original remains the default. Historical result packets and decisions were not rewritten.

The revised prompt prioritized a named protagonist plus central mission, necessary referents/setup, and distinct major plot threads. It explicitly explained that whole sentences would be joined verbatim and prohibited creator advertising, sales language and misleading rhetorical or ironic assertions. Model, temperature zero, thinking-off request setting, 200 output-token limit, three-excerpt cap, parser and source packet bytes were identical. Both runs used qwen3.5-4b. The revised run reused the original run's 25 freshly selected packets; it is a paired comparison, not 50 different books.

## Findings

The revised prompt correctly abstained on the plot-free Star Comics cast list. However, it changed Deadpool Classic Companion from a safe abstention to a promotional sentence, reduced X-Corp from leadership/staffing/investor action to a cast description, and left Moon Girl with an Or worse yet fragment after removing the question it depended on. It also added an explicit artist/writer advertising sentence to Man-Thing despite instructions to reject credits.

Some changes were locally useful: Zombies Assemble removed a redundant question, and Daredevil restored the Omega Drive premise. Neither outweighed the regressions under the fixed rubric; Daredevil still needed editing. Contents-only Death of Wolverine and creator-history Eternals remained invalid synopsis selections under both prompts.

Whole-sentence extraction has a structural limit: when plot and advertising share a sentence, choosing IDs cannot remove the advertising or safely combine several omitted threads into a concise original sentence. More instructions did not solve that limit on this model. The next experiment should evaluate short source-cited rewrites as a separate output mode, with unsupported-claim checks and the existing edition/publication review gates. That mode was not implemented or validated by this experiment.

## Local publication

Three original-policy Qwen drafts passed source review and had no unresolved edition flags: X-Corp By Tini Howard Vol. 1 (9781302939847), Hulk: Tempest Fugit (9781302496715), and Uncanny Avengers: Unity Vol. 4: Red Skull (9781302499075). Published their original text unchanged, recording Codex as delegated reviewer with user authorization. Twenty-one editions remain held, and the existing Fatal Attractions editorial synopsis was retained. There are now 63 approved synopsis overlays.

The rejected revised policy was not made the production default. No synopsis correction was quietly counted as an unchanged model pass. No inventory, appearance, reading-order or borrowing-availability claim was added.

## Validation and reproducibility

All 97 selected quotations matched the frozen source text. Packet equality, code hashes and actual request prompt hashes passed for both runs. Publication checks verified only the three intended records and synopsis/provenance/source fields changed, every backup and target hash matched, and localhost:5173/enrichment.json served exactly the published bytes. All 35 Python worker/review/staging/promotion tests and 18 catalog tests passed; git diff --check passed. No UI code changed, so the existing static app did not require rebuilding.

Artifacts: data/local-ai-trials/policy-v2-control-25-20261030 and policy-v2-revised-25-20261030. The control directory contains assessment-plan.json, source-checklist.json, both policy assessments, paired-assessment.json, comparison-summary.json, immutable delegated-decisions, approved-staging, publish-receipt and publication-verification.json. Both directories retain complete model attempts and review queues. Re-run inference only with new experiment names; completed runs are immutable.

To select the experiment at preparation time, pass --premise-policy revised alongside --prepare-only. To execute, use --run-prepared; it always uses the frozen premisePrompt. Keep original for normal work based on this result.

## Per-edition assessment

| ISBN | Edition | Original | Revised | Revised assessment |
| --- | --- | --- | --- | --- |
| 9781302506919 | Star Comics: All-Star Collection Vol. 1: Issues #1-3 | needs_edit | appropriate_abstention | Improvement: declines the disconnected cast/genre advertising with no specific plot. |
| 9781302532697 | Marvel Masterworks: The Man-Thing Vol. 2: Issues #2-14 | needs_edit | needs_edit | Adds an explicitly promotional creator-credit sentence to the original's meta commentary despite the revised instructions. |
| 9781302528355 | X-Men Epic Collection: Fatal Attractions | needs_edit | needs_edit | Still omits the Gambit/New Orleans thread; the shorter selection does not fix edition coverage. |
| 9781302502522 | All-New Wolverine Vol. 5: Orphans of X: Issues #25-30 | pass | pass | Same self-contained Wolverine/Daken rescue premise as the original. |
| 9781302495770 | Scarlet Witch Vol. 2: World of Witchcraft: Issues #6-10 | needs_edit | needs_edit | Still opens with unintroduced she and now omits even Wanda's named action; missing global/Pietro conflict. |
| 9781302479916 | Deadpool Classic Companion | appropriate_abstention | needs_edit | Regression from safe abstention to sales-boost humor with an unnamed subject and no concrete plot. |
| 9781302488567 | Ms. Marvel Vol. 5: Super Famous: Issues #1-6 | needs_edit | needs_edit | Kamala's Avengers transition and Jersey City protector role remain, but the actual development-company conflict is absent. |
| 9781302531966 | Black Widow Modern Era Epic Collection: The Itsy-Bitsy Spider | needs_edit | needs_edit | Selects Natasha biography and praise while omitting both the Yelena mantle rivalry and investigations. |
| 9781302532192 | Fantastic Four vs. Galactus: Issues #48-50, 242-244 | needs_edit | needs_edit | Cleaner two-sentence version still omits the later Terrax encounter. |
| 9781302535179 | Gwenpool: All-New, All-Deadly: Issues #1-5 | needs_edit | needs_edit | Adds favorite-character advertising; the doppelganger question is still a teaser rather than a clean edition overview. |
| 9781302939816 | Untold Tales Of Spider-Man: The Complete Collection Vol. 1: Issues #1-14 | needs_edit | needs_edit | Identical extended reader-directed hype and premier-superhero promotion. |
| 9781302478544 | Death Of Wolverine: Issues #1-4 | needs_edit | needs_edit | Still repeats the contents-only description instead of abstaining. |
| 9781302939847 | X-Corp By Tini Howard Vol. 1: Issues #1-5 | pass | needs_edit | Regression: names the X-Corp leaders but drops the staffing/investor actions, leaving only a cast/characterization sentence. |
| 9781302523916 | Incredible Hulk Epic Collection: The Lone and Level Sands | needs_edit | needs_edit | Still starts with creator credit and adds a vague everything-changes tragedy without restoring the specific grief/action context. |
| 9781302494346 | Eternals by Jack Kirby Vol. 2: Issues #12-19 | needs_edit | needs_edit | Same creator-history sentence, no collection-specific premise. |
| 9780785182191 | Deadpool Vol. 8: Operation Annihilation: Issues #36-39 | needs_edit | needs_edit | Repeats the death-seeking premise and omits the distinct Macho Gomez/aggrieved friends conflict. |
| 9781302514389 | Moon Girl And Devil Dinosaur Vol. 7: Bad Dream: Issues #37-41 | pass | needs_edit | Regression: retains Or worse yet without the preceding fearsome-fiends question, creating a dangling fragment. |
| 9781302496715 | Hulk: Tempest Fugit: Issues #77-82 | pass | pass | Identical coherent Hulk/Banner island and childhood-memory premise. |
| 9781302503420 | Green Goblin: A Lighter Shade Of Green: Issues #1-13 | needs_edit | needs_edit | Identical hero background without the Green Goblin role or conflict. |
| 9781302500726 | The Art of Marvel Studios: Doctor Strange | source_integrity_hold | source_integrity_hold | Identical film-plot-only summary still fails to describe the concept-art/analysis edition. |
| 9781302501945 | Zombies Assemble 2: Issues #1-4 | pass | pass | Keeps the stranded Avengers and attributed cure claim; removes a redundant teaser without asserting the cure works. |
| 9781302499075 | Uncanny Avengers: Unity Vol. 4: Red Skull: Issues #18-23 | pass | pass | Names the weakened Avengers Unity squad and impending Red Skull threat. Less concrete than the original trap description, but a coherent concise central conflict. |
| 9781302014155 | Daredevil By Mark Waid Vol. 3: Issues #11-15 | needs_edit | needs_edit | Restores the Omega Drive team-up and Latveria, but the first sentence contains reader-directed meanest-team-up hype and the romance thread is omitted. |
| 9781302535209 | Hulk Modern Era Epic Collection: Code Red | needs_edit | needs_edit | Red Hulk/X-Force setup still omits the separate Banner/Skaar/Osborn thread. |
| 9781302506322 | Dracula: Issues #1-4 | needs_edit | needs_edit | Identical promotional definitive/classic/invented-the-genre cast list, not a clean plot sentence. |
