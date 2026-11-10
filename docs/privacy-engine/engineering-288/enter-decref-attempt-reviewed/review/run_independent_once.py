"""Single bounded reviewer child. No retries; all records outside candidate."""
from pathlib import Path
import subprocess,time,sys,json,hashlib,os,datetime
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B));from bytes_only import save,fid
assert not (B/'independent').exists() and not (B/'independent-exit.json').exists()
cmd=[sys.executable,'-I','-B',str(B/'independent_controls.py')];save(B/'independent-launch.json',{'command':cmd,'reviewer_code':fid(B/'independent_controls.py'),'timeout_seconds':180,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'fresh pure-source/model controls only; public and authenticated constructed execution forbidden'})
t=time.monotonic();timedout=False
with (B/'independent.stdout').open('xb') as so,(B/'independent.stderr').open('xb') as se:
 try:rc=subprocess.run(cmd,stdout=so,stderr=se,timeout=180).returncode
 except subprocess.TimeoutExpired:rc=None;timedout=True
save(B/'independent-exit.json',{'returncode':rc,'timed_out':timedout,'seconds':time.monotonic()-t,'no_retry':True,'streams':{s:fid(B/('independent.'+s)) for s in ('stdout','stderr')},'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
raise SystemExit(0 if rc==0 and not timedout else 1)
