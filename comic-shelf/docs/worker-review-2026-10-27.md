# Ten-edition Qwen draft review

Reviewed October 27, 2026 against the frozen packets in `data/local-ai-trials/worker-20261027-ten-v2`. This is an assistant editorial assessment of source fidelity and usefulness, not independent human adjudication or verification against the comics. No new sources, model calls, worker changes, or publication occurred during this review.

## Rubric

Score synopsis usefulness from 0–3: 0 missing or unsuitable for this edition pending research; 1 a supported fragment that misses the main premise or most of a multi-thread collection; 2 a useful premise needing context or another major thread; 3 usable as a short source excerpt. A score of 3 does not establish complete story coverage. Corrections below describe editorial work, not measured correction time. Evidence availability and extraction quality are assessed separately.

## Results

| Edition / ISBN | Synopsis score | Decision | Correction or research needed |
| --- | ---: | --- | --- |
| Runaways: Teenage Wasteland / 9780785170891 | 3 | Keep synopsis draft | Clear protagonists and new arrival. Contents are absent from the supplied source; research exact edition contents. Do not fill them from the catalog title alone. |
| Spider-Man/Deadpool: Arms Race / 9781302503789 | 1 | Revise synopsis | “The battle” and “them” lack context. The excerpt omits the source's central trigger: Wade selling S.H.I.E.L.D. tech leads to the pair's falling-out. Select that premise before the Chameleon thread. Contents year uses a provisional same-source bibliographic mapping. |
| Amazing Spider-Man: Worldwide Vol. 1 / 9781302513924 | 0 | Hold for edition research | Source has #12–19 while catalog title says #1–11. The Regent excerpt is source-faithful, but its applicability to the intended catalog edition remains unresolved. Preserve it as source evidence; do not approve a shelf synopsis until identity is resolved. |
| Trials of X Vol. 12 / 9781302525460 | 1 | Revise synopsis | Selected Marauders sentence covers one of four explicit threads. Include Emma Frost/Kingpin, X-Men/M.O.D.O.K., and Sabretooth, as well as the Marauders mission. Contents match the four stated source ranges, totaling five issues. |
| Venom: Devil's Pack / 9781302483081 | 1 | Revise synopsis and contents | Selected rescue question covers the Philadelphia thread but omits Hellstrom, the pact and Flash's soul. Contents parser accepts #23–25 but leaves #28–30 unparsed; do not imply the accepted inventory is exhaustive. The source explicitly supplies both disjoint ranges. |
| Venom: Infiltration / 9781302528874 | 2 | Revise synopsis | Excerpt gives Venom/Toxin's rescue premise but leaves the hero unnamed and omits Eddie Brock's separate journey. Source explicitly identifies Natasha Romanoff and Eddie's confrontation with manifestations of his anger, hate and wrath. |
| Deadpool: Millionaire With a Mouth / 9781302485597 | 3 | Keep synopsis draft | Establishes Deadpool's mercenary work and popularity. The source itself is promotional and offers little specific conflict; do not infer deeper story coverage. Contents directly match stated #1–5. |
| Ultimate X-Men: Absolute Power / 9781302478698 | 3 | Keep synopsis draft | Clear team, aftermath and new adversary. Source leaves adversary unnamed, so retained generality is appropriate. Contents year uses a provisional same-source bibliographic mapping. |
| X-Men: Dark Phoenix Saga / 9781302513696 | 2 | Revise synopsis; review extras | Jean Grey's corruption is central, but “one of their own” lacks an explicit team antecedent. Add the source's X-Men decision about saving Jean versus the universe. Main #129–138 inventory is supported; partial extras remain unresolved and must stay partial. |
| All-New X-Men: The Ultimate Adventure / 9781302478865 | 0 | Correct abstention; retrieve evidence | Supplied synopsis contains only a collecting statement. No plot can be recovered from it. Contents year uses a provisional same-source bibliographic mapping. |

Three of ten synopsis drafts are usable short excerpts; five need editorial revision, one needs edition research, and one correctly abstains. Nine of ten have exact source grounding, but grounding alone does not establish synopsis usefulness. Among eight cases with plot evidence and no detected edition conflict, three score 3, two score 2 and three score 1. These are judgment calls on a small development sample, not a catalog-wide accuracy estimate.

The worker's five mechanically unblocked drafts include three synopses needing revision: Spider-Man/Deadpool, Trials of X and Venom: Infiltration. Mechanical status therefore cannot substitute for editorial acceptance.

## Contents and review-gate findings

Seven editions account for all explicitly listed whole-issue ranges in their packets, conditional on the provisional series-year mappings where used. Runaways has no source collecting statement; Worldwide is withheld for conflict; Devil's Pack misses the second range. Dark Phoenix's main whole-issue range is captured, but extras remain unresolved. This measures agreement with supplied text, not independently verified edition completeness.

Three results contain `identityResolution.state: draft`: Spider-Man/Deadpool, Ultimate X-Men and All-New X-Men. The small worker does not add a dedicated bibliographic-identity review reason, although the full pipeline already does. All results retain `readyForPublication: false`; none should be treated as independently verified identities. Dark Phoenix also has partial material that warrants an explicit review reason beyond its current unparsed/unresolved flags.

## Correction effort and decision

Eight packets have enough nonconflicting plot evidence for a reviewer to keep or revise a synopsis without additional retrieval. Of those, five need another selection/editing pass. Two cases require retrieval or identity research; missing Runaways contents creates an additional field-specific research task. Actual correction time and a manual-work baseline were not measured, so this trial does not establish net time saved.

Keep Qwen as a draft worker. It executes quickly, preserves evidence, and abstains when the packet contains no plot. The bottleneck demonstrated here is choosing sufficient premise coverage, alongside source and edition gaps. Do not expand the batch yet.

The next bounded change should let Qwen select up to three short premise excerpts, asking for explicit protagonists and all major source-described threads. Validate each excerpt verbatim and keep research failures separate from editorial gaps. Also surface provisional identity and partial-material review reasons. Test those changes on these now-development cases, then freeze a fresh ten-edition sample. Keep this run and review unchanged; improvements on these books are regression evidence, not fresh validation.
