import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from fixtures.occurrence import make_data,tse_bytes
from fixtures.integrated import export
from fixtures.construct import wire,sha
from recovery_schedule.runner import run
from integrated_auth.collector import run as plain
from link_recovery.cli import create_key,PauseRequested
from semantic_stream.storage import Store,ACTIVE
from occurrence_values.codec import validate
from v4_ingest.typed import Codec

class OccurrenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name);create_key(self.p/'key');self.n=0
 def case(self,mutation=None,**kw):
  q,t,o=make_data(**kw)
  if mutation:mutation(q,t)
  self.n+=1;p=self.p/str(self.n);m,tr=export(p,q,t);return m,tr,o,p
 def go(self,case,**kw):m,t,o,p=case;return run(m,t,p/'journal',self.p/'key',**kw)
 def oracle(self,r,o):
  self.assertFalse(r['failures'],r);self.assertFalse(r['profile_admitted']);self.assertFalse(r['actual_qualification_established'])
  for scope,e in o.items():
   s=r['bindings']['scope_validation']['scopes'][scope];self.assertEqual(s['node_indices'],e['indices']);v=s['link_validation'];self.assertEqual(v['complete_stream_sha256'],e['links_sha256']);self.assertEqual(v['structural_rows'],e['structural']);self.assertEqual(v['potential_rows'],e['potential']);self.assertTrue(r['bindings']['bundle_authentication'][scope]['signature_valid'])
 def replace(self,q,t,ref,fn):
  old=ref['material_sha256'];obj=json.loads(bytes.fromhex(q['materials'][old]));fn(obj['payload']);raw=wire(obj);new=sha(raw);q['materials'][new]=raw.hex();t['anchors'][ref['source_anchor']]=new;ref['material_sha256']=new
 def test_all_phases_two_codecs_and_families(self):
  for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
   for codec in ('TSEV1','S90-JSON-LF'):
    for family in ('GAMMA','DELTA'):
     c=self.case(phase=phase,codec=codec,family=family);self.oracle(self.go(c),c[2])
 def test_disconnected_scope_exact_projection(self):
  c=self.case(disconnected=True);r=self.go(c);self.oracle(r,c[2]);self.assertEqual(len(c[2]['ROOT-ELIGIBLE']['indices']),2)
 def test_bucket_collisions_never_merge_unequal_values(self):
  c=self.case()
  with patch('occurrence_values.index.bucket',return_value='COLLISION'):self.oracle(self.go(c),c[2])
 def test_missing_or_unavailable_never_symbolic_fallback(self):
  for mutation in (lambda q,t:q['occurrence_bindings'].pop(next(iter(q['occurrence_bindings']))),lambda q,t:q['materials'].pop(next(iter(t['occurrence_bindings'].values()))['material_sha256']),lambda q,t:t.pop('occurrence_source_ref')):
   c=self.case(mutation);r=self.go(c);self.assertTrue(r['failures']);self.assertIsNone(r['occurrence_acquisition']);self.assertFalse(r['bindings']['computed_budgets'])
 def test_wrong_owner_source_binding(self):
  def mut(q,t):t['source_id']='WRONG'
  r=self.go(self.case(mut));self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures'])
 def test_duplicate_conflicting_and_missing_assignments(self):
  for kind in ('duplicate','conflict','missing','unexpected'):
   def mut(q,t):
    def change(p):
     if kind=='missing':p['assignments'].pop()
     elif kind=='unexpected':p['assignments'][0]['token_id']='ABSENT'
     else:
      p['assignments'][1]['token_id']=p['assignments'][0]['token_id']
      if kind=='duplicate':p['assignments'][1]=copy.deepcopy(p['assignments'][0])
    self.replace(q,t,t['occurrence_source_ref'],change)
   r=self.go(self.case(mut));self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures'])
 def test_exact_metadata_joins(self):
  for key in ('phase','model_sha256','profile_sha256','contract_sha256','source_sha256','mapping_digest','attempt'):
   def mut(q,t):self.replace(q,t,t['occurrence_source_ref'],lambda p:p['binding'].__setitem__(key,999 if key=='attempt' else 'WRONG'))
   r=self.go(self.case(mut));self.assertIn('INVALID-ACTION-CONTEXT',r['failures'])
 def test_occurrence_owner_context_record_and_type(self):
  for key in ('surface_id','context','record','type_id'):
   def mut(q,t):self.replace(q,t,t['occurrence_source_ref'],lambda p:p['assignments'][0].__setitem__(key,'WRONG'))
   self.assertTrue(self.go(self.case(mut))['failures'])
 def test_cross_scope_signed_bundle_substitution(self):
  def mut(q,t):q['bundles']['ROOT-ELIGIBLE']=copy.deepcopy(q['bundles']['NOT-APPLICABLE'])
  self.assertTrue(self.go(self.case(mut,disconnected=True))['failures'])
 def test_cross_phase_input_substitution(self):
  def mut(q,t):q['phase']='PRE-COMMITMENT'
  r=self.go(self.case(mut));self.assertIn('INVALID-ACTION-CONTEXT',r['failures']);self.assertFalse(r['bindings']['computed_budgets'])
 def test_qualification_not_inferred_from_index_or_signatures(self):
  def mut(q,t):t['laboratory_assumptions'].pop('source-producer-correspondence')
  r=self.go(self.case(mut));self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['bindings']['computed_budgets']);self.assertFalse(r['actual_qualification_established'])
 def test_arbitrary_chunk_boundaries_and_repeated_resume(self):
  for chunk in (1,7,31,65536):
   c=self.case(phase='PRE-EXECUTION');r=self.go(c,new_bytes=1,chunk_bytes=chunk);self.assertEqual(r['result'],'PAUSED')
   r=self.go(c,resume=True,new_bytes=53,chunk_bytes=chunk);self.assertEqual(r['result'],'PAUSED')
   r=self.go(c,resume=True,chunk_bytes=chunk);self.oracle(r,c[2]);self.oracle(self.go(c,resume=True),c[2])
 def test_native_partial_row_and_uninterrupted_oracle(self):
  from link_recovery import cli
  c=self.case(phase='PRE-COMMITMENT',disconnected=True);original=cli.execute
  def cut(a):a.new_bytes=23;return original(a)
  with patch.object(cli,'execute',cut):self.assertEqual(self.go(c)['result'],'PAUSED')
  self.oracle(self.go(c,resume=True),c[2]);m,t,o,p=c;self.oracle(plain(m,t,p/'plain',self.p/'key'),o)
 def test_interrupted_index_build_and_complete_stage_resume(self):
  import occurrence_values.acquire as mod
  c=self.case();original=mod.build
  def stop(*args,**kw):original(*args,**kw);raise PauseRequested()
  with patch.object(mod,'build',stop),self.assertRaises(PauseRequested):self.go(c)
  self.oracle(self.go(c,resume=True),c[2])
 def test_index_corruption_after_terminal_completion(self):
  c=self.case();self.go(c);p=Path(str(c[3]/'journal')+'.stages')/'occurrence-equality.sqlite';p.write_bytes(b'CORRUPT')
  with self.assertRaises(ValueError):self.go(c,resume=True)
 def test_input_mutation_after_completion(self):
  c=self.case();self.go(c);m=json.loads(c[0].read_bytes());p=c[3]/next(iter(m['materials'].values()))['path'];raw=p.read_bytes();p.write_bytes(raw[:-1]+b' ')
  self.assertTrue(self.go(c,resume=True)['failures'])
 def test_noncanonical_owned_value_fails_before_equality(self):
  for codec,bad in [('TSEV1',tse_bytes(b'x')+b'junk'),('S90-JSON-LF',b'"AB"\n')]:
   def mut(q,t):
    name=next(iter(t['occurrence_bindings']));ref=t['occurrence_bindings'][name];old=ref['material_sha256']
    self.replace(q,t,ref,lambda p:p.update(encoded_hex=bad.hex()))
    q['occurrence_bindings'][name]=copy.deepcopy(ref)
    root=t['occurrence_source_ref'];obj=json.loads(bytes.fromhex(q['materials'][root['material_sha256']]))
    for row in obj['payload']['assignments']:
     if row['token_id']==name:row['value_ref']=copy.deepcopy(ref)
    obj['dependencies']=[ref['material_sha256'] if h==old else h for h in obj['dependencies']]
    raw=wire(obj);h=sha(raw);q['materials'][h]=raw.hex();t['anchors'][root['source_anchor']]=h;root['material_sha256']=h
   r=self.go(self.case(mut,codec=codec));self.assertIn('INVALID-PROFILE-SCHEMA',r['failures']);self.assertIsNone(r['occurrence_acquisition'])
 def test_legacy_hex_entry_cannot_bypass_owning_validation(self):
  from admission_kernel.admission import collect
  q,t,o=make_data();r=collect(q,t)
  self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures']);self.assertFalse(r['profile_admitted']);self.assertFalse(r['bindings']['computed_budgets'])
 def test_actual_mode_stays_disabled(self):
  c=self.case(lambda q,t:q.update(mode='ACTUAL'));r=self.go(c);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['profile_admitted'])

