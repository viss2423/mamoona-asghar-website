'use strict';
const list = document.querySelector('#publication-list');
const search = document.querySelector('#publication-search');
const year = document.querySelector('#publication-year');
const count = document.querySelector('#result-count');
let articles = [];
function safeLink(value) {
  try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.href : null; } catch { return null; }
}
function render() {
  const query = search.value.trim().toLowerCase();
  const matches = articles.filter(a => (!year.value || String(a.year) === year.value) && [a.title, a.authors, a.publication].join(' ').toLowerCase().includes(query));
  list.replaceChildren();
  for (const a of matches) {
    const item = document.createElement('li');
    const heading = document.createElement('h3');
    const link = document.createElement('a');
    link.textContent = a.title;
    const href = safeLink(a.link); if (href) link.href = href;
    heading.append(link);
    const authors = document.createElement('p'); authors.textContent = a.authors || '';
    const venue = document.createElement('p'); venue.className = 'venue';
    venue.textContent = [a.publication, a.year, a.citations == null ? '' : `${a.citations} citations`].filter(Boolean).join(' · ');
    item.append(heading, authors, venue); list.append(item);
  }
  count.textContent = matches.length ? `${matches.length} publication${matches.length === 1 ? '' : 's'}` : 'No publications match your search.';
}
async function loadPublications() {
  try {
    const response = await fetch('publications.json');
    if (!response.ok) throw new Error('Publication data unavailable');
    const data = await response.json();
    if (!Array.isArray(data.articles) || !data.articles.length) throw new Error('Publication list empty');
    articles = data.articles;
    for (const value of [...new Set(articles.map(a => String(a.year || '')).filter(Boolean))].sort().reverse()) {
      const option = document.createElement('option'); option.value = value; option.textContent = value; year.append(option);
    }
    if (data.mode === 'scholar') document.querySelector('#publication-note').textContent = `Publications from Google Scholar. Last checked ${data.updated}.`;
    search.addEventListener('input', render); year.addEventListener('change', render); render();
  } catch {
    count.textContent = 'Showing selected publications. Visit Google Scholar for the complete list.';
    search.disabled = true; year.disabled = true;
  }
}
loadPublications();
