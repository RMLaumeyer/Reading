import assert from 'node:assert/strict';
const base='http://127.0.0.1:5173/api/enrichment';
const post=(action,headers={})=>fetch(base+'/'+action,{method:'POST',headers});
assert.equal((await post('start')).status,403);
assert.equal((await post('start',{'X-Panel-Local':'1',Origin:'https://example.com'})).status,403);
assert.equal((await fetch(base+'/start')).status,405);
assert.equal((await post('unknown',{'X-Panel-Local':'1'})).status,404);
const before=await (await fetch(base+'/status')).json();
assert.equal(before.active,false,'Run this check with the worker idle.');
const started=await post('start',{'X-Panel-Local':'1'});assert.equal(started.status,202);
assert.equal((await post('start',{'X-Panel-Local':'1'})).status,409);
assert.equal((await post('pause',{'X-Panel-Local':'1'})).status,200);
let paused;
for(let i=0;i<45;i++){
  await new Promise(resolve=>setTimeout(resolve,1000));
  paused=await(await fetch(base+'/status')).json();
  if(!paused.active)break;
}
assert.equal(paused.active,false,'Worker should honor pause at its next checkpoint.');
assert.equal(paused.status,'paused');
assert.equal((await post('start',{'X-Panel-Local':'1'})).status,202);
console.log('Local access, duplicate-start protection, pause and resume passed. Collector resumed.');
