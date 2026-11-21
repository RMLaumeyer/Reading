# Panel — your local Marvel shelf

Double-click **Start Panel.cmd** in the Reading folder. It opens http://localhost:5173/ in your browser. Double-click **Stop Panel.cmd** to stop the local server. Closing the browser leaves the small server running; restarting Windows stops it. Nothing is hosted publicly.

## What is ready

- **Expanded event timelines (November 6, 2026):** the event index now has 11 routes. New additions are the full Krakoa era (38 selected stages through the collected June 2024 conclusion), Annihilation, Annihilation: Conquest, War of Kings → Realm of Kings → The Thanos Imperative, House of M/Decimation → the Messiah trilogy, and Secret Invasion → Dark Reign → Siege. The index searches event names and chapter/character text. Story arc filters on longer routes isolate periods such as Dawn of X, Fall of X, or Realm of Kings, and related-route links connect the larger sagas. Every match remains a supplied-catalog snapshot; the Krakoa route flags the unconfirmed Immortal X-Men #6 collection and the Messiah route flags two incomplete Cable bridges.

- **Event timelines:** `/event-timelines/` adds Hickman’s Avengers/New Avengers → Infinity → Time Runs Out → Secret Wars (2015), the original Infinity Gauntlet, Avengers vs. X-Men, Civil War and Civil War II. Routes mark Core, Recommended and Optional stages, distinguish setup/main event/aftermath, show expandable issue-order blocks and cross-reference exact catalog ISBNs. The routes are selective, not exhaustive tie-in checklists. Print matches are labeled separately from Hoopla listings. Run `npm run timelines:build` to validate/generate/copy pages and `npm run timelines:test` to check renderer filters and key ordering cases.
- **New character/team guides:** Shadowcat (Kitty/Kate Pryde), Fantastic Four, and Agents of S.H.I.E.L.D. bring the index to 31 pages. The S.H.I.E.L.D. guide distinguishes TV-inspired comics from TV continuity and wider Fury/Hickman background. New research is dated October 30, 2026; older guides preserve their own dates.

- **Team and character guide index:** `/reading-guides/` now links 28 guides, including Avengers, X-Men, twelve Avengers members, eleven X-Men members, Moon Knight, Black Knight, and Spider-Man. The 196 page-level selections include 181 with catalog matches (shared stories can occur on multiple guides). Search the index by character or team. Each guide has publication chronology, starting points, source links, catalog links, identity/continuity labels, and partial/overlapping-collection notes. This is a curated member set, not a measured popularity ranking.

Guide JSON is the source of truth. Run `npm run guides:build` after editing it to validate ISBNs, ordering, evidence references and anchors, regenerate the HTML index/pages, and copy guide assets into the local static build if present. Run `npm run guides:test` for renderer/filter checks across every guide. The guide build does not rewrite the catalog or enrichment records. The source shelf header and the saved home page link to the guide index.

- **Spider-Man reading guide:** open `/reading-guides/spider-man.html` or use the header link. It contains 24 curated starting points/key stories in original publication order, 19 with exact-ISBN Hoopla-listed catalog matches and five with no confirmed match. Continuity labels, source links, edition-overlap notes, and availability/starting-point filters are included. Research is dated October 27, 2026; borrowing status remains the imported catalog snapshot. Guide data and assets live in `public/reading-guides/` and copy into static builds.

- All 4,000 imported catalog records are searchable. The default availability filter includes the 3,948 explicitly listing Hoopla; 52 are retained as unconfirmed.
- The **Enriched pilot** contains 26 books: Moon Knight, Spider-Man, and one X-Men collection. Each has a short original synopsis, named storylines, page count, a reading path, source links, and an exact Hoopla title link extracted from OCLS.
- 18 pilot collections have Comic Book Roundup critic and reader scores where available. Missing scores are not zeros; sorting places them last.
- Character filters combine title matches with appearances supported by the pilot sources. **Sourced appearances only** excludes unverified title matches. This is not yet an exhaustive appearance or cameo index for 4,000 books.
- Reading order groups books within runs. Complete collections are marked as alternatives, and overlapping issues are shown in book details. Starting-point suggestions are editorial recommendations, not externally scored rankings.

## Data limits

The export is a snapshot, not live borrowing availability and not proof that every Marvel title at OCLS is included. Grouped catalog records can represent multiple editions. ISBNs remain strings. Review matches use title, creators, series, and collected issues, rather than an exact digital ISBN. Critic aggregates cover the issues reviewed by Comic Book Roundup and can omit annuals or bonus material. The review detail panel states this explicitly.

