"""Mandatory state return-value correspondence over the reviewed binding chain.
All observations remain saved evidence. No application/session code executes.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 111127, 'sha256': '2fb641ae9776153bd0512d2863c081bd9fcb1a555e983a4d81703e742c1dcec1'}
CONFIG_MANIFEST={'bytes': 220312, 'sha256': '7d38b312dd7b615401935e4463098f8ba8aa2e01908e49d894ca1bf8703130c7'}
CONFIG_RECEIPT={'bytes': 805314, 'sha256': '7d82305c3eb4646b0d9072daec9d93186848ac2b8e1aa71d6ac6de77fbbf12a3'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,message):
 if not v:raise ValueError(message)
def same(a,b,message):require(enc(a)==enc(b),message)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'retained/config'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'STATE-ROOT-TYPE')
 p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'STATE-MANIFEST-TYPE');raw=p.read_bytes();require(identity(raw)==CONFIG_MANIFEST,'STATE-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen_dirs=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'STATE-UNDECLARED-DIRECTORY');seen_dirs.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'STATE-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen_dirs==dirs,'STATE-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'STATE-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);producer=root/'code/managed_coverage.py'
 require(stat.S_ISREG(producer.lstat().st_mode),'STATE-PRODUCER-TYPE');require(identity(producer.read_bytes())==PRODUCER_PIN,'STATE-PRODUCER-SOURCE')
 prior=module(base/'code/correspondence.py','_state_config_predecessor');data=prior.inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_state_managed_coverage')}

def inner(data):return data['prior_data']['prior_data']['prior_data']
def catalogue(data):
 d=inner(data);v=d['values'];g=d['guards'];obs=d['ctx']['c']['retained/candidate/compiler/managed_observations.py'];refs=d['reference_module'].reference_catalogue(d)
 return data['coverage'].compile_state_return(d['manager'],d['authority'],obs,v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],refs)

def _basis(data):
 # Fresh authority on every invocation; candidate values and returned trees
 # never act as validation expectations or replace the predecessor's evidence.
 fresh=inputs(data['root']);p=fresh['prior_module'];d=fresh['prior_data'];prior=p.derive_config(d,p.catalogue(d))
 saved=(fresh['prior_root']/'results/config-correspondence.json').read_bytes();require(identity(saved)==CONFIG_RECEIPT and enc(prior)==saved,'STATE-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'evidence':dict(inner(fresh)['ctx']['e']),'catalogue':catalogue(fresh)}

def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'STATE-EVIDENCE-BYTES')
 path='evidence/recovery-export-0.json';require(path in candidate,'STATE-MISSING-EXPORT');want=json.loads(basis['evidence'][path]);got=json.loads(candidate[path]);require(type(got) is dict and type(got.get('head')) is str,'STATE-MISSING-HEAD')
 expected=json.loads(bytes.fromhex(want['head']));supplied=json.loads(bytes.fromhex(got['head']))
 basis['fresh']['coverage'].state_value_compare(basis['catalogue'],supplied,expected)
 # Type/value comparison is prior to the inherited exact state/config/owner
 # and full evidence gates. Mutually consistent reports cannot be authority.
 binding_module=basis['fresh']['prior_data']['prior_module']
 binding_module._compare_evidence(basis['evidence'],candidate,'binding')

def _rows(basis):
 rows=[];cat=basis['catalogue'];e=basis['evidence'];path='evidence/recovery-export-0.json';export=json.loads(e[path]);raw=bytes.fromhex(export['head']);state=json.loads(raw)
 trace_path='evidence/execution-trace.json';events=json.loads(e[trace_path])['events'];hand_path='evidence/client-handoff.json';hands=json.loads(e[hand_path]);require(type(hands) is list and len(hands)==1,'STATE-OBSERVER-RECORD')
 for context in basis['prior']['contexts']:
  name=context['context'];hb=context['hf01_evidence_binding'];config=context['config_return_correspondence']['validated_configuration_anchor'];binding=context['binding_return_correspondence']['validated_binding_anchor'];inst=hb['instance'];occ=hb['occurrence'];record=hb['head_record']
  same(cat['inherited_head'],hb['head_declaration'],'STATE-HEAD-DECLARATION-JOIN');same(config['instance'],inst,'STATE-CONFIG-INSTANCE');same(binding['instance'],inst,'STATE-BINDING-INSTANCE')
  same(config['configuration'],export['config'],'STATE-CONFIG-JOIN');same(state['binding'],inst['binding'],'STATE-INSTANCE-BINDING')
  same(record,binding['record'],'STATE-HEAD-RECORD-JOIN');require(record['artifact']==path and record['pointer']=='/head','STATE-HEAD-RECORD')
  require({k:record[k] for k in ('bytes','sha256')}==identity(e[path]) and record['acquisition']==occ['call']['acquisition'],'STATE-HEAD-IDENTITY')
  anchor={'context':name,'instance':copy.deepcopy(inst),'record':copy.deepcopy(record),'decoded_state_identity':identity(raw),'validated_state':copy.deepcopy(state),
   'configuration_record':copy.deepcopy(config['record']),'recovery_occurrence':occ['id'],'recovery_frame':occ['frame'],'recovery_parent':occ['parent_frame'],'recovery_call':copy.deepcopy(occ['call']),'recovery_completion':copy.deepcopy(occ['completion']),
   'reference_relation_ids':copy.deepcopy(binding['reference_relation_ids']),'predecessor_receipt':identity(basis['saved']),
   'meaning':'Same validated recovery frontier, not the time or value of an unobserved later state dispatch. Conditional mapping only.'}
  source_calls=[{'frame':x['frame'],'parent':x['parent'],'function':x['function'],'record':{'acquisition':record['acquisition'],'artifact':trace_path,**identity(e[trace_path]),'pointer':'/events/'+str(i)}} for i,x in enumerate(events) if x['event']=='call' and x['function'] in ('ManagedAuthority.state','ManagedAuthority._run','Authority.state')]
  observer={'kind':'explicit-observer-call','id':record['acquisition'].removeprefix('sha256:')+':'+name+':observer-state:0','record':{'acquisition':record['acquisition'],'artifact':hand_path,**identity(e[hand_path]),'pointer':'/0/state'},
   'value':copy.deepcopy(hands[0]['state']),'caller':hands[0]['observer_call_site'],'frame':None,'parent_frame':None,'joins_to_three_return_links':None,'meaning':'Retained separate Client.state observation; no invented underlying, run or wrapper frame/value edge.'}
  links=[{'declaration':d['id'],'conditional_value_at_validated_frontier':copy.deepcopy(state),'source_origin':copy.deepcopy(d['origin']),'observed_value':None,'frame':None,'object_reference_observed':None} for d in cat['declarations']]
  rows.append({'context':name,'declaration':copy.deepcopy(cat),'validated_state_anchor':anchor,'conditional_links':links,'runtime_links':None,'unjoined_trace_calls':source_calls,'separate_observer':observer,
   'actual_call_count':None,'classification':'UNKNOWN','multiplicity':None,'gap':'No captured backend-state/result-assignment/wrapper-return chain. Source and recorded value agreement do not establish object identity or actual execution.'})
 return rows

def _check_rows(basis,submitted,expected):
 require(type(submitted) is list and len(submitted)==len(expected)==2,'STATE-CONTEXT-DOMAIN')
 for got,want in zip(submitted,expected):
  require(type(got) is dict and set(got)==set(want) and got['context']==want['context'],'STATE-CONTEXT-FIELDS');a=got['validated_state_anchor'];b=want['validated_state_anchor']
  require(type(a) is dict and set(a)==set(b),'STATE-ANCHOR-FIELDS');c=basis['fresh']['coverage'];c.state_value_compare(basis['catalogue'],a['validated_state'],b['validated_state']);same(a,b,'STATE-ANCHOR-LINEAGE')
  links=got['conditional_links'];require(type(links) is list and len(links)==len(want['conditional_links']),'STATE-LINK-COVERAGE')
  for row,wr in zip(links,want['conditional_links']):
   require(type(row) is dict and set(row)==set(wr) and row['declaration']==wr['declaration'],'STATE-LINK-FIELDS');c.state_value_compare(basis['catalogue'],row['conditional_value_at_validated_frontier'],b['validated_state']);same(row,wr,'STATE-LINK-CORRESPONDENCE')
  same(got,want,'STATE-CONTEXT-CORRESPONDENCE')

def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'STATE-SOURCE-CATALOGUE');d=inner(data);fd=inner(basis['fresh'])
 for k in ('manager','authority'):require(d[k]==fd[k],'STATE-CANDIDATE-SOURCE:'+k)
 require(d['ctx']['c']==fd['ctx']['c'],'STATE-CANDIDATE-CONTEXT');same(d['ctx']['binding'],fd['ctx']['binding'],'STATE-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence);rows=_rows(basis)
 if claims is not None:_check_rows(basis,claims,rows)
 return rows,basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def derive_state(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);result=copy.deepcopy(basis['prior']);result['format']='I164-MANAGED-STATE-RETURN-CORRESPONDENCE-1'
 result['prior_config_components']=result.pop('extension_components');result['prior_config_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'STATE-DERIVATION-CONTEXT');context['state_return_correspondence']=copy.deepcopy(row)
 result['new_state_slice_limits']={'static_conditional_correspondence':True,'saved_three_link_execution_chain':'UNAVAILABLE','actual_state_call_count':None,'physical_result_identity':None,'reference_forwarding_is_source_semantics':True,'equal_contents_establish_identity':False,
  'no_new_HEAD_authentication_or_ingestion_rule':True,'no_wrapper_copy':True,'separate_observer_Client_state_call':True,'observer_frame':None,'missing_state_ingest_assignment_and_historical_frames':True,'traced_invocations':18,
  'validated_frontier_is_not_current_or_lifetime_state':True,'complete_repetition_coverage':False,'no_runtime_changes':True,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,
  'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return result

def reference_scope(anchor):
 return {'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence']}
def constructed_projection(data,submitted_catalogue,case):
 rows,basis=_checked(data,submitted_catalogue);require(type(case) is dict and set(case)=={'kind','context','anchor','projection'},'STATE-CASE-FIELDS');require(case['kind']=='CONSTRUCTED-CONDITIONAL-STATE','STATE-CASE-NOT-EXECUTION')
 found=[r for r in rows if r['context']==case['context']];require(len(found)==1,'STATE-CASE-CONTEXT');anchor=found[0]['validated_state_anchor'];same(case['anchor'],anchor,'STATE-CASE-ANCHOR')
 projection=case['projection'];require(type(projection) is dict and type(projection.get('live_reference')) is dict,'STATE-CASE-REFERENCE');same(projection['live_reference'].get('scope'),reference_scope(anchor),'STATE-CASE-REFERENCE-SCOPE')
 result=basis['fresh']['coverage'].state_value_projection(basis['catalogue'],projection,anchor['validated_state'])
 return {'kind':'CONSTRUCTED-CONDITIONAL-STATE','context':case['context'],'anchor':copy.deepcopy(anchor),'projection':result,'runtime_observation':False}
def derive(root=ROOT):
 data=inputs(root);return derive_state(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-STATE-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'runtime_state_chain':'UNAVAILABLE','actual_admission':False,'complete_repetition_coverage':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
