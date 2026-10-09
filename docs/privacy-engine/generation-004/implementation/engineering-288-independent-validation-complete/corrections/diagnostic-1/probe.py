"""Maximum three <=60-second attempts, durably prepaid; no automatic retry."""
from superlib import *
import argparse

def run(task,manifest):
 t=Path(task).resolve();need('Speak-up-appV3' not in t.parts and '.env' not in t.parts,'isolated probe task')
 new=not t.exists()
 if new:t.mkdir(parents=True,mode=0o700);core.fsyncdir(t.parent);core.keygen(t/'execution.key')
 key=core.keyread(t/'execution.key')
 with Lock(t/'CONTROL.LOCK'):
  m=core.load_json(manifest);identity={'implementation':binding(),'manifest':m,'task':str(t),'format':'CP4W-PROBE-1'};ih=hashlib.sha256(core.wire(identity)).hexdigest();path=t/'PROBE-BUDGET.json'
  if path.exists():b=read(path,key);need(b['identity_sha256']==ih,'probe identity changed')
  else:
   need(new,'missing durable probe budget; never reset an existing namespace')
   need(not any(t.glob('attempt-*')) and not any(t.glob('probe-*.json')),'missing probe budget with retained work');b={'identity_sha256':ih,'attempts':0,'charged_upper_seconds':0,'status':'NEW'}
  need(b['charged_upper_seconds']+60<=180,'aggregate probe allowance exhausted; do not restart under another namespace')
  b['attempts']+=1;b['charged_upper_seconds']+=60;b['status']='PREPAID-IN-FLIGHT';save(path,b,key)
  start=time.monotonic();p=spawn([sys.executable,'-B',str(ROOT/'probe_worker.py'),str(t),str(Path(manifest).resolve())],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);fd=os.pidfd_open(p.pid)
  try:
   try:out,err=p.communicate(timeout=55)
   except subprocess.TimeoutExpired:
    killfd(fd);out,err=p.communicate(timeout=3)
   elapsed=time.monotonic()-start
   need(len(out)<core.STATE_LIMIT and len(err)<16384,'probe output bound');r=json.loads(out) if out else {'result':'PROBE-TIMEOUT-OR-INTERRUPTION'}
   r.update(attempt=b['attempts'],attempt_wall_seconds=elapsed,aggregate_attempt_allowance_charged_seconds=b['charged_upper_seconds'],maximum_attempt_seconds=60,aggregate_ceiling_seconds=180,actual_admission=False)
   b['status']='COMPLETE' if p.returncode==0 and elapsed<60 else 'FAILED';b['last_result']=r['result'];save(path,b,key);save(t/f"probe-{b['attempts']}.json",r,key)
   if p.returncode or elapsed>=60:r['result']='PROBE-FAILED-OR-TIMED-OUT';r['detail']=err.decode(errors='replace')[:2048]
   return r
  finally:killfd(fd);os.close(fd)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--manifest',required=True);a=p.parse_args()
 try:print(json.dumps(run(a.task,a.manifest),indent=2))
 except BaseException as e:print(json.dumps({'result':'PROBE-BLOCKED','detail':str(e),'actual_admission':False}));sys.exit(2)
