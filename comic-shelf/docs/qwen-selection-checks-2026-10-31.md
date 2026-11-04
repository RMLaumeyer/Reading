# Qwen selection review checks — October 31, 2026

Added three deterministic review checks to the existing Qwen worker. They flag a draft made entirely of rhetorical questions, selected text with broken contractions/replacement characters, and a selected assertion that omits an immediately following short caveat such as “Or is he?” The review queue includes literal evidence and the omitted caveat when applicable. The original Qwen prompt, model configuration, source eligibility and selected text remain unchanged.

These are publication holds requiring explicit source/context assessment. An accept decision or a revised string with valid citations cannot bypass an unresolved warning in the queue. Tests exercise that behavior through the actual worker-review, decision and staging pipeline. The worker still never publishes.

## Retrospective replay

Replayed the latest available accept/revise decision per ISBN against the original selected synopsis and full source descriptions, matching each immutable queue to its decision hash. Excluded rewritten or empty proposals. All 108 eligible selection drafts had matching queues. No model requests were needed, and historical model results, decisions and publications were not modified.

| Previous review outcome | Drafts replayed | Newly flagged |
| --- | ---: | ---: |
| Accepted unchanged | 44 | 0 |
| Required revision | 64 | 6 |

Four flags identify damaged source text, one identifies the lost Hank Pym/Ultron caveat, and one identifies the question-only Monsters Unleashed synopsis. The six flagged revisions are distinct editions.

The first qualifier pattern was too broad: it also treated new plot questions about She-Hulk and Hawkeye as qualifiers. Both initial code and replay are preserved. The final pattern recognizes only short pronoun questions, with optional words such as “really”; tests explicitly exclude follow-on plot questions and hyphenated names. The final replay removes those two ambiguous matches.

This is an in-sample development replay using the same corpus that informed the checks. Zero flags among previously accepted drafts is not an independently measured false-positive rate. Catching six of 64 revised drafts leaves 58 without a new warning. Missing protagonists, missing setup, promotion, additional plot threads and many semantic qualifications still require editorial assessment. These checks do not make Qwen more factually accurate, verify entailment, certify completeness or improve its unchanged acceptance rate by themselves.

## Validation and artifacts

All 348 Python tests passed, including positive/negative boundary cases, same-source/immediate-context constraints, preservation of raw model selections, and staging refusal for both accept and revise decisions with unresolved warnings. Whitespace checks passed. Production catalog data was not changed by this work; the approved total remains 117.

The final replay is data/local-ai-trials/selection-check-replay-v2-20261031, with replay.py, replay.json, summary.json, replay.log and worker-v2.py. The broader first attempt is data/local-ai-trials/selection-check-replay-20261031, including worker-v1.py. Queue/event paths and hashes are retained per replay row. New inference runs must freeze the updated code into a new manifest; older prepared runs retain their historical code hashes and must not be rewritten to bypass their freeze checks.

Next, use a small newly reviewed batch to assess the checks outside these development examples. Measure unchanged Qwen acceptance and editorial corrections separately from new warnings. Preserve source/identity holds and manual review; absence of a warning is not publication approval.

That follow-up is complete in [the fresh ten-edition validation report](qwen-selection-check-fresh-ten-2026-10-31.md). It found one new warning and five other editorial problems without new warnings; the original replay counts above remain historical.
