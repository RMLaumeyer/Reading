# Edition-first 4B pilot

## Fresh collection and registered reading lists (September 26)

The solo command now retrieves missing/fresh Google Books edition pages by ISBN,
validates the returned identity, and collects public Marvel reading lists. Registered
Absolute Carnage and Messiah Complex sources remove the need for per-issue URL plans
in those cases. Strict automatic year matching and search checkpoints address two
additional unattended-operation risks.

Fresh checks: five of six ISBN lookups succeeded; a 404 failed cleanly and later
books continued. Two reading lists yielded 31 and 13 issue cards; an unsupported
page format failed explicitly. Two automatically sourced Absolute Carnage editions
gained four and five publisher-list placements. No new named-story titles or complete
reading-path claims were established. 139 tests pass; 4,701 prior public/data files
are unchanged. Arbitrary discovery and catalog-wide completeness remain unproven.
See [the live assessment, confidence limits and reproduction command](../data/local-ai-trials/solo-v2-validation/assessment.md).

## Single-command solo draft workflow (September 25)

`scripts/solo_enrich.py` now connects ISBN intake, optional bounded Brave search,
issue fetching, local extraction and explicit review decisions. Search credentials
come only from `BRAVE_SEARCH_API_KEY`; none are configured here, so live discovery
remains unverified. A synthetic end-to-end test covers the discovery path.

Three live 4B drafts completed with zero stage errors and were correctly routed to
review; no unsupported stories or publication were produced. 125 targeted tests
pass, and 4,677 pre-existing public/data files are unchanged. This improves autonomous
draft operation, not the evidence for unattended publishing.
See [the solo workflow assessment and remaining gates](../data/local-ai-trials/solo-v1-validation/assessment.md).

## Issue-source acquisition (September 25)

`scripts/issue_fetch.py` now fetches selected issue URLs, saves source/provenance
records, extracts explicit matching issue-heading subtitles and optionally runs
4B on the resulting supplement. It records blocked downloads and accepts only
explicitly imported, URL-matched search snapshots as fallbacks.

The live Angela trial recovered one new draft chapter title and rejected a cover
variant label. Both direct downloads returned 403; the accepted title came from
an attributed search excerpt, not a successfully downloaded page. URL discovery
and series years still require curation. 117 tests and ten final checks pass;
4,654 pre-existing public/data files remain unchanged.
See [the fetch assessment and usage](../data/local-ai-trials/issue-fetch-v1-validation/assessment.md).

## Automatic source intake (September 25)

`scripts/edition_sources.py` now prepares multiple ISBNs directly from raw cached
publisher metadata, extracts explicit TOC rows, saves evidence packets and generates
research tasks for missing stories/identities. Optional `--model qwen3.5-4b` runs
inference sequentially. No enrichment answers or website writes are involved.

Eight editions were prepared; Marvels order was recovered automatically and seven
other TOCs remain visibly blocked for review. Three additional live drafts completed
without stage errors. The queue contains 55 tasks, including 38 issue-level story
requests. This uses existing caches; it does not yet fetch new issue pages.
109 targeted tests pass; 4,566 pre-existing public/data files are unchanged.
See [the intake assessment and usage](../data/local-ai-trials/source-intake-v1-validation/assessment.md).

## Latest validation: version 10 (September 25)

Marvels now has five sourced draft story labels linked to the edition's explicit
table-of-contents order. Indexed titles, printed order, chronology and overall
story completeness remain distinct. The #0 label is an editorial/index title
requiring review. The new TOC stage rejects ambiguous, duplicate and partial-issue
rows without discarding independent story work.

Version 9 exposed another title-formatting error; its failure is preserved.
Version 10 removes exact issue-heading prefixes while retaining the original model
output. All 11 live checks and 103 offline tests pass; all 4,549 pre-existing
public/data files are preserved. This remains curated development evidence rather
than a held-out accuracy result.
See [the versions 9–10 assessment](../data/local-ai-trials/edition-v9-validation/assessment.md).

## Earlier validation: version 8 (September 25)

