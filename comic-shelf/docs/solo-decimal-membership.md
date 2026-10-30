# Automatic decimal issue membership candidates

2026-10-08. The reading-order collector now links unsupported decimal issue
positions to explicit alias evidence in saved edition packets. This addresses
an actual Original Sin gap without editing previous trial results or website data.

The parser requires source-specific matching ISBN identifiers, an explicit
collecting statement with `aka`, equal-length integer and decimal ranges, and a
dated series label matching the decimal series. It retains designators as strings
and rejects leading-zero suffix normalization, mismatched counts and unsupported
statement formats. Publication year is not substituted for series year.

The live run `original-sin-decimal-membership-v1` acquired both guides using public
indexes without registered event URLs. Its `decimal-membership.json` linked four
positions, Original Sin #3.1–3.4, to the edition's explicit Hulk vs. Iron Man #1–4
alias statement. Six other decimal positions lacked matching evidence. Each
candidate retains the source quote, URL, ISBN evidence and the existing contents
conflict. No conflict is cleared and no candidate becomes an accepted issue.

The two guides retain their previous 22 and 33 resolved identities across 67 and
141 source positions. Different scopes remain separate. This is a development
evidence-matching result, not a human-adjudicated accuracy benchmark.

255 tests pass. The new live-run audit verifies input and production code hashes,
unchanged resolved sequences and preservation of 5,651 pre-existing public/data
files. Saved results remain unchanged.

The next step is to reconcile the explicitly stated equivalent numbering with
the inventory conflict rules, then support a typed decimal issue identity through
mapping and comparison. That requires new negative cases before accepting
membership. Complete reading order and contained/featured stories remain the
priorities; unaided enrichment is still unproven.

## Scoped numbering reconciliation

A second live run, `original-sin-decimal-reconciliation-v1`, adds a strict
reconciliation check. The catalog title and integer range must match the alias,
and every supplied source must agree with the explicit decimal range. The
alias statement alone is insufficient. A separate ISBN-matched collecting
statement is required. Additional collecting claims, mismatched ISBNs, conflicting
ranges, unsupported source text or repeated source identifiers veto reconciliation.

All four #3.1–3.4 candidates pass this scoped check automatically. The report
records `equivalent_numbering_supported` and retains both collecting quotes.
The global edition conflict stays visible: this check explains the numbering
equivalence without establishing that all edition metadata is correct. Decimal
identities still require review and are not inserted into the integer inventory
or compared as floating-point values. Accepted reading-order identity counts
remain 22 and 33, and six decimal positions still lack matching evidence.

258 tests pass, including wrong ISBN, unequal ranges, extra-source disagreement,
missing corroboration, catalog mismatch and additional collecting-claim cases.
The new run's `checks.json` verifies code/input hashes, previous resolved
sequences and preservation of 5,651 pre-existing public/data files. The result
is evidence reconciliation on a development case; unaided accuracy has not
been established. A general decimal identity representation and mapping remain
the next implementation requirement before these candidates can be accepted.
