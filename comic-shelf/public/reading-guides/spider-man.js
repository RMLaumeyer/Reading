const byId = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = (url) => { try { const parsed = new URL(url); return parsed.protocol === 'https:' ? escapeHtml(parsed.href) : '#'; } catch { return '#'; } };
async function loadJson(url) { const response = await fetch(url); if (!response.ok) throw new Error(`Could not load ${url}`); return response.json(); }
Promise.all([loadJson('/reading-guides/spider-man.json'), loadJson('/catalog.json')]).then(([guide, catalog]) => {
  const booksByIsbn = new Map(catalog.books.map(book => [book.isbn, book]));
  const stories = guide.stories.map((story, index) => ({...story, index, books: story.isbns.map(isbn => booksByIsbn.get(isbn)).filter(Boolean)}));
  const listed = story => story.books.some(book => book.hooplaListed);
  const availableCount = stories.filter(listed).length;
  byId('stats').innerHTML = `<span><strong>${stories.length}</strong> selected stories</span><span><strong>${availableCount}</strong> with Hoopla-listed matches</span><span><strong>${stories.filter(s => !s.books.length).length}</strong> catalog gaps to check</span>`;
  byId('sources').innerHTML = Object.values(guide.sources).map(source => `<li><a href="${safeUrl(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)} ↗</a></li>`).join('');
  function render() {
    const availability = byId('availability').value;
    const universe = byId('universe').value;
    const selected = stories.filter(story => (availability !== 'listed' || listed(story)) && (availability !== 'missing' || !story.books.length) && (!byId('starts-only').checked || story.start) && (universe === 'all' || (universe === 'main' ? story.universe.startsWith('Main') : universe === 'alternate' ? story.universe.startsWith('Alternate') : story.universe.includes(universe))));
    byId('shown').textContent = `${selected.length} of ${stories.length} stories · oldest first`;
    byId('timeline').innerHTML = selected.length ? selected.map(story => `<article class="story" id="${escapeHtml(story.id)}"><div class="year"><span class="number">${String(story.index + 1).padStart(2,'0')} /</span>${story.year}</div><div class="story-body"><div class="badges"><span class="badge">${escapeHtml(story.universe)}</span>${story.start ? '<span class="badge start">STARTING POINT</span>' : ''}<span class="badge ${listed(story) ? 'available' : 'gap'}">${listed(story) ? 'HOOPLA LISTED' : story.books.length ? 'LISTING UNCONFIRMED' : 'NO CONFIRMED MATCH'}</span></div><h3>${escapeHtml(story.title)}</h3><p class="issues">${escapeHtml(story.date)} · ${escapeHtml(story.issues)}</p><p>${escapeHtml(story.why)}</p><div class="matches"><h4>${story.books.length ? 'IN YOUR LIBRARY CATALOG' : 'LIBRARY MATCH TO CHECK'}</h4>${story.books.map(book => `<div class="book"><a href="${safeUrl(book.catalogUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(book.title)} ↗</a><small>ISBN ${escapeHtml(book.isbn)} · ${book.hooplaListed ? 'Hoopla listed in supplied export' : 'Hoopla not confirmed in supplied export'}</small></div>`).join('')}<p class="match-note">${escapeHtml(story.match)}</p></div><p class="evidence">Evidence: ${story.sources.map(key => {const source = guide.sources[key];return `<a href="${safeUrl(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)} ↗</a>`}).join('')}</p></div></article>`).join('') : '<p class="empty">No stories match these filters. Reset filters to see the full guide.</p>';
  }
  byId('filters').addEventListener('submit', event => event.preventDefault());
  byId('filters').addEventListener('change', render);
  byId('reset').addEventListener('click', () => { byId('availability').value = 'all'; byId('universe').value = 'all'; byId('starts-only').checked = false; render(); });
  document.querySelectorAll('.start-options a').forEach(link => link.addEventListener('click', () => { byId('availability').value = 'all'; byId('universe').value = 'all'; byId('starts-only').checked = false; render(); }));
  render();
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
}).catch(error => { byId('stats').textContent = 'Catalog could not be loaded.'; byId('timeline').textContent = `${error.message}. Reload this page from the running Panel site to try again.`; });
