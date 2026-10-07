"""External 60-second per process and 180-second aggregate benchmark enforcement."""
import os,sys,time,subprocess,resource,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
previous=ROOT/'results/4M-benchmarks.json'
correction='--correction' in sys.argv
if correction:
 prior=json.loads(previous.read_bytes());(ROOT/'results/4M-benchmarks-initial.json').write_text(json.dumps(prior,indent=2)+'\n');rows=prior['processes'];total=prior['total_seconds']
else:rows=[];total=0
for mode in (('validate','scheduler') if correction else ('generate','validate','scheduler')):
 start=time.monotonic()
 with (ROOT/('results/4M-benchmark-'+mode+'.log')).open('a' if correction else 'w') as log:
  p=subprocess.Popen([sys.executable,'run_4m_metadata.py',mode],cwd=ROOT,stdout=log,stderr=log)
  try:
   # wait4 provides THIS child's independent RSS, not accumulated parent RSS.
   while True:
    pid,status,usage=os.wait4(p.pid,os.WNOHANG)
    if pid:break
    if time.monotonic()-start>=min(59.5,179.5-total):p.kill();pid,status,usage=os.wait4(p.pid,0);break
    time.sleep(.05)
   p.returncode=os.waitstatus_to_exitcode(status)
  finally:
   if p.returncode is None:p.kill();p.wait()
 elapsed=time.monotonic()-start;total+=elapsed;rows.append({'stage':mode,'seconds':elapsed,'exit':p.returncode,'child_maxrss_kib':usage.ru_maxrss,'child_cpu_seconds':usage.ru_utime+usage.ru_stime,'corrective':correction})
 print(json.dumps(rows[-1]),flush=True)
 if p.returncode:break
r={'result':'PASS-AFTER-CORRECTION' if correction and len(rows)==5 and all(x['exit']==0 for x in rows[-2:]) else 'PASS' if len(rows)==3 and all(x['exit']==0 for x in rows) else 'BOUNDED-LIMIT-OR-FAILURE','processes':rows,'total_seconds':total,'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':{'individual_seconds':60,'aggregate_seconds':180},'full_stream_processed':False}
(ROOT/'results/4M-benchmarks.json').write_text(json.dumps(r,indent=2)+'\n')
