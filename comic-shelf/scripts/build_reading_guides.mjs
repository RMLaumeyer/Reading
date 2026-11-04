import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
const project = fileURLToPath(new URL('../', import.meta.url));
const directory = path.join(project, 'public/reading-guides');
const catalog = JSON.parse(fs.readFileSync(path.join(project, 'public/catalog.json'), 'utf8'));
const byIsbn = new Map(catalog.books.map(book => [book.isbn, book]));
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const guides = fs.readdirSync(directory).filter(name => name.endsWith('.json')).map(name => {
  const guide = JSON.parse(fs.readFileSync(path.join(directory, name), 'utf8'));
  const slug = name.slice(0, -5);
  assert(/^[a-z0-9-]+$/.test(slug));
  if (slug === 'spider-man') Object.assign(guide, {title:'Spider-Man', subtitle:'Peter Parker, from the first swing to fresh starts.', group:'More Marvel', intro:'Pick Bendis for modern teenage Peter, JMS for main-universe adult Peter, or the original Lee/Ditko stories for the foundation. The two Ultimate universes are separate paths.'});
  assert(guide.title && guide.group && guide.stories.length, `${slug}: metadata`);
  const ids = new Set();
  for (const [index, story] of guide.stories.entries()) {
    assert(story.id && !ids.has(story.id), `${slug}: duplicate story`); ids.add(story.id);
    assert(Number.isInteger(story.year) && (!index || story.year >= guide.stories[index - 1].year), `${slug}: chronology`);
    for (const field of ['title','issues','universe','date','why','match']) assert(typeof story[field] === 'string' && story[field], `${slug}: ${field}`);
    assert(story.sources.length, `${slug}: missing evidence`);
    for (const isbn of story.isbns) assert(byIsbn.has(isbn), `${slug}: missing ISBN ${isbn}`);
    for (const key of story.sources) assert(guide.sources[key], `${slug}: source ${key}`);
  }
  for (const source of Object.values(guide.sources)) assert(new URL(source.url).protocol === 'https:', `${slug}: unsafe source`);
  for (const start of guide.starts || []) assert(ids.has(start.storyId), `${slug}: start target ${start.storyId}`);
  return {slug, guide};
});
const header = `<header><a class="brand" href="/">▤ PANEL <span>/ reading guides</span></a><nav aria-label="Main navigation"><a href="/">Shelf</a><a href="/reading-guides/" aria-current="page">Character guides</a><a href="/event-timelines/">Event timelines</a></nav></header>`;
const footer = `<footer>PANEL / Your library. Your next story. <a href="/reading-guides/">Browse all guides →</a></footer>`;
function shell(title, content, script, attributes = '') {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} · Panel</title><link rel="stylesheet" href="/reading-guides/style.css"><script src="/reading-guides/${script}" defer></script></head><body id="top" ${attributes}>${header}<main>${content}</main>${footer}</body></html>`;
}
for (const {slug, guide} of guides) {
  const checkedLabel = new Date(`${guide.checkedAt}T12:00:00Z`).toLocaleDateString('en-US', {month:'long',day:'numeric',year:'numeric',timeZone:'UTC'});
  const starts = guide.starts?.length ? guide.starts : guide.stories.filter(story => story.start).slice(0, 4).map(story => ({storyId:story.id,label:story.title,description:story.date}));
  const universes = [...new Set(guide.stories.map(story => story.universe))];
  const html = shell(`${guide.title} reading guide`, `
    <section class="hero"><p class="eyebrow">${escape(guide.group.toUpperCase())} / READING GUIDE</p><h1>${escape(guide.title)}<br><em>Your reading order.</em></h1><p class="lede">${escape(guide.subtitle || '')}</p><div id="stats" class="stats" aria-live="polite">Checking your local catalog…</div></section>
    <section class="starts" aria-labelledby="start-title"><div><p class="eyebrow">PICK A DOOR IN</p><h2 id="start-title">Where to begin.</h2><p>${escape(guide.intro || 'Choose a starting point, then explore the key stories below.')}</p></div><div class="start-options">${starts.map(start => `<a href="#${escape(start.storyId)}"><strong>${escape(start.label)} ↗</strong><span>${escape(start.description || '')}</span></a>`).join('')}</div></section>
    <section class="method"><h2>How to read this guide</h2><p><strong>Chronological means original story publication order</strong>, not the catalog edition or reprint year. Entries follow their first publication year; overlapping runs may cover the same period. This is a curated selection of starting points and key stories, not a complete issue-by-issue chronology. Alternate settings and continuity are labeled. A team-book recommendation on a member’s page explains that member’s role; it is not a solo series.</p><p><strong>Library matches use your supplied catalog snapshot</strong>, imported September 8, 2026. “Hoopla listed” is not a live borrowing check. “No confirmed match” is a gap in this cross-reference, not proof that the library lacks the story. Read collection notes: some books are alternatives, others are consecutive volumes or cover only part of a larger saga. Recommendations reflect the linked readers and critics rather than a measured consensus. Story titles may reveal major milestones.</p></section>
    <section aria-labelledby="timeline-title"><div class="timeline-heading"><div><p class="eyebrow">THE KEY-STORY TIMELINE</p><h2 id="timeline-title">Start here. Explore from there.</h2></div><p id="shown" aria-live="polite"></p></div>
    <form class="filters" id="filters"><label for="availability">Show<select id="availability"><option value="all">All recommendations</option><option value="listed">Hoopla-listed matches</option><option value="missing">No confirmed match</option></select></label><label for="universe">Reading path<select id="universe"><option value="all">All continuities</option>${universes.map(universe => `<option value="${escape(universe)}">${escape(universe)}</option>`).join('')}</select></label><label class="check"><input id="starts-only" type="checkbox"> Starting points only</label><button id="reset" type="button">Reset filters</button></form>
    <div id="timeline" aria-live="polite"><p>Loading the reading guide…</p></div><noscript><p>Enable JavaScript to load catalog matches and filters.</p></noscript></section>
    <section class="sources"><p class="eyebrow">FOLLOW THE RESEARCH</p><h2>Sources & selection</h2><p>Each entry links recommendation and/or chronology evidence. Catalog links and exact ISBNs identify matching collections; notes describe partial coverage and overlap. Team stories can appear on several character pages—these are shared recommendations, not extra books to borrow. Research checked ${escape(checkedLabel)}.</p><ul id="sources"></ul></section>
  `, 'guide.js', `data-guide="${escape(slug)}"`);
  fs.writeFileSync(path.join(directory, `${slug}.html`), html);
}
const groups = ['Avengers', 'X-Men', 'More Marvel'];
const index = shell('Marvel reading guides', `<section class="hero"><p class="eyebrow">FIND YOUR NEXT STORY</p><h1>Your Marvel<br><em>reading guides.</em></h1><p class="lede">Reader recommendations and key stories, matched to your library and arranged in original publication order.</p><div class="stats"><span><strong>${guides.length}</strong> team & character guides</span><span>Source links in every guide</span><span>Library matches & catalog gaps</span></div></section><section class="guide-intro"><h2>Choose a team or follow a favorite.</h2><p>These member selections are an editorial starting set, not a popularity ranking. Characters cross between teams; the groups help you browse. Team stories may appear on several pages. Moon Knight, Black Knight, and Spider-Man have their own guides below.</p><label for="guide-search">Find a guide<input id="guide-search" type="search" placeholder="Search characters or teams…"></label><p id="guide-results" aria-live="polite">${guides.length} guides</p></section>${groups.map(group => `<section class="guide-group" data-group="${escape(group)}"><p class="eyebrow">${escape(group.toUpperCase())}</p><div class="guide-grid">${guides.filter(item => item.guide.group === group).sort((a,b) => (['avengers','x-men','fantastic-four','agents-of-shield'].includes(a.slug) ? -1 : ['avengers','x-men','fantastic-four','agents-of-shield'].includes(b.slug) ? 1 : a.guide.title.localeCompare(b.guide.title))).map(({slug, guide}) => {const matched = guide.stories.filter(story => story.isbns.some(isbn => byIsbn.get(isbn)?.hooplaListed)).length;return `<a class="guide-card" href="/reading-guides/${slug}.html" data-search="${escape((guide.title+' '+group+' '+guide.subtitle).toLowerCase())}"><span class="eyebrow">${['avengers','x-men','fantastic-four','agents-of-shield'].includes(slug) ? 'TEAM GUIDE' : 'CHARACTER GUIDE'}</span><h2>${escape(guide.title)} ↗</h2><p>${escape(guide.subtitle || '')}</p><small>${guide.stories.length} selections · ${matched} with Hoopla-listed matches</small></a>`}).join('')}</div></section>`).join('')}<p class="index-note">Library matches reflect the supplied September 8, 2026 catalog snapshot; verify current borrowing options through each collection’s catalog link. Research dates: October 27–30, 2026; each guide lists its own date.</p>`, 'index.js');
fs.writeFileSync(path.join(directory, 'index.html'), index);
const output = path.join(project, 'dist/client');
if (fs.existsSync(output)) fs.cpSync(directory, path.join(output, 'reading-guides'), {recursive:true});
console.log(`Validated and generated ${guides.length} guides; ${guides.reduce((sum, {guide}) => sum + guide.stories.length, 0)} selections. Copied to local build when present.`);
