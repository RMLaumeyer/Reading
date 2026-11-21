import { readQueue, saveStatus, queueKey, statuses } from './reading-queue.js';
function refresh() {
 let queue; try { queue = readQueue(); } catch { queue = {}; }
 document.querySelectorAll('[data-reading-id]').forEach(book => {
  let select = book.querySelector('select');
  if (!select) {
   const label = document.createElement('label'); label.className = 'reading-control'; label.textContent = 'Reading status ';
   select = document.createElement('select'); select.setAttribute('aria-label', 'Reading status for ' + book.querySelector('a').textContent);
   statuses.forEach(([value,text]) => select.add(new Option(text,value)));
   const message = document.createElement('span'); message.setAttribute('role','status');
   select.addEventListener('change', () => {
    try {
      saveStatus(book.dataset.readingId, select.value);
      message.textContent = 'Saved';
      refresh();
      window.dispatchEvent(new Event('panel:reading-queue-change'));
    }
    catch { message.textContent = 'Could not save progress. Check browser storage access.'; }
   });
   label.append(select,message); book.append(label);
  }
  select.value = queue[book.dataset.readingId]?.status || 'none';
 });
}
const timeline = document.getElementById('timeline');
if (timeline) {
 const observer = new MutationObserver(refresh);
 observer.observe(timeline, {childList: true});
 const alternatives = document.getElementById('route-alternatives');
 if (alternatives) observer.observe(alternatives, {childList: true});
 window.addEventListener('storage', e => { if (e.key === queueKey || e.key === null) refresh(); });
 refresh();
}
