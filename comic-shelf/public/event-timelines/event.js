import { queueKey, readQueue } from '../reading-queue.js';
import { routeCoverage } from './issue-coverage.js';

const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = value => {try {const url = new URL(value);return url.protocol === 'https:' ? escapeHtml(url.href) : '#';}catch{return '#';}};
export async function initEventTimeline(doc, fetcher, view) {
  const byId = id => doc.getElementById(id);
  const slug = doc.body.dataset.event;
  async function loadJson(url) {
    const response = await fetcher(url);
    if (!response.ok) throw new Error('Could not load ' + url);
    return response.json();
  }
  const progress = slug === 'hickman-secret-wars' ? byId('route-progress') : null;
  const coverageRequest = progress ? loadJson('/hickman-coverage.json').catch(() => null) : null;
  return Promise.all([loadJson('/event-timelines/' + slug + '.json'), loadJson('/catalog.json'), coverageRequest]).then(([event, catalog, coverage]) => {
  const byIsbn = new Map(catalog.books.map(book => [book.isbn,book]));
  const steps = event.steps.map((step,index) => ({...step,index,books:step.isbns.map(isbn => byIsbn.get(isbn)).filter(Boolean)}));
  const listed = step => step.books.some(book => book.hooplaListed);
  byId('stats').innerHTML = `<span><strong>${steps.length}</strong> selected stages</span><span><strong>${steps.filter(step=>step.role==='Core').length}</strong> core stages</span><span><strong>${steps.filter(listed).length}</strong> with Hoopla-listed matches</span><span><strong>${steps.filter(step=>!step.books.length).length}</strong> catalog gaps</span>`;
  byId('sources').innerHTML = Object.values(event.sources).map(source => `<li><a href="${safeUrl(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)} ↗</a></li>`).join('');
  function borrowingLink(book, edition) {
    if (edition?.hoopla) return `<a href="${safeUrl(edition.hoopla.url)}" target="_blank" rel="noopener noreferrer">Open Hoopla ↗</a>`;
    return `<a href="${safeUrl(book.catalogUrl)}" target="_blank" rel="noopener noreferrer">Open library record ↗</a>`;
  }
  function issueList(issues) {
    return `<ul class="coverage-issues">${issues.map(issue => `<li>${escapeHtml(issue)}</li>`).join('')}</ul>`;
  }
  function renderBook(book) {
    const edition = coverage?.editions[book.isbn];
    const format = book.hooplaListed ? "Hoopla listed in export" : "Hoopla not confirmed in export";
    const details = edition ? `<details class="issue-order"><summary>${edition.issueKeys.length} confirmed collected issues</summary>
      ${issueList(edition.issueKeys)}${edition.note ? `<p>${escapeHtml(edition.note)}</p>` : ""}
      <a href="${safeUrl(edition.source.url)}" target="_blank" rel="noopener noreferrer">Edition contents source ↗</a></details>` : "";
    const direct = edition?.hoopla ? `<div>${borrowingLink(book, edition)}</div>` : "";
    return `<div class="book" data-reading-id="${escapeHtml(book.id)}"><a href="${safeUrl(book.catalogUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(book.title)} ↗</a>
      <small>ISBN ${escapeHtml(book.isbn)} · ${escapeHtml(book.format || "Check format")} · ${format}</small>${direct}${details}</div>`;
  }
  function renderProgress() {
    if (!progress) return;
    if (!coverage) { progress.textContent = "Issue coverage could not be loaded."; return; }
    let queue = {};
    let queueMessage = "";
    try { queue = readQueue(view.localStorage); }
    catch { queueMessage = "<p>Saved reading progress could not be loaded.</p>"; }
    const result = routeCoverage(steps, coverage, byIsbn, queue);
    const gaps = result.missing.length ? `<details><summary>Missing verified collection coverage (${result.missing.length})</summary>${issueList(result.missing)}</details>` : "";
    let recommendation = "<p>Core route complete.</p>";
    if (result.next) {
      const { book, edition } = result.next;
      recommendation = `<p><strong>Next collection</strong> · ${escapeHtml(book.title)}</p>
        <p>Pick up at ${escapeHtml(result.nextIssue)} · ${escapeHtml(result.stage.title)}</p>
        <p>${result.adds.length} new core ${result.adds.length === 1 ? "issue" : "issues"} · ${result.repeats.length} already read</p>
        <div>${borrowingLink(book, edition)}</div>
        <details><summary>Issues this collection adds or repeats</summary>
          <p>New core issues</p>${issueList(result.adds)}
          ${result.repeats.length ? `<p>Already read</p>${issueList(result.repeats)}` : ""}</details>`;
    } else if (result.nextIssue) {
      recommendation = `<p>Still to read · ${escapeHtml(result.nextIssue)}. No verified collection match yet.</p>`;
    }
    progress.innerHTML = `<p aria-live="polite"><strong>${result.read} of ${result.total} core issues read</strong> · ${result.fullyMappedStages} of ${steps.filter(step => step.role === "Core").length} stages covered by verified collections</p>
      ${recommendation}${gaps}${queueMessage}`;
  }
  if (progress) {
    const alternatives = byId('route-alternatives');
    if (coverage && alternatives) {
      const matches = coverage.alternatives.map(isbn => byIsbn.get(isbn)).filter(Boolean);
      alternatives.innerHTML = matches.length ? `<details class="issue-order">
        <summary>Compare larger collections</summary>
        <p>These editions combine several stages. Check the issues you still need before choosing a book.</p>
        ${matches.map(renderBook).join('')}
      </details>` : '';
    }
    view.addEventListener("panel:reading-queue-change", renderProgress);
    view.addEventListener("storage", event => { if (event.key === queueKey || event.key === null) renderProgress(); });
    renderProgress();
  }
  function render(){
    const route = byId('route').value, availability = byId('availability').value, phase = byId('phase').value, era = byId('era')?.value || 'all';
    const visible = steps.filter(step => (route === 'all' || (route === 'core' ? step.role === 'Core' : step.role !== 'Optional')) && (availability !== 'listed' || listed(step)) && (availability !== 'missing' || !step.books.length) && (phase === 'all' || phase === step.phase) && (era === 'all' || era === step.era));
    byId('shown').textContent = `${visible.length} of ${steps.length} stages · reading sequence`;
    byId('timeline').innerHTML = visible.length ? visible.map(step => `<article class="story event-step" id="${escapeHtml(step.id)}"><div class="year"><span class="number">STAGE</span>${String(step.index+1).padStart(2,'0')}<span class="stage-date">${escapeHtml(step.date)}</span></div><div class="story-body"><div class="badges">${step.era?`<span class="badge era">${escapeHtml(step.era)}</span>`:''}<span class="badge ${step.role==='Core'?'core':''}">${escapeHtml(step.role.toUpperCase())}</span><span class="badge">${escapeHtml(step.phase)}</span><span class="badge ${listed(step)?'available':'gap'}">${listed(step)?'HOOPLA LISTED':step.books.length?'CATALOG MATCH · CHECK FORMAT':'NO CONFIRMED MATCH'}</span></div><h3>${escapeHtml(step.title)}</h3><p class="issues">${escapeHtml(step.issues)}</p><p>${escapeHtml(step.why)}</p>${step.order?.length?`<details class="issue-order"><summary>Issue order · ${step.order.length} reading blocks</summary><ol>${step.order.map(item=>`<li>${escapeHtml(item)}</li>`).join('')}</ol></details>`:''}<div class="matches"><h4>${step.books.length?'IN YOUR LIBRARY CATALOG':'LIBRARY MATCH TO CHECK'}</h4>${step.books.map(renderBook).join('')}<p class="match-note">${escapeHtml(step.match)}</p></div><p class="evidence">Evidence: ${step.sources.map(key=>{const source=event.sources[key];return `<a href="${safeUrl(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)} ↗</a>`;}).join('')}</p></div></article>`).join('') : '<p class="empty">No stages match these filters. Reset filters to see the complete selected timeline.</p>';
  }
  byId('filters').addEventListener('submit', e=>e.preventDefault());
  byId('filters').addEventListener('change',render);
  byId('reset').addEventListener('click',()=>{byId('route').value='all';byId('availability').value='all';byId('phase').value='all';if(byId('era'))byId('era').value='all';render();});
  render();
}).catch(error=>{byId('stats').textContent='Timeline data could not be loaded.';byId('timeline').textContent=`${error.message}. Reload from the running Panel site.`;});

}

if (typeof document !== "undefined") void initEventTimeline(document, fetch, window);
