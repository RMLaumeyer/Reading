# Qwen adjacent-passage block comparison — October 31, 2026

Implemented an opt-in block selection mode and compared it with the saved ten-edition sentence-selection cohort. Keep sentence selection as the default. Blocks produced three unchanged editorial passes versus four for sentences, with one improvement and two regressions. No experimental draft was published; the approved synopsis total remains 123.

| Measure | Sentences | Blocks |
| --- | ---: | ---: |
| Unchanged editorial passes | 4/10 | 3/10 |
| Needs revision/research | 6/10 | 7/10 |
| Mean synopsis words | 63.7 | 79.5 |

These are Codex development judgments under the same review standard as the preceding cohort, not independent gold labels. Existing edition eligibility is separate: an editorial pass does not clear missing years, unspecified partial material, source-name damage or source-contents differences.

## Implementation

The new --excerpt-mode blocks option pairs nonoverlapping adjacent eligible passages from the same source. A pair must be separated only by whitespace and cannot cross a blank paragraph, filtered text, source boundary or bibliographic section. Pairing preserves the exact intervening whitespace and literal source substring. Pairs are limited to 100 words and 1,200 characters; longer existing passages remain intact singletons rather than being truncated. Source eligibility and collecting/creator filters remain in force.

Qwen still selects at most three IDs using the original prompt, model configuration and grounding validation. Block evidence is exported as literal block quotations, and omitted-passage review uses the corresponding block candidates. Manual source holds and the selection-warning checks remain active. Rewriting cannot be combined with the experimental block option. Prepared manifests freeze the excerpt mode; older manifests default to sentence mode.

The three-ID limit now permits up to six eligible passage units instead of three. This is an expanded evidence budget, so any coverage benefit cannot be attributed solely to coherence. Pairing is positional, not a claim that the sentences form a complete semantic unit. Blocks can still begin with a dependent pronoun or omit necessary earlier context.

Example experimental preparation:

```powershell
python scripts/enrichment_worker.py --name NEW_UNIQUE_RUN --count 10 --packets-from data/local-ai-trials/selection-check-fresh-ten-20261031 --excerpt-mode blocks --prepare-only
```

The default remains sentences. New runs must use a new name and freeze current code; old run manifests and raw results are preserved.

## Reviewed cases

| Edition | Sentence pass | Block pass | Finding |
| --- | --- | --- | --- |
| Shuri | No | No | Restores search/rescue setup, but retains damaged names/contractions and extra filler |
| Hunt for Wolverine | No | No | More investigator questions without the missing resurrection/search setup |
| Laura Kinney: Wolverine | Yes | No | Regression: starts with an unexplained past-life reference and drops the X-23 introduction |
| Miles Morales: Beyond | No | No | Adds the distinct Amulet thread, but keeps damaged text and more rhetorical filler |
| Annihilation Vol. 2 | Yes | Yes | Coherent central war premise; loses the baseline's Ronan subplot, so coverage is a tradeoff |
| Kanan | No | No | Loses Order 66 setup and retains the damaged character identity and promotional directions |
| Star Wars: The Escape | Yes | No | Regression: loses named rebel context and adds damaged punctuation and a reader-directed opener |
| Darth Maul | No | No | Adds protagonist/setup and clears the question-only warning, but retains broken source text |
| Return of the Valkyries | No | Yes | Improvement: introduces Jane Foster and preserves the further-Valkyrie revelation |
| Doctor Doom | Yes | Yes | Usable Doom/Kang mission overview; opening pronoun and lost Latveria setup are weaker than baseline |

The Annihilation and Doctor Doom passes allow limited overviews rather than requiring every subplot. Those judgments and their coverage losses are explicit in assessment.json; stricter editing would lower the block result further. The two regressions and extra source/filler problems already fail the stated adoption rule, regardless of those borderline cases.

## Verification and limits

All 355 Python tests passed, including exact-whitespace preservation, pair limits, filtered-text/source/paragraph boundaries, unchanged prompt/schema behavior, block-aware omitted passages and preservation of manual holds. Whitespace checks passed.

All ten cases completed without worker failures using ten new model requests in 60.64 worker seconds, excluding review. All 21 selected block quotations are literal source substrings. All 77 frozen Python files, packets, prompts, model identifiers and inventories passed verification. The current sentence candidate generator exactly reproduces the historical baseline's actual candidate payloads, so the comparison did not silently change the sentence baseline. The input source packets are byte-identical to the original ten-case run.

The original sentence run preceded the block run; order was not randomized and there were no repeated trials or independent adjudication. The small reused cohort is development evidence, not a general accuracy estimate. Larger outputs, rhetorical questions and source damage remain important review concerns. Clearing a narrow mechanical warning is not evidence of overall quality: Darth Maul demonstrates that directly.

Exact before/after hashes confirm that canonical, public and built enrichment files are unchanged. No new publication or remote deployment occurred. Experimental review findings do not supersede the site's approved revisions or the latest held-edition research decisions.

Artifacts are in data/local-ai-trials/block-comparison-ten-20261031: rubric.json, frozen inputs/code, original model responses, review exports, assessment.json, assessment.md and verification.json. The control inputs/results remain in selection-check-fresh-ten-20261031.

The next decision should be based on whether a narrower, context-aware approach actually saves editorial work. This trial does not justify a broader block rollout, a prompt switch, or relaxed publication gates.

The subsequent [selection-audit experiment](qwen-selection-audit-2026-10-31.md) returned the same outputs in all ten cases and added ten requests without saving editorial work. It was not adopted.
