# Explicit synopsis-only record initialization

Normal synopsis staging still excludes missing enrichment records. When a uniquely matched catalog ISBN has completed source and edition review, `stage_enrichment.py --initialize-isbn ISBN` permits a minimal record for that ISBN. The option can be repeated. It does not clear review flags, waive citations or permit ambiguous catalog matches.

The initialized record includes the reviewed synopsis, review provenance and cited sources. It has the site's required display fields, with pages unknown and appearances, stories, issues and reading order unindexed. It does not copy metadata from a different edition or infer those fields from the synopsis.

The staging manifest records the explicit ISBN list and represents the missing prior record as `before: null`. Promotion rebuilds the package using that same list, checks the resulting payload and change entries, and writes exact backups through the existing transaction. Default staging and the explicit initialization package should be reviewed separately; do not hand-create a base record to evade a missing-record exclusion.

Canonical approved patches retain an `initializeMissing` marker. `approved_synopses.apply` uses it to restore a reviewed minimal record when a collector rebuild lacks that ID. If the collector supplies a record, approved summary/review fields and citations merge into it without replacing its other metadata. Later synopsis updates preserve the marker. The marker is promotion-owned provenance, not a substitute for review.

The November 3 implementation was validated with default rejection, explicit initialization, unresolved flags, ambiguous identity, stale/tampered staging, injected write failure, rebuild persistence, later revision and exact rollback. All 385 Python tests and 18 catalog tests passed. The first local use was the reviewed Atlantis Rising synopsis; no remote deployment occurred.