class OwningCodecTests(unittest.TestCase):
 def setUp(self):self.s=Store();self.t=ACTIVE.set(self.s)
 def tearDown(self):ACTIVE.reset(self.t);self.s.close()
 def check(self,b,typ,derived=(),codec='TSEV1'):return validate(self.s.write([b]),codec,typ,derived,[])
 def test_independent_typed_oracle_primitive_derived_values(self):
  types=[('PAIR','TUPLE',['PE-TSE-UINT','PE-TSE-BYTES']),('ITEMS','SET',['PAIR'])];c=Codec(types)
  for typ,v in [('PE-TSE-BOOL3','TRUE'),('PE-TSE-BYTES',b''),('PE-TSE-ID','abc'),('PE-TSE-UINT',123),('PAIR',[7,b'x']),('ITEMS',[[7,b'x'],[2,b'yz']])]:self.check(c.encode(typ,v),typ,types)
 def test_malformed_truncated_wrong_type_tag_and_lengths(self):
  good=tse_bytes(b'abc')
  for b in (good[:-1],good+b'X',b'X'+good[1:],good[:9]+b'PE-TSE-BOGUS'+good[21:],b'TSEV1'+b'\xff'*4):
   with self.assertRaises(ValueError):self.check(b,'PE-TSE-BYTES')
  for body in (b'00',b'+1',b'',b' 1',b'-1'):
   name=b'PE-TSE-UINT';b=b'TSEV1'+len(name).to_bytes(4,'big')+name+b'\3'+len(body).to_bytes(8,'big')+body
   with self.assertRaises(ValueError):self.check(b,'PE-TSE-UINT')
 def test_set_order_duplicates_reserved_id_and_type_cycles(self):
  types=[('S','SET',['PE-TSE-BYTES'])];c=Codec(types);a=c.encode('PE-TSE-BYTES',b'a');b=c.encode('PE-TSE-BYTES',b'b')
  for elems in ((a,a),(b,a)):
   body=(2).to_bytes(4,'big')+b''.join(len(x).to_bytes(8,'big')+x for x in elems);raw=b'TSEV1'+(1).to_bytes(4,'big')+b'S'+b'\x10'+len(body).to_bytes(8,'big')+body
   with self.assertRaises(ValueError):self.check(raw,'S',types)
  with self.assertRaises(ValueError):self.check(c.encode('PE-TSE-ID','PE-TSE-SET'),'PE-TSE-ID')
  with self.assertRaises(ValueError):self.check(a,'S',[('S','SET',['S'])])
 def test_s90_canonical_json_lf_bytes_not_decoded_octets(self):
  self.check(b'"00ff"\n','BYTES',codec='S90-JSON-LF')
  for raw in (b'"00FF"\n',b'"00ff"',b' "00ff"\n',b'"0"\n',b'01\n',b'true\n'):
   with self.assertRaises(ValueError):self.check(raw,'BYTES',codec='S90-JSON-LF')
 def test_codec_capability_and_large_typed_body(self):
  raw=tse_bytes(b'x'*2097153);self.check(raw,'PE-TSE-BYTES')
  with self.assertRaises(ValueError):self.check(raw,'PE-TSE-BYTES',codec='UNKNOWN')
