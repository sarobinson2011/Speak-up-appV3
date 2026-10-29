"""Mandatory internal status forwarding over the reviewed client-state chain. Saved evidence only."""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 192484, 'sha256': '903b4369f0e9d009b60c60a260e3dc44c399c0a69629eacdf7870a5d7feba7b0'}
CLIENT_MANIFEST={'bytes':426786,'sha256':'f57144894667a71fce5ae3acca0229e2c95313db307f6ffbb8e02a04c8cf72f3'}
STATE_RECEIPT={'bytes':2180446,'sha256':'feefd0f5282b51608c7fd95ab24518aa1be9e491aa24f004ed588b1906c7aab9'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def require(v,message):
 if not v:raise ValueError(message)

def same(a,b,message):require(enc(a)==enc(b),message)

def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'retained/state'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CLIENT-ROOT-TYPE')
 p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'CLIENT-MANIFEST-TYPE');raw=p.read_bytes();require(identity(raw)==CLIENT_MANIFEST,'CLIENT-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen_dirs=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CLIENT-UNDECLARED-DIRECTORY');seen_dirs.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CLIENT-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen_dirs==dirs,'CLIENT-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CLIENT-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);producer=root/'code/managed_coverage.py'
 require(stat.S_ISREG(producer.lstat().st_mode),'CLIENT-PRODUCER-TYPE');require(identity(producer.read_bytes())==PRODUCER_PIN,'CLIENT-PRODUCER-SOURCE')
 prior=module(base/'code/correspondence.py','_state_client_predecessor');data=prior.inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_client_state_coverage')}

def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def manager_fields(data):
 d=inner(data);v=d['values'];g=d['guards']
 return data['coverage'].compile_status_fields(d['manager'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'])
def catalogue(data):return data['coverage'].compile_status_forward(*sources(data),manager_fields(data),inner(data)['ctx']['binding'])
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];prior=p.derive_client_state(pd,p.catalogue(pd))
 saved=(fresh['prior_root']/'results/client-state-correspondence.json').read_bytes();require(identity(saved)==STATE_RECEIPT and enc(prior)==saved,'STATUS-FORWARD-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e'])}
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'STATUS-FORWARD-EVIDENCE-TYPES')
 # The same validated predecessor supplies the trace/status source snapshots,
 # acquisition/instance and HEAD bindings. Mutually agreeing reports cannot.
 expected=basis['evidence'];path='evidence/execution-trace.json';require(path in candidate,'STATUS-FORWARD-MISSING-TRACE')
 want=json.loads(expected[path]);got=json.loads(candidate[path]);require(type(got) is dict and type(got.get('events')) is list,'STATUS-FORWARD-TRACE-SHAPE')
 for event in want['events']:
  if event.get('function')=='ManagedAuthority.status' and event.get('event')=='return' and event.get('normal_return'):
   seq=event['seq'];require(len(got['events'])>seq and type(got['events'][seq]) is dict,'STATUS-FORWARD-MISSING-STATUS')
   other=got['events'][seq];same(other.get('value'),event['value'],'STATUS-FORWARD-VALIDATED-STATUS-VALUE');same(other.get('state'),event['state'],'STATUS-FORWARD-VALIDATED-STATUS-SNAPSHOT')
 p=basis['fresh']['prior_module'];p._compare_evidence({'fresh':basis['fresh']['prior_data'],'catalogue':p.catalogue(basis['fresh']['prior_data']),'evidence':expected},candidate)
