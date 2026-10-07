import copy,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from fixtures.projections import make_data,export
from fixtures.construct import wire,sha
from fixtures.integrated import export as carrier
from semantic_stream.storage import Store,ACTIVE
from semantic_stream.provider import StreamingProvider
from occurrence_values.projection import Projections,FRAMES,law,FORMAT
from occurrence_values.codec import validate
from v4_ingest.records import SPEC,IDENTITY,ValidationError
from recovery_schedule.runner import run
from recovery_schedule.state import Scheduler
from link_recovery.cli import create_key,PauseRequested

class ProjectionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name);self.seq=0
 def harness(self,phase='E',change=None,raw_override=None,read_null=True):
  q,t,o=make_data(phase,read_null=read_null);sec=json.loads(bytes.fromhex(q['security_records_hex']));binding=o['binding']
  if change:change(sec)
  raw=wire(sec) if raw_override is None else raw_override;q['security_records_hex']=raw.hex()
  s=Store(self.p);self.addCleanup(s.close);token=ACTIVE.set(s);self.addCleanup(ACTIVE.reset,token)
  def material(anchor,v):
   b=wire({'format':'CP3-LAB-MATERIAL-V1','payload':v,'dependencies':[]});h=sha(b);q['materials'][h]=b.hex();t['anchors'][anchor]=h
   return dict(owner_source_id=t['source_id'],source_sha256=t['source_sha256'],source_anchor=anchor,material_sha256=h)
  ref=material('unit-containing-record',{'format':'CP4O-S90-CONTAINER-1','binding':binding,'encoded_hex':raw.hex(),'rules_ref':t['projection_rules_ref']})
  provider=StreamingProvider(t,{k:s.write([bytes.fromhex(v)]) for k,v in q['materials'].items()},{k:s.write([bytes.fromhex(v)]) for k,v in q['source_objects'].items()},s)
  reg=json.loads((Path(__file__).resolve().parents[1]/'rebinding/field-class-register.json').read_bytes())
  model=SimpleNamespace(value={'surfaces':[{'node_id':x} for x in reg]})
  adapter=SimpleNamespace(store=s,octets=lambda n:s.write([raw]))
  engine=Projections(adapter,provider,t,binding,model)
  return engine,ref,sec,binding,t,provider
 def project(self,h,surface,record=None,occurrence=None):
  e,ref,sec,binding,t,p=h;schema,field,kind=law(surface)
  record=record if record is not None else 'CP2-DIRECTORY-'+schema
  tok={'id':'UNIT','surface':surface,'context':'SYMBOLIC-U-ONE','record':occurrence or record}
  rid=None if record.startswith('CP2-DIRECTORY-') else record
  obj={'format':FORMAT,'binding':binding,'token_id':'UNIT','surface_id':surface,'context':tok['context'],'record':tok['record'],'codec':'S90-JSON-LF','type_id':kind,'container_ref':ref,'record_id':rid}
  return e.project(obj,{'codec':'S90-JSON-LF','type_id':kind},tok).small(4194304)
 def test_exhaustive_all_s90_fields_records_and_frames_against_python_oracle(self):
  h=self.harness();sec=h[2];count=0
  for schema,d in sec['records'].items():
   for rec in d['instances']:
    rid=rec[IDENTITY[schema]]
    self.assertEqual(self.project(h,'SECURITY:'+schema+'.$record',rid),wire(rec));count+=1
    for field,value in rec.items():
     self.assertEqual(self.project(h,'SECURITY:'+schema+'.'+field,rid),wire(value));count+=1
     self.assertEqual(self.project(h,'SECURITY-FRAME:'+schema+'.present:'+field,rid),wire(value is not None));count+=1
   for field,v in [('status',d['status']),('justification',d['justification']),('instance_count',len(d['instances'])),('record_directory',[r[IDENTITY[schema]] for r in d['instances']])]:
    self.assertEqual(self.project(h,'SECURITY-FRAME:'+schema+'.'+field),wire(v));count+=1
  for f in ('format','profile_digest','phase','schema_directory'):
   self.assertEqual(self.project(h,'SECURITY-FRAME:ROOT.'+f),wire(sorted(sec['records']) if f=='schema_directory' else sec[f]));count+=1
  self.assertEqual(count,sum(1+2*len(r) for d in sec['records'].values() for r in d['instances'])+4*len(sec['records'])+4)
 def test_exhaustive_source_reference_subfields_and_list_occurrences(self):
  h=self.harness();count=0
  for schema,d in h[2]['records'].items():
   for rec in d['instances']:
    rid=rec[IDENTITY[schema]]
    for f,kind in SPEC[schema].items():
     if kind not in ('SOURCE-REF','LIST-SOURCE-REF') or rec[f] is None:continue
     for i,ref in enumerate(rec[f] if kind.startswith('LIST') else [rec[f]],1):
      for part,v in ref.items():
       self.assertEqual(self.project(h,'CP2-REF-PARSER:'+schema+'.'+f+'.'+part,rid,rid+':REF:'+f+':'+f'{i:06}'),wire(v));count+=1
  self.assertGreater(count,200)
 def test_null_is_record_interpretation_not_primitive_weakening(self):
  h=self.harness();self.assertEqual(self.project(h,'SECURITY:ASSESSOR-EVENT.input_bytes','G-EVENT-COLLISION-0'),b'null\n')
  s=h[0].store
  with self.assertRaises(ValueError):validate(s.write([b'null\n']),'S90-JSON-LF','BYTES',[],[])
  self.assertNotEqual(self.project(h,'SECURITY:ASSESSOR-EVENT.input_bytes','G-EVENT-COLLISION-1'),b'null\n')
  present=self.harness(read_null=False)
  self.assertEqual(self.project(present,'SECURITY:ASSESSOR-EVENT.input_bytes','G-EVENT-COLLISION-0'),b'""\n')
  self.assertEqual(self.project(present,'SECURITY-FRAME:ASSESSOR-EVENT.present:input_bytes','G-EVENT-COLLISION-0'),b'true\n')
 def test_invalid_unavailable_assessment_null_and_union_exact_null(self):
  for status in ('INVALID','UNAVAILABLE'):
   def mutate(sec):
    r=sec['records']['ASSESSMENT']['instances'][0];r.update(complete_result=status,validated_bound=None)
   h=self.harness(change=mutate);r=h[2]['records']['ASSESSMENT']['instances'][0]
   self.assertEqual(self.project(h,'SECURITY:ASSESSMENT.validated_bound',r['assessment_id']),b'null\n')
  h=self.harness()
  for schema,field,cond in [('COMPOSITION','theorem_ref',lambda r:True),('OBLIGATION','experiment_id',lambda r:r['kind']=='EXACT')]:
   r=next(r for r in h[2]['records'][schema]['instances'] if cond(r));self.assertEqual(self.project(h,'SECURITY:'+schema+'.'+field,r[IDENTITY[schema]]),b'null\n')
 def test_missing_field_not_schema_null_and_duplicate_record(self):
  for change in (lambda s:s['records']['ASSESSOR-EVENT']['instances'][0].pop('input_bytes'),lambda s:s['records']['ASSESSOR-EVENT']['instances'].append(copy.deepcopy(s['records']['ASSESSOR-EVENT']['instances'][0]))):
   h=self.harness(change=change)
   with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
 def test_directory_unavailable_inapplicable_not_missing_field_fallback(self):
  for status in ('UNAVAILABLE','INAPPLICABLE'):
   def mutate(s):
    d=s['records']['ASSESSOR-EVENT'];d['justification']=d['instances'][0]['owner'] if status=='INAPPLICABLE' else None;d.update(status=status,instances=[])
   h=self.harness(change=mutate)
   self.assertEqual(self.project(h,'SECURITY-FRAME:ASSESSOR-EVENT.status'),wire(status));self.assertEqual(self.project(h,'SECURITY-FRAME:ASSESSOR-EVENT.instance_count'),b'0\n')
   with self.assertRaises(ValueError):self.project(h,'SECURITY:ASSESSOR-EVENT.input_bytes','G-EVENT-COLLISION-0')
 def test_trace_null_correspondence_and_missing_qualification(self):
  for mode in ('trace','qualification','rules'):
   h=self.harness();e,ref,sec,b,t,p=h
   if mode=='trace':t['trace_refs'].pop('G-ASSESS-COLLISION')
   elif mode=='qualification':t['laboratory_assumptions'].pop('assessor-competence')
   else:t.pop('projection_rules_ref')
   with self.assertRaises((ValueError,KeyError)):self.project(h,'SECURITY:ASSESSOR-EVENT.input_bytes','G-EVENT-COLLISION-0')
 def test_lazy_eviction_and_mutated_snapshot(self):
  h=self.harness();e=h[0];self.project(h,'SECURITY-FRAME:ROOT.phase')
  for i in range(10):e.store.parse(e.store.write([wire({'i':i})]))
  self.assertEqual(self.project(h,'SECURITY-FRAME:ROOT.phase'),b'"E"\n')
  entry=e.objects[h[1]['material_sha256']];Path(entry['path']).write_bytes(b'{}\n')
  with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
 def test_exact_record_and_reference_ordinal_binding(self):
  h=self.harness()
  for surface,rid,occ in [('SECURITY:ASSESSOR-EVENT.input_bytes','ABSENT',None),('CP2-REF-PARSER:ASSESSOR-EVENT.owner.source_anchor','G-EVENT-COLLISION-0','G-EVENT-COLLISION-0:REF:owner:000002')]:
   with self.assertRaises(ValueError):self.project(h,surface,rid,occ)
 def case(self,phase='E',mutate=None):
  q,t,o=make_data(phase)
  if mutate:mutate(q,t)
  self.seq+=1;p=self.p/str(self.seq);m,tr=carrier(p,q,t);create_key(p/'key');return m,tr,o,p
 def go(self,c,**kw):m,t,o,p=c;return run(m,t,p/'job',p/'key',**kw)
 def oracle(self,r,o):
  self.assertFalse(r['failures'],r['reasons']);self.assertFalse(r['profile_admitted']);self.assertFalse(r['actual_qualification_established']);self.assertEqual(r['occurrence_acquisition']['tokens'],32)
  for scope in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'):
   actual=r['bindings']['scope_validation']['scopes'][scope]['link_validation'];expected=o[scope]
   for a,b in [('complete_stream_sha256','links_sha256'),('structural_rows','structural'),('potential_rows','potential')]:self.assertEqual(actual[a],expected[b])
   self.assertTrue(r['bindings']['bundle_authentication'][scope]['signature_valid'])
 def test_integrated_all_phases_pause_repeat_resume_and_oracle(self):
  for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
   c=self.case(phase);self.assertEqual(self.go(c,new_bytes=1)['result'],'PAUSED');self.assertEqual(self.go(c,resume=True,new_bytes=31)['result'],'PAUSED');self.oracle(self.go(c,resume=True),c[2]);self.oracle(self.go(c,resume=True),c[2])
 def test_integrated_hash_collisions(self):
  c=self.case()
  with patch('occurrence_values.index.bucket',return_value='same'):self.oracle(self.go(c),c[2])
 def test_interrupted_projection_and_equality_recovery(self):
  c=self.case();original=Projections.project;count=[0]
  def cut(*a,**kw):
   count[0]+=1
   if count[0]==8:raise PauseRequested()
   return original(*a,**kw)
  with patch.object(Projections,'project',cut),self.assertRaises(PauseRequested):self.go(c)
  self.oracle(self.go(c,resume=True),c[2])
 def test_late_interruption_reuses_verified_indexes(self):
  c=self.case();save=Scheduler.save
  def stop(s,label,*a,**kw):
   if label=='ordered-ledger':raise PauseRequested()
   return save(s,label,*a,**kw)
  with patch.object(Scheduler,'save',stop),self.assertRaises(PauseRequested):self.go(c)
  self.oracle(self.go(c,resume=True),c[2])
 def test_integrated_mutation_and_journal_corruption(self):
  c=self.case();self.oracle(self.go(c),c[2]);p=c[3]/'security_records_hex.bin';raw=p.read_bytes();p.write_bytes(raw[:-1]+b' ');r=self.go(c,resume=True);self.assertTrue(r['failures']);self.assertFalse(r['profile_admitted'])
  d=self.case();self.go(d);(d[3]/'job').write_bytes(b'{}\n')
  with self.assertRaises(ValueError):self.go(d,resume=True)
 def test_generated_events_use_their_separate_containing_adapter(self):
  from occurrence_values.generated import law as generated_law
  for surface in ('CP2-RECORD-PARSER:input_record','CP2-REFERENCE-MATERIAL:lookup_status'):
   with self.assertRaises(ValidationError):law(surface)
   self.assertIsNotNone(generated_law(surface))


 def test_projection_binding_dimensions_reject_exactly(self):
  h=self.harness();e,ref,sec,binding,t,p=h;surface='SECURITY:ASSESSOR-EVENT.input_bytes';rid='G-EVENT-COLLISION-0'
  tok={'id':'UNIT','surface':surface,'context':'SYMBOLIC-U-ONE','record':rid}
  original={'format':FORMAT,'binding':binding,'token_id':'UNIT','surface_id':surface,'context':tok['context'],'record':rid,'codec':'S90-JSON-LF','type_id':'BYTES','container_ref':ref,'record_id':rid}
  for field in ('token_id','surface_id','context','record','record_id','type_id'):
   obj=copy.deepcopy(original);obj[field]='WRONG'
   with self.assertRaises(ValueError):e.project(obj,{'codec':'S90-JSON-LF','type_id':'BYTES'},tok)
  for field in binding:
   obj=copy.deepcopy(original);obj['binding'][field]='WRONG'
   with self.assertRaises(ValueError):e.project(obj,{'codec':'S90-JSON-LF','type_id':'BYTES'},tok)
  obj=copy.deepcopy(original);obj['container_ref']['owner_source_id']='WRONG'
  with self.assertRaises(ValueError):e.project(obj,{'codec':'S90-JSON-LF','type_id':'BYTES'},tok)
 def test_cross_record_container_and_malformed_bytes_reject(self):
  for raw in (b'{} \n',b'{"a":1,"a":2}\n'):
   h=self.harness(raw_override=raw)
   with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
  h=self.harness();h[5].materials.pop(h[1]['material_sha256'])
  with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
  h=self.harness();h[0].a.octets=lambda n:h[0].store.write([wire({'other':True})])
  with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
 def test_integrated_duplicate_assignment_and_absent_qualification(self):
  def missing(q,t):t['laboratory_assumptions'].pop('source-producer-correspondence')
  r=self.go(self.case(mutate=missing));self.assertIn('INVALID-EVIDENCE-AUTHORITY',r['failures']);self.assertFalse(r['bindings']['computed_budgets'])
  def duplicate(q,t):
   ref=t['occurrence_source_ref'];obj=json.loads(bytes.fromhex(q['materials'][ref['material_sha256']]))
   obj['payload']['assignments'][1]=copy.deepcopy(obj['payload']['assignments'][0]);raw=wire(obj);h=sha(raw);q['materials'][h]=raw.hex();ref['material_sha256']=h;t['anchors'][ref['source_anchor']]=h
  r=self.go(self.case(mutate=duplicate));self.assertIn('INCOMPLETE-EVIDENCE-UNIVERSE',r['failures'])

 def test_standalone_equal_bytes_cannot_bypass_containing_record(self):
  from fixtures.projection_mutations import standalone
  q,t,o=make_data();standalone(q,t,o);p=self.p/'bypass';m,tr=carrier(p,q,t);create_key(p/'key');r=run(m,tr,p/'job',p/'key')
  self.assertIn('MISSING-EVIDENCE',r['failures']);self.assertIsNone(r['occurrence_acquisition']);self.assertFalse(r['bindings']['computed_budgets']);self.assertFalse(r['profile_admitted'])
 def test_nonnull_theorem_reference_and_false_null_bound(self):
  def modify(s):
   r=s['records']['COMPOSITION']['instances'][0];r['method']='SOURCE-QUALIFIED-THEOREM';r['theorem_ref']=s['records']['ASSESSOR-EVENT']['instances'][0]['owner']
  h=self.harness(change=modify);r=h[2]['records']['COMPOSITION']['instances'][0];rid=r['composition_id']
  self.assertEqual(self.project(h,'SECURITY:COMPOSITION.theorem_ref',rid),wire(r['theorem_ref']))
  for k,v in r['theorem_ref'].items():self.assertEqual(self.project(h,'CP2-REF-PARSER:COMPOSITION.theorem_ref.'+k,rid,rid+':REF:theorem_ref:000001'),wire(v))
  def invalid(s):s['records']['ASSESSMENT']['instances'][0]['validated_bound']=None
  h=self.harness(change=invalid)
  with self.assertRaises(ValueError):self.project(h,'SECURITY-FRAME:ROOT.phase')
