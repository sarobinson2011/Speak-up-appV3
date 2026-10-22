import subprocess,resource,time,os,signal,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
BIN=P/'bin/i164-aurora-stages'
if '--actual-begin' in sys.argv:
 sys.argv.remove('--actual-begin');P=P/'actual-begin'
def limit():
 resource.setrlimit(resource.RLIMIT_AS,(256*1024**3,)*2);resource.setrlimit(resource.RLIMIT_CPU,(45,)*2)
rows=[]
for case in (list(map(int,sys.argv[1:])) or list(range(7))):
 t=time.monotonic();out=P/'results'/f'engine-{case}.jsonl';err=P/'results'/f'engine-{case}.stderr'
 with out.open('ab') as f,err.open('ab') as e:
  p=subprocess.Popen([str(BIN),str(P),str(case),'1000000000000000','20'],stdout=f,stderr=e,preexec_fn=limit,start_new_session=True)
  try:
   deadline=time.monotonic()+50
   while p.poll() is None:
    if time.monotonic()>deadline:raise subprocess.TimeoutExpired(p.args,50)
    stat=Path('/proc')/str(p.pid)/'status'
    if stat.exists():
     rss=next((int(x.split()[1])*1024 for x in stat.read_text().splitlines() if x.startswith('VmRSS:')),0)
     if rss>2*1024**3:raise subprocess.TimeoutExpired(p.args,50)
    time.sleep(.05)
   rc=p.returncode
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);rc=p.wait()
 r={'case':case,'exit':rc,'seconds':time.monotonic()-t,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'local_near_prepaid':10**15,'resident_monitor_limit':2*1024**3,'virtual_reservation_limit':256*1024**3,'cpu_seconds_limit':45,'wall_limit':50};rows.append(r);print(json.dumps(r),flush=True)
 if rc:break
with (P/'results/run-resources.jsonl').open('a') as f:
 for r in rows:f.write(json.dumps(r)+'\n')
