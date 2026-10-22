import unittest,tempfile,shutil,subprocess,os,sqlite3,json
from fixtures import *
class Repair(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'job';self.c=config();self.b=Bridge(self.p,self.c,True)
 def tearDown(self):self.b.close();self.tmp.cleanup()
 def reopen(self):self.b.close();self.b=Bridge(self.p,self.c)
 def prepare(self):self.b.retire('LAB-U-1',intent(self.c));self.b.seal_conditional('LAB-U-1');self.b.prepare('LAB-U-1',*envelope(self.b))
 def test_before_acceptance_cuts(self):
  for cut in ['before_reservation','inside_reservation']:
   with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),cut)
   self.reopen();self.assertEqual(self.b.reservations(),{});self.assertEqual(self.b.executor.states,{})
 def test_all_accepted_cuts(self):
  for cut in ['after_reservation','before_executor','after_executor','after_clear']:
   with tempfile.TemporaryDirectory() as d:
    b=Bridge(d,self.c,True)
    try:
     with self.assertRaises(RuntimeError):b.retire('LAB-U-1',intent(self.c),cut)
    finally:b.close()
    with Bridge(d,self.c) as b:
     self.assertEqual(b.executor.states['LAB-U-1']['status'],'RETIRED')
     for _ in range(3):b.recover()
     for changed in [False,True]:
      i=intent(self.c)
      if changed:i['registry']='3'*40
      with self.assertRaisesRegex(ValueError,'IRREVERSIBLY'):b.retire('LAB-U-1',i)
 def test_D1_old_executor_anchor_intact(self):
  old=Path(self.tmp.name)/'backup.zip';self.b.backup(old,'backup')
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'after_executor')
  self.b.close();anchor=(self.p/'independent-anchor.db').read_bytes();transport=(self.p/'transport.db').read_bytes()
  with zipfile.ZipFile(old) as z:(self.p/'executor.db').write_bytes(z.read('executor.db'))
  self.assertEqual(anchor,(self.p/'independent-anchor.db').read_bytes());self.assertEqual(transport,(self.p/'transport.db').read_bytes())
  self.b=Bridge(self.p,self.c);self.assertEqual(self.b.executor.states['LAB-U-1']['intent_sha256'],e.sha(e.enc(intent(self.c))))
  i=intent(self.c);i['registry']='3'*40
  with self.assertRaises(ValueError):self.b.retire('LAB-U-1',i)
  self.assertEqual(self.b.transport.counts['snapshot'],1)
 def test_same_intent_single_lifecycle(self):
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'before_executor')
  self.reopen();self.b.seal_conditional('LAB-U-1');self.b.prepare('LAB-U-1',*envelope(self.b));sim=t.OfflineTransport();self.b.submit('LAB-U-1','a',sim);self.reopen()
  with self.assertRaises(ValueError):self.b.submit('LAB-U-1','retry',sim)
  with self.assertRaises(ValueError):self.b.retire('LAB-U-1',intent(self.c))
  self.assertEqual(sim.calls,1);self.assertEqual(self.b.transport.counts['attempt'],1)
 def test_real_process_exit_after_commit(self):
  self.b.close();script="from fixtures import *;import os,sys;b=Bridge(sys.argv[1],config());\ntry:b.retire('LAB-U-1',intent(config()),'after_executor')\nexcept RuntimeError:os._exit(77)"
  r=subprocess.run([sys.executable,'-B','-c',script,str(self.p)],env=dict(os.environ,PYTHONPATH=str(ROOT/'code')),capture_output=True,timeout=10);self.assertEqual(r.returncode,77,r.stderr);self.b=Bridge(self.p,self.c);self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'RETIRED')
 def test_uncommitted_reservation_process_exit(self):
  self.b.close();script="from fixtures import *;import sys,os;b=Bridge(sys.argv[1],config());b.transport.db.execute('BEGIN IMMEDIATE');b.transport.db.execute(\"INSERT INTO guard.reservations VALUES ('bad',x'00','bad','bad','bad','bad','bad')\");os._exit(78)"
  r=subprocess.run([sys.executable,'-B','-c',script,str(self.p)],env=dict(os.environ,PYTHONPATH=str(ROOT/'code')),capture_output=True,timeout=10);self.assertEqual(r.returncode,78,r.stderr);self.b=Bridge(self.p,self.c);self.assertEqual(self.b.reservations(),{})
 def test_competing_open(self):
  with self.assertRaises(ValueError):Bridge(self.p,self.c)
 def test_snapshot_after_completed_retirement_rejects_old(self):
  old=(self.p/'executor.db').read_bytes();self.b.retire('LAB-U-1',intent(self.c));self.b.close();(self.p/'executor.db').write_bytes(old)
  with self.assertRaises(ValueError):Bridge(self.p,self.c)
 def test_missing_pending_does_not_erase_reservation(self):
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'before_executor')
  self.b.transport.db.execute('UPDATE guard.bridge SET pending=NULL');self.b.close()
  with self.assertRaisesRegex(ValueError,'RESERVATION-COVERAGE'):Bridge(self.p,self.c)
 def test_reservation_immutable(self):
  self.b.retire('LAB-U-1',intent(self.c))
  for sql in ['DELETE FROM guard.reservations','UPDATE guard.reservations SET digest=\'bad\'']:
   with self.assertRaises(sqlite3.IntegrityError):self.b.transport.db.execute(sql)
 def test_corrupt_reservation_fails(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.transport.db.execute('DROP TRIGGER guard.reservations_no_update');self.b.transport.db.execute("UPDATE guard.reservations SET digest='bad'");self.b.close()
  with self.assertRaises(ValueError):Bridge(self.p,self.c)
 def test_duplicate_nonce_cannot_create_partial_reservation(self):
  self.b.retire('LAB-U-1',intent(self.c))
  with self.assertRaises(sqlite3.IntegrityError):self.b.retire('U2',intent(self.c,'U2'))
  self.reopen();self.assertEqual(set(self.b.reservations()),{'LAB-U-1'})
 def test_exhaustion_no_renewal(self):
  self.b.close();self.p=Path(self.tmp.name)/'small';self.c['attempt_limit']=1;self.c['query_limit']=1;self.b=Bridge(self.p,self.c,True);self.prepare();sim=t.OfflineTransport()
  with self.assertRaises(RuntimeError):self.b.submit('LAB-U-1','a',sim,'after_charge')
  self.b.status('q');self.reopen();self.b.recover()
  with self.assertRaises(ValueError):self.b.submit('LAB-U-1','retry',sim)
  with self.assertRaises(ValueError):self.b.status('q2')
  self.assertEqual(self.b.transport.counts,{'attempt':1,'query':1,'snapshot':0});self.assertEqual(sim.calls,0)
 def test_pre_evm_failure_distinct(self):
  self.prepare();sim=t.OfflineTransport();self.b.submit('LAB-U-1','a',sim);sim.outcome=outcome(self.b,near='FAILURE',evm='NOT-EXECUTED');r=self.b.reconcile('LAB-U-1','q',sim);self.assertIn('UNAVAILABLE',r['executor_resolution']);self.reopen();self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_operational_block(self):
  with self.assertRaises(ValueError):self.b.operational_submit()
 def test_interruption_during_recovery_commit(self):
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'before_executor')
  self.b.transport.db.execute("CREATE TRIGGER guard.block_clear BEFORE UPDATE ON bridge WHEN NEW.pending IS NULL BEGIN SELECT RAISE(ABORT,'INTERRUPT-CLEAR'); END")
  with self.assertRaises(sqlite3.IntegrityError):self.b.recover()
  self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'RETIRED')
  self.b.transport.db.execute('DROP TRIGGER guard.block_clear');self.reopen();self.b.recover()
  self.assertEqual(len(self.b.reservations()),1)
if __name__=='__main__':unittest.main(verbosity=2)
