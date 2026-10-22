import unittest,tempfile,copy,json,subprocess,sys,shutil
from pathlib import Path
import test_provider as t,provider,outcome,connected,sole_service,backend,strict_types as strict
from anchor import *
ROOT=Path(__file__).resolve().parents[1]
CASES=['nonce-boolean','query-ordinal-boolean','gas-float']
def rebind(p,f):
 src=p['statement']['claim']['source'];inv=provider.invocation(src,f.policy['domain'],f.policy['finality_basis']);a=p['assessment']['claim'];a['invocation']=inv
 for tr in a['trace']:tr['invocation_sha256']=sha(enc(inv))
 a['result']['invocation_sha256']=sha(enc(inv));a['result']['trace_sha256']=sha(enc(a['trace']));t.resign(p)
def mutate(p,f,case):
 s=p['statement']['claim']['source']
 if case=='query-ordinal-boolean':s['context']['query_ordinal']=True
 else:
  z=json.loads(bytes.fromhex(s['rpc_response_hex']))
  if case=='nonce-boolean':z['result']['transaction']['nonce']=True
  else:z['result']['transaction']['actions'][0]['FunctionCall']['gas']=1e15
  s['rpc_response_hex']=enc(z).hex()
 rebind(p,f);return p

def seed_invalid_saved(f,packet):
 """Adversarial persistence fixture, NOT a production migration or repair.
 Make a coherent one-event saved-evidence mutation, retaining old SUCCESS cache.
 All service history/receipt/blob hashes are updated so rejection must reach types.
 """
 s=f.s.fresh();v=s['u'][f.u];saved=v['saved'];body=enc({'evidence':packet});ref=sha(body)
 event=parse(f.b.get('SEQ/'+str(saved['seq'])),MAX_EVENT)
 event['request']['body_hash']=sha(body);event['after']['u'][f.u]['saved']['ref']=ref
 ev=enc(event);head=sha(ev);new=dict(event['after'],head=head)
 receipt={'request':event['request'],'seq':saved['seq'],'head':head}
 f.b.db.execute('BEGIN IMMEDIATE')
 for key,value in [('BLOB/'+ref,body),('SEQ/'+str(saved['seq']),ev),('OP/'+saved['op'],enc(receipt)),('HEAD',enc(new))]:f.b.db.execute('INSERT OR REPLACE INTO objects VALUES (?,?)',(key,value))
 f.b.db.execute('COMMIT')
 return head
