# Fresh-source validation: Vision and Annihilation — 2026-09-27

**Decision: the collector is not ready for unaided complete enrichment.** The
fresh sample recovered only 2–3 of 12 annotated premise facts per repetition and
18 of 47 reference inventory units. Correct abstention prevented unsupported
completeness claims, but did not supply the missing reading order or story scope.

This is the first six-edition slice of the larger independent-validation plan.
It uses two paths not previously found in saved trial records, with reference
labels frozen before model inference. It is **provisional source research by one
assistant, not independent human adjudication**, and does not complete the planned
30-edition/six-path benchmark. No extractor changes were made during this test.

## What was tested

Three Vision editions test a short numbered run and a reprint/overlap problem.
Three Annihilation books test a multi-series event, abbreviated titles, missing
years, a prologue, and an ancillary handbook. There are 47 edition-specific
narrative issue units in the reference inventory, counting repeated/reprinted
editions separately. The two reference paths contain 12 and 29 unique original
issue nodes respectively. These are different denominators for different tasks.

The pipeline acquired fresh Google Books pages by ISBN, then used its existing
OverDrive fallback condition for editions without accepted inventory. The final
packets and TOC supplements were frozen and hashed. Unchanged extraction stages
ran sequentially three times with Qwen3.5-4B. Research references, expected
inventories and benchmark answers were not passed to inference. No live retrieval
occurred during inference; this is not a full live autonomous-search benchmark.

The evaluation separately checks exact series/year/issue inventory, twelve
predeclared premise facts, three provisional scope anchors and available path
evidence. Empty inventories count as zero recall, wrong years cannot match, and
duplicate ranges cannot inflate coverage. Exact quote grounding is reported
separately from premise recovery. Gold inventory and premise definitions were not
changed after seeing outputs.

## Results

All 18 edition attempts completed without a stage exception. This operational
success is not semantic success.

| Metric | Repetition 1 | Repetition 2 | Repetition 3 |
| --- | --- | --- | --- |
| Correct draft inventory units / reference units | 18/47 | 18/47 | 18/47 |
| Correct / all emitted inventory units | 18/18 | 18/18 | 18/18 |
| Fully recovered annotated premise facts | 2/12 | 3/12 | 3/12 |
| Exact-source highlights / emitted highlights | 11/11 | 12/12 | 12/12 |
| Recovered provisional scope anchors | 0/3 | 0/3 | 0/3 |
| False completeness claims | 0 | 0 | 0 |

The inventory score includes twelve correctly inferred units still flagged for
bibliographic identity review. Only six units were accepted without that flag.
The conservative gates are doing useful work, but 100% precision on a small
withheld subset is not complete collection. The 47-unit denominator excludes the
ancillary handbook and does not claim an exhaustive inventory of extras.

Premise recovery uses fixed term combinations in exact selected excerpts. It is
a conservative check for the annotated complete facts, not a human semantic score
or exhaustive assessment of every useful statement. For example, the Vision
wife-killing fact also asks for the concealment; a quote mentioning only the
killing receives no full-fact credit. Drax mentoring Nova is a useful selected
premise outside the twelve annotated facts and must not be called false merely
because it is absent from the labels. No same-model critic graded the outputs.

Manual inspection confirms substantial quality problems behind the low score:

- Vision volume one selects context fragments, including "There, he builds them."
  It does not clearly communicate the creation of the family.
- Vision volume two selects the wife's killing but omits the protection/lie and
  ensuing Avengers confrontation.
- Annihilation book two misses the Silver Surfer and Ronan premises. The second
  and third repetitions additionally recover the Super-Skrull fight; the first
  selects promotional creator framing instead. Temperature zero was not stable.
- The complete Vision edition remains withheld because the catalog's original
  numbering and the description's Director's Cut numbering conflict. The needed
  reprint relation cannot safely be guessed.
- Annihilation books one and two have unresolved series identities; book three
  accepts the six main-series issues but leaves Heralds of Galactus unresolved.

No reading paths were produced. The configured source registry returns no lists
for these editions, no search key was present, and research-only reference paths
were intentionally not supplied as collector answers. Thus **order accuracy and
mandatory prerequisite accuracy are unmeasured**, rather than falsely reported
as 0% or 100%. Inventories contain 12/12 Vision reference nodes and 6/29
Annihilation reference nodes before strict identity-review exclusions; neither
number establishes a recovered reading order.

The three missing scope anchors were absent from the input packets: this is a
retrieval-coverage failure. The model was correct not to invent their names or
boundaries. Broad required/optional classification remains unadjudicated, so it
cannot earn a completeness pass. The fresh result does not invalidate the earlier
7/7 on its tuned set; it shows that result did not generalize to these books.

