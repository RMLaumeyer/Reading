# Namespace recovery — October 31, 2026

Researched six held editions, retried five through the unchanged local Qwen selector, and published five reviewed synopses locally. The canonical approved overlay now contains 117 editions. Strange Academy was accepted unchanged; the other four drafts required explicit Codex revisions. Fearless Defenders remains held without another model request. Of the original 166 held editions, 142 remain unpublished after the recovery passes.

| ISBN | Edition | Result |
| --- | --- | --- |
| 9781302479831 | Avengers West Coast: Vision Quest | Published revision restoring the team and Vision's capture/dismantling setup |
| 9781302498955 | Monsters Unleashed | Published revision restoring the protagonist teams omitted by the question-only selection |
| 9781302532857 | Spider-Boy: The Dragon's Challenge | Published revision restoring the young heroes and tournament stakes |
| 9781302501945 | Zombies Assemble 2 | Published revision using intact punctuation and preserving the alleged cure's uncertainty |
| 9781302942205 | Strange Academy: First Class Collection | Published unchanged Qwen selection |
| 9781302369903 | Fearless Defenders: Doom Maidens | Held for stronger plot evidence; distributor metadata repeats promotion |

## Edition evidence

Vision Quest's original exact-ISBN description and #42–50 collecting statement match [Marvel's Vision Quest collection](https://www.marvel.com/comics/collection/51440/). The publisher's [Vision Quest reading list](https://share.marvel.com/comics/discover/2047/vision-quest) calls the relevant run West Coast Avengers (1985), while the collection calls it Avengers West Coast. That shared collection/arc, plot and issue context supports a manual name/year reconciliation for this synopsis. No global alias was added and the reading list did not expand the edition's membership.

Monsters Unleashed's original exact-ISBN description and [separate exact-ISBN library record](https://www.richlandlibrary.com/catalog/detail/1774724) identify the Leviathons threat to Marvel's hero teams. Marvel's [five-issue event guide](https://www.marvel.com/comics/guides/824/monsters-unleashed) and [January 2017 issue #1](https://www.marvel.com/comics/issue/60625/monsters_unleashed_2017_1) identify that limited event. The [April 2017 issue #1](https://www.marvel.com/comics/issue/62724/read) instead introduces the Kid Kaiju/Elsa Bloodstone ongoing series. Both pages display the same series name, year and issue number. This is explicit evidence that those fields alone cannot establish unique issue identity. The synopsis is now associated with the limited event; no issue keys or run mappings were changed.

Spider-Boy's original exact-ISBN #11–16 collecting statement and 2023 bibliographic identity are corroborated by the [publisher's series listing](https://www.marvel.com/comics/series/38659/spider-boy_2023_-_present?creatorId=11482&variants=true). That reference supplies a namespace, not new edition membership or plot facts.

Zombies Assemble 2's two cached distributor records match the exact ISBN and explicitly collect Zombies Assemble 2 #1–4, despite the broader undated category label Zombies Assemble. Their descriptions differ only in apostrophe characters after case-specific inspection. The [publisher's Zombies Assemble 2 (2017) listing](https://www.marvel.com/comics/series/23388/zombies_assemble_2_%282017%29) independently corroborates the literal series/year. The original ISBN collecting statement establishes the range. The parser's unresolved supplementary entry and strict aggregate failure remain in the raw artifacts; the manual review resolves them for this edition only.

Strange Academy's two exact-ISBN distributor records have identical descriptions and #1–6 contents. Their labels are Strange Academy (2020) and Strange Academy (2020-). Both identify the same start year as the original source. The open-ended-label difference was assessed manually; the strict aggregate failure and original labels remain preserved. Fearless Defenders's exact-ISBN distributor record supports the 2013 identity but supplies no better conflict or mission than the existing promotional copy, so it remains held.

Publisher and library namespace findings are based on short excerpts returned by the web search tool. They are explicitly distinguished from cached full source pages. The direct library download returned 403; prior failed distributor lookups are not relabeled as successful. These metadata references do not independently prove all target ISBNs or completeness. Original exact-ISBN descriptions remain the plot and membership evidence.

## Worker results and verification

Five cases completed without worker failures using five model requests in 35.24 worker seconds, excluding research/review. All 13 selected evidence quotes are literal source text. One unchanged acceptance out of five is 20% for this targeted development cohort. Codex performed the source assessment and revisions under user authorization; this is not independent gold adjudication or a general accuracy estimate.

The unchanged Strange Academy selection retains some publisher enthusiasm but clearly establishes the school, students and first-field-trip danger. The revised cases exposed four recurring limitations: missing setup, question-only selection without protagonists, unclear references to young heroes, and selection of damaged source punctuation when an intact equivalent exists. Publication of a revised draft is not evidence that Qwen solved its omission.

All 18 catalog tests passed. Production code, parser, prompt, model configuration and source eligibility rules did not change; previously passing publication lifecycle checks were not repeated. Packet, parent, prompt, frozen-code, downloaded-source and citation checks passed. Manual namespace holds were retained in the model packets and explicitly resolved after source review, rather than silently dropped before inference.

Only five intended enrichment records changed, limited to summary, synopsis-review provenance and source fields. Other records and fields were preserved. Exact backups and receipt hashes chain to the preceding eight-edition publication. The local site serves the exact staged bytes. No remote deployment occurred.

Artifacts are in data/local-ai-trials/namespace-recovery-six-20261031: selection.json, source acquisition audits/pages, individual distributor records, namespace-evidence.json, immutable packets/results/code, source-review.json, resolved-review-queue.json, delegated decisions, approved-staging, publish-receipt and verification.json. remaining-held.json holds the current 142-edition baseline remainder. selection-review-cases.json records these reviewed cases for future worker evaluation; it is development evidence, not an independent test set.

## Next step

Improve selection validation before another large enrichment batch. Use the preserved question-only, missing-subject, missing-setup and damaged-punctuation examples to test whether a change reduces editorial corrections while retaining good selections. Keep uncertainty preservation as a separate check, using the preceding Uncanny Avengers example. Do not interpret the five publications as five autonomous successes or loosen source/identity gates to raise throughput.
