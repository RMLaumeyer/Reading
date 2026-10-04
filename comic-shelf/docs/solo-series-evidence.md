# Series evidence development trial — 2026-09-29

The source-first approach improves draft issue inventory substantially, but does
not establish complete reading order or story coverage. Those remain the main
priorities; character extraction remains disabled.

## Approach

The collector now fetches bounded, registered public distributor references with
explicit original series years. These references corroborate the identity of
issues already listed in the target edition; they cannot add another edition's
contents. Matching requires the same series name (punctuation normalization only),
a containing issue range, and a unique year. Conflicting years remain unresolved.

The two registered Annihilation references are PRH's
[Annihilation Day](https://prhcomics.com/book/?isbn=9781302963255) and
[Desperate Measures](https://penguinrandomhouselibrary.com/book/?isbn=9781302963262).
Reference URLs were selected during research, so this is not general autonomous
source discovery. Raw pages, hashes, membership evidence and identity evidence
are retained separately. All inferred identities remain drafts requiring review.

ISBN lookup also examines at most three public catalog candidates. Multiple
matching records are accepted only when series and synopsis agree exactly,
allowing a narrowly recognized trailing credits/legal appendix. Differences in
substantive descriptions or years still block acceptance. The chosen record and
all equivalent record evidence are retained. Book Two's two ISBN matches exposed
this duplicate-record case.

Finally, contents parsing recognizes an ampersand between explicit named issue
entries, while retaining ampersands within titles and numeric disjoint ranges.

## Measured results

| Edition | Previous correct units | Final inventory replay | Reference units |
| --- | ---: | ---: | ---: |
| Annihilation Book One | 0 | 4 | 9 |
| Annihilation Book Two | 0 | 12 | 12 |
| Annihilation Book Three | 6 | 8 | 8 |
| Total | 6 | 24 | 29 |

All 24 emitted units match the frozen provisional reference. They still require
identity review. The 29-unit denominator excludes the ancillary handbook and
does not establish exhaustive extras coverage. Book One still lacks the prologue
and four Nova issues because its compound contents statement remains unresolved.

The final deterministic replay used saved live source packets and the unchanged
reference/scorer. It supplied no gold labels to extraction. Vision's three cases
remained 6/6, 6/6 and 0/6, giving 36/47 across the combined inventory replay.
These are now development cases, not fresh held-out validation, and the reference
remains assistant research pending independent adjudication.

Two full live runs were preserved: `evidence-v1-annihilation-three` recovered
12/29; `evidence-v2-annihilation-three` recovered 16/29 after duplicate-record
handling. The final ampersand parser correction was tested by deterministic
inventory replay, **not a third full model run**. The second live run completed
without stage exceptions but produced no named stories or reading paths. No
story-accuracy improvement is claimed.

## Verification and next work

201 tests pass, including conflicting years/descriptions, wrong ISBNs, ambiguous
candidates, partial scope, issue-range boundaries and parsing regressions.
The preservation audit verified all 5,424 pre-existing public/data files unchanged.
Website data, historical trials, frozen labels and local model settings were
preserved. New evidence is isolated under `data/local-ai-trials/`.

Audit artifacts: `evidence-v1-validation/final-inventory-replay.json` and its
reproducible `validate_final.py`; live source acquisition and model outputs remain
in the two run directories above. The validator writes exclusively to a new file,
so preserve/rename its output explicitly before any intentional rerun.

Next priorities are evidence-backed resolution of Book One's compound contents,
issue-level contained-story evidence, and a sourced sequence with explicit scope
and prerequisites. Adding issue inventory alone does not solve those tasks.
After development fixes, use new editions and paths with frozen references for
the wider accuracy benchmark. The collector is not yet ready for complete
unaided enrichment.
