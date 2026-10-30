# Bounded Qwen worker trial — October 27, 2026

`scripts/enrichment_worker.py` processes up to ten frozen edition packets sequentially. Code parses contents; Qwen3.5-4B selects a cited synopsis excerpt. It skips character and reading-order stages, isolates failures, checkpoints a review queue after every book, and never publishes. Each experiment requires a new directory. Packet and Python code hashes are verified before inference.

The first completed run is `data/local-ai-trials/worker-20261027-ten-v2`. Ten ISBNs were sampled with seed 20261027 from cached Google Books editions, excluding ISBNs found in prior model input packets and edition result directories. Sources were frozen before inference. This tests extraction from cached evidence, not fresh retrieval or catalog-wide accuracy. The earlier `worker-20261027-ten` preparation failed before inference because its exclusion rule incorrectly included catalog snapshots; that failed directory remains preserved.

Results: 10/10 processed, zero worker errors, five drafts without mechanical blockers, five flagged for review, and nine verbatim source-grounded synopsis excerpts. One edition had no synopsis. Total processing time was 53.37 seconds. Grounding does not measure relevance, full plot coverage, or correct edition attribution. For example, Trials of X selects a single plot thread; Spider-Man/Deadpool selects a climax rather than the broader premise. No independent semantic accuracy or correction-time score has been established.

53 existing edition-parser tests pass. The code and sources remained fixed during inference. Outputs live in the isolated trial folder; the worker has no publication code. All drafts require human review, including those without mechanical blockers.

To run a new sample from the project directory:

```powershell
python scripts/enrichment_worker.py --name UNIQUE_NAME --prepare-only
python scripts/enrichment_worker.py --name UNIQUE_NAME --run-prepared
```

Use the same Python environment as the project and a local LM Studio endpoint at port 1234. The model ID defaults to `qwen3.5-4b`. `status.json`, `review-queue.json`, individual results with raw attempts, and `report.json` make runs inspectable. This is a command-driven local worker, not a persistent scheduled agent. Next: review the frozen outputs for usefulness and correction effort before changing extraction or expanding the batch.