Missing series years can now resolve from an exact bibliographic series label and
matching ISBN in the same source, with both evidence spans retained. Conflicting
years withhold resolution. On unchanged Marvels inputs, 4B now accepts the contained
story Monsters in issue #2; four issues still lack story mappings and reading order
remains unestablished. 95 tests pass, ten historical inventories replay unchanged,
and all 4,532 pre-existing public/data files are preserved. The initial unavailable
server attempt and successful retry are saved separately.
See [the version 8 assessment](../data/local-ai-trials/edition-v8-validation/assessment.md).

## Earlier validation: version 7 (September 25)

Named stories now have an independent extraction stage, with exact partial-story
scope and separately cited prelude relationships. Ben Reilly has all five supported
Humanity Agenda parts. Pools of Blood retains four parts and adds a reviewable
Annual D-story candidate, Prelude. A fresh Marvels edition correctly abstains on
story mapping while its series identity remains unresolved. Characters remain out
of scope; no website data was changed.

Version 6 exposed a title-footnote error despite completing all three drafts. Its
failure is preserved. Version 7 cleans only explicitly declared heading artifacts
and retains the original model title. 88 offline tests pass. These checks measure
extraction from curated evidence, not independently verified catalog accuracy.
See [the version 7 assessment](../data/local-ai-trials/edition-v7-validation/assessment.md)
and [the preserved version 6 failure](../data/local-ai-trials/edition-v6-validation/assessment.md).

## Earlier validation: version 5 (September 25)

Explicit arc-length headings now reveal missing trailing parts, and separate arcs
no longer imply a combined reading order. Numbered-arc completeness is distinct
from edition completeness. Invalid/conflicting supplement data fails visibly while
preserving independent work. 80 offline tests pass; two fresh 4B live checks preserve
Pools of Blood and recover three Ben Reilly arc mappings with explicit evidence gaps.
See [the version 5 assessment](../data/local-ai-trials/edition-v5-validation/assessment.md).

## Earlier validation: version 4

The ten-book development run completed 10/10 drafts with zero stage errors.
Contents were recovered for all eight non-conflicting books, including markerless
Spider-Man 2099 contents. The parser now separates conjunction-linked partial
entries correctly and retains five missing-year identities as unresolved.
Coverage reports expose unmapped issues, missing arc parts and partial-story gaps.
72 offline tests pass. Only Pools of Blood currently has supplementary evidence
for an arc sequence; complete shelf-wide reading order is not established.
See [the full assessment](../data/local-ai-trials/edition-v4-validation/assessment.md).
The earlier pilot results below are retained as history.

September 22, 2026. Working model: Qwen3.5-4B. Priority: complete edition contents and reading order, then summaries; character appearances are optional secondary work.

## Implemented

`scripts/edition_trial.py` is a separate development harness. The v18 scripts and their saved results remain unchanged. Nothing publishes to the website.

- Inventory records whole-issue ranges and partial material separately, retaining the source's portion label (such as D story). Unknown collecting entries remain in `unparsed`; edition conflicts withhold dependent inventory. The parser is deliberately limited, and its output never declares the edition complete.
- A curated supplement supplies short issue-level excerpts and explicit issue identities. 4B extracts named arcs, part numbers and source IDs. The program attaches original evidence and checks literal arc support, explicit part numbers, whole-issue membership and conflicting assignments. It sorts supported parts within each named arc; it does not infer cross-arc chronology.
- Contents, arc extraction and synopsis are independent. A failed model stage leaves the inventory available and does not prevent the synopsis stage. Characters and reviews are not requested in this pilot. Synopsis selection receives no character filter.
- New run names are mandatory; existing output folders cannot be overwritten. Inputs, code/prompt hashes, raw model responses, retries, errors and resulting drafts are saved outside served assets.

This is focused assisted extraction, not autonomous research or a complete catalog pipeline. Source IDs and issue identities in the supplement are manually curated; they are not model discoveries. All outputs remain drafts requiring semantic review. No score is claimed against independently adjudicated gold.

## Live results

