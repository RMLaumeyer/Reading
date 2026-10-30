# Synopsis staging publisher

`scripts/stage_enrichment.py` creates a new isolated package containing `preview.md`, a record-level `changes.diff`, the complete `enrichment.staged.json`, an exact `enrichment.before.json` rollback snapshot and a manifest with source/decision hashes. It never writes live or served files. Only approved synopsis text, synopsis provenance and additional source links change; edition data, reading order and unrelated records are preserved.

Default gates require a human accept/revise decision, a unique catalog ISBN mapping, an existing enrichment record and exact source citations. All unresolved review reasons block staging, except a short-synopsis flag after explicit revision. Human approval of a synopsis never silently resolves contents/identity flags. A missing review decision does not stage a book.

`--preview-assistant` produces an explicitly marked preview of assistant decisions. It does not authorize publication. The initial preview (`data/local-ai-trials/staging-preview-20261030`) contains Blade, Moon Knight, Doom and the corrected Doctor Strange synopsis. Star-Lord & Kitty Pryde remains blocked for missing inventory. Five editions remain unreviewed. The normal gate check (`staging-gate-check-20261030`) stages zero records because all current decisions are assistant assessments.

Four staging tests and four review-decision tests pass. Tests cover approval/preview gates, conflict blocking, field preservation and exact backup/live preservation. The real enrichment file and rollback snapshot hashes match. This completes staging-package creation, not live deployment or rendered application verification. There is no promotion command yet; a live promotion must revalidate source/decision hashes, handle the catalog's canonical enrichment inputs so subsequent collectors do not erase changes, and support guarded rollback.

## Command

```powershell
python scripts/stage_enrichment.py --queue REVIEW_QUEUE_JSON --decisions DECISION_DIRECTORY --catalog public/catalog.json --enrichment public/enrichment.json --output NEW_PACKAGE_DIRECTORY
```

Use `--preview-assistant` only to inspect assistant-assessed proposals. The package requires a new output directory, so earlier staging packages are preserved.

## Qwen settings

No new UI settings are required for this staging step; it performs no inference. The worker already sends `reasoning_effort: none`, temperature 0, structured JSON schema and a 200-token output cap for excerpt-ID selection. It processes requests sequentially. Keep the previously tested model/context configuration while evaluating these workflow changes; the historical context was 8192, but the current runtime context was not re-inspected. No model/runtime settings were changed here.
