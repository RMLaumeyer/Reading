'use client';
import { useEffect, useMemo, useState } from 'react';
import { flushSync } from 'react-dom';
import EnrichmentControls from './enrichment-controls';
import {
  BookOpen,
  Search,
  ArrowUpRight,
  Library,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  SlidersHorizontal,
  Check,
  Layers,
  Route,
  Star,
  Info,
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet';
import { Checkbox } from '@/components/ui/checkbox';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Book,
  Enrichment,
  Filters,
  initialFilters,
  filterBooks,
  matchesCharacter,
  overlaps,
  sortOptions,
} from '@/lib/catalog';
function Choice({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: readonly (readonly [string, string])[];
  onChange: (v: string) => void;
}) {
  return (
    <div className="filter-choice">
      <label>{label}</label>
      <Select
        value={value}
        onValueChange={(v) => {
          if (v !== null) onChange(v);
        }}
      >
        <SelectTrigger aria-label={label}>
          <SelectValue>
            {options.find((o) => o[0] === value)?.[1] ?? value}
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {options.map(([key, name]) => (
            <SelectItem key={key} value={key}>
              {name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
function Cover({ book, large = false }: { book: Book; large?: boolean }) {
  const [broken, setBroken] = useState(false);
  return (
    <div className={`cover ${large ? 'cover-large' : ''}`}>
      {book.detail?.coverUrl && !broken ? (
        <img
          src={book.detail.coverUrl}
          alt={`Cover of ${book.title}`}
          loading="lazy"
          referrerPolicy="no-referrer"
          onError={() => setBroken(true)}
        />
      ) : (
        <div className="cover-fallback">
          <BookOpen size={32} />
          <span>{book.title.split(':')[0]}</span>
          <small>Cover unavailable</small>
        </div>
      )}
    </div>
  );
}
type ModelContext = {
  registerTool: (
    tool: {
      name: string;
      description: string;
      inputSchema: object;
      annotations: object;
      execute: (input: unknown) => unknown;
    },
    options: { signal: AbortSignal },
  ) => void | Promise<void>;
};
export default function Shelf() {
  const [books, setBooks] = useState<Book[]>([]);
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [notice, setNotice] = useState('');
  const [progress, setProgress] = useState<{status: string; processed: number; total: number; basic: number; fullyChecked: number; message: string} | null>(null);
  useEffect(() => {
    const controller = new AbortController();
    const refresh = async () => {
      try {
        const response = await fetch('/enrichment-status.json', {signal: controller.signal});
        if (!response.ok) return;
        const status = await response.json() as NonNullable<typeof progress>;
        const data = await fetch('/enrichment.json', {signal: controller.signal});
        if (!data.ok) return;
        const extra = await data.json() as {books: Record<string, Enrichment>};
        if (!controller.signal.aborted) {
          setProgress(status);
          setBooks(old => old.map(b => ({...b, detail: extra.books[b.id]})));
        }
      } catch { /* Keep the last successful snapshot during a transient failure. */ }
    };
    void refresh();
    const timer = setInterval(refresh, 15000);
    return () => { controller.abort(); clearInterval(timer); };
  }, []);
  useEffect(() => {
    const abort = new AbortController();
    (async () => {
      try {
        const r = await fetch('/catalog.json', { signal: abort.signal });
        if (!r.ok) throw Error('Your catalog could not be loaded.');
        const catalog = (await r.json()) as { books: Book[] };
        if (!Array.isArray(catalog.books))
          throw Error('The catalog file is invalid.');
        let enrichment: { books: Record<string, Enrichment> } = { books: {} };
        try {
          const e = await fetch('/enrichment.json', { signal: abort.signal });
          if (!e.ok) throw Error();
          enrichment = await e.json();
        } catch {
          if (!abort.signal.aborted) {
            setNotice(
              'Story details could not be loaded. Showing the imported catalog.',
            );
            setFilters((f) => ({ ...f, scope: 'all' }));
          }
        }
        if (!abort.signal.aborted) {
          setBooks(
            catalog.books.map((b: Book) => ({
              ...b,
              detail: enrichment.books[b.id],
            })),
          );
          setLoading(false);
        }
      } catch (e) {
        if (!abort.signal.aborted) {
          setError(
            e instanceof Error ? e.message : 'Unable to load the catalog.',
          );
          setLoading(false);
        }
      }
    })();
    return () => abort.abort();
  }, []);
  const update = (changes: Partial<Filters>) => {
    setFilters((f) => ({ ...f, ...changes }));
    setPage(1);
  };
  const results = useMemo(() => filterBooks(books, filters), [books, filters]);
  const enriched = books.filter((b) => b.detail);
  const countHoopla = books.filter((b) => b.hooplaListed).length;
  const characterNames = useMemo(
    () => [
      'All characters',
      'Spider-Man',
      'Moon Knight',
      'Avengers',
      'X-Men',
      ...Array.from(
        new Set(
          books.flatMap((b) => [...(b.detail?.characters.map((c) => c.name) ?? []), ...(b.detail?.automation?.characterMentions ?? [])]),
        ),
      )
        .filter(
          (c) =>
            !['Spider-Man', 'Moon Knight', 'Avengers', 'X-Men'].includes(c),
        )
        .sort(),
    ],
    [books],
  );
  const runs = useMemo(
    () => [
      'All runs',
      ...Array.from(
        new Set(
          books
            .filter((b) => matchesCharacter(b, filters.character))
            .flatMap((b) => (b.detail?.readingPath.name ? [b.detail.readingPath.name] : [])),
        ),
      ).sort(),
    ],
    [books, filters.character],
  );
  const current = books.find((b) => b.id === selected);
  const detail = current?.detail;
  const shared = current ? overlaps(current, books) : [];
  const runBooks = current?.detail?.readingPath.name
    ? enriched
        .filter(
          (b) =>
            b.detail!.readingPath.name === current.detail!.readingPath.name,
        )
        .sort(
          (a, b) =>
            a.detail!.readingPath.position - b.detail!.readingPath.position ||
            Number(a.detail!.readingPath.alternative) -
              Number(b.detail!.readingPath.alternative),
        )
    : [];
  const pages = Math.max(1, Math.ceil(results.length / 24));
  const currentPage = Math.min(page, pages);
  const shown = results.slice((currentPage - 1) * 24, currentPage * 24);
  useEffect(() => {
    const context = (document as Document & { modelContext?: ModelContext })
      .modelContext;
    if (!context?.registerTool || !books.length) return;
    const lifecycle = new AbortController();
    Promise.resolve(
      context.registerTool(
        {
          name: 'search_comic_catalog',
          description:
            'Search the local comic catalog and update visible results. Matches include sourced appearances and title matches.',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string' },
              character: { type: 'string', enum: characterNames },
            },
            additionalProperties: false,
          },
          annotations: { readOnlyHint: false, untrustedContentHint: true },
          execute(input) {
            if (!input || typeof input !== 'object' || Array.isArray(input))
              throw Error('Expected an object.');
            const i = input as Record<string, unknown>;
            if (Object.keys(i).some((k) => !['query', 'character'].includes(k)))
              throw Error('Unknown field.');
            if (i.query !== undefined && typeof i.query !== 'string')
              throw Error('query must be text.');
            if (
              i.character !== undefined &&
              (typeof i.character !== 'string' ||
                !characterNames.includes(i.character))
            )
              throw Error('Unknown character.');
            const next = {
              ...initialFilters,
              scope: 'all',
              query: (i.query as string) ?? '',
              character: (i.character as string) ?? 'All characters',
            };
            const matches = filterBooks(books, next);
            flushSync(() => {
              setFilters(next);
              setPage(1);
              setSelected(null);
            });
            return {
              count: matches.length,
              books: matches
                .slice(0, 24)
                .map((b) => ({
                  id: b.id,
                  title: b.title,
                  enriched: !!b.detail,
                })),
            };
          },
        },
        { signal: lifecycle.signal },
      ),
    ).catch(() => {});
    return () => lifecycle.abort();
  }, [books, characterNames]);
  return (
    <main>
      <header className="masthead">
        <a className="brand" href="/">
          <span className="brand-icon">
            <Library size={24} />
          </span>
          PANEL<span className="brand-light">/ your comic shelf</span>
        </a>
        <span className="local-label">
          ON THIS COMPUTER · ORANGE COUNTY, FL
        </span>
      </header>
      <section className="workspace">
        <div className="intro">
          <div>
            <p className="eyebrow">MARVEL AT YOUR LIBRARY</p>
            <h1>Find your next story.</h1>
          </div>
          <div className="catalog-count">
            {countHoopla.toLocaleString()}
            <span>Hoopla-listed records</span>
          </div>
        </div>
        <div className="search-row">
          <label className="search">
            <Search size={20} />
            <input
              aria-label="Search comics"
              placeholder="Try Kraven’s Last Hunt, a creator, or a character…"
              value={filters.query}
              onChange={(e) => update({ query: e.target.value })}
            />
            {filters.query && (
              <button
                className="clear-search"
                onClick={() => update({ query: '' })}
                aria-label="Clear search"
              >
                ×
              </button>
            )}
          </label>
        </div>
        <div className="browse-layout">
          <aside className="filter-panel">
            <div className="filter-heading">
              <SlidersHorizontal size={17} />
              <h2>Find a book</h2>
              <button
                onClick={() => {
                  setFilters(initialFilters);
                  setPage(1);
                }}
              >
                Reset
              </button>
            </div>
            <Choice
              label="Character or team"
              value={filters.character}
              options={characterNames.map((c) => [c, c])}
              onChange={(v) => update({ character: v, run: 'All runs' })}
            />
            <Choice
              label="Match type"
              value={filters.match}
              options={[
                ['any', 'Titles + appearances + mentions'],
                ['verified', 'Sourced appearances only'],
              ]}
              onChange={(v) => update({ match: v })}
            />
            <Choice
              label="Series / reading path"
              value={filters.run}
              options={runs.map((r) => [r, r])}
              onChange={(v) => update({ run: v })}
            />
            <Choice
              label="Library availability"
              value={filters.availability}
              options={[
                ['hoopla', 'Hoopla listed'],
                ['all', 'All imported records'],
                ['unconfirmed', 'Needs availability check'],
              ]}
              onChange={(v) =>
                update({
                  availability: v,
                  scope: v === 'unconfirmed' ? 'all' : filters.scope,
                })
              }
            />
            <label className="check-label">
              <Checkbox
                checked={filters.starting}
                onCheckedChange={(v) => update({ starting: !!v })}
              />
              Suggested starting points
            </label>
            <div className="filter-note">
              <Info size={17} />
              <p>
                Automatic mentions are suggestions. Choose sourced appearances
                only for checked entries. Team membership does not prove an appearance.
              </p>
            </div>
            <details className="data-details">
              <summary>About this catalog</summary>
              <p>
                {books.length.toLocaleString()} imported records.{' '}
                {books.length - countHoopla} need an availability check.{' '}
                {enriched.length} have at least basic metadata;{' '}
                {enriched.filter((b) => b.detail?.review).length} have review
                scores.
              </p>
              <p>
                Availability is a September 8, 2026 snapshot. Confirm borrowing
                on Hoopla. Page counts are ISBN-matched Google Books values and
                may differ on Hoopla.
              </p>
              <p>
                Suggested starting points are editorial choices. Reading paths
                follow collected-volume order, not a universal Marvel
                chronology.
              </p>
            </details>
          </aside>
          <div className="results-panel">
            <EnrichmentControls onSelect={setSelected} />
            <div className="result-controls">
              <Tabs
                value={filters.scope}
                onValueChange={(v) => update({ scope: String(v) })}
              >
                <TabsList>
                  <TabsTrigger value="pilot">
                    Enriched books <span>{enriched.length}</span>
                  </TabsTrigger>
                  <TabsTrigger value="all">Full catalog</TabsTrigger>
                </TabsList>
              </Tabs>
              <Choice
                label="Sort books"
                value={filters.sort}
                options={sortOptions}
                onChange={(v) => update({ sort: v })}
              />
            </div>
            <div className="results-heading">
              <h2>
                {filters.character === 'All characters'
                  ? filters.scope === 'pilot'
                    ? 'Stories to explore'
                    : 'Your Marvel catalog'
                  : filters.character}
              </h2>
              <span role="status">
                {loading
                  ? 'Loading…'
                  : `${results.length.toLocaleString()} books`}
              </span>
            </div>
            <p className="scope-note">
              {filters.sort === 'reading'
                ? 'Reading order is grouped by run. Alternative collections overlap; they are not extra steps.'
                : filters.scope === 'pilot'
                  ? 'Includes checked story details, automatic suggestions, and basic ISBN matches. Suggestions still need review.'
                  : 'All imported records. Missing descriptions, page counts, and ratings have not been guessed.'}{' '}
              {['critic', 'user', 'pages-asc', 'pages-desc'].includes(
                filters.sort,
              ) && 'Books with missing values appear last.'}
            </p>
            {notice && (
              <p className="notice" role="status">
                {notice}
              </p>
            )}
            {error && (
              <div role="alert" className="empty">
                {error}
                <button
                  className="primary-button"
                  onClick={() => window.location.reload()}
                >
                  Retry
                </button>
              </div>
            )}
            {loading ? (
              <p className="empty" role="status">
                Loading your library…
              </p>
            ) : !error && !results.length ? (
              <div className="empty">
                <BookOpen size={30} />
                <h3>No books match these filters.</h3>
                <p>
                  {filters.scope === 'pilot'
                    ? 'This character or story may not have been enriched yet.'
                    : 'Try fewer filters or a different title.'}
                </p>
                <button
                  className="primary-button"
                  onClick={() =>
                    update(
                      filters.scope === 'pilot'
                        ? { scope: 'all', starting: false, run: 'All runs' }
                        : {
                            query: '',
                            character: 'All characters',
                            run: 'All runs',
                            match: 'any',
                            starting: false,
                            availability: 'all',
                          },
                    )
                  }
                >
                  {filters.scope === 'pilot'
                    ? 'Search the full catalog'
                    : 'Clear filters'}
                </button>
              </div>
            ) : (
              <div className="book-grid">
                {shown.map((b) => (
                  <article className="book-card" key={b.id}>
                    <button
                      className="card-open"
                      onClick={() => setSelected(b.id)}
                      aria-label={`Read details for ${b.title}`}
                    >
                      <Cover book={b} />
                      <div className="book-copy">
                        <div className="card-kicker">
                          {b.detail?.startingPoint ? (
                            <span className="start-badge">START HERE</span>
                          ) : (
                            <span>
                              {b.detail?.automation ? 'AUTO · NEEDS REVIEW' : b.detail?.level === 'basic' ? 'BASIC METADATA' : b.detail ? 'STORY DETAILS' : 'CATALOG RECORD'}
                            </span>
                          )}
                          <span>{b.publication}</span>
                        </div>
                        <h3>{b.title.replace(/: Issues? #.*$/i, '')}</h3>
                        <p className="author">{b.author}</p>
                        {b.detail && (
                          <p className="card-summary">{b.detail.summary}</p>
                        )}
                        <div className="book-metrics">
                          <span>
                            <BookOpen size={14} />
                            {b.detail?.pages
                              ? `${b.detail.pages} pages`
                              : 'Length unknown'}
                          </span>
                          <span className={b.detail?.review ? 'rating' : ''}>
                            <Star size={14} />
                            {b.detail?.review
                              ? `${b.detail.review.criticScore.toFixed(1)} critic`
                              : 'Not rated'}
                          </span>
                        </div>
                        <span className="details-link">
                          Explore this book <ArrowRight size={16} />
                        </span>
                      </div>
                    </button>
                  </article>
                ))}
              </div>
            )}
            {results.length > 24 && (
              <div className="pagination">
                <button
                  disabled={currentPage === 1}
                  onClick={() => setPage((p) => p - 1)}
                  aria-label="Previous page"
                >
                  <ChevronLeft size={18} />
                  Previous
                </button>
                <span>
                  Page {currentPage} of {pages}
                </span>
                <button
                  disabled={currentPage === pages}
                  onClick={() => setPage((p) => p + 1)}
                  aria-label="Next page"
                >
                  Next
                  <ChevronRight size={18} />
                </button>
              </div>
            )}
          </div>
        </div>
        <footer className="app-footer">
          Personal catalog · Metadata checked September 8, 2026 · Borrow and
          read through Hoopla
        </footer>
      </section>
      <Sheet
        open={!!current}
        onOpenChange={(open) => {
          if (!open) setSelected(null);
        }}
      >
        <SheetContent className="book-sheet">
          <SheetHeader>
            <p className="eyebrow">INSIDE THE BOOK</p>
            <SheetTitle>
              {current?.title.replace(/: Issues? #.*$/i, '') ?? 'Book details'}
            </SheetTitle>
            <SheetDescription>
              {current?.author} · Catalog edition {current?.publication}
            </SheetDescription>
          </SheetHeader>
          {current && (
            <div className="detail-body">
              <div className="detail-top">
                <Cover key={current.id} book={current} large />
                <div className="detail-facts">
                  <p className="availability">
                    <Check size={16} />
                    {current.hooplaListed
                      ? 'Hoopla listed in your export'
                      : 'Availability needs checking'}
                  </p>
                  <strong className="page-total">
                    {detail?.pages ?? '—'}
                    <span>
                      {detail?.pages
                        ? 'pages · matched edition'
                        : 'page count unavailable'}
                    </span>
                  </strong>
                  {detail?.hooplaUrls?.map((url, i) => (
                    <a
                      className="primary-button"
                      key={url}
                      href={url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Open {i > 0 ? `edition ${i + 1} on ` : ''}Hoopla{' '}
                      <ArrowUpRight size={16} />
                    </a>
                  ))}
                  <a
                    className="secondary-link"
                    href={current.catalogUrl}
                    target="_blank"
                    rel="noreferrer"
                  >
                    View OCLS record <ArrowUpRight size={15} />
                  </a>
                </div>
              </div>
              {detail ? (
                <>
                  <section className="detail-section">
                    <h3>What’s the story?</h3>
                    <p>{detail.summary}</p>
                    <p className="subtle">
                      {detail.level === 'basic' ? 'Basic ISBN match · short publisher excerpt. Open Google Books below for the full synopsis. Story arcs and appearances are not yet checked.' : 'Spoiler-light summary based on the sources below.'}
                    </p>
                    <div className="story-list">
                      {detail.stories.map((s) => (
                        <div key={s.title}>
                          <Layers size={17} />
                          <span>
                            <strong>{s.title}</strong>
                            <small>{s.coverage}</small>
                          </span>
                        </div>
                      ))}
                    </div>
                  </section>
                  <section className="detail-section">
                    <h3>Characters & teams</h3>
                    <div className="character-tags">
                      {detail.characters.map((c) => (
                        <button
                          key={c.name}
                          title={c.role}
                          onClick={() => {
                            update({
                              character: c.name,
                              run: 'All runs',
                              scope: 'all',
                            });
                            setSelected(null);
                          }}
                        >
                          {c.name}
                        </button>
                      ))}
                    </div>
                    <p className="subtle">
                      Lead characters and appearances supported by the source
                      synopsis. This is not a complete cameo index.
                    </p>
                  </section>
                  {detail.automation && <section className="detail-section">
                    <h3>Automatic suggestions · needs review</h3>
                    <p className="subtle">Extracted from the publisher description and catalog title. Mentions can refer to comparisons or backstory; they are not confirmed appearances.</p>
                    {detail.automation.characterMentions.length>0 && <p><strong>Characters mentioned:</strong> {detail.automation.characterMentions.join(', ')}</p>}
                    {detail.automation.suggestedReadingPath && <p><strong>Possible volume order:</strong> {detail.automation.suggestedReadingPath.name}, volume {detail.automation.suggestedReadingPath.position}. {detail.automation.suggestedReadingPath.note}</p>}
                    {detail.automation.suggestedIssues.length>0 && <details><summary>Suggested collected issues</summary><ul className="issue-list">{detail.automation.suggestedIssues.map(i=><li key={i}>{i}</li>)}</ul><p>Not used for overlap matching until the edition is confirmed.</p></details>}
                    {detail.automation.reviewCandidate && <p><strong>Possible review match:</strong> <a className="secondary-link" href={detail.automation.reviewCandidate.url} target="_blank" rel="noreferrer">{detail.automation.reviewCandidate.title}</a>. Matches the suggested issue set; confirm the edition before using its score.</p>}
                    <ul>{detail.automation.reasons.map(r=><li key={r}>{r}</li>)}</ul>
                  </section>}
                  <section className="detail-section">
                    <h3>
                      <Route size={18} />
                      Where to start
                    </h3>
                    <p>{detail.readingPath.note}</p>
                    {detail.readingPath.name && <p className="subtle">
                      {detail.readingPath.name} ·{' '}
                      {detail.readingPath.alternative
                        ? 'Alternative collection'
                        : `Step ${detail.readingPath.position}`}
                    </p>}
                    <ol className="reading-list">
                      {runBooks.map((b) => (
                        <li key={b.id}>
                          <button
                            aria-current={
                              b.id === current.id ? 'step' : undefined
                            }
                            onClick={() => setSelected(b.id)}
                          >
                            <span>
                              {b.detail!.readingPath.alternative
                                ? 'ALT'
                                : b.detail!.readingPath.position}
                            </span>
                            {b.title.replace(/: Issues? #.*$/i, '')}
                            {b.id === current.id && <Check size={16} />}
                          </button>
                        </li>
                      ))}
                    </ol>
                  </section>
                  <section className="detail-section">
                    <h3>Reviews</h3>
                    {detail.review ? (
                      <>
                        <div className="review-scores">
                          <div>
                            <strong>
                              {detail.review.criticScore.toFixed(1)}
                              <small>/10</small>
                            </strong>
                            <span>Critic aggregate</span>
                            <small>{detail.review.criticCount} reviews</small>
                          </div>
                          <div>
                            <strong>
                              {detail.review.userScore?.toFixed(1) ?? '—'}
                              {detail.review.userScore != null && (
                                <small>/10</small>
                              )}
                            </strong>
                            <span>Reader score</span>
                            <small>
                              {detail.review.userCount
                                ? `${detail.review.userCount} ratings`
                                : 'No reader ratings'}
                            </small>
                          </div>
                        </div>
                        <p className="subtle">
                          {detail.review.scope} {detail.review.match}
                        </p>
                        <a
                          className="secondary-link"
                          href={detail.review.url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          Read reviews on Comic Book Roundup{' '}
                          <ArrowUpRight size={15} />
                        </a>
                      </>
                    ) : (
                      <p>No reliable collection score has been matched yet.</p>
                    )}
                  </section>
                  {shared.length > 0 && (
                    <section className="detail-section">
                      <h3>
                        <Layers size={18} />
                        Overlapping collections
                      </h3>
                      <p className="subtle">
                        These books share checked issues. Extra material
                        can differ.
                      </p>
                      {shared.map(({ book, count }) => (
                        <button
                          className="overlap-link"
                          key={book.id}
                          onClick={() => setSelected(book.id)}
                        >
                          <span>
                            {book.title.replace(/: Issues? #.*$/i, '')}
                            <small>{count} shared issues</small>
                          </span>
                          <ArrowRight size={17} />
                        </button>
                      ))}
                    </section>
                  )}
                  <details className="detail-section">
                    <summary>Collected issues & edition details</summary>
                    <p>{detail.contentsNote}</p>
                    <ul className="issue-list">
                      {detail.issueKeys.map((i) => (
                        <li key={i}>{i}</li>
                      ))}
                    </ul>
                    <p className="subtle">
                      ISBN {current.isbn}. Page count is for this ISBN on Google
                      Books; Hoopla’s displayed total may differ.
                    </p>
                  </details>
                  <section className="detail-section sources">
                    <h3>Sources</h3>
                    {detail.sources.map((s) => (
                      <a
                        key={s.url}
                        href={s.url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        {s.label}
                        <ArrowUpRight size={14} />
                      </a>
                    ))}
                    <p className="subtle">
                      Checked {detail.checkedAt}. Summaries and starting-point
                      suggestions are editorial; scores come from the linked
                      source.
                    </p>
                  </section>
                </>
              ) : (
                <section className="detail-section">
                  <h3>This book hasn’t been enriched yet.</h3>
                  <p>
                    The imported record includes its title, creator, ISBN, and
                    library holdings. Storylines, appearances, reviews, and page
                    counts still need matching.
                  </p>
                  <p>ISBN {current.isbn || 'not provided'}</p>
                  <p className="subtle">{current.holdings}</p>
                </section>
              )}
            </div>
          )}
        </SheetContent>
      </Sheet>
    </main>
  );
}
