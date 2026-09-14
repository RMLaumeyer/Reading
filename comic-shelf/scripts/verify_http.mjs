import assert from 'node:assert/strict';
const base='http://localhost:5173';
const health=await fetch(base+'/health');assert.equal(health.status,200);assert.equal((await health.json()).app,'panel-comic-shelf');
const response=await fetch(base+'/');assert.equal(response.status,200);const html=await response.text();assert.ok(html.includes('Panel'));
const queue=[...html.matchAll(/(?:src|href)="([^"<>]+)"/g)].map(m=>m[1].replaceAll('&amp;','&')).filter(p=>p.startsWith('/')&&!p.startsWith('//'));
const seen=new Set();
while(queue.length){const pathname=queue.shift();if(seen.has(pathname))continue;seen.add(pathname);const url=new URL(pathname,base);assert.equal(url.origin,base);const r=await fetch(url);assert.equal(r.status,200,`Asset unavailable: ${pathname}`);if(url.pathname.endsWith('.js')){const js=await r.text();for(const m of js.matchAll(/(?:from\s*|import\s*\()?["'](\.?\.?\/[^"']+\.js)["']/g)){const child=new URL(m[1],url);if(child.origin===base)queue.push(child.pathname)}}}
const catalog=await(await fetch(base+'/catalog.json')).json();const enrich=await(await fetch(base+'/enrichment.json')).json();assert.equal(catalog.books.length,4000);assert.ok(Object.keys(enrich.books).length>=26);
for(const pathname of ['/scripts/build_pilot.py','/data/cache/midnight.html','/%2e%2e%5cscripts/start.ps1']){const r=await fetch(base+pathname);assert.ok([400,403,404].includes(r.status),`Source exposed: ${pathname}`)}
assert.equal((await fetch(base+'/catalog.json',{method:'POST'})).status,405);
console.log(`Production HTTP checks passed: ${seen.size} linked assets, 4,000 catalog records, ${Object.keys(enrich.books).length} enriched books, source files inaccessible.`);
