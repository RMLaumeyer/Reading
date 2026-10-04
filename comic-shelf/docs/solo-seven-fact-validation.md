# Seven-fact development benchmark — 2026-09-27

The final version recovered **7/7 annotated facts in all three repetitions**, up
from 6/7 previously. All 24 emitted excerpts were exact source quotations, with
zero unsupported story-title or issue-scope claims. This is a development-set
improvement, not proof of complete unaided enrichment.

The retained approach preserves the existing story selector and adds a bounded
review of omitted planning excerpts when fewer than three highlights were
selected. It does not change reading-path assembly, edition inventory, source
retrieval, model/server settings, or character collection.

The missing excerpt was present in the edition source: "Learn all about Nick
Fury's master plan." The legacy keyword filter excluded it beside battle-related
evidence. Allowing it through the filter was insufficient: the model still
omitted it. Replacing selection instructions also lost previously recovered
facts. The retained second pass classifies each omitted planning excerpt and may
accept it as a premise or abstain. There are no edition names, character names or
benchmark reference terms hardcoded into the collector.

The review retains the source-quality filters, validates every expected evidence
ID and classification, rejects duplicate JSON keys, preserves exact quotations,
and caps total highlights at three. It records selected and deferred supplemental
IDs. A full primary selection triggers no second request. The legacy trial and
quality modules remain unchanged. Plan details, official story titles and issue
boundaries are never inferred from this excerpt.

## Controlled experiments

All runs use the unchanged `accuracy-v1-validation/suite.json`, the same four
cached editions, Qwen3.5-4B, temperature zero and sequential requests. The suite's
original description predates tuning: all four cases are now development cases.
Reference labels were not edited and are not passed to the model. Every run,
including regressions, is preserved in its own directory.

| Run | Recovered facts | Result |
| --- | --- | --- |
| Previous retained `accuracy-v1-candidate3` | 6/7 in each of three repetitions | Comparison baseline |
| `accuracy-v2-planning` | 6/7 in each of three repetitions | Filter expansion alone insufficient |
| `accuracy-v2-planning-prompt` | 5/7 in each of three repetitions | Rejected |
| `accuracy-v2-coverage-probe` | 4/7, one repetition | Rejected |
| `accuracy-v2-classify-probe` | 6/7, one repetition | Recovered the plan but lost another premise |
| `accuracy-v2-supplement-probe` | 7/7, one repetition | Selected for repeatability validation |
| `accuracy-v2-final` | 7/7 in each of three repetitions | Retained |

Final repetitions and preservation checks are recorded in
`data/local-ai-trials/accuracy-v2-validation/checks.json`; raw final outputs are in
`accuracy-v2-final`. The final version adds strict classification validation and
audit logging after the initial supplemental probe. Tests caught an invalid-enum
validation gap; explicit validation was added before the final repetitions.

The separate `accuracy-v2-final-challenges` run uses three synthetic regression
cases: a battle plus a differently named participant's scheme, promotional
planning copy, and unanchored pronouns. These are small development probes, not
additional real editions or a held-out accuracy estimate. Promotion/pronoun
rejection occurs in the deterministic filter; it is not evidence of model judgment.

## Limits

Seven annotated facts are not seven complete stories. This suite has four editions
from two event families, with provisional assistant/source-based labels. Repeated
inference measures stability, not independent accuracy. Tuning on these cases does
not establish generalization. Front Line still contains a vague extra battle
excerpt; verbatim grounding is not the same as useful distinct-story precision.

The recovered plan is only a source teaser. What the plan involves, where the
story begins and ends, and which issues contain it remain unknown. The three-item
cap can still omit a fourth premise, and keyword filtering can still miss other
forms of plot evidence. A failed supplemental request fails the highlight stage
under the existing stage-error handling; it is not silently treated as complete.

The next gate remains an independently adjudicated held-out set for actual
edition contents, featured-story scope and complete required reading order, as
defined in [the broader benchmark](solo-accuracy-benchmark.md). Website data and
publication eligibility remain unchanged.

## Validation and preservation

189 tests pass. All nine synthetic case/repetition checks passed: the separate
scheme was recovered and promotional/unanchored examples emitted nothing. SHA-256
verification found no changed or missing files among 5,224 pre-existing public/data
files. Final code snapshots, raw attempts and checks are preserved in the audit
folder. Website data and historical runs are unchanged. `git diff --check` passed.
