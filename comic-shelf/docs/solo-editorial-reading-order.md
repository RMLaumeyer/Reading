# Editorial reading-order import — 2026-09-29

The collector can now import a scoped independent reading guide and map its
issue sequence to saved edition drafts. The Annihilation trial extracted 29/29
reference nodes in the same order, including all 28 adjacent pairs. It found
28 draft edition matches and one unresolved membership gap: the prologue.

## Proposed sequence for review

This sequence follows the Road to Annihilation and Annihilation sections of
[Marvel Guides](https://marvelguides.com/annihilation-reading-order), an independent
editorial recommendation. Original series years are corroborated separately by
the existing publisher references. The source's broader Cosmic Forces section
was not selected; no judgment that it is unnecessary is implied.

| Order | Issues | Draft edition match |
| --- | --- | --- |
| 1 | Drax the Destroyer (2005) #1–4 | Book One |
| 2 | Annihilation Prologue (2006) #1 | Unresolved: Book One names an unnumbered prologue |
| 3 | Annihilation: Nova (2006) #1–4 | Book One |
| 4 | Annihilation: Silver Surfer (2006) #1–4 | Book Two |
| 5 | Annihilation: Super-Skrull (2006) #1–4 | Book Two |
| 6 | Annihilation: Ronan (2006) #1–4 | Book Two |
| 7 | Annihilation (2006) #1–6 | Book Three |
| 8 | Annihilation: Heralds of Galactus (2007) #1–2 | Book Three |

Book One ISBN: 9781302484576; Book Two: 9780785182856; Book Three: 9780785182849.
These are proposed issue-level placements, not confirmation of printed contents
order, exhaustive contained stories, chronology or mandatory prerequisites.

## Implementation

`scripts/guide_order.py` is a separate deterministic post-processing command for
saved enrichment results. It downloads a bounded public guide, selects exact
section headings, reads only lists following Reading Order labels, expands
explicit issue ranges, and saves source quotes and hashes. It excludes collected
edition shopping links, navigation, scripts and other sections. Unknown years,
conflicting identities, duplicate issues and malformed ranges remain problems.
Missing, duplicated or empty selected sections fail closed.

It uses publisher reference evidence to identify undated series but never adds
issues to an edition's inventory. The mapping retains independent-editorial
source attribution, draft identity candidates, gaps, and overlap warnings when
edition spans interleave. Required-reading status remains unknown. Even a fully
mapped editorial guide cannot be labeled publisher-endorsed or exhaustive.

This is registered-source acquisition with manually selected sections, not
general autonomous discovery. It does not call the language model or alter its
configuration. It does not yet run automatically inside `solo_enrich.py`.

```powershell
python scripts/guide_order.py --url https://marvelguides.com/annihilation-reading-order --section "Part 5.2: Road to Annihilation" --section "Part 5.3: Annihilation" --edition-run data/local-ai-trials/evidence-v3-annihilation-three --name YOUR_UNIQUE_RUN_NAME
```

The output directory is created exclusively; old results cannot be overwritten.

## Validation and limits

Final live acquisition: `data/local-ai-trials/reading-order-v2-annihilation`.
`path.json` holds the sequence; `collection-path.json` holds edition matches;
`manifest.json` records input and code hashes. The preceding v1 run is preserved.
The audit, scorer and assessment are in `reading-order-v1-validation`.

- 29 sequence nodes and 28 adjacent pairs match the frozen provisional reference.
- 28 nodes need identity review; one node lacks an accepted edition match. There
  are zero fully verified whole-issue matches under the existing strict gate.
- 213 tests pass, including range order, conflicting years, exact section scope,
  empty sections, duplicate nodes, source attribution and interleaved book spans.
- All 5,547 pre-existing public/data files remain unchanged. Edition inputs and
  code hashes were unchanged during the final acquisition. Website data is untouched.

The frozen reference used this same guide, so matching it measures parser fidelity,
not independent validation of the reading recommendation. No required-reading,
complete-event or story-exhaustiveness claim is established. No existing story
extraction score improved merely from importing a sequence.

Next: compare a second independent sequence, surface disagreements instead of
silently selecting one, resolve the prologue's edition membership, and test a
new event with interleaved issues. These are prerequisites for claiming general
unaided reading-order collection.
