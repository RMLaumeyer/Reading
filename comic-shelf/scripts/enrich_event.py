"""Collect isolated event edition drafts and reading guides from one event slug."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def select(books,event,limit):
    if not 1<=limit<=8:raise ValueError('Edition budget must be one to eight')
    phrase=' '.join(event.split('-'))
    found={}
    for book in books:
        words=' '.join(re.findall(r'[a-z0-9]+',book.get('title','').casefold()))
        isbn=book.get('isbn','')
        if (re.fullmatch(r'\d{13}',isbn) and re.search(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',words)):
            found.setdefault(isbn,{'isbn':isbn,'title':book['title'],'startsWithEvent':words.startswith(phrase+' ') or words==phrase})
    candidates=sorted(found.values(),key=lambda b:(not b['startsWithEvent'],b['isbn']))
    return {'selected':candidates[:limit],'omitted':candidates[limit:],
            'scope':'Catalog title candidates only; neither membership nor complete event coverage established.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--event',required=True)
    parser.add_argument('--name',required=True)
    parser.add_argument('--max-editions',type=int,default=8)
    parser.add_argument('--max-identity-pages',type=int,default=6)
    parser.add_argument('--model',default='qwen3.5-4b')
    args=parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.event) or len(args.event)>80:parser.error('Use a bounded event slug')
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,40}',args.name):parser.error('Use a unique safe name of at most forty characters')
    if not 1<=args.max_editions<=8 or not 0<=args.max_identity_pages<=12:parser.error('Budgets out of bounds')
    root=Path(__file__).resolve().parents[1];trials=root/'data/local-ai-trials'
    catalog=root/'public/catalog.json'
    selection=select(json.loads(catalog.read_text(encoding='utf-8'))['books'],args.event,args.max_editions)
    if not selection['selected']:parser.error('No matching catalog title candidates')
    folder=trials/args.name;edition_name=args.name+'-editions';order_name=args.name+'-orders'
    if any(p.exists() for p in (folder,trials/edition_name,trials/order_name)):parser.error('Run names already exist')
    folder.mkdir()
    def save(name,data):
        with (folder/name).open('x',encoding='utf-8') as stream:json.dump(data,stream,indent=2)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    save('manifest.json',{'event':args.event,'selection':selection,'model':args.model,
        'catalogSha256':sha(catalog),'codeSha256':{p.name:sha(p) for p in (root/'scripts').glob('*.py') if not p.name.startswith('test_')},
        'editionRun':edition_name,'orderRun':order_name,'maxIdentityPages':args.max_identity_pages,
        'eligibleForPublication':False})
    commands=[('edition_enrichment',[sys.executable,str(root/'scripts/solo_enrich.py'),
        '--name',edition_name,'--model',args.model,'--refresh-edition','--max-queries','1']+
        [value for b in selection['selected'] for value in ('--isbn',b['isbn'])]),
        ('reading_order',[sys.executable,str(root/'scripts/order_research.py'),'--event',args.event,
        '--edition-run',str(trials/edition_name),'--name',order_name,'--discover-guides',
        '--discover-identities','--max-identity-pages',str(args.max_identity_pages)])]
    stages=[]
    for stage,command in commands:
        result=subprocess.run(command,cwd=root)
        stages.append({'stage':stage,'exitCode':result.returncode})
        if result.returncode:break
    save('report.json',{'stages':stages,'state':'needs_review' if all(s['exitCode']==0 for s in stages) else 'incomplete',
        'completeReadingOrderEstablished':False,'unaidedAccuracyEstablished':False,'eligibleForPublication':False})
    if any(s['exitCode'] for s in stages):sys.exit(1)


if __name__=='__main__':main()
