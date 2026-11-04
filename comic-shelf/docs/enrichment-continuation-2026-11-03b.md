# Qwen review-check improvement and source recovery — November 3, 2026, second block

Added a production review warning for selected drafts that begin with a referential pronoun after omitting earlier source context. Published one source-recovered synopsis, increasing the local approved total from **324 to 325**. The known reviewed backlog decreased from **415 to 414**. This block improves review coverage; it does not demonstrate improved Qwen writing or independent publication ability.

## Worker improvement

The sentence selector can choose a grammatically intact quotation that begins “For if he…” or “Yet her…” while leaving out the source passage identifying the person and situation. The new opening_reference_requires_context_review warning surfaces that pattern and includes up to 600 characters of literal earlier source context. It only examines the first selected passage, requires earlier non-contents source text from the same source, and excludes self-introductions such as “Her name is Janet…” and hyphenated names such as He-Man and She-Hulk. It does not claim to resolve pronouns or detect every missing premise.

The warning reaches the review queue and blocks staging while unresolved, including attempts to accept or revise a draft without resolving the queue flag. It does not change Qwen’s prompt, inputs, chosen passages, output, evidence or inventory. It does not rewrite text, infer identities or automatically approve any result. The renderer distinguishes earlier context from the existing immediate-following-qualifier warnings. Reviewers must still assess the full source.

## Validation

All **377 Python tests** and **18 catalog tests** passed. Five new worker tests exercise skipped setup, intact setup, self-introductions, contents-only prefixes, same-source boundaries, hyphenated names and unchanged proposal export. The existing staging integration test now also confirms that both accept and revise actions cannot bypass this new unresolved flag.

Replayed **963 saved result/packet pairs** against the captured baseline worker and final worker. The final rule adds **19 warnings for 19 ISBNs**, including the prior Black Bolt and Mighty Thor context omissions. All prior review reasons remain. Proposed synopses, evidence, full descriptions and omitted-passage lists are identical. Canonical/public publication files were byte-identical during replay. Three packet/result pairs without a synopsis or book were explicitly excluded and listed in the replay artifact.

The initial broader rule produced 24 warnings. Inspecting those results exposed avoidable warnings on named self-introductions and contents-only prefixes. The narrowed rule excludes five of those cases. Both replay artifacts are preserved. This is development on saved data, not an untouched evaluation set, independent gold labeling or an accuracy/recall estimate. The new live recovery did not trigger the warning; no prospective model-quality gain is claimed.

Parser version 25 and the original three-passage selection policy remain unchanged. Changes are limited to enrichment_worker.py and its worker/staging tests. Their exact before/after hashes and a focused diff are saved. The publication run was prepared after these changes and froze all 78 current Python scripts.

## Source recovery and publication

Used the tested acquisition-history helper for two previously untried ISBNs. All-New X-Men Vol. 3: Out of Their Depth gained a validated exact-ISBN OverDrive description with actual plot, where its old record supplied only #11–15. Spider-Man/Doctor Octopus: Negative Exposure’s lookup failed; its audit and downloaded search page are saved and attached to the backlog so the same lookup is not repeated blindly. The first invocation of each stopped before any network access because the archive parent directory was missing; creating the parent fixed that invocation issue. The actual acquisition outcomes remain one accepted and one failed.

The All-New X-Men recovery made **one Qwen request**, completing in **7.88 seconds** with no worker failure and **two literal selected quotes**. Both exact-ISBN sources label the original series 2012 and collect #11–15. [Marvel’s original #11](https://www.marvel.com/comics/issue/43476/all-new_x-men_2012_11) confirms that namespace, Bendis/Immonen and the Jean Grey/defection premise. The explicit review resolves synopsis-only identity checking; no years, aliases, issue keys or order metadata were published.

Qwen’s recovered draft covers the main setup and defection. A source-backed editorial revision removes promotional comparisons and tightens the prose: the time-displaced young X-Men adjust to the present; Jean Grey pushes her powers; one member leaves to join adult Cyclops. The departing member stays unnamed because the source does not identify them. No subsequent outcome is invented.

Guarded staging and publication passed: exact backups, packet/source/parent hashes, frozen scripts, prompt and finish reason, citations and the actual HTTP-served payload all agree. Only the intended record’s summary/source/review fields changed. Earlier approvals, unrelated fields and top-level metadata were preserved. The local total is **325**. The legacy collector remains paused and no remote deployment occurred.

## Atlantis Rising: reviewed proposal remains held

Resolved the three undated series identities for synopsis review using [Marvel’s Namor namespace](https://www.marvel.com/comics/collection/37393/namor_visionaries_by_john_byrne_vol_1_trade_paperback), [the 1995 Atlantis Rising series](https://www.marvel.com/comics/series/23531/fantastic_four%3A_atlantis_rising_%281995_-_present%29) and [Fantastic Four Unlimited #11 in the 1993 series](https://www.marvel.com/comics/series/23532/fantastic_four_unlimited_%281993_-_present%29). The target’s intact ISBN source supplies its own membership and plot. Other-format descriptions and supplemental material were not transferred. Raw inventory remains unchanged; the assessment does not claim complete chapter coverage or publish issue metadata.

Reviewed the existing saved Qwen draft and prepared a source-backed correction restoring Morgan Le Fay’s raising of Atlantis and the resulting crisis. No repeated inference was needed. Staging then correctly excluded it with missing_existing_enrichment: its catalog ID has no base enrichment object for this patch-only publication path to update. The first staging assertion expected a change and failed; the saved package itself correctly contains zero changes. The proposal, decision, source assessment, zero-change package and separate verification remain preserved. There is no publication receipt and this book remains in the held backlog.

Creating a supported, auditable base enrichment record is now a concrete next task. It needs a guarded initialization path that preserves catalog identity and other records; bypassing the existing staging rule would hide the missing-record problem. Historical approval of the proposed wording alone is not publication eligibility.

## Handoff

Current artifacts are in data/local-ai-trials/continued-20261103b, source-recovery-one-20261103b and namespace-review-atlantis-20261103b. The new source candidate is Daredevil: Hell to Pay Vol. 1 (9781302431693): it currently has only a no_synopsis hold and no prior acquisition audit was found. Recheck history before lookup. Negative Exposure, Deadpool Classic Vol. 8 and Winter Soldier retain failed lookup histories. Darth Vader’s namespace review remains separate and unresolved.

Prioritize the guarded missing-record initialization path and source recovery before another bulk batch. For model development, the remaining challenge is complete setup and distinct-thread coverage; this new warning detects one bounded symptom and does not solve that challenge.
