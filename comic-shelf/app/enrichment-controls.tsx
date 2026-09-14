'use client';
import { useEffect, useState } from 'react';
type Status = {status:string; active:boolean; processed:number; total:number; automatic:number; editorial:number; reviewCount:number; pendingLookups:number; message:string; current?:string};
type Item = {id:string; title:string; reasons:string[]; status:string};
export default function EnrichmentControls({onSelect}:{onSelect:(id:string)=>void}) {
  const [status,setStatus]=useState<Status|null>(null);
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);
  const [show,setShow]=useState(false);
  const [queue,setQueue]=useState<Item[]>([]);
  const [filter,setFilter]=useState('all');
  const [page,setPage]=useState(1);
  useEffect(()=>{
    const abort=new AbortController();
    async function refresh() {
      try {
        const r=await fetch('/api/enrichment/status',{signal:abort.signal});
        if (!r.ok) throw Error('Enrichment controls are unavailable. Relaunch Panel with Start Panel.cmd.');
        setStatus(await r.json() as Status); setError('');
        if (show) {
          const q=await fetch('/review-queue.json',{signal:abort.signal});
          if (q.ok) setQueue((await q.json() as {records:Item[]}).records);
        }
      } catch(e) { if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Unable to refresh enrichment.'); }
    }
    void refresh(); const timer=setInterval(refresh,5000);
    return ()=>{abort.abort();clearInterval(timer);};
  },[show]);
  async function control(action:string) {
    setBusy(true); setError('');
    try {
      const r=await fetch('/api/enrichment/'+action,{method:'POST',headers:{'X-Panel-Local':'1'}});
      const data=await r.json() as Status;
      if(!r.ok)throw Error(data.message);
      setStatus(data);
    } catch(e) {setError(e instanceof Error?e.message:'Unable to start. Try relaunching Panel.');}
    finally {setBusy(false);}
  }
  const filtered=queue.filter(q=>filter==='all'||(filter==='lookup'?['pending','error','unmatched'].includes(q.status):q.reasons.some(r=>r.toLowerCase().includes(filter))));
  const pages=Math.max(1,Math.ceil(filtered.length/20)); const current=Math.min(page,pages);
  return <section className="enrichment-controls" aria-label="Automatic enrichment">
    <div className="enrichment-actions">
      <button className="primary-button" disabled={busy||!status||status.active} onClick={()=>void control('start')}>
        {status?.active?'Enrichment running…':status?.status==='paused'?'Resume enrichment':'Enrich remaining books'}
      </button>
      {status?.active && <button className="secondary-link" disabled={busy} onClick={()=>void control('pause')}>Pause</button>}
      {!status?.active && !!status?.pendingLookups && <button className="secondary-link" disabled={busy} onClick={()=>void control('retry')}>Retry lookup errors</button>}
      <button className="secondary-link" aria-expanded={show} onClick={()=>setShow(v=>!v)}>Needs review{status?` (${status.reviewCount.toLocaleString()})`:''}</button>
    </div>
    <p className="scope-note" role="status">{status?`${status.status === 'finished'?'Automatic pass complete':status.status} · ${status.processed.toLocaleString()} / ${status.total.toLocaleString()} catalog records checked · ${status.automatic.toLocaleString()} automatic suggestions · ${status.pendingLookups} pending or failed lookups. ${status.message}`:'Connecting to the collector…'}</p>
    {status?.active && status.current && <p className="subtle">Current book: {status.current}</p>}
    <p className="subtle">Free sources · progress saved on this computer. You can close this tab while it runs; keep the computer awake. Suggested appearances and reading order stay separate from checked details.</p>
    {error&&<p role="alert">{error}</p>}
    {show&&<div className="review-queue">
      <label>Show books needing <select value={filter} onChange={e=>{setFilter(e.target.value);setPage(1);}}>
        <option value="all">Any check</option><option value="lookup">An edition lookup</option><option value="review score">A review score</option><option value="reading order">Reading-order review</option><option value="page count">A page count</option><option value="story">Story and character review</option>
      </select></label>
      <p className="subtle">{filtered.length.toLocaleString()} books. Open one to see its sources and suggestions. This queue is for unresolved details, not a list of failed downloads.</p>
      <ul>{filtered.slice((current-1)*20,current*20).map(item=><li key={item.id}><button onClick={()=>onSelect(item.id)}>{item.title}</button><small>{item.reasons.join(' · ')}</small></li>)}</ul>
      {!filtered.length&&<p>No books in this category yet.</p>}
      {pages>1&&<div className="pagination"><button disabled={current===1} onClick={()=>setPage(current-1)}>Previous</button><span>{current} / {pages}</span><button disabled={current===pages} onClick={()=>setPage(current+1)}>Next</button></div>}
    </div>}
  </section>;
}
