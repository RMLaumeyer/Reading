# Compound contents validation — 2026-09-29

The full three-book Annihilation retest recovered 28/29 expected issue units,
up from 24/29 in the previous deterministic replay. All 28 emitted units match
the frozen provisional reference. This is progress in edition inventory, not
proof of complete reading order or contained-story coverage.

## Change

The parser now separates an unnumbered work joined to a numbered series only
when both names are independently present in the registered publisher identity
references. Book One's compound prologue/Nova statement consequently yields
Nova #1–4. The prologue remains unparsed: an unnumbered work does not automatically
mean issue #1. A recognized combined series title takes precedence over splitting.
Partial contents stay partial, and conflicting years still prevent acceptance.

This uses the existing saved reference sources and generic name/range matching;
no benchmark answer or Annihilation-specific issue number was added to code.

## Results

| Edition | Previous replay | Full live retest | Expected |
| --- | ---: | ---: | ---: |
| Annihilation Book One | 4 | 8 | 9 |
| Annihilation Book Two | 12 | 12 | 12 |
| Annihilation Book Three | 8 | 8 | 8 |
| Total | 24 | 28 | 29 |

The new run is `data/local-ai-trials/evidence-v3-annihilation-three`. It acquired
fresh sources and ran Qwen3.5-4B sequentially with unchanged model settings.
All three editions completed without stage exceptions. Code hashes remained
unchanged during the run. All inferred identities still require review, and no
edition was declared ready for publication. The denominator excludes the ancillary
handbook and does not establish exhaustive extras coverage.

Story extraction recovered only 2/6 annotated central facts. Its four selected
highlights were exact source quotes, but quotation accuracy did not produce full
premise coverage. There were no named stories or publisher path placements.
Character extraction remained disabled. These are reused development cases with
assistant-researched provisional references, not independent held-out validation.

The cached Vision inventory controls were unchanged (6/6, 6/6, 0/6). They did not
undergo another model run. 204 tests pass, including combined titles, missing
reference names, partial scope and conflicting years. SHA256 checks verified all
5,509 pre-existing public/data files unchanged. Scores and a reproducible validator
are saved in `data/local-ai-trials/evidence-v3-validation`.

## Remaining priorities

The next major gain should come from contained-story evidence and reading-list
acquisition, alongside explicit identification of the unnumbered prologue. A
targeted publisher-list search did not identify a matching original Annihilation
sequence in this pass. Marvel Cosmic Invasion and Annihilation: Conquest results
were not adopted as substitutes. A series index establishes neither reading
sequence nor required prerequisites.

Keep proposed issue membership, source-listed order, and required-reading claims
separate. Preserve unresolved abbreviations and conflicting reprint identities
until evidence resolves them. Complete unaided enrichment remains unproven.
