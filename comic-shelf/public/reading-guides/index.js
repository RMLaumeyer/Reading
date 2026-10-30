const search = document.getElementById('guide-search');
search.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase();
  let visible = 0;
  document.querySelectorAll('.guide-card').forEach(card => {card.hidden = !card.dataset.search.includes(query); if (!card.hidden) visible++;});
  document.querySelectorAll('.guide-group').forEach(group => {group.hidden = !Array.from(group.querySelectorAll('.guide-card')).some(card => !card.hidden);});
  document.getElementById('guide-results').textContent = visible ? `${visible} guides` : 'No guides match. Try a character name or team.';
});
