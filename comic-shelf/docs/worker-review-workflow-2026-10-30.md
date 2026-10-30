# Evidence-preserving worker review

The local Qwen worker now produces a dedicated `review/review.md` and `review/review-queue.json` after each batch. Each edition includes full source descriptions, the proposed synopsis, eligible but unselected passages, edition/contents flags, and explicit unreviewed editorial status. A proposal under eight words gets a context-review flag; this is a heuristic, not a semantic quality score. Full descriptions are retained in individual result files before the model call, including when inference subsequently fails.

The source description and proposal remain separate. Unselected passages may be redundant or irrelevant, and passages rejected by the evidence filter are only visible in the full description. All outputs remain unpublished drafts.

Export existing runs without inference or overwriting their artifacts:

```powershell
python scripts/enrichment_worker.py --review-run data/local-ai-trials/worker-v3-fresh-20261027 --review-output data/local-ai-trials/NEW_REVIEW_DIRECTORY
```

The export verifies frozen packet hashes and requires a new output directory. The original ten-book run was exported into `worker-review-20261030`. Its Doctor Strange proposal is now explicitly flagged for insufficient length/context. No historical result was rewritten.

A live two-book Qwen3.5-4B smoke run, `worker-review-smoke-20261030`, completed both editions with zero worker failures, generating review files automatically. These are reused development packets, not new accuracy evidence. Seven worker tests and 53 edition-parser tests pass. Source preservation and review routing were checked; human review time and net effort saved remain unmeasured.

Next product step: use this evidence-preserving queue to record reviewer decisions and corrections separately from frozen model output. The current export intentionally makes no acceptance or publication decisions.
