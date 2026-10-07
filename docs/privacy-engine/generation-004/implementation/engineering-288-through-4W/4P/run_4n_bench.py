"""Three bounded children. Exact fixtures; no retained pair/link stream."""
import os,sys,time,json,resource,subprocess,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work/4N-benchmark'

def disk(p):return sum(f.stat().st_size for f in Path(p).rglob('*') if f.is_file())
def child(mode):
 resource.setrlimit(resource.RLIMIT_NOFILE,(96,96));before=len(os.listdir('/proc/self/fd'));peak=[before];done=threading.Event()
 def monitor():
  while not done.wait(.002):
   try:peak[0]=max(peak[0],len(os.listdir('/proc/self/fd')))
   except OSError:pass
 thread=threading.Thread(target=monitor,daemon=True);thread.start();start=time.monotonic();WORK.mkdir(parents=True,exist_ok=True)
 result={}
 try:
  if mode=='construct':
   from fixtures.lifetime import export
   m,t=export(WORK/'fixture',768);result={'required_shared_fragments':768,'input_bytes':disk(WORK/'fixture'),'independent_signing':True}
  elif mode=='validate':
   from recovery_schedule.runner import run
   from recovery_schedule.state import Scheduler
   from link_recovery.cli import create_key,PauseRequested
   from unittest.mock import patch
   p=WORK/'fixture';create_key(WORK/'key');save=Scheduler.save
   def pause(s,label,*args,**kwargs):
    if label=='ordered-ledger':raise PauseRequested()
    return save(s,label,*args,**kwargs)
   with patch.object(Scheduler,'save',pause):
    try:run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',seconds=50)
    except PauseRequested:pass
    else:raise AssertionError('expected pre-ledger interruption')
   first=json.loads((Path(str(WORK/'job')+'.stages')/'ledger-output.json').read_bytes())
   r=run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',resume=True,seconds=50)
   assert not r['failures'] and r['processing_complete'],r['reasons']
   oracle=json.loads((p/'oracle.json').read_bytes());assert {i['sha256'] for i in r['semantic_acquisition']['invocations']}==set(oracle['calls'].values())
   for scope,e in oracle['scopes'].items():
    v=r['bindings']['scope_validation']['scopes'][scope]['link_validation'];assert v['complete_stream_sha256']==e['links_sha256'] and v['structural_rows']==e['structural'] and v['potential_rows']==e['potential']
   final=run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',resume=True,seconds=50);assert final['stage_schedule']['terminal_reused'] and not final['failures'] and not final['profile_admitted']
   result={'initial_semantic_acquisition':first['semantic_acquisition'],'semantic_acquisition':r['semantic_acquisition'],'oracle_invocation_count':len(oracle['calls']),'required_shared_fragments':768,'terminal_reused':True,'work_bytes':disk(WORK),'conditional_ledger_result':r['result'],'full_model_witness':False}
  elif mode=='cycles':
   from semantic_stream.storage import Store
   from fixtures.construct import wire
   metrics=[]
   for cycle in range(4):
    s=Store(WORK);blobs=[]
    try:
     for i in range(512):
      b=s.write([wire({'ordinal':i,'cycle':cycle})]);blobs.append(b);assert s.parse(b)=={'ordinal':i,'cycle':cycle}
     for i,b in enumerate(blobs):assert s.parse(b)['ordinal']==i
     metrics.append(s.metrics())
    finally:s.close()
    assert not s.root.exists();assert len(os.listdir('/proc/self/fd'))==before
   result={'documents':2048,'repeat_accesses':2048,'cycles':metrics,'cleanup_each_cycle':True}
  else:raise ValueError(mode)
 finally:done.set();thread.join()
 result.update(result='PASS',seconds=time.monotonic()-start,open_file_limit=96,peak_open_handles=peak[0],handles_before=before,handles_after=len(os.listdir('/proc/self/fd')),child_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,full_retained_stream_processed=False,profile_admitted=False,authoritative_qualification=False)
 (ROOT/('results/4N-benchmark-'+mode+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

def supervise():
 rows=[];total=0
 for mode in ('construct','validate','cycles'):
  start=time.monotonic()
  with (ROOT/('results/4N-benchmark-'+mode+'.log')).open('w') as log:
   p=subprocess.Popen([sys.executable,__file__,mode],cwd=ROOT,stdout=log,stderr=log)
   while True:
    pid,status,usage=os.wait4(p.pid,os.WNOHANG)
    if pid:break
    if time.monotonic()-start>=min(59.5,179.5-total):p.kill();pid,status,usage=os.wait4(p.pid,0);break
    time.sleep(.05)
   p.returncode=os.waitstatus_to_exitcode(status)
  elapsed=time.monotonic()-start;total+=elapsed;row={'stage':mode,'seconds':elapsed,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'cpu_seconds':usage.ru_utime+usage.ru_stime};rows.append(row);print(json.dumps(row),flush=True)
  if p.returncode:break
 r={'result':'PASS' if len(rows)==3 and all(x['exit']==0 for x in rows) else 'LIMIT-OR-FAILURE','runs':rows,'total_seconds':total,'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'individual_limit_seconds':60,'aggregate_limit_seconds':180,'full_retained_stream_processed':False}
 (ROOT/'results/4N-benchmark-summary.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':child(sys.argv[1]) if len(sys.argv)>1 else supervise()
