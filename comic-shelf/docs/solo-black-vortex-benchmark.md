# Frozen Black Vortex benchmark — 2026-09-29

**The collector does not yet generalize to new reading orders.** With unchanged
code, it recovered only 2/13 reference event nodes and 0/12 adjacent pairs. It
did not produce a usable edition-linked reading path. The test exposed missing
series-identity evidence and undetected source conflicts, despite successful
basic inventory extraction from four series volumes.

## Design frozen before execution

The Black Vortex was selected because its 13 central chapters cross several
series and appear in overlapping collections. Five selected ISBNs had no prior
saved `result.json` matches by path or content. The reference, source selection
and all production Python hashes were frozen before inference. No production
code or model settings were changed during this benchmark.

The reference is provisional assistant research, not independent human
adjudication. It draws on exact-ISBN Google Books publisher metadata,
[Marvel's event collection listing](https://www.marvel.com/comics/collection/55082/),
an explicit [chapter-three issue description](https://www.marvel.com/comics/issue/52029/legendary_star-lord_2014_9),
and two editorial sequences:
[Marvel Guides](https://marvelguides.com/black-vortex-reading-order) and
[Comic Book Reading Orders](https://comicbookreadingorders.com/marvel/events/black-vortex-reading-order/).
The guides agree on the selected central sequence; agreement is not proof of
independent research or exhaustive required reading. The official event-guide
URL returned HTTP 403 during reference research and was not bypassed.

The labels deliberately distinguish a confirmed-minimum inventory from a
disputed event-collection case. The Guardians annual's identity and Star-Lord
#11–12 membership are unadjudicated and excluded from the primary inventory
denominator. Digital ISBN metadata says Star-Lord #6–10; print descriptions
describe a broader collection. No silent transfer between editions is permitted.

The current collector requires registered sources. A test harness supplied only
two URLs and an exact section heading, without changing production code or giving
the collector reference identities, order labels or a manually curated identity
reference. This is an assisted-source-selection test of automated acquisition,
extraction and mapping, not a test of autonomous web discovery.

## Results

| Measurement | Result |
| --- | --- |
| Edition runs completed without stage exceptions | 5/5 |
| Confirmed-minimum units recovered across four series volumes | 18/18 |
| Disputed event collection: reference-matching units | 5/13 |
| Disputed event collection: emitted units | 7; two use disputed Guardians year 2014 |
| Guide pages downloaded | 2/2 |
| Guide pages yielding any accepted nodes | 1/2 |
| Best/combined recovered central-event nodes | 2/13 |
| Correct adjacent pairs out of reference pairs | 0/12 |
| Verified issue-to-edition placements in produced paths | 0 |
| Unsupported complete-reading/required-reading claims | 0 |

The four series volumes were All-New X-Men: The Utopians (9781302480783),
Captain Marvel: Alis Volat Propriis (9781302481735), Guardians: Through the Looking
Glass (9781302482084), and Legendary Star-Lord: Rise of the Black Vortex
(9781302481346). Their accepted inventories contain seven central-event positions,
but this potential coverage did not become a usable extracted reading path.
The Guardians volume additionally emits a generic `Annual (2015) #1`, which is
reported separately and not counted as validated identity.

The event collection (9781302480899) has source disagreements: Google metadata
lists Guardians (2014) #24–25 and Guardians Team-Up #2, while Marvel's listing
identifies Guardians (2013) and Team-Up #3. The collector emitted the two disputed
2014 Guardians identities and did not raise a contents conflict. Team-Up remained
unresolved. The 5/13 score is diagnostic against the provisional event reference,
not proof of exact digital-edition contents.

Marvel Guides downloaded successfully and contained the selected section, but
its undated entries had no identity references available to the collector. The
parser raised its generic empty/invalid-guide error. The second guide yielded
the explicitly dated Alpha and Omega issues only; eleven rows were retained as
problems due to missing years and volume-style labels. These two nodes have the
right relative order but do not form a correct adjacent chapter pair. Neither
has accepted whole-issue edition coverage; both only have unresolved candidates.

This was one full local-model run per edition and one live acquisition per guide.
It does not measure model repeatability. Story accuracy was not newly scored;
character extraction remained disabled. The earlier 223 passing tests establish
regression coverage, not success on this new event.

## Next fixes, in priority order

1. Preserve unresolved reading-list rows with their original positions and source
   labels. A missing series year should not discard the observed sequence or
   collapse it to two misleadingly adjacent accepted nodes.
2. Add an evidence-backed identity-resolution stage for those rows, using dated
   issue/series sources and exact edition evidence. Volume numbers and shortened
   titles need verified aliases; simply stripping them is unsafe.
3. Cross-check already accepted identities and issue numbers against independent
   evidence. Current fallback/corroboration mostly helps unresolved entries and
   misses confident source errors such as Guardians (2014).
4. Re-run these now-preserved cases as development tests, then freeze another new
   event to assess generalization. Keep source failures distinct from parser
   failures and keep required-reading claims unknown without evidence.

No patch was applied after seeing these results. Historical outputs, reference
labels, input data and website data were preserved. SHA256 validation checked
5,583 pre-existing public/data files with no changes; all frozen production-code
hashes remained unchanged.

Artifacts: `data/local-ai-trials/black-vortex-v1-validation` contains selection,
reference, freeze, source config, research pages, runner, scorer and scores;
`black-vortex-v1-five` contains the live edition run; `black-vortex-v1-orders`
contains the guide acquisitions, failures, partial path and mapping. These remain
separate from website data and are not publication candidates.
