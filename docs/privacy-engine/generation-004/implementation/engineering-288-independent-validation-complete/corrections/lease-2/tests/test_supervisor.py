import json,os,signal,sys,tempfile,time,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'runtime/tests')]
from superlib import *
from launch import launch,verify_completion
from oracle import make,manifest,digest
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.f=make(self.d/'inputs');self.jobs=[]
 def tearDown(self):
  for t in self.jobs:
   try:
    t,key,c=config(t);save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'test-cleanup'},key)
   except Exception:pass
  time.sleep(.15);self.tmp.cleanup()
 def new(self,seconds=10,cap=113,delay=0,quantum=2):
  t=self.d/f'job{len(self.jobs)}';create(t,manifest(self.f),cap,delay,int(quantum*NS));self.jobs.append(t);t,key,c=config(t);grant(t,key,c,seconds,'test');return t,key,c
 def wait(self,t,key,c,timeout=15):
  end=time.monotonic()+timeout
  while time.monotonic()<end:
   s=status(t,key,c)
   if not s['running']:return s
   time.sleep(.03)
  self.fail('supervisor did not stop')
 def launch(self,t,key,c):
  r=launch(t,key,c);self.assertEqual(r['result'],'DETACHED-SUPERVISOR-LAUNCHED');return r
 def progress(self,t,key,c,offset=1,timeout=10):
  end=time.monotonic()+timeout
  while time.monotonic()<end:
   if (t/'data/STATE.json').exists() and read(t/'data/STATE.json',key)['offset']>=offset:return
   if not status(t,key,c)['running']:self.fail(json.dumps(status(t,key,c)))
   time.sleep(.01)
  self.fail('no progress')
 def test_complete_and_exact_reused_terminal(self):
  t,k,c=self.new();self.launch(t,k,c);s=self.wait(t,k,c);self.assertEqual(s['status'],'COMPLETE',s)
  r=verify_completion(t,k,c);self.assertEqual(r['whole_stream_sha256'],digest(self.f['text']));self.assertEqual((r['structural'],r['potential']),(4,10));before=budget(t,k,c)['charged_ns'];self.assertEqual(launch(t,k,c)['result'],'ALREADY-COMPLETE');self.assertEqual(before,budget(t,k,c)['charged_ns'])
 def test_exhausted_budget_resume_does_not_reset(self):
  t,k,c=self.new(seconds=.35,cap=17,delay=.03,quantum=1);self.launch(t,k,c);s=self.wait(t,k,c);b=budget(t,k,c);self.assertGreaterEqual(b['charged_ns'],b['authorized_ns']);self.assertFalse(s['validation_status']=='PASS-CONDITIONAL-BYTE-VALIDATION')
  with self.assertRaises(core.Error):launch(t,k,c)
  grant(t,k,c,8,'more');charged=budget(t,k,c)['charged_ns'];self.launch(t,k,c);self.assertEqual(self.wait(t,k,c)['status'],'COMPLETE');self.assertGreater(budget(t,k,c)['charged_ns'],charged)
 def test_graceful_pause_repeated_resume(self):
  t,k,c=self.new(cap=31,delay=.03)
  for _ in range(2):
   self.launch(t,k,c);self.progress(t,k,c);save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'pause'},k);s=self.wait(t,k,c);self.assertIn(s['status'],['PAUSED','COMPLETE']);old=s['offset']
  self.launch(t,k,c);s=self.wait(t,k,c);self.assertEqual(s['status'],'COMPLETE');self.assertGreaterEqual(s['offset'],old)
 def test_competing_launch_rejected(self):
  t,k,c=self.new(cap=17,delay=.05);self.launch(t,k,c)
  with self.assertRaises(core.Error):launch(t,k,c)
  save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'pause'},k);self.wait(t,k,c)
 def test_supervisor_kill_full_lease_charged_and_resume(self):
  t,k,c=self.new(cap=17,delay=.03,quantum=1);r=self.launch(t,k,c);self.progress(t,k,c);before=budget(t,k,c);fd=os.pidfd_open(r['pid']);killfd(fd);os.close(fd);self.wait(t,k,c);self.assertEqual(budget(t,k,c)['charged_ns'],before['charged_ns']);self.assertIsNotNone(budget(t,k,c)['lease'])
  self.launch(t,k,c);s=self.wait(t,k,c);self.assertEqual(s['status'],'COMPLETE',s);self.assertGreaterEqual(budget(t,k,c)['charged_ns'],before['charged_ns'])
 def test_worker_failure_preserves_progress(self):
  t,k,c=self.new(cap=17,delay=.03);self.launch(t,k,c);self.progress(t,k,c);running=read(t/'RUNNING.json',k);fd=os.pidfd_open(running['worker_pid']);killfd(fd);os.close(fd);s=self.wait(t,k,c);self.assertEqual(s['status'],'WORKER-FAILED');old=s['offset'];self.launch(t,k,c);s=self.wait(t,k,c);self.assertEqual(s['status'],'COMPLETE');self.assertGreaterEqual(s['offset'],old)
 def test_watchdog_enforces_deadline_when_supervisor_stopped(self):
  t,k,c=self.new(seconds=3,cap=1,delay=.05,quantum=1);r=self.launch(t,k,c);self.progress(t,k,c);record=read(t/'RUNNING.json',k);fd=os.pidfd_open(r['pid']);killfd(fd,signal.SIGSTOP);time.sleep(2.4);killfd(fd,signal.SIGCONT);os.close(fd);s=self.wait(t,k,c);self.assertNotEqual(s['validation_status'],'PASS-CONDITIONAL-BYTE-VALIDATION');self.assertIn(s['status'],['BUDGET-EXHAUSTED','WATCHDOG-STOP','WORKER-FAILED'])
 def test_backup_restore_never_restores_budget(self):
  t,k,c=self.new(cap=31,delay=.02);self.launch(t,k,c);self.progress(t,k,c);save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'pause'},k);self.wait(t,k,c)
  with Lock(t/'CONTROL.LOCK'):r=backup(t,k,c)
  original=read(t/'data/STATE.json',k)['offset'];self.launch(t,k,c);self.wait(t,k,c);charged=budget(t,k,c)['charged_ns']
  with Lock(t/'CONTROL.LOCK'):rest=restore(t,k,c,r['path'])
  self.assertEqual(rest['restored_offset'],original);self.assertEqual(budget(t,k,c)['charged_ns'],charged);self.launch(t,k,c);self.assertEqual(self.wait(t,k,c)['status'],'COMPLETE');self.assertEqual(verify_completion(t,k,c)['whole_stream_sha256'],digest(self.f['text']))
 def test_corrupt_and_cross_job_budget_rejected(self):
  t,k,c=self.new();p=t/'BUDGET.json';raw=p.read_bytes();p.write_bytes(raw.replace(b'INITIALIZED',b'CORRUPTEDXX'))
  with self.assertRaises(core.Error):launch(t,k,c)
  p.write_bytes(raw);b=budget(t,k,c);b['config_sha256']='0'*64;save(p,b,k)
  with self.assertRaises(core.Error):launch(t,k,c)
 def test_corrupt_checkpoint_not_silently_reset(self):
  t,k,c=self.new();self.launch(t,k,c);self.wait(t,k,c);p=t/'data/STATE.json';p.write_bytes(b'corrupt')
  with self.assertRaises(Exception):launch(t,k,c)
  self.assertEqual(p.read_bytes(),b'corrupt')
 def test_mutation_and_stale_code_refused(self):
  t,k,c=self.new();self.launch(t,k,c);self.wait(t,k,c);p=self.f['root']/'descriptor.txt';p.write_bytes(p.read_bytes()+b' ')
  with self.assertRaises(core.Error):verify_completion(t,k,c)
 def test_backup_corruption_and_cross_job_substitution(self):
  t,k,c=self.new();self.launch(t,k,c);self.wait(t,k,c)
  with Lock(t/'CONTROL.LOCK'):r=backup(t,k,c)
  q,kq,cq=self.new()
  with self.assertRaises(Exception):restore(q,kq,cq,r['path'])
  p=Path(r['path']);raw=p.read_bytes();p.write_bytes(raw[:len(raw)//2])
  with self.assertRaises(Exception):restore(t,k,c,p)
  self.assertEqual(verify_completion(t,k,c)['whole_stream_sha256'],digest(self.f['text']))
 def test_probe_aggregate_ceiling_and_corruption(self):
  from probe import run
  t=self.d/'probe';t.mkdir();core.keygen(t/'execution.key');k=core.keyread(t/'execution.key');m=manifest(self.f);mp=self.d/'source.json';mp.write_bytes(core.wire(m));identity={'implementation':binding(),'manifest':m,'task':str(t),'format':'CP4W-PROBE-1'}
  save(t/'PROBE-BUDGET.json',{'identity_sha256':hashlib.sha256(core.wire(identity)).hexdigest(),'attempts':3,'charged_upper_seconds':180,'status':'COMPLETE'},k)
  with self.assertRaisesRegex(core.Error,'exhausted'):run(t,mp)
  (t/'PROBE-BUDGET.json').unlink()
  with self.assertRaisesRegex(core.Error,'missing durable'):run(t,mp)
  (t/'PROBE-BUDGET.json').write_bytes(b'corrupt')
  with self.assertRaises(Exception):run(t,mp)
 def test_worker_death_cleans_native_children(self):
  import select
  t,k,c=self.new(cap=17,delay=.02);self.launch(t,k,c);self.progress(t,k,c)
  deadline=time.monotonic()+3
  while not (t/'WORKERS.json').exists() and time.monotonic()<deadline:time.sleep(.02)
  fds=[os.pidfd_open(pid) for pid in read(t/'WORKERS.json',k)['native_pids']];running=read(t/'RUNNING.json',k);fd=os.pidfd_open(running['worker_pid']);killfd(fd);os.close(fd);self.wait(t,k,c)
  for fd in fds:self.assertTrue(select.select([fd],[],[],2)[0]);os.close(fd)
 def test_explicit_restore_repairs_corrupt_state_without_budget_rollback(self):
  t,k,c=self.new();self.launch(t,k,c);self.wait(t,k,c)
  with Lock(t/'CONTROL.LOCK'):r=backup(t,k,c)
  before=budget(t,k,c)['charged_ns'];(t/'data/STATE.json').write_bytes(b'corrupt')
  with Lock(t/'CONTROL.LOCK'):restore(t,k,c,r['path'])
  self.assertEqual((t/'previous-data/STATE.json').read_bytes(),b'corrupt');self.assertEqual(budget(t,k,c)['charged_ns'],before);self.assertEqual(verify_completion(t,k,c)['whole_stream_sha256'],digest(self.f['text']))
 def test_active_progress_heartbeat_within_minute(self):
  t,k,c=self.new(seconds=25,cap=1,delay=.04,quantum=15);self.launch(t,k,c);deadline=time.monotonic()+20;events=[]
  while time.monotonic()<deadline:
   if (t/'progress.log').exists():events=[json.loads(x) for x in (t/'progress.log').read_text().splitlines() if x]
   heartbeats=[x for x in events if x['event']=='PROGRESS']
   if len(heartbeats)>=2:break
   time.sleep(.1)
  self.assertGreaterEqual(len(heartbeats),2);self.assertLess((heartbeats[1]['utc_ns']-heartbeats[0]['utc_ns'])/NS,60)
  save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':'pause'},k);self.wait(t,k,c)
 def test_interrupted_restore_transaction(self):
  from unittest.mock import patch
  t,k,c=self.new();self.launch(t,k,c);self.wait(t,k,c)
  with Lock(t/'CONTROL.LOCK'):r=backup(t,k,c)
  original=os.replace
  def crash(src,dst):
   original(src,dst)
   if Path(dst)==t/'previous-data':raise core.Interrupted('after old data preserved')
  with self.assertRaises(core.Interrupted):
   with patch('os.replace',crash):restore(t,k,c,r['path'])
  self.assertTrue((t/'RESTORE.json').exists());charged=budget(t,k,c)['charged_ns'];finish_restore(t,k);self.assertEqual(budget(t,k,c)['charged_ns'],charged);self.assertEqual(verify_completion(t,k,c)['whole_stream_sha256'],digest(self.f['text']))
 def test_interrupted_budget_reservation_is_never_refunded(self):
  from unittest.mock import patch
  t,k,c=self.new(quantum=2);original=core.atom
  def crash(path,data,fault=None):
   original(path,data,fault)
   if Path(path)==t/'BUDGET.json':raise core.Interrupted('reservation already published')
  with self.assertRaises(core.Interrupted):
   with patch.object(core,'atom',crash):launch(t,k,c)
  self.assertEqual(budget(t,k,c)['charged_ns'],2*NS);self.launch(t,k,c);self.assertEqual(self.wait(t,k,c)['status'],'COMPLETE');self.assertGreater(budget(t,k,c)['charged_ns'],2*NS)
 def test_portable_spool_cap_is_enforced(self):
  with self.assertRaisesRegex(core.Error,'64 MiB'):create(self.d/'oversize',manifest(self.f),64*1048576+1)
  self.assertFalse((self.d/'oversize').exists())
 def test_log_rotation_bounded(self):
  t,k,c=self.new()
  for n in range(1100):log(t,{'n':n,'padding':'x'*4000})
  files=list(t.glob('progress.log*'));self.assertLessEqual(len(files),3);self.assertLessEqual(sum(p.stat().st_size for p in files),3*LOG_CAP)
 def test_idempotent_grants_and_cap(self):
  t,k,c=self.new();a=budget(t,k,c)['authorized_ns'];grant(t,k,c,10,'test');self.assertEqual(budget(t,k,c)['authorized_ns'],a)
  with self.assertRaises(core.Error):grant(t,k,c,11,'test')
if __name__=='__main__':unittest.main(verbosity=2)
