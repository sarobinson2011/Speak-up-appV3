"""Mandatory stored-failure rethrow-to-token-revocation over the reviewed normal-finalization chain.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 238369, 'sha256': '94ec72e419daf90b5b5d34b5c52af345d0bf6fb6325b96b887251274b877e542'}
PREDECESSOR_MANIFEST={'bytes': 690980, 'sha256': '5d3bd027372da6610ce1a05fec8fb75fcf19acb303b58692d61b038a5e6e1c4c'}
PREDECESSOR_RECEIPT={'bytes': 4348225, 'sha256': '6f2d1ac375017fd2f92923522aeba36defb89992d7fd071dd385e11d991d3c42'}
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
 root=Path(root);base=root/'retained/owner'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'STORED-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'STORED-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'STORED-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'STORED-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'STORED-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'STORED-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'STORED-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'STORED-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'STORED-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_stored_owner_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_stored_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def routes(data):
 owner=data['prior_data'];exit_=owner['prior_data'];token=exit_['prior_data'];status=token['prior_data'];state=status['prior_data'];client=state['prior_data']
 return {'token_module':exit_['prior_module'],'token_data':token,'state_module':status['prior_module'],'state_data':state,'client_module':state['prior_module'],'client_data':client,'handle_module':client['prior_module'],'handle_data':client['prior_data']}
def dependencies(data):
 r=routes(data);return r['token_module'].catalogue(r['token_data']),r['client_module'].catalogue(r['client_data']),r['state_module'].catalogue(r['state_data'])
def catalogue(data):return data['coverage'].compile_stored_failure(*sources(data),*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,ob=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,ob)
 saved=(fresh['prior_root']/'results/primary/owner-lock-finalization.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'STORED-VALIDATED-PREDECESSOR-RECEIPT')
 r=routes(fresh);_,authority,anchor,observations=r['handle_module'].sources(r['handle_data'])
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'owner_basis':ob,'token_basis':ob['exit_basis']['token_basis'],'routes':r,'verification':fresh['coverage'].handle_authentication(authority,anchor,observations)}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'STORED-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  token=row['token_registration_correspondence'];anchor=token['instance_anchor'];same(anchor,row['client_state_return_correspondence']['validated_state_anchor'],'STORED-VALIDATED-STATE-INSTANCE');same(token['declaration']['source']['entry'],cat['source']['sources']['entry'],'STORED-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(anchor),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'failure_predecessors':{k:{'declaration':copy.deepcopy(row['client_'+k+'_return_correspondence']['declaration']),'runtime_chain':None} for k in ('handle','state')},
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'runtime_stored_failure_chain':None,'original_exception_observation':None,'physical_reference_observation':None,'actual_invocation_count':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'separate_observer':copy.deepcopy(token['separate_observer']),'observer_join':None,
   'selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','guard_slot_premise':cat['source']['guard_slot_premise'],'outer_cleanup_complete':False,'gap':'No runtime storage/callback/rethrow/finally/pop chain. Other callback failures, outer cleanup, physical identity, custody and durability remain unexpanded/unestablished.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'STORED-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'STORED-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'STORED-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'STORED-EVIDENCE-TYPES');require(candidate==basis['evidence'],'STORED-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'STORED-CATALOGUE');exact(claims,'STORED-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'STORED-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'STORED-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'STORED-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'STORED-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-STORED-FAILURE-REVOCATION-1';result['prior_owner_finalization_components']=result.pop('extension_components');result['prior_owner_finalization_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['stored_failure_revocation_correspondence']=copy.deepcopy(row)
 result['new_stored_failure_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','selected_owner_continuity':'Explicit premise','guard_slot_error_continuity':'Explicit source-state premise, not intervening-history evidence','observer_join':None,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_stored(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _selected(basis,context):
 rows=[r for r in basis['prior']['contexts'] if r['context']==context];require(len(rows)==1,'STORED-CONSTRUCTED-CONTEXT');return rows[0]
def failure_inputs(basis,context,invocation,token):
 """Canonical reference correspondences, not physical identity observations."""
 row=_selected(basis,context);refs=token['reference_bindings'];scope=token['scope'];child=invocation+'/client-operation';state_scope={**copy.deepcopy(scope),'invocation':child}
 handle_scope=copy.deepcopy(row['client_handle_return_correspondence']['validated_scope']);handle_scope['instance']=copy.deepcopy(row['client_handle_return_correspondence']['instance_request_context'])
 def references(kind):
  sc=state_scope if kind=='state' else handle_scope;out={}
  for role in ('client','token','owner','session','manager'):
   out[role]={'scope':copy.deepcopy(sc),'symbol':refs[role]['symbol']}
   if kind=='state':out[role]['kind']=role+'-reference'
  for a,b in (('client.token','token'),('owners[token]','owner'),('owner.wrapper','session'),('session.managed','manager')):out[a]=copy.deepcopy(out[b])
  out['owner_failed']=False
  if kind=='state':
   for role in ('manager-result','data-result'):out[role]={'kind':'state-result-reference','scope':copy.deepcopy(sc),'symbol':child+'/'+role}
  return out
 return {'child':child,'state_scope':state_scope,'handle_scope':handle_scope,'state_references':references('state'),'handle_references':references('handle')}
def _failure(basis,case,token):
 route=case['failure_route'];require(route in ('handle','state'),'STORED-FAILURE-ROUTE');p=case['failure_input'];require(type(p) is dict,'STORED-FAILURE-INPUT');b=failure_inputs(basis,case['context'],case['invocation'],token);row=_selected(basis,case['context']);c=basis['fresh']['coverage'];cat=row['client_'+route+'_return_correspondence']['declaration']
 same(p.get('scope'),b[route+'_scope'],'STORED-FAILURE-SCOPE');same(p.get('references'),b[route+'_references'],'STORED-FAILURE-REFERENCES');require(p.get('occurrence')==b['child'] and p.get('callback')=='returns','STORED-FAILURE-INVOCATION-CALLBACK');same(p.get('cleanup'),dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved'),'STORED-NO-OPAQUE-CLEANUP-JOIN')
 if route=='state':
  anchor=row['client_state_return_correspondence']['validated_state_anchor'];result=c.client_state_projection(cat,p,{'scope':b['state_scope'],'state':anchor['validated_state']})
 else:
  # Finite arguments/outcomes are constructed premises. Scope/reference/error
  # expectations come from validated predecessor evidence and source checks.
  validated=copy.deepcopy(p);validated['scope']=copy.deepcopy(b['handle_scope']);validated['references']=copy.deepcopy(b['handle_references']);result=c.client_handle_projection(cat,basis['verification'],p,validated)
 require(result['retained_original'] is True and result['completion']=='fixed-client-failure' and type(result['original_exception']) is dict,'STORED-NO-VALIDATED-FAILURE')
 require(result['original_exception']['reference']==b['child']+'/error','STORED-ERROR-OCCURRENCE');same(case['failure_result'],result,'STORED-FAILURE-RESULT')
 return result
def _premises(basis,case):
 exact(case,'STORED-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','failure_route','failure_input','failure_result','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-STORED-FAILURE-REVOCATION','STORED-CONSTRUCTED-CASE')
 row=_selected(basis,case['context']);anchor=row['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'STORED-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'STORED-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'STORED-TOKEN-INVOCATION')
 token=basis['routes']['token_module']._construct_checked(basis['token_basis'],tc)['projection'];require(token['completion']=='stored-failure-exceptional-frontier' and token['client_callback_completed_in_model'] is True,'STORED-TOKEN-FRONTIER')
 failure=_failure(basis,case,token);refs=token['reference_bindings'];scope=token['scope'];cat=basis['catalogue']
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','error':copy.deepcopy(failure['original_exception']),'child_operation':case['failure_input']['occurrence'],'route':case['failure_route'],'storage_source':copy.deepcopy(cat['source']['storage']),'source':copy.deepcopy(cat['source']['sources']['entry']),'guard_slot_premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'physical_object_identity':None}
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_prefix':token,'failure_provenance':failure,'stored_error_binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.stored_failure_projection(cat,case['projection'],v);c.validate_stored_failure_projection(cat,case['projection'],v,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Finite constructed callback normal return and same stored original at guard, source-qualified error/owner/token references, explicit selected-owner registry continuity. Not observed history or arbitrary callback safety.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'STORED-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def derive(root=ROOT):
 data=inputs(root);return derive_stored(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'STORED-RECEIPT-BYTES');v=json.loads(saved);require(type(v) is dict and v.get('format')=='I164-STORED-FAILURE-REVOCATION-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and 'stored_failure_revocation_correspondence' in c for c in v['contexts']),'STORED-MANDATORY-RELATION');require(saved==enc(derive(root)),'STORED-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_stored_failure_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
