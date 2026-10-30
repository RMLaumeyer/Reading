import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const project = fileURLToPath(new URL('../', import.meta.url));
const directory = path.join(project, 'public/reading-guides');
const catalog = JSON.parse(fs.readFileSync(path.join(project, 'public/catalog.json'), 'utf8'));
const renderer = fs.readFileSync(path.join(directory, 'guide.js'), 'utf8');
let count = 0;
for (const name of fs.readdirSync(directory).filter(name => name.endsWith('.json'))) {
  const guide = JSON.parse(fs.readFileSync(path.join(directory, name), 'utf8'));
  const elements = new Map();
  const element = id => {
    if (!elements.has(id)) elements.set(id, {value:'all',checked:false,innerHTML:'',textContent:'',events:{},addEventListener(type, callback){this.events[type] = callback;}});
    return elements.get(id);
  };
  const starts = [{events:{},addEventListener(type, callback){this.events[type] = callback;}}];
  const document = {body:{dataset:{guide:name.slice(0,-5)}},getElementById:element,querySelectorAll:() => starts};
  await vm.runInNewContext(renderer, {document,location:{hash:''},URL,fetch:async url => ({ok:true,json:async () => url === '/catalog.json' ? catalog : guide})});
  const shown = () => (element('timeline').innerHTML.match(/<article /g) || []).length;
  const change = () => element('filters').events.change();
  const reset = () => element('reset').events.click();
  assert.equal(shown(),guide.stories.length,`${name}: initial rendering`);
  assert(!element('timeline').innerHTML.includes('undefined'), `${name}: missing rendered field`);
  element('availability').value = 'listed'; change();
  assert.equal(shown(),guide.stories.filter(story => story.isbns.some(isbn => catalog.books.some(book => book.isbn === isbn && book.hooplaListed))).length,`${name}: availability`);
  reset(); element('availability').value = 'missing'; change();
  assert.equal(shown(),guide.stories.filter(story => !story.isbns.length).length,`${name}: gaps`);
  reset(); element('universe').value = guide.stories[0].universe; change();
  assert.equal(shown(),guide.stories.filter(story => story.universe === guide.stories[0].universe).length,`${name}: continuity`);
  reset(); element('starts-only').checked = true; change();
  assert.equal(shown(),guide.stories.filter(story => story.start).length,`${name}: starting points`);
  element('availability').value = 'missing'; starts[0].events.click();
  assert.equal(shown(),guide.stories.length,`${name}: quickstart resets filters`);
  count++;
}
console.log(`All ${count} guides: catalog rendering, availability, missing matches, continuity, starting points, reset, and quickstart passed.`);
