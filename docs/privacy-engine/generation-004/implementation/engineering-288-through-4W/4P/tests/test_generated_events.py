import copy,json,tempfile,unittest,sqlite3
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from fixtures.generated_events import make_data,export,PARSER,MATERIAL
from fixtures.construct import wire,sha
from fixtures.integrated import export as carrier
from semantic_stream.storage import Store,ACTIVE
from semantic_stream.provider import StreamingProvider
from occurrence_values.projection import Projections
from occurrence_values.generated import Generated,selector,law,FORMAT
from v4_ingest.records import ValidationError
from recovery_schedule.runner import run
from link_recovery.cli import create_key,PauseRequested
from recovery_schedule.state import Scheduler

class GeneratedTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=make_data()
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.path=Path(self.tmp.name);self.seq=0
 def harness(self):
  q,t,o=self.base;t=copy.deepcopy(t);s=Store(self.path);self.addCleanup(s.close);tok=ACTIVE.set(s);self.addCleanup(ACTIVE.reset,tok)
  mats={h:s.write([bytes.fromhex(raw)]) for h,raw in q['materials'].items()};sources={h:s.write([bytes.fromhex(raw)]) for h,raw in q['source_objects'].items()}
  provider=StreamingProvider(t,mats,sources,s);raw=s.write([bytes.fromhex(q['security_records_hex'])]);adapter=SimpleNamespace(store=s,octets=lambda n:raw)
  model=SimpleNamespace(value=t['model'],tokens=t['model']['tokens']);p=Projections(adapter,provider,t,o['binding'],model);g=Generated(p)
  def put(anchor,v,deps=None):
   b=wire({'format':'CP3-LAB-MATERIAL-V1','payload':v,'dependencies':deps or []});h=sha(b);mats[h]=s.write([b]);t['anchors'][anchor]=h
   return dict(owner_source_id=t['source_id'],source_sha256=t['source_sha256'],source_anchor=anchor,material_sha256=h)
  return g,t,provider,put
 def event(self,h,kind='PARSER',schema='OBSERVER',context='SYMBOLIC-U-ONE'):
  g,t,p,put=h;d=p.payload(t['generated_source_ref'])
  r=next(r for r in d['events'] if '|'+kind+'|'+schema+':' in r['key'] and r['key'].startswith(context))
  return r['key'],json.loads(p.raw(r['event_ref']).small(16777216))['payload']
 def check(self,h,key,obj):return h[0].validate(key,h[3]('unit-'+str(h[0].event_count)+'-'+sha(wire(obj))[:12],obj))
 def test_all_13_forms_all_parser_branches_against_independent_bytes(self):
  h=self.harness();g,t,p,put=h;g.prepare();q,_,o=self.base;seen=set();statuses=set()
  for tok in t['model']['tokens']:
   if not tok['surface'].startswith('CP2-'):continue
   obj=json.loads(bytes.fromhex(q['materials'][t['occurrence_bindings'][tok['id']]['material_sha256']]))['payload'];kind,field,typ=law(tok['surface'])
   self.assertEqual(g.project(obj,dict(codec='S90-JSON-LF',type_id=typ),tok).small(16777216),bytes.fromhex(o['values_hex'][tok['id']]))
   seen.add(tok['surface'])
   if field=='result_kind':statuses.add(json.loads(bytes.fromhex(o['values_hex'][tok['id']])))
  self.assertEqual(len(seen),13);self.assertEqual(statuses,{'VALID-LOCAL','INVALID-LOCAL','UNAVAILABLE','INAPPLICABLE'});self.assertEqual(g.event_count,12)
 def test_dishonest_branches_and_outputs(self):
  h=self.harness();key,base=self.event(h)
  for mutate in (lambda o:o['events'][0]['fields'].__setitem__('result_kind','INVALID-LOCAL'),lambda o:o['events'][1]['fields'].__setitem__('result_kind','VALID-LOCAL'),lambda o:o['events'][0]['fields'].__setitem__('output_record','00'),lambda o:o['events'][1]['fields'].__setitem__('output_record',''),lambda o:o['events'][0]['fields'].__setitem__('result_kind','PASS')):
   obj=copy.deepcopy(base);mutate(obj)
   with self.assertRaises(ValueError):self.check(h,key,obj)
 def test_all_binding_parent_and_ordinal_joins(self):
  h=self.harness();key,base=self.event(h)
  for k in base['binding']:
   obj=copy.deepcopy(base);obj['binding'][k]='WRONG'
   with self.assertRaises(ValueError):self.check(h,key,obj)
  for k,v in [('context','SYMBOLIC-U-TWO'),('record_id','WRONG'),('invocation_id','WRONG')]:
   obj=copy.deepcopy(base);obj[k]=v
   with self.assertRaises(ValueError):self.check(h,key,obj)
  for k,v in [('phase','PRE-COMMITMENT'),('attempt_ordinal',True),('attempt_ordinal',2),('record_id','WRONG'),('parent_invocation','WRONG'),('owner_reference',base['rules_ref']),('grammar_reference',base['container_ref'])]:
   obj=copy.deepcopy(base);obj['events'][0]['fields'][k]=v
   with self.assertRaises(ValueError):self.check(h,key,obj)
 def test_missing_extra_conflicting_attempts_and_guards(self):
  h=self.harness();key,base=self.event(h)
  for events in (base['events'][:1],base['events']*2,[base['events'][0]]*2):
   obj=copy.deepcopy(base);obj['events']=events
   with self.assertRaises(ValueError):self.check(h,key,obj)
  key,base=self.event(h,schema='ALGORITHM')
  for f in ('input_record','output_record'):
   obj=copy.deepcopy(base);obj['events'][0]['fields'][f]=''
   with self.assertRaises(ValueError):self.check(h,key,obj)
  obj=copy.deepcopy(base);obj['events'][0]['justification_ref']=None
  with self.assertRaises(ValueError):self.check(h,key,obj)
  obj=copy.deepcopy(base);obj['events'][1]['justification_ref']=obj['events'][0]['justification_ref']
  with self.assertRaises(ValueError):self.check(h,key,obj)
 def test_missing_duplicate_extra_directory_and_qualification(self):
  for mode in ('missing','duplicate','extra','role','rules','partial-model'):
   h=self.harness();g,t,p,put=h;d=json.loads(p.raw(t['generated_source_ref']).small(16777216))['payload']
   if mode=='missing':d['events'].pop()
   if mode=='duplicate':d['events'].append(d['events'][0])
   if mode=='extra':d['events'].append(dict(key='ZZZ',event_ref=d['events'][0]['event_ref']))
   if mode=='role':t['laboratory_assumptions'].pop('observer-completeness')
   if mode=='rules':t['generated_rules_ref']=t['projection_rules_ref']
   if mode=='partial-model':g.p.model.tokens=g.p.model.tokens[1:]
   t['generated_source_ref']=put('changed-directory',d)
   with self.assertRaises(ValueError):g.prepare()
 def test_material_all_statuses_exact_bytes_and_dependency_closure(self):
  h=self.harness();key,base=self.event(h,'MATERIAL');own=base['events'][0]['fields']['owning_reference'];provider=h[2];raw=provider.materials[own['material_sha256']]
  self.check(h,key,base)
  # Explicit absence is observable acquisition evidence, not source qualification.
  provider.materials.pop(own['material_sha256']);obj=copy.deepcopy(base);obj['events'][0]['fields'].update(lookup_status='UNAVAILABLE',exact_bytes=None);self.check(h,key,obj)
  for v in ('', '00'):
   obj['events'][0]['fields']['exact_bytes']=v
   with self.assertRaises(ValueError):self.check(h,key,obj)
  bad=b'NOT THE REFERENCED BYTES';provider.materials[own['material_sha256']]=h[0].store.write([bad]);obj=copy.deepcopy(base);obj['events'][0]['fields'].update(lookup_status='INVALID',exact_bytes=bad.hex());self.check(h,key,obj)
  obj['events'][0]['fields']['lookup_status']='PRESENT'
  with self.assertRaises(ValueError):self.check(h,key,obj)
  provider.materials[own['material_sha256']]=raw
  obj=copy.deepcopy(base);obj['events'][0]['fields']['lookup_status']='INAPPLICABLE'
  with self.assertRaises(ValueError):self.check(h,key,obj)
 def test_null_parent_no_reference_children_and_list_multiplicity(self):
  h=self.harness();g,t,p,put=h;key,base=self.event(h,'MATERIAL');sec=json.loads(g.p.a.octets('security_records_hex').small(16777216));ref=base['events'][0]['fields']['owning_reference']
  # Unit snapshot oracle changes source bytes and authenticated comparison together.
  def container(sec):
   raw=wire(sec);g.p.a.octets=lambda n:g.store.write([raw]);return put('unit-container-'+sha(raw)[:8],dict(format='CP4O-S90-CONTAINER-1',binding=g.binding,encoded_hex=raw.hex(),rules_ref=t['projection_rules_ref']))
  sec['records']['OBSERVER']['instances'][0]['member_role_refs']=[ref,ref];obj=copy.deepcopy(base);obj['container_ref']=container(sec);obj['events'][0]['ordinal']=2;key2=key[:-6]+'000002';self.check(h,key2,obj)
  obj['events'][0]['ordinal']=3
  with self.assertRaises(ValueError):self.check(h,key[:-6]+'000003',obj)
  sec['records']['COMPOSITION']['instances'][0]['theorem_ref']=None;rid=sec['records']['COMPOSITION']['instances'][0]['composition_id'];obj=copy.deepcopy(base);obj.update(schema_id='COMPOSITION',record_id=rid,container_ref=container(sec));obj['events'][0]['field']='theorem_ref';obj['events'][0]['fields']['owning_reference']=None
  with self.assertRaises(ValueError):self.check(h,'SYMBOLIC-U-ONE|MATERIAL|COMPOSITION:'+rid+':REF:theorem_ref:000001',obj)
 def test_mutation_eviction_cross_context_replay(self):
  h=self.harness();g,t,p,put=h;key,obj=self.event(h);ref=put('replay-event',obj);g.validate(key,ref)
  for i in range(20):g.store.parse(g.store.write([wire({'i':i})]))
  self.assertEqual(g.validate(key,ref)['record_id'],'G-COALITION')
  with self.assertRaises(ValueError):g.validate(key.replace('U-ONE','U-TWO'),ref)
  p.materials[ref['material_sha256']].path.write_bytes(b'{}\n')
  with self.assertRaises(ValueError):g.validate(key,ref)
 def case(self,phase='E',mutate=None):
  self.seq+=1;p=self.path/str(self.seq);q,t,o=make_data(phase)
  if mutate:mutate(q,t,o)
  m,tr=carrier(p,q,t);create_key(p/'key');return m,tr,o,p
 def go(self,c,**kw):m,t,o,p=c;return run(m,t,p/'job',p/'key',**kw)
 def oracle(self,r,o,p=None):
  self.assertFalse(r['failures'],r['reasons']);self.assertFalse(r['actual_qualification_established']);self.assertFalse(r['profile_admitted']);self.assertEqual(r['occurrence_acquisition']['generated_projections'],92)
  for scope in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'):
   a=r['bindings']['scope_validation']['scopes'][scope]['link_validation'];e=o[scope]
   for k,v in [('complete_stream_sha256','links_sha256'),('structural_rows','structural'),('potential_rows','potential')]:self.assertEqual(a[k],e[v])
   self.assertTrue(r['bindings']['bundle_authentication'][scope]['signature_valid'])
  if p:
   root=Path(str(p/'job')+'.stages');db=sqlite3.connect(root/'occurrence-equality.sqlite')
   try:
    for tok,v in o['values_hex'].items():
     name=db.execute('select file from assignments join groups using(g) where token=?',(tok,)).fetchone()[0];self.assertEqual((root/name).read_bytes(),bytes.fromhex(v))
   finally:db.close()
 def test_integrated_all_phases_oracle_pause_resume_and_terminal(self):
  for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
   c=self.case(phase);self.assertEqual(self.go(c,new_bytes=1)['result'],'PAUSED');self.assertEqual(self.go(c,resume=True,new_bytes=31)['result'],'PAUSED');self.oracle(self.go(c,resume=True),c[2],c[3]);self.oracle(self.go(c,resume=True),c[2])
 def test_integrated_event_interruption_and_index_collision(self):
  c=self.case();original=Generated.project;n=[0]
  def stop(*a,**kw):
   n[0]+=1
   if n[0]==11:raise PauseRequested()
   return original(*a,**kw)
  with patch.object(Generated,'project',stop),self.assertRaises(PauseRequested):self.go(c)
  with patch('occurrence_values.index.bucket',return_value='FORCED-COLLISION'):self.oracle(self.go(c,resume=True),c[2],c[3])
 def test_integrated_ledger_interruption_and_mutation(self):
  c=self.case();save=Scheduler.save
  def stop(s,label,*a,**kw):
   if label=='ordered-ledger':raise PauseRequested()
   return save(s,label,*a,**kw)
  with patch.object(Scheduler,'save',stop),self.assertRaises(PauseRequested):self.go(c)
  self.oracle(self.go(c,resume=True),c[2],c[3]);f=c[3]/'security_records_hex.bin';b=f.read_bytes();f.write_bytes(b[:-1]+b' ');self.assertTrue(self.go(c,resume=True)['failures'])
 def test_integrated_standalone_bypass_rejected(self):
  def change(q,t,o):
   from fixtures.projection_mutations import standalone
   standalone(q,t,o)
  r=self.go(self.case(mutate=change));self.assertTrue(r['failures']);self.assertIsNone(r['occurrence_acquisition']);self.assertFalse(r['profile_admitted'])
 def test_integrated_missing_rules_and_corrupt_journal(self):
  r=self.go(self.case(mutate=lambda q,t,o:t.pop('generated_rules_ref')));self.assertIn('MISSING-EVIDENCE',r['failures'])
  c=self.case();self.go(c,new_bytes=1);(c[3]/'job').write_bytes(b'{}\n')
  with self.assertRaises(ValueError):self.go(c,resume=True)
 def test_selected_contract_and_13_exact_domains(self):
  c=json.loads((Path(__file__).resolve().parents[1]/'rebinding/selected-contract.json').read_bytes());self.assertEqual(c['parser']['event_fields'],list(PARSER));self.assertEqual(c['material_acquisition']['fields'],list(MATERIAL))
  for s in ['CP2-RECORD-PARSER:nope','CP2-REFERENCE-MATERIAL:status']:
   with self.assertRaises(ValueError):law(s)
 def test_ledger_lazy_source_readonly_no_deepcopy(self):
  # Reproduces pre-4P deepcopy failure with the first >=64 KiB lazy ledger array.
  from ledger_kernel.construct import from_source
  h=self.harness();g,t,p,put=h;source=p.payload(t['ledger_source_ref']);before=sha(g.p.a.octets('security_records_hex').small(16777216))
  from admission_kernel.model import Model
  # Integrated oracle above exercises the same real source/model path.
  self.assertGreater(len(wire(self.base[1]['ledger'])),65536)
  with self.assertRaises(TypeError):copy.deepcopy(source['obligations'])
  model=Model(t['model']);security=json.loads(g.p.a.octets('security_records_hex').small(16777216));result=from_source(source,model,security['records']['POLICY']['instances'][0])
  self.assertEqual(result['obligations'],source['obligations']);self.assertEqual(before,sha(g.p.a.octets('security_records_hex').small(16777216)))
 def test_malformed_material_envelope_and_missing_dependencies(self):
  for bad,valid_status in [(b'{"unrecognized":true}\n','INVALID'),(wire({'format':'CP3-LAB-MATERIAL-V1','payload':0,'dependencies':['0'*64]}),None)]:
   h=self.harness();g,t,p,put=h;key,obj=self.event(h,'MATERIAL');old=obj['events'][0]['fields']['owning_reference'];hash_=sha(bad);ref=dict(old,source_anchor='bad-lookup',material_sha256=hash_);t['anchors']['bad-lookup']=hash_;p.materials[hash_]=g.store.write([bad])
   sec=json.loads(g.p.a.octets('security_records_hex').small(16777216));sec['records']['OBSERVER']['instances'][0]['member_role_refs']=[ref];raw=wire(sec);g.p.a.octets=lambda n:g.store.write([raw]);obj['container_ref']=put('unit-material-container',dict(format='CP4O-S90-CONTAINER-1',binding=g.binding,encoded_hex=raw.hex(),rules_ref=t['projection_rules_ref']));obj['events'][0]['fields'].update(owning_reference=ref,exact_bytes=bad.hex(),lookup_status=valid_status or 'PRESENT')
   if valid_status:self.check(h,key,obj)
   else:
    with self.assertRaises(ValueError):self.check(h,key,obj)
 def test_unavailable_parent_record_guarded_events_not_fabricated_values(self):
  h=self.harness();g,t,p,put=h;key,obj=self.event(h,schema='ALGORITHM');sec=json.loads(g.p.a.octets('security_records_hex').small(16777216));sec['records']['ALGORITHM'].update(status='UNAVAILABLE',instances=[]);raw=wire(sec);g.p.a.octets=lambda n:g.store.write([raw]);ref=put('absent-parent-container',dict(format='CP4O-S90-CONTAINER-1',binding=g.binding,encoded_hex=raw.hex(),rules_ref=t['projection_rules_ref']));obj['container_ref']=ref
  for event in obj['events']:event['fields']['owner_reference']=ref
  self.check(h,key,obj)
 def test_projection_carrier_exact_join_and_noncanonical_input(self):
  h=self.harness();g,t,p,put=h;g.prepare();tok=t['model']['tokens'][0];q=self.base[0];obj=json.loads(bytes.fromhex(q['materials'][t['occurrence_bindings'][tok['id']]['material_sha256']]))['payload'];row=dict(codec=obj['codec'],type_id=obj['type_id'])
  for k in ('token_id','surface_id','context','record','codec','type_id'):
   v=copy.deepcopy(obj);v[k]='WRONG'
   with self.assertRaises(ValueError):g.project(v,row,tok)
  v=copy.deepcopy(obj);v['event_ref']=t['projection_rules_ref']
  with self.assertRaises(ValueError):g.project(v,row,tok)
  key,event=self.event(h);event['events'][0]['fields']['input_record']=b'{"x": 0}\n'.hex()
  with self.assertRaises(ValueError):self.check(h,key,event)
 def test_arbitrary_chunk_boundaries_keep_event_bytes(self):
  for chunk in (1,7,31):
   h=self.harness();key,obj=self.event(h)
   with patch('semantic_stream.storage.CHUNK',chunk):
    # Parse the complete nested containing-event bytes through every split,
    # including hex, null, source refs and two attempt records.
    blob=h[0].store.write([wire(obj)]);parsed=h[0].store.parse(blob)
    self.assertEqual(parsed,obj)
    for ev in parsed['events']:
     raw=ev['fields']['input_record']
     if raw is not None:self.assertEqual(h[0].bytes(raw).small(65536),bytes.fromhex(obj['events'][ev['fields']['attempt_ordinal']-1]['fields']['input_record']))