class Tests(unittest.TestCase):
 def test_exact_signed_review_witnesses(self):
  for case in CASES:
   x=json.loads((ROOT/'evidence/witnesses'/(case+'-fixture.json')).read_bytes())
   with self.assertRaisesRegex(Blocked,'TYPE:'):provider.validate(x['packet'],x['expected'],bytes.fromhex(x['evm_hex']),x['policy'])
 def test_preserved_adjacent_witnesses(self):
  for p in (ROOT/'results/adjacent-original').glob('*.json'):
   if p.name=='results.json':continue
   x=json.loads(p.read_bytes())
   with self.assertRaisesRegex(Blocked,'TYPE:'):provider.validate(x['packet'],x['expected'],bytes.fromhex(x['evm_hex']),x['policy'])
 def test_old_version_job_refuses_migration(self):
  import zipfile,io
  with zipfile.ZipFile(ROOT/'evidence/type-review.zip') as z:old=z.read('evidence/input.zip')
  with tempfile.TemporaryDirectory() as d:
   with zipfile.ZipFile(io.BytesIO(old)) as z:
    prefix='Engineering-288B-I164-outcome-provider/results/fixture-before-repair/'
    for name in z.namelist():
     if name.startswith(prefix):
      p=Path(d)/name[len(prefix):];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
   before={str(p.relative_to(d)):sha(p.read_bytes()) for p in Path(d).rglob('*') if p.is_file()}
   p=subprocess.run([sys.executable,'-B',str(ROOT/'code/provider_cli.py'),'recover',d],capture_output=True,timeout=15)
   self.assertNotEqual(p.returncode,0);self.assertIn(b'WIRE-JOURNAL-BINDING',p.stderr)
   after={str(p.relative_to(d)):sha(p.read_bytes()) for p in Path(d).rglob('*') if p.is_file()};self.assertEqual(before,after)
 def test_normal_observation_all_three(self):
  for case in CASES:
   with tempfile.TemporaryDirectory() as d:
    f=t.Fixture(d)
    try:
     f.sent();p=mutate(f.packet(),f,case);before=connected.copy_counts(f.s.fresh())
     with self.assertRaisesRegex(Blocked,'TYPE:'):f.x.save_outcome_evidence(f.u,'observe',p)
     self.assertEqual(before,connected.copy_counts(f.s.fresh()));self.assertIsNone(f.s.fresh()['u'][f.u]['saved']);self.assertEqual(f.x.executor.states[f.u]['status'],'UNCERTAIN');self.assertEqual(len(f.sink.sent),1)
    finally:f.close()
 def test_saved_evidence_service_repair_all_three(self):
  for case in CASES:
   with tempfile.TemporaryDirectory() as d:
    f=t.Fixture(d);f.sent();p=f.packet();f.x.save_outcome_evidence(f.u,'observe',p)
    head=seed_invalid_saved(f,mutate(copy.deepcopy(p),f,case));cfg,pre,desc=f.cfg,f.pre,f.desc;f.close()
    b=backend.SimulatedBackend(Path(d)/'service.db',desc);s=sole_service.Service(b,cfg,pre);before=b.get('HEAD')
    try:
     with self.assertRaisesRegex(Blocked,'TYPE:'):s.commit(head,'repair-malformed','REPAIR','LAB-U-1')
     self.assertEqual(before,b.get('HEAD'));self.assertIsNone(b.get('OP/repair-malformed'))
    finally:b.close()
    # Normal Connected construction calls recovery; invalid persisted evidence
    # fails before even a cached SUCCESS computation can be considered eligible.
    with self.assertRaisesRegex((Blocked,Uncertain),'TYPE:|INGRESS'):t.Fixture(d,False)
 def test_connected_internal_repair_all_three(self):
  for case in CASES:
   with tempfile.TemporaryDirectory() as d:
    f=t.Fixture(d);f.sent();p=f.packet();f.x.save_outcome_evidence(f.u,'observe',p);seed_invalid_saved(f,mutate(copy.deepcopy(p),f,case))
    # Cache removal models a reopened client; no authority is introduced. The
    # malformed authoritative service bytes are the test's fault injection.
    f.client.last=None;f.s.last=None
    before=f.b.get('HEAD')
    try:
     with self.assertRaisesRegex((Blocked,Uncertain),'TYPE:|INGRESS'):f.x.internal_terminal_repair()
     self.assertEqual(before,f.b.get('HEAD'));self.assertEqual(len(f.sink.sent),1)
    finally:f.close()
 def test_nested_assessment_domain_and_appointment(self):
  with tempfile.TemporaryDirectory() as d:
   f=t.Fixture(d);f.sent();p=f.packet()
   try:
    for loc in ['statement','invocation']:
     q=copy.deepcopy(p)
     if loc=='statement':q['statement']['claim']['domain']['protocol']=87.0
     else:q['assessment']['claim']['invocation']['context']['query_ordinal']=True
     t.resign(q)
     with self.assertRaisesRegex(Blocked,'TYPE:'):f.decode(q)
    pol=copy.deepcopy(f.policy);a=pol['provider']['appointment']['claim'];a['laboratory_assumption']=1;pol['provider']['appointment']=t.signed('authority','appointment',a)
    with self.assertRaisesRegex(Blocked,'TYPE:'):provider.validate_policy(pol)
    pol=copy.deepcopy(f.policy);pol['assessor']['qualification']['claim']=copy.deepcopy(pol['assessor']['qualification']['claim']);a=pol['assessor']['qualification']['claim'];a['domain']['protocol']=87.0;pol['assessor']['qualification']=t.signed('qualifier','qualification',a)
    with self.assertRaisesRegex(Blocked,'TYPE:'):provider.validate_policy(pol)
   finally:f.close()
 def test_optional_priority_and_source_boolean_flags(self):
  with tempfile.TemporaryDirectory() as d:
   f=t.Fixture(d);f.sent()
   try:
    for value in [False,0.0]:
     p=f.packet();s=p['statement']['claim']['source'];z=json.loads(bytes.fromhex(s['rpc_response_hex']));z['result']['transaction']['priority_fee']=value;s['rpc_response_hex']=enc(z).hex();rebind(p,f)
     with self.assertRaisesRegex(Blocked,'TYPE:'):f.decode(p)
    for field in ['source_authenticated','qualification_established']:
     p=f.packet();p['statement']['claim']['source']['provenance'][field]=0;rebind(p,f)
     with self.assertRaisesRegex(Blocked,'TYPE:'):f.decode(p)
    p=f.packet();s=p['statement']['claim']['source'];z=json.loads(bytes.fromhex(s['rpc_response_hex']));del z['result']['transaction']['priority_fee'];s['rpc_response_hex']=enc(z).hex();rebind(p,f);self.assertEqual(f.decode(p)['conditional_terminal'],'SUCCESS')
   finally:f.close()
 def test_declared_integer_boundaries_and_opaque_values(self):
  for bits in (64,128):
   for v in (0,2**bits-1):strict.uint(v,bits,'fixture')
   for v in (True,False,0.0,1.0,-1,2**bits):
    with self.assertRaises(Blocked):strict.uint(v,bits,'fixture')
  # Generic JSON parsing is unchanged; no global float ban.
  self.assertEqual(outcome.obj(b'{"opaque":[true,1.5,null]}'),{'opaque':[True,1.5,None]})
  self.assertTrue(strict.same({'x':1.5},{'x':1.5}))
  with self.assertRaises(Blocked):strict.same({'x':[True]},{'x':[1]})
 def test_valid_saved_recovery_and_unavailable(self):
  for missing in [None,'provider','assessor']:
   with tempfile.TemporaryDirectory() as d:
    f=t.Fixture(d,missing=missing);f.sent();f.x.save_outcome_evidence(f.u,'observe',f.packet());before=connected.copy_counts(f.s.fresh());f.close();f=t.Fixture(d,False,missing=missing)
    try:
     f.x.internal_terminal_repair();f.x.internal_terminal_repair();self.assertEqual(before,connected.copy_counts(f.s.fresh()));self.assertEqual(f.x.executor.states[f.u]['status'],'UNCERTAIN' if missing else 'SUCCESS')
    finally:f.close()
if __name__=='__main__':unittest.main()
