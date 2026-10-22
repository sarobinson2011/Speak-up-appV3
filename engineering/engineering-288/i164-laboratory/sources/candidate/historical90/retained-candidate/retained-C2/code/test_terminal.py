import unittest,tempfile,shutil,sqlite3,subprocess,os,json
from fixtures import *
class C1(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)/'job';self.c=config();self.c['query_limit']=1;self.b=Bridge(self.p,self.c,True);self.sim=t.OfflineTransport()
 def tearDown(self):self.b.close();self.tmp.cleanup()
 def reopen(self):self.b.close();self.b=Bridge(self.p,self.c)
 def prepare(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.seal_conditional('LAB-U-1');self.b.prepare('LAB-U-1',*envelope(self.b));self.b.submit('LAB-U-1','a',self.sim)
 def gap(self,evm='SUCCESS',near='SUCCESS'):
  self.prepare();self.sim.outcome=outcome(self.b,near=near,evm=evm)
  with self.assertRaises(RuntimeError):self.b.reconcile('LAB-U-1','q',self.sim,'after_transport_result')
 def conserved(self):
  return (self.b.transport.head,dict(self.b.transport.counts),dict(self.b.transport.staging),list(self.b.transport.db.execute('SELECT * FROM guard.reservations')),self.sim.calls)
 def test_supplied_C1_closed(self):
  self.gap();self.reopen();before=self.conserved();self.assertIsNone(self.b.allowances.repair_anchor());self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'SUCCESS');self.assertEqual(before,self.conserved())
  with self.assertRaises(ValueError):self.b.status('extra')
  with self.assertRaises(ValueError):self.b.submit('LAB-U-1','retry',self.sim)
 def test_idempotent(self):
  self.gap();self.b.internal_terminal_repair();head=self.b.executor.head;before=self.conserved()
  for _ in range(5):self.reopen();self.assertIsNone(self.b.internal_terminal_repair());self.assertEqual(head,self.b.executor.head);self.assertEqual(before,self.conserved())
 def test_reverted(self):
  self.gap('REVERTED');self.b.internal_terminal_repair();self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'FAILED');self.assertEqual(self.b.executor.states['LAB-U-1']['reconciliation']['outcome'],'REVERTED')
 def test_pre_evm_not_reverted(self):
  self.gap('NOT-EXECUTED','FAILURE');before=self.conserved();head=self.b.executor.head;self.assertIsNone(self.b.internal_terminal_repair());self.assertEqual(self.b.executor.head,head);self.assertEqual(before,self.conserved());self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_no_outcome_keeps_uncertain(self):
  self.prepare();self.b.reconcile('LAB-U-1','q',self.sim);before=self.conserved();self.b.internal_terminal_repair();self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'UNCERTAIN');self.assertEqual(before,self.conserved())
 def test_no_oracle_calls(self):
  self.gap();self.sim.send=lambda *x:(_ for _ in ()).throw(AssertionError('send'));self.sim.lookup=lambda *x:(_ for _ in ()).throw(AssertionError('lookup'));self.b.allowances.reserve=lambda *x:(_ for _ in ()).throw(AssertionError('charge'));self.assertIsNone(self.b.internal_terminal_repair())
 def test_all_cuts(self):
  self.gap();base=Path(self.tmp.name)/'base';base.mkdir();self.b.close()
  for n in ['executor.db','transport.db','independent-anchor.db']:shutil.copyfile(self.p/n,base/n)
  for cut in ['after_validation','before_transition','before_executor','after_executor','after_clear']:
   d=Path(self.tmp.name)/cut;shutil.copytree(base,d)
   with Bridge(d,self.c) as b:
    with self.assertRaises(RuntimeError):b.internal_terminal_repair(cut)
   with Bridge(d,self.c) as b:
    b.internal_terminal_repair();b.internal_terminal_repair();self.assertEqual(b.executor.states['LAB-U-1']['status'],'SUCCESS');self.assertEqual(b.transport.counts['query'],1);self.assertEqual(b.transport.counts['attempt'],1)
  self.b=Bridge(self.p,self.c)
 def test_process_death(self):
  self.gap();self.b.close();script="from fixtures import *;import os,sys;c=config();c['query_limit']=1;b=Bridge(sys.argv[1],c);\ntry:b.internal_terminal_repair('after_executor')\nexcept RuntimeError:os._exit(77)"
  p=subprocess.run([sys.executable,'-B','-c',script,str(self.p)],env=dict(os.environ,PYTHONPATH=str(ROOT/'code')),capture_output=True,timeout=5);self.assertEqual(p.returncode,77,p.stderr);self.b=Bridge(self.p,self.c);self.b.internal_terminal_repair();self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'SUCCESS')
 def test_competing(self):
  self.gap()
  with self.assertRaises(ValueError):Bridge(self.p,self.c)
 def test_corrupt_or_missing_evidence(self):
  self.gap();ref=self.b.transport.states['LAB-U-1']['evidence'];self.b.transport.db.execute('UPDATE blobs SET b=? WHERE h=?',(b'corrupt',ref));head=self.b.executor.head
  with self.assertRaises(ValueError):self.b.internal_terminal_repair()
  self.assertEqual(head,self.b.executor.head)
 def test_wrong_charge_reference(self):
  self.gap();db=self.b.transport.db;seq,raw,h=db.execute('SELECT seq,b,h FROM log ORDER BY seq DESC LIMIT 1').fetchone();x=t.parse(raw);x['request']='a';raw=t.enc(x);digest=t.sha(raw);db.execute('UPDATE log SET b=?,h=? WHERE seq=?',(raw,digest,seq));db.execute('UPDATE guard.head SET h=?',(digest,))
  with self.assertRaises(ValueError):self.b.internal_terminal_repair()
  self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'UNCERTAIN')
 def test_wrong_outcome_binding(self):
  self.gap();db=self.b.transport.db;ref=self.b.transport.states['LAB-U-1']['evidence'];x=t.parse(self.b.transport.blob(ref));x['txid']='0'*64;raw=t.enc(x);new=t.sha(raw);db.execute('INSERT INTO blobs VALUES (?,?)',(new,raw));seq,event,h=db.execute('SELECT seq,b,h FROM log ORDER BY seq DESC LIMIT 1').fetchone();event=t.parse(event);event['evidence']=new;event=t.enc(event);db.execute('UPDATE log SET b=?,h=? WHERE seq=?',(event,t.sha(event),seq));db.execute('UPDATE guard.head SET h=?',(t.sha(event),))
  with self.assertRaises(ValueError):self.b.internal_terminal_repair()
 def test_conflicting_executor_terminal(self):
  self.gap();v=self.b.executor.states['LAB-U-1'];ev={'conditional_fixture':True,'tx_sha256':v['tx_sha256'],'intent_sha256':v['intent_sha256'],'outcome':'REVERTED','finality':'LAB-FINAL','source':'LAB-ORACLE'};r=dict(self.b.executor._latest['LAB-U-1']);r.update(status='FAILED',reconciliation_ref=e.sha(e.enc(ev)));self.b.transition('LAB-U-1',r,lambda:self.b.executor.reconcile('LAB-U-1',ev))
  with self.assertRaisesRegex(ValueError,'TERMINAL-CONFLICT'):self.b.internal_terminal_repair()
 def test_no_submission_evidence(self):
  self.b.retire('LAB-U-1',intent(self.c));self.b.seal_conditional('LAB-U-1');self.b.prepare('LAB-U-1',*envelope(self.b))
  with self.assertRaises(RuntimeError):self.b.submit('LAB-U-1','a',self.sim,'after_charge')
  self.sim.outcome=outcome(self.b);self.b.transport.reconcile('LAB-U-1','q',self.sim)
  with self.assertRaisesRegex(ValueError,'NO-EXECUTOR-SUBMISSION'):self.b.internal_terminal_repair()
 def test_cli_no_output(self):
  self.gap();self.b.close();script="from fixtures import *;import sys;c=config();c['query_limit']=1;\nwith Bridge(sys.argv[1],c) as b:b.internal_terminal_repair()"
  p=subprocess.run([sys.executable,'-B','-c',script,str(self.p)],env=dict(os.environ,PYTHONPATH=str(ROOT/'code')),capture_output=True,timeout=5);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout,b'');self.b=Bridge(self.p,self.c)
 def test_D1_reservation_retained(self):
  old=(self.p/'executor.db').read_bytes()
  with self.assertRaises(RuntimeError):self.b.retire('LAB-U-1',intent(self.c),'after_executor')
  self.b.close();(self.p/'executor.db').write_bytes(old);self.b=Bridge(self.p,self.c);self.assertIsNone(self.b.internal_terminal_repair());changed=intent(self.c);changed['registry']='3'*40
  with self.assertRaises(ValueError):self.b.retire('LAB-U-1',changed)
  self.assertEqual(self.b.executor.states['LAB-U-1']['status'],'RETIRED')
if __name__=='__main__':unittest.main(verbosity=2)
