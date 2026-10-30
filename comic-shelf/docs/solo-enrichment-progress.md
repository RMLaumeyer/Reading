# Autonomous collection progress — September 26, 2026

Later iteration: [publisher story evidence and stricter year-conflict handling](solo-featured-evidence.md).

Later iteration: [cross-edition reading paths and broader source-gap checks](solo-collection-paths.md).

Latest iteration: [automatic edition fallback and cited story highlights](solo-edition-fallback.md).

The collector now covers four registered Marvel events and exposes issue-level
coverage gaps. It remains a draft collector, not an independently validated source
of complete reading orders or featured stories. Characters remain lower priority.

## This iteration

- Added registered publisher sources for Civil War and Secret Invasion. Both live
  pages supplied 98 issue cards. Source selection excludes Civil War II; mappings
  still require exact series, year and issue number. Automatic selection now obeys
  the same three-source batch limit as explicitly supplied URLs.
- Added separate counts for inventoried whole issues, issues with story evidence,
  issues with publisher-list positions, partial entries and unresolved contents.
  Multiple lists cannot inflate unique issue coverage. Lists needing review do
  not contribute to accepted position coverage.
- Added explicit reporting of same-title/number, different-year candidates.
  These remain unmerged. Bibliographic year resolution now has its own review
  blocker: a Google Books series label is not sufficient independent validation.
- Edition parser v11 accepts explicit dated disjoint ranges such as
  `Fantastic Four (1961) #300 & #357-358`. It retains the full source quote, gaps
  and partial-material scope. Unsupported qualifiers and malformed ranges remain
  withheld. This recovered three previously unparsed issues in the live example.

## Final live check

Fresh Google Books metadata, automatically selected publisher lists, Qwen3.5-4B,
no per-issue plans and no search API calls. Model/server settings unchanged.

| Edition | Inventoried whole issues | Publisher positions | Named stories |
| --- | ---: | ---: | ---: |
| Civil War, 9780785170242 | 7 | 7 | 0 |
| Civil War: Captain America, 9780785178088 | 3 | 3 | 0 |
| Secret Invasion, 9780785170914 | 8 | 8 | 0 |
| Secret Invasion: Fantastic Four, 9781302494971 | 6 | 0 | 0 |

All four completed without model-stage errors. Secret Invasion also supplied an
ISBN-matched table of contents covering its eight inventoried issues in printed
order. Printed order and publisher event positions are separate evidence types.

The Fantastic Four collection exposed a real source disagreement: Google Books
labels its miniseries 2009, while Marvel lists the corresponding title/numbers as
2008. Three candidate placements are explicitly flagged and withheld. Its other
three inventoried issues are Fantastic Four (1961) #300 and #357-358; they are not
present in the event list. No missing issue is silently treated as covered.

These are development observations, not a blinded accuracy benchmark. The four
editions form only two event families, Civil War is familiar from prior work, and
the conflict case was used for a targeted fix. No independent gold adjudication
was performed. Zero new named stories is an important retrieval gap, even though
18 issue positions and one printed contents order were recovered successfully.

## Validation and preservation

145 targeted tests pass. Replay of 96 saved packets removed no previously accepted
inventory entries; three packets gained disjoint-range entries. These are stored
packets, not 96 independent editions or accuracy judgments.

SHA-256 verification found zero changes to 4,792 pre-existing public/data files.
Website data and historical results remain unchanged. `git diff --check` passed.
Original/final script snapshots, raw pages, replay details and checks are preserved
under `data/local-ai-trials/solo-v4-validation`. Live runs are separately preserved
as `solo-v4-events-four`, `solo-v4-year-conflict` and `solo-v4-final-four`.

## Next evidence needed

Prioritize issue/edition story evidence and independent series identity resolution,
then assemble the path-level held-out benchmark defined in
`enrichment-reassessment-2026-09-22.md`. The publisher adapter still supports the
issue-card layout only; the differently formatted Magneto page was inspected but
not added as a character-focused development task. No general website-format
coverage, required/optional classification or exhaustive story coverage is claimed.

