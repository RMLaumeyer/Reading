# Automatic enrichment

Open Panel using **Start Panel.cmd**, then choose **Enrich remaining books**.

The collector processes saved publisher descriptions first, then tries exact ISBN matches in Google Books and Open Library for missing editions. It uses free public sources, waits between requests, saves results locally, and pauses when a source requests a traffic check or returns an access/rate-limit error. No accounts, paid APIs, or AI services are required.

You can close the browser tab while collection runs. Keep the computer awake. After shutting down or an interruption, relaunch Panel and choose Resume enrichment. Retry lookup errors reattempts failures; completed records are reused. Only one collector can write the catalog at a time, including the older command-file collectors.

**Needs review** lists missing metadata, review scores, uncertain collected issues, and story/character checks. Open a book to inspect suggestions and linked sources. A completed automatic pass does not mean every field is verified.

Automatic character mentions appear in broad character searches. The sourced-appearances filter still uses checked entries only. Numbered-volume and issue-range suggestions do not change verified reading paths or overlap matching. Possible review matches are based on known reviewed issue sets and remain suggestions until the edition is confirmed. The collector does not invent story summaries or ratings, and does not perform broad review-site searching. New or ambiguous review sources still require research.

Previously checked editorial details are preserved. Checkpoints live in `data/auto-enrichment-state.json`; generated metadata also lives in `data/automatic-enrichment.json`. `auto-enrichment.log` records worker progress and unexpected errors. Keep the project folder to retain saved work.
