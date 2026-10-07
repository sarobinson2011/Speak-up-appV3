"""Bounded, separate emission/validation measurements. No full retained stream."""
import argparse,hashlib,itertools,json,os,resource,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'tests')]
from adapter.core import *
from oracle import HEADER
def entry(p):return {"path":str(p.resolve()),"bytes":p.stat().st_size,"sha256":sha(p)}

def synthetic(d,n=384):
 # Independent oracle: all original-order pairs; lexical order is independently sorted.
 names=[f'token.{i:06d}.'+'v'*48 for i in reversed(range(n))]
 rows=sorted((names[a],names[b],'000000','EQUALS') for a,b in itertools.combinations(range(n),2))
 body=HEADER+b''.join(('\t'.join((f'{i:06d}',*r))+'\n').encode() for i,r in enumerate(rows,1))
 (d/'model').write_bytes(wire({'laboratory_only':True,'names':names}));(d/'contract').write_bytes(b'synthetic-complete-static-contract-v1\n');(d/'descriptor').write_text(f'LINKS {n} 0 0\n'+'\n'.join(names)+'\n')
 return {'format':'CP4V-BYTE-SOURCE-1','model':entry(d/'model'),'contract':entry(d/'contract'),'descriptor':entry(d/'descriptor'),'source':{'kind':'deterministic-laboratory-emitter'},'expected':{'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'serialization':'S90-FCR-S70-STATIC-LINKS-TSV','laboratory_only':True},len(rows)

def run(m,d,cap,full=False):
 k=d/'key';keygen(k);initialize(d/'job',k,m,cap);t=time.monotonic()
 with Job(d/'job',k) as j:
  j.services('emit');j.services('validate');startup=time.monotonic()-t
  oldp=j.produce;generation=[];validation=[]
  def timed(c,o):
   before=time.monotonic();v=oldp(c,o);elapsed=time.monotonic()-before;need(elapsed<60,'individual generation benchmark exceeded 60 seconds');generation.append({'wall_seconds':elapsed,'worker_seconds':v['seconds'],'bytes':v['bytes'],'rss_kib':j.emitter.ready['rss_kib']});return v
  j.produce=timed;olda=j.validator.ask
  def ask(q):
   before=time.monotonic();v=olda(q);elapsed=time.monotonic()-before;need(elapsed<60,'individual validation benchmark exceeded 60 seconds');validation.append({'wall_seconds':elapsed,'worker_seconds':v['seconds'],'offset':v['offset'],'rss_kib':v['rss_kib']});return v
  j.validator.ask=ask;began=time.monotonic()
  for _ in range(100):
   need(time.monotonic()-BENCH_START<175,'aggregate measurement budget');r=j.step()
   if not full or r['complete']:break
  elapsed=time.monotonic()-began
  if full:need(r['complete'],'synthetic full coverage not complete')
  else:need(not r['complete'],'retained prefix must not be complete')
  allocated=sum(p.stat().st_blocks*512 for p in (d/'job').iterdir() if p.is_file())
  return {'scope':'COMPLETE-SYNTHETIC-ORACLE' if full else 'RETAINED-PREFIX-PERFORMANCE-ONLY','ready':j.ready,'startup_seconds':startup,'generation':generation,'validation':validation,'loop_wall_seconds':elapsed,'peak_job_file_bytes':j.peak_disk,'terminal_allocated_job_bytes':allocated,'job_disk_bound_bytes':j.disk_bound(),'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'result':r,'metrics':j.state['metrics']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--contract',required=True);p.add_argument('--descriptor',required=True);p.add_argument('--out',required=True);a=p.parse_args();parent_limit();BENCH_START=time.monotonic()
 with tempfile.TemporaryDirectory() as t:
  d=Path(t);(d/'synthetic').mkdir();m,count=synthetic(d/'synthetic');small=run(m,d/'synthetic',4*1048576,True);need(small['result']['rows']==count,'independent synthetic count')
  m={'format':'CP4V-BYTE-SOURCE-1','model':entry(Path(a.model)),'contract':entry(Path(a.contract)),'descriptor':entry(Path(a.descriptor)),'source':{'kind':'deterministic-laboratory-emitter'},'expected':{'bytes':19909380154846,'sha256':TEXT},'serialization':'S90-FCR-S70-STATIC-LINKS-TSV','laboratory_only':True}
  (d/'retained').mkdir();large=run(m,d/'retained',64*1048576)
  total=time.monotonic()-BENCH_START;need(total<180,'aggregate benchmark ceiling');Path(a.out).write_bytes(wire({'result':'PASS-BOUNDED-MEASUREMENTS','aggregate_wall_seconds_including_oracle_and_setup':total,'maximum_individual_seconds':max(x['wall_seconds'] for r in [small,large] for group in ['generation','validation'] for x in r[group]),'records':[small,large],'implementation':code_identity(),'full_retained_validation':False,'actual_admission':False}))
