"""Mandatory client handle forwarding over the reviewed manager-return chain.
All observations remain saved evidence. No application/session code executes.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 153726, 'sha256': '80caea048af5946a39e01d0f30b0e6ded7509684d67ce59b5fcff3cf224d2213'}
HANDLE_MANIFEST={'bytes': 276308, 'sha256': '71a7cb2823f6b35bb0fa3bcf87b677d07d076f98f8d63ed70c58538c94ae1567'}
HANDLE_RECEIPT={'bytes': 1156238, 'sha256': 'c840ab87c77c6900c457f39d029f51175546225b8af69e0fb6262bfcc52276ad'}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(v,message):
 if not v:raise ValueError(message)
def same(a,b,message):require(enc(a)==enc(b),message)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def predecessor_root(root):
 root=Path(root);base=root/'original/retained/handle'
 for p in (root,root/'original',root/'original/retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CLIENT-ROOT-TYPE')
 p=base/'MANIFEST.json';require(stat.S_ISREG(p.lstat().st_mode),'CLIENT-MANIFEST-TYPE');raw=p.read_bytes();require(identity(raw)==HANDLE_MANIFEST,'CLIENT-PREDECESSOR-MANIFEST')
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
 prior=module(base/'code/correspondence.py','_client_handle_predecessor');data=prior.inputs(base)
 return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':data,'coverage':module(producer,'_client_managed_coverage')}

def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):
 c=inner(data)['ctx']['c'];return c['retained/launcher/code/lab_bootstrap.py'],c['code/prospective_entry.py']
def catalogue(data):
 p=data['prior_module'];pd=data['prior_data'];return data['coverage'].compile_client_handle(*sources(data),p.catalogue(pd),inner(data)['ctx']['binding'])
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];cat=p.catalogue(pd);prior=p.derive_handle(pd,cat)
 saved=(fresh['prior_root']/'results/handle-correspondence.json').read_bytes();require(identity(saved)==HANDLE_RECEIPT and enc(prior)==saved,'CLIENT-PREDECESSOR-RECEIPT')
 _,authority,anchor,observations=p.sources(pd)
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':fresh['coverage'].compile_client_handle(*sources(fresh),cat,inner(fresh)['ctx']['binding']),'evidence':dict(inner(fresh)['ctx']['e']),'verification':fresh['coverage'].handle_authentication(authority,anchor,observations)}
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CLIENT-EVIDENCE-TYPES')
 # Reuse manager journal and full binding/source-evidence gates with the SAME
 # freshly validated predecessor basis, not mutually consistent candidate reports.
 fresh=basis['fresh'];fresh['prior_module']._compare_evidence({'fresh':fresh['prior_data'],'evidence':basis['evidence']},candidate)
 for n in ('evidence/execution-trace.json','evidence/client-handoff.json','evidence/smoke.stdout','evidence/smoke.stderr'):
  require(n in candidate and candidate[n]==basis['evidence'][n],'CLIENT-VALIDATED-EVIDENCE:'+n)
def _rows(basis):
 cat=basis['catalogue'];e=basis['evidence'];events=json.loads(e['evidence/execution-trace.json'])['events'];rows=[]
 for context in basis['prior']['contexts']:
  m=context['handle_return_correspondence'];name=context['context'];scope=copy.deepcopy(m['validated_scope'])
  records=[]
  for i,v in enumerate(events):
   if v['event']=='call' and v['function'] in ('Client.handle','ManagedSession.handle','_dispatch'):
    records.append({'record':{'acquisition':scope['acquisition'],'artifact':'evidence/execution-trace.json',**identity(e['evidence/execution-trace.json']),'pointer':'/events/'+str(i)},'event':copy.deepcopy(v),'route':'requires supported arguments; _dispatch alone does not establish handle'})
  rows.append({'context':name,'declaration':copy.deepcopy(cat),'validated_scope':scope,'instance_request_context':copy.deepcopy(m['instance_request_context']),'manager_predecessor_receipt':identity(basis['saved']),
   'manager_relation':copy.deepcopy(m),'boundary_binding':identity(enc(inner(basis['fresh'])['ctx']['binding'])),
   'captured_forwarding_calls':records,'runtime_forwarding_links':None,'actual_client_handle_call_count':None,'packet_observation':None,'inject_observation':{'observed':False,'value':None},'reference_identity_observations':None,'original_exception_observation':None,'fixed_failure_observation':None,
   'saved_general_output':{n:{'acquisition':scope['acquisition'],'artifact':'evidence/smoke.'+n,**identity(e['evidence/smoke.'+n])} for n in ('stdout','stderr')},
   'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'gap':'No captured client/launcher handle return chain. Source defaults, conditional references and constructed exceptions are not runtime values or records; the separate observer Client.state call is not a forwarding frame.'})
 return rows
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CLIENT-SOURCE-CATALOGUE');d=inner(data);fd=inner(basis['fresh'])
 require(sources(data)==sources(basis['fresh']),'CLIENT-CANDIDATE-SOURCE');require(d['ctx']['c']==fd['ctx']['c'],'CLIENT-CANDIDATE-CONTEXT');same(d['ctx']['binding'],fd['ctx']['binding'],'CLIENT-CANDIDATE-BINDING')
 _compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence);rows=_rows(basis)
 if claims is not None:
  require(type(claims) is list and len(claims)==len(rows)==2,'CLIENT-CONTEXT-DOMAIN')
  for actual,expected in zip(claims,rows):same(actual,expected,'CLIENT-CONTEXT-CORRESPONDENCE')
 return rows,basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def derive_client(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);result=copy.deepcopy(basis['prior']);result['format']='I164-CLIENT-HANDLE-RETURN-CORRESPONDENCE-2'
 result['prior_handle_components']=result.pop('extension_components');result['prior_handle_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for context,row in zip(result['contexts'],rows):require(context['context']==row['context'],'CLIENT-DERIVATION-CONTEXT');context['client_handle_return_correspondence']=copy.deepcopy(row)
 result['new_client_slice_limits']={'static_conditional_correspondence':True,'runtime_chain':'UNAVAILABLE','actual_call_count':None,'constructed_cases_not_evidence':True,'exact_response_bytes':True,'best_effort_failure_record_not_guaranteed':True,'outside_catch_and_interruption_limits_preserved':True,'physical_identity':None,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}
 return result
def derive(root=ROOT):
 data=inputs(root);return derive_client(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes and saved==enc(derive(root)),'STALE-OR-ALTERED-CLIENT-CORRESPONDENCE')
 return {'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(saved),'runtime_client_handle_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))

