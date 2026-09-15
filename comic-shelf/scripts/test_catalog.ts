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
test('Seventh batch preserves crossover gaps, partial material and alternate editions', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/deep-batch-07.json', root), 'utf8')) as string[];
  const previous = ['04','05','06'].flatMap(n => JSON.parse(readFileSync(new URL(`../data/deep-batch-${n}.json`, root), 'utf8')) as string[]);
  assert.equal(ids.length,90);
  assert.equal(new Set([...previous,...ids]).size,340);
  assert.ok(ids.every(isbn => get(isbn).detail?.level !== 'basic' && get(isbn).detail?.summary));
  assert.match(get('9781302527327').detail!.readingPath.note,/Carnage Reigns/);
  assert.match(get('9781302532260').detail!.readingPath.note,/Pools of Blood/);
  assert.deepEqual(get('9781302964924').detail!.issueKeys,[
    'Miles Morales: Spider-Man (2022) #30','Miles Morales: Spider-Man (2022) #31',
    'Deadpool (2024) #11','Deadpool (2024) #12',
  ]);
  for (const isbn of ['9781302531546','9781302532260']) {
    assert.ok(!get(isbn).detail!.issueKeys.some(k=>k.includes('Annual') || k.endsWith('#25')));
  }
  assert.equal(overlaps(get('9781302513627'),[get('9781302535377')])[0]?.count,16);
  assert.equal(overlaps(get('9781302479336'),[get('9781302485719')]).length,0);
  assert.equal(overlaps(get('9781302510572'),[get('9780785182177')])[0]?.count,5);
  assert.equal(overlaps(get('9781302532956'),[get('9780785179474')])[0]?.count,4);
  assert.equal(get('9781302515041').detail!.review,undefined);
  assert.equal(get('9781302485665').detail!.issueKeys.length,0);
  assert.ok(get('9781302529192').detail!.characters.some(c=>c.name==='Moon Knight 2099'));
  assert.ok(!get('9781302529192').detail!.characters.some(c=>c.name==='Moon Knight'));
});
test('Sixth batch finishes X-Men and adds Spider-Man without conflating editions or issue suffixes', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/deep-batch-06.json', root), 'utf8')) as string[];
  const previous = ['04','05'].flatMap(n => JSON.parse(readFileSync(new URL(`../data/deep-batch-${n}.json`, root), 'utf8')) as string[]);
  assert.equal(ids.length, 100);
  assert.equal(new Set([...previous, ...ids]).size, 250);
  for (const isbn of ids) {
    const d = get(isbn).detail!;
    assert.ok(d.summary && d.stories.length && d.sources.length && d.issueKeys.length);
    assert.notEqual(d.level, 'basic');
    assert.ok(!d.automation);
  }
  assert.equal(books.filter(b => b.title.toLowerCase().includes('x-men') && (!b.detail || b.detail.level === 'basic')).length, 0);
  assert.equal(ids.filter(isbn => get(isbn).detail!.review).length, 40);
  assert.equal(overlaps(get('9781302479817'), [get('9781302478476')]).length, 0);
  assert.ok(get('9781302479817').detail!.issueKeys.includes('Edge of Spider-Verse (2014) #5'));
  assert.equal(overlaps(get('9781302513924'), [get('9781302485504')])[0].count, 5);
  assert.equal(overlaps(get('9781302513924'), [get('9781302489199')])[0].count, 6);
  assert.equal(overlaps(get('9781302936006'), [get('9781302935993')]).length, 0);
  assert.ok(get('9781302936006').detail!.issueKeys.includes('Amazing Spider-Man (2018) #50.LR'));
  assert.ok(get('9781302940195').detail!.issueKeys.includes('Amazing Spider-Man (2018) #78.BEY'));
  assert.equal(get('9781302516420').detail!.readingPath.name,get('9781302507206').detail!.readingPath.name);
  assert.equal(get('9781302516420').detail!.readingPath.position,5);
  assert.equal(get('9781302939588').detail!.readingPath.position,15);
  assert.ok(!get('9780785182177').detail!.issueKeys.includes('Avenging Spider-Man (2011) #6'));
});
test('Fifth batch corrects wrong synopses and distinguishes overlapping editions', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/deep-batch-05.json', root), 'utf8')) as string[];
  const prior = JSON.parse(readFileSync(new URL('../data/deep-batch-04.json', root), 'utf8')) as string[];
  assert.equal(ids.length, 50);
  assert.equal(new Set([...ids, ...prior]).size, 150);
  for (const isbn of ids) {
    const d = get(isbn).detail!;
    assert.ok(d.summary && d.stories.length && d.sources.length && d.issueKeys.length);
    assert.notEqual(d.level, 'basic');
    assert.ok(!d.automation);
  }
  const coming = get('9780785171485').detail!;
  assert.ok(coming.summary.includes('Hope'));
  assert.ok(!coming.summary.includes('Basilisk'));
  assert.equal(coming.pages, null);
  assert.ok(coming.issueKeys.includes('X-Force (2008) #28'));
  assert.equal(overlaps(get('9781302967314'), [get('9781302940157')]).length, 0);
  assert.equal(overlaps(get('9781302517489'), [get('9781302479787')])[0].count, 8);
  assert.equal(overlaps(get('9781302533014'), [get('9781302939113')])[0].count, 4);
  assert.ok(!get('9781302488819').detail!.issueKeys.includes('S.W.O.R.D. (2020) #1'));
  assert.equal(ids.filter(isbn => get(isbn).detail!.review).length, 5);
});
test('Fourth research batch adds 100 distinct books with edition-safe reviews and overlaps', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/deep-batch-04.json', root), 'utf8')) as string[];
  const previous = ['01', '02', '03'].flatMap(n => JSON.parse(readFileSync(new URL(`../data/xmen-batch-${n}.json`, root), 'utf8')) as string[]);
  assert.equal(ids.length, 100);
  assert.equal(new Set([...previous, ...ids]).size, 250);
  for (const isbn of ids) {
    const detail = get(isbn).detail!;
    assert.ok(detail.summary && detail.stories.length && detail.sources.length);
    assert.notEqual(detail.level, 'basic');
    assert.ok(!detail.automation);
  }
  assert.ok(get('9781302515423').detail!.issueKeys.includes('Giant-Size Astonishing X-Men (2008) #1'));
  assert.equal(get('9781302515423').detail!.readingPath.name, get('9780785170068').detail!.readingPath.name);
  for (const isbn of ['9781302478711', '9781302533083', '9781302531669']) assert.ok(!get(isbn).detail!.review);
  assert.equal(ids.filter(isbn => get(isbn).detail!.review).length, 33);
  assert.ok(!get('9781302506414').detail!.characters.some(c => c.name === 'X-Men'));
  assert.ok(get('9781302533977').detail!.issueKeys.includes('X-Factor (1986) #27'));
  assert.ok(!get('9781302533977').detail!.issueKeys.includes('X-Factor (1986) #51'));
});
test('Third X-Men batch preserves distinct editions, gaps and prior batches', () => {
  const batches = ['01', '02', '03'].map(n => JSON.parse(readFileSync(new URL(`../data/xmen-batch-${n}.json`, root), 'utf8')) as string[]);
  assert.ok(batches.every(ids => ids.length === 50));
  assert.equal(new Set(batches.flat()).size, 150);
  for (const isbn of batches.flat()) {
    const d = get(isbn).detail!;
    assert.ok(d && d.level !== 'basic' && d.summary && d.stories.length && d.sources.length);
  }
  assert.equal(get('9780785178798').detail!.readingPath.position, 7);
  assert.equal(get('9780785179627').detail!.readingPath.position, 8);
  assert.equal(get('9780785179801').detail!.readingPath.position, 9);
  assert.ok(!get('9780785182108').detail!.issueKeys.includes('Uncanny X-Men (2011) #5'));
  assert.ok(!get('9780785183006').detail!.issueKeys.includes('Uncanny X-Men (2011) #10'));
  assert.ok(!get('9781302479626').detail!.issueKeys.includes('Uncanny X-Men (1963) #160'));
  assert.ok(get('9781302377717').detail!.issueKeys.includes('Uncanny X-Men (2013) #15.INH'));
  assert.ok(!get('9781302377717').detail!.issueKeys.includes('Uncanny X-Men (2013) #15'));
  assert.ok(get('9781302479596').detail!.issueKeys.includes('X-Men Annual (1970) #4'));
  const master = get('9781302479602').detail!.issueKeys;
  assert.equal(master.filter(k => get('9780785180012').detail!.issueKeys.includes(k)).length, 3);
  assert.ok(get('9781302508715').detail!.issueKeys.includes('Uncanny X-Men (1963) #534.1'));
  assert.ok(get('9781302530754').detail!.issueKeys.every(k => !k.startsWith('Weapon X-Men (2025)')));
  assert.ok(get('9781302534158').detail!.issueKeys.every(k => k.startsWith('Weapon X-Men (2025)')));
});
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
  assert.ok(found.every(b=>b.detail!.characters.some(c=>c.name==='Avengers')));
  assert.ok(!found.some(b=>b.isbn==='9781302514075'));
});
test('X-Men batch contains fifty records with conservative edition matching', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/xmen-batch-01.json', root), 'utf8')) as string[];
  assert.equal(ids.length,50);
  assert.equal(new Set(ids).size,50);
  assert.ok(ids.every(isbn=>get(isbn).detail?.stories.length));
  assert.ok(!get('9781302392925').detail!.issueKeys.some(x=>x.endsWith('#30')));
  assert.ok(!get('9781302498870').detail!.issueKeys.some(x=>x.endsWith('#21')));
  assert.equal(get('9781302478865').detail!.review,undefined);
  assert.ok(!get('9781302481605').detail!.characters.some(c=>c.name==='X-Men'));
  const shared = overlaps(get('9781302527464'), books);
  assert.equal(shared.find(x=>x.book.isbn==='9780785170037')?.count,6);
  assert.equal(shared.find(x=>x.book.isbn==='9780785170044')?.count,6);
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
test('Second X-Men batch preserves separate universes, overlap and gaps', () => {
  const ids = JSON.parse(readFileSync(new URL('../data/xmen-batch-02.json', root), 'utf8')) as string[];
  const first = JSON.parse(readFileSync(new URL('../data/xmen-batch-01.json', root), 'utf8')) as string[];
  assert.equal(new Set([...ids,...first]).size,100);
  assert.ok(ids.every(isbn=>get(isbn).detail!.summary.length>60));
  assert.notEqual(get('9781302530365').detail!.readingPath.name,get('9780785171256').detail!.readingPath.name);
  assert.equal(overlaps(get('9781302530365'),[get('9780785171256')]).length,0);
  assert.equal(overlaps(get('9781302532048'),[get('9780785171256'),get('9780785171263')]).length,2);
  assert.equal(overlaps(get('9781302508203'),[get('9781302479152')])[0].count,4);
  assert.ok(!get('9781302482312').detail!.issueKeys.some(i=>i.endsWith('#12')));
  assert.ok(!get('9781302524258').detail!.issueKeys.some(i=>i.endsWith('#6')));
  assert.equal(get('9781302530365').detail!.review,undefined);
  assert.equal(get('9781302436469').detail!.review,undefined);
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
