from pathlib import Path
import json,subprocess,sys,time,datetime
B=Path(__file__).resolve().parent;t=time.monotonic();cmd=[sys.executable,'-I','-B','-u',str(B/'independent_controls.py')]
def save(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')
save(B/'independent-launch.json',{'command':cmd,'timeout_seconds':600,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'automatic_retries':0,'scope':'Independent pure source/model only; no public authentication or application execution'})
with (B/'independent.stdout').open('xb') as out,(B/'independent.stderr').open('xb') as err:
 try:r=subprocess.run(cmd,stdout=out,stderr=err,timeout=600);result={'exit_code':r.returncode,'timed_out':False}
 except subprocess.TimeoutExpired:result={'exit_code':None,'timed_out':True,'qualification':'not successful completion'}
result.update(seconds=time.monotonic()-t,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save(B/'independent-exit.json',result);print(result,flush=True)
