import unittest,tempfile,shutil,threading,json,time,resource
from pathlib import Path
import backend,sole_service,connected,runtime
from anchor import *
from connected import Connected,OfflineSink,implementation,copy_counts
from sole_service import Service
from backend import SimulatedBackend
import importlib.util
spec=importlib.util.spec_from_file_location('sole_fixtures',runtime.ROOT/'retained-C2/code/fixtures.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
config,intent=f.config,f.intent
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name);self.c=config();self.pre={k:self.c['prerequisites'][v] for k,v in [('model','model'),('profile','profile'),('config','configuration')]}
  self.desc={'kind':'SIMULATED-NOT-DYNAMODB','table_id':'LAB-TABLE','service_identity':'LAB-SERVICE'}
  self.cfg={'pilot':'LAB-SOLE-ANCHOR','session':'LAB-1','implementation':implementation(runtime.Guard(),self.pre),'backend':self.desc,'origin':'0'*64,'limits':{'attempt':2,'query':2,'snapshot':2,'staging_query':2,'staging_snapshot':2}}
  self.b=SimulatedBackend(self.p/'service.db',self.desc);self.s=Service(self.b,self.cfg);self.s.genesis({'executor_head':'0'*64,'transport_head':'0'*64,'transport_seq':0})
  self.x=Connected(self.p/'local',self.s,self.pre,True);self.i=intent(self.c);self.u='LAB-U-1';self.sink=OfflineSink()
  self.old=(self.p/'local/executor.db').read_bytes()
 def tearDown(self):self.x.close();self.b.close();self.tmp.cleanup()
 def reopen(self,old=None):
  self.x.close()
  if old is not None:(self.p/'local/executor.db').write_bytes(old)
  self.x=Connected(self.p/'local',self.s,self.pre)
 def retire(self):self.x.retire(self.u,self.i,'retire')
 def sent(self):self.retire();self.x.seal_conditional(self.u,'seal');self.x.submit_conditional(self.u,'attempt',self.sink)
 def test_normal_one_submission(self):
  self.sent();self.assertEqual(len(self.sink.sent),1)
  self.reopen(self.old)
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'again',self.sink)
  self.assertEqual(len(self.sink.sent),1);self.assertEqual(self.s.fresh()['counts']['attempt'],1)
 def test_pending_old_rollback_different_intent(self):
  with self.assertRaises(Uncertain):self.x.retire(self.u,self.i,'r',crash='after_service')
  self.reopen(self.old);changed=dict(self.i,nonce='2')
  with self.assertRaises(ValueError):self.x.retire(self.u,changed,'another')
  self.assertEqual(self.x.executor.states[self.u]['intent'],self.i)
 def test_retirement_faults(self):
  for f in ['before_service','before','partial','ack_loss','after_service','after_local']:
   case=Tests();case.setUp()
   try:
    with self.assertRaises((Uncertain,OSError)):case.x.retire(case.u,case.i,'r',f)
    case.x.recover();state=case.s.fresh();accepted=f in ['ack_loss','after_service','after_local']
    self.assertEqual(case.u in state['u'],accepted)
    if accepted:self.assertEqual(case.x.executor.states[case.u]['intent'],case.i)
    else:
     with self.assertRaises(ValueError):case.x.retire('other',intent(case.c,'other',nonce=2),'new')
   finally:case.tearDown()
 def test_interrupted_recovery(self):
  self.retire();self.reopen(self.old);self.x.close();(self.p/'local/executor.db').write_bytes(self.old)
  # Interrupt the repair of an already opened rolled-back replica.
  self.x=Connected(self.p/'local',self.s,self.pre)
  self.x.close();(self.p/'local/executor.db').write_bytes(self.old)
  code=runtime.Guard().base.executor_code();code['sole_anchor']=self.cfg['implementation']
  self.x.executor=runtime.executor.Session(self.p/'local/executor.db',self.cfg['pilot'],bound_code=code)
  with self.assertRaises(Uncertain):self.x.recover('after_local')
  self.x.recover();self.x.recover();self.assertEqual(len(self.s.fresh()['u']),1)
 def test_attempt_ack_loss_freezes(self):
  self.retire();self.x.seal_conditional(self.u,'seal')
  with self.assertRaises(Uncertain):self.x.submit_conditional(self.u,'attempt',self.sink,'ack_loss')
  self.reopen(self.old)
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'new',self.sink)
  self.assertEqual(self.sink.sent,[]);self.assertEqual(self.s.fresh()['counts']['attempt'],1)
 def test_after_send_no_reauthorization(self):
  self.retire();self.x.seal_conditional(self.u,'seal')
  with self.assertRaises(Uncertain):self.x.submit_conditional(self.u,'attempt',self.sink,'after_send')
  self.reopen(self.old)
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'new',self.sink)
  self.assertEqual(len(self.sink.sent),1)
 def test_unavailable_no_fallback(self):
  self.retire();self.b.available=False
  with self.assertRaises(OSError):self.x.recover()
  with self.assertRaises(OSError):self.x.seal_conditional(self.u,'seal')
  self.assertFalse((self.p/'local/independent-anchor.db').exists())
 def test_lost_local_replica(self):
  self.sent();self.x.close();shutil.rmtree(self.p/'local')
  self.x=Connected(self.p/'local',self.s,self.pre,True)
  self.assertEqual(self.x.executor.states[self.u]['status'],'UNCERTAIN')
  with self.assertRaises(ValueError):self.x.submit_conditional(self.u,'again',self.sink)
 def test_stale_read_fresh_client(self):
  raw=self.b.get('HEAD');self.retire();self.s.last=None;self.b.stale=raw
  with self.assertRaises(ValueError):self.x.recover()
 def test_duplicate_exact_service_request(self):
  s=self.s.fresh();body={'intent_hex':runtime.executor.enc(self.i).hex()}
  a=self.s.commit(s['head'],'r','RETIRE',self.u,body)
  b=self.s.commit(s['head'],'r','RETIRE',self.u,body)
  self.assertFalse(b['release']);self.assertEqual(a['receipt'],b['receipt']);self.x.recover()
  with self.assertRaises(ValueError):self.s.commit(s['head'],'r','RETIRE',self.u,{'intent_hex':'00'})
 def test_concurrent_clients(self):
  expected=self.s.fresh()['head'];barrier=threading.Barrier(2);results=[]
  def run(n):
   b=SimulatedBackend(self.p/'service.db',self.desc);s=Service(b,self.cfg)
   try:
    barrier.wait();s.commit(expected,'r'+str(n),'RETIRE',self.u,{'intent_hex':runtime.executor.enc(dict(self.i,nonce=str(n+1))).hex()});results.append('commit')
   except (ValueError,Uncertain):results.append('blocked')
   finally:b.close()
  ts=[threading.Thread(target=run,args=(n,)) for n in range(2)]
  for t in ts:t.start()
  for t in ts:t.join()
  self.assertEqual(sorted(results),['blocked','commit']);self.x.recover()
 def test_local_conflict(self):
  self.retire();self.x.executor.db.execute('UPDATE log SET digest=?',('f'*64,))
  with self.assertRaises(ValueError):self.x.recover()
 def test_c1_repair_conservation(self):
  self.sent();self.x.save_conditional_observation(self.u,'observe','REVERTED');before=copy_counts(self.s.fresh())
  with self.assertRaises(Uncertain):self.x.internal_terminal_repair('ack_loss')
  self.reopen(self.old)
  self.assertIsNone(self.x.internal_terminal_repair());self.assertIsNone(self.x.internal_terminal_repair())
  self.assertEqual(self.x.executor.states[self.u]['status'],'FAILED');self.assertEqual(copy_counts(self.s.fresh()),before);self.assertEqual(len(self.sink.sent),1)
 def test_success_repair(self):
  self.sent();self.x.save_conditional_observation(self.u,'observe','SUCCESS');self.x.internal_terminal_repair();self.assertEqual(self.x.executor.states[self.u]['status'],'SUCCESS')
 def test_not_executed_uncertain(self):
  self.sent();self.x.save_conditional_observation(self.u,'observe','NOT-EXECUTED');self.x.internal_terminal_repair();self.assertEqual(self.x.executor.states[self.u]['status'],'UNCERTAIN')
 def test_missing_evidence_no_terminal(self):
  self.sent();self.x.internal_terminal_repair();self.assertEqual(self.x.executor.states[self.u]['status'],'UNCERTAIN')
 def test_corrupted_evidence_blocks(self):
  self.sent();self.x.save_conditional_observation(self.u,'observe','SUCCESS');ref=self.s.fresh()['u'][self.u]['saved']['ref']
  self.b.db.execute('UPDATE objects SET v=? WHERE k=?',(b'{}\n','BLOB/'+ref))
  with self.assertRaises(ValueError):self.x.internal_terminal_repair()
 def test_exhaustion(self):
  self.sent();self.x.save_conditional_observation(self.u,'observe','SUCCESS');self.x.internal_terminal_repair()
  u='U2';self.x.retire(u,intent(self.c,u,nonce=2),'r2');self.x.seal_conditional(u,'s2');self.x.submit_conditional(u,'a2',self.sink)
  u='U3';self.x.retire(u,intent(self.c,u,nonce=3),'r3');self.x.seal_conditional(u,'s3')
  with self.assertRaises(ValueError):self.x.submit_conditional(u,'a3',self.sink)
  self.assertEqual(self.s.fresh()['counts']['attempt'],2)
 def test_identity_replacement_and_restore(self):
  self.retire();p=Path(connected.__file__);raw=p.read_bytes()
  try:
   p.write_bytes(raw+b'\n# replacement\n')
   with self.assertRaises(ValueError):self.x.seal_conditional(self.u,'s')
  finally:p.write_bytes(raw)
  self.x.recover();self.assertEqual(self.x.executor.states[self.u]['status'],'RETIRED')
 def test_changed_prerequisites(self):
  self.x.close()
  with self.assertRaises(ValueError):Connected(self.p/'local',self.s,dict(self.pre,model='f'*64))
 def test_operational_block(self):
  with self.assertRaises(ValueError):self.x.operational_submit()
 def test_changed_backend_identity(self):
  self.retire();self.b.descriptor['table_id']='OTHER'
  with self.assertRaises(ValueError):self.x.recover()
 def test_missing_service(self):
  self.b.db.execute("DELETE FROM objects")
  with self.assertRaises(ValueError):self.x.recover()
 def test_stale_pending_substitution(self):
  self.retire();self.x.outbox.execute('UPDATE requests SET request=?',(enc({'wrong':'request'}),))
  with self.assertRaises(ValueError):self.x.seal_conditional(self.u,'s')
 def test_abi_replacement(self):
  p=runtime.retained.ROOT/'retained/executor-basis/retained/kernel/candidate/contract/ABI.json';raw=p.read_bytes()
  try:
   p.write_bytes(raw+b' ')
   with self.assertRaises(ValueError):self.x.retire(self.u,self.i,'r')
  finally:p.write_bytes(raw)
 def test_inflight_commit_then_identity_rejection(self):
  p=Path(connected.__file__);raw=p.read_bytes();original=self.b.commit
  def altered(old,new,puts,fault=None):
   original(old,new,puts,fault)
   if puts:p.write_bytes(raw+b'\n# concurrent replacement\n')
  self.b.commit=altered
  try:
   with self.assertRaises(ValueError):self.x.retire(self.u,self.i,'r')
  finally:p.write_bytes(raw);self.b.commit=original
  self.assertIn(self.u,self.s.fresh()['u']);self.x.recover()
  self.assertEqual(self.x.executor.states[self.u]['status'],'RETIRED')
 def test_loaded_function_replacement(self):
  old=connected.Connected.retire
  try:
   connected.Connected.retire=lambda *a:None
   with self.assertRaises(ValueError):self.x.recover()
  finally:connected.Connected.retire=old
 def test_repair_before_local_and_restart(self):
  self.sent();self.x.save_conditional_observation(self.u,'obs','SUCCESS');counts=copy_counts(self.s.fresh())
  with self.assertRaises(Uncertain):self.x.internal_terminal_repair('after_service')
  self.reopen(self.old);self.assertIsNone(self.x.internal_terminal_repair())
  self.assertEqual(copy_counts(self.s.fresh()),counts);self.assertEqual(len(self.sink.sent),1)
 def test_connected_concurrent_retirement(self):
  barrier=threading.Barrier(2);results=[]
  def run(n):
   b=SimulatedBackend(self.p/'service.db',self.desc);s=Service(b,self.cfg);x=None
   try:
    x=Connected(self.p/('client'+str(n)),s,self.pre,True);barrier.wait()
    x.retire(self.u,dict(self.i,nonce=str(n+1)),'retire-'+str(n));results.append('commit')
   except (ValueError,Uncertain):results.append('blocked')
   finally:
    if x:x.close()
    b.close()
  ts=[threading.Thread(target=run,args=(n,)) for n in range(2)]
  for t in ts:t.start()
  for t in ts:t.join(timeout=10)
  self.assertEqual(sorted(results),['blocked','commit']);self.x.recover();self.assertEqual(len(self.s.fresh()['u']),1)
 def test_query_exhausted_internal_repair(self):
  self.sent();self.x.save_conditional_observation(self.u,'obs1','SUCCESS')
  u='U2';self.x.retire(u,intent(self.c,u,nonce=2),'r2');self.x.seal_conditional(u,'s2');self.x.submit_conditional(u,'a2',self.sink)
  self.x.save_conditional_observation(u,'obs2','REVERTED');before=copy_counts(self.s.fresh())
  self.assertIsNone(self.x.internal_terminal_repair());self.assertIsNone(self.x.internal_terminal_repair())
  self.assertEqual(copy_counts(self.s.fresh()),before);self.assertEqual(self.s.fresh()['counts']['query'],2);self.assertEqual(len(self.sink.sent),2)
if __name__=='__main__':unittest.main()
