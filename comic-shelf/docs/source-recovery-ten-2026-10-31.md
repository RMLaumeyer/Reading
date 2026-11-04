# Ten-edition source recovery — October 31, 2026

Researched ten previously held editions, retried eight with improved evidence, and published eight reviewed synopses to the local site. Four Qwen selections were accepted unchanged; four required source-backed Codex revisions. The approved synopsis overlay now contains 112 editions. Of the original 166 held editions, 147 remain unpublished after this and the preceding recovery pass.

This is a targeted development cohort assessed by Codex under the user's publication authorization. The 50% unchanged acceptance rate is descriptive of these eight retries, not an independent accuracy estimate or evidence of improved autonomous model performance. No production parser, prompt, model configuration or source filter changed.

## Results

| ISBN | Edition | Outcome |
| --- | --- | --- |
| 9780785179719 | Deadpool Vol. 6: I Rule, You Suck | Revised to include the separate Draculas job |
| 9781302386498 | Daredevil by Mark Waid Vol. 7 | Revised to restore the enemy and justice-system conflict |
| 9781302434120 | Fear Itself: The Fearless | Unchanged Qwen selection |
| 9781302479831 | Avengers West Coast: Vision Quest | Held; series-name reconciliation needed, no new model call |
| 9781302480332 | Figment | Unchanged Qwen selection |
| 9781302488611 | Spider-Woman: Baby Talk | Unchanged Qwen selection |
| 9781302493424 | Uncanny Avengers: Unity Vol. 2 | Revised to preserve uncertainty about Hank Pym's control of Ultron |
| 9781302498955 | Monsters Unleashed | Held; distinguish the 2017 event from the 2017B ongoing run, no new model call |
| 9781302502522 | All-New Wolverine: Orphans of X | Unchanged Qwen selection; concise central mission, no complete subplot claim |
| 9781302516475 | Star Wars: Galaxy's Edge | Revised to restore the outpost and Dok-Ondar context |

Qwen used the original sentence-selection policy, qwen3.5-4b, temperature zero and thinking off. Across eight unique retried editions there were nine worker case executions and eight actual model requests, with zero worker failures. The initial Deadpool case made no request because the source filter excluded the supplementary Rakuten record. A separate immutable retry promoted the validated exact-ISBN record to primary input and retained the original dated Google collecting statement as a second source. Both raw outcomes remain preserved. No source was mislabeled as OverDrive and no production allowlist was broadened.

The workers took 52.42 seconds in total, excluding research and editorial review. All 16 selected evidence quotations are literal source text. The four revisions are explicitly attributed to Codex and are not counted as unchanged model accepts.

## Source evidence and limits

Three aggregate OverDrive acquisitions succeeded: Daredevil, Uncanny Avengers and All-New Wolverine. Daredevil gained plot text where the old source contained only a collecting statement. Its distributor description explicitly dates the original series to 2011. Uncanny Avengers likewise has an explicit dated collecting statement. All-New Wolverine's separate exact-ISBN distributor record corroborates the original bibliographic year and matching issue range.

Figment's first distributor record validated the exact ISBN, series year and #1–5 range; a second candidate returned 404. The valid cached record was assessed individually. The failed aggregate acquisition remains failed, and agreement with the unavailable duplicate is not claimed.

Deadpool gained its missing plot from the [exact-ISBN Rakuten Kobo publisher description](https://books.rakuten.co.jp/rk/57f7c51809f23a519062bf202bd38d75/). The page's product identifier matches the requested ISBN. Its yearless #27–31 collecting statement matches the original exact-ISBN source's explicitly dated Deadpool (2008) #27–31. That is a manual resolution for this edition only; the parser still reports the yearless supplementary entry as unresolved in the raw result.

Three namespace reviews use short publisher excerpts returned by web search: [Fear Itself: The Fearless (2011) #1](https://www.marvel.com/comics/issue/39953/fear_itself_the_fearless_2011_1), [Spider-Woman: Baby Talk's dated collecting statement](https://www.marvel.com/comics/collection/55977/spider-woman_shifting_gears_vol_1_-_baby_talk_2016), and [Star Wars: Galaxy's Edge (2019) #1](https://www.marvel.com/comics/issue/75139/star_wars_galaxys_edge_2019_1). Direct publisher page downloads returned 403, including attempts through the web reader. The short indexed excerpts and failed download audits are recorded separately. These excerpts corroborate the original series namespace; they do not establish the target ISBN, membership or completeness. Those remain grounded in the original exact-ISBN collecting statements. Publisher issue descriptions were not substituted for edition synopses.

Vision Quest remains held because the [publisher reading list](https://www.marvel.com/comics/guides/2047/vision-quest/) calls the run West Coast Avengers, while the original edition metadata calls it Avengers West Coast. No global name alias or expansion to the event list was added. Monsters Unleashed remains held because the publisher distinguishes the [2017 event collection](https://www.marvel.com/comics/collection/63379/monsters_unleashed_monster-size_trade_paperback) from the [2017B Monster Mash collection](https://www.marvel.com/comics/collection/56273/monsters_unleashed_vol_1_monster_mash_tpb_2017_1). Their shared year and numbering alone do not justify merging them.

## Publication verification

All 18 publication lifecycle tests and 18 catalog tests passed. Packet, parent-packet, actual prompt, frozen code and downloaded-source hashes passed verification. No production code changed, so the previous parser suite was not repeated.

Only eight intended book records changed, and only summary, synopsis-review provenance and source fields changed within those records. Existing approved overlays and editorial synopses were not overwritten. Issue inventories, borrowing availability and reading-order information were preserved. Exact backups and final hashes passed; localhost:5173/enrichment.json serves the exact staged bytes. Publication is local; no remote deployment occurred.

The previous receipt's canonical overlay hash chains directly into this promotion. The public and built enrichment payloads had a top-level updatedAt change between turns, from 2026-09-15 to 2026-10-31. Verification confirmed that every other field, including all book records, was identical. The newer timestamp was preserved and the metadata transition is recorded explicitly, rather than claiming an uninterrupted byte-identical chain for those files.

Artifacts are in data/local-ai-trials/source-recovery-ten-20261031: selection.json, downloaded research and audits, publisher-reference-excerpts.json, frozen packets/code, raw results, source-review.json, resolved-review-queue.json, immutable delegated decisions, approved-staging, publish-receipt, preflight-verification.json and final verification.json. The separate Deadpool retry is in data/local-ai-trials/source-recovery-deadpool-followup-20261031. remaining-held.json contains the updated baseline remainder of 147 editions.

## Next priorities

Resolve Vision Quest's series-name relationship with explicit publisher evidence. For Monsters Unleashed, seek an exact-edition record that identifies which 2017 run is collected. More generally, prioritize unresolved source inventories before spending further model calls on unchanged packets. Keep unchanged Qwen acceptance, editorial revision, source-adapter failures and held research outcomes separate in future batch reports.
