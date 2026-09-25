# Enrichment reassessment and controlled benchmark

September 22, 2026. Decision document only: no implementation changes, model downloads, inference runs, or website updates.

## Decision

Prioritize **complete reading orders, then useful featured stories**. Contents and edition identity are prerequisites for reliable ordering. Summaries support those outcomes; characters and review scores are secondary. Stop iterating on character heuristics as the main measure of progress.

The recommendations here supersede the character-first next-fix priorities in the historical v18 assessment, without modifying that assessment or its results. Keep v18 as an immutable diagnostic baseline. Compare a larger model before further extraction patches, then evaluate any workflow change separately.

## What the existing evidence establishes

Read: `docs/local-ai-trial.md`, `data/local-ai-trials/trial-18-full/assessment.md`, its run manifest, and relevant extraction/control flow in `scripts/local_ai_trial.py`.

- V18 completed 8/10 drafts, with two errors, versus 10/10 in v14. Seven summaries, seven issue lists and eight page counts include partial results; completed drafts alone have six issue lists and seven page counts. There is no reading-order guidance or review score.
- Exact citations and 56 passing offline tests did not catch incorrect creator roles. Neither is a semantic accuracy score. The ten familiar cases are now a development/regression set, not an untouched test set.
- Character extraction precedes stories, summary and reading advice. A primary character failure exits the book, preventing those later stages. Surviving bibliography is retained, but useful narrative work is never attempted.
- Extractive story/summary selection filters evidence by extracted character names when names exist. Missing or incorrect names can therefore remove relevant plot evidence even when character extraction completes.
- Current `readingOrder` is a single text claim. It does not represent or validate an entire sequence, required predecessor links, crossover interleaving, duplicate editions, or missing volumes.
- Current highlights are selected publisher sentences. They can be faithful yet repetitive, incidental, or insufficient to describe the featured stories. Selection of plot excerpts is not proof of arc coverage or significance.
- Cached publisher copy and trade-review rows were collected for book enrichment, not comprehensive reading-order research. A larger model cannot supply missing source evidence reliably. The current zero reading-order yield cannot distinguish model weakness from inadequate retrieval on its own.

## Hardware and comparison model

Read-only inspection used Windows CIM and `lms ps` / `lms ls`.

| Item | Observed |
| --- | --- |
| Computer | Lenovo 82YN |
| CPU | Intel Core i7-1360P, 12 cores / 16 logical processors |
| OS-visible physical RAM | 14,743,887,872 bytes, about 13.73 GiB |
| Free physical RAM at inspection | 761,524 KiB, about 0.73 GiB; transient snapshot |
| Graphics | Intel Iris Xe integrated graphics; no discrete GPU reported by CIM |
| Loaded model | Qwen3.5-4B, reported size 3.38 GB, context 8192, parallel setting 4, idle |
| Other installed model | Nomic text embedding model, 84.11 MB |

The adapter's reported roughly 2 GiB is not a separate dedicated VRAM budget; integrated graphics share system memory. Installed DIMM capacity was not independently measured. Do not size a model by adding the graphics figure to usable RAM.

**Recommend Qwen3.5-9B, post-trained, GGUF Q4_K_M**, as the stronger comparison candidate. Staying in the same family reduces architecture/template differences while increasing capacity. Qwen's published results favor 9B over 4B on several general benchmarks, but do not establish comics accuracy, quantized performance, or superiority with reasoning disabled. See the [official model card](https://huggingface.co/Qwen/Qwen3.5-9B).