def _rows(basis):
 rows=[];cat=basis['catalogue'];coverage=basis['fresh']['coverage'];e=basis['evidence'];path='evidence/execution-trace.json';trace=json.loads(e[path]);defs=cat['manager_fields']['declarations']
 for context in basis['prior']['contexts']:
  same(context['field_declarations'],cat['manager_fields'],'STATUS-FORWARD-PREDECESSOR-FIELDS')
  anchor=context['client_state_return_correspondence']['validated_state_anchor'];samples=[]
  for sample in context['saved_status_fields']:
   same(sample['instance'],anchor['instance'],'STATUS-FORWARD-VALIDATED-INSTANCE');same(sample['trace_identity'],identity(e[path]),'STATUS-FORWARD-TRACE-PIN')
   returned=[v for v in trace['events'] if v.get('frame')==sample['frame'] and v.get('event')=='return' and v.get('normal_return')];require(len(returned)==1,'STATUS-FORWARD-STATUS-RETURN');ret=returned[0];require(ret['function']=='ManagedAuthority.status','STATUS-FORWARD-MANAGER-CALLER')
   snapshot={d['value']['name']:ret['state'][d['value']['name']] for d in defs if d['value']['op']=='state'};value=coverage.status_snapshot_value(cat,snapshot);same(ret['value'],value,'STATUS-FORWARD-SAVED-SELECTORS')
   same([f['declaration'] for f in sample['fields']],[d['id'] for d in defs],'STATUS-FORWARD-SAVED-FIELD-COVERAGE')
   for f,d in zip(sample['fields'],defs):same(f['value'],value[d['name']],'STATUS-FORWARD-SAVED-FIELD');require(f['return_pointer']==f"/events/{ret['seq']}/value/{d['name']}",'STATUS-FORWARD-FIELD-POINTER')
   samples.append({'occurrence':sample['occurrence'],'frame':sample['frame'],'instance':copy.deepcopy(sample['instance']),'record':{'acquisition':anchor['record']['acquisition'],'artifact':path,**identity(e[path]),'return_pointer':f"/events/{ret['seq']}/value",'snapshot_pointer':f"/events/{ret['seq']}/state"},'value':copy.deepcopy(value),'snapshot':copy.deepcopy(snapshot),'existing_field_links':copy.deepcopy(sample),'forwarding_frame_join':None,'meaning':'Validated manager sample only; not a session/control status call or its forwarding history'})
  rows.append({'context':context['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(anchor),'validated_manager_samples':samples,'predecessor_receipt':identity(basis['saved']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'field_links':copy.deepcopy(d['fields']),'same_result_reference_as':'manager-return','frame':None,'observed_value':None,'invocation':None} for d in cat['declarations']],
   'validated_reference_basis':{'static_manager_references':copy.deepcopy(context['reference_declarations']),'saved_reference_scope':copy.deepcopy(context['saved_reference_scope']),'source_owner_token_edges':copy.deepcopy(cat['reference_edges']),'physical_identity':None,'underlying_connection_identity':None},
   'scope':{'context':context['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':None,'request_identifier':None},'destination':'designated internal control caller','runtime_forwarding_links':None,'actual_status_forwarding_count':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'separate_observer':copy.deepcopy(context['client_state_return_correspondence']['separate_observer']),'observer_join':None,'missing':'No ManagedSession.status/_Control.status frames or physical return-reference observations; conditional expressions do not fill them.'})
 return rows
def _check_rows(basis,claims,rows):
 require(type(claims) is list and len(claims)==len(rows)==2,'STATUS-FORWARD-CONTEXT-DOMAIN')
 for got,want in zip(claims,rows):
  require(type(got) is dict and set(got)==set(want),'STATUS-FORWARD-CONTEXT-FIELDS');same(got['context'],want['context'],'STATUS-FORWARD-CONTEXT-ORDER')
  same(got['instance_anchor'],want['instance_anchor'],'STATUS-FORWARD-INSTANCE-ANCHOR');same(got['validated_manager_samples'],want['validated_manager_samples'],'STATUS-FORWARD-SAMPLES')
  same(got,want,'STATUS-FORWARD-CORRESPONDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'STATUS-FORWARD-CATALOGUE');d=inner(data);fd=inner(basis['fresh'])
 require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'] and d['manager']==fd['manager'],'STATUS-FORWARD-CANDIDATE-SOURCES');same(d['ctx']['binding'],fd['ctx']['binding'],'STATUS-FORWARD-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence);rows=_rows(basis)
 if claims is not None:_check_rows(basis,claims,rows)
 return rows,basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 result=copy.deepcopy(basis['prior']);result['format']='I164-INTERNAL-STATUS-FORWARD-CORRESPONDENCE-1';result['prior_client_state_components']=result.pop('extension_components');result['prior_client_state_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'STATUS-FORWARD-DERIVE-CONTEXT');context['internal_status_return_correspondence']=copy.deepcopy(row)
 result['new_internal_status_limits']={'static_conditional_correspondence':True,'runtime_forwarding':'UNAVAILABLE','physical_reference_identity':None,'observer_join':None,'actual_call_count':None,'request_independent':True,'READY_requirement_added':False,'data_conversion_added':False,'new_output_or_capture_permission':False,'history_evidence_invented':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return result
def derive_status(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def invocation_scope(anchor,invocation):
 require(type(invocation) is str and bool(invocation),'STATUS-FORWARD-INVOCATION')
 return {'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
def reference_premises(scope,owner_present,owner_failed):
 require(type(owner_present) is bool and type(owner_failed) is bool,'STATUS-FORWARD-OWNER-PREMISE')
 refs={n:{'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/'+n+'-symbol'} for n in ('control','token','owner','session','manager','result')}
 refs.update({'control.token':copy.deepcopy(refs['token']),'owners[token]':copy.deepcopy(refs['owner']) if owner_present else None,'owner.wrapper':copy.deepcopy(refs['session']),'session.managed':copy.deepcopy(refs['manager']),'owner_failed':owner_failed});return refs
def _construct_checked(basis,rows,case):
 require(type(case) is dict and set(case)=={'kind','context','anchor','owner_present','owner_failed','manager_basis','projection'} and case['kind']=='CONSTRUCTED-INTERNAL-STATUS-FORWARD','STATUS-FORWARD-CONSTRUCTED-CASE')
 matches=[r for r in rows if r['context']==case['context']];require(len(matches)==1,'STATUS-FORWARD-CONSTRUCTED-CONTEXT');row=matches[0];anchor=row['instance_anchor'];same(case['anchor'],anchor,'STATUS-FORWARD-CONSTRUCTED-ANCHOR')
 p=case['projection'];require(type(p) is dict and type(p.get('occurrence')) is str,'STATUS-FORWARD-CONSTRUCTED-PROJECTION');scope=invocation_scope(anchor,p['occurrence']);refs=reference_premises(scope,case['owner_present'],case['owner_failed'])
 mb=case['manager_basis'];require(type(mb) is dict,'STATUS-FORWARD-MANAGER-BASIS')
 if mb.get('kind')=='saved-manager-value':
  require(set(mb)=={'kind','sample_occurrence'},'STATUS-FORWARD-SAMPLE-BASIS');found=[x for x in row['validated_manager_samples'] if x['occurrence']==mb['sample_occurrence']];require(len(found)==1,'STATUS-FORWARD-SAMPLE-OCCURRENCE');snapshot=copy.deepcopy(found[0]['snapshot'])
 elif mb.get('kind')=='constructed-snapshot':
  require(set(mb)=={'kind','snapshot'},'STATUS-FORWARD-SNAPSHOT-BASIS');snapshot=copy.deepcopy(mb['snapshot']);basis['fresh']['coverage'].status_snapshot_value(basis['catalogue'],snapshot)
 else:require(mb=={'kind':'unreached'},'STATUS-FORWARD-UNSUPPORTED-BASIS');snapshot=None
 validated={'occurrence':p['occurrence'],'scope':scope,'references':refs,'outcomes':copy.deepcopy(p.get('outcomes')),'manager_snapshot':snapshot}
 value=basis['fresh']['coverage'].status_forward_projection(basis['catalogue'],p,validated)
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(anchor),'manager_basis':copy.deepcopy(mb),'projection':value,'premises':'Explicit constructed conditional snapshot/outcomes and source-derived references; saved sample used only where selected, no runtime forwarding join','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 rows,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,rows,case)
def derive(root=ROOT):
 data=inputs(root);return derive_status(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'STATUS-FORWARD-RECEIPT-BYTES');value=json.loads(saved);require(type(value) is dict and value.get('format')=='I164-INTERNAL-STATUS-FORWARD-CORRESPONDENCE-1' and type(value.get('contexts')) is list and len(value['contexts'])==2 and all(type(c) is dict and 'internal_status_return_correspondence' in c for c in value['contexts']),'STATUS-FORWARD-MANDATORY-RELATION')
 require(saved==enc(derive(root)),'STALE-OR-ALTERED-INTERNAL-STATUS-CORRESPONDENCE');return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'runtime_status_forwarding':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
