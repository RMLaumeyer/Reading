# Local AI trial

## Latest validation — September 21, 2026

### Full version 18 benchmark: regression found

`trial-18-full` completed all ten attempts in **551.13 seconds (9m 11s)**:
**eight drafts and two errors**, versus ten drafts in the earlier version 14 run.
The script and model configuration were held fixed throughout this run.

- Ben Reilly failed primary extraction: Qwen joined J.M. DeMatteis across a
  sentence split and cited a fragment that did not contain the full name.
- Civil War failed primary extraction: Qwen expanded source text Peter into
  unsupported Peter Parker. The correction attempt repeated the error.
- Smack to the Future completed but incorrectly accepted Peter David and Will
  Sliney as characters from a creatively worded creator credit. This is a semantic
  regression even though its quotes are exact.

The other completed drafts preserve the targeted synopsis/contents improvements.
There are seven summaries, seven books with issue ranges and eight page counts
when retained partial results are included. Complete drafts alone contain six
issue lists and seven page counts. No reviews or reading-order guidance were
established. Both known edition conflicts remain gated; the contents-only book
abstains on narrative fields. Alias/group identity ambiguity remains.

All 56 offline tests still pass, and revalidation found zero citation/schema/fact
gate errors in saved accepted fields. This does **not** invalidate the live
failures or the creator-role error: the suite has missing semantic coverage.
Do not use this version for unattended enrichment. Prioritize literal-name
generation/claim isolation, initials-aware sentence splitting and broader creator
credit handling before another full benchmark.

Detailed assessment: `data/local-ai-trials/trial-18-full/assessment.md` and
`assessment.json`. No website data changed; Qwen remains running. The run time is
descriptive, not a controlled speed comparison.

### Version 18: character mentions and suggestion role checks

Primary extraction now explicitly covers named people mentioned in backstory,
comparisons and final clauses, even when they are not the current protagonist.
Reports define character scope as explicit source mentions, **not verified on-page
appearances**. This does not infer aliases or continuity.

Suggestions now pass through the same creator/location quarantine as primary
extraction. Candidate scanning strips creator-role prefixes and compares Unicode
apostrophe variants consistently, avoiding redundant suggestions.

The first live Pools of Blood run recovered Peter Parker but also admitted
descriptive phrases. A subsequent conservative quarantine withholds lowercase
labels, generic plural role labels and standalone family-role words for review.
For example, web-head, Marvel's silver-screen icons, Mercs and Daughter are
withheld with their original evidence. This is a heuristic: unusual legitimate
names can be withheld, so rejected claims remain available for human review.

**56 offline tests pass.** Tests cover deliberately misclassified creator/place
suggestions, Unicode deduplication and descriptive labels versus named people and
teams. A ten-book offline replay of current normalization/quarantine on saved
version 14 claims preserves other accepted names and withholds the same five
known role errors: `data/local-ai-trials/role-replay-v18.json`.

The initial live experiments are retained for diagnosis: Pools of Blood
(`trial-18-9781302964924`, 57.12 seconds) exposed the descriptive-label regression;
End of the Spider-Verse (`trial-18-9781302524692`, 84.67 seconds) preserved its five
names, Shathra synopsis and creator/location exclusions. Both started before the
final descriptive-label filter was added.

Final live run `trial-18-final-9781302964924` completed in **61.98 seconds** with
no citation errors or audit warnings. Peter Parker is now in primary extraction;
Daughter, Mercs, Marvel's silver-screen icons and web-head are withheld with
evidence. Ten mention labels remain, not ten verified distinct identities:
Miles/Miles Morales is flagged, and Deadpools/group identities still need review.
The complete assignment synopsis and both supported issue ranges are preserved.
This is targeted validation, not a fresh ten-book model benchmark. No model
settings or website data changed; the existing model server remains running.

### Version 17: resilient optional auditing and cleaner name suggestions

Three concrete defects from the preceding results/code review are fixed:

- A malformed response or connection failure in the optional character coverage
  audit no longer discards the already validated primary extraction. A visible
  `quality.auditWarnings` entry records the failed check. Primary extraction
  failures still fail the stage, and normal role quarantine still runs.
- Possible first-name aliases exclude conjunction/group phrases. Deadpool is no
  longer flagged as a possible short form of Deadpool & Daughter. Peter/Peter
  Parker remains a review candidate; no identity merging is performed.
