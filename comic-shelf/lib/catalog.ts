export type Source = { label: string; url: string };
export type Enrichment = {
  level?: 'basic';
  automation?: {
    version: number;
    characterMentions: string[];
    suggestedIssues: string[];
    reviewCandidate?: {title:string; url:string; criticScore:number} | null;
    suggestedReadingPath: {name: string; position: number; note: string} | null;
    reasons: string[];
  };
  summary: string;
  synopsisReview?: {
    decisionId: string;
    reviewerKind: 'human' | 'assistant' | 'delegated';
  };
  pages: number | null;
  pagesSource: string;
  coverUrl?: string;
  coverSource: string;
  checkedAt: string;
  sources: Source[];
  hooplaUrls?: string[];
  characters: { name: string; role: string; source: string }[];
  stories: { title: string; coverage: string }[];
  readingPath: {
    name: string;
    position: number;
    note: string;
    alternative: boolean;
  };
  issueKeys: string[];
  contentsNote: string;
  startingPoint: boolean;
  review?: {
    criticScore: number;
    criticCount: number;
    userScore: number | null;
    userCount: number | null;
    url: string;
    checkedAt: string;
    scope: string;
    match: string;
    title: string;
  };
};
export type Book = {
  id: string;
  title: string;
  author: string;
  isbn: string;
  publisher: string;
  publication: string;
  format: string;
  catalogUrl: string;
  holdings: string;
  hooplaListed: boolean;
  detail?: Enrichment;
};
export type Filters = {
  query: string;
  character: string;
  scope: string;
  availability: string;
  match: string;
  run: string;
  sort: string;
  starting: boolean;
};
export const initialFilters: Filters = {
  query: '',
  character: 'All characters',
  scope: 'pilot',
  availability: 'hoopla',
  match: 'any',
  run: 'All runs',
  sort: 'recommended',
  starting: false,
};
export const sortOptions = [
  ['recommended', 'Enriched first'],
  ['reading', 'Reading order within runs'],
  ['pages-asc', 'Shortest first'],
  ['pages-desc', 'Longest first'],
  ['critic', 'Highest critic score'],
  ['user', 'Highest reader score'],
  ['title', 'Title A–Z'],
] as const;
export const normalize = (s: string) =>
  s
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]/g, '');
export function matchesCharacter(b: Book, c: string, verified = false) {
  if (c === 'All characters') return !verified || !!b.detail?.characters.length;
  const target = normalize(c);
  const appearance = b.detail?.characters.some(
    (x) => normalize(x.name) === target,
  );
  return !!appearance || (!verified && (normalize(b.title).includes(target) || !!b.detail?.automation?.characterMentions.some(n => normalize(n) === target)));
}
export function filterBooks(books: Book[], f: Filters): Book[] {
  const terms = f.query.trim().split(/\s+/).filter(Boolean).map(normalize);
  const result = books.filter(
    (b) =>
      (f.scope !== 'pilot' || !!b.detail) &&
      (f.availability !== 'hoopla' || b.hooplaListed) &&
      (f.availability !== 'unconfirmed' || !b.hooplaListed) &&
      matchesCharacter(b, f.character, f.match === 'verified') &&
      (f.run === 'All runs' || b.detail?.readingPath.name === f.run) &&
      (!f.starting || b.detail?.startingPoint) &&
      terms.every((t) =>
        normalize(
          [
            b.title,
            b.author,
            b.isbn,
            b.detail?.summary,
            ...(b.detail?.stories.map((s) => s.title) ?? []),
            ...(b.detail?.characters.map((c) => c.name) ?? []),
            ...(b.detail?.automation?.characterMentions ?? []),
          ].join(' '),
        ).includes(t),
      ),
  );
  const collator = new Intl.Collator('en', {
    numeric: true,
    sensitivity: 'base',
  });
  const title = (a: Book, b: Book) =>
    collator.compare(a.title, b.title) || a.id.localeCompare(b.id);
  const nullable = (
    a: number | undefined | null,
    b: number | undefined | null,
    descending = false,
  ) =>
    a == null
      ? b == null
        ? 0
        : 1
      : b == null
        ? -1
        : descending
          ? b - a
          : a - b;
  return result.sort((a, b) => {
    let n = 0;
    if (f.sort === 'pages-asc' || f.sort === 'pages-desc')
      n = nullable(a.detail?.pages, b.detail?.pages, f.sort === 'pages-desc');
    else if (f.sort === 'critic')
      n = nullable(
        a.detail?.review?.criticScore,
        b.detail?.review?.criticScore,
        true,
      );
    else if (f.sort === 'user')
      n = nullable(
        a.detail?.review?.userScore,
        b.detail?.review?.userScore,
        true,
      );
    else if (f.sort === 'reading') {
      if (!a.detail?.readingPath.name || !b.detail?.readingPath.name)
        n = Number(!!b.detail?.readingPath.name) - Number(!!a.detail?.readingPath.name);
      else
        n =
          collator.compare(
            a.detail.readingPath.name,
            b.detail.readingPath.name,
          ) ||
          a.detail.readingPath.position - b.detail.readingPath.position ||
          Number(a.detail.readingPath.alternative) -
            Number(b.detail.readingPath.alternative);
    } else if (f.sort === 'recommended')
      n =
        Number(!!b.detail) - Number(!!a.detail) ||
        Number(b.detail?.level !== 'basic') - Number(a.detail?.level !== 'basic') ||
        Number(!!b.detail?.startingPoint) - Number(!!a.detail?.startingPoint);
    return n || title(a, b);
  });
}
export function overlaps(book: Book, books: Book[]) {
  if (!book.detail) return [];
  const own = new Set(book.detail.issueKeys);
  return books
    .filter((b) => b.id !== book.id && b.detail)
    .map((b) => ({
      book: b,
      count: b.detail!.issueKeys.filter((i) => own.has(i)).length,
    }))
    .filter((x) => x.count > 0)
    .sort((a, b) => b.count - a.count);
}
