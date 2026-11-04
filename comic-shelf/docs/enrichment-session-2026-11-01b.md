# Second long enrichment session — November 1, 2026

Published **36 reviewed synopses**, increasing the approved total from **158 to 194**. The session processed **100 new ISBN editions** through the local Qwen workflow. Ten publications use unchanged Qwen selections; 26 are explicit source-backed Codex revisions. The 36 additions include two source recoveries and two parser recoveries from this session's initially held editions.

| Work | New ISBNs | Published | Unchanged Qwen | Revised | Initially held |
| --- | ---: | ---: | ---: | ---: | ---: |
| First 25 | 25 | 12 | 3 | 9 | 13 |
| Second 25 | 25 | 8 | 1 | 7 | 17 |
| Third 25 | 25 | 6 | 3 | 3 | 19 |
| Fourth 25 | 25 | 6 | 2 | 4 | 19 |
| Source recovery | 0 | 2 | 1 | 1 | 0 |
| Parser recovery | 0 | 2 | 0 | 2 | 0 |

These are delegated Codex source/editorial assessments, not independent human gold labels or a general Qwen accuracy estimate. Unresolved editions were not uniformly graded for prose quality. Publication counts include revisions; source clearance is separate from model quality. The original single-pass sentence-selection prompt remains the default. No experimental rewrite, block-selection or self-audit policy was enabled.

## Evidence and source findings

Publisher issue and series metadata independently corroborated 2016 Infamous Iron Man, 2000 Ultimate Spider-Man, 2019 New Agents of Atlas, 2018 Asgardians, 2012 Avengers Arena, 2019 Target Vader, 2022 Halcyon Legacy, 2014 Superior Iron Man, 2022 Knights of X, 2001 Ultimate X-Men, 2015 Daredevil, 2018 Miles Morales, 2008 Marvel Zombies 3, 2009 Secret Warriors, 2018 Black Panther vs. Deadpool and 2018 Legion. These indexed excerpts corroborate namespaces only; the frozen exact-ISBN descriptions establish target edition membership. Reference URLs, retrieval limitations and hashes are recorded beside each resolved review queue.

