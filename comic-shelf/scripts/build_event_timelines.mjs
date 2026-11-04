import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const directory = path.join(root, 'public/event-timelines');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'public/catalog.json'), 'utf8'));
const books = new Map(catalog.books.map(book => [book.isbn, book]));
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const events = fs.readdirSync(directory).filter(file => file.endsWith('.json')).map(file => {
  const event = JSON.parse(fs.readFileSync(path.join(directory, file), 'utf8'));
  const slug = file.slice(0, -5);
  assert(/^[a-z0-9-]+$/.test(slug));
  for (const field of ['title','subtitle','years','checkedAt','intro']) assert(event[field], `${slug}: ${field}`);
  assert(event.steps.length && event.steps.some(step => step.role === 'Core'), `${slug}: core route`);
  const ids = new Set();
  for (const step of event.steps) {
    assert(step.id && !ids.has(step.id), `${slug}: duplicate ID`); ids.add(step.id);
    assert(['Core','Recommended','Optional'].includes(step.role), `${slug}: role`);
    assert(['Setup','Main event','Aftermath'].includes(step.phase), `${slug}: phase`);
    assert(Number.isInteger(step.year), `${slug}: year`);
    for (const field of ['title','issues','date','why','match']) assert(typeof step[field] === 'string' && step[field], `${slug}: ${field}`);
    assert(Array.isArray(step.isbns) && step.sources.length, `${slug}: evidence`);
    for (const isbn of step.isbns) assert(books.has(isbn), `${slug}: missing ISBN ${isbn}`);
    for (const key of step.sources) assert(event.sources[key], `${slug}: unknown source ${key}`);
    if (step.order) assert(Array.isArray(step.order) && step.order.every(item => typeof item === 'string'), `${slug}: issue order`);
  }
  for (const source of Object.values(event.sources)) assert(new URL(source.url).protocol === 'https:', `${slug}: source URL`);
  return {slug, event};
});
function shell(title, content, script, attributes = '') {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} · Panel</title><link rel="stylesheet" href="/reading-guides/style.css"><link rel="stylesheet" href="/event-timelines/style.css"><script src="/event-timelines/${script}" defer></script></head><body id="top" ${attributes}><header><a class="brand" href="/">▤ PANEL <span>/ event timelines</span></a><nav aria-label="Main navigation"><a href="/">Shelf</a><a href="/reading-guides/">Character guides</a><a href="/event-timelines/" aria-current="page">Event timelines</a></nav></header><main>${content}</main><footer>PANEL / Follow the whole story. <a href="/event-timelines/">All event timelines →</a></footer></body></html>`;
}
for (const {slug, event} of events) {
  const html = shell(`${event.title} timeline`, `
    <section class="hero"><p class="eyebrow">MARVEL / EVENT TIMELINE / ${escape(event.years)}</p><h1>${escape(event.title)}<br><em>Follow the story.</em></h1><p class="lede">${escape(event.subtitle)}</p><div class="stats" id="stats" aria-live="polite">Matching library collections…</div></section>
    <section class="event-intro"><h2>Your route through the event.</h2><p>${escape(event.intro)}</p><div class="route-legend"><span class="badge core">CORE · selected main route</span><span class="badge">RECOMMENDED · useful context</span><span class="badge">OPTIONAL · expand when interested</span></div></section>
    <section class="method"><h2>Use the sequence, then check the collection.</h2><p>Stages are in the recommended reading sequence, not simply sorted by publication date. <strong>Core is defined for this selected route</strong>: on the Hickman page it includes the lead-up saga, while on a self-contained event it can be the main miniseries alone. Expand “Issue order” where chapters cross between books. Optional tie-ins with repeated main-series anchors are alternate expansion paths, not instructions to reread those chapters after finishing the event. Read each match note before borrowing: some books overlap, some continue one another, and some provide only part of a stage.</p><p>Library matches use your supplied catalog snapshot, imported September 8, 2026. A catalog match can be a print record. <strong>“Hoopla listed” is not a live availability check.</strong> Unmatched stages stay visible; this does not prove the library lacks them. Story names may reveal turning points. Research checked ${escape(event.checkedAt)}.</p></section>
    <section aria-labelledby="timeline-title"><div class="timeline-heading"><div><p class="eyebrow">THE READING SEQUENCE</p><h2 id="timeline-title">One stage at a time.</h2></div><p id="shown" aria-live="polite"></p></div>
    <form class="filters" id="filters"><label for="route">Route<select id="route"><option value="all">Full selected timeline</option><option value="core">Core route only</option><option value="recommended">Core + recommended context</option></select></label><label for="availability">Library match<select id="availability"><option value="all">All stages</option><option value="listed">Hoopla-listed stages</option><option value="missing">No confirmed match</option></select></label><label for="phase">Phase<select id="phase"><option value="all">All phases</option><option>Setup</option><option>Main event</option><option>Aftermath</option></select></label><button id="reset" type="button">Reset filters</button></form>
    <div id="timeline" aria-live="polite"><p>Loading event timeline…</p></div><noscript><p>Enable JavaScript to load this timeline’s catalog matches and filters.</p></noscript></section>
    <section class="sources"><p class="eyebrow">FOLLOW THE RESEARCH</p><h2>Reading-order sources</h2><p>Sources document the event route and collection contents. Adjacent parallel chapters can have more than one reasonable arrangement. The selected timeline keeps the main story clear and marks optional extensions.</p><ul id="sources"></ul></section>
  `, 'event.js', `data-event="${escape(slug)}"`);
  fs.writeFileSync(path.join(directory, `${slug}.html`), html);
}
const index = shell('Marvel event timelines', `<section class="hero"><p class="eyebrow">THE BIG STORIES / MARVEL</p><h1>Follow the thread.<br><em>Event timelines.</em></h1><p class="lede">From the first setup to the finale: reading sequences, interwoven chapters, and library collections for Marvel’s major stories.</p><div class="stats"><span><strong>${events.length}</strong> event routes</span><span>Core & optional paths</span><span>Exact catalog matches</span></div></section><section class="guide-intro"><h2>Choose your next big story.</h2><p>Start with the full selected timeline, or switch to the core route. Each page separates setup, main event, and aftermath. The two Civil Wars are distinct events; the original Infinity Gauntlet is separate from Hickman’s Infinity.</p></section><section class="guide-grid event-grid">${events.sort((a,b) => Math.min(...a.event.steps.filter(s=>s.role==='Core').map(s=>s.year)) - Math.min(...b.event.steps.filter(s=>s.role==='Core').map(s=>s.year))).map(({slug,event}) => {const core = event.steps.filter(step => step.role === 'Core');const matched = event.steps.filter(step => step.isbns.length);return `<a class="guide-card" href="/event-timelines/${slug}.html"><span class="eyebrow">${escape(event.years)}</span><h2>${escape(event.title)} ↗</h2><p>${escape(event.subtitle)}</p><small>${event.steps.length} stages · ${core.length} core · ${matched.length} with catalog matches</small></a>`;}).join('')}</section><p class="index-note">Looking for a hero’s best starting points? <a href="/reading-guides/">Browse the character and team guides →</a></p>`, 'index.js');
fs.writeFileSync(path.join(directory, 'index.html'), index);
if (fs.existsSync(path.join(root, 'dist/client'))) fs.cpSync(directory, path.join(root, 'dist/client/event-timelines'), {recursive:true});
console.log(`Validated and generated ${events.length} event timelines; ${events.reduce((sum,{event}) => sum + event.steps.length,0)} stages.`);
