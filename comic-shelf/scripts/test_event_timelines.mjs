import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const directory = path.join(root,'public/event-timelines');
const catalog = JSON.parse(fs.readFileSync(path.join(root,'public/catalog.json'),'utf8'));
const renderer = fs.readFileSync(path.join(directory,'event.js'),'utf8');
let count = 0;
for (const file of fs.readdirSync(directory).filter(file=>file.endsWith('.json'))) {
  const event = JSON.parse(fs.readFileSync(path.join(directory,file),'utf8'));
  const elements = new Map();
  function element(id){if(!elements.has(id))elements.set(id,{value:'all',innerHTML:'',textContent:'',events:{},addEventListener(type,callback){this.events[type]=callback;}});return elements.get(id);}
  await vm.runInNewContext(renderer,{document:{body:{dataset:{event:file.slice(0,-5)}},getElementById:element},URL,fetch:async url=>({ok:true,json:async()=>url==='/catalog.json'?catalog:event})});
  const shown=()=>(element('timeline').innerHTML.match(/<article /g)||[]).length;
  const change=()=>element('filters').events.change();
  const reset=()=>element('reset').events.click();
  assert.equal(shown(),event.steps.length,`${file}: initial route`);
  assert(!element('timeline').innerHTML.includes('undefined'),`${file}: rendered fields`);
  for(const step of event.steps)for(const item of step.order||[])assert(element('timeline').innerHTML.includes(item.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))),`${file}: issue-order block`);
  element('route').value='core';change();
  assert.equal(shown(),event.steps.filter(step=>step.role==='Core').length,`${file}: core`);
  element('route').value='recommended';change();
  assert.equal(shown(),event.steps.filter(step=>step.role!=='Optional').length,`${file}: expanded`);
  reset();element('availability').value='listed';change();
  assert.equal(shown(),event.steps.filter(step=>step.isbns.some(isbn=>catalog.books.some(book=>book.isbn===isbn&&book.hooplaListed))).length,`${file}: Hoopla filter respects print records`);
  reset();element('availability').value='missing';change();
  assert.equal(shown(),event.steps.filter(step=>!step.isbns.length).length,`${file}: catalog gaps`);
  reset();element('phase').value='Aftermath';change();
  assert.equal(shown(),event.steps.filter(step=>step.phase==='Aftermath').length,`${file}: aftermath`);
  if(event.steps.some(step=>step.era)){
    reset();const era=event.steps.find(step=>step.era).era;element('era').value=era;change();
    assert.equal(shown(),event.steps.filter(step=>step.era===era).length,`${file}: story arc`);
    element('route').value='core';change();
    assert.equal(shown(),event.steps.filter(step=>step.era===era&&step.role==='Core').length,`${file}: core story arc`);
  }
  reset();assert.equal(shown(),event.steps.length,`${file}: reset`);
  count++;
}
const hickman=JSON.parse(fs.readFileSync(path.join(directory,'hickman-secret-wars.json'),'utf8'));
const infinity=hickman.steps.find(step=>step.id==='infinity');
assert(infinity.order.indexOf('Infinity #1')<infinity.order.indexOf('New Avengers #8'),'Infinity: place NA8 after Infinity1');
assert(hickman.steps.find(step=>step.id==='time-four').isbns.includes('9780785192244'),'Time Runs Out must include the final volume');
assert(hickman.steps.at(-1).issues.includes('#1–9'),'Secret Wars must reach #9');
const civil=JSON.parse(fs.readFileSync(path.join(directory,'civil-war.json'),'utf8'));
assert(civil.steps.findIndex(step=>step.id==='cap25')<civil.steps.findIndex(step=>step.id==='confession'),'Confession follows Captain America25');
const krakoa=JSON.parse(fs.readFileSync(path.join(directory,'krakoa-era.json'),'utf8'));
assert(krakoa.steps[0].issues.includes('House of X'),'Krakoa must begin with House/Powers');
assert(krakoa.steps.at(-1).issues.includes('#35'),'Krakoa must continue past Inferno through the final epilogue');
assert.equal(krakoa.steps.filter(step=>/Hellfire Gala\s?202[123]/.test(step.era)).length,3,'Krakoa must include all three Gala turns');
assert(krakoa.steps.find(step=>step.id==='immortal-six-gap').isbns.length===0,'Do not silently claim Immortal6 is matched');
const messiah=JSON.parse(fs.readFileSync(path.join(directory,'mutant-messiah-saga.json'),'utf8'));
for(const [id,chapters]of [['messiah-complex',13],['messiah-war',7],['second-coming',14]])assert.equal(messiah.steps.find(step=>step.id===id).order.length,chapters,`Complete ${id} crossover order`);
const cosmic=JSON.parse(fs.readFileSync(path.join(directory,'cosmic-war-of-kings.json'),'utf8'));
assert(cosmic.steps.some(step=>step.issues.includes('Ignition')),'Thanos Imperative includes its opening one-shot');
assert(cosmic.steps.some(step=>step.issues.includes('Devastation')),'Cosmic route includes the closing one-shot');
console.log(`All ${count} timelines: routes, issue-order rendering, format-aware availability, gaps, story arcs, phases and reset passed. Key crossover/era completeness checks passed.`);