Official source pages:
[Civil War](https://share.marvel.com/comics/discover/114/civil-war-the-complete-event),
[Secret Invasion](https://share.marvel.com/comics/discover/133/secret-invasion-the-complete-event).

Reproduce from the project root with a new unique run name:

```powershell
python scripts/solo_enrich.py --isbn 9780785170242 --isbn 9780785178088 --isbn 9780785170914 --isbn 9781302494971 --refresh-edition --name NEW-UNIQUE-RUN
```

## Controlled accuracy comparison — 2026-09-26

See [the story and reading-path benchmark](solo-accuracy-benchmark.md). A narrow
sentence correction raised provisional fact recovery from 5/7 to 6/7 across three
repetitions; the broader candidate regressed and was rejected. Three familiar
path replays passed, but complete unaided enrichment remains unproven. All prior
public/data files and all comparison runs were preserved.

## Seven-fact development benchmark — 2026-09-27

The bounded supplemental planning review recovered 7/7 annotated facts in each
of three runs. See [results and limitations](solo-seven-fact-validation.md).
189 tests passed; website data and prior results remain unchanged. Independent
validation of complete story scope and reading order remains outstanding.

## Fresh six-edition validation — 2026-09-27

[Fresh Vision/Annihilation validation](solo-fresh-validation.md) found 18/47
reference inventory units and 2–3/12 annotated premise facts per repetition.
No complete reading path was produced. The frozen collector made no false
completeness claims, but is not ready for complete unaided enrichment. Labels
remain provisional pending independent human adjudication; all prior data was
preserved and no extractor patch was made during this evaluation.

## Source identity development — 2026-09-29

[Series evidence trial](solo-series-evidence.md) improves Annihilation inventory
from 6/29 to 24/29 correct draft units in a final deterministic source replay.
The two preceding full live runs recovered 12/29 and 16/29. Vision's inventory
results were unchanged. 201 tests pass and all 5,424 pre-existing public/data
files remain unchanged. Story coverage and complete reading order are still
unproven; these reused cases now serve development, not held-out validation.

## Compound contents validation — 2026-09-29

[Full live retest](solo-compound-contents.md) recovered 28/29 Annihilation issue
units after evidence-backed separation of the prologue/Nova contents statement.
The prologue remains unresolved; story recovery is only 2/6 annotated facts and
no reading path was produced. 204 tests pass, code stayed fixed during the live
run, and all 5,509 pre-existing public/data files remain unchanged.

## Independent editorial reading order — 2026-09-29

[Reading-order importer](solo-editorial-reading-order.md) recovered a scoped
29-issue Annihilation sequence and 28 adjacent pairs matching the frozen
reference. It maps 28 issues to draft edition candidates, leaving the prologue
unresolved. Source attribution, scope and identity review remain explicit;
mandatory prerequisites and completeness remain unknown. 213 tests pass and
5,547 existing public/data files are unchanged. This measures extraction from
a known guide, not independent validation of its recommended order.

## Two-source order collection — 2026-09-29

[Registered collection and comparison](solo-order-comparison.md) now acquires
two guides in one command. The live Annihilation comparison finds 29 shared issues
in the same relative order and four source-only additions, retaining review status.
223 tests pass and all 5,560 pre-existing public/data files remain unchanged.
A Conquest smoke check exposed unresolved annotations/year gaps; general unaided
collection and exhaustive reading-order accuracy remain unproven.

## Frozen new-event benchmark — 2026-09-29

[Black Vortex validation](solo-black-vortex-benchmark.md) tested five previously
unused edition ISBNs with code and reference frozen before execution. Four
volumes recovered 18/18 confirmed-minimum inventory units, but reading-order
recovery was only 2/13 nodes and 0/12 adjacent pairs, with no verified edition
placements. The disputed event collection retained two conflicting-year entries
without flagging the conflict. No completeness claims were made, no production
patches were added, and all 5,583 pre-existing public/data files were preserved.

## Preserve and resolve reading-order gaps — 2026-10-01

[Saved-source development replay](solo-order-identity.md) retains all 13 Black
Vortex positions in each guide and resolves seven correct draft identities per
guide. Conflicting years and unverified volume aliases remain unresolved.
227 tests pass; Annihilation sequence controls remain unchanged, and 5,642
pre-existing public/data files were preserved. Complete reading order and
verified edition coverage remain outstanding.

## Index discovery and decimal capture — 2026-10-08

[Discovery assessment](solo-index-discovery.md) records automatic event-page
discovery, bounded ISBN identity research and overlapping-year conflict warnings.
Black Vortex now resolves eight of thirteen identities per source, with six and
four of twelve adjacent pairs. Complete order and verified placements remain
outstanding. Original Sin discovery preserved 67 and 141 source positions in
different scopes; these are operational results without accuracy adjudication.
Decimal capture retains nine and one previously unsupported designations without
accepting identities or membership. All six saved-source regression sequences
remain unchanged. 252 tests pass and 5,651 pre-existing public/data files are
unchanged. Reading order and contained/featured stories remain the priorities.

## Automatic decimal membership evidence — 2026-10-08

[Decimal membership trial](solo-decimal-membership.md) automatically links four
Original Sin source positions to explicit ISBN-matched equivalent numbering.
Six decimal positions remain without evidence. Both guides were discovered and
downloaded in a live run. Candidates retain the existing inventory conflict and
do not add accepted identities. 255 tests pass; prior resolved sequences and
5,651 pre-existing public/data files remain unchanged.

## Scoped numbering reconciliation — 2026-10-08

The [decimal membership collector](solo-decimal-membership.md) now automatically
checks catalog numbering against the explicit alias and all supplied collecting
evidence. Four Original Sin candidates pass; six decimal positions still lack
evidence. Global conflicts and identity review remain visible. A fresh live
run preserved previous accepted sequences; 258 tests pass and the preservation
audit finds no changes to 5,651 pre-existing public/data files. Typed decimal
mapping and independent accuracy validation remain outstanding.

## Typed decimal mapping and unattended event collection — 2026-10-08

[Unattended event trial](solo-unattended-event.md) now selects edition candidates
from the catalog and runs local enrichment plus guide discovery from a single
event slug. The seven-edition Original Sin run completed with no model stage
errors, producing 26/50 draft reading-path identities and four decimal placements
per guide. Explicit alias normalization revealed four source order inversions,
now retained as evidence-linked research tasks. Zero placements are fully
verified; issue-level named stories remain absent. 270 tests pass. Annihilation
29/33 sequences remain unchanged, and all 6,211 pre-run public/data files are
preserved. Unaided accuracy and completeness remain unproven.