One concrete artifact is `Qwen3.5-9B-Q4_K_M.gguf` in [bartowski/Qwen_Qwen3.5-9B-GGUF](https://huggingface.co/bartowski/Qwen_Qwen3.5-9B-GGUF), listed at 6.17 GB. This is a community quantization; pin its revision and file SHA-256. Weight-file size excludes runtime buffers and context memory. Expect CPU/shared-memory operation; acceleration and throughput remain unmeasured.

This is a conditional fit, not a model ready to load alongside the current one. For a future trial, unload the 4B before loading 9B, free application memory, use one inference slot, and start with the same 8192-token context for both. Reserve at least 2 GiB free physical memory during a representative maximum-size request and reject sustained paging or allocation failures. Measure peak process/total memory. If either model cannot fit the shared setup, define a smaller-context experiment for **both**, with identical evidence fitting the limit; never silently truncate one arm. Larger 14B/27B-class models are not the first choice on this memory budget. No model or server settings were changed in this reassessment.

## Proposed enrichment design after comparison

1. Resolve edition identity and complete contents first, recording exact ISBN, series start year, issue identifiers, partial-story material, overlaps, and unresolved conflicts. Retain conservative deterministic parsing for unambiguous bibliography; model size should not receive credit for those deterministic results.
2. Collect evidence specifically for reading orders and featured stories. Prefer publisher contents/collection pages, official issue descriptions and explicit event checklists; use attributed specialist guides for disputed recommended order. Cache dated sources and distinguish publication order, recommended order and in-universe chronology. Publication dates alone do not establish mandatory story order.
3. Build a collection-level order with stable issue/volume identities and supported predecessor relationships. Label required reading, optional tie-ins and alternative editions separately. Include needed books outside the owned shelf as explicit gaps. An edition conflict blocks dependent placement, not unrelated story facts.
4. Define completeness against a stated series/run/event boundary and date. A disconnected partial sequence is not a complete order. Preserve legitimate alternative orders and disputed links; check missing nodes, duplicate content, cycles and contradictory links deterministically.
5. Produce one to three distinct featured stories per collection when supported: central premise, scope/covered issues when known, and why the story is featured. Use official arc names only with evidence; label descriptive headings and editorial recommendations accordingly. Do not equate promotional praise with importance.
6. Run characters as optional independent enrichment. Character errors must not block ordering or stories, and character recall must not filter their evidence. This is a proposed architecture change, not a patch made here.

## Controlled accuracy benchmark

### Two separate experiments

**A — model comparison with frozen v18:** rerun the existing ten packets with 4B and 9B under the same frozen scripts, prompts, schema and inference policy. This tests whether a stronger model helps the current workflow. Count blocked stages and errors explicitly. Use the old v18 results only as historical reference, not as the controlled 4B arm. Character-stage failures remain visible in this experiment; do not fix them between arms. No claim of reading-order completeness can follow from experiment A.

**B — product benchmark:** after A, define and freeze a separate reading-order/story-focused harness and richer packets. Run both models on that same harness. Compare models within B; compare workflow changes within a fixed model and matched evidence. Do not attribute an A-to-B improvement solely to the model because sources and workflow also change. Freeze the design below before inspecting test outputs.

### Dataset and gold answers

- Keep the ten repeatedly tuned books as development/regression cases, including both edition conflicts, initials, creator credits, partial Annual material and contents-only evidence.
- Add 30 previously unused collection editions across six complete, bounded reading paths (five evaluated editions per path, with external prerequisites recorded separately). Select two straightforward runs, two crossovers and two relaunch/overlap-heavy paths. Include at least six absent/ambiguous-evidence cases across the set. This is a proposed selection quota, not an already assembled dataset.
- Split by entire reading path: two paths / ten editions for development, four paths / twenty editions held out. Do not split adjacent volumes across development and test. Maintain at least one crossover and one relaunch/overlap path in held-out evaluation.
- Before inference, record the complete expected node inventory, required predecessor links, acceptable alternative links/orders, optional tie-ins, duplicates, missing shelf volumes, expected abstentions and featured-story facts. Give each gold fact exact source passages and edition identity. Existing website annotations are comparison material, not automatic ground truth.
- Separate two labels: whether a fact is true in the independently researched gold set, and whether the supplied packet supports it. Missing evidence reduces retrieval coverage; unsupported invention remains an extraction error even when accidentally true.
- Have two human reviewers independently annotate/adjudicate gold answers and blind-score shuffled model outputs. Resolve disagreements with evidence and keep the original judgments. If only one reviewer is available, label the assessment provisional. A same-model critic is not the gold evaluator.

### Fixed execution conditions

- Hash scripts (including imported quality helpers), source bytes, normalized packets, schema, prompts and gold files; gold remains outside model input. Record exact GGUF revision/hash, quantization, chat template, LM Studio/runtime versions, hardware, context, offload, threads, batch size and all sampling parameters. The existing manifest alone does not record all these controls.
- Use one loaded model and one active request at a time; identical context, stage token budgets, temperature 0, reasoning disabled, retry limit (one) and ten-minute request timeout. Verify on a development probe that both models actually suppress thinking and support the requested JSON schema. If not, record incompatibility rather than changing one arm silently.
- Use the same packet order and three fresh repetitions per model. Alternate model blocks 4B/9B, 9B/4B, 4B/9B. Warm up once per load on a non-test packet; report load/warm-up separately. Keep power mode and background workload comparable. Temperature zero does not guarantee identical outputs.
- Save every raw response, retry, validation error, abstention, partial result and per-stage time into new uniquely named folders. Never resume into or regenerate reports inside historical trial folders. No publication or live web retrieval during inference.
- Hash website data and historical trial files before/after execution. Benchmark output stays outside served assets. Freeze any failed run; changes require a new experiment ID and rerunning both arms.

### Scoring and release gates

Report raw numerators/denominators per case and per field, plus macro averages by path. Repetitions measure stability, not additional independent test cases. Report uncertainty with resampling by whole path and acknowledge that four held-out paths cannot support strong population claims.

| Priority | Metric | Proposed gate for a reviewed pilot |
| --- | --- | --- |
| Reading order | Required node recall: correctly included mandatory nodes / all mandatory gold nodes | 100% in every held-out bounded path before calling it complete |
| Reading order | Required edge precision and recall; score allowed alternatives against their annotated constraints | At least 98% precision and 95% recall overall; no reversed mandatory dependency, unresolved required gap, or cycle in a path labeled complete |
| Reading order | Whole-path completeness: paths satisfying all required nodes/links and edition/alternative constraints / all evaluated paths | 100% of paths labeled complete must actually be complete; publish numerator/denominator for all paths |
| Featured stories | Supported atomic claims / all emitted story claims | At least 98%; zero invented official arc titles, edition mix-ups or material plot fabrications |
| Featured stories | Recovered distinct central gold story facts / all packet-supported central gold facts | At least 90%; missing outputs count as missed facts |
| Featured stories | Human relevance/usefulness, 0 unusable, 1 incidental/repetitive, 2 useful but incomplete, 3 central/distinct/sufficient | At least 2 on 90% of evidence-sufficient editions |
| Reliability | Completed core fields / requested core fields with adequate evidence; separately report full-book completion | At least 95%; character failure cannot block a core field in B |
| Abstention | Correct abstentions / cases requiring abstention; also false abstentions / answerable cases | 100% on known edition conflicts; at most 10% false abstention on answerable core cases |
| Secondary | Character mention precision/recall and role errors; review accuracy | Diagnostic only; cannot compensate for core-field failures |

Keep evidence coverage separate: gold core facts available in packets / all gold core facts. Report missing-source cases in end-to-end completeness, even if abstention is correct. An empty system must not earn a high score merely by avoiding false claims. For precision with no predictions, report N/A, not 100%.

Compare paired results: correct/incorrect/abstained/failed/not-attempted for every field, exact supported facts, critical errors, and human review time. Report latency median/p95, retries, tokens and memory as secondary costs. No single weighted score may hide a reading-order failure. Prefer 9B only if it meets core gates and improves supported core coverage without new critical errors; a tie does not justify its memory/latency cost. These small pilot gates do not authorize unattended publication.

## Next sequence

First perform the 9B memory/compatibility probe and frozen model comparison A. Then assemble the independent gold/source set for B and implement its minimal isolated harness. Only after those measurements choose targeted workflow patches, prioritizing independent core stages, order evidence and featured-story coverage. Preserve v18 and all previous trials as evidence throughout.

This reassessment does not execute either benchmark or establish that 9B is more accurate on this collection.
