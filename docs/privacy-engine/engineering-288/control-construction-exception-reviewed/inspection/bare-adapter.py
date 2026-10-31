"""Mandatory exact-None callback bare-rethrow relation over both reviewed stored-failure branches.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 263743, 'sha256': 'c684cb3e599b4a5d0c9616436f6f4b341f96c47eaf10cee6b4194d0d6a357622'}
PREDECESSOR_MANIFEST={'bytes': 819714, 'sha256': 'dd9371b8c8520a3950f3fc26915884be9e0f2f6239a97ab7c6dbd00d6323223a'}
PREDECESSOR_RECEIPT={'bytes': 6418679, 'sha256': 'c5504cf29408dad2e916a2dedd43b654f88fd2e88bb26682e0ceaa31ee2268a0'}
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
 root=Path(root);base=root/'retained/callback'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'BARE-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'BARE-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'BARE-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'BARE-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'BARE-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'BARE-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'BARE-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'BARE-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'BARE-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_callback_stored_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_callback_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependencies(data):
 p=data['prior_module'];pd=data['prior_data'];return (p.catalogue(pd),*p.dependencies(pd))
def catalogue(data):return data['coverage'].compile_callback_bare(*sources(data)[:2],*dependencies(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,cb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,cb)
 saved=(fresh['prior_root']/'results/primary/callback-stored-failure.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'BARE-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e']),'callback_basis':cb,'callback_module':p,'stored_basis':cb['stored_basis']}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'BARE-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  callback=row['callback_stored_failure_correspondence'];token=row['token_registration_correspondence'];same(callback['instance_anchor'],token['instance_anchor'],'BARE-VALIDATED-INSTANCE');same(callback['declaration']['source']['sources'],cat['source']['sources'],'BARE-VALIDATED-SOURCE')
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(callback['instance_anchor']),'predecessor_receipt':identity(basis['saved']),'scope':copy.deepcopy(token['scope']),'reference_basis':copy.deepcopy(token['reference_basis']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'reviewed_stored_failure_relations_preserved':['stored_failure_revocation_correspondence','callback_stored_failure_correspondence'],'guard_slot_premise':cat['source']['guard_slot_premise'],'selected_owner_continuity':'Explicit conditional premise; not runtime exclusivity','runtime_callback_bare_revocation_chain':None,'callback_exception_producer_history':None,'exception_chain_observation':None,'prior_failure_storage_history':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(callback['separate_observer']),'outer_cleanup_complete':False,'gap':'No runtime callback/error/bare-raise/finally/pop chain or existing cause/context observations. Control failures and full outer cleanup remain unexpanded.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'BARE-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'BARE-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'BARE-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'BARE-EVIDENCE-TYPES');require(candidate==basis['evidence'],'BARE-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'BARE-CATALOGUE');exact(claims,'BARE-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'BARE-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'BARE-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'BARE-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'BARE-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CALLBACK-BARE-RETHROW-1';result['prior_callback_stored_components']=result.pop('extension_components');result['prior_callback_stored_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['callback_bare_rethrow_correspondence']=copy.deepcopy(row)
 result['new_callback_bare_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','selected_owner_continuity':'Explicit premise','guard_slot_continuity':'Explicit exact-None premise at selected guard, not absence of historical storage','callback_exception_producer_history':'UNAVAILABLE','existing_cause_context_suppression':'UNKNOWN','physical_identity_or_inequality':None,'observer_join':None,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_bare(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _selected(basis,context):
 rows=[r for r in basis['prior']['contexts'] if r['context']==context];require(len(rows)==1,'BARE-CONSTRUCTED-CONTEXT');return rows[0]
def _premises(basis,case):
 exact(case,'BARE-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','token_case','callback_error','none_guard_binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CALLBACK-BARE-RETHROW','BARE-CONSTRUCTED-CASE')
 row=_selected(basis,case['context']);anchor=row['token_registration_correspondence']['instance_anchor'];same(case['anchor'],anchor,'BARE-CONSTRUCTED-ANCHOR');tc=case['token_case'];require(type(tc) is dict,'BARE-TOKEN-CASE');same({k:tc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'BARE-TOKEN-INVOCATION')
 sb=basis['stored_basis'];token=sb['routes']['token_module']._construct_checked(sb['token_basis'],tc)['projection'];require(tc['owner_failure_none'] is True,'BARE-SELECTED-NONE-SLICE');require(token['registration_completed_in_model'] is True and token['completion']=='unexpected-raise' and token['client_callback_completed_in_model'] is False and token['events'][-1]['stage']=='client-callback' and token['events'][-1]['outcome']=='raise','BARE-TOKEN-FRONTIER')
 refs=token['reference_bindings'];scope=token['scope'];cat=basis['catalogue'];client=basis['fresh']['coverage'].callback_error_binding(cat,scope);same(case['callback_error'],client,'BARE-CAUGHT-ERROR')
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':cat['source']['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(cat['source']['guard']),'source':copy.deepcopy(cat['source']['sources']['entry']),'premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 same(case['none_guard_binding'],binding,'BARE-SELECTED-GUARD-BINDING')
 return {'scope':copy.deepcopy(scope),'references':copy.deepcopy(refs),'token_prefix':token,'none_guard_binding':binding,'callback_error':client,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.callback_bare_projection(cat,case['projection'],v);c.validate_callback_bare_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Conditional caught callback error, exact None at selected same-owner guard and selected-owner registry continuity. Bare raise preserves that selected error role without asserting existing cause/context absence. Not runtime history.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'BARE-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def constructed_normal_callback(data,submitted_catalogue,case):
 exact(case,'BARE-PRIOR-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);cb=basis['callback_basis'];return cb['stored_module']._construct_checked(cb['stored_basis'],case)
def derive(root=ROOT):
 data=inputs(root);return derive_bare(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'BARE-RECEIPT-BYTES');v=json.loads(saved);required={'callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence'}
 require(type(v) is dict and v.get('format')=='I164-CALLBACK-BARE-RETHROW-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and required<=set(c) for c in v['contexts']),'BARE-MANDATORY-RELATIONS');require(saved==enc(derive(root)),'BARE-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_callback_bare_revocation_chain':'UNAVAILABLE','actual_admission':False}
def constructed_stored_callback(data,submitted_catalogue,case):
 exact(case,'BARE-PRIOR-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return basis['callback_module']._construct_checked(basis['callback_basis'],case)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
