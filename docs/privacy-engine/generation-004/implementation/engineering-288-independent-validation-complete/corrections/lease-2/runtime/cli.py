#!/usr/bin/env python3
"""Bounded driver. No command silently starts a full stream run."""
import argparse,json,sys,time
from pathlib import Path
from adapter.core import *
def main():
 p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
 q=s.add_parser('keygen');q.add_argument('--key',required=True)
 q=s.add_parser('fixture');q.add_argument('--directory',required=True)
 q=s.add_parser('manifest');q.add_argument('--model',required=True);q.add_argument('--contract',required=True);q.add_argument('--descriptor',required=True);q.add_argument('--out',required=True)
 for name in ['init','step','status']:
  q=s.add_parser(name);q.add_argument('--job',required=True);q.add_argument('--key',required=True)
  if name=='init':q.add_argument('--manifest',required=True);q.add_argument('--spool-mib',type=int,default=64)
  if name=='step':
   q.add_argument('--steps',type=int,default=1);q.add_argument('--review-seconds',type=int,default=120);q.add_argument('--new-bytes',type=int);q.add_argument('--chunk-bytes',type=int,default=65536)
 a=p.parse_args()
 if a.command=='keygen':keygen(a.key);print(json.dumps({'result':'LOCAL-EXECUTION-KEY-CREATED','source_authority':False}));return
 if a.command=='fixture':
  sys.path.insert(0,str(ROOT/'tests'));from oracle import make,manifest
  d=Path(a.directory).resolve();f=make(d);(d/'source.json').write_bytes(wire(manifest(f)));print(json.dumps({'source_manifest':str(d/'source.json'),'bytes':len(f['text']),'laboratory_only':True}));return
 if a.command=='manifest':
  def entry(v):
   f=Path(v).resolve();return {'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f)}
  m={'format':'CP4V-BYTE-SOURCE-1','model':entry(a.model),'contract':entry(a.contract),'descriptor':entry(a.descriptor),'source':{'kind':'deterministic-laboratory-emitter'},'expected':{'bytes':19909380154846,'sha256':TEXT},'serialization':'S90-FCR-S70-STATIC-LINKS-TSV','laboratory_only':True}
  need(m['model']['sha256']==MODEL,'retained candidate required');validate_manifest(m);out=Path(a.out);need(not out.exists(),'new manifest output required');atom(out,wire(m));print(json.dumps({'result':'RETAINED-MANIFEST-PREPARED','full_execution_started':False}));return
 if a.command=='init':
  initialize(a.job,a.key,load_json(a.manifest),a.spool_mib*1048576);print(json.dumps({'result':'INITIALIZED-NOT-STARTED','actual_admission':False}));return
 with Job(a.job,a.key) as j:
  if a.command=='status':print(json.dumps({'result':j.state['status'],'offset':j.state['offset'],'expected_bytes':j.manifest['expected']['bytes'],'sequence':j.state['sequence'],'metrics':j.state['metrics'],'last_result':j.state['result'],'actual_admission':False},sort_keys=True));return
  need(1<=a.steps<=1024 and 1<=a.review_seconds<=3600,'bounded driver capability: <=1024 steps, <=3600 review seconds')
  start=time.monotonic()
  for i in range(a.steps):
   if i and time.monotonic()-start>=a.review_seconds:break
   r=j.step(a.new_bytes,a.chunk_bytes);print(json.dumps({'step':i+1,'sequence':j.state['sequence'],'offset':j.state['offset'],'result':r,'disk_bytes':j.disk_bytes(),'disk_bound_bytes':j.disk_bound(),'wall_seconds':time.monotonic()-start},sort_keys=True),flush=True)
   if r['result']!='PAUSED':break
  print(json.dumps({'result':'BOUNDED-INVOCATION-END','status':j.state['status'],'durable_offset':j.state['offset'],'review_limit_note':'Soft boundary checked between bounded steps; a step can add up to 2 worker budgets plus index/hash startup. Not a full-run supervisor.','actual_admission':False}))
if __name__=='__main__':
 try:main()
 except KeyboardInterrupt:print(json.dumps({'result':'INTERRUPTED','recovery':'Reopen same job with same key; only committed state is reusable','actual_admission':False}));sys.exit(130)
 except Exception as e:print(json.dumps({'result':'REJECTED-OR-BLOCKED','detail':str(e),'actual_admission':False}));sys.exit(2)