Page counts come from ISBN-matched Google Books bibliographic records; a platform may count covers, advertisements, and bonus pages differently. Dates in the CSV describe catalog editions rather than original story chronology. The Hunted publisher listing has a supplemental-issue suffix discrepancy, which is noted and excluded from overlap indexing.

All catalog and enrichment JSON is stored locally. Browsing and sorting do not call data APIs. Covers are loaded from Google Books or Comic Book Roundup, so cover images and external borrowing/review links require internet access. No paid API, model, subscription, or API key is used. No library credentials are stored.

## Maintenance

Source CSVs in the parent folder remain unchanged. `public/catalog.json` is rebuilt by `scripts/import_catalog.py`. `data/pilot.json` identifies the pilot ISBNs; `scripts/build_pilot.py` contains explicit editorial annotations and produces `public/enrichment.json` plus `data/audit.json`.

The collection scripts cache public HTML in ignored `data/cache/`. OCLS requests are spaced at least 20 seconds apart according to its crawl policy. Requests to restricted endpoints are not used. Review matching is explicitly recorded in `data/review-matches.json`; there is no indiscriminate full-site crawler or automatic background refresh.

To rebuild with installed tools:

```text
python scripts/import_catalog.py
python scripts/build_pilot.py
npm run build
npm start
```

Python scripts use only the standard library. The launcher uses the bundled Node runtime if available, falling back to a system Node installation. Node 22.13 or newer is required for development. The saved app uses a zero-dependency Node static server bound to 127.0.0.1; it exposes only `dist/client`, with no write routes.

The build command includes a Windows-only one-second graceful-exit shim for Vinext's native bundler teardown. It does not suppress nonzero exit codes or build errors.

## Validation

`npm test` checks reconciliation, source coverage, missing-value sorting, appearance matching outside titles, edition overlap, and reading order. `npm run typecheck` checks TypeScript. Production HTTP checks verify the saved page, data files, and browser asset references. Browser interaction and visual testing were not requested and have not been performed. An optional WebMCP search tool is feature-detected; no supported validation context was available, so that tool is not claimed as tested.

The next expansion is metadata enrichment beyond the pilot, especially Avengers/X-Men appearance mapping and more review matches. Unknown data is deliberately left unfilled until verified.
# Bulk enrichment

Double-click `Enrich Panel.cmd` in the parent Reading folder to start or resume the free ISBN metadata pass. It processes the 967 Spider-Man, Moon Knight, Avengers, and X-Men title matches first, then the rest of the 4,000-record catalog. Keep the computer awake and online. The full pass can take several hours; each new request waits at least three seconds. `Pause Enrichment.cmd` stops after the current request. Starting twice does not create competing workers.

Panel refreshes enrichment and progress every 15 seconds. **Basic metadata** means an exact ISBN match with any available page count, cover, and short publisher excerpt linked to the full synopsis. It does not mean that story arcs, character appearances, reviews, or reading order have been checked. The 26 editorial pilot records retain their fuller annotations and take precedence over automatic data. Missing ISBN matches and errors are recorded separately; no scores or reading-order steps are invented.

Progress lives in `data/enrichment-progress.json`; automatic records live in `data/automatic-enrichment.json`. Public metadata is updated as each record finishes, so no rebuild is required. HTTP 401/403/429 or a traffic challenge pauses the pass. Resume later instead of bypassing a source restriction. To retry previously unmatched or failed records manually, run `python scripts/enrich_catalog.py --retry` after the current pass has stopped. Cached pages are reused.

Validation for this extension: `python scripts/test_enrichment.py`, `npm test`, `npm run typecheck`, and `npm run build`. Browser interactions have not been tested.

## Personal reading queue

Use Reading status on shelf cards, book details, guide matches, or event timeline matches to choose Want to read, Reading, or Finished. Choose Not in queue to remove an edition. The shelf queue filter includes saved editions regardless of enrichment or availability; other search filters can then narrow them. Continue reading opens books marked Reading, most recently updated first.

Progress is stored in this browser on this device and shared across tabs at the same Panel address. Use the same hostname and browser profile each time. Clearing browser site data removes progress. Storage errors are shown without claiming a successful save. Run `node scripts/test_reading_queue.mjs` to check persistence and storage failure handling.
