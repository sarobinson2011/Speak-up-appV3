import json,tempfile,unittest,copy
from pathlib import Path
from unittest.mock import patch
from fixtures.integrated import make,export
from fixtures.construct import dataset,wire
from integrated_auth.collector import run as uninterrupted
from recovery_schedule.runner import run
from recovery_schedule.state import Scheduler
from link_recovery.cli import create_key,PauseRequested
from v4_ingest.records import ValidationError

class SchedulingTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.p=Path(self.temp.name);self.m,self.t=make(self.p/'input');create_key(self.p/'key');self.ck=self.p/'journal'
 def execute(self,**kw):return run(self.m,self.t,self.ck,self.p/'key',**kw)
 def semantic(self,r):
  x=copy.deepcopy(r)
  for k in ('stage_schedule','semantic_acquisition'):x.pop(k,None)
  # Timings/replay diagnostics differ; exact verdict, failures, commitments and
  # separate validated counts must be identical.
  if x.get('bindings'):
   for auth in x['bindings']['bundle_authentication'].values():
    for s in ('byte_stage','crypto_stage'):auth.pop(s,None)
   for scope in x['bindings']['scope_validation']['scopes'].values():
    link=scope.get('link_validation',{});scope['link_validation']={k:link[k] for k in ('complete','complete_stream_sha256','structural_rows','potential_rows') if k in link}
  return x
 def test_native_scoped_completion_matches_uninterrupted(self):
  expected=uninterrupted(self.m,self.t,self.p/'plain',self.p/'key');actual=self.execute();self.assertFalse(actual['failures'],actual)
  self.assertEqual(self.semantic(actual),self.semantic(expected));self.assertFalse(actual['profile_admitted'])
  for s in actual['bindings']['scope_validation']['scopes'].values():self.assertIn('expected_potential_rows',s['link_validation'])
 def test_completed_stages_and_terminal_reuse(self):
  a=self.execute()
  with patch('integrated_auth.collector.collect',side_effect=AssertionError('ledger recomputed')),patch('link_recovery.cli.execute',side_effect=AssertionError('native rerun')):
   b=self.execute(resume=True)
  self.assertTrue(b['stage_schedule']['terminal_reused']);self.assertGreater(b['stage_schedule']['identity_bytes_reread'],0);self.assertEqual(self.semantic(a),self.semantic(b))
 def test_repeat_pause_partial_rows(self):
  r=self.execute(new_bytes=1);self.assertEqual(r['result'],'PAUSED')
  for n in (17,83,10000000):r=self.execute(resume=True,new_bytes=n)
  self.assertFalse(r['failures'],r);self.assertTrue(r['processing_complete'])
 def test_native_partial_state_and_quanta(self):
  # Semantic bytes finish first; force native worker to pause at arbitrary row
  # offsets independently of larger authentication/acquisition byte limits.
  from link_recovery import cli
  orig=cli.execute
  def cut(a):a.new_bytes=23;return orig(a)
  with patch.object(cli,'execute',cut):r=self.execute(auth_new_bytes=10000000)
  self.assertEqual(r['result'],'PAUSED')
  states=list(Path(str(self.ck)+'.stages').glob('*.native'));self.assertEqual(len(states),3)
  for p in states:
   obj=json.loads(p.read_text())['payload'];self.assertEqual(obj['state']['offset'],23);self.assertIsNotNone(obj['state']['sha_h'])
  r=self.execute(resume=True,new_bytes=10000000,quanta=3);self.assertFalse(r['failures'],r)
 def test_index_reuse_after_interruption_before_ledger_commit(self):
  original=Scheduler.save
  def stop(s,label,*a,**kw):
   if label=='ordered-ledger':raise PauseRequested()
   return original(s,label,*a,**kw)
  with patch.object(Scheduler,'save',stop),self.assertRaises(PauseRequested):self.execute()
  with patch('semantic_stream.storage.Document.parse',side_effect=AssertionError('canonical parse repeated')):
   r=self.execute(resume=True)
  self.assertFalse(r['failures'],r);self.assertTrue(any(x['status']=='REUSED-CANONICAL-INDEX-EXACT-BYTES' for x in r['stage_schedule']['events']))
 def test_source_mutation_after_completion_collects_failure(self):
  self.execute();p=self.p/'input/security_records_hex.bin';raw=p.read_bytes();p.write_bytes(raw[:-1]+b' ')
  r=self.execute(resume=True);self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted'])
 def test_corrupt_and_substituted_receipts(self):
  self.execute();root=Path(str(self.ck)+'.stages');receipts=list(root.glob('*.json'));p=next(p for p in receipts if 'ledger-output' not in p.name);raw=p.read_bytes();p.write_bytes(raw[:-1]+b'x')
  with self.assertRaises((ValueError,KeyError)):self.execute(resume=True)
 def test_corrupt_native_state_even_after_completion(self):
  self.execute();p=next(Path(str(self.ck)+'.stages').glob('*.native'));p.write_bytes(b'{}\n')
  with self.assertRaises(ValueError):self.execute(resume=True)
 def test_corrupt_main_journal_after_completion(self):
  self.execute();self.ck.write_bytes(b'{}\n')
  with self.assertRaises(ValueError):self.execute(resume=True)
 def test_corrupt_index_rejected(self):
  self.execute();p=next(Path(str(self.ck)+'.stages').glob('*.sqlite'))
  with p.open('r+b') as f:f.write(b'WRONG')
  with self.assertRaises(ValueError):self.execute(resume=True)
 def test_wrong_trusted_input_or_missing_qualification_rejects(self):
  self.execute();t=json.loads(self.t.read_bytes());t['laboratory_assumptions'].pop('assessor-competence');self.t.write_bytes(wire(t))
  with self.assertRaises(ValueError):self.execute(resume=True)
  fresh=run(self.m,self.t,self.p/'new',self.p/'key');self.assertIn('INVALID-EVIDENCE-AUTHORITY',fresh['failures']);self.assertFalse(fresh['bindings']['computed_budgets'])
 def test_atomic_stage_write_interruption_recovers(self):
  def fault(stage):
   if stage=='after_file_fsync':raise OSError('injected stage receipt interruption')
  with self.assertRaises(OSError):self.execute(fault=fault)
  r=self.execute(resume=self.ck.exists());self.assertFalse(r['failures'],r)
 def test_changed_scope_descriptor_not_caller_authority(self):
  self.execute();p=next(Path(str(self.ck)+'.stages').glob('*.descriptor'));p.write_text('LINKS 2 0 0\nA\nB\n')
  with self.assertRaises(ValueError):self.execute(resume=True)
 def test_cross_scope_native_journal_substitution(self):
  self.execute();ps=list(Path(str(self.ck)+'.stages').glob('*.native'));ps[0].write_bytes(ps[1].read_bytes())
  with self.assertRaises(ValueError):self.execute(resume=True)
 def test_independent_signature_failure_and_malformed_record(self):
  from tests.test_admission import bad_signature
  q,t=dataset();bad_signature(q);q['security_records_hex']=b'{} '.hex();m,tp=export(self.p/'bad',q,t)
  r=run(m,tp,self.p/'bad-journal',self.p/'key');self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures']);self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')

 def test_deadline_during_terminal_recheck_is_pause_not_success(self):
  from integrated_auth.collector import Paused
  self.execute()
  with patch.object(Scheduler,'verify',side_effect=Paused()),self.assertRaises(Paused):self.execute(resume=True)
 def test_pending_native_journal_substitution_collects_failure(self):
  from link_recovery import cli
  orig=cli.execute
  def cut(a):a.new_bytes=23;return orig(a)
  with patch.object(cli,'execute',cut):self.execute()
  ps=list(Path(str(self.ck)+'.stages').glob('*.native'));ps[0].write_bytes(ps[1].read_bytes())
  r=self.execute(resume=True)
  self.assertIn('INVALID-ACTION-CONTEXT',r['failures']);self.assertFalse(r['profile_admitted'])
 def test_multiple_quanta_retain_one_execution_boundary(self):
  from link_recovery import cli
  orig=cli.execute
  def cut(a):a.new_bytes=97;return orig(a)
  with patch.object(cli,'execute',cut):r=self.execute(quanta=100,auth_new_bytes=10000000)
  self.assertFalse(r['failures'],r);self.assertTrue(r['processing_complete'])
  self.assertGreater(sum(x['stage']=='collector-quantum' for x in r['stage_schedule']['events']),1)
 def test_crypto_partial_then_resume_preserves_exact_verdict(self):
  a=self.execute(auth_new_bytes=23);self.assertEqual(a['result'],'PAUSED')
  journals=list(self.p.glob('journal.*.crypto'));self.assertEqual(len(journals),3)
  for path in journals:
   result=json.loads(path.read_bytes())['payload']['result'];self.assertFalse(result['cryptographic_signature_verified']);self.assertEqual(result['offset'],23)
  self.assertFalse(a['processing_complete']);self.assertFalse(a['profile_admitted'])
  b=self.execute(resume=True,auth_new_bytes=10000000);self.assertFalse(b['failures'],b)
  expected=uninterrupted(self.m,self.t,self.p/'reference',self.p/'key')
  self.assertEqual(self.semantic(b),self.semantic(expected))
 def test_independent_delta_and_noncontiguous_scope_projection(self):
  from fixtures.scope_cases import disconnected
  for name,pair in [('delta',dataset('DELTA')),('disconnected',disconnected())]:
   m,t=export(self.p/name,*pair)
   a=run(m,t,self.p/(name+'-scheduled'),self.p/'key');b=uninterrupted(m,t,self.p/(name+'-plain'),self.p/'key')
   self.assertFalse(a['failures'],a);self.assertEqual(self.semantic(a),self.semantic(b))
  descriptors=list(Path(str(self.p/'disconnected-scheduled')+'.stages').glob('*.descriptor'))
  self.assertTrue(any(int(p.read_text().split()[1])<6 for p in descriptors))
