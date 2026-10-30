# Event acquisition and decimal reading-order mapping

2026-10-08. Reading order and contained/featured stories remain the priorities.
Character extraction remains disabled. Website data and previous results are
preserved, and all generated outputs remain research drafts.

## What now runs unattended

```text
python scripts/enrich_event.py --event original-sin --name UNIQUE_NAME --max-editions 8 --max-identity-pages 6
```

This command selects up to eight matching catalog title candidates, downloads
edition evidence, runs the configured local model, discovers public reading-guide
pages and compares their sequences. It requires an event slug and a unique run
name. It does not require manually entered ISBNs or guide URLs. Selection retains
omitted candidates and does not infer edition contents or complete event scope
from titles. Default model: the existing Qwen3.5-4B endpoint.

Identity discovery uses one shared ISBN lookup budget. Up to two slots may be
reserved for event decimal evidence, so integer lookups cannot consume every
slot. Distributor discovery adds bounded requests per ISBN. The workflow does
not enable Brave search or change model hardware settings. Empty selections,
existing run names and failed subprocess stages stop or report incomplete work.

The first smoke run, `original-sin-unattended-v1`, stopped because the edition
CLI rejects a zero query budget even when search is disabled. Its results remain
saved. The replacement uses the accepted minimum budget with search disabled.

## Decimal identity and edition placement

Reconciled explicit equivalent numbering now produces decimal draft inventory
entries and issue nodes with exact string designators. `3.1` and `3.10` remain
distinct; neither becomes a floating-point number or an integer-range member.

The saved collecting evidence explicitly equates Hulk vs. Iron Man #1–4 with
Original Sin #3.1–3.4. The parser requires the catalog range, exact ISBN evidence,
stated alias and a second matching collecting statement to agree. It keeps the
global contents conflict and identity review visible. It does not assign the
primary alias a series year. Instead, a matching yearless primary source issue
can map to the stated decimal identity, with the original source issue retained.

Conflicting canonical identities, duplicate issues, unstated aliases, explicit
primary years, different suffixes and disagreement among supplied collecting
statements do not qualify. Decimal inventory outside a source remains listed
separately without any event-membership or reading-requirement inference.

## Results and limits

| Trial | CBRO identities | Marvel Guides identities | Interpretation |
| --- | --- | --- | --- |
| Previous three-edition Original Sin run | 22 | 33 | Operational baseline |
| Typed decimal/alias run | 26 | 37 | Four supported decimal draft identities added per source |
| Unattended seven-edition run | 26 | 50 | More supplied edition evidence; operational coverage expansion |

The unattended run `original-sin-unattended-v2` completed seven selected editions
with zero model stage errors. It recovered 31 integer inventory units and five
edition-level story highlights. No issue-level named stories were recovered.
These counts are not independently adjudicated accuracy scores or exhaustive
story inventories.

The two paths retain 67 and 141 source positions in different scopes. The final
run leaves 41 and 91 source positions unresolved. Each has four decimal draft
placements; all placements still require identity review or remain uncovered.
There are zero fully verified whole-issue placements.

Canonical alias resolution increased shared identities from nine to thirteen,
revealing four order inversions: CBRO places #3.1–3.4 before Original Sin #3,
while Marvel Guides places that block after #3. All four disagreements enter the
research queue with original source quotes, positions and issues. The collector
does not choose an order or merge the recommendations.

Bounded decimal discovery automatically found the catalog's Thor & Loki edition.
The retrieved source lists its standalone #1–5 but supplies no verified decimal
alias, and distributor evidence was unavailable. It therefore does not establish
#5.1–5.5 membership. Publisher search results point to relevant Marvel pages,
but direct retrieval returned HTTP 403. Search snippets were not imported as
accepted collector evidence.

270 tests pass. New live Annihilation regression runs retain the original 29/33
sequences. The audit preserves all 6,211 files in the pre-run public/data snapshot.
The principal evidence artifacts are:

- `data/local-ai-trials/typed-decimal-v2-validation/checks.json`
- `data/local-ai-trials/original-sin-unattended-v2/checks-corrected.json`
- `data/local-ai-trials/original-sin-unattended-v2-orders/research-tasks.json`

The original `checks.json` remains preserved; its highlight counter read the
wrong result field. `checks-corrected.json` uses `featuredStoryHighlights` and
records the correct count of five. Other audit findings remain unchanged.

## Next accuracy work

Unattended acquisition is now exercised end to end, but reliable unaided
enrichment is still unproven. Resolve source ordering conflicts with explicit
sequence evidence, acquire verifiable decimal aliases and years for outstanding
nodes, and validate new events against independently adjudicated frozen labels.
Contained/featured stories also need fresh issue-level evidence and accuracy
validation before completeness can be claimed.