- Sentence-start contractions are excluded from candidate names: It's Spidey
  becomes Spidey, including the curly-apostrophe spelling. Original supporting
  quotes remain unchanged. Invalid audit suggestions are never exposed as accepted
  suggestions before their validation succeeds.

**53 offline tests pass**, including malformed/connection-failure recovery,
primary-stage failure propagation, group-name exclusions and contraction handling.
These changes improve reliability and review quality; they do not establish
complete character coverage or resolve missing review/reading-order evidence.

The existing Qwen3.5-4B server was already running on port 1234 with an 8192-token
context. No model settings were changed.

Fresh end-to-end run `trial-17-9781302964924` completed in **60.89 seconds**
with no citation errors. It retains both whole-issue ranges and the complete
Deadpool & Daughter assignment synopsis. The false group-name alias flag is gone;
seven primary names remain, with Peter Parker, Deadpools, Miles and Mercs left as
unapplied suggestions. This does not establish complete or correct entity coverage.
The optional audit completed normally in this live run. A separate offline
malformed-response injection retained all eight names from the prior saved primary
extraction and recorded a warning:
`data/local-ai-trials/audit-failure-replay-v17.json`.
This is one targeted live test, not a full ten-book rerun or a controlled speed
comparison. The already-running model server was left running.

### Version 16: specific remaining defects and implemented fixes

| Observed defect | Implemented fix | Validation |
| --- | --- | --- |
| Article/case/apostrophe variants create duplicate character names. | Normalize surface forms and merge their evidence; retain short/full names separately with possible-alias flags. | Regression covers the Hobgoblin/Hobgoblin, curly apostrophes and Peter/Peter Parker. |
| A longer teaser can still displace a useful plot sentence. | Rank eligible source passages for concrete threats/actions/missions; penalize generic teasers and hype. Copy selected text verbatim. | Regression uses the actual Shathra sentence that describes her attack on Peter and Ezekiel. This is a relevance heuristic, not a fact checker. |
| Whole ranges disappear in mixed-series or hashless COLLECTING lists. | Parse each explicitly named series/year/range, retain exact source evidence, omit partial-story material and entries without years. | Offline replay increases books with supported ranges from 3/10 to 7/10, retaining both known conflict abstentions. |
| Empty fields hide whether evidence is missing or a stage failed. | Save per-field draft/withheld/not-completed states with reasons, possible aliases, suggestions and withheld names. | Conflict, missing-evidence and unfinished-stage regression tests. |
| Failure of a later stage hides successful earlier work. | Save completed fields as partialResult on failure. | CLI regression fails the review stage and verifies the earlier page count survives. |
| A cast above ten can fail final schema validation. | Allow up to thirty aggregated character names without silently truncating. | Twelve-character regression. |
| Sentence splitting at `vs.` clips the Pools of Blood synopsis. | Preserve common internal abbreviations such as vs., Dr. and Mr. while keeping exact source text. | Regression checks complete original sentences and their citations. |

**49 offline tests pass.** The deterministic replay is saved in
`data/local-ai-trials/contents-audit-v16.json`. It validates bibliography against
the ten cached source packets; it is not a fresh ten-book model benchmark.

Three fresh end-to-end Qwen runs completed with no citation errors:

| Run | Seconds | Manually checked result |
| --- | ---: | --- |
| trial-16-9781302524692 | 62.55 | Concrete Shathra synopsis replaces vague Morlun teaser; Peter/Peter Parker flagged; creator/location exclusions preserved. |
| trial-16-9781302527327 | 135.31 | All nine extracted names retained; Hobgoblin and Cape Killers normalized; concrete attack synopsis selected. |
| trial-16-9781302964924 | 133.25 | Miles Morales #30-31 and Deadpool #11-12 recovered with exact evidence; partial Annual story omitted. Exposed the abbreviation boundary bug subsequently fixed above. |

