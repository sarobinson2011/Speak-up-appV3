import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from semantic_stream.storage import Store,ACTIVE,Hex,unhex
from v4_ingest.records import canonical,parse,digest,primitive,ValidationError
from fixtures.construct import dataset,wire,sha
from fixtures.integrated import export
from integrated_auth.collector import run
from link_recovery.cli import create_key
from admission_kernel.sources import FiniteLabProvider
from semantic_stream.provider import StreamingProvider

class SemanticTests(unittest.TestCase):
 def setUp(self):self.store=Store();self.token=ACTIVE.set(self.store)
 def tearDown(self):ACTIVE.reset(self.token);self.store.close()
 def indexed(self,b):return parse(self.store.write([b]))
 def test_independent_exhaustive_canonical_values_and_chunk_boundaries(self):
  leaves=[None,True,False,0,1,-1,'','a','é','\\','"','\n','.$record']
  values=leaves+[[x,y] for x in leaves for y in leaves]+[{'a':x,'b':[x]} for x in leaves]
  for chunk in (1,2,7,65536):
   with patch('semantic_stream.storage.CHUNK',chunk):
    for v in values:
     raw=(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode();self.assertEqual(self.indexed(raw),v)
 def test_noncanonical_malformed_and_truncated(self):
  for b in (b'{}',b'{}\n\n',b'{"b":0,"a":0}\n',b'{"a":0,"a":1}\n',b'[01]\n',b'[-0]\n',b'[1.0]\n',b'[NaN]\n',b'"\\u0061"\n',b'[ ]\n',b'[true,]\n',b'"\xc3\xa9"\n',b'"unterminated',b'{} \n'):
   with self.subTest(b=b),self.assertRaises(ValueError):self.indexed(b)
 def test_disk_arrays_and_exact_roundtrip(self):
  v=[{'k':str(i),'v':[i,None]} for i in range(4000)];raw=wire(v);p=self.indexed(raw)
  self.assertEqual(p,v);self.assertEqual(v,p);self.assertEqual(digest(canonical(p)),sha(raw));self.assertEqual(p[3456],v[3456])
 def test_large_hex_and_primitive_id_unchanged(self):
  raw=b'{"bytes":"'+b'ab'*600000+b'"}\n';v=self.indexed(raw)['bytes'];self.assertIsInstance(v,Hex)
  primitive('BYTES',v);self.assertEqual(digest(unhex(v)),sha(b'\xab'*600000));self.assertEqual(v,('ab'*600000))
  with self.assertRaises(ValidationError):primitive('ID',v)
 def test_caps_are_inability(self):
  for b in (b'"'+b'Z'*1048577+b'"\n',b'['*130+b'0'+b']'*130+b'\n'):
   with self.assertRaises(ValidationError) as cm:self.indexed(b)
   self.assertEqual(cm.exception.category,'INCOMPLETE-EVIDENCE-UNIVERSE')
 def test_exact_two_source_invocation_oracles(self):
  from v4_ingest.wire import decode_container
  for family in ('GAMMA','DELTA'):
   q,t=dataset(family);e=json.loads(bytes.fromhex(q['security_records_hex']));p=json.loads(decode_container(bytes.fromhex(q['outer_hex']))['PRIVACY']);arg=e['records']['ARGUMENT']['instances'][0]
   mm={k:bytes.fromhex(v) for k,v in q['materials'].items()};ss={k:bytes.fromhex(v) for k,v in q['source_objects'].items()};old=FiniteLabProvider(t,mm,ss)
   new=StreamingProvider(t,{k:self.store.write([v]) for k,v in mm.items()},{k:self.store.write([v]) for k,v in ss.items()},self.store)
   expected=old.invocation(arg,p['security_contract'],sha(wire(t['model'])));actual=new.invocation(arg,self.indexed(wire(p['security_contract'])),sha(wire(t['model'])))
   self.assertEqual(actual,expected);self.assertEqual(digest(actual),sha(expected))
 def test_collision_key_equivalence_oracle(self):
  values=[None,True,False,0,1,2,-1,'0','1','', 'a']
  for x in values:
   for y in values:self.assertEqual(x==y,StreamingProvider._collision_key(x)==StreamingProvider._collision_key(y))
 def test_dependency_closure_and_missing_transitive_material(self):
  q,t=dataset();mm={k:bytes.fromhex(v) for k,v in q['materials'].items()};ss={k:bytes.fromhex(v) for k,v in q['source_objects'].items()}
  leaf=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{'real':'dependency'},'dependencies':[]});middle=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{},'dependencies':[sha(leaf)]});root=wire({'format':'CP3-LAB-MATERIAL-V1','payload':{},'dependencies':[sha(middle)]})
  mm[sha(root)]=root;mm[sha(middle)]=middle;ref={'owner_source_id':t['source_id'],'source_sha256':t['source_sha256'],'source_anchor':'new','material_sha256':sha(root)};t['anchors']['new']=sha(root)
  p=StreamingProvider(t,{k:self.store.write([v]) for k,v in mm.items()},{k:self.store.write([v]) for k,v in ss.items()},self.store)
  with self.assertRaises(ValueError):p.invocation({'argument_id':'TEST-ARG','premise_ids':[],'ref':ref},{},'0'*64)
  p.materials[sha(leaf)]=self.store.write([leaf]);a=p.invocation({'argument_id':'TEST-ARG','premise_ids':[],'ref':ref},{},'0'*64);self.assertEqual(p.invocation_receipts[-1]['dependency_count'],4);self.assertTrue(len(a)>len(root))

