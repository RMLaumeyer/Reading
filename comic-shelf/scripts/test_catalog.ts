import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import {
  filterBooks,
  initialFilters,
  overlaps,
  type Book,
  type Enrichment,
} from '../lib/catalog.ts';
const root = new URL('../public/', import.meta.url);
const raw = JSON.parse(readFileSync(new URL('catalog.json', root), 'utf8'));
const extra = JSON.parse(readFileSync(new URL('enrichment.json', root), 'utf8'))
  .books as Record<string, Enrichment>;
const books: Book[] = raw.books.map((b: Book) => ({
  ...b,
  detail: extra[b.id],
}));
const get = (isbn: string) => {
  const b = books.find((b) => b.isbn === isbn);
  assert.ok(b);
  return b;
};
test('Imported catalog reconciles; identifiers stay strings', () => {
  assert.equal(books.length, 4000);
  assert.equal(new Set(books.map((b) => b.id)).size, 4000);
  assert.equal(books.filter((b) => b.hooplaListed).length, 3948);
  assert.ok(books.every((b) => typeof b.isbn === 'string'));
});
test('Pilot details have complete provenance and valid scores', () => {
  const pilot = JSON.parse(readFileSync(new URL('../data/pilot.json', root), 'utf8')).isbns;
  assert.equal(books.filter(b => pilot.includes(b.isbn) && b.detail).length, 26);
  for (const b of books.filter((b) => pilot.includes(b.isbn) && b.detail)) {
    const d = b.detail!;
    assert.ok(d.pages && d.pages > 0);
    assert.ok(d.hooplaUrls?.length);
    assert.ok(d.summary.length > 30);
    assert.ok(d.sources.length >= 2);
    assert.ok(d.sources.every((s) => new URL(s.url).protocol === 'https:'));
    if (d.review) {
      assert.ok(d.review.criticScore >= 0 && d.review.criticScore <= 10);
      assert.ok(d.review.criticCount > 0);
    }
  }
});
test('Missing scores and lengths sort last in both directions', () => {
  for (const sort of ['critic', 'user', 'pages-asc', 'pages-desc']) {
    const list = filterBooks(books, { ...initialFilters, scope: 'all', sort });
    let missing = false;
    let prev: number | undefined;
    for (const b of list) {
      const value =
        sort === 'critic'
          ? b.detail?.review?.criticScore
          : sort === 'user'
            ? b.detail?.review?.userScore
            : b.detail?.pages;
      if (value == null) {
        missing = true;
        continue;
      }
      assert.equal(missing, false);
      if (prev !== undefined)
        assert.ok(sort === 'pages-asc' ? value >= prev : value <= prev);
      prev = value;
    }
  }
});
test('Character search finds a sourced appearance outside the title', () => {
  const found = filterBooks(books, {
    ...initialFilters,
    character: 'Venom',
    match: 'verified',
  });
  assert.ok(found.some((b) => b.isbn === '9781302525651'));
  assert.ok(
    found.every((b) => b.detail?.characters.some((c) => c.name === 'Venom')),
  );
});
test('Team membership is not treated as an appearance', () => {
  const found = filterBooks(books, {
    ...initialFilters,
    character: 'Avengers',
    match: 'verified',
  });
  assert.equal(found.length, 0);
});
test('Search handles punctuation and character aliases', () => {
  assert.ok(
    filterBooks(books, {
      ...initialFilters,
      query: 'spiderman life story',
    }).some((b) => b.isbn === '9781302516468'),
  );
  assert.ok(
    filterBooks(books, { ...initialFilters, query: "Kraven's Last Hunt" }).some(
      (b) => b.isbn === '9781302935818',
    ),
  );
});
test('Availability filter retains unconfirmed records without claiming Hoopla', () => {
  const list = filterBooks(books, {
    ...initialFilters,
    scope: 'all',
    availability: 'unconfirmed',
  });
  assert.equal(list.length, 52);
  assert.ok(list.every((b) => !b.hooplaListed));
});
test('Different Kraven editions share exactly the six central issues', () => {
  const short = get('9781302935818');
  const epic = get('9781302498139');
  const match = overlaps(short, books).find((x) => x.book.id === epic.id);
  assert.equal(match?.count, 6);
  assert.ok(epic.detail!.pages! > short.detail!.pages!);
});
test('Complete collection overlaps smaller volumes, not other Moon Knight series', () => {
  const shared = overlaps(get('9781302940973'), books);
  assert.deepEqual(shared.map((x) => x.count).sort((a,b)=>a-b), [4, 5, 5, 14]);
  assert.equal(shared.length, 4);
});
test('Moon Knight new annotations preserve edition and appearance boundaries', () => {
  const bendis = get('9781302514075');
  assert.equal(bendis.detail!.characters.some(c=>c.name==='Avengers'),false);
  const legacy = overlaps(get('9781302941314'), books);
  assert.deepEqual(legacy.map(x=>x.count).sort((a,b)=>a-b),[6,7]);
  assert.equal(get('9781302488871').detail!.issueKeys.some(x=>x.endsWith('#10')),false);
  assert.equal(get('9781302368197').detail!.issueKeys.length,0);
});
test('Reading order follows a run and preserves alternative editions', () => {
  const f = {
    ...initialFilters,
    run: 'Moon Knight — Jed MacKay (2021)',
    sort: 'reading',
  };
  const list = filterBooks(books, f);
  assert.deepEqual(
    list.map((b) => b.detail!.readingPath.position),
    [1, 2, 3, 4, 5],
  );
  assert.equal(list[0].isbn, '9781302940669');
});
