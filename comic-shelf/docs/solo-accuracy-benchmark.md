# Story coverage and reading-path validation — 2026-09-26

The retained change improves recovery of annotated edition premises from 5/7 to
6/7 on four fixed source packets, consistently across three repetitions. This is
small development-set evidence, not readiness for complete unaided enrichment.
Reading order and contained/featured stories remain the priorities; character
appearances were not requested or tested.

## Controlled comparison

`scripts/benchmark_enrichment.py` reads a frozen suite whose reference facts are
never sent to the model. Input, suite and implementation hashes, raw model
responses, failures, timings and per-case scores are retained in new directories.
All inference used the loaded Qwen3.5-4B model, sequential requests, temperature
zero and the same source packets. No live retrieval occurred during inference.
Server settings were not changed.

Four editions cover two event families: Civil War: Front Line, Siege, Siege:
Embedded and Siege: Battlefield. Seven provisional source-grounded facts were
annotated before the baseline inference. These are assistant annotations, not
independent human gold. Front Line is a familiar regression case; the other cases
became development cases when their failures informed changes. Three repetitions
measure stability; they do not make twelve independent cases.

| Version/run | Facts recovered per repetition | Exact grounded excerpts across repetitions | Decision |
| --- | --- | --- | --- |
| `accuracy-v1-baseline` | 5/7, 5/7, 5/7 | 15/15 | Preserved comparison |
| `accuracy-v1-candidate` | 4/7, 4/7, 4/7 | 21/21 | Rejected: broader evidence selection regressed |
| `accuracy-v1-candidate2` | No valid inference | No output | Preserved implementation failure: wrong legacy call signature |
| `accuracy-v1-candidate3` | 6/7, 6/7, 6/7 | 21/21 | Retained narrow correction |

Candidate2 logged twelve local TypeErrors before making model requests. The call
signature was corrected and unit tests passed before candidate3 ran. These failed
records remain intact; they are not model failures. Baseline's scorer hash differs
from later runs because suite-ID validation was added; scoring logic did not change.

The retained extractor protects numbered abbreviations such as `No. 1` while
splitting sentences and rejects `[Author]` placeholder sentences. It restores
original punctuation and requires exact source membership. The frozen legacy
selector and its keyword pruning remain unchanged. The sentence correction
keeps Speedball's name, imprisonment and Stamford in one excerpt, recovering the
previously missed premise. Removing keyword pruning exposed more candidates but
produced less useful selections, so that larger change was removed.

## What the scores do and do not establish

The benchmark checks verbatim source grounding with the correct edition ISBN,
predeclared term combinations for central-fact recall, source placeholders, and
unsupported story-title/issue-scope claims. All successful runs emitted zero
unsupported scope claims. Grounding precision is undefined for empty output.
Term matching is an auditable reference check, not independent semantic judgment.

The retained output still misses Nick Fury's plan in Battlefield: keyword pruning
discards that evidence. Front Line also emits a vague, pronoun-dependent sentence
about braving the battle; it is grounded but not a useful distinct story. Therefore
21/21 grounded excerpts must not be presented as 100% useful-story precision.
Neither the labels nor the source descriptions establish exhaustive story titles,
story boundaries, exact issue scopes or completeness of the editions.

## Reading-order checks

`accuracy-v1-validation/check_reading_paths.py` reparses three saved publisher
pages and builds collection mappings from saved edition inventories. Expected
placements and uncertainty states were fixed before replay. All 30 assertions
passed, including exact sequence, edition placements, gaps, alternatives and
abstention from required-reading or complete-order claims.

| Familiar case | Source issues | Unique whole-issue matches | Identity-review positions | Remaining source positions without whole coverage |
| --- | --- | --- | --- | --- |
| Civil War, three selected editions | 98 | 10 | 0 | 88 |
| Secret Invasion, X-Men edition | 98 | 0 | 3 | 98 |
| Absolute Carnage, two selected editions | 31 | 9 | 0 | 22 |

The Civil War overlap remains seven alternative-edition positions, not duplicated
coverage. Secret Invasion's inferred year remains under review. These gaps concern
only the selected editions, not the user's entire collection. Preserving a
publisher's displayed sequence is not proof of correct complete reading order.
This is a familiar regression check, not independent path-accuracy measurement.

## Acceptance benchmark still needed

Keep this suite as development/regression evidence. Before calling collection
unaided, freeze the broader benchmark proposed in the original reassessment:
30 distinct editions and six reading paths, with event families reserved from
tuning. Independently adjudicate reference inventories, exact editions/series
years, whole versus partial contents, official story names and boundaries, and
required versus optional issue order. Mark facts unknown when sources do not
establish them rather than awarding credit for guesses.

Score retrieval availability separately from extraction accuracy. Report exact
inventory precision/recall, useful distinct-story precision/recall and exact
story scope, required-issue coverage and pairwise order accuracy on adjudicated
relations, plus unsupported claims, correct abstentions and manual interventions.
Use the same cached inputs for model comparisons, then a separate end-to-end live
retrieval pass. Do not tune on the held-out results; a failed case becomes
development evidence and requires a replacement held-out case.

For an initial autonomy gate, require zero incorrect accepted edition identities,
invented issue/story scope or false completeness claims, at least 95% precision
and recall on adjudicated inventories and useful stories, and complete recovery
of adjudicated required issues and ordering constraints on every evaluated path.
Report denominators and uncertainty: even passing this small gate would support
only bounded draft collection, not unrestricted catalog-wide accuracy or
automatic publication. This gate has not been met or fully evaluated.

The next substantive work is source-backed story boundaries and independent
series identification, followed by held-out path evaluation. More attractive
synopsis excerpts alone cannot satisfy the user's complete-reading-order goal.

## Validation and preservation

185 targeted tests pass. SHA-256 checks found zero changed or missing files among
5,151 pre-existing public/data files. Website data and historical results are
unchanged. All new runs, including rejected and failed candidates, are preserved.
`git diff --check` passed with only Windows line-ending notices. The audit folder
contains the frozen suite, inputs, before/rejected/final extractor snapshots,
reading-path replay and `checks.json`.

Reproduce the story comparison from the project root with a fresh output name:

```powershell
python scripts/benchmark_enrichment.py --suite data/local-ai-trials/accuracy-v1-validation/suite.json --name NEW-UNIQUE-RUN --model qwen3.5-4b --repeats 3
```

Add `--extractor data/local-ai-trials/accuracy-v1-validation/edition_highlights_before.py`
for the preserved baseline. Existing output names are intentionally rejected.
