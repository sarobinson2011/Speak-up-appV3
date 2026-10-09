import json,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'runtime/tests')]
from superlib import *
from launch import launch,verify_completion
from oracle import make,manifest,digest
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp);f=make(d/'inputs');t=d/'job';create(t,manifest(f),31,.02);t,k,c=config(t);grant(t,k,c,10,'fresh')
 def wait():
  end=time.monotonic()+10
  while status(t,k,c)['running'] and time.monotonic()<end:time.sleep(.02)
  need(not status(t,k,c)['running'],'smoke deadline')
 launch(t,k,c)
 while not (t/'data/STATE.json').exists():time.sleep(.01)
 save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'pause'},k);wait()
 with Lock(t/'CONTROL.LOCK'):b=backup(t,k,c)
 charged=budget(t,k,c)['charged_ns'];launch(t,k,c);wait();first=verify_completion(t,k,c)
 with Lock(t/'CONTROL.LOCK'):r=restore(t,k,c,b['path'])
 need(budget(t,k,c)['charged_ns']>=charged,'restored budget rolled back');launch(t,k,c);wait();second=verify_completion(t,k,c)
 need(first==second and second['whole_stream_sha256']==digest(f['text']),'fresh recovery oracle disagreement')
 print(json.dumps({'result':'PASS-FRESH-EXTRACTION-SUPERVISOR-RECOVERY','validation':second,'charged_seconds':budget(t,k,c)['charged_ns']/NS,'backup_restored_without_budget_rollback':True,'actual_admission':False}))
