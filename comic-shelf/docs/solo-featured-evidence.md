# Publisher story evidence — September 26, 2026

The collector now obtains issue-linked publisher descriptions without per-issue
plans or a search API key. This improves the evidence available for featured
stories; it does not yet establish complete story inventories or reading orders.

## What changed

`featured_sources.py` reads bounded feature blocks from public Marvel lists,
keeping each description attached to its own explicit series/year/issue heading
and issue link. Script/style content, unsafe URLs, duplicate identities, missing
descriptions and malformed blocks cannot become accepted automatic evidence.

Fantastic Four edition titles automatically select the publisher's
[Start Here: Fantastic Four](https://share.marvel.com/comics/discover/1233/start-here-fantastic-four)
page. Selection only identifies a candidate source: attachment requires an exact
match to an explicitly dated whole issue in the edition's collecting statement.
Partial material and identities inferred from bibliography alone are withheld.
Other supported feature lists may be supplied with `--featured-list`.

Results retain the description, identity quote, source URL, raw-page hash and scope
limitation in `featuredStoryEvidence`. These are publisher descriptions of featured
issues and may describe a wider arc. They are not automatically official story
titles, exhaustive issue story lists, or required reading. Feature-list position
is kept for provenance and never enters the reading-order adapter. Explicit
numbered-part excerpts can feed the existing separately validated local-model arc
stage; that branch has fixture coverage but no new positive live arc in this run.

Edition parser v12 also withholds a bibliographically inferred year when a fetched
publisher issue list presents the same title/number with a different year. It
retains both pieces of evidence and removes the disputed identity from automatic
issue research. It does not substitute the publisher year without establishing
the edition-to-series relationship. Explicit years in collecting statements are
not silently rewritten.

## Live development results

The page supplied 16 complete feature blocks with no parser problems. Four fresh
edition lookups completed without model-stage errors:

| Edition | New attached publisher description | Other outcome |
| --- | --- | --- |
| Ryan North vol. 1, 9781302524920 | Fantastic Four (2022) #1 | One description among six inventoried issues |
| Hickman Complete Collection vol. 1, 9781302510442 | Fantastic Four (1998) #570 | Other contents remain unresolved |
| Coming of Galactus, 9781302505332 | Fantastic Four (1961) #48 | Other contents remain unresolved |
| Secret Invasion: Fantastic Four, 9781302494971 | None | Disputed miniseries year withheld; three older Fantastic Four issues remain accepted |

No new official story titles or numbered arc parts were accepted. Description
coverage is counted separately from accepted title/part coverage. The final
two-book run repeated the positive Ryan North case and the year-conflict case
after correcting the diagnostic count to retain withheld conflicts.

This is development validation, not a blinded benchmark. Cases were chosen after
inspecting available publisher evidence. The named-story and full-scope gaps
remain; the collector is still not ready to claim complete unaided enrichment.

## Validation and preservation

155 targeted tests pass. New checks cover source-block boundaries, nested markup,
scripts, wrong years, partial issues, inferred identities, duplicates, unsafe
links, conflicting bibliographic years, and the separation of descriptions from
titles/order. Nine recorded live checks pass. Model/server settings were unchanged.

SHA-256 verification found no changes to 4,887 pre-existing public/data files.
Website data and all older trials are preserved. Audit files and original/final
script snapshots are in `data/local-ai-trials/solo-v5-validation`; live runs are
`solo-v5-featured-four` and `solo-v5-final-two`. `git diff --check` passed.

Direct issue-page probes returned Marvel 403, Marvel share 500, GCD 403 and
ComicBooks.com 410. The collector did not bypass those failures. Wider discovery,
edition-linked title/scope evidence and independent held-out scoring remain the
next requirements; characters remain secondary.

Reproduce with a fresh run name:

```powershell
python scripts/solo_enrich.py --isbn 9781302524920 --isbn 9781302494971 --refresh-edition --name NEW-UNIQUE-RUN
```
