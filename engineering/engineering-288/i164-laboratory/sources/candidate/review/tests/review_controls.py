"""Fresh independent candidate controls; in-memory substitutions only.
Usage: python -B review_controls.py EXTRACTED_CANDIDATE RESULT_JSON
No runtime lifecycle, source rewrite, network, large model or streams.
"""
import copy,hashlib,json,pathlib,resource,socket,sys,time,traceback
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]);sys.dont_write_bytecode=True
sys.path.insert(0,str(root/'tools'))
def no_network(*a,**k):raise AssertionError('Network forbidden in review')
socket.socket=no_network;socket.create_connection=no_network
import baseline as bl
from common import Invalid,enc,parse,sha
from ingest import validate_export
from static_ingest import ingest
start=time.monotonic();checks=[]
def check(name,fn):
 try:result=fn();checks.append({'name':name,'status':'PASS','detail':result})
 except BaseException as e:
  checks.append({'name':name,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc()});raise
 finally:out.write_text(json.dumps({'checks':checks,'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
def rejection(fn,prefix):
 try:fn()
 except Invalid as e:
  assert str(e).startswith(prefix),(str(e),prefix);return str(e)
 raise AssertionError('unexpected acceptance')
expected=bl.construct();actual={p.name:json.loads(p.read_bytes()) for p in (root/'candidate').iterdir() if p.is_file()}
check('fresh-source-construction-and-exact-candidate-bytes',lambda:(bl.validate_values(actual,expected),all((root/'candidate'/p).read_bytes()==enc(v) for p,v in expected.items()))[0])
assert all((root/'candidate'/p).read_bytes()==enc(v) for p,v in expected.items())
# Use one altered artifact first in the expected iteration order: values are unmodified.
# This preserves the real comparison gate while avoiding repeatedly serializing 44MB.
def mutate(label,p,change,repin=False):
 def run():
  val=copy.deepcopy(actual[p]);change(val);a={**actual,p:val}
  if repin:
   profile=copy.deepcopy(a['profile-binding.json'])
   for n in profile['metadata']:profile['metadata'][n]={'bytes':len(enc(a[n])),'sha256':sha(enc(a[n]))}
   a['profile-binding.json']=profile
   identity=copy.deepcopy(a['identity.json'])
   for n in identity['artifacts']:identity['artifacts'][n]={'bytes':len(enc(a[n])),'sha256':sha(enc(a[n]))}
   a['identity.json']=identity
  return {'rehashed_metadata':repin,'rejection':rejection(lambda:bl.validate_values(a,{p:expected[p],**{k:v for k,v in expected.items() if k!=p}}),'ARTIFACT-SUBSTITUTION:'+p)}
 check(label,run)
mutate('rehashed-parent-rebinding','fields.json',lambda x:x['prospective'][1].update(parent=x['prospective'][-1]['id']),True)
mutate('rehashed-field-type-coercion','fields.json',lambda x:x['prospective'][0]['native_template'].update(type='STRING'),True)
mutate('rehashed-optional-guard-promotion','fields.json',lambda x:next(r for r in x['prospective'] if r['template_id']=='PENDING:/result')['native_template'].update(guard='present',presence='required'),True)
mutate('rehashed-source-selector-substitution','fields.json',lambda x:next(r for r in x['prospective'] if r['template_id']=='ACTION:/template')['native_template'].update(selector='/intent'),True)
mutate('rehashed-namespace-class-deletion','namespace.json',lambda x:x['historical_classes'].remove('CORE:AUTHORIZATION-HEADER.serialization-domain'),True)
mutate('rehashed-schema-variant-loss','schemas.json',lambda x:x['prospective']['ABI-signPetitionWithZKProof'].pop(next(iter(x['prospective']['ABI-signPetitionWithZKProof']))),True)
mutate('rehashed-source-form-membership-mismatch','source-forms.json',lambda x:x['prospective'][0]['field_classes'].pop(),True)
mutate('rehashed-context-class-directory','contexts.json',lambda x:x['associations'][1].update(class_directory='fields.json#/inherited'),True)
mutate('rehashed-duplicate-context','contexts.json',lambda x:x['associations'][1].update(context=x['associations'][0]['context']),True)
mutate('rehashed-ancestry-endpoint-swap','associations.json',lambda x:x['prospective'][0]['endpoints'][0].update(**{'class':x['prospective'][1]['endpoints'][0]['class']}),True)
mutate('rehashed-custody-promotion','associations.json',lambda x:x['prospective'][0].update(custody=['CONFIDENTIAL']*7),True)
mutate('rehashed-physical-storage-blocker-erasure','directories.json',lambda x:x.update(physical_storage={'bound':0,'status':'COMPLETE'}),True)
mutate('rehashed-external-evidence-bound-invention','directories.json',lambda x:x.update(external_evidence={'bound':1024,'status':'COMPLETE'}),True)
mutate('rehashed-journal-limit-increase','directories.json',lambda x:x['local']['journal'].update(max=384001),True)
mutate('rehashed-ledger-duty-deletion','ledger-duties.json',lambda x:x['prospective_duties'].pop(),True)
mutate('rehashed-appointed-assessor-invention','ledger-duties.json',lambda x:x['prospective_duties'][0].update(qualified_assessor='MADE-UP'),True)
mutate('stale-runtime-binding','profile-binding.json',lambda x:x['runtime'][0].update(sha256='0'*64))
mutate('mixed-adapter-binding','profile-binding.json',lambda x:x['adapters'][0].update(sha256=x['runtime'][0]['sha256']))
mutate('mixed-field-artifact-binding','profile-binding.json',lambda x:x['metadata']['fields.json'].update(sha256=x['metadata']['schemas.json']['sha256']))
mutate('rehashed-status-and-stream-promotion','status.json',lambda x:x.update(canonical_registration='COMPLETE',canonical_head='INVENTED',complete_immutable_model_binding=True,qualification=True,stream_identities='COMPLETE',actual_admission=True,blockers=[]),True)
check('unknown-candidate-artifact-rejected',lambda:rejection(lambda:bl.validate_values({**actual,'rogue.json':{}},expected),'ARTIFACT-MEMBERSHIP'))
check('missing-profile-artifact-rejected',lambda:rejection(lambda:bl.validate_values({k:v for k,v in actual.items() if k!='profile-binding.json'},expected),'ARTIFACT-MEMBERSHIP'))
check('final-binding-rejects-claimed-authority-and-qualification',lambda:rejection(lambda:bl.final_binding(actual,{'authority':'Steve','qualified':True,'all_evidence':True}),'FINAL-BINDING-BLOCKED:'))
check('final-binding-rejects-erased-blockers',lambda:rejection(lambda:bl.final_binding({**actual,'status.json':{'blockers':[],'actual_admission':True}},{}),'FINAL-BINDING-BLOCKED:'))
# Input substitution reaches the pinned-input boundary without modifying any bytes on disk.
for path in ['native/prior-code/model_kernel/catalog.py','native/retained/registers/fields.json','support/reference/runtime/authority.py','provenance/input-pins.json']:
 def altered_input(path=path):
  original=bl.read
  bl.read=lambda p:original(p)+(b' ' if p==path else b'')
  try:return rejection(bl.pin_inputs,'INPUT-PIN-SUBSTITUTION' if path=='provenance/input-pins.json' else 'INPUT-IDENTITY:'+path)
  finally:bl.read=original
 check('pinned-input-substitution:'+path,altered_input)
# Test the collision guard against a prospective ID present in the full inherited argument.
bundle=json.loads((root/'support/declarations/static.json').read_bytes());ns=bl.namespace()
check('full-namespace-collision-rejection',lambda:rejection(lambda:bl.declarations(bundle,ns+[actual['fields.json']['prospective'][0]['id']]),'INHERITED-CLASS-CONFLICT'))
def roundtrip():
 rows=bl.mapping('records/added-fields.json');rows[0]['native']['slots']=float(rows[0]['native']['slots'])
 return rejection(lambda:bl.roundtrip(rows,'records/added-fields.json'),'NATIVE-ROUNDTRIP')
check('native-roundtrip-integer-to-float-rejection',roundtrip)
# Fresh semantic parsing of a small selected subset, not all prior controls.
by={r['template_id']:r['id'] for r in actual['fields.json']['prospective']}
for name in ['ord-abandon','failed-zk-proceed','exit-after_signature_commit']:
 def example(name=name):
  x=parse((root/'support/fixtures'/f'{name}.json').read_bytes(),200000000);v=validate_export(x);record=json.loads((root/'results/examples'/f'{name}.json').read_bytes())
  assert len(record['attempt_occurrences'])==v['attempts'] and len(record['action_occurrences'])==v['actions']
  observed={'ATTEMPT':{},'ACTION':{}}
  for kind,obj in v['objects']:
   if kind in observed:observed[kind][sha(enc(obj))]=obj
  for field,kind in [('attempt_occurrences','ATTEMPT'),('action_occurrences','ACTION')]:
   assert {r['reference'] for r in record[field]}==set(observed[kind])
   for r in record[field]:assert r['parsed']==observed[kind][r['reference']] and r['class']==by[kind+':']
  projected=ingest(x,bundle);joins={r['occurrence_id']:r for r in projected['response_selector_coverage'] if r['pointer']=='/signature'}
  occ={r['id']:r for r in projected['actual_occurrences']}
  assert len(joins)==len(record['response_signature_joins'])
  for r in record['response_signature_joins']:
   assert {k:v for k,v in r.items() if k not in ['candidate_class','exact_bytes_hex']}==joins[r['occurrence_id']]
   assert r['exact_bytes_hex']==occ[r['occurrence_id']]['exact_bytes_hex'] and r['candidate_class']==by['RESPONSE:/signature']
  assert projected['actual_admission'] is False and projected['stream_identities']=='UNCOMPUTED'
  return {'attempts':v['attempts'],'actions':v['actions'],'signature_joins':len(joins),'events':v['events'],'saved_only':True,'actual_admission':False}
 check('fresh-saved-association-reconstruction:'+name,example)
x=parse((root/'support/fixtures/ord-early.json').read_bytes(),200000000)
for label,alter,code in [
 ('cross-export-head',lambda q:q.update(head=json.loads((root/'support/fixtures/zk-early.json').read_bytes())['head']),'HEAD-HISTORY'),
 ('omitted-event',lambda q:q['events'].pop(0),'EVENT-ORDER'),
 ('forged-signed-envelope',lambda q:q['journal'][0].__setitem__(2,enc({**parse(bytes.fromhex(q['journal'][0][2])),'signature':'00'*64}).hex()),'AUTHENTICATION')]:
 def negative(alter=alter,code=code):
  q=copy.deepcopy(x);alter(q);return rejection(lambda:validate_export(q),code)
 check('saved-evidence-negative:'+label,negative)
print(json.dumps({'controls':len(checks),'all_pass':all(x['status']=='PASS' for x in checks),'seconds':time.monotonic()-start}))