The third full-run artifact intentionally preserves the original clipped passage
as diagnostic evidence. A fresh summary/story-stage retest of the boundary fix is
saved separately as
`data/local-ai-trials/trial-16-9781302964924/sentence-boundary-retest.json`.
This focused retest reuses the preceding run's extracted character names.
It completed in 9.78 seconds with no citation errors, selecting the complete
"Deadpool & Daughter embark on their first major assignment: to take out
Spider-Man!" passage for summary and story highlight. The earlier pronoun filter
excludes the repaired "It's Spidey vs." sentence; it no longer admits its clipped
second half as standalone prose. The API server was stopped after validation to
restore its initial state. Website data and model settings remain unchanged.

Identity aliases, absent source evidence, ambiguous review matching and independent
source discovery remain unresolved. All output is a draft requiring review.
No model or LM Studio settings changes are required for these script fixes.

### Version 15: source-role checks and fuller summary passages

**40 offline tests pass.** After extraction, names with setting/organization suffixes
or explicit creator/location cues in the source are withheld for role review.
Examples include `-Verse`, `Industries`, `writer NAME`, `artist NAME` and
`faraway NAME`. This uses source wording rather than a hand-written comics roster.
Each withheld claim and supporting role clue is preserved in raw output and listed
in the comparison report. These conservative rules may withhold a legitimate
character with an unusual name/role; they are not a complete entity classifier.

Summary selection prefers a passage of at least 12 words when one exists, while
retaining shorter passages if that is all the evidence offers. First-name surface
forms may help select relevant passages, but are never merged into identities.
Prose remains verbatim source excerpts. Longer passages are not automatically
better summaries, and the script does not claim semantic approval.

Validation consisted of an offline replay across all ten version 14 drafts and
three fresh live tests, **not a fresh ten-book version 15 run**. The replay withheld
all five observed role errors and retained the other previously accepted names.
Audit: `data/local-ai-trials/role-audit-v15.json`.

| Fresh run | Seconds | Manually checked result |
| --- | ---: | --- |
| trial-15-9781302532260 | 141.64 | Wakanda withheld; Miles Morales, Black Panther, Spider-Man, T'Challa, Bast and Spidey retained. Source-based ritual/Bast summary preserved. |
| trial-15-9781302532956 | 86.88 | Spider-Verse withheld; nine character names retained and origin synopsis preserved. |
| trial-15-9781302524692 | 90.53 | Spider-Verse, Dan Slott and Mark Bagley withheld. Morlun, Peter Parker, Shathra, Peter and Ezekiel retained. Summary now uses a longer source sentence, but remains vague. |

Total fresh inference time: 319.05 seconds. Remaining limitations include missing
characters, aliases such as Peter/Peter Parker, unhelpful teaser selection,
ambiguous review matching and absent reading-order evidence. Website data remains
unchanged. The local API server was restarted for the tests and stopped afterward
to restore its prior state; model/settings were not changed.

### Completed full benchmark: versions 13 and 14

The earlier full version 14 run completed **10/10 drafts in 756.58 seconds**
(12m 37s), improving on version 13's six drafts/four errors in 825.11 seconds.
It produced nine source-based summaries, eight page counts, three simple issue
lists, and no review scores or reading guidance. The contents-only book correctly
abstained on narrative enrichment. Draft status does not establish correctness.

Version 14 fixed the character-list overflow regression by saving extra names as
unapplied review suggestions, improved apostrophe/conjunction handling, and filtered
creator credits/damaged text from prose selection. It still admitted the role
errors addressed in version 15. Detailed manual assessment:
`data/local-ai-trials/trial-14-full/assessment.md`.

The current scope is assisted enrichment from fixed cached sources. It is not
ready for automatic catalog publication or independent source discovery.

### Version 12: deterministic bibliography and second-book validation

**31 offline tests pass.** Contents/pages now come from conservative exact-source
parsing, without a model request. This fixes a newly observed version 11 failure:
on the Ben Reilly control book, Qwen invented `contentsConflict=true` despite the
input explicitly being false, and withheld supported issues/pages. Conflict gates
still take precedence. Page counts require an exact ISBN match and one unique
positive length in the bibliographic section. Whole-issue parsing accepts only
an explicit standalone `Collects Series (year) #range` clause; partial material and
more complex listings abstain rather than being guessed. Absence of a detected
conflict is not proof that an edition match is correct.

The offline audit of all ten packets preserved both conflicts, obtained page
counts for the other eight, and accepted three simple whole-issue ranges. The
remaining five non-conflict books have contents left for more capable parsing or
manual review. Saved audit: `data/local-ai-trials/structured-audit-v12.json`.

