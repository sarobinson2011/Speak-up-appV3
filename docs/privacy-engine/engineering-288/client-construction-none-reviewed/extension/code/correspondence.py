"""Mandatory client-construction exact-None handler-to-finally/removal correspondence. Saved inputs only."""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 307101, 'sha256': 'a879216a176955cc60c76150f1bdc2bfd7bff7b2dfab3b3340361fbe5cb6b2ab'}
PREDECESSOR_MANIFEST={'bytes': 1034275, 'sha256': '6c2b8a3bf2600bff776eeaec35a91653f8b39118d0c6172152cb392fa33115cb'}
PREDECESSOR_RECEIPT={'bytes': 8000877, 'sha256': 'd8a46dbf6aa29299a4a96a4c0132af217c9093e165c49409797112556f40b518'}
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
 root=Path(root);base=root/'retained/control-construction'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CLIENT-CONSTRUCTION-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'CLIENT-CONSTRUCTION-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'CLIENT-CONSTRUCTION-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CLIENT-CONSTRUCTION-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CLIENT-CONSTRUCTION-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'CLIENT-CONSTRUCTION-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CLIENT-CONSTRUCTION-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'CLIENT-CONSTRUCTION-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'CLIENT-CONSTRUCTION-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_control_construction_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_client_construction_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependencies(data):
 p=data['prior_module'];pd=data['prior_data'];return (p.catalogue(pd),*p.dependencies(pd))
def catalogue(data):return data['coverage'].compile_client_construction(*sources(data)[:2],*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,bb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,bb)
 saved=(fresh['prior_root']/'results/primary/control-construction.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'CLIENT-CONSTRUCTION-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'construction_basis':bb,'construction_module':p,'stored_basis':bb['stored_basis']}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'CLIENT-CONSTRUCTION-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  prior=row['control_construction_revocation_correspondence'];token=row['token_registration_correspondence'];same(prior['instance_anchor'],token['instance_anchor'],'CLIENT-CONSTRUCTION-VALIDATED-INSTANCE');same(prior['declaration']['source']['sources'],cat['source']['sources'],'CLIENT-CONSTRUCTION-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(token['instance_anchor']),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'reviewed_relations_preserved':copy.deepcopy(cat['preserved_relations']),'prefix_variants':['control-absent','control-construction-and-callback-completed-normally'],'guard_slot_continuity':'Explicit same-owner exact-None premise; not historical absence of storage','selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','client_handler_applicable':True,'construction_completed':False,'completed_client_object_reference':None,'client_callback_execution':False,'earlier_control_execution':'Conditional on selected validated prefix; no new runtime observation','constructor_substep_history':None,'runtime_client_construction_revocation_chain':None,'client_construction_producer_history':None,'exception_chain_observation':None,'prior_failure_storage_history':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(prior['separate_observer']),'outer_cleanup_complete':False,'gap':'No runtime Client construction/error/handler/bare-rethrow/pop chain or constructor progress. Non-None constructor handler branch and full outer cleanup remain unexpanded.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'CLIENT-CONSTRUCTION-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'CLIENT-CONSTRUCTION-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'CLIENT-CONSTRUCTION-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CLIENT-CONSTRUCTION-EVIDENCE-TYPES');require(candidate==basis['evidence'],'CLIENT-CONSTRUCTION-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'CLIENT-CONSTRUCTION-CATALOGUE');exact(claims,'CLIENT-CONSTRUCTION-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'CLIENT-CONSTRUCTION-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'CLIENT-CONSTRUCTION-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'CLIENT-CONSTRUCTION-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'CLIENT-CONSTRUCTION-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CLIENT-CONSTRUCTION-NONE-CORRESPONDENCE-1';result['prior_control_construction_components']=result.pop('extension_components');result['prior_control_construction_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['client_construction_none_correspondence']=copy.deepcopy(row)
 result['new_client_construction_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','guard_slot_continuity':'Explicit same-owner exact-None premise','selected_owner_continuity':'Explicit premise','construction_completion_established':False,'client_callback_execution_established':False,'earlier_control_progress':'Preserve selected validated prefix separately','existing_cause_context_suppression':'UNKNOWN','physical_identity_or_inequality':None,'observer_join':None,'outer_cleanup_complete':False,'non_none_constructor_branch_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_client_construction(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'CLIENT-CONSTRUCTION-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','construction_error','none_guard_binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','CLIENT-CONSTRUCTION-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'CLIENT-CONSTRUCTION-CONSTRUCTED-CONTEXT');anchor=rows[0]['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CLIENT-CONSTRUCTION-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'CLIENT-CONSTRUCTION-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CLIENT-CONSTRUCTION-TOKEN-INVOCATION')
 sb=basis['stored_basis'];token=sb['routes']['token_module']._construct_checked(sb['token_basis'],tc)['projection'];require(tc['owner_failure_none'] is True,'CLIENT-CONSTRUCTION-SELECTED-NONE-SLICE');require(token['registration_completed_in_model'] is True and token['completion']=='unexpected-raise' and token['client_callback_completed_in_model'] is False and token['events'][-1]['stage']=='client-create' and token['events'][-1]['outcome']=='raise','CLIENT-CONSTRUCTION-TOKEN-FRONTIER')
 refs=token['reference_bindings'];scope=token['scope'];cat=basis['catalogue'];error=basis['fresh']['coverage'].client_construction_binding(cat,scope,tc['control_present']);same(case['construction_error'],error,'CLIENT-CONSTRUCTION-EXPRESSION-ERROR')
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':cat['source']['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(cat['source']['guard']),'source':copy.deepcopy(cat['source']['sources']['entry']),'premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 same(case['none_guard_binding'],binding,'CLIENT-CONSTRUCTION-SELECTED-GUARD-BINDING')
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_inputs':copy.deepcopy(tc['projection']),'token_prefix':token,'construction_error':error,'none_guard_binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.client_construction_projection(cat,case['projection'],v);c.validate_client_construction_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Selected Client(token) expression raises before client callback; control absent or its selected earlier path completed normally. Same-owner exact-None guard and selected-owner continuity are explicit conditional premises. No allocation, initializer history, physical identity or existing cause/context absence is inferred.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'CLIENT-CONSTRUCTION-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 exact(case,'CLIENT-CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');require(type(branch) is str and branch in ('control-construction','control','bare','stored-client','stored-normal','normal-token'),'CLIENT-CONSTRUCTION-PRIOR-BRANCH');_,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def _construct_prior(basis,branch,case):
 exact(case,'CLIENT-CONSTRUCTION-PRIOR-CONSTRUCTED-INPUT');p=basis['construction_module'];b=basis['construction_basis']
 if branch=='control-construction':return p._construct_checked(b,case)
 return p._construct_prior(b,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_client_construction(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'CLIENT-CONSTRUCTION-RECEIPT-BYTES');v=json.loads(saved);required={'client_construction_none_correspondence','control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'}
 require(type(v) is dict and v.get('format')=='I164-CLIENT-CONSTRUCTION-NONE-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and required<=set(c) for c in v['contexts']),'CLIENT-CONSTRUCTION-MANDATORY-RELATIONS');require(saved==enc(derive(root)),'CLIENT-CONSTRUCTION-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_client_construction_revocation_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
