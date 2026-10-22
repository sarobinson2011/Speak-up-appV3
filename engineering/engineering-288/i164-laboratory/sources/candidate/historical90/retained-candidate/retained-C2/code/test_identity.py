"""Disposable-copy only C2 cases. Never point at an operational installation."""
import unittest,tempfile,shutil,subprocess,os,sys,json,threading
from fixtures import *
from session_identity import EXECUTOR_ROOT,IdentityBlocked
class C2(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'job';self.c=config();self.c['query_limit']=1;self.b=Bridge(self.p,self.c,True);self.sim=t.OfflineTransport();self.original={n:(ROOT/n).read_bytes() for n in self.b.identity.raw}
 def tearDown(self):
  for n,raw in self.original.items():(ROOT/n).write_bytes(raw)
  self.b.close();self.tmp.cleanup()
 def snap(self):return tuple((self.p/n).read_bytes() for n in ['executor.db','transport.db','independent-anchor.db'])
 def change(self,n):
  p=ROOT/n;p.write_bytes(self.original[n]+b'\n');return p
 def ready(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.seal_conditional('LAB-U-1');self.b.prepare('LAB-U-1',*envelope(self.b))
 def gap(self):
  self.ready();self.b.submit('LAB-U-1','attempt',self.sim);self.sim.outcome=outcome(self.b)
  with self.assertRaises(RuntimeError):self.b.reconcile('LAB-U-1','query',self.sim,'after_transport_result')
 def test_all_bound_files_replaced(self):
  self.b.retire('LAB-U-1',intent(self.c));before=self.snap()
  for n,raw in self.original.items():
   self.change(n)
   with self.assertRaises(IdentityBlocked,msg=n):self.b.seal_conditional('LAB-U-1')
   self.assertEqual(before,self.snap());(ROOT/n).write_bytes(raw)
 def test_unavailable(self):
  n=EXECUTOR_ROOT+'contract/ABI.json';p=ROOT/n;p.unlink();before=self.snap()
  with self.assertRaisesRegex(IdentityBlocked,'UNAVAILABLE'):self.b.status('q')
  self.assertEqual(before,self.snap())
 def test_supplied_selector_probe(self):
  n=EXECUTOR_ROOT+'contract/method-identifiers.json';p=ROOT/n;m=json.loads(p.read_bytes());k=next(k for k in m if k.startswith('signPetition('));m[k]='00000000';p.write_bytes(e.enc(m))
  i=intent(self.c);self.assertFalse(i['calldata_hex'].startswith('00000000'));before=self.snap()
  with self.assertRaisesRegex(IdentityBlocked,'IDENTITY-CHANGED'):self.b.retire('LAB-U-1',i)
  self.assertEqual(before,self.snap());self.assertEqual(self.sim.calls,0)
 def test_each_action_checks_before_use(self):
  self.ready();before=self.snap();self.change(EXECUTOR_ROOT+'contract/ABI.json')
  actions=[lambda:self.b.retire('x',{}),lambda:self.b.seal_conditional('LAB-U-1'),lambda:self.b.prepare('LAB-U-1',{},b''),lambda:self.b.submit('LAB-U-1','a',self.sim),lambda:self.b.reconcile('LAB-U-1','q',self.sim),self.b.internal_terminal_repair,self.b.recover,lambda:self.b.status('s'),lambda:self.b.backup(self.p/'backup','b'),lambda:self.b.allowances.reserve('status','r')]
  for action in actions:
   with self.assertRaises(IdentityBlocked):action()
   self.assertEqual(before,self.snap())
  self.assertEqual(self.sim.calls,0)
 def test_loaded_encoder_reference(self):
  old=e.abi_encode;e.abi_encode=lambda *args:b'changed'
  try:
   with self.assertRaisesRegex(IdentityBlocked,'ENCODER-REFERENCE'):self.b.status('q')
  finally:e.abi_encode=old
 def test_loaded_function_body(self):
  old=a.encode.__code__;a.encode.__code__=(lambda *args:b'changed').__code__
  try:
   with self.assertRaisesRegex(IdentityBlocked,'LOADED-CODE'):self.b.status('q')
  finally:a.encode.__code__=old
 def test_loaded_source_mismatch_before_session(self):
  n=EXECUTOR_ROOT+'executor/abi.py';(ROOT/n).write_bytes(self.original[n].replace(b'def word(n):',b'def word(n):\n if n==17: return b"bad"'))
  with self.assertRaisesRegex(IdentityBlocked,'LOADED-CODE'):Bridge(Path(self.tmp.name)/'new',self.c,True)
  self.assertFalse((Path(self.tmp.name)/'new').exists())
 def test_loaded_constant_source_mismatch(self):
  n=EXECUTOR_ROOT+'executor/session.py';(ROOT/n).write_bytes(self.original[n].replace(b'MAX_ATTEMPTS=64',b'MAX_ATTEMPTS=63'))
  with self.assertRaisesRegex(IdentityBlocked,'LOADED-CONSTANT'):Bridge(Path(self.tmp.name)/'new',self.c,True)
  self.assertFalse((Path(self.tmp.name)/'new').exists())
 def test_restart_changed_implementation(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.close();before=self.snap();self.change('code/bridge.py')
  child="from fixtures import *;import sys;c=config();c['query_limit']=1;\ntry:Bridge(sys.argv[1],c)\nexcept ValueError as x:print(str(x))\nelse:raise AssertionError('accepted changed implementation')"
  p=subprocess.run([sys.executable,'-B','-c',child,str(self.p)],env=dict(os.environ,PYTHONPATH=str(ROOT/'code')),capture_output=True,timeout=5);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(before,self.snap())
 def test_same_bytes_new_path(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.close();kit=Path(self.tmp.name)/'moved';kit.mkdir()
  for n in ['code','retained']:shutil.copytree(ROOT/n,kit/n)
  child="from fixtures import *;import sys;c=config();c['query_limit']=1;\nwith Bridge(sys.argv[1],c) as b:b.internal_terminal_repair();assert b.executor.states['LAB-U-1']['status']=='RETIRED'"
  before=self.snap();p=subprocess.run([sys.executable,'-B','-c',child,str(self.p)],env=dict(os.environ,PYTHONPATH=str(kit/'code')),capture_output=True,timeout=5);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(before,self.snap())
 def test_pending_recovery_blocked_until_identity_restored(self):
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'after_reservation')
  n=EXECUTOR_ROOT+'contract/ABI.json';self.change(n);before=self.snap()
  with self.assertRaises(IdentityBlocked):self.b.recover()
  self.assertEqual(before,self.snap());(ROOT/n).write_bytes(self.original[n]);self.b.recover()
  with self.assertRaises(ValueError):self.b.retire('LAB-U-1',intent(self.c))
  self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'RETIRED')
 def test_C1_identity_and_recovery(self):
  self.gap();n=EXECUTOR_ROOT+'executor/abi.py';self.change(n);before=self.snap()
  with self.assertRaises(IdentityBlocked):self.b.allowances.repair_anchor()
  self.assertEqual(before,self.snap());(ROOT/n).write_bytes(self.original[n]);counts=dict(self.b.transport.counts);head=self.b.transport.head
  self.b.allowances.repair_anchor();self.b.close();self.b=Bridge(self.p,self.c);self.b.allowances.repair_anchor()
  self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'SUCCESS');self.assertEqual(counts,self.b.transport.counts);self.assertEqual(head,self.b.transport.head);self.assertEqual(self.sim.calls,1)
 def test_concurrent_replacement(self):
  self.ready();n=EXECUTOR_ROOT+'contract/method-identifiers.json';done=threading.Event()
  def replace():self.change(n);done.set()
  thread=threading.Thread(target=replace);thread.start();done.wait(2);thread.join();before=self.snap()
  with self.assertRaises(IdentityBlocked):self.b.submit('LAB-U-1','a',self.sim)
  self.assertEqual(before,self.snap());self.assertEqual(self.sim.calls,0)
 def test_check_use_interval_frozen(self):
  # Privileged trace injects file replacement after final checks, at send entry.
  # No application function or snapshot is replaced. In-flight code/bytes remain exact.
  self.ready();expected=self.b.transport.blob(self.b.transport.hydrate(self.b.transport.states['LAB-U-1'])[0]['near_bytes']);n=EXECUTOR_ROOT+'contract/method-identifiers.json';fired=[]
  def trace(frame,event,arg):
   if event=='call' and frame.f_code is t.OfflineTransport.send.__code__:
    self.change(n);fired.append(True)
   return trace
  sys.settrace(trace)
  try:self.b.submit('LAB-U-1','a',self.sim)
  finally:sys.settrace(None)
  self.assertEqual(fired,[True]);self.assertEqual(list(self.sim.seen.values()),[expected]);self.assertEqual(self.sim.calls,1)
  before=self.snap()
  with self.assertRaises(IdentityBlocked):self.b.reconcile('LAB-U-1','q',self.sim)
  self.assertEqual(before,self.snap())
if __name__=='__main__':unittest.main(verbosity=2)