| Live test | Seconds | Result |
| --- | ---: | --- |
| trial-11-conflict | 41.70 | Source-excerpt mode recovered Aunt May; disputed contents/pages/review withheld. |
| trial-11-control | 143.53 | Ben Reilly source selection worked, but model invented a metadata conflict. |
| trial-12-control | 30.16 | Ben Reilly (2022) #1–5 and 112 pages correctly extracted; ambiguous review withheld. |

Manual review of the latest control: the selected summary accurately quotes the
source's mystery involving a figure from Ben's past and Ravencroft. It does not
invent an answer to the source's question. Limitations remain: character extraction
returned only Ben Reilly despite other named mentions, one highlight includes
creator credits and a cached encoding error, and the passages are not polished
original prose. The conflict-book selection also favors some minor publisher-copy
details. Two live books are not full-benchmark validation. No website data was
changed; no settings or model downloads were needed.

### Version 11: source-excerpt baseline and character coverage

The CLI now defaults to `--narrative-mode extractive`: Qwen selects at most one
source sentence per summary/highlight, and Python copies it verbatim. It does not
ask Qwen to rewrite these passages. Reports label this mode explicitly; these are
source excerpts, not original synopses or official arc names. The experimental
generated-prose pipeline remains available with `--narrative-mode paraphrase`.
The mode is included in the saved run metadata and resume fingerprint.

Extractive-mode character extraction requires a name list for every source
excerpt. The script checks literal name support, combines duplicate names and
attaches citations itself. Missing excerpt keys, invented aliases, and exceeding
the character limit trigger bounded correction or rejection. This improves
coverage but does not prove each named person appears in the book, resolve
identities, or guarantee that Qwen distinguishes creators from characters.

**28 offline tests pass**, including exact source copying, prevention of combining
two excerpts into a new claim, recovery from a missing final excerpt, and rejection
of unsupported aliases. A pronoun-start filter reduces contextless prose choices;
it is a conservative heuristic, not a full discourse parser.

`trial-11-conflict` completed ISBN 9781302515041 in **41.70 seconds**. It retained
Spider-Man, Peter Parker and Aunt May, kept the conflict-dependent fields empty,
and introduced no new wording into the summary/highlights. Selection quality is
still limited: it chose publisher jokes about villains/property damage/rent rather
than the central threat. This is a more faithful but less polished baseline, not
automatic approval for website publication. LM Studio settings are unchanged.

### Version 10: evidence selection and claim review

The paraphrase pipeline selects evidence before writing narrative claims. Each writing
request sees only the selected group, then a separate local Qwen request checks
each claim against its own citations. Unsupported/uncertain judgments trigger the
single bounded repair attempt. Malformed/missing judgments fail closed. Claims
also have deterministic word limits and character names must occur in their cited
text. Review requests, judgments and selection responses are saved with the run.

Narrative excerpts now preserve sentence boundaries instead of splitting at 20
words. Evidence allows up to 60 words / 450 characters; longer sentences are
omitted rather than truncated. This can reduce coverage, and punctuation-based
sentence splitting is imperfect, particularly around abbreviations. A conservative
best/worst/greatest/biggest-ever pattern excludes obvious publisher superlatives
from prose selection but not character extraction. It is not a general sarcasm
detector. No LM Studio settings were changed.

Validation: **23 offline tests pass**. Excerpts for all ten cached books match
their source text and satisfy the new limits. A four-case live reviewer probe
rejected invented threat scope and chronology while accepting two supported
claims (`data/local-ai-trials/support-probe-v8.json`). This small probe does not
establish reviewer reliability.

Live results for the same Friendly Neighborhood Spider-Man conflict book:

| Run | Seconds | Finding |
| --- | ---: | --- |
| trial-08-single | 96.36 | Stopped on unsupported story claims after correction. |
| trial-09-single | 176.50 | Evidence-first generation shortened claims, but promotional rhetoric and truncated citations still misled the model. |
| trial-10-single | 196.09 | Full-sentence evidence removed the universe-threatening exaggeration; kept disputed contents/pages/review withheld. |

