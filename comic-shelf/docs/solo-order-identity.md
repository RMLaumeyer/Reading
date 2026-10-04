# Preserve reading-order gaps — 2026-10-01

Both frozen Black Vortex guide pages now retain all 13 source positions. Each
resolves seven correct draft identities, versus the prior results of zero and
two respectively. Missing years no longer discard the observable sequence.
This is a development replay of saved sources, not a new held-out benchmark or
a new local-model run.

The parsers retain `sourceSequence` separately from accepted `orderedIssues`.
Unresolved, conflicting, duplicate and unsupported entries keep their source
position and quote. Accepted positions retain gaps instead of being renumbered.
The edition mapping exposes unresolved source positions and cannot declare full
source coverage while those gaps remain.

The new `order_identity.py` stage proposes missing years using existing edition
evidence. It requires an exact series name after punctuation normalization, a
containing issue range and a unique year across candidate editions. Conflicting
edition years veto inference. It does not strip volume labels, invent aliases,
override explicit source conflicts or change edition membership. Duplicate
resolved identities are withheld. Every proposal requires identity review;
original parser problems remain visible.

Both `order_research.py` and the standalone guide importer apply this stage and
save their original extracted paths before resolution. No reference answers
are supplied to extraction or identity resolution.

| Frozen-source replay | Marvel Guides | Comic Book Reading Orders |
| --- | ---: | ---: |
| Source positions retained | 13 | 13 |
| Correct resolved identities | 7 | 7 |
| Unexpected resolved identities | 0 | 0 |
| Correct adjacent pairs with no intervening unresolved slot | 5/12 | 3/12 |
| Remaining unresolved positions | 6 | 6 |
| Fully verified edition placements | 0 | 0 |

Resolved identities remain draft candidates. The two guides resolve different
subsets; no automatic merged sequence or completeness claim is produced. The
Guardians (2013)/(2014) disagreement blocks resolution in the first guide.
Volume-style labels remain unresolved in the second. Existing erroneous accepted
edition identities have not been repaired: broader cross-source validation of
accepted entries remains necessary.

227 tests pass, including missing positions, conflicting evidence, unsupported
aliases and duplicate proposals. Saved Annihilation controls retain their prior
29- and 33-node identities and order. The preservation audit checked 5,642
pre-existing public/data files with no changes. Website data, frozen references,
historical results and model settings remain unchanged.

Artifacts are in `data/local-ai-trials/order-identity-v1-validation`: `checks.json`
records scoring/preservation; `final-source-1.json` and `final-source-2.json`
contain final paths and mappings; `final-verification.json` records code hashes
and Annihilation regression checks. Earlier replay outputs are also preserved.

Next: acquire explicit evidence for unresolved volume aliases and series years,
and detect contradictions in already accepted edition entries. Source-position
retention is now working, but complete unaided reading-order collection remains
unproven.
