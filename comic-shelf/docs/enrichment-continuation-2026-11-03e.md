# Source recovery and prospective input comparison — November 3, 2026, fifth block

Published **one unchanged Qwen synopsis**, increasing the local approved total from **339 to 340**. A prospective five-edition comparison found two gains in available plot coverage, two coverage tradeoffs and one appropriate abstention under both policies. No comparison output became a clean unchanged synopsis, so the production word allowance remains 60. The experiment had one rejected harness request, corrected transparently without rerunning completed outputs.

## Unchanged selection published

New X-Men by Grant Morrison Vol. 2: Imperial (9780785170853) previously lacked collecting evidence. A guarded exact-ISBN public-library lookup supplied New X-Men (2001) #118–126, agreeing with the catalog range and old bibliographic label. The new source was appended to a new packet; the original packet and output remain preserved.

Qwen’s selected overview passed delegated review unchanged. It names the X-Men and mutant-grafting threat, covers Cyclops/Jean Grey and Professor X’s predicament, and adds John Sublime/U-Men and the return of an unidentified villain. It does not identify that villain from memory, supply a successful resolution or include creator advertising. The omitted new-Angel introduction is a cast teaser rather than a separate described mission. This is a central overview, not a claim that every chapter is indexed.

The recovery made one successful model request in 6.48 seconds and selected three literal quotations. Guarded staging/publication, exact backups, source/parent hashes, preserved prior approvals and actual HTTP-served bytes verified. The known production-review backlog decreased from **425 to 424**. This one editing-free recovery is a useful observation, not evidence of a general model-quality gain.

Siege: Embedded (9780785147640) had a failed exact-ISBN lookup. The downloaded search page, failure audit and hash are attached to its backlog entry so the same lookup is not repeated blindly. Both acquisition audits and every downloaded page hash passed closing checks. No collecting statement was inferred from the title alone.

## Prospective comparison design

Before reviewing any model outputs, selected five input-affected editions absent from this project’s prior frozen model inputs. The scan used a fixed seed over 2,839 unused cached ISBNs and found the first five affected cases after examining 1,732. This stopping rule does not estimate prevalence across the whole catalog. Prior-input exclusion was rechecked at assessment: 888 prior input ISBNs, with none of these five among them.

Each case compared the production 60-word candidate allowance with 90 words. The 450-character bound, exact source bytes, original prompt, three selected IDs, temperature zero, thinking off and 200-token response budget stayed fixed. All baseline candidates remain in the treatment; candidate IDs may shift when a passage is inserted. Policy order alternates across cases. The manifest, candidate inputs, source/cache hashes and generic editorial rubric were saved before inference. The same source and inventory limits apply regardless of text quality.

| Previously unused case | Result | Editorial interpretation |
| --- | --- | --- |
| Sgt. Fury: Berlin Breakout | Longer input restores Fury/Commandos and WWII missions | Trades away the eyepatch/Dum Dum selection and still misses the Korean War thread |
| Ultimates: Homeland Security | Default has no candidates; longer input exposes the whole plot passage | Useful input coverage, but damaged possessives/grammar and unclear team reference need editing |
| Art of Marvel Studios: Thor | Both policies abstain | Correct abstention on film casting/director promotion; art-book format is not a comic-story synopsis |
| Mighty Avengers by Dan Slott | Longer input adds roster and Chthon/Cabal/Unspoken | Drops team-formation context and the later Loki/Siege/Ultron thread |
| Phases of the Moon Knight | Longer input restores other-era anthology scope | Creator advertising and reader hype remain |

The comparison therefore has two coverage gains requiring editing, two mixed tradeoffs, and one unchanged appropriate abstention. It has zero clean unchanged synopses under either policy. An abstention on promotion is a correct behavior, not a failed draft. Publication/edition approval was not granted for any comparison case, and those five remain in a separate research queue rather than being silently added to the production-review backlog or published.

## Harness error and exact request counts

The initial isolated runner attempted a request whose candidate enum was empty. The local server rejected it with HTTP 400. Production correctly skips inference when there are no eligible excerpts; the runner was corrected to do the same. The rejected request, original runner, stderr, completed responses and error audit remain saved. The resumed runner reuses completed results and issues no repeated inference for them.

Ten policy outcomes completed: **eight successful model responses** and **two no-call abstentions**. There was **one rejected harness request**, for nine HTTP attempts in the comparison. The eight successful responses took 35.39 seconds and selected eight literal quotes. Every request body, source quote, response schema, stop reason, packet/cache hash and frozen script hash passed verification. The no-call baseline outcomes are explicitly marked and are not counted as successful model responses.

Across recovery and comparison work there were nine successful responses, eleven literal selected quotes, two no-call abstentions and one rejected harness request. The production recovery worker had zero failures. The failed comparison request is not hidden inside a zero-failures claim. Production code and settings are unchanged; no new unit-test run is claimed for this artifact/data-only block. Prior validation remains 385 Python tests and 18 catalog tests.

## Working decision and handoff

Keep the 60-word production default. The prospective sample confirms that the word filter can hide useful plot evidence, but more candidate text does not establish less editing: the selector can replace setup or another thread with the new long passage. The five-case study is small, uses cached descriptions, alternates order without repeated requests, and relies on delegated Codex judgments rather than independent gold labels. It does not support a general accuracy claim or autonomous publication.

Prioritize evidence recovery and edition review. Next exact-ISBN source candidates are Ultimate X-Men Vol. 3: World Tour and Venom vs. Carnage, both lacking inventory evidence; recheck history before lookup. Preserve Siege’s newly failed lookup and earlier failed attempts. The five prospective packets/results are saved for separate edition/source review; do not rerun the same experiment without a concrete new mechanism to test.

Artifacts are in data/local-ai-trials/continued-20261103e and source-recovery-one-20261103e. The continuation folder contains the prospective manifest, original and corrected runner, rejected request/error audit, exact requests/responses, assessment, source-audit verification, final-verification.json, known-held.json and next-session-priorities.json. Earlier approvals, the initialized Atlantis Rising record and unrelated metadata remain intact. Public, built and actually served data agree at 340 approved synopses. The collector remains paused; no remote deployment occurred.