**Version 10 still requires manual review.** The summary says Peter is uncovering
Aunt May's secret, whereas the cited source only says she has a secret; Qwen's
reviewer missed that added action. Aunt May is absent from the character output,
and two highlights are vague descriptions of repairs/groceries. The draft remains
unpublished. A same-model reviewer is a useful filter, not independent factual
verification. Next evaluate stricter one-premise generation or explicitly labeled
source-excerpt output, and test on additional books rather than tuning indefinitely
on this one. None of these runs establishes full-benchmark quality.

### Earlier version 7 result

Version 7 (`trial-07-single`) completed the same conflict book in **75.12 seconds**,
versus 361.33 seconds for version 5. No LM Studio settings were changed: the loaded
model is `qwen3.5-4b`, context 8192, and the script requests temperature 0 and
`reasoning_effort: none`. Existing settings are sufficient for the current test.

Changes since version 5:
- Narrative tasks receive numbered short excerpts, with bibliography and collecting
  sentences excluded. The model selects IDs; the script restores exact quotes.
- Known contents conflicts deterministically withhold issues/pages/reviews without
  inference. A conservative prose gate also rejects issue/page/contents claims
  during a conflict; it is not a general semantic contradiction detector.
- Characters, story highlights, and summary/reading advice have separate stages.
- Corrective retries retain the previous response when bounded in size and ask
  for targeted repairs. List claims require at least one evidence ID.
- Stage progress is printed, and the run metadata includes the script version.

Fifteen offline tests pass. All generated excerpts across the ten cached books
passed quote/length checks. Replaying the version 5 draft now rejects its disputed
contents in the summary. Version 6 took 75.22 seconds and recovered three character
names but no story highlights. Version 7 recovered Spider-Man, Peter Parker, Aunt
May, and three story highlights, with no disputed issue numbers in its prose.
Spider-Man and Peter Parker are separate extracted names, not distinct identities.

**Manual review: still unsuitable for publication.** Version 7's summary invents a
"universe-threatening" threat, although the source describes a threat to Spider-Man
and his neighbors. It also turns promotional worst/best-neighbor rhetoric into a
temporal progression. Story highlights are repetitive and include details not
supported by their selected quotes. Valid evidence IDs establish source existence,
not semantic support. The next quality improvement should constrain each generated
claim to its selected evidence and evaluate that support independently. These are
single-book results, not a successful full benchmark. Website data is unchanged.

### Earlier version 5 result

Version 5 clarified that contents conflicts block issues/pages/reviews, while the
synopsis and explicitly named characters remain usable. It also requested shorter
verbatim evidence quotes. All eight offline guardrail tests passed.

`trial-05-single` retried ISBN 9781302515041 with local `qwen3.5-4b` in 361.33
seconds, compared with 238.98 seconds for `trial-04-single`. It produced a summary
but still returned no characters or story highlights after corrective retries.
Issues, pages and review correctly remained empty/null. However, the summary
asserted the disputed #1–5 contents: the field-specific conflict validator does
not catch contents claims embedded in prose. Passing structural/evidence checks
therefore did not make this draft acceptable. No website data was changed.

Those contents/evidence handling changes are included above; semantic accuracy
remains the limiting factor.

This is an isolated ten-book experiment. It does not change your website, overwrite enrichment, install software, download a model, or start itself.

First live test (September 15, 2026): `trial-01` stopped on its first book after 386.55 seconds because the model used all 3,500 output tokens for reasoning and returned no final answer. Version 2 requests `reasoning_effort: none`; a small probe confirmed this works with the installed Qwen3.5-4B. The revised `trial-02` produced its first draft in 108.2 seconds, with evidence-length violations and incomplete enrichment that require review. The ten-book trial was then continuing; see the saved reports for its latest progress. Existing website data is untouched.

## What the first experiment measures

The script supplies saved publisher metadata and, where available, cached Comic Book Roundup trade rows to a local model. The selection includes alternate identities, two Spider-Man 2099 series, conflicting contents, partial annuals and crossovers. The local model does not receive our completed annotations. Those are frozen separately as a comparison baseline when a run begins.

This first experiment tests evidence interpretation, not independent web research. Sources are curated, may be stale, and may omit facts in our existing annotations. Abstaining because a source is missing is appropriate. A successful result would justify adding a separate public-source discovery/fetching stage; this version cannot yet research unfinished books end to end.

## Before we test together