## Reference basis and uncertainties

| Edition ISBN | Provisional narrative inventory | Reference basis |
| --- | --- | --- |
| 9781302488703 | Vision (2015) #1–6 | [ISBN-matched library metadata](https://ppld.overdrive.com/media/4455726) |
| 9781302494711 | Vision (2015) #7–12 | [ISBN-matched library metadata](https://lfpl.overdrive.com/media/5884902) |
| 9781302502072 | Vision Director's Cut (2017) #1–6 | [ISBN-specific bibliography](https://books.google.com/books/about/Vision.html?hl=en&id=uF47DwAAQBAJ&output=html_text); original-issue conversion remains incomplete |
| 9781302484576 | Drax the Destroyer (2005) #1–4; Annihilation Prologue (2006) #1; Annihilation: Nova (2006) #1–4 | [ISBN-specific contents](https://glllibraries.overdrive.com/media/4455429), with separately researched series identities |
| 9780785182856 | Annihilation: Silver Surfer, Super-Skrull and Ronan (all 2006), #1–4 each | [ISBN-specific full series names](https://lancasteruniversity.overdrive.com/media/5901805) |
| 9780785182849 | Annihilation (2006) #1–6; Annihilation: Heralds of Galactus (2007) #1–2 | [ISBN-specific contents](https://www.kobo.com/ww/en/ebook/annihilation-book-three); handbook tracked separately |

[Marvel's Annihilation omnibus listing](https://www.marvel.com/comics/collection/97245/)
corroborates the event's series identities and years. It is not used as proof that
a different edition contains every omnibus item. Independent hosts often repeat
the same publisher copy; that is not independent authorship or human review.

[Marvel's Vision series page](https://www.marvel.com/comics/series/20897/vision_2015_-_present)
establishes the twelve-issue run. Ascending issue-number order is a provisional
run-order annotation, not an independently established in-universe chronology or
proof of no outside prerequisites. The Annihilation reference follows sections
5.2–5.3 of [Marvel Guides' recommended order](https://marvelguides.com/annihilation-reading-order).
It does not label every tie-in universally mandatory or establish all acceptable
alternative interleavings.

The scope anchors are deliberately separate from prose highlights:

- [Director's Cut #1](https://www.marvel.com/comics/issue/62998) explicitly reprints
  Vision (2015) #1–2 plus extras. This does not authorize an automatic one-to-one
  mapping of all reprints to originals.
- Two issue-title anchors, for Vision #7 and #12, come from the
  [secondary issue-title table](https://en.wikipedia.org/wiki/Vision_%282015_comic_book%29).
  They remain provisional until checked against the issues themselves.

Those three anchors are absent from the collector's supplied evidence, so failure
to recover them is an evidence-coverage gap, not a model extraction error. Some
Marvel pages returned 403 during research; indexed passages were used only as
research references, never mislabeled as freshly fetched collector evidence.

## How to inspect or adjudicate

The audit directory is `data/local-ai-trials/holdout-v1-validation`.
`reference.json` contains the pre-inference annotations; `freeze.json` pins the
source packets and collector scripts. `run_frozen.py` never reads the gold file.
The raw results and attempts are in `holdout-v1-frozen-six`.
`score_frozen.py` evaluates the completed run and writes `scores.json` once.

`reviewer-a.json` and `reviewer-b.json` are **unfilled** independent review forms.
They let reviewers record inventories, featured stories, boundaries, required
nodes, dependencies, alternatives and evidence before adjudication. Their presence
does not mean two reviewers have approved the reference answers.

Once these failures are used to guide patches, the cases become development cases.
They must not be called an untouched holdout in later comparisons. Reserve other
entire reading paths for the next test rather than tuning to these six editions
and reporting their improvement as catalog-wide accuracy.

## Next work and preservation

Prioritize retrieving exact series identities and reprint relationships, then
source-backed issue/story boundaries and path discovery. Preserve multi-sentence
context when selecting premises. Do not optimize another seven-fact score as a
substitute for those capabilities. Any patch informed by this sample needs a new
held-out path for evaluation. Human adjudication and the remaining 24 editions
and four paths in the proposed benchmark are still outstanding.

SHA-256 checks found no changes to 5322 pre-existing public/data files,
all frozen collector scripts, input packets or reference labels. Three scorer
sanity checks passed. All attempts, source packets and scores were preserved in
new folders. Website data and prior trials remain unchanged.
