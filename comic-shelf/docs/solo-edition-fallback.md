# Automatic edition fallback and story highlights — September 26, 2026

The collector now recovers useful edition evidence when Google Books supplies no
accepted contents. It also selects cited story-premise excerpts from ISBN-matched
edition descriptions, including fallback sources. Website publication stays disabled.

## What changed

`overdrive_sources.py` performs a bounded public ISBN lookup. It first requests
OverDrive's public catalog search. If that resolves to one media page, it requests
the corresponding public library metadata page and verifies the ISBN in that exact
record's format identifiers. A search match alone is never identity proof.

The adapter saves both downloaded pages and an acquisition audit. It uses no login,
private API, embedded site credentials or user account. Hosts and routes are restricted,
redirects are checked, response sizes/timeouts are bounded, and ambiguous results
or mismatched records are withheld. HTTP 403/429/503 disables further fallback
lookups in the batch. This fallback currently depends on one public library catalog;
it is not universal OverDrive availability.

Fallback runs when the primary intake has no accepted inventory. It adds evidence
without discarding the original source or clearing an existing contents conflict.
New catalog/range conflicts also block inventory. A supplied series label can resolve
a yearless collecting entry provisionally, with field-level provenance; this remains
a draft bibliographic identity requiring review. It does not fill strict collection-
level whole-issue coverage.

The older narrative helper reads only the first source. A separate
`edition_highlights.py` stage now reads eligible ISBN-matched descriptions, reuses
the existing sentence/selection filters, and attaches exact source excerpts to model-
selected highlights. It neither rewrites those excerpts nor calls character extraction.
Highlights retain the actual source ID/URL and remain edition-level descriptions:
official story titles, covered-issue boundaries and complete story scope are unknown.
A highlight-stage failure preserves contents and other completed stages.

## Live development results

| Edition | Fallback | Accepted draft contents | New edition highlights |
| --- | --- | ---: | ---: |
| Civil War: Front Line Complete Collection, 9781302518585 | Exact ISBN record accepted | 11 issues, previously none | 1 from fallback |
| Civil War: Amazing Spider-Man, 9780785170259 | Search did not resolve uniquely | 0; original range conflict preserved | 1 from primary description |
| Fantastic Four by Ryan North vol. 1, 9781302524920 | Not needed | 6 issues | 1 from primary description |

The [public Front Line record](https://knoxcounty.overdrive.com/media/8771024)
supplied its collecting statement and series label. All eleven draft issue identities
matched the existing publisher event list. Their bibliographic identity remains
review-gated, so this is not eleven independently verified full-path placements.

All three final runs completed without model-stage errors. Each new highlight is an
exact source excerpt; none has an invented official title or assigned issue scope.
The excerpts vary in usefulness: the Spider-Man selection is a broad personal-decision
premise, not a detailed story inventory. Three highlights do not establish three
distinct complete stories or adequate recall of everything contained in these editions.

No search API key was required. A Google Books API probe returned HTTP 429 and was
not added as a live dependency. The supported fallback uses public catalog pages.

## Validation and preservation

181 targeted tests pass, including ISBN/media mismatches, ambiguous searches,
unsupported redirects, failed downloads, source-conflict retention, unknown/repeated
model evidence IDs, contents-only abstention and isolated highlight-stage failure.
Nine recorded live checks pass. These are development checks, not a blinded
independently adjudicated accuracy benchmark.

SHA-256 checks found no changes to 5,080 pre-existing public/data files. Earlier trials,
website data and model/server settings were preserved. `git diff --check` passed.

Runs and audit files under `data/local-ai-trials/`:

- `solo-v7-overdrive-two`: first fallback-positive and conflict-negative checks.
- `solo-v7-final-three`: fallback plus the new highlight stage.
- `solo-v7-validation`: raw source probes, preservation hashes, checks and script snapshots.

Remaining requirements are wider fallback coverage, stronger series-identity evidence,
official story titles and boundaries, required/optional reading distinctions, and the
independent reading-path benchmark. The system is more useful for unattended draft
collection; complete unaided enrichment is still unproven.

Example (choose a new unique run name):

```powershell
python scripts/solo_enrich.py --isbn 9781302518585 --isbn 9780785170259 --isbn 9781302524920 --refresh-edition --name NEW-UNIQUE-RUN
```
