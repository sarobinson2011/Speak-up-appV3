"""Mandatory control-callback exception-to-finally/removal correspondence. Saved inputs only."""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 275943, 'sha256': '4c41e45bf4472168c7ddcf418834c564301b8251cde18e17e465594e7c81dd06'}
PREDECESSOR_MANIFEST={'bytes': 890147, 'sha256': '8e4139615c328790f34857737e03cbea4295d25bc09d9d34389ebf6056716589'}
PREDECESSOR_RECEIPT={'bytes': 6854670, 'sha256': '30dfb6840ab7e3bdab7bc812ab76923dd3380002149ec05a6423f54e9920ee89'}
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
 root=Path(root);base=root/'retained/bare'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CONTROL-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'CONTROL-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'CONTROL-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CONTROL-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CONTROL-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'CONTROL-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CONTROL-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'CONTROL-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'CONTROL-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_bare_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_control_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependencies(data):
 p=data['prior_module'];pd=data['prior_data'];return (p.catalogue(pd),*p.dependencies(pd))
def catalogue(data):return data['coverage'].compile_control_exception(*sources(data)[:2],*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,bb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,bb)
 saved=(fresh['prior_root']/'results/primary/callback-bare-rethrow.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'CONTROL-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'bare_basis':bb,'bare_module':p,'stored_basis':bb['stored_basis']}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'CONTROL-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  bare=row['callback_bare_rethrow_correspondence'];token=row['token_registration_correspondence'];same(bare['instance_anchor'],token['instance_anchor'],'CONTROL-VALIDATED-INSTANCE');same(bare['declaration']['source']['sources'],cat['source']['sources'],'CONTROL-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(token['instance_anchor']),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'reviewed_relations_preserved':copy.deepcopy(cat['preserved_relations']),'selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','owner_failure_guard_applicable':False,'client_handler_applicable':False,'runtime_control_exception_revocation_chain':None,'control_exception_producer_history':None,'exception_chain_observation':None,'prior_failure_storage_history':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(bare['separate_observer']),'outer_cleanup_complete':False,'gap':'No runtime control callback/error/finally/pop chain or existing cause/context observations. Control constructor failures and full outer cleanup remain unexpanded.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'CONTROL-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'CONTROL-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'CONTROL-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CONTROL-EVIDENCE-TYPES');require(candidate==basis['evidence'],'CONTROL-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'CONTROL-CATALOGUE');exact(claims,'CONTROL-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CONTROL-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'CONTROL-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'CONTROL-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'CONTROL-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CONTROL-EXCEPTION-CORRESPONDENCE-1';result['prior_callback_bare_components']=result.pop('extension_components');result['prior_callback_bare_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['control_exception_revocation_correspondence']=copy.deepcopy(row)
 result['new_control_exception_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','selected_owner_continuity':'Explicit premise','owner_failure_guard_applicable':False,'subsequent_client_handler_applicable':False,'control_exception_producer_history':'UNAVAILABLE','existing_cause_context_suppression':'UNKNOWN','physical_identity_or_inequality':None,'observer_join':None,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_control(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'CONTROL-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','control_error','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CONTROL-EXCEPTION','CONTROL-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'CONTROL-CONSTRUCTED-CONTEXT');anchor=rows[0]['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CONTROL-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'CONTROL-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CONTROL-TOKEN-INVOCATION')
 sb=basis['stored_basis'];token=sb['routes']['token_module']._construct_checked(sb['token_basis'],tc)['projection'];require(tc['control_present'] is True and token['registration_completed_in_model'] is True and token['completion']=='unexpected-raise' and token['control_callback_completed_in_model'] is False and token['client_callback_completed_in_model'] is False and token['events'][-1]['stage']=='control-callback' and token['events'][-1]['outcome']=='raise','CONTROL-TOKEN-FRONTIER')
 refs=token['reference_bindings'];scope=token['scope'];error=basis['fresh']['coverage'].control_exception_binding(basis['catalogue'],scope);same(case['control_error'],error,'CONTROL-CALLBACK-ERROR')
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_inputs':copy.deepcopy(tc['projection']),'token_prefix':token,'control_error':error,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.control_exception_projection(cat,case['projection'],v);c.validate_control_exception_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Selected control callback raises after control construction, under conditional selected-owner continuity. No client handler or owner.failure guard is selected. Existing exception chain/history remain unknown; role identity is not runtime object identity.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'CONTROL-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 exact(case,'CONTROL-PRIOR-CONSTRUCTED-INPUT');require(type(branch) is str and branch in ('bare','stored-client','stored-normal','normal-token'),'CONTROL-PRIOR-BRANCH');_,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def _construct_prior(basis,branch,case):
 exact(case,'CONTROL-PRIOR-CONSTRUCTED-INPUT');bb=basis['bare_basis'];sb=basis['stored_basis']
 if branch=='bare':return basis['bare_module']._construct_checked(bb,case)
 if branch=='stored-client':return bb['callback_module']._construct_checked(bb['callback_basis'],case)
 if branch=='stored-normal':return bb['callback_basis']['stored_module']._construct_checked(sb,case)
 if branch=='normal-token':return sb['routes']['token_module']._construct_checked(sb['token_basis'],case)
 raise ValueError('CONTROL-PRIOR-BRANCH')
def derive(root=ROOT):
 data=inputs(root);return derive_control(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'CONTROL-RECEIPT-BYTES');v=json.loads(saved);required={'control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'}
 require(type(v) is dict and v.get('format')=='I164-CONTROL-EXCEPTION-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and required<=set(c) for c in v['contexts']),'CONTROL-MANDATORY-RELATIONS');require(saved==enc(derive(root)),'CONTROL-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_control_exception_revocation_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