The existing LM Studio installation has Qwen3.5-4B loaded at an 8192-token context,
using about 3.38 GB according to `lms ps`. Its API endpoint is
`http://127.0.0.1:1234/v1`. Keep that setup for these tests. If local API
authentication is enabled, set `LOCAL_AI_TOKEN` in the current terminal.

We have not installed LM Studio or downloaded a model as part of this change. Do not run the commands below until you want to start testing.

## Commands for later

Version 18 uses six stages (contents/pages, reviews, characters, story highlights,
summary, and reading advice). Extractive mode selects/copies narrative passages;
paraphrase mode also generates and reviews prose. Each generation has at most one
corrective retry. Contents/pages are parsed deterministically in both modes.
Attempts and validation failures are retained. Thinking is disabled.

Catalog-versus-synopsis range conflicts are detected before inference. Detected conflicts require empty issue lists and null page/review claims. Bibliographic page counts require an exact ISBN match. Review HTML is parsed into separately labeled critic/user fields with trade titles and issue counts; unfamiliar markup yields no usable rows. Numeric review claims must match a cited row, with conservative title/count checks. These checks intentionally abstain on ambiguous matches and do not establish full semantic correctness or detect every possible edition conflict.

Fifty-six offline tests cover suggestion role checks, descriptive labels, Unicode deduplication,
optional-audit failure recovery, group-name alias exclusions,
contraction handling, abbreviation boundaries, name normalization, partial-result recovery, field-quality reporting,
mixed-series parsing, source-role quarantine, summary selection, candidate suggestions,
deterministic bibliography, conflicts, partial material, review scores,
evidence selection/copying, character coverage, claim isolation, support-review
failures, complete evidence sentences, promotional filtering, and bounded retries.

To retry the previously failing book, use a fresh folder name:

```powershell
python scripts/local_ai_trial.py run --model "qwen3.5-4b" --name trial-18-repeat --isbn 9781302515041 --narrative-mode extractive
```

Run from `comic-shelf`. `python` means an available Python 3 interpreter; this project also has the bundled interpreter at `C:/Users/rmlau/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.

```powershell
# Checks source files and lists local model IDs; no inference or model download.
python scripts/local_ai_trial.py preflight

# Replace the model ID with the exact ID from preflight.
python scripts/local_ai_trial.py run --model "MODEL-ID" --name trial-01

# Resume after correcting an error. Completed drafts are preserved.
python scripts/local_ai_trial.py run --model "MODEL-ID" --name trial-01 --retry-errors

# Rebuild the comparison report without contacting the model.
python scripts/local_ai_trial.py report --name trial-01
```

For another model or changed inputs, use a new name, such as `trial-02`. Resume rejects changes to model, prompt, schema, sources or configuration. Requests go only to the local server; proxies and redirects are disabled. One book runs at a time with a ten-minute request timeout. Errors stop the batch and are saved. Ctrl+C interrupts; rerunning resumes at the unfinished book. Alternatively create `data/local-ai-trials/trial-01/STOP` to stop between books, and remove it before resuming.

## Results and interpretation

All outputs live outside the served website, under `data/local-ai-trials/<name>/`:

- `run.json`: model and experiment fingerprint.
- `reference-private.json`: frozen comparison answers; never sent to the model.
- `<isbn>-sources.json`: exact input evidence packet and cache hashes.
- `<isbn>.json`: raw response, parsed draft, elapsed time, errors and evidence checks.
- `comparison.md`: side-by-side summaries, storylines, pages, reading advice and reviews, plus a human review checklist.
- `comparison.json`: exact character/issue agreement counts and differences.

The script validates output shape and checks whether cited quotes exist in the supplied sources. That does **not** prove that a quote supports a claim. It does not automatically grade prose, treat every baseline fact as truth, or promote any result to verified enrichment. Character aliases can cause exact-string mismatches. Review dates and missing sources can also explain differences. Our final assessment needs to examine those differences, not just a single score.

If output is truncated or the model rejects structured JSON, the trial stops with an error. We should tune the model/context/output settings before retrying rather than accepting incomplete research.

API implementation references: [LM Studio structured output](https://lmstudio.ai/docs/developer/openai-compat/structured-output) and [local server quickstart](https://lmstudio.ai/docs/developer/rest/quickstart).
