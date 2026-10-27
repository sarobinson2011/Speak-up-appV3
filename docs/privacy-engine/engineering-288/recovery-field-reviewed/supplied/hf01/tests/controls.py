"""HF-01 new focused controls. No previous review/suite or runtime operation."""
import argparse,copy,hashlib,json,os,runpy,sys,types
from pathlib import Path

def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 name=frame.f_code.co_filename.rsplit('/',1)[-1]
 if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
def module(p):
 m=types.ModuleType('_hf01_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];error=None;projections=[];sources={n:identity((a.root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
 def check(label,f):
  v=f();assert v is not False,label;rows.append({'check':label,'result':'PASS'})
  with (a.output/'progress.jsonl').open('a') as out:out.write(json.dumps(rows[-1])+'\n')
  return v
 def reject(f,expected=None):
  try:f()
  except (ValueError,TypeError,KeyError) as e:
   if expected is not None:assert str(e)==expected,(str(e),expected)
   return str(e)
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.recovery_inputs(a.root);cat=m.recovery_catalogue(data);e=dict(data['ctx']['e'])
  check('unchanged supported producer bytes',lambda:(a.root/'code/managed_coverage.py').read_bytes()==(a.root/'original/code/managed_coverage.py').read_bytes())
  check('pristine source catalogue',lambda:m.check_recovery_catalogue(data,cat))
  observed,capture,row=check('pristine semantic connection',lambda:m.connected_recovery(data,cat))
  bundle=check('pristine derivation',lambda:m.derive_recovery(data,cat));saved=m.enc(bundle)
  if a.write:
   with (a.root/'results/hf01-correspondence.json').open('xb') as f:f.write(saved)
  else:assert saved==(a.root/'results/hf01-correspondence.json').read_bytes()
  check('pristine public validation',lambda:m.validate(a.root,saved))
  original_receipt=json.loads((a.root/'original/results/recovery-field-correspondence.json').read_bytes())
  for index,context in enumerate(bundle['contexts']):
   old=original_receipt['contexts'][index];new=context['hf01_evidence_binding']
   check('all old context members preserved '+context['context'],lambda old=old,context=context:all(m.enc(context[k])==m.enc(v) for k,v in old.items()))
   check('same occurrence/instance/acquisition '+context['context'],lambda context=context,new=new:new['occurrence']['id']==context['saved_recovery_fields'][0]['occurrence'] and new['instance']==context['saved_recovery_fields'][0]['instance'] and new['head_record']['acquisition']==new['occurrence']['call']['acquisition'])
   check('same predecessor trace identity '+context['context'],lambda context=context,new=new:new['trace_identity']==context['saved_recovery_fields'][0]['trace_identity']==next(r['trace_identity'] for r in context['saved_reference_scope'] if r['occurrence']==new['occurrence']['id']))
   check('boolean constants preserved '+context['context'],lambda context=context:{d['name']:d['origin'].get('value') for d in context['recovery_field_declarations']['declarations'] if d['origin']['kind']=='literal'}=={'recovery_only':True,'new_attempt_authorized':False})
  check('no missing scalar/frame fabricated',lambda:row['fields'][0]['head_relation']['validator_scalar_pointer'] is None and not capture['scalar_return_recorded'] and bundle['new_recovery_slice_limits']['observer_frame'] is None)
  # The exact independently retained witness is applied as byte substitutions.
  def witness(which):
   altered=dict(e);folder=a.root/'retained/review'/which/'mutated'
   members=[p for p in folder.rglob('*') if p.is_file()];assert len(members)==7
   for p in members:altered[p.relative_to(folder).as_posix()]=p.read_bytes()
   return altered
  minimal=witness('head-witness-primary');exploratory=witness('coordinated-head-probe')
  for label,altered in [('minimal seven-report witness',minimal),('reserialized seven-report witness',exploratory)]:
   check('semantic rejects '+label,lambda altered=altered:reject(lambda:m.connected_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE'))
   check('derivation rejects '+label,lambda altered=altered:reject(lambda:m.derive_recovery(data,cat,altered),'HF01-HEAD-EXPECTED-STATE'))
  for name in ('head-witness-primary','coordinated-head-probe'):
   raw=(a.root/'retained/review'/name/'altered-derived-receipt.json').read_bytes()
   check('public rejects original mixed receipt '+name,lambda raw=raw:reject(lambda:m.validate(a.root,raw)))
  # This deliberately mutates the candidate's baseline too. Its changed reports
  # must not become the independently reloaded predecessor expectations.
  d=dict(data);d['ctx']=dict(data['ctx']);d['ctx']['e']=minimal
  check('semantic rejects candidate baseline plus reports substitution',lambda:reject(lambda:m.connected_recovery(d,cat),'HF01-HEAD-EXPECTED-STATE'))
  check('derivation rejects candidate baseline plus reports substitution',lambda:reject(lambda:m.derive_recovery(d,cat),'HF01-HEAD-EXPECTED-STATE'))
  basis=m._validated_predecessor_basis(data)
  check('pure binder rejects witness against independently validated basis before byte-map gate',lambda:reject(lambda:m._bind_predecessor_evidence(basis,minimal,observed,cat),'HF01-HEAD-EXPECTED-STATE'))
  # Establish that comparison is a relationship, not a zero-head blacklist or
  # a convenient new string/domain bound. These are explicit algebra premises,
  # never authenticated evidence, requests or claimed runtime observations.
  export=json.loads(e['evidence/recovery-export-0.json']);state=json.loads(bytes.fromhex(export['head']))
  for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
   for value in ('1'+'0'*63,'f'*64,'nonzero\u2603\x00\n'+'x'*16385):
    expected=copy.deepcopy(export);s=copy.deepcopy(state);s['head']=value;expected['head']=m.enc(s).hex();expected['expected_head']=value
    check('constructed equal head premise '+context+' '+str(len(value)),lambda expected=expected:m._compare_validated_head(expected,expected,'head'))
    candidate=copy.deepcopy(expected);candidate['expected_head']=value+'different'
    check('constructed distinct expected head rejects '+context+' '+str(len(value)),lambda candidate=candidate,expected=expected:reject(lambda:m._compare_validated_head(candidate,expected,'head'),'HF01-HEAD-EXPECTED-STATE'))
    projections.append({'kind':'CONSTRUCTED-HEAD-COMPARISON','context':context,'head':value,'actual_observation':False,'authenticated_state':False,'new_limit':False})
  # Adjacent semantic relations are exercised directly using a freshly validated
  # basis, while end-to-end checks below cover missing/stale/mixed evidence.
  mutations=[('decoded head',lambda x:x.update(head=m.enc(dict(state,head='f'*64)).hex()),'HF01-HEAD-STATE-SELECTOR'),
   ('other state field',lambda x:x.update(head=m.enc(dict(state,seq=17)).hex()),'HF01-COMPLETE-VALIDATED-STATE'),
   ('raw state representation',lambda x:x.update(head=(bytes.fromhex(x['head'])+b' ').hex()),'HF01-EXACT-VALIDATED-STATE-BYTES'),
   ('configuration',lambda x:x.update(config={'session':'other'}),'HF01-CONFIGURATION-BASIS'),
   ('ownership',lambda x:x.update(ownership_meta='00'),'HF01-OWNERSHIP-BASIS')]
  for label,edit,reason in mutations:
   x=copy.deepcopy(export);edit(x);check('head relation rejects '+label,lambda x=x,reason=reason:reject(lambda:m._compare_validated_head(x,export,'head'),reason))
  for idx in (0,1):
   o=copy.deepcopy(observed);o['contexts'][idx]['instance']['ownership_incarnation']='other'
   check('binding rejects mixed instance context '+str(idx),lambda o=o:reject(lambda:m._bind_predecessor_evidence(basis,e,o,cat),'HF01-ACQUISITION-INSTANCE-OCCURRENCE-BASIS'))
   o=copy.deepcopy(observed);o['contexts'][idx]['occurrences']=[]
   check('binding rejects missing occurrences context '+str(idx),lambda o=o:reject(lambda:m._bind_predecessor_evidence(basis,e,o,cat),'HF01-ACQUISITION-INSTANCE-OCCURRENCE-BASIS'))
  altered=dict(e);altered.pop('evidence/session-records/binding.json')
  check('semantic rejects missing instance binding',lambda:reject(lambda:m.connected_recovery(data,cat,altered)))
  check('derivation rejects missing instance binding',lambda:reject(lambda:m.derive_recovery(data,cat,altered)))
  altered=dict(e);altered['evidence/execution-trace.json']=minimal['evidence/execution-trace.json']
  check('semantic rejects stale single trace',lambda:reject(lambda:m.connected_recovery(data,cat,altered)))
  check('derivation rejects stale single trace',lambda:reject(lambda:m.derive_recovery(data,cat,altered)))
  if not a.recovered:
   for name in ('evidence/recovery-export-0.json','evidence/confirmed-close.json','preparation/worker.py'):
    altered=dict(e);del altered[name]
    check('semantic missing '+name,lambda altered=altered:reject(lambda:m.connected_recovery(data,cat,altered)))
    check('derivation missing '+name,lambda altered=altered:reject(lambda:m.derive_recovery(data,cat,altered)))
   altered=dict(e);altered['MANIFEST.json']=b'{}\n'
   check('semantic unused record substitution rejects',lambda:reject(lambda:m.connected_recovery(data,cat,altered)))
   check('derivation unused record substitution rejects',lambda:reject(lambda:m.derive_recovery(data,cat,altered)))
   for name in minimal:
    if minimal[name]==e[name]:continue
    restored=dict(minimal);restored[name]=e[name]
    check('semantic one-member restoration '+name,lambda restored=restored:reject(lambda:m.connected_recovery(data,cat,restored)))
  for idx in (0,1):
   b=copy.deepcopy(bundle);del b['contexts'][idx]['hf01_evidence_binding']['head_record']
   check('public missing binding context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
   b=copy.deepcopy(bundle);b['contexts'][idx]['saved_recovery_fields'][0]['fields'][0]['value']='f'*64;b['contexts'][idx]['hf01_evidence_binding']['occurrence']['observed_local_values']['managed-local:recovery-result']['head']='f'*64
   check('public coordinated receipt mutation context '+str(idx),lambda b=b:reject(lambda:m.validate(a.root,m.enc(b))))
  if not a.recovered:
   b=copy.deepcopy(bundle);b['contexts'].pop();check('public missing context',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
   b=copy.deepcopy(bundle);b['contexts'][1]=copy.deepcopy(b['contexts'][0]);check('public duplicated context',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
   b=copy.deepcopy(bundle);b['prior_reference_receipt']['sha256']='0'*64;check('public stale predecessor',lambda:reject(lambda:m.validate(a.root,m.enc(b))))
  # Mutate every returned result category. No later expectations may alias it.
  answer=m.validate(a.root,saved);answer['contexts'].clear();answer['receipt'].clear()
  observed['contexts'][0]['occurrences'].clear();observed['contexts'][1]['instance'].clear();row['fields'].clear();capture['value_functions'].clear()
  bundle['contexts'][0]['hf01_evidence_binding']['head_record'].clear();bundle['contexts'][1]['hf01_evidence_binding']['occurrence']['observed_local_values'].clear()
  basis['observed']['contexts'].clear();basis['bindings'].clear();basis['prior']['contexts'].clear();basis['evidence'].clear()
  check('semantic pristine after nested result mutations',lambda:m.connected_recovery(data,cat))
  check('derivation pristine after nested result mutations',lambda:m.enc(m.derive_recovery(data,cat))==saved)
  check('public pristine after nested result mutations',lambda:m.validate(a.root,saved))
  check('public mutated result remains rejected',lambda:reject(lambda:m.validate(a.root,m.enc(bundle))))
  check('boundaries unchanged',lambda:bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and bundle['new_recovery_slice_limits']['all_eleven_obligations_preserved'] and bundle['new_recovery_slice_limits']['actual_admission'] is False)
  assert sources=={n:identity((a.root/'code'/n).read_bytes()) for n in sources}
 except BaseException as ex:error=repr(ex);raise
 finally:
  (a.output/'constructed-premises.json').write_text(json.dumps(projections,indent=2)+'\n')
  (a.output/'RESULT.json').write_text(json.dumps({'result':'PASS' if error is None else 'FAIL','passed':len(rows),'checks':rows,'error':error,'sources':sources,'source_after':{n:identity((a.root/'code'/n).read_bytes()) for n in sources},'root':str(a.root),'python':sys.version,'optimization':sys.flags.optimize,'focused_recovered':a.recovered,'new_HF01_controls_only':True,'database_connections':0,'runtime_operations':0,'no_completed_review_rerun':True},indent=2)+'\n')
 print('PASS',len(rows),'HF-01 controls')
if __name__=='__main__':main()
