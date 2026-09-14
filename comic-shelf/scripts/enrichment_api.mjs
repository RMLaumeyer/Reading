import { readFile, writeFile, unlink, access, open } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import os from 'node:os';

export function enrichmentApi(project) {
  let child = null;
  let starting = false;
  let failure = '';
  const flag = path.join(project, 'data/pause-auto-enrichment');
  async function status() {
    let state = {status:'idle',processed:0,total:4000,reviewCount:0,pendingLookups:0,automatic:0,editorial:0,message:'Ready to process saved descriptions and look up missing editions.'};
    try { state=JSON.parse(await readFile(path.join(project,'public/auto-enrichment-status.json'),'utf8')); } catch {}
    let alive=!!child || starting;
    if (!alive && state.status==='running' && state.pid) {
      try { process.kill(state.pid,0); alive=true; } catch {}
    }
    if (state.status==='running' && !alive) state={...state,status:'paused',message:'The worker stopped. Resume to continue from saved progress.'};
    if (failure) state={...state,status:'paused',message:failure};
    return {...state,active:alive};
  }
  return async (req,res,url) => {
    if (!url.pathname.startsWith('/api/enrichment')) return false;
    const reply=(code,body)=>{res.writeHead(code,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(body));return true;};
    const allowed=new Set(['127.0.0.1:5173','localhost:5173']);
    if (!allowed.has(req.headers.host)) return reply(403,{message:'Local access only.'});
    if (url.pathname==='/api/enrichment/status' && req.method==='GET') return reply(200,await status());
    if (req.method!=='POST') return reply(405,{message:'Use POST for enrichment controls.'});
    if (req.headers['x-panel-local']!=='1' || (req.headers.origin && !['http://127.0.0.1:5173','http://localhost:5173'].includes(req.headers.origin))) return reply(403,{message:'Open these controls in Panel on this computer.'});
    if (!['/api/enrichment/start','/api/enrichment/retry','/api/enrichment/pause'].includes(url.pathname)) return reply(404,{message:'Unknown action.'});
    if (url.pathname.endsWith('/pause')) {
      await writeFile(flag,'pause'); return reply(200,{...(await status()),message:'Pause requested. The current lookup will finish and be saved.'});
    }
    if ((await status()).active) return reply(409,{message:'Enrichment is already running.'});
    starting=true; failure='';
    try {
      let python=path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe');
      try { await access(python); } catch { python='python'; }
      await unlink(flag).catch(e=>{if(e.code!=='ENOENT')throw e;});
      const log=await open(path.join(project,'auto-enrichment.log'),'a');
      try {
        child=spawn(python,[path.join(project,'scripts/auto_enrich.py'),...(url.pathname.endsWith('/retry')?['--retry']:[])],{cwd:project,windowsHide:true,stdio:['ignore',log.fd,log.fd]});
        child.once('error',()=>{failure='Unable to start the collector. Check that Python is installed.';child=null;});
        child.once('exit',(code)=>{child=null;if(code)failure=code===2?'Another collector is running. Pause or finish that collector before starting this one.':'Collector stopped. Results are saved; resume to continue.';});
      } finally { await log.close(); }
      return reply(202,{...(await status()),active:true,status:'running',message:'Starting. Saved work will be reused.'});
    } catch {
      failure='Unable to start enrichment. Check auto-enrichment.log.';return reply(500,{message:failure});
    } finally { starting=false; }
  };
}
