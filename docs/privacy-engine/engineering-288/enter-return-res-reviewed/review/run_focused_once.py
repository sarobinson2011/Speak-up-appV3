"""One fresh bounded reviewer child; incremental logs and no automatic retry."""
from pathlib import Path
import sys,subprocess,time,os
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B))
from bytes_only import fid,save
cmd=[sys.executable,'-I','-B',str(B/'focused_independent.py')]
save(B/'independent-launch.json',{'command':cmd,'code':fid(B/'focused_independent.py'),'timeout_seconds':180,'automatic_retry':False,'utc':datetime.now(timezone.utc).isoformat()})
t=time.monotonic();timeout=False
with (B/'independent.stdout').open('xb') as out,(B/'independent.stderr').open('xb') as err:
 p=subprocess.Popen(cmd,stdout=out,stderr=err,cwd=B);save(B/'independent-process.json',{'pid':p.pid,'command':cmd})
 try:rc=p.wait(timeout=180)
 except subprocess.TimeoutExpired:timeout=True;p.terminate();rc=p.wait(timeout=10)
 out.flush();err.flush();os.fsync(out.fileno());os.fsync(err.fileno())
save(B/'independent-exit.json',{'returncode':rc,'timed_out':timeout,'seconds':time.monotonic()-t,'streams':{s:fid(B/('independent.'+s)) for s in ('stdout','stderr')},'no_retry':True,'utc':datetime.now(timezone.utc).isoformat()})
raise SystemExit(rc)
