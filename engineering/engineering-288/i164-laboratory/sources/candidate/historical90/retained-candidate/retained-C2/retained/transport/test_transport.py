import unittest,tempfile,copy,sqlite3,shutil,multiprocessing,os,json,time,resource,sys
from pathlib import Path
from transport import *
from fixtures import *
class Cases(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.p=Path(self.temp.name);self.c=config();self.db=self.p/'job.db';self.anchor=self.p/'anchor.db';self.s=Session(self.db,self.anchor,self.c,True);self.t=OfflineTransport()
 def tearDown(self):
  self.s.close();self.temp.cleanup()
 def prepare(self):self.s.prepare(*make(self.c))
 def reopen(self):self.s.close();self.s=Session(self.db,self.anchor,self.c)
 def test_success_and_terminal_query_charged(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.t.outcome=outcome(self.s);a=self.s.reconcile('LAB-U-1','q1',self.t);self.reopen();b=self.s.reconcile('LAB-U-1','q2',self.t)
  self.assertEqual(a['status'],'SUCCESS');self.assertEqual(b['status'],'SUCCESS');self.assertNotEqual(a['receipt'],b['receipt']);self.assertEqual(self.s.counts,{'attempt':1,'query':2,'snapshot':0});self.assertFalse(b['actual_admission'])
 def test_mutation_after_prepare(self):
  x=make(self.c);x[1]=bytearray(x[1]);x[2]=bytearray(x[2]);x[4]=bytearray(x[4]);self.s.prepare(*x);saved=self.s.hydrate(self.s.states[x[0]])[1]
  x[1][0]^=1;x[2][0]^=1;x[4][0]^=1;x[3]['gas']=1;x[5]['retired']=False
  self.s.submit('LAB-U-1','a',self.t);self.assertEqual(next(iter(self.t.seen.values())),saved)
 def test_maximum_and_oversize(self):
  self.s.prepare(*make(self.c,size=74829));self.reopen();self.assertEqual(len(self.s.hydrate(self.s.states['LAB-U-1'])[1]),74829+206)
  with self.assertRaises(Blocked):make(self.c,'x',2,size=74830)
 def test_wrong_exact_near(self):
  x=make(self.c);x[4]=x[4][:-1]+bytes([x[4][-1]^1])
  with self.assertRaises(Blocked):self.s.prepare(*x)
 def test_gas_and_nonce_substitution(self):
  for key,value in [('gas',1),('nonce',2),('engine','elsewhere'),('network','mainnet'),('method','submit_with_args')]:
   x=make(self.c);x[3][key]=value
   with self.assertRaises(Blocked):self.s.prepare(*x)
 def test_handoff_missing_qualification_never_authorizes(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.t.outcome=outcome(self.s);r=self.s.reconcile('LAB-U-1','q',self.t);self.assertFalse(r['actual_admission'])
 def test_unretired_wrong_handoff(self):
  for key,value in [('retired',False),('intent_sha256','0'*64),('evm_sha256','1'*64),('u','other')]:
   x=make(self.c);x[5][key]=value
   with self.assertRaises(Blocked):self.s.prepare(*x)
 def test_before_charge(self):
  self.prepare()
  with self.assertRaises(RuntimeError):self.s.submit('LAB-U-1','a',self.t,'before_charge')
  self.reopen();self.assertEqual(self.s.counts['attempt'],0);self.s.submit('LAB-U-1','b',self.t)
 def test_after_charge_frozen(self):
  self.prepare()
  with self.assertRaises(RuntimeError):self.s.submit('LAB-U-1','a',self.t,'after_charge')
  self.reopen();self.assertEqual(self.s.counts['attempt'],1);self.assertEqual(self.t.calls,0)
  with self.assertRaises(Blocked):self.s.submit('LAB-U-1','b',self.t)
 def test_ack_loss_recovery(self):
  self.prepare();self.t.mode='ack_loss'
  with self.assertRaises(TimeoutError):self.s.submit('LAB-U-1','a',self.t)
  self.reopen();self.t.outcome=outcome(self.s);self.assertEqual(self.s.reconcile('LAB-U-1','q',self.t)['status'],'SUCCESS');self.assertEqual(self.t.calls,1)
 def test_after_send_crash(self):
  self.prepare()
  with self.assertRaises(RuntimeError):self.s.submit('LAB-U-1','a',self.t,'after_send')
  self.reopen();self.assertEqual(len(self.t.seen),1);self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_timeout_rejection_nonce_conflict(self):
  for mode in ['timeout_before','reject','conflict']:
   # Separate lifetime fixture per mode, never reset existing state.
   c=config();d=self.p/(mode+'.db');a=self.p/(mode+'-anchor.db')
   with Session(d,a,c,True) as s:
    s.prepare(*make(c));t=OfflineTransport();t.mode=mode
    if mode=='conflict':r,_=s.hydrate(s.states['LAB-U-1']);sp=r['near_spec'];t.nonces[(sp['signer'],sp['public_key'],sp['nonce'])]='e'*64
    with self.assertRaises((Blocked,TimeoutError)):s.submit('LAB-U-1','a',t)
    self.assertEqual(s.counts['attempt'],1);self.assertEqual(s.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_hash_substituted_ack(self):
  self.prepare();self.t.mode='wrong_hash'
  with self.assertRaises(Blocked):self.s.submit('LAB-U-1','a',self.t)
  self.reopen();self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_network_duplicate_not_authorized_retry(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);r,raw=self.s.hydrate(self.s.states['LAB-U-1']);self.t.send(r,raw) # simulated network duplicates one admitted delivery
  self.assertEqual(len(self.t.seen),1)
  with self.assertRaises(Blocked):self.s.submit('LAB-U-1','explicit-retry',self.t)
  self.assertEqual(self.s.counts['attempt'],1)
 def test_outcome_identity(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t)
  for i,k in enumerate(['txid','raw_sha256','network','signer']):
   self.t.outcome=outcome(self.s);self.t.outcome[k]='substituted'
   with self.assertRaises(Blocked):self.s.reconcile('LAB-U-1','q'+str(i),self.t)
  self.assertEqual(self.s.counts['query'],4);self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_finality_and_not_found(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.assertEqual(self.s.reconcile('LAB-U-1','q1',self.t)['status'],'UNCERTAIN')
  self.t.outcome=outcome(self.s);self.t.outcome['finality']='EXECUTED_OPTIMISTIC'
  with self.assertRaises(Blocked):self.s.reconcile('LAB-U-1','q2',self.t)
 def test_near_success_evm_reverted(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.t.outcome=outcome(self.s,evm='REVERTED');self.assertEqual(self.s.reconcile('LAB-U-1','q',self.t)['status'],'FAILED')
  with self.assertRaises(Blocked):self.s.prepare(*make(self.c))
 def test_near_failure(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.t.outcome=outcome(self.s,near='FAILURE',evm='NOT-EXECUTED');self.assertEqual(self.s.reconcile('LAB-U-1','q',self.t)['status'],'FAILED')
 def test_query_crash_consumed(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t)
  with self.assertRaises(RuntimeError):self.s.reconcile('LAB-U-1','q',self.t,'after_charge')
  self.reopen();self.assertEqual(self.s.counts['query'],1)
  with self.assertRaises(Blocked):self.s.reconcile('LAB-U-1','q',self.t)
 def test_outcome_before_commit_crash(self):
  self.prepare();self.s.submit('LAB-U-1','a',self.t);self.t.outcome=outcome(self.s)
  with self.assertRaises(RuntimeError):self.s.reconcile('LAB-U-1','q',self.t,'after_lookup')
  self.reopen();self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN');self.assertEqual(self.s.reconcile('LAB-U-1','q2',self.t)['status'],'SUCCESS')
 def test_concurrent_lock(self):
  with self.assertRaises(Blocked):Session(self.db,self.anchor,self.c)
 def test_budget_shared_across_u(self):
  c=config(attempts=1,queries=1,snapshots=1)
  with Session(self.p/'limited.db',self.p/'limited-anchor.db',c,True) as s:
   s.prepare(*make(c));s.prepare(*make(c,'LAB-U-2',2));t=OfflineTransport();s.submit('LAB-U-1','a',t)
   with self.assertRaises(Blocked):s.submit('LAB-U-2','b',t)
   s.reconcile('LAB-U-1','q1',t)
   with self.assertRaises(Blocked):s.reconcile('LAB-U-1','q2',t)
   self.assertIsNone(s.internal_repair());self.assertEqual(t.calls,1)
   s.backup(self.p/'snap.db','snap1')
   with self.assertRaises(Blocked):s.backup(self.p/'snap2.db','snap2')
 def test_backup_restore_no_reset(self):
  self.prepare();backup=self.p/'backup.db';self.s.backup(backup,'backup');self.s.submit('LAB-U-1','a',self.t);self.s.close();shutil.copyfile(backup,self.db)
  with self.assertRaises(Blocked):Session(self.db,self.anchor,self.c)
 def test_current_backup_reopen(self):
  self.prepare();backup=self.p/'backup.db';self.s.backup(backup,'backup');self.s.close();shutil.copyfile(backup,self.db);self.s=Session(self.db,self.anchor,self.c);self.assertEqual(self.s.counts['snapshot'],1)
 def test_changed_prerequisite(self):
  self.prepare();self.s.close();c=copy.deepcopy(self.c);c['prerequisites']['configuration']='0'*64
  with self.assertRaises(Blocked):Session(self.db,self.anchor,c)
 def test_nonce_reserved(self):
  self.prepare()
  with self.assertRaises(Blocked):self.s.prepare(*make(self.c,'LAB-U-2',1))
 def test_blob_corruption(self):
  self.prepare();self.s.close();d=sqlite3.connect(self.db);d.execute("UPDATE blobs SET b=x'00' WHERE h=(SELECT h FROM blobs LIMIT 1)");d.commit();d.close()
  with self.assertRaises((Blocked,ValueError)):Session(self.db,self.anchor,self.c)
 def test_anchor_substitution(self):
  self.prepare();self.s.close();d=sqlite3.connect(self.anchor);d.execute("UPDATE head SET seq=0,h=?",('0'*64,));d.commit();d.close()
  with self.assertRaises(Blocked):Session(self.db,self.anchor,self.c)
 def test_real_process_exit_after_charge(self):
  self.prepare();self.s.close()
  def worker():
   s=Session(self.db,self.anchor,self.c);s.charge('attempt','LAB-U-1','a');os._exit(77)
  p=multiprocessing.get_context('fork').Process(target=worker);p.start();p.join(5);self.assertEqual(p.exitcode,77);self.s=Session(self.db,self.anchor,self.c);self.assertEqual(self.s.counts['attempt'],1);self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_partition_shared_consumers(self):
  c=config(queries=3,snapshots=3);c['staging_query_limit']=2;c['staging_snapshot_limit']=2
  with Session(self.p/'part.db',self.p/'part-anchor.db',c,True) as x:
   x.prepare(*make(c));x.charge('query',None,'outside','other');x.charge('query','LAB-U-1','inside1');x.charge('query','LAB-U-1','inside2')
   with self.assertRaises(Blocked):x.charge('query','LAB-U-1','inside3')
   with self.assertRaises(Blocked):x.charge('query',None,'outside2','other')
   x.charge('snapshot',None,'s1');x.charge('snapshot',None,'s2')
   with self.assertRaises(Blocked):x.charge('snapshot',None,'s3')
   x.charge('snapshot',None,'other-snapshot','other');self.assertEqual(x.counts['snapshot'],3)
 def test_real_exit_after_transmission(self):
  self.prepare();self.s.close();received=self.p/'simulated-receiver.bin'
  def worker():
   x=Session(self.db,self.anchor,self.c);t=OfflineTransport();original=t.send
   def send(rec,raw):
    original(rec,raw)
    with received.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os._exit(78)
   t.send=send;x.submit('LAB-U-1','a',t)
  p=multiprocessing.get_context('fork').Process(target=worker);p.start();p.join(5);self.assertEqual(p.exitcode,78)
  self.s=Session(self.db,self.anchor,self.c);rec,raw=self.s.hydrate(self.s.states['LAB-U-1']);self.assertEqual(received.read_bytes(),raw)
  self.assertEqual(self.s.states['LAB-U-1']['status'],'UNCERTAIN');self.t.outcome=outcome(self.s);self.assertEqual(self.s.reconcile('LAB-U-1','q',self.t)['status'],'SUCCESS')
 def test_configuration_input_mutation(self):
  self.c['prerequisites']['model']='0'*64
  self.s.internal_repair() # constructor owns its own immutable config
  self.assertNotEqual(self.s.config['prerequisites']['model'],self.c['prerequisites']['model'])
 def test_operational_pilot_forbidden(self):
  c=config();c['pilot']='I164-NORMAL-REJECTION-PILOT-001'
  with self.assertRaises(Blocked):Session(self.p/'no.db',self.p/'no-anchor.db',c,True)
 def test_reopen_missing_anchor_no_replacement(self):
  self.prepare();self.s.close();self.anchor.unlink()
  with self.assertRaises(Blocked):Session(self.db,self.anchor,self.c)
  self.assertFalse(self.anchor.exists())
 def test_two_process_competing_send(self):
  self.prepare();self.s.close();ctx=multiprocessing.get_context('fork');held=ctx.Event();release=ctx.Event();queue=ctx.Queue()
  def owner():
   with Session(self.db,self.anchor,self.c) as x:
    held.set();release.wait(3);x.submit('LAB-U-1','a',OfflineTransport());queue.put('SENT')
  def rival():
   held.wait(3)
   try:
    with Session(self.db,self.anchor,self.c) as x:x.submit('LAB-U-1','b',OfflineTransport())
    queue.put('ERROR')
   except Blocked:queue.put('BLOCKED')
   finally:release.set()
  a=ctx.Process(target=owner);b=ctx.Process(target=rival);a.start();b.start();a.join(5);b.join(5)
  self.assertEqual(sorted([queue.get(timeout=1),queue.get(timeout=1)]),['BLOCKED','SENT']);self.s=Session(self.db,self.anchor,self.c);self.assertEqual(self.s.counts['attempt'],1)
 def test_uncommitted_write_process_crash(self):
  self.prepare();self.s.close()
  def child():
   x=Session(self.db,self.anchor,self.c);x.db.execute('BEGIN IMMEDIATE');x.db.execute("UPDATE guard.head SET h=?",('e'*64,));os._exit(79)
  p=multiprocessing.get_context('fork').Process(target=child);p.start();p.join(5);self.assertEqual(p.exitcode,79);self.s=Session(self.db,self.anchor,self.c);self.assertEqual(self.s.counts['attempt'],0)
 def test_receipt_coordinates_across_requests(self):
  self.prepare();self.s.prepare(*make(self.c,'LAB-U-2',2));a=self.s.charge('query','LAB-U-1','q1');b=self.s.charge('query','LAB-U-2','q2')
  self.assertNotEqual(a['binding'],b['binding']);self.assertEqual((a['ordinal'],b['ordinal']),(1,2));self.assertEqual(a['pilot'],self.c['pilot']);self.reopen();self.assertEqual(self.s.receipts['q1'],a)
if __name__=='__main__':
 t=time.monotonic();suite=unittest.defaultTestLoader.loadTestsFromTestCase(Cases);result=unittest.TextTestRunner(verbosity=2).run(suite)
 print(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'seconds':time.monotonic()-t,'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'actual_admission':False,'transport':'OFFLINE-SIMULATED'},indent=2));sys.exit(not result.wasSuccessful())
