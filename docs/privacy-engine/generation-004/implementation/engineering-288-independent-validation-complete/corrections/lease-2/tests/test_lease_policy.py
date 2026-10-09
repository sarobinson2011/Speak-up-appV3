import json,os,signal,subprocess,sys,tempfile,time,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'runtime/tests')]
import superlib as S
from superlib import *
from launch import launch
from oracle import make,manifest
OLD=Path(sys.argv.pop(1)).resolve()
class Tests(unittest.TestCase):
 def test_twenty_second_supervisor_stall(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);f=make(d/'inputs');m=d/'manifest.json';m.write_text(json.dumps(manifest(f)));jobs=[]
   for kit,name in [(OLD,'old'),(ROOT,'new')]:
    t=d/name
    script="import sys;sys.path.insert(0,sys.argv[1]);from superlib import *;from launch import launch; t=Path(sys.argv[2]);create(t,core.load_json(sys.argv[3]),1,.05);t,k,c=config(t);grant(t,k,c,180,'fixture');print(json.dumps(launch(t,k,c)))"
    r=subprocess.run([sys.executable,'-B','-c',script,str(kit),str(t),str(m)],capture_output=True,text=True,check=True);r=json.loads(r.stdout);t,k,c=config(t);jobs.append((name,t,k,c,r['pid']))
   stopped=[]
   try:
    for name,t,k,c,pid in jobs:
     end=time.monotonic()+5
     while time.monotonic()<end:
      if (t/'data/STATE.json').exists() and read(t/'data/STATE.json',k)['offset']>0:break
      time.sleep(.01)
     self.assertTrue((t/'data/STATE.json').exists());os.kill(pid,signal.SIGSTOP);stopped.append(pid)
    time.sleep(20)
    for pid in stopped:os.kill(pid,signal.SIGCONT)
    stopped=[]
    oldname,ot,ok,oc,op=jobs[0];end=time.monotonic()+5
    while status(ot,ok,oc)['running'] and time.monotonic()<end:time.sleep(.02)
    self.assertFalse(status(ot,ok,oc)['running']);self.assertIn(budget(ot,ok,oc)['status'],['LEASE-EXPIRED-WITH-BUDGET-REMAINING','BUDGET-EXHAUSTED']);self.assertGreater(budget(ot,ok,oc)['authorized_ns'],budget(ot,ok,oc)['charged_ns']);events=[json.loads(x) for x in (ot/'progress.log').read_text().splitlines()];diag=next(x for x in events if x['event']=='EXIT-DIAGNOSTICS');self.assertEqual(json.loads(diag['watchdog_report_raw'])['reason'],'PREPAID-LEASE-EXPIRED')
    name,t,k,c,pid=jobs[1];before=read(t/'data/STATE.json',k)['offset'];end=time.monotonic()+5
    while time.monotonic()<end and read(t/'data/STATE.json',k)['offset']<=before:time.sleep(.02)
    self.assertTrue(status(t,k,c)['running']);self.assertGreater(read(t/'data/STATE.json',k)['offset'],before)
    save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'test-stop'},k);end=time.monotonic()+5
    while status(t,k,c)['running'] and time.monotonic()<end:time.sleep(.02)
    self.assertFalse(status(t,k,c)['running'])
    print(json.dumps({'experiment':'20-second-supervisor-scheduling-stall','old':status(ot,ok,oc),'new':status(t,k,c),'new_progress_after_stall':True,'laboratory_only':True,'past_host_stall_cause_proved':False}),flush=True)
   finally:
    for pid in stopped:
     try:os.kill(pid,signal.SIGCONT)
     except ProcessLookupError:pass
    for _,t,k,c,pid in jobs:
     if status(t,k,c)['running']:
      save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'cleanup'},k)
      end=time.monotonic()+5
      while status(t,k,c)['running'] and time.monotonic()<end:time.sleep(.02)
 def test_budget_math_and_atomic_delay(self):
  original_now=S.now;original_bsave=S.bsave;original_log=S.log
  clock=[0];published=[];latency=[0]
  try:
   S.now=lambda:clock[0]
   def publish(t,k,b):clock[0]+=latency[0];published.append(copy.deepcopy(b))
   S.bsave=publish;S.log=lambda *_:None
   c={'quantum_ns':120*NS};b={'lease':{'deadline_ns':120*NS,'reserved_ns':120*NS},'charged_ns':120*NS,'authorized_ns':1000*NS,'sequence':0}
   clock[0]=61*NS;latency[0]=20*NS;self.assertTrue(S.renew(None,None,c,b));self.assertEqual(clock[0],81*NS);self.assertEqual(b['lease']['deadline_ns'],240*NS);self.assertLess(clock[0],120*NS)
   # Maximum prepaid tail under the half-quantum renewal threshold is <180 seconds.
   self.assertLess(b['lease']['deadline_ns']-clock[0],180*NS)
   b['authorized_ns']=b['charged_ns']+7*NS;clock[0]=181*NS;latency[0]=0;self.assertTrue(S.renew(None,None,c,b));self.assertEqual(b['charged_ns'],b['authorized_ns']);self.assertFalse(S.renew(None,None,c,b))
   clock[0]=b['lease']['deadline_ns']+1;b['authorized_ns']+=100*NS;before=copy.deepcopy(b);self.assertFalse(S.renew(None,None,c,b));self.assertEqual(b,before)
  finally:S.now=original_now;S.bsave=original_bsave;S.log=original_log
if __name__=='__main__':unittest.main()
