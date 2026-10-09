import json,os,signal,subprocess,sys,tempfile,time,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'runtime/tests')]
from superlib import *
from launch import launch,verify_completion
from migrate import migrate,TRANSITION
from oracle import make,manifest,digest
from supervisor import StderrTail
OLD=Path(sys.argv.pop(1)).resolve() if len(sys.argv)>1 and not sys.argv[1].startswith('-') else None
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.f=make(self.d/'inputs');self.t=self.d/'job'
 def tearDown(self):self.tmp.cleanup()
 def oldjob(self):
  m=self.d/'manifest.json';m.write_text(json.dumps(manifest(self.f)))
  code="import sys;sys.path.insert(0,sys.argv[1]);from superlib import *;from worker import initialized; t=Path(sys.argv[2]);create(t,core.load_json(sys.argv[3]),31);t,k,c=config(t);grant(t,k,c,20,'fixture');b=budget(t,k,c);b['charged_ns']=NS;bsave(t,k,b);initialized(t,k,c);j=core.Job(t/'data',t/'execution.key');j.step();j.close()"
  # Job has context-manager cleanup; no public close method is assumed.
  code=code.replace("j=core.Job(t/'data',t/'execution.key');j.step();j.close()", "exec(\"with core.Job(t/'data',t/'execution.key') as j:j.step()\")")
  subprocess.run([sys.executable,'-B','-c',code,str(OLD),str(self.t),str(m)],check=True,capture_output=True)
 def wait(self,t,k,c):
  end=time.monotonic()+12
  while status(t,k,c)['running'] and time.monotonic()<end:time.sleep(.02)
  self.assertFalse(status(t,k,c)['running']);return status(t,k,c)
 def test_migration_resume_oracle(self):
  self.oldjob();before={n:core.sha(self.t/'data'/n) for n in ['STATE.json','IDENTITY.json','spool.bin'] if (self.t/'data'/n).exists()}
  r=migrate(self.t,OLD);self.assertEqual(r['result'],'PASS-MIGRATED-NOT-STARTED');self.assertEqual(before,{n:core.sha(self.t/'data'/n) for n in before})
  t,k,c=config(self.t);b=budget(t,k,c);self.assertEqual(b['charged_ns'],NS);self.assertEqual(b['authorized_ns'],20*NS)
  self.assertEqual(migrate(t,OLD)['result'],'ALREADY-MIGRATED');launch(t,k,c);self.assertEqual(self.wait(t,k,c)['status'],'COMPLETE');v=verify_completion(t,k,c);self.assertEqual(v['whole_stream_sha256'],digest(self.f['text']));self.assertEqual((v['rows'],v['structural'],v['potential']),(14,4,10))
  with Lock(t/'CONTROL.LOCK'):saved=backup(t,k,c)
  with Lock(t/'CONTROL.LOCK'):restore(t,k,c,saved['path'])
  self.assertEqual(verify_completion(t,k,c),v)
 def test_interruption_each_publication(self):
  self.oldjob()
  for point in ['plan','config','budget']:
   def fail(p):
    if p==point:raise RuntimeError('simulated interruption '+point)
   with self.assertRaises(RuntimeError):migrate(self.t,OLD,fail)
  r=migrate(self.t,OLD);self.assertEqual(r['charged_seconds'],1);self.assertEqual(r['authorized_seconds'],20)
 def test_corrupt_plan_rejected(self):
  self.oldjob()
  with self.assertRaises(RuntimeError):migrate(self.t,OLD,lambda p:(_ for _ in ()).throw(RuntimeError()))
  p=self.t/TRANSITION/'PLAN.json';raw=p.read_bytes();p.write_bytes(raw.replace(b'CP4W-LEASE',b'BAD-LEASE'));self.assertNotEqual(p.read_bytes(),raw)
  with self.assertRaises(Exception):migrate(self.t,OLD)
 def test_state_mutation_rejected(self):
  self.oldjob()
  with self.assertRaises(RuntimeError):migrate(self.t,OLD,lambda p:(_ for _ in ()).throw(RuntimeError()))
  p=self.t/'data/STATE.json';p.write_bytes(p.read_bytes()+b' ')
  with self.assertRaises(Exception):migrate(self.t,OLD)
 def test_input_mutation_rejected(self):
  self.oldjob();p=self.f['root']/'descriptor.txt';p.write_bytes(p.read_bytes()+b' ')
  with self.assertRaises(Exception):migrate(self.t,OLD)
 def test_cross_job_plan_rejected(self):
  self.oldjob();migrate(self.t,OLD);t,k,c=config(self.t);plan=read(t/TRANSITION/'PLAN.json',k);plan['task']=str(self.d/'other');save(t/TRANSITION/'PLAN.json',plan,k)
  with self.assertRaises(Exception):migrate(self.t,OLD)
 def test_worker_sigkill_diagnostics(self):
  create(self.t,manifest(self.f),1,.03);t,k,c=config(self.t);grant(t,k,c,10,'test');launch(t,k,c)
  end=time.monotonic()+5
  while not (t/'data/STATE.json').exists() and time.monotonic()<end:time.sleep(.01)
  r=read(t/'RUNNING.json',k);fd=os.pidfd_open(r['worker_pid']);killfd(fd);os.close(fd);self.wait(t,k,c)
  events=[json.loads(x) for x in (t/'progress.log').read_text().splitlines()];e=next(x for x in events if x['event']=='EXIT-DIAGNOSTICS');self.assertEqual(e['worker_before_cleanup']['signal'],'SIGKILL')
 def test_watchdog_corrupt_budget_reason(self):
  create(self.t,manifest(self.f));t,k,c=config(self.t)
  (t/'BUDGET.json').write_bytes(b'corrupt')
  worker=subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)']);fd=os.pidfd_open(worker.pid)
  try:
   guard=subprocess.run([sys.executable,'-B',str(ROOT/'supervisor.py'),'watch',str(t),str(fd)],pass_fds=(fd,),capture_output=True,text=True,timeout=5)
   self.assertEqual(json.loads(guard.stdout)['reason'],'BUDGET-READ-OR-INTEGRITY-ERROR');self.assertEqual(worker.wait(timeout=3),-signal.SIGKILL)
  finally:
   os.close(fd)
   if worker.poll() is None:worker.kill();worker.wait()
 def test_stderr_bounded_drain(self):
  p=subprocess.Popen([sys.executable,'-c','import sys;sys.stderr.write("x"*200000)'],stderr=subprocess.PIPE);tail=StderrTail(p.stderr);p.wait(timeout=5);tail.thread.join(timeout=2);self.assertEqual(tail.total,200000);self.assertLessEqual(len(tail.tail),1024);p.stderr.close()
 def test_watchdog_deadline_reason(self):
  create(self.t,manifest(self.f),1,.03,NS);t,k,c=config(self.t);grant(t,k,c,3,'test');r=launch(t,k,c)
  end=time.monotonic()+5
  while not (t/'data/STATE.json').exists() and time.monotonic()<end:time.sleep(.01)
  fd=os.pidfd_open(r['pid']);killfd(fd,signal.SIGSTOP);time.sleep(1.4);killfd(fd,signal.SIGCONT);os.close(fd);self.wait(t,k,c)
  es=[json.loads(x) for x in (t/'progress.log').read_text().splitlines()];e=next(x for x in es if x['event']=='EXIT-DIAGNOSTICS');self.assertEqual(json.loads(e['watchdog_report_raw'])['reason'],'PREPAID-LEASE-EXPIRED')
if __name__=='__main__':unittest.main()
