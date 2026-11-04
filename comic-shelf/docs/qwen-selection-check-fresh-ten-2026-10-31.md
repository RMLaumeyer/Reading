# Fresh validation of Qwen selection checks — October 31, 2026

Ran ten previously unused ISBN editions through the original Qwen selector with the new review checks enabled. Six reviewed synopses were published locally, bringing the approved overlay to 123 editions: three unchanged model drafts and three explicit Codex revisions. Four editions remain held.

All ten cases completed without worker failures, using ten model requests in 69.34 worker seconds, excluding research and review. All 26 selected evidence quotes are literal source text. The cases were selected by the existing seeded sampler from unused cached Google Books editions, excluding prior packets. Verification also compared the selected ISBNs with prior run manifests and found no overlap. This is a new development cohort after the checks were frozen, not an independently adjudicated test set.

## Editorial quality and publication

| ISBN | Edition | Original draft assessment | Publication |
| --- | --- | --- | --- |
| 9781302510756 | Shuri: The Search for Black Panther | Needs revision: damaged proper name/contractions and incomplete search setup | Published source-backed revision |
| 9781302506575 | Hunt for Wolverine | Needs revision: context-dependent questions | Held: no usable inventory |
| 9781302533366 | Laura Kinney: Wolverine — One-Mutant Army | Pass unchanged; central mission and threat are explicit | Published unchanged |
| 9781302941796 | Miles Morales: Beyond | Needs revision: damaged text and omitted distinct thread | Held: partial annual material |
| 9781302510404 | Annihilation: Complete Collection Vol. 2 | Pass unchanged; cosmic war and Ronan threads are clear | Held: unresolved undated/unnumbered contents |
| 9781302533458 | Kanan: The Last Padawan | Needs revision/research: damaged character identity | Held: unresolved inventory and plot identity |
| 9781302510626 | Star Wars: The Escape | Pass unchanged; pursuit, stranded-world stakes and named rebels | Published unchanged |
| 9781302499716 | Star Wars: Darth Maul | Needs revision: question-only selection and broken source token | Published source-backed revision |
| 9781302938031 | King in Black: Return of the Valkyries | Needs revision: introduce Jane Foster and preserve further Valkyrie context | Published source-backed revision |
| 9781302936099 | Doctor Doom: Bedford Falls | Pass unchanged; Doom/Kang mission and black-hole threat | Published unchanged |

Four of ten original drafts passed editorial review unchanged. One of those four remains blocked by edition evidence; six drafts needed revision or research. Publication counts therefore differ from editorial quality counts. Accepted synopses do not claim exhaustive subplot coverage: Laura's Bucky subplot and Doom's alternate-Earth details remain omitted. Codex assessed these drafts under the user's delegated publication authorization; this is not independent human gold data.

## What the new checks did

The question-only check flagged Darth Maul's selected question. Explicit source-backed revision added the named protagonist and setup, avoided the damaged token, and preserved uncertainty about the Padawan and bounty hunters. The original warning remains in the raw run; its resolution is recorded specifically as requiring revision. The original selection was not approved unchanged.

No other draft triggered the three new checks. Manual assessment still found damaged proper names and contractions outside the narrow negative-contraction pattern, missing context, omitted threads and the Kanan identity problem. The checks caught one of the six drafts requiring further editorial work and did not flag the four editorial passes in this small sample. Those are descriptive counts, not reliable sensitivity or false-positive estimates. The five unflagged problem drafts show why an empty warning list cannot justify autonomous publication.

The original selection prompt, model configuration and source eligibility were unchanged. No code or warning rules were tuned after seeing this cohort, and no inference was rerun to improve the observed rate. The checks add review holds and context; they do not improve the model's selected prose or independently verify semantic entailment.

## Edition/source review

Shuri's aggregate distributor lookup failed because its two exact-ISBN records label the series Shuri (2018) and Shuri (2018-2019). Their plot descriptions and #1–5 ranges are identical. Manual review corroborated the original 2018 start year, preserved both labels and the failed aggregate audit, and used an intact record to repair the synopsis's punctuation and name. No global year normalization was added.

Laura Kinney's distributor lookup failed. The publisher's [Laura Kinney: Wolverine (2024) #1 metadata](https://www.marvel.com/comics/issue/120402/read), returned by web search, independently corroborates the original source's series/start year. That indexed excerpt is a namespace reference only; it does not establish target ISBN, membership or plot. Those remain grounded in the original exact-ISBN source.

Darth Maul's accepted exact-ISBN distributor record corroborates the original 2017 year and #1–5 membership. Both sources retain the damaged word in the Padawan question; the revision avoids reproducing it and does not infer the Padawan's name or the bounty hunters' allegiance.

Hunt for Wolverine's malformed collecting marker and multi-series list remain unresolved. Miles Morales's annual contribution remains unspecified partial material. Annihilation includes undated series and an unnumbered Nova Corps Files entry. Kanan's source calls the character Caleb Dune, while the publisher's [Kanan issue #2 metadata](https://www.marvel.com/comics/issue/52010/kanan_2015_2) names Caleb Dume. That discrepancy is an additional research hold; no silent correction or issue expansion was published.

## Verification and artifacts

All 18 catalog tests passed. The unchanged production worker code had already passed the 348-test Python suite in the preceding checks change; that suite was not repeated for this data-only run. All 77 frozen Python code hashes, packet/cache hashes, actual prompt hashes, literal citations and manual-resolution source hashes passed verification.

Only six intended book records changed, limited to summary, synopsis provenance and source fields. Other fields and records were preserved. Exact backups and final hashes chain to the preceding five-edition publication. The local site serves the exact staged payload. No remote deployment occurred.

Artifacts are in data/local-ai-trials/selection-check-fresh-ten-20261031: the frozen manifest/packets/code, source-review snapshot, original model results and review queue, acquisition audits, resolved-review-queue.json, immutable decisions, approved-staging, publish-receipt and verification.json. The four held cases are recorded in new-held.json; known-held.json combines them with the preceding 142-edition remainder. These four are new editions, not recoveries from the original 166-edition held baseline.

Next, keep this cohort fixed for future comparisons and assess source preparation improvements separately from model quality. The observed review misses support further context work, while the previous prompt/rewrite trials still argue against assuming that a longer prompt or free-form rewrite will improve Qwen's reliability.
