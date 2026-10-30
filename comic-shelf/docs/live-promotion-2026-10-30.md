# Local enrichment promotion and rollback

`scripts/promote_enrichment.py` promotes nonempty human-reviewed staging packages to the local served catalog. It rejects assistant previews and rebuilds staging from the current queue, decisions, catalog and enrichment to detect changed inputs or withdrawn approval. The staged payload hash must match. Publication requires the shared collector lock, so collectors cannot run concurrently with promotion.

The publisher writes a synopsis-only canonical overlay in `data/approved-synopses.json`, then the public enrichment file and the built client enrichment file if that directory exists. The automatic, ISBN and Open Library collector publication paths now merge that overlay after their ordinary records, preserving approved summaries and synopsis citations without upgrading edition verification or replacing other fields. This does not deploy a remote website.

A new receipt directory records exact backups, before/after hashes and transaction state. Ordinary write errors trigger restoration of files already written. Rollback first validates every target and backup and refuses to erase edits made after promotion. Multi-file writes are not an atomic filesystem transaction: abrupt process termination may leave a prepared receipt requiring inspection/recovery. Human reviewer labels are workflow attestations, not authenticated identities.

## Commands after explicit human review

First record actual human decisions and build a new staging package without `--preview-assistant`, using `review_decisions.py` and `stage_enrichment.py`. Do not relabel assistant decisions as human approvals. Review `preview.md` and `changes.diff` before promotion.

```powershell
python scripts/promote_enrichment.py --package STAGING_DIRECTORY --queue REVIEW_QUEUE_JSON --decisions HUMAN_DECISIONS_DIRECTORY --receipt NEW_RECEIPT_DIRECTORY
python scripts/promote_enrichment.py --rollback --receipt RECEIPT_DIRECTORY
```

Run from the project directory. The default project root comes from the script location; `--root` is available for temporary integration fixtures.

## Validation

Temporary-catalog integration checks exercise successful promotion, collector overlay persistence, exact rollback, withdrawn approval, changed live files, assistant-preview rejection, stale rollback rejection and simulated write failure. Fourteen staging/promotion test executions and four decision tests pass. Synthetic human approvals exist only inside temporary test fixtures. The real catalog remains unchanged and has no approved-synopsis overlay yet.

The existing four-proposal preview remains available at `data/local-ai-trials/staging-preview-20261030/preview.md`. Blade, Doom and Doctor Strange replace basic publisher snippets. Moon Knight replaces an existing editorial synopsis with a longer publisher excerpt; this is not clearly an improvement and should receive particular scrutiny. All four require explicit human review before staging for actual promotion.
