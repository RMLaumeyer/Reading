const search=document.getElementById('event-search');
const cards=Array.from(document.querySelectorAll('.event-grid .guide-card'));
search?.addEventListener('input',()=>{
  const query=search.value.trim().toLowerCase();let count=0;
  for(const card of cards){card.hidden=!card.dataset.search.includes(query);if(!card.hidden)count++;}
  document.getElementById('event-results').textContent=count?`${count} timelines`:'No timelines match. Try an event, team, or era name.';
});