class CollectorSemanticTests(unittest.TestCase):
 def case(self,mutate=None,**kwargs):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);p=Path(self.tmp.name);q,t=dataset(**kwargs)
  if mutate:mutate(q,t)
  m,tp=export(p/'input',q,t);create_key(p/'key');return p,m,tp
 def execute(self,p,m,t,**kw):return run(m,t,p/'journal',p/'key',**kw)
 def test_complete_both_families(self):
  for fam in ('GAMMA','DELTA'):
   p,m,t=self.case(name=fam);r=self.execute(p,m,t);self.assertFalse(r['failures'],r);self.assertEqual(len(r['semantic_acquisition']['invocations']),3);self.assertFalse(r['profile_admitted'])
 def test_missing_qualification_never_replaced_by_signature(self):
  p,m,t=self.case(lambda q,t:t['laboratory_assumptions'].pop('assessor-competence'));r=self.execute(p,m,t);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['bindings']['computed_budgets'])
 def test_missing_dependency(self):
  p,m,t=self.case(lambda q,t:q['materials'].pop(t['premises']['G-PREMISE']['material_sha256']));r=self.execute(p,m,t);self.assertIn('MISSING-EVIDENCE',r['failures'])
 def test_wrong_source_ownership(self):
  p,m,t=self.case(lambda q,t:t.update(source_id='WRONG'));r=self.execute(p,m,t);self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures'])
 def test_substituted_invocation_and_result(self):
  for field,value in [('exact_input_digest','0'*64),('validated_bound',[1,2])]:
   def mutation(q,t):
    e=json.loads(bytes.fromhex(q['security_records_hex']));e['records']['ASSESSMENT']['instances'][0][field]=value;q['security_records_hex']=wire(e).hex()
   p,m,t=self.case(mutation);r=self.execute(p,m,t);self.assertTrue(r['failures']);self.assertFalse(r.get('bindings',{}).get('computed_budgets'))
 def test_malformed_records_preserve_signature_failure(self):
  from tests.test_admission import bad_signature
  def mutation(q,t):bad_signature(q);q['security_records_hex']=b'{} '.hex()
  p,m,t=self.case(mutation);r=self.execute(p,m,t);self.assertIn('INVALID-EVIDENCE-AUTHENTICATION',r['failures']);self.assertEqual(r['earliest_failure'],'INVALID-PROFILE-SCHEMA')
 def test_repeated_pause_resume_exact_prefix_and_terminal_revalidation(self):
  p,m,t=self.case();r=self.execute(p,m,t,new_bytes=1);self.assertEqual(r['result'],'PAUSED')
  r=self.execute(p,m,t,resume=True,new_bytes=3);self.assertEqual(r['result'],'PAUSED')
  r=self.execute(p,m,t,resume=True);self.assertFalse(r['failures'],r);r2=self.execute(p,m,t,resume=True);self.assertEqual(r['semantic_acquisition']['invocations'],r2['semantic_acquisition']['invocations']);self.assertEqual(r['result'],r2['result'])
 def test_changed_input_after_pause_and_corrupt_receipt(self):
  p,m,t=self.case();self.execute(p,m,t,new_bytes=2);b=p/'input/outer_hex.bin';x=bytearray(b.read_bytes());x[0]^=1;b.write_bytes(x)
  r=self.execute(p,m,t,resume=True);self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted'])
  (p/'journal').write_bytes(b'{}')
  with self.assertRaises((ValueError,KeyError)):self.execute(p,m,t,resume=True)
 def test_literal_amendment_stays_closed(self):
  from fixtures.field_class import literal
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);m,t=export(p/'input',*literal('GAMMA'));create_key(p/'key');r=self.execute(p,m,t);self.assertFalse(r['failures'],r)


class RecoveryParserTests(unittest.TestCase):
 def test_interruption_inside_json_rebuilds_from_bytes(self):
  from semantic_stream.storage import Cursor
  from link_recovery.cli import PauseRequested
  raw=wire({'rows':[{'id':i,'bytes':'aabb'*30} for i in range(1500)]})
  for stop in (1,9,101,2049):
   with tempfile.TemporaryDirectory() as directory:
    store=Store(directory);original=Cursor.take;calls=[0]
    def interrupt(cursor,n):
     calls[0]+=1
     if calls[0]==stop:raise PauseRequested()
     return original(cursor,n)
    with patch.object(Cursor,'take',interrupt),self.assertRaises(PauseRequested):store.parse(store.write([raw]))
    store.close();self.assertEqual(list(Path(directory).iterdir()),[])
    fresh=Store(directory)
    try:
     x=fresh.parse(fresh.write([raw]));self.assertEqual(x,json.loads(raw));self.assertEqual(digest(canonical(x)),sha(raw))
    finally:fresh.close()
 def test_integrated_interrupted_parser_never_imports_partial_success(self):
  from semantic_stream.storage import Document
  from link_recovery.cli import PauseRequested
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory);m,t=export(p/'input',*dataset());create_key(p/'key');original=Document.node;calls=[0]
   def interrupt(doc,depth):
    calls[0]+=1
    # Trusted input is parsed before journals; interrupt after semantic acquisition.
    if (p/'journal').exists() and calls[0]>100:raise PauseRequested()
    return original(doc,depth)
   with patch.object(Document,'node',interrupt),self.assertRaises(PauseRequested):run(m,t,p/'journal',p/'key')
   self.assertTrue((p/'journal').exists());r=run(m,t,p/'journal',p/'key',resume=True);self.assertFalse(r['failures'],r);self.assertFalse(r['profile_admitted'])
 def test_large_hex_changed_nibble_odd_and_wrong_case(self):
  for suffix in (b'A',b'g',b'0'):
   store=Store()
   try:
    with self.assertRaises(ValidationError):store.parse(store.write([b'"'+b'ab'*600000+suffix+b'"\n']))
   finally:store.close()
