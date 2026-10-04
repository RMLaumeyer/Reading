# Two-source reading-order collection — 2026-09-29

A single command now fetches the registered guides for an event, extracts their
sequences, maps each to saved edition drafts, and reports scope/order differences.
It writes isolated evidence and review results; it cannot publish website data.

```powershell
python scripts/order_research.py --event annihilation --edition-run data/local-ai-trials/evidence-v3-annihilation-three --name YOUR_UNIQUE_RUN_NAME
```

## Live result

The final run acquired both registered sources successfully:
[Marvel Guides](https://marvelguides.com/annihilation-reading-order), using the
previously selected Road to Annihilation and Annihilation sections, and
[Comic Book Reading Orders](https://comicbookreadingorders.com/marvel/events/annihilation-reading-order/),
using its full Single Issues tab.

| Check | Result |
| --- | --- |
| Sources acquired | 2/2 |
| Issues shared by the selected source scopes | 29 |
| Reversed relative-order pairs among shared issues | 0 |
| Issues listed only by the second source | 4 |
| Final decision | Review required: different scope |

The four additional source entries are What If: Annihilation Reached Earth? #1
(2008) and Nova Vol. 4 #1–3 (2007). They remain source-only additions, not required
prerequisites or additions to owned-edition contents. Volume labels are retained;
the collector does not silently equate Nova Vol. 4 with another Nova identity.
The existing prologue membership gap is not resolved by guide agreement.

Both are editorial guides. Agreement neither proves that their research is
independent nor establishes exhaustive story coverage or mandatory reading.
Comparing relative order on shared issues avoids mistaking extra issues for
contradictions. Actual inversions retain the conflicting issue pairs; sources
with parsing problems cannot yield a clean agreement claim. No merged order is
automatically selected.

## Collection behavior

`cbro_order.py` identifies the Single Issues panel via its labeled tab, ignoring
the separate collected-editions panel, navigation and scripts. It retains the
listed order and explicit issue numbers. An undated issue can use a unique year
attached to the exact same series elsewhere within that tab; the dated quote is
retained and the inference requires review. Conflicting years block acceptance.
Years never transfer between different series or from another page.

`order_research.py` supplies registered URLs and scope, acquires each source once,
saves raw pages and hashes, maps editions, and compares results. One unavailable
source remains a recorded failure and cannot become false agreement. A separate
research candidate, CMRO, returned HTTP 403 through browsing and was not adopted
or bypassed.

This is unattended collection from a manually maintained source registry. Only
Annihilation is registered so far. It is not broad web discovery or a claim of
complete unaided enrichment. Existing edition results are read-only inputs;
model settings and the story extractor are unchanged.

## Broader check and validation

A new-page structural check on the same site's Annihilation: Conquest guide
initially accepted 19 rows and flagged 14. Exact-series year reuse across
paragraphs increased this to 23 accepted rows and 10 unresolved rows in a saved
source replay. Remaining rows include a recap annotation and Nova issues with
no supported year in that tab. They stay visible as problems. This page became
a development case when used to adjust the parser; it has no independent gold
labels and is not an accuracy benchmark.

223 tests pass. Cases cover source/tab isolation, conflicting years, unsupported
numbers, duplicates, no shared issues, added-issue scope differences, inversions,
source problems and punctuation-only identity normalization.

Final artifacts: `data/local-ai-trials/order-comparison-v2-annihilation`, including
`report.json`, per-source raw HTML, parsed paths, edition maps and a manifest.
The preceding v1 run is preserved. Validation artifacts are in
`order-comparison-v1-validation`, including both Conquest outputs and `checks.json`.
All 5,560 pre-existing public/data files, input edition hashes and final-run code
hashes were unchanged. Website data remains untouched.

Next priorities: establish a fresh event benchmark with independently checked
scope/order labels, add bounded discovery of suitable sources, and resolve the
remaining identity and annotated-row cases without hiding uncertainty.
