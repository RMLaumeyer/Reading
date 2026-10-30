# Full-description baseline comparison

October 27, 2026. Compared the ten frozen first-inference editions from `worker-v3-fresh-20261027` with a baseline that preserves each full publisher description before bibliographic information. No additional inference, retrieval, publication or changes to prior outputs were needed.

## Result

| Measurement | Full description | Qwen selection |
| --- | ---: | ---: |
| Total words | 962 | 407 |
| Retained review cues | 27/27 | 17/27 |
| Cases losing at least one cue versus full description | 0/10 | 6/10 |

Qwen removes about 58% of the words while omitting about 37% of the chosen review cues. This is a coverage/compression tradeoff, not proof of factual errors. The full description has all cues by construction because labels were drawn from these sources. It also retains marketing language, collecting statements and creator credits, so it is not automatically a polished synopsis.

Labels are post-hoc assistant judgments from already examined books. Exact string alternatives measure whether selected passages retain those specific cues; they do not establish semantic truth, exhaustive plot coverage, equal importance of cues, or independently adjudicated accuracy. Human correction time and net time savings remain unknown. The selected text also needs checking against the full description for omissions, so shorter text alone is not a review-time measurement.

## Where context is lost

- Hawkeye loses the explicit Clint Barton identity cue even though “Clint” remains; the reviewer must supply the missing first-name/surname context. The diagnostic cue deliberately counts Clint only, so it does not score this editorial defect.
- Marvels loses New York and the explicit ordinary/fantastic framing.
- Doctor Strange loses both threat context and the cost-of-magic premise.
- Ms. Marvel loses Bruno/Wakanda and the powers-disruption thread.
- Star-Lord & Kitty Pryde loses the Age of Apocalypse identity distinction.
- Captain America loses the dangerous 1950s Captain America thread.
- Deadpool loses the Iron Man flashback and Spider-Man team-up.

Hawkeye's wording issue is outside the literal omission count; the other six editions account for the ten omitted cues. Blade, Moon Knight and Doom retain all their chosen cues. Retaining those cues is not proof of complete synopsis coverage.

## Concrete recommendation

Keep the full publisher description as the evidence preserved for review. Show Qwen's shorter selection beside it as an optional proposed synopsis, with identity/contents flags visible. Do not replace the source description automatically or treat a mechanically unblocked selection as approved enrichment.

This keeps the local worker useful for drafting and queue processing without asking it to decide which source context can be discarded permanently. A future Qwen role worth evaluating is identifying candidate fields or research tasks while retaining the full evidence. Such a role needs its own bounded evaluation; it has not been implemented or validated here.

The comparison artifact already provides this side-by-side review format for all ten books. The worker and website remain unchanged during this baseline assessment. No additional prompt patch is justified solely to improve these now-familiar cases.

## Reproduce

```powershell
python scripts/compare_worker_baseline.py --run data/local-ai-trials/worker-v3-fresh-20261027 --output data/local-ai-trials/NEW_UNIQUE_COMPARISON
```

The diagnostic script has labels for these ten editions only and rejects an existing output folder. `comparison.json` records source/result hashes, per-case word counts and retained/omitted cues. `comparison.md` includes both texts and the per-case coverage table. It is a review artifact, not a live website change.
