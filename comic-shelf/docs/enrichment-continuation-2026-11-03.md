# Qwen enrichment and improvement block — November 3, 2026

Published **11 reviewed synopses**, increasing the local approved total from **313 to 324**. Ten came from 25 new editions; one came from two targeted source-recovery runs. All eleven required explicit source-backed revision. This is useful enrichment throughput, but it is not evidence that Qwen is becoming an independent publisher.

## Enrichment results

The 27 worker cases completed without failures. Two fresh cases had no eligible plot excerpts, leaving 25 recorded model responses. All 55 selected quotes are literal frozen-source text. Worker time was 168.81 seconds. Fifteen fresh editions remain held; one previous hold was recovered. The reviewed backlog is now **415 editions** (401 + 15 − 1).

New exact-ISBN public-library records supplied collecting evidence for Secret Invasion: Inhumans and plot/contents for Fantastic Four/Inhumans: Atlantis Rising. The Secret Invasion source labels the original series 2008 while the old bibliographic label says 2009. [Marvel’s original four-issue series](https://www.marvel.com/comics/series/5352/Secret_Invasion%3A_Inhumans_%282008_-_2009%29) and [original #1](https://www.marvel.com/comics/issue/21774) corroborate 2008 and the same missing-Black-Bolt premise. The explicit manual assessment resolves the parser conflict for synopsis review only. Raw inventory remains unchanged; no issue keys, years, aliases or ordering were published. The revision names the searching family members and preserves uncertainty about Black Bolt’s survival.

Atlantis Rising remains held: the new collecting list includes undated Namor, Atlantis Rising and Fantastic Four Unlimited entries whose series identities remain unresolved. Its new plot evidence does not remove those gates. Deadpool Classic Vol. 8’s lookup failed reconciliation: two ISBN-matched records share a description but carry different series labels, Deadpool Classic (2008) and Deadpool (1997), while their collecting sentence says Deadpool (1998). The failure, downloaded records and hashes are retained; do not bypass the disagreement or repeat the same lookup.

The fresh review restores omitted setup and threads: Black Bolt’s imprisonment, Wolverine’s concrete investigation and leviathan hunt, Joe Fixit’s Hulk/Las Vegas context, Jane Foster’s identity, and all seven Uncanny Origins stories. It removes advertising and rhetorical questions while preserving uncertain outcomes. [Doctor Strange #381](https://www.marvel.com/comics/issue/65070/doctor-strange-2015-381) establishes the publisher’s 2015 original-series namespace and November 2017 release; the target’s generic 2017 label is explicitly distinguished for synopsis-only review. No additional plot from the publisher issue was inserted.

Punisher by Rucka retains a concrete range hold: catalog title #1–5 versus source #1–6 plus unnumbered partial material. Darth Vader retains a 2023 target-label versus 2020 original-run namespace research hold; the exact original #37 publisher page was inaccessible. Partial material, unnumbered extras, empty descriptions and other unresolved flags remain held.

## Improvement experiment: four passages instead of three

Tested a new narrow hypothesis: allowing four verbatim passages may recover named setup or distinct threads that the default three-passage selector omits. Six difficult cases from this fresh batch were selected deliberately. Source bytes, candidate inputs, model, temperature, thinking-off setting and response budget were fixed. Only “three” became “four” in the original prompt and schema maxItems increased to four. The manifest and per-case criteria were saved before the six requests. Original results and production code were preserved.

| Comparison | Original three | Experimental four |
| --- | ---: | ---: |
| Drafts passing delegated editorial review unchanged | 0/6 | 0/6 |
| New model requests | Saved baseline | 6 |
| Literal selected quotes in new requests | — | 19 |

Three outputs were identical (Wolverine, Black Bolt and Joe Fixit). Uncanny Origins added Daredevil, covering four of seven separately described origin characters; it still omitted three. Mighty Thor restored Jane Foster and realm unrest but dropped Malekith’s distinct war thread. Loki added a war exclamation without identifying King Loki. These outcomes do not justify changing the default. The experiment completed with zero failures in 44.05 seconds and no publication.

This is a six-case targeted development probe with baseline-first order, no repeats and delegated Codex judgments, not independent gold data. It does not estimate general accuracy or establish that four passages always perform worse. It does show that this capacity increase did not eliminate editing in the selected cases.

## Operational improvement: acquisition history guard

Added reusable acquire_with_history.py in this continuation’s artifact folder. It defaults to a read-only history plan. With --execute it permits a new exact-ISBN lookup only when no prior acquisition audit exists, requires an output inside the trial archive, and preserves the acquisition/source evidence. Existing accepted and failed attempts both skip network calls and report audit paths, hashes and URLs. It neither runs inference nor publishes. Prior sources remain available for explicit reviewed reuse; a changed source strategy requires separate review.

Four fixture tests passed: accepted/failed history prevents network and output creation; a new lookup is saved once and then skipped; an outside-archive destination is refused before acquisition; and unknown/incomplete audit states fail explicitly. A read-only check against the real Deadpool ISBN found the failed attempt and returned skip_existing_attempt. This helper is an opt-in handoff utility, not a production worker integration or a concurrency lock.

## Verification and limits

Both publication receipts, exact backups, all 78 frozen worker script hashes, source and parent packet hashes, prompt hashes, successful finish reasons, and all reviewed citations passed. Only eleven intended summary/source/review records changed. Prior approvals, unrelated book fields and top-level metadata were preserved. Canonical approved overlay, public data, built data and actual localhost-served bytes agree. The old preview was unavailable during the first HTTP check; it was restored and both publication checks subsequently passed. No failed HTTP check is represented as a successful verification.

The original selector and parser version 25 remain unchanged. The production test suite was not rerun for this data-only work; the four new tests apply specifically to the new helper. The legacy collector stays paused and no remote deployment occurred. Across production and isolated experiment there were 33 case executions, 31 model responses and 74 literal selected quotations; experiment requests are not additional enriched editions.

## Next work

Use the history guard before new exact-ISBN acquisitions. Prioritize missing source evidence for All-New X-Men Vol. 3 and Spider-Man/Doctor Octopus: Negative Exposure. Research the already improved Atlantis Rising packet’s series identities without repeating its acquisition. Resolve the Darth Vader original-series label using exact publisher issue or dated same-title collection evidence. Preserve the Deadpool and earlier Winter Soldier failed lookup histories.

Further autonomy work should target self-contained setup and distinct-thread coverage, with a new mechanism tested on preserved failures and then untouched cases. Repeating the same prompt, increasing batch size or counting published editorial revisions does not demonstrate model improvement. Keep publication review gates in place.

Artifacts: data/local-ai-trials/continued-20261103, sustained-25r-20261103 and source-recovery-two-20261103. The continuation folder includes final-verification.json, known-held.json, the isolated four-passage-experiment, lookup helper/tests and next-session-priorities.json.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302940744 | Wolverine by Benjamin Percy Vol. 3: Issues #14-19 | Source-backed revision |
| 9781302533618 | Immortal Thor Vol. 5: Death of the Immortal Thor: Issues #21-25 | Source-backed revision |
| 9781302501488 | Black Bolt Vol. 1: Hard Time: Issues #1-6 | Source-backed revision |
| 9781302482121 | Loki: Agent of Asgard Vol. 3: Last Days: Issues #12-17 | Source-backed revision |
| 9781302496111 | Deadpool: Back In Black: Issues #1-5 | Source-backed revision |
| 9781302504717 | Doctor Strange By Donny Cates Vol. 1: God of Magic: Issues #381-385 | Source-backed revision |
| 9781302499211 | Doctor Strange/Punisher: Magic Bullets: Issues #1-4 | Source-backed revision |
| 9781302525255 | Joe Fixit | Source-backed revision |
| 9781302517595 | Uncanny Origins Vol. 2: Myth & Magic: Issues #8-14 | Source-backed revision |
| 9781302486259 | The Mighty Thor Vol. 1: Thunder In Her Veins: Issues #1-5 | Source-backed revision |
| 9781302481070 | Secret Invasion: Inhumans: Issues #1-4 | Source-backed revision |
