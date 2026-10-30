# Reading-order discovery and remaining accuracy gaps

Recorded 2026-10-08. Reading order and contained/featured stories remain the
priorities; character extraction remains disabled. All outputs are research
drafts. Website data and historical trial results are preserved.

## Discovery and evidence improvements

The collector can discover exact event pages through the public Comic Book
Reading Orders event index and Marvel Guides sitemap. This removes manual page
registration for events present in those indexes. It does not establish general
web coverage. Selection requires an exact event match and allowed source URL.
Ambiguous matches and failed requests remain recorded failures.

Discovered Marvel Guides pages use all explicit reading-list sections, with the
full-page selection mode recorded. A registered event may retain its previously
selected scope. Neither mode establishes mandatory reading or chronology.

Optional catalog research selects at most six ISBN pages by default, with a
twelve-page maximum. Candidate titles select pages to inspect; they do not prove
contents. Evidence requires matching ISBN, consistent contents, explicit dated
inventory and an event-context mention. The latter only screens context. Foreign
edition evidence can propose identity, but cannot add membership to an owned
edition. Removing a volume suffix is permitted for candidate lookup only;
accepting an alias still requires evidence.

An audit now flags overlapping issue ranges with the same series label and
different years. The Black Vortex inputs produce one warning. This exposes a
conflict without choosing a year or proving either edition wrong. Affected
entries cannot supply verified edition placement.

## Measured results

| Case | Result | Meaning |
| --- | --- | --- |
| Black Vortex, Marvel Guides | 8/13 identities; 6/12 adjacent pairs | Development replay against provisional reference |
| Black Vortex, CBRO | 8/13 identities; 4/12 adjacent pairs | Development replay against provisional reference |
| Annihilation | 29 and 33 source positions retained | Sequence regression controls unchanged |
| Original Sin, CBRO | 67 positions; 22 resolved identities | Operational smoke, no adjudicated accuracy score |
| Original Sin, Marvel Guides | 141 positions; 33 resolved identities | Full-page scope differs; positions include unsupported text |

Black Vortex improves from seven identities per source in the previous development
replay, and two in the original frozen run. Five positions per source remain
unresolved. Each mapping has seven placements requiring identity review, one
uncovered resolved issue and zero fully verified placements. The two source
sequences are not merged. Existing provisional labels are not an independent
human accuracy benchmark.

Original Sin was acquired without registered event URLs. The first layout failure
remains saved; a document-title validation fix allowed both pages to parse in a
new run. Decimal numbering and series aliases remain substantial gaps.

## Decimal issue capture

The latest saved-source replay preserves decimal issue designations as strings,
including the distinction between `3.1` and `3.10`. It captures nine positions in
the CBRO Original Sin page and one in Marvel Guides. These slots remain
unsupported with no accepted issue identity or edition membership. Ranges,
annotations and contradictory years are not guessed. All six replayed source
sequences retain their prior resolved nodes and position counts.

252 tests pass. The preservation audit checks 5,651 pre-existing public/data
files and finds no changes. Historical results remain intact. New validation:
`data/local-ai-trials/decimal-designators-v1-validation/checks.json`.
Earlier discovery and accuracy evidence:
`data/local-ai-trials/order-evidence-v2-validation/final-checks.json`.

## Use and next work

Given an existing saved edition trial, discover and compare event guides with:

```text
python scripts/order_research.py --event EVENT_SLUG --edition-run SAVED_RUN --discover-guides --discover-identities --max-identity-pages 6 --name UNIQUE_NAME
```

The next accuracy work is evidence-backed decimal membership and series alias
resolution, followed by new frozen events and independent human adjudication.
Contained/featured story accuracy also needs a fresh benchmark; this work has
not demonstrated a new story accuracy gain. Unaided enrichment remains unproven,
particularly complete reading order and verified coverage of owned editions.
