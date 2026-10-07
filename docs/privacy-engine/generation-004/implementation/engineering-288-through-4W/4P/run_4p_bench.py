"""Externally bounded source-grounded projection benchmark; no retained stream."""
import os,sys,json,time,subprocess,resource,threading
from pathlib import Path
ROOT=Path(__file__).resolve().parent;WORK=ROOT/'work/4P-benchmark'
def disk(p):return sum(f.stat().st_size for f in Path(p).rglob('*') if f.is_file())
def child(mode):
 resource.setrlimit(resource.RLIMIT_NOFILE,(96,96));before=len(os.listdir('/proc/self/fd'));peak=[before];done=threading.Event()
 def monitor():
  while not done.wait(.002):
   try:peak[0]=max(peak[0],len(os.listdir('/proc/self/fd')))
   except OSError:pass
 t=threading.Thread(target=monitor,daemon=True);t.start();start=time.monotonic();WORK.mkdir(parents=True,exist_ok=True)
 try:
  if mode=='construct':
   from fixtures.generated_events import export
   export(WORK/'fixture',semantic_documents=128);r={'input_bytes':disk(WORK/'fixture'),'shared_dependencies':128,'signing_included':True}
  else:
   from recovery_schedule.runner import run
   from recovery_schedule.state import Scheduler
   from link_recovery.cli import create_key,PauseRequested
   from unittest.mock import patch
   p=WORK/'fixture';create_key(WORK/'key');save=Scheduler.save
   def stop(s,label,*a,**kw):
    if label=='ordered-ledger':raise PauseRequested()
    return save(s,label,*a,**kw)
   with patch.object(Scheduler,'save',stop):
    try:run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',seconds=50)
    except PauseRequested:pass
    else:raise AssertionError('interruption absent')
   r=run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',resume=True,seconds=50)
   assert not r['failures'] and not r['profile_admitted'],r['reasons']
   oracle=json.loads((p/'oracle.json').read_bytes())
   for scope in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'):
    got=r['bindings']['scope_validation']['scopes'][scope]['link_validation'];e=oracle[scope]
    assert got['complete_stream_sha256']==e['links_sha256'] and got['structural_rows']==e['structural'] and got['potential_rows']==e['potential']
   import sqlite3,hashlib
   with sqlite3.connect(Path(str(WORK/'job')+'.stages')/'occurrence-equality.sqlite') as db:
    for token,expected in oracle['values_hex'].items():
     name,h=db.execute('select file,sha from assignments join groups using(g) where token=?',(token,)).fetchone();raw=(Path(str(WORK/'job')+'.stages')/name).read_bytes()
     assert raw==bytes.fromhex(expected) and hashlib.sha256(raw).hexdigest()==h
   db.close()
   terminal=run(p/'manifest.json',p/'trusted.json',WORK/'job',WORK/'key',resume=True,seconds=50);assert terminal['stage_schedule']['terminal_reused'] and not terminal['failures']
   r={'oracle_values':len(oracle['values_hex']),'occurrence_acquisition':r['occurrence_acquisition'],'semantic_acquisition':r['semantic_acquisition'],'terminal_reused':True,'retained_work_bytes':disk(WORK),'conditional_result':r['result']}
 finally:done.set();t.join()
 r.update(result='PASS',seconds=time.monotonic()-start,child_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,peak_handles=peak[0],handles_before=before,handles_after=len(os.listdir('/proc/self/fd')),full_retained_stream_processed=False,actual_admission=False)
 (ROOT/('results/4P-benchmark-'+mode+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
def supervise():
 rows=[];total=0
 for mode in ('construct','validate'):
  start=time.monotonic()
  with (ROOT/('results/4P-benchmark-'+mode+'.log')).open('w') as log:
   p=subprocess.Popen([sys.executable,__file__,mode],cwd=ROOT,stdout=log,stderr=log)
   while True:
    pid,status,usage=os.wait4(p.pid,os.WNOHANG)
    if pid:break
    if time.monotonic()-start>=min(59.5,179.5-total):p.kill();pid,status,usage=os.wait4(p.pid,0);break
    time.sleep(.05)
   p.returncode=os.waitstatus_to_exitcode(status)
  elapsed=time.monotonic()-start;total+=elapsed;row={'stage':mode,'seconds':elapsed,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'cpu_seconds':usage.ru_utime+usage.ru_stime};rows.append(row);print(json.dumps(row),flush=True)
  if p.returncode:break
 r={'result':'PASS' if len(rows)==2 and all(x['exit']==0 for x in rows) else 'FAIL-OR-LIMIT','runs':rows,'total_seconds':total,'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'individual_limit_seconds':60,'aggregate_limit_seconds':180,'full_retained_stream_processed':False}
 (ROOT/'results/4P-benchmark-summary.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':child(sys.argv[1]) if len(sys.argv)>1 else supervise()