Books of Doom remains held: its cached bibliography proposes 2024, but [Marvel lists the original Brubaker/Raimondi series as 2005–2006](https://www.marvel.com/comics/series/850/books_of_doom_2005_-_2006?byZone=marvel_site_zone). The reprint label was not treated as the original issue year.

Ten initial distributor ISBN lookups returned eight accepted records and two failed acquisitions. Runaways gained an explicit dated #1–6 collecting statement and a useful unchanged Qwen synopsis. Secret Warriors gained plot evidence instead of an issue-list-only source, then needed revision of a bare question into a neutral organizational mystery. The other fetched records did not justify source-recovery publication on their own: an ISBN match does not remove missing namespaces, malformed source text, conflicting metadata or partial-material requirements. Legion was later recovered from its original source through the parser fix. X-23, Wolverine: The Reckoning, Incredible Hercules, Master of Kung Fu and Loki remain held.

A separate eleventh distributor lookup for Secret Wars failed with HTTP 404; a direct Kobo download failed with HTTP 403. [Kobo's indexed exact-ISBN record](https://www.kobo.com/us/en/ebook/secret-wars-5) supplies a Battleworld premise and a partial FCBD bonus story, while the cached Google Books synopsis describes a different clandestine mission. [Marvel's original-series context](https://www.marvel.com/amp/articles/comics/a-traveler-s-guide-to-the-spider-verse?linkId=61074729) supports the integrity concern. The edition stays unpublished. No full-page parse is claimed for failed downloads, and inconsistent retail release dates were not used as original-series years.

Two art books were identified in the fresh sample and explicitly held for review appropriate to that book type. A Guardians of the Galaxy movie-art book has no existing enrichment record; the worker's selected comic-story setup was not published as an art-book description.

## Parser recovery

Parser version 24 preserves vs. inside collecting titles and recognizes a narrowly bounded malformed sentence boundary such as #1–5 .David Haller. Four regression tests cover literal evidence, missing years, decimals and variant suffixes. No dates or issue numbers are inferred. These fixes recovered Black Panther vs. Deadpool and Legion: Trauma for explicit source/namespace review and synopsis revision. Their original Qwen candidate inputs are exactly unchanged, so their immutable proposals were reused with zero new model requests.

The fixes were made after all inference runs. Every model run retains its version-23 frozen code archive and original source/result hashes. Replay of all 102 cases found changed inventories only for the two explicitly recovered editions; none of the 34 earlier publications is affected. Collecting lists with unknown years, unsupported fractions/decimals, unidentified one-shots, range disagreements and partial material remain blocked. An artificial leading And in some parsed series names remains a known issue in held editions and was not silently normalized.

## Runtime and verification

There were 102 worker executions: 100 new editions and two source retries. The worker logs contain 96 successful model responses, five cases with no eligible excerpts and one request ending in TimeoutError. The timeout case, X-Force by Benjamin Percy Vol. 7 (9781302526122), remains unpublished. It has no worker response/token log; none was fabricated. Its recorded case duration was 764.95 seconds. The cause is not established. The reconstructed input contains ten eligible excerpts, but that reconstruction is not a server request log.

Late investigation found the corresponding LM Studio server request with reasoning_effort set to none. The server reported 100% prompt processing at 20:12:04 local, then client disconnection at 20:24:42. At disconnection it logged a complete selection of E2, E4 and E9 with finish_reason stop and zero reasoning tokens; prompt/completion token counts are absent. The request body is truncated in the server log, so a full request hash cannot be verified from that log alone. The separately preserved timeout-server-evidence.json and timeout-recovered-draft.json retain this useful candidate for explicit identity/source/editorial review. The original failed result and worker_error publication hold remain unchanged. The 96 successful-worker-response metric excludes this cancellation-time server record; the 217-quote worker audit excludes its three separately verified literal quotations.

Total recorded worker time was 1,353.42 seconds; median case time was 6.07 seconds. The outlier must not be presented as normal throughput or attributed to context size, model behavior or server queueing without evidence. No automatic timeout retry ran.

All **370 Python tests**, **18 catalog tests** and whitespace checks passed. The audit verified 217 literal selected quotations, frozen source/code/prompt hashes, explicit review resolutions and exact source citations. Six additive publication receipts and one final wording correction form a consistent seven-receipt backup/hash chain. The correction tightens a Defenders sentence to avoid implying completed loss of territory or physical danger from bad press; it adds no new approval. A whole-session comparison proves that exactly 36 book records changed, limited to summary, sources and synopsis-review provenance. Other records, catalog fields and top-level enrichment metadata were preserved. The canonical overlay, public payload, built preview payload and actual local served bytes agree. Publication was to the local site; no remote deployment occurred.

The known reviewed held backlog is now **245 editions**: the previous 181 plus 64 new unresolved editions from this session. This is not the count of every unenriched book in the catalog. The automatic enrichment collector remains paused as it was at session start.

## Artifacts and next work

The aggregate artifacts are in data/local-ai-trials/timed-session-20261101b: final-verification.json, known-held.json, published-editions.json, latencies.json, timeout-note.json, backlog-summary.json and source-recovery records. The completion audit additionally verifies the final wording correction and writes completion.json and published-editions-final.json; the earlier aggregate audit is preserved as its checkpoint. Batch manifests and raw results are in sustained-25c/d/e/f-20261101; source retries are in sustained-recovery-two-20261101; parser recovery is in parser-recovery-b-20261101; the final wording package is final-wording-20261101. Each publication directory has exact rollback backups. A historical receipt must never overwrite a later publication.

Next useful work is targeted source recovery for held editions and investigating the isolated local inference timeout before unattended publishing. Keep book-type checks, source eligibility and model/editorial quality distinct. No model accuracy or review-effort savings claim follows from these publication counts.

The next-session research queue is saved in next-session-plan.json. A short final research pass found publisher corroboration for Dracula (2010) and Mighty Thor (2015), preserved in next-namespace-references.json. Both remain held for explicit synopsis review. In particular, [Marvel's Thor overview](https://www.marvel.com/amp/articles/comics/the-full-reading-order-of-jason-aaron-s-thor) confirms that the League material covers the opening part of Asgard/Shi'ar War, while the source lacks the later Shi'ar thread. Namespace corroboration alone must not clear that coverage gap.

## Published editions

| ISBN | Edition | Treatment |
| --- | --- | --- |
| 9781302535605 | Spider-Man Noir: The Gwen Stacy Affair: Issues #1-5 | Source-backed revision |
| 9781302499310 | Savage She-Hulk Masterworks Vol. 1: Issues #1-14 | Source-backed revision |
| 9781302510060 | Avengers by Jason Aaron Vol. 2: World Tour: Issues #7-12 | Source-backed revision |
| 9781302500962 | Infamous Iron Man Vol. 2: The Absolution Of Doom: Issues #7-12 | Source-backed revision |
| 9780785178712 | Ultimate Spider-Man Vol. 10: Hollywood: Issues #54-59 | Unchanged Qwen selection |
| 9781302938321 | Miles Morales: Ultimate End: Issues #1-12 | Source-backed revision |
| 9781302515560 | War of the Realms: New Agents of Atlas: Issues #1-4 | Source-backed revision |
| 9780785170198 | Captain America: The Death Of Captain America Vol. 2: The Burden Of Dreams: Issues #31-36 | Source-backed revision |
| 9781302510329 | Asgardians of the Galaxy Vol. 1: The Infinity Armada: Issues #1-5 | Source-backed revision |
| 9781302369880 | Avengers Arena Vol. 2: Game On: Issues #7-12 | Source-backed revision |
| 9781302519704 | Star Wars: Target Vader: Issues #1-6 | Unchanged Qwen selection |
| 9781302529987 | Invincible Iron Man By Gerry Duggan Vol. 3: Iron & Diamonds: Issues #13-20 | Unchanged Qwen selection |
| 9781302431457 | Daredevil: Cruel and Unusual: Issues #106-110 | Source-backed revision |
| 9781302944193 | Star Wars: The Halcyon Legacy: Issues #1-5 | Source-backed revision |
| 9781302497729 | Champions Vol. 1: Change The World: Issues #1-5 | Source-backed revision |
| 9781302518332 | Ironheart Vol. 2: Ten Rings: Issues #7-12 | Unchanged Qwen selection |
| 9781302501129 | X-Men Gold Vol. 2: Evil Empires: Issues #7-12 | Source-backed revision |
| 9781302482183 | Superior Iron Man Vol. 2: Stark Contrast: Issues #6-9 | Source-backed revision |
| 9781302504700 | Defenders Vol. 2: Kingpins of New York: Issues #6-10 | Source-backed revision |
| 9781302938208 | Avengers By Jason Aaron Vol. 8: Enter The Phoenix: Issues #39-45 | Source-backed revision |
| 9781302935313 | Ravencroft: Issues #1-5 | Unchanged Qwen selection |
| 9781302520564 | X-Men Milestones: Messiah War | Unchanged Qwen selection |
| 9781302938772 | Hellions By Zeb Wells Vol. 2: Issues #7-12 | Source-backed revision |
| 9781302944063 | Knights of X: Issues #1-5 | Source-backed revision |
| 9781302501808 | Fantastic Four by Mark Waid and Mike Wieringo: Ultimate Collection Book 4: Issues #514-524 | Source-backed revision |
| 9781302478681 | Ultimate X-Men Vol. 18: Apocalypse: Issues #89-93 | Unchanged Qwen selection |
| 9781302482473 | Doctor Strange: Don't Pay the Ferryman: Issues #75-81 | Source-backed revision |
| 9781302498856 | Daredevil: Back in Black Vol. 4: Identity: Issues #15-20 | Source-backed revision |
| 9781302515133 | Miles Morales Vol. 1: Straight Out of Brooklyn: Issues #1-6 | Unchanged Qwen selection |
| 9781302525781 | Venom by Al Ewing & Ram V Vol. 4: Illumination: Issues #16-20 | Source-backed revision |
| 9781302940478 | Wolverine by Claremont & Miller: Deluxe Edition | Source-backed revision |
| 9780785179559 | Marvel Zombies 3: Issues #1-4 | Unchanged Qwen selection |
| 9780785170884 | Runaways Vol. 1: Pride & Joy: Issues #1-6 | Unchanged Qwen selection |
| 9781302415303 | Secret Warriors Vol. 6: Wheels Within Wheels: Issues #25-28 | Source-backed revision |
| 9781302510251 | Black Panther Vs. Deadpool: Issues #1-5 | Source-backed revision |
| 9781302505097 | Legion: Trauma: Issues #1-5 | Source-backed revision |
