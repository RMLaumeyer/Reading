# Qwen multi-passage trial — October 27, 2026

The bounded worker now asks Qwen3.5-4B for up to three premise passages, emphasizing protagonists, central conflicts and distinct plot threads. It accepts only valid unique excerpt IDs, restores source order, and verifies each quote against its cited source. Individual passages remain separately cited; the joined synopsis is a collection of source excerpts, not original prose.

Contents review now flags provisional bibliographic series identity and partial material explicitly. Six worker tests cover invented/duplicate IDs, truncated model output, abstention, ordering, provisional identity/partial flags and initialism boundaries. The 53 existing edition-parser tests also pass. No publication code was added.

## Development runs

The first ten-book revised run (`worker-v2-dev-20261027`) exposed pre-existing sentence splitting at S.H.I.E.L.D. and M.O.D.O.K. It was completed and preserved. A worker-local protection/restoration step fixes initialism boundaries without altering the shared legacy splitter. Replacement code was then frozen for `worker-v3-dev-20261027` and `worker-v3-fresh-20261027`; no further extraction changes were made during those runs.

On the original development books, Spider-Man/Deadpool now includes the black-market-tech trigger, Trials of X covers three explicit threads, and Dark Phoenix includes the X-Men's central dilemma. Venom selections still omit threads or spend slots on repeated context. Using the earlier editorial rubric, four synopses are usable short drafts (Runaways, Deadpool, Ultimate X-Men, Dark Phoenix), up from three in the original run. Three need edits (Spider-Man/Deadpool, Trials of X, Venom: Infiltration), Devil's Pack remains a weak fragment, Worldwide remains held for edition conflict, and All-New X-Men correctly abstains. These reused cases are development evidence only.

## Fresh sample

Ten new cached editions were selected and packets frozen in `worker-v2-fresh-20261027` before fresh inference. That directory never ran inference. The identical packets were copied into the v3 experiment after the initialism fix. Its manifest's generic “Reused development cases” label describes the copying mechanism inaccurately for this batch: these ISBNs had no outputs in the earlier development run, and this was their first worker inference. Source-derived expectations were saved in `pre-inference-review.txt` before fresh inference. They were not sent to Qwen. Selection excludes prior model packets and edition-result directories; it is not a guarantee against every possible historical use.

All ten completed without worker errors. Every emitted passage is verbatim-grounded. Packet and code hash checks passed. These checks establish execution and source fidelity, not semantic accuracy or edition truth. All judgments below are assistant editorial review of supplied evidence, not independent human adjudication.

| Fresh edition | Usefulness 0–3 | Review |
| --- | ---: | --- |
| Blade: Evil Against Evil | 3 | Captures Dracula's instruction, Blade's powers, and preparation for Adana with Bruce Banner context. Usable short draft. |
| Hawkeye: My Life As a Weapon | 2 | Includes Kate Bishop and Clint's evidence-interception mission, but starts with an unclear “his.” Identify Clint before the opening sentence. Contents remain unparsed. |
| Marvels | 1 | Atmospheric excerpt starts “Here” and misses a clear framing premise. The detected contents conflict appears to be a parser false positive: catalog #0 – 4 is recorded as [0,0], versus source [0,4]. Preserve the flag until separately corrected. |
| Moon Knight: God & Country | 3 | Clear violent return, registration question, Tony Stark and mounting pressure. Usable as a source-excerpt draft. |
| Doctor Strange: The Way of the Weird | 0 | Entire selection is “Doctor Strange, of course.” Source-grounded but unusable. Source offers threat context; the cost-of-magic sentence also mixes creator credits. Both eligibility and selection warrant later investigation. |
| Ms. Marvel: Something New | 2 | Covers old enemy, trust and friendships. Omits Bruno/Wakanda and the powers/reunion thread; opening “her” relies on the later name. |
| Star-Lord & Kitty Pryde | 2 | Gives Battleworld survival premise but misses the crucial Age of Apocalypse Kitty distinction explicitly present in the source. |
| Captain America: Two Americas | 1 | Captures shield succession but misses the threatening 1950s Captain America and urgency. |
| Deadpool: Soul Hunter | 2 | Includes demon's soul-recovery mission and aquatic target; omits Iron Man flashback and Spider-Man team-up. Useful partial premise. |
| Doom Treasury Edition | 3 | Clear Doom/Valeria mission to stop Galactus. Usable main-story premise; does not describe anthology extras or claim exhaustive coverage. |

Three usable drafts, four requiring edits, and three weak/unusable outputs. Four editions have no mechanical blockers, but one is the unusable Doctor Strange draft. “Draft for review” must never be read as editorial acceptance. Contents parsing was unchanged; source gaps and parser limitations persist independently of synopsis changes.

## Decision

The requested worker changes and fresh trial are complete. Keep the bounded worker available for reviewed drafts; do not expand to unattended catalog publication. Multiple passages improve some familiar cases but did not establish reliable coverage on this fresh sample. Actual correction time, an independent human review and a manual-work baseline remain unmeasured, so no time-saving claim is justified.

Preserve these experiments as the decision evidence. A further experiment should compare selection with a simple full-source-description baseline and evaluate whether Qwen reduces reviewer effort at all, before another round of exception-specific patches. Previous runs and served website data were not modified by these worker runs.
