"""Mandatory config return/copy correspondence over the reviewed binding chain.
All observations remain saved evidence. No application/session code executes.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 95842, 'sha256': '9dca02b1a52f8e3db950d39c57db4cc60204bb81fcc012f6bac3891709b57c9e'}
BINDING_MANIFEST={'bytes':194315,'sha256':'c1ee52e07d02c3dd81d0de6c5f8c0c11e455aca3da447f34e6a846bd674c05f8'}
BINDING_RECEIPT={'bytes':746342,'sha256':'c284875c104ff8fad9690e1018c7c653f5f8116bc030cf9fbe26994f3311698b'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,message):
 if not v:raise ValueError(message)
def same(a,b,message):require(enc(a)==enc(b),message)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'retained/binding'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CONFIG-ROOT-TYPE')
 p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'CONFIG-MANIFEST-TYPE');raw=p.read_bytes();require(identity(raw)==BINDING_MANIFEST,'CONFIG-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen_dirs=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CONFIG-UNDECLARED-DIRECTORY');seen_dirs.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CONFIG-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen_dirs==dirs,'CONFIG-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CONFIG-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);producer=root/'code/managed_coverage.py'
 require(stat.S_ISREG(producer.lstat().st_mode),'CONFIG-PRODUCER-TYPE');require(identity(producer.read_bytes())==PRODUCER_PIN,'CONFIG-PRODUCER-SOURCE')
 prior=module(base/'code/correspondence.py','_config_binding_predecessor');data=prior.inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_config_managed_coverage')}

def catalogue(data):
 d=data['prior_data']['prior_data'];v=d['values'];g=d['guards'];refs=d['reference_module'].reference_catalogue(d)
 return data['coverage'].compile_config_return(d['manager'],d['authority'],v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],refs)

def _basis(data):
 # Reload sources, evidence and predecessor validation. No returned object is
 # used as an expectation, even after nested/candidate baseline mutations.
 fresh=inputs(data['root']);p=fresh['prior_module'];d=fresh['prior_data']
 prior=p.derive_binding(d,p.catalogue(d));saved=(fresh['prior_root']/'results/binding-correspondence.json').read_bytes()
 require(identity(saved)==BINDING_RECEIPT and enc(prior)==saved,'CONFIG-PREDECESSOR-RECEIPT')
 evidence=dict(d['prior_data']['ctx']['e']);cat=catalogue(fresh)
 return {'fresh':fresh,'prior':prior,'saved':saved,'evidence':evidence,'catalogue':cat}

def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CONFIG-EVIDENCE-BYTES')
 path='evidence/recovery-export-0.json';require(path in candidate,'CONFIG-MISSING-EXPORT');want=json.loads(basis['evidence'][path]);got=json.loads(candidate[path])
 require(type(got) is dict and 'config' in got,'CONFIG-MISSING-VALUE');basis['fresh']['coverage'].config_value_type(basis['catalogue'],got['config'])
 same(got['config'],want['config'],'CONFIG-VALIDATED-INSTANCE-VALUE')
 # Independent semantic comparison is before the exact full evidence gate.
 basis['fresh']['prior_module']._compare_evidence(basis['evidence'],candidate,'binding')

def _rows(basis):
 rows=[];cat=basis['catalogue'];e=basis['evidence'];path='evidence/recovery-export-0.json';export=json.loads(e[path]);value=export['config'];basis['fresh']['coverage'].config_value_type(cat,value)
 trace_path='evidence/execution-trace.json';trace=json.loads(e[trace_path])
 for context in basis['prior']['contexts']:
  name=context['context'];binding=context['binding_return_correspondence']['validated_binding_anchor'];hb=context['hf01_evidence_binding'];inst=hb['instance'];occ=hb['occurrence']
  same(binding['instance'],inst,'CONFIG-INSTANCE-JOIN');same(value['session'],inst['session_label'],'CONFIG-SESSION-JOIN')
  same(binding['record'],hb['head_record'],'CONFIG-RECOVERY-RECORD-JOIN');require(binding['record']['artifact']==path,'CONFIG-RECORD-PATH')
  require({k:binding['record'][k] for k in ('bytes','sha256')}==identity(e[path]),'CONFIG-RECORD-IDENTITY')
  calls=[(i,x) for i,x in enumerate(trace['events']) if x['frame']==inst['managed_constructor_frame'] and x['event']=='call' and x['function']=='ManagedAuthority.__init__']
  require(len(calls)==1,'CONFIG-CONSTRUCTOR-FRAME');i,call=calls[0]
  require(call['parent']==occ['parent_frame'],'CONFIG-CONSTRUCTOR-RECOVERY-PARENT')
  record=dict(copy.deepcopy(binding['record']),pointer='/config')
  constructor={'acquisition':record['acquisition'],'artifact':trace_path,**identity(e[trace_path]),'pointer':'/events/'+str(i),'frame':call['frame'],'parent':call['parent']}
  anchor={'context':name,'instance':copy.deepcopy(inst),'record':record,'configuration':copy.deepcopy(value),'constructor':constructor,
   'recovery_occurrence':occ['id'],'recovery_frame':occ['frame'],'recovery_parent':occ['parent_frame'],'recovery_call':copy.deepcopy(occ['call']),'recovery_completion':copy.deepcopy(occ['completion']),
   'predecessor_receipt':identity(basis['saved']),'reference_relation_ids':copy.deepcopy(binding['reference_relation_ids']),
   'getter_frame':None,'storage_assignment_frame':None,'copy_identity_observations':None,'underlying_connection_identity':None,
   'meaning':'Configuration values from the same validated recovery export and recorded managed instance. Constructor frame exists; input/storage/getter object identity and copy execution are not captured.'}
  rows.append({'context':name,'declaration':copy.deepcopy(cat),'validated_configuration_anchor':anchor,'getter_observations':None,'actual_getter_count':None,'classification':'UNKNOWN','multiplicity':None})
 return rows

def _check_rows(basis,submitted,expected):
 require(type(submitted) is list and len(submitted)==len(expected)==2,'CONFIG-CONTEXT-DOMAIN')
 for got,want in zip(submitted,expected):
  require(type(got) is dict and set(got)==set(want),'CONFIG-ROW-FIELDS');require(got['context']==want['context'],'CONFIG-CONTEXT-IDENTITY')
  a=got['validated_configuration_anchor'];b=want['validated_configuration_anchor'];require(type(a) is dict and set(a)==set(b),'CONFIG-ANCHOR-FIELDS')
  basis['fresh']['coverage'].config_value_type(basis['catalogue'],a['configuration']);same(a['configuration'],b['configuration'],'CONFIG-ANCHOR-VALUE')
  same(a,b,'CONFIG-ANCHOR-LINEAGE');same(got,want,'CONFIG-CONTEXT-CORRESPONDENCE')

def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CONFIG-SOURCE-CATALOGUE')
 d=data['prior_data']['prior_data'];fd=basis['fresh']['prior_data']['prior_data']
 for k in ('manager','authority'):require(d[k]==fd[k],'CONFIG-CANDIDATE-SOURCE:'+k)
 require(d['ctx']['c']==fd['ctx']['c'],'CONFIG-CANDIDATE-CONTEXT');same(d['ctx']['binding'],fd['ctx']['binding'],'CONFIG-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 rows=_rows(basis)
 if claims is not None:_check_rows(basis,claims,rows)
 return rows,basis

def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)

def derive_config(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);result=copy.deepcopy(basis['prior']);result['format']='I164-MANAGED-CONFIG-RETURN-CORRESPONDENCE-1'
 result['prior_binding_components']=result.pop('extension_components');result['prior_binding_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'CONFIG-DERIVATION-CONTEXT');context['config_return_correspondence']=copy.deepcopy(row)
 result['new_config_slice_limits']={'static_conditional_correspondence':True,'saved_getter_execution_evidence':'UNAVAILABLE','actual_getter_count':None,'copy_identity_observations':None,
  'source_copy_graph_domain':'ordinary builtin dict/list and immutable scalar leaves; not arbitrary hooks/subclasses','actual_CONFIG_is_flat_scalar':True,
  'constructor_input_is_not_storage_alias':True,'later_input_mutation_is_not_configuration_change_evidence':True,'internal_alias_preservation_required':True,'immutable_leaf_sharing_allowed':True,
  'validated_frontier_is_not_current_or_lifetime_state':True,'separate_observer_Client_state_call':True,'observer_frame':None,'missing_historical_producer_frames':True,'traced_invocations':18,
  'complete_repetition_coverage':False,'no_runtime_changes':True,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,
  'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return result

def constructed_projection(data,submitted_catalogue,case):
 """In-memory builtin constructed case; emitted graph retains alias topology.
 The input value is at constructor-copy evaluation, not a later caller value.
 """
 rows,basis=_checked(data,submitted_catalogue)
 require(type(case) is dict and set(case)=={'kind','context','anchor','premise','constructor_input_at_copy','stored','returned'},'CONFIG-CASE-FIELDS')
 require(case['kind']=='CONSTRUCTED-CONDITIONAL-CONFIG','CONFIG-CASE-NOT-EXECUTION');selected=[r for r in rows if r['context']==case['context']];require(len(selected)==1,'CONFIG-CASE-CONTEXT');anchor=selected[0]['validated_configuration_anchor']
 same(case['anchor'],anchor,'CONFIG-CASE-ANCHOR');c=basis['fresh']['coverage']
 for k in ('constructor_input_at_copy','stored','returned'):c.config_value_type(basis['catalogue'],case[k]);same(case[k],anchor['configuration'],'CONFIG-CASE-VALIDATED-VALUE')
 constructor=c.validate_copy_graph(c.copy_graph(case['constructor_input_at_copy'],case['stored']))
 projected=c.config_value_projection(basis['catalogue'],case['premise'],case['stored'],case['returned'])
 # With all three constructed objects alive, a new dict cannot be the original
 # caller dict either. This is conditional construction, not host identity proof.
 c.validate_copy_graph(c.copy_graph(case['constructor_input_at_copy'],case['returned']))
 return {'kind':'CONSTRUCTED-CONDITIONAL-CONFIG','context':case['context'],'anchor':copy.deepcopy(anchor),'constructor_copy':constructor,'getter_copy':projected,
  'constructed_graph':c.copy_graph(case['constructor_input_at_copy'],case['stored'],case['returned']),'runtime_observation':False}

def derive(root=ROOT):
 data=inputs(root);return derive_config(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-CONFIG-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'getter_runtime_evidence':'UNAVAILABLE','actual_admission':False,'complete_repetition_coverage':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
