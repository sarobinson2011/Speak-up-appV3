"""Mandatory callback-exception/stored-failure relation over the reviewed normal-callback chain.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 251922, 'sha256': '85fa719362b2cec22a8ea2ed4906aea983b2f6d955c09b27510e5bf7fbcfda95'}
PREDECESSOR_MANIFEST={'bytes':753872,'sha256':'5e86ced8e4e4f662472a95cb6e61aa59d50ce0b33e3cd425f7b8668c4c067a8e'}
PREDECESSOR_RECEIPT={'bytes':5337262,'sha256':'2523144c01a3bfa57d7e85b51ec3c907dab787ff23057bb4be5763ac9edc4548'}
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(ok,code):
 if not ok:raise ValueError(code)
def exact(value,code):
 stack=[(value,False)];active=set()
 while stack:
  node,leave=stack.pop();kind=type(node)
  if leave:active.remove(id(node));continue
  if kind is dict or kind is list:
   require(id(node) not in active,code+':CYCLE');active.add(id(node));stack.append((node,True))
   if kind is dict:
    for k,v in node.items():require(type(k) is str,code+':KEY-TYPE');stack.append((v,False))
   else:
    for v in node:stack.append((v,False))
  else:require(any(kind is t for t in (str,int,bool,float,type(None))),code+':VALUE-TYPE')
def same(a,b,code):exact(a,code);exact(b,code);require(enc(a)==enc(b),code)
def module(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def predecessor_root(root):
 root=Path(root);base=root/'retained/stored'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CALLBACK-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'CALLBACK-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'CALLBACK-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CALLBACK-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CALLBACK-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'CALLBACK-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CALLBACK-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'CALLBACK-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'CALLBACK-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_callback_stored_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_callback_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependencies(data):
 p=data['prior_module'];pd=data['prior_data'];return (p.catalogue(pd),*p.dependencies(pd))
def catalogue(data):return data['coverage'].compile_callback_failure(*sources(data)[:2],*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,sb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,sb)
 saved=(fresh['prior_root']/'results/correction/stored-failure-revocation.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'CALLBACK-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'stored_basis':sb,'stored_module':p,'verification':sb['verification']}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'CALLBACK-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  stored=row['stored_failure_revocation_correspondence'];token=row['token_registration_correspondence'];same(stored['instance_anchor'],token['instance_anchor'],'CALLBACK-VALIDATED-INSTANCE');same(stored['declaration']['source']['sources'],cat['source']['sources'],'CALLBACK-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(stored['instance_anchor']),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'normal_callback_relation_preserved':True,'failure_predecessors':copy.deepcopy(stored['failure_predecessors']),'guard_slot_premise':cat['source']['guard_slot_premise'],'selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','runtime_callback_cause_revocation_chain':None,'callback_exception_producer_history':None,'original_exception_observation':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(stored['separate_observer']),'outer_cleanup_complete':False,'gap':'No runtime callback/error/cause/finally/pop chain. Bare raise without stored error, control failures and full outer cleanup remain unexpanded.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'CALLBACK-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'CALLBACK-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'CALLBACK-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CALLBACK-EVIDENCE-TYPES');require(candidate==basis['evidence'],'CALLBACK-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'CALLBACK-CATALOGUE');exact(claims,'CALLBACK-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CALLBACK-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'CALLBACK-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'CALLBACK-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'CALLBACK-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CALLBACK-STORED-FAILURE-1';result['prior_stored_failure_components']=result.pop('extension_components');result['prior_stored_failure_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['callback_stored_failure_correspondence']=copy.deepcopy(row)
 result['new_callback_failure_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','selected_owner_continuity':'Explicit premise','guard_slot_error_continuity':'Explicit premise','callback_exception_producer_history':'UNAVAILABLE','physical_identity_or_inequality':None,'observer_join':None,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_callback(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _selected(basis,context):
 rows=[r for r in basis['prior']['contexts'] if r['context']==context];require(len(rows)==1,'CALLBACK-CONSTRUCTED-CONTEXT');return rows[0]
def failure_inputs(basis,context,invocation,token):return basis['stored_module'].failure_inputs(basis['stored_basis'],context,invocation,token)
def _failure(basis,case,token):
 route=case['failure_route'];require(route in ('handle','state'),'CALLBACK-FAILURE-ROUTE');p=case['failure_input'];require(type(p) is dict,'CALLBACK-FAILURE-INPUT');b=failure_inputs(basis,case['context'],case['invocation'],token);row=_selected(basis,case['context']);c=basis['fresh']['coverage'];cat=row['client_'+route+'_return_correspondence']['declaration']
 same(p.get('scope'),b[route+'_scope'],'CALLBACK-FAILURE-SCOPE');same(p.get('references'),b[route+'_references'],'CALLBACK-FAILURE-REFERENCES');require(p.get('occurrence')==b['child'] and p.get('callback')=='raises','CALLBACK-FAILURE-INVOCATION-RAISE');same(p.get('cleanup'),dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved'),'CALLBACK-NO-OPAQUE-CLEANUP-JOIN')
 if route=='state':result=c.client_state_projection(cat,p,{'scope':b['state_scope'],'state':row['client_state_return_correspondence']['validated_state_anchor']['validated_state']})
 else:
  validated=copy.deepcopy(p);validated['scope']=copy.deepcopy(b['handle_scope']);validated['references']=copy.deepcopy(b['handle_references']);result=c.client_handle_projection(cat,basis['verification'],p,validated)
 require(result['retained_original'] is True and result['completion'] in ('fixed-client-failure','unqualified-escape') and type(result['original_exception']) is dict,'CALLBACK-NO-VALIDATED-FAILURE');require(result['original_exception']['reference']==b['child']+'/error','CALLBACK-ERROR-OCCURRENCE');same(case['failure_result'],result,'CALLBACK-FAILURE-RESULT');return result
def _premises(basis,case):
 exact(case,'CALLBACK-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','failure_route','failure_input','failure_result','callback_error','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CALLBACK-STORED-FAILURE','CALLBACK-CONSTRUCTED-CASE')
 row=_selected(basis,case['context']);anchor=row['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CALLBACK-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'CALLBACK-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CALLBACK-TOKEN-INVOCATION')
 sb=basis['stored_basis'];token=sb['routes']['token_module']._construct_checked(sb['token_basis'],tc)['projection'];require(tc['owner_failure_none'] is False,'CALLBACK-SELECTED-NONNONE-SLICE');require(token['completion']=='unexpected-raise' and token['client_callback_completed_in_model'] is False and token['events'][-1]['stage']=='client-callback' and token['events'][-1]['outcome']=='raise','CALLBACK-TOKEN-FRONTIER')
 failure=_failure(basis,case,token);refs=token['reference_bindings'];scope=token['scope'];cat=basis['catalogue'];client=basis['fresh']['coverage'].callback_error_binding(cat,scope);same(case['callback_error'],client,'CALLBACK-CAUGHT-ERROR')
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','error':copy.deepcopy(failure['original_exception']),'child_operation':case['failure_input']['occurrence'],'route':case['failure_route'],'storage_source':copy.deepcopy(cat['source']['storage']),'guard_source':copy.deepcopy(cat['source']['guard']),'source':copy.deepcopy(cat['source']['sources']['entry']),'guard_slot_premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'physical_object_identity':None}
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_prefix':token,'failure_provenance':failure,'stored_error_binding':binding,'callback_error':client,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.callback_failure_projection(cat,case['projection'],v);c.validate_callback_failure_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Conditional caught callback exception, selected stored original at guard, invocation-qualified role references and selected-owner registry continuity. Not runtime history or physical object inequality.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'CALLBACK-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def constructed_normal_callback(data,submitted_catalogue,case):
 exact(case,'CALLBACK-PRIOR-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return basis['stored_module']._construct_checked(basis['stored_basis'],case)
def derive(root=ROOT):
 data=inputs(root);return derive_callback(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'CALLBACK-RECEIPT-BYTES');v=json.loads(saved);require(type(v) is dict and v.get('format')=='I164-CALLBACK-STORED-FAILURE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and 'callback_stored_failure_correspondence' in c and 'stored_failure_revocation_correspondence' in c for c in v['contexts']),'CALLBACK-MANDATORY-RELATIONS');require(saved==enc(derive(root)),'CALLBACK-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_callback_cause_revocation_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
