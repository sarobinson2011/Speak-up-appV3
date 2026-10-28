"""Mandatory handle return-value correspondence over the reviewed binding chain.
All observations remain saved evidence. No application/session code executes.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 128258, 'sha256': 'b7108d38407c11f1e09f91ba56d29402cc0a900076a45d5edacd236856bb3bef'}
STATE_MANIFEST={'bytes': 250218, 'sha256': 'ca6d7832a1bbcec72acf4730ff5f7c267f9c65ff110b1c3807cc10193c1558fd'}
STATE_RECEIPT={'bytes': 942948, 'sha256': '7b5f2d1286fd6c3d02a16c15f42da0c3e6491c5582beb882f64115a691bd0186'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,message):
 if not v:raise ValueError(message)
def same(a,b,message):require(enc(a)==enc(b),message)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'retained/state'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'HANDLE-ROOT-TYPE')
 p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'HANDLE-MANIFEST-TYPE');raw=p.read_bytes();require(identity(raw)==STATE_MANIFEST,'HANDLE-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen_dirs=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'HANDLE-UNDECLARED-DIRECTORY');seen_dirs.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'HANDLE-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen_dirs==dirs,'HANDLE-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'HANDLE-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);producer=root/'code/managed_coverage.py'
 require(stat.S_ISREG(producer.lstat().st_mode),'HANDLE-PRODUCER-TYPE');require(identity(producer.read_bytes())==PRODUCER_PIN,'HANDLE-PRODUCER-SOURCE')
 prior=module(base/'code/correspondence.py','_handle_state_predecessor');data=prior.inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_handle_managed_coverage')}

def inner(data):return data['prior_data']['prior_data']['prior_data']['prior_data']
def sources(data):
 d=inner(data);c=d['ctx']['c']
 return d['manager'],d['authority'],c['retained/launcher/sources/anchor.py'],c['retained/candidate/compiler/managed_observations.py']
def catalogue(data):
 d=inner(data);g=d['guards'];v=d['values']
 return data['coverage'].compile_handle_return(*sources(data),v['candidate/managed-route/model.json'],v['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],d['reference_module'].reference_catalogue(d))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];prior=p.derive_state(pd,p.catalogue(pd))
 saved=(fresh['prior_root']/'results/state-correspondence.json').read_bytes();require(identity(saved)==STATE_RECEIPT and enc(prior)==saved,'HANDLE-PREDECESSOR-RECEIPT')
 raw,authority,anchor,observations=sources(fresh)
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'verification':fresh['coverage'].handle_authentication(authority,anchor,observations)}
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'HANDLE-EVIDENCE-TYPES')
 expected=basis['evidence'];path='evidence/recovery-export-0.json';require(path in candidate,'HANDLE-MISSING-EXPORT')
 want=json.loads(expected[path]);got=json.loads(candidate[path]);require(type(got) is dict and 'journal' in got,'HANDLE-MISSING-JOURNAL')
 # The validated predecessor, never mutually consistent submitted reports,
 # supplies the exact request/response rows. No row invented for an empty journal.
 same(got['journal'],want['journal'],'HANDLE-VALIDATED-JOURNAL')
 hf=inner(basis['fresh']);bm=basis['fresh']['prior_data']['prior_data']['prior_module']
 bm._compare_evidence(expected,candidate,'binding')
def _rows(basis):
 e=basis['evidence'];path='evidence/recovery-export-0.json';export=json.loads(e[path]);trace='evidence/execution-trace.json';events=json.loads(e[trace])['events'];cat=basis['catalogue'];rows=[]
 for context in basis['prior']['contexts']:
  state=context['state_return_correspondence']['validated_state_anchor'];config=context['config_return_correspondence']['validated_configuration_anchor'];instance=state['instance'];name=context['context']
  same(instance,config['instance'],'HANDLE-INSTANCE-JOIN');same(config['configuration'],export['config'],'HANDLE-CONFIG-JOIN')
  binding={'binding':instance['binding'],'pilot':export['config']['pilot'],'session':export['config']['session']}
  scope={'context':name,'acquisition':state['record']['acquisition'],'instance':copy.deepcopy(instance),'recovery_frontier':state['recovery_occurrence']}
  records=[]
  for i,j in enumerate(export['journal']):
   require(type(j) is list and len(j)==3 and type(j[0]) is str and type(j[1]) is str and (j[2] is None or type(j[2]) is str),'HANDLE-JOURNAL-ROW')
   packet={'bytes_hex':j[1]};basis['verification']['exact_bytes'](packet);response=None if j[2] is None else {'bytes_hex':j[2]}
   pair=None if response is None else basis['fresh']['coverage'].handle_pair(cat,basis['verification'],packet,response,binding)
   if pair is not None:same(pair['request']['challenge'],j[0],'HANDLE-JOURNAL-CHALLENGE')
   records.append({'id':scope['acquisition']+':'+name+':journal:'+str(i),'record':{'acquisition':scope['acquisition'],'artifact':path,**identity(e[path]),'pointer':'/journal/'+str(i)},'challenge':j[0],'packet':copy.deepcopy(packet),'response':copy.deepcopy(response),'pair':pair,'inject':{'observed':False,'value':None},'call_or_return_frame':None,'meaning':'Retained journal occurrence, not an invented call or return observation.'})
  calls=[{'record':{'acquisition':scope['acquisition'],'artifact':trace,**identity(e[trace]),'pointer':'/events/'+str(i)},'event':copy.deepcopy(x)} for i,x in enumerate(events) if x['event']=='call' and (x['function'] in ('ManagedAuthority.handle','Authority.handle') or x['function']=='ManagedAuthority._run' and x.get('arguments',{}).get('method')=='handle')]
  rows.append({'context':name,'declaration':copy.deepcopy(cat),'validated_scope':scope,'validated_state_anchor':copy.deepcopy(state),'instance_request_context':binding,'predecessor_receipt':identity(basis['saved']),
   'saved_journal_records':records,'saved_journal_rows':len(records),'captured_handle_call_records':calls,'runtime_links':None,'packet_observation':None,'inject_observation':{'observed':False,'value':None},'underlying_response_observation':None,'run_result_observation':None,'wrapper_return_observation':None,
   'actual_handle_call_count':None,'classification':'UNKNOWN','multiplicity':None,'gap':'No captured handle return chain in this saved smoke; empty journal is not lifetime zero calls or proof of nonexecution. A record or equal bytes does not supply missing frames, identities or inject.'})
 return rows
def _check_rows(basis,submitted,expected):
 require(type(submitted) is list and len(submitted)==len(expected)==2,'HANDLE-CONTEXT-DOMAIN')
 for a,b in zip(submitted,expected):
  require(type(a) is dict and set(a)==set(b) and a['context']==b['context'],'HANDLE-CONTEXT-FIELDS')
  same(a['declaration'],b['declaration'],'HANDLE-DECLARATIONS');same(a['validated_scope'],b['validated_scope'],'HANDLE-INSTANCE-LINEAGE');same(a['saved_journal_records'],b['saved_journal_records'],'HANDLE-JOURNAL-CORRESPONDENCE');same(a,b,'HANDLE-CONTEXT-CORRESPONDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'HANDLE-SOURCE-CATALOGUE');d=inner(data);fd=inner(basis['fresh'])
 require(sources(data)==sources(basis['fresh']),'HANDLE-CANDIDATE-SOURCE');require(d['ctx']['c']==fd['ctx']['c'],'HANDLE-CANDIDATE-CONTEXT');same(d['ctx']['binding'],fd['ctx']['binding'],'HANDLE-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence);rows=_rows(basis)
 if claims is not None:_check_rows(basis,claims,rows)
 return rows,basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def derive_handle(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);result=copy.deepcopy(basis['prior']);result['format']='I164-MANAGED-HANDLE-RETURN-CORRESPONDENCE-1'
 result['prior_state_components']=result.pop('extension_components');result['prior_state_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'HANDLE-DERIVATION-CONTEXT');context['handle_return_correspondence']=copy.deepcopy(row)
 result['new_handle_slice_limits']={'static_conditional_correspondence':True,'actual_handle_chain':'UNAVAILABLE','actual_handle_call_count':None,'empty_journal_not_lifetime_zero':True,'exact_response_bytes_preserved':True,'decoded_reencoding_not_substituted':True,'inject_unknown_not_None':True,'authentication_fixture_not_runtime':True,'physical_result_identity':None,'distinct_occurrences_not_merged':True,'complete_repetition_coverage':False,
  'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}
 return result
def derive(root=ROOT):
 data=inputs(root);return derive_handle(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-HANDLE-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'runtime_handle_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))

