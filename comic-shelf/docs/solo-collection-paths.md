# Cross-edition reading-path collection — September 26, 2026

The collector now produces `collection-paths.json` for each batch with publisher
reading-list sources. It maps source issues across all supplied edition drafts,
preserving issue sequence, edition alternatives, overlapping book spans, partial
material, unresolved identities and missing evidence. It never writes website data.

## Capabilities and limits

- Each publisher-list node carries its matching editions and their inventory
  evidence. Accepted story titles, numbered parts and publisher descriptions stay
  attached to their matching issue; they do not leak into adjacent issues.
- Unique issue coverage does not increase when two editions contain the same
  material. Both editions remain visible as alternatives.
- Overlapping edition spans warn that sorting whole volumes cannot reproduce the
  publisher's issue sequence. The report does not invent mandatory dependencies.
- Partial issues and bibliographically inferred series years do not fill whole-issue
  gaps in this collection-level report. Older per-edition placement counts include
  draft bibliographic matches, so those counts are not interchangeable.
- Issues collected in supplied editions but absent from the publisher list are
  explicitly retained in `editionIssuesOutsideSource`. They may be unrelated extras
  or list omissions; event membership and required reading are not inferred.
- Full coverage of the supplied list is distinct from a complete reading order.
  `completeReadingOrder`, `requiredReadingEstablished` and publication eligibility
  remain false. The evaluated scope is the supplied editions, not the entire shelf.

## Broader development checks

Nine distinct editions were exercised across three live batches, including repeated
checks after fixes (13 book attempts). All produced drafts without model-stage
errors, but draft completion does not mean that usable contents were found.

The three-edition Civil War batch covered 10 unique issues out of 98 publisher-listed
nodes. Seven positions had alternative editions; 88 positions remained uncovered.
The Captain America issues occurred inside the main book's span of source positions,
showing why a whole-volume sequence would be misleading.

Six further tie-in editions exposed separate failure modes:

- Front Line Complete Collection supplied ISBN metadata but no contents description.
  Intake now creates an explicit edition-contents research task.
- Civil War: Amazing Spider-Man has a catalog/source issue-range disagreement.
  Its inventory remains withheld, now with an explicit contents-conflict diagnostic.
- Secret Invasion: X-Men joined its collecting statement and synopsis as
  `#1-4.The...`. Parser v13 recognizes this narrow sentence-boundary case while
  continuing to withhold unsupported decimal issues and variant suffixes.

The X-Men case exposed a source-list gap as well: the downloaded Secret Invasion
page listed #1, #3 and #4, while the edition's collecting range was #1-4. The final
report retains #2 outside the source list. Its bibliographically inferred year
still requires review; recovering a range does not establish series identity.

No new named-story titles were acquired in this iteration. This round improved
reading-path assembly, contents intake and visibility of missing evidence. It does
not resolve the remaining title/scope retrieval or independent accuracy requirements.

## Validation and preservation

167 targeted tests pass. Replay of 115 stored packets removed no previously accepted
inventory entries; two packets gained the missing-space contents extraction. These
are stored packets, including repeated editions, not independent accuracy cases.

Nine final recorded checks pass. An initial check incorrectly expected four X-Men
candidate nodes in the publisher list; the failed check is preserved, and the
corrected report explicitly exposes the omitted node. This is development analysis,
not a blinded or independently adjudicated benchmark.

SHA-256 checks found no changes to 4,953 pre-existing public/data files. Website data,
earlier trials and model/server settings were preserved. `git diff --check` passed.

Artifacts under `data/local-ai-trials/`:

- `solo-v6-civil-three`: live edition alternatives and overlapping book spans.
- `solo-v6-tieins-six`: broader live source-coverage observations.
- `solo-v6-final-four`: live checks after contents/diagnostic changes.
- `solo-v6-validation/final-replay`: final collection report replayed from saved live
  inputs, including issues absent from the publisher list; input/code hashes recorded.
- `solo-v6-validation`: original/final scripts, original failed check, final checks,
  inventory replay and preservation hashes.

The collector is increasingly useful for unattended draft collection with explicit
gaps. Complete unaided enrichment still needs broader evidence discovery, reliable
edition-to-series identity, story scope, required/optional distinctions and the
independent path-level benchmark described in the reassessment document.

Example (use a fresh run name):

```powershell
python scripts/solo_enrich.py --isbn 9780785170242 --isbn 9780785178088 --isbn 9781302532567 --refresh-edition --name NEW-UNIQUE-RUN
```
