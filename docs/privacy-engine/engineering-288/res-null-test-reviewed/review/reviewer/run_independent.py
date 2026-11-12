from bytes_only import *
import subprocess,sys,time,datetime
cmd=[sys.executable,'-I','-B','-u',str(B/'independent_controls.py')]
save(B/'independent-launch.json',{'command':cmd,'timeout_seconds':600,'automatic_retry':False,'scope':'new independent pure-source/model controls only','script':fid(B/'independent_controls.py'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
start=time.monotonic();timeout=False
with (B/'independent.stdout').open('xb') as so,(B/'independent.stderr').open('xb') as se:
 try:rc=subprocess.run(cmd,stdout=so,stderr=se,timeout=600).returncode
 except subprocess.TimeoutExpired:rc=None;timeout=True
save(B/'independent-exit.json',{'exit':rc,'timed_out':timeout,'seconds':time.monotonic()-start,'automatic_retry':False,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps(read(B/'independent-exit.json')),flush=True)
