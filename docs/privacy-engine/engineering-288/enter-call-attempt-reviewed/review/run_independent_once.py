"""One bounded reviewer child; exclusive output files and saved exit. No retry."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B))
from review_bytes import save,fid
launch={'command':[sys.executable,'-I','-B',str(B/'independent_controls.py')],'timeout_seconds':150,'automatic_retry':False,'started_utc':datetime.now(timezone.utc).isoformat(),'code':fid(B/'independent_controls.py'),'target_root':str(B/'candidate')}
save(B/'independent-launch.json',launch)
t=time.monotonic();timeout=False
with (B/'independent.stdout').open('xb') as out,(B/'independent.stderr').open('xb') as err:
 p=subprocess.Popen(launch['command'],stdout=out,stderr=err,cwd=B)
 save(B/'independent-process.json',{'pid':p.pid,'launch':launch})
 try:rc=p.wait(timeout=150)
 except subprocess.TimeoutExpired:timeout=True;p.terminate();rc=p.wait(timeout=10)
 out.flush();err.flush();os.fsync(out.fileno());os.fsync(err.fileno())
save(B/'independent-exit.json',{'returncode':rc,'timed_out':timeout,'seconds':time.monotonic()-t,'finished_utc':datetime.now(timezone.utc).isoformat(),'streams':{s:fid(B/('independent.'+s)) for s in ('stdout','stderr')},'no_retry':True})
raise SystemExit(rc)
