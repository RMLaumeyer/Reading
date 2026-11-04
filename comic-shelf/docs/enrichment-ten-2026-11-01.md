# Ten-edition Qwen enrichment batch — November 1, 2026

Ran ten new ISBN editions through the original single-pass Qwen selector and published four reviewed synopses locally. The approved overlay now contains 127 editions. One published synopsis is an unchanged Qwen selection; three are explicit source-backed Codex revisions. Six editions remain held for source/edition research.

All ten cases completed without worker failures using ten model requests in 58.18 worker seconds, excluding research and review. All 25 selected evidence quotes are literal source text. The existing seeded sampler excluded prior packets, and verification also found no ISBN overlap with prior run manifests. Sentence mode and the original prompt remain the defaults; blocks, rewriting and the extra audit pass were not used.

## Published

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9780785178903 | X-23: Target X | Revised to remove reader-addressed questions and promotional framing while preserving the prospective Wolverine confrontation |
| 9781302525729 | Star Wars: Bounty Hunters — Bedlam on Bestine | Unchanged Qwen selection covering the Crimson Dawn/Empire job, Valance's mission and T'onga's threatened team |
| 9781302532796 | Daredevil: The Devil in Cell-Block D | Revised to restore imprisonment, the Foggy investigation and the other-Daredevil mystery |
| 9781302482510 | Jessica Jones: Alias Vol. 2 | Revised to introduce Jessica by full name and restore the distinct Ant-Man date thread |

The Bounty Hunters synopsis is a limited overview and omits the Zuckuss thread; it makes no exhaustive coverage claim. The revisions do not identify Ant-Man from memory, add an X-23/Wolverine relationship explanation, resolve Foggy's story or invent a successful rescue, solved mystery or victory.

## Held

| ISBN | Edition | Main blocker |
| --- | --- | --- |
| 9781302507602 | Hunt for Wolverine: Weapon Lost | Source additionally collects Hunt for Wolverine #1 beyond the catalog title range; preserve contents conflict |
| 9781302485696 | New Avengers: A.I.M. — Everything Is New | Avengers #0 contributes a named partial story but lacks an original series year; provisional New Avengers identity also remains |
| 9781302531195 | Daredevil: Born Again | Source includes Daredevil #219 beyond the catalog title's #226–233 range |
| 9781302493998 | Agents of Atlas: Dark Reign | Unnumbered/undated extras and partial material remain unresolved |
| 9781302535186 | Hawkeye: Marked for Death | Unspecified partial material from Marvel Comics Presents #83 |
| 9781302521219 | Avengers: Live Kree or Die | Unspecified partial material from Avengers #364 and #366 |

Four original drafts passed editorial review unchanged: Bounty Hunters, Born Again, Agents of Atlas and Hawkeye. Three of those still failed edition eligibility, so only one was published unchanged. Six original drafts needed editorial revision or context work; three were revised for publication and the others remain held. Mild publisher enthusiasm was allowed in otherwise coherent drafts, consistent with the preceding review standard. These are Codex development assessments under user authorization, not independent gold labels or a general accuracy estimate.

## X-23 identity assessment

The original exact-ISBN source identifies X-23: Target X's issue run as starting in 2006. Two independently downloaded distributor records match the ISBN and #1–6 contents but label the category X-23: Target X (2007); their descriptions differ, so aggregate reconciliation correctly remained failed.

The publisher distinguishes the original [X-23: Target X (2006) issue context](https://www.marvel.com/comics/discover/598/x-23) and [2006–2007 run listing](https://www.marvel.com/comics/series) from the [2007 collection node](https://www.marvel.com/comics/series/2693/x-23_target_x_2007). The [collection page](https://www.marvel.com/comics/collection/16200/x-23_target_x_trade_paperback) is dated August 22, 2007 and collects #1–6 with matching plot copy. Manual assessment used the original-run metadata for the 2006 namespace rather than treating the distributor category date as an original issue year. Both conflicting labels and the failed aggregate audit remain preserved.

The publisher references are short metadata excerpts returned by web search, not cached full-page publisher downloads. They establish the run/collection distinction, not independent target-ISBN identity. Target membership and plot remain grounded in the original exact-ISBN description and the matching distributor records. This resolution is specific to this synopsis review; no global year alias, catalog-range rewrite or issue-key change was made.

## Verification and recovery

All 18 catalog tests passed. Production worker code did not change; the preceding 355-test Python validation was not repeated for this data-only batch. All 78 frozen Python code files, input/cache/prompt hashes, literal citations, review queue/decision inputs and manual-resolution evidence hashes passed verification.

Only four intended book records changed, limited to summary, synopsis provenance and source fields. Other records, issue inventories, borrowing availability and reading-order information were preserved. Exact promotion backups and production hashes passed. The local server was initially offline; after restarting the existing scripts/serve.mjs server on its configured loopback port, localhost:5173/enrichment.json matched the exact staged payload. No remote deployment occurred.

The final X-23 decision supersedes an earlier unpromoted wording draft; its immutable event and initial staging directory remain preserved. The actual publication uses approved-staging-final. No previously approved synopsis was overwritten.

Artifacts are in data/local-ai-trials/enrichment-ten-20261101: manifest/packets/frozen-code, source-review.json, original model results, source acquisition audits and records, x23-publisher-reference.json, resolved-review-queue.json, immutable decisions, approved-staging-final, publish-receipt and verification.json. new-held.json contains six new holds; known-held.json combines them with the preceding 146-edition remainder for 152 known held editions. It is a reviewed backlog, not a count of every unenriched book in the catalog.

Continue using Qwen as a bounded first-draft selector. Track unchanged editorial passes separately from source eligibility, corrected publications and model latency. Preserve the contents conflicts and partial-material holds until their evidence is resolved.