| Run | Seconds | Outcome |
| --- | ---: | --- |
| edition-4b-pools-sourced-01 | 63.83 | Initial prototype failed exact quote checks because 4B changed curly quotation marks. Contents and synopsis survived. Preserved as a counterexample. |
| edition-4b-pools-sourced-02 | 26.33 | Source-ID evidence attachment recovered all four supported arc parts. |
| edition-4b-pools-control-02 | 3.66 | Same version, original packet without issue supplement: inventory and synopsis, no arc parts/order. The absence of issue evidence bypasses arc inference, so this is a missing-source control, not an accuracy comparison. |
| edition-4b-pools-sourced-03 | 13.53 | Final version: four supported parts, partial Annual material retained, no stage errors. |
| edition-4b-ben-03 | 5.69 | Final version: Ben Reilly #1–5 and a supported mystery/Ravencroft synopsis; no character-stage blockage. No invented reading guidance. |

Times are descriptive. These are shorter tasks with different sources, potentially warm caches and unchanged user-loaded parallel setting 4; they are not controlled speed comparisons against v18 or 9B. One request runs at a time. No model settings were changed for this pilot.

The supported Pools of Blood sequence is:

1. Deadpool (2024) #11 — part 1 ([Marvel](https://www.marvel.com/comics/issue/122785/deadpool_2024_11)).
2. Miles Morales: Spider-Man (2022) #30 — part 2 ([Marvel issue variant page](https://www.marvel.com/comics/issue/125841/miles_morales_spider-man_2022_30_variant/variant)).
3. Deadpool (2024) #12 — part 3 ([Marvel](https://www.marvel.com/comics/issue/122786/deadpool_2024_12)).
4. Miles Morales: Spider-Man (2022) #31 — part 4 ([publisher solicitation, printed page 61](https://prhcomics.com/wp-content/uploads/2024/12/PREVIEWS2021040_March_2025_FINAL.pdf)).

The edition also includes the D story from Miles Morales: Spider-Man Annual (2024) #1, confirmed by the cached packet and the [ISBN-matched distributor listing](https://www.penguinrandomhouse.com/books/788671/miles-morales-spider-mandeadpool---pools-of-blood-by-cody-ziglar/). Its title, relationship to the crossover and placement remain unresolved. It is retained as partial material, not expanded to the whole Annual or silently inserted into the order. Consequently `complete` remains false for both inventory and edition reading order.

Source provenance: the issue excerpts came from primary-source search-index snapshots; direct Marvel page requests returned 403. This is explicitly recorded in the supplement. Full-page caches and independent issue/edition adjudication are still needed for a held-out benchmark.

## Validation and remaining work

66 offline tests pass (56 existing, 10 new). New coverage includes partial-story retention, unparsed contents, conflict abstention, invented arc/part rejection, whole-versus-partial issue mapping, duplicate-part conflicts, Unicode evidence preservation, isolated model failures, collecting-sentence boundaries and avoiding false completeness from a gapless prefix.

A deterministic replay across all ten cached packets finds inventory entries for seven books and partial material for two. Both known edition conflicts remain withheld. The markerless Spider-Man 2099 contents still need handling; missing-year/ambiguous entries remain unparsed. This replay is not a ten-book live accuracy benchmark. It caught a sentence-boundary defect in the initial prototype, fixed in version 3 and covered by a test; earlier script snapshots and replay output are retained.

Before/after hashes checked 4,404 pre-existing data/public files with zero changes. Historical results are preserved. The v18 script and quality helper were not edited.

Next development targets are evidence discovery for further editions, story titles and scope for partial material, explicit arc boundaries and prerequisites, and markerless/ambiguous contents. Then evaluate on the independent reading-path holdout specified in `enrichment-reassessment-2026-09-22.md`. Do not mistake success on this familiar book for catalog-wide accuracy or complete story coverage.

## Running an isolated draft

From `comic-shelf`, with the local model/server available, use an available Python interpreter:

```powershell
python scripts/edition_trial.py --packet data/local-ai-trials/trial-18-full/9781302964924-sources.json --supplement data/local-ai-trials/edition-pilot-20260922/pools-issue-evidence.json --model qwen3.5-4b --name NEW-UNIQUE-NAME
```

Omit `--supplement` to test missing issue evidence. The harness never reads existing website annotations as answers and never writes website data. `complete: false` is intentional until broader source coverage and human review establish completeness.
