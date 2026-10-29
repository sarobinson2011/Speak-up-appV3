"""Mandatory bounded normal owner-lock descriptor finalization over the reviewed exit chain.
Saved evidence only. No application method or database connection is invoked.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 227678, 'sha256': '2f9807a5c75a9a8ff4307312bb341cf173cfc5dd92f5c99cd14b856a73274955'}
PREDECESSOR_MANIFEST={'bytes':633328,'sha256':'8dcadeb9a5f023fb9c614facf47c7e02929a0a2b231abc277599ecddc7f6cdd8'}
PREDECESSOR_RECEIPT={'bytes':4032928,'sha256':'928726175efbb720b03dc722de67477fa7ea3b3ce43b4c37bbeb2c9a730fea07'}
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
 root=Path(root);base=root/'retained/exit'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'OWNER-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'OWNER-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'OWNER-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'OWNER-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'OWNER-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'OWNER-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'OWNER-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode),'OWNER-PRODUCER-TYPE');require(identity(path.read_bytes())==PRODUCER_PIN,'OWNER-PRODUCER-PIN')
 prior=module(base/'code/correspondence.py','_owner_exit_predecessor');return {'root':root,'prior_root':base,'prior_module':prior,'prior_data':prior.inputs(base),'coverage':module(path,'_owner_coverage')}
def inner(data):return data['prior_module'].inner(data['prior_data'])
def sources(data):return data['prior_module'].sources(data['prior_data'])
def dependency(data):return data['prior_module'].catalogue(data['prior_data'])
def catalogue(data):return data['coverage'].compile_owner_finalization(sources(data)[0],dependency(data))
def _basis(data):
 fresh=inputs(data['root']);p=fresh['prior_module'];pd=fresh['prior_data'];rows,eb=p._checked(pd,p.catalogue(pd));prior=p._assemble(pd,rows,eb)
 # Exactly the predecessor derive_exit validation/assembly, preserving its basis
 # so the selected invocation consumes the same authenticated evidence chain.
 saved=(fresh['prior_root']/'results/primary/normal-session-exit-correspondence.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT and enc(prior)==saved,'OWNER-VALIDATED-PREDECESSOR-RECEIPT')
 return {'fresh':fresh,'prior':prior,'saved':saved,'exit_basis':eb,'catalogue':catalogue(fresh),'evidence':dict(inner(fresh)['ctx']['e'])}
def _rows(basis):
 rows=[];cat=basis['catalogue'];require(tuple(r['context'] for r in basis['prior']['contexts'])==CONTEXTS,'OWNER-CONTEXT-DOMAIN')
 for row in basis['prior']['contexts']:
  previous=row['normal_session_exit_correspondence'];anchor=previous['instance_anchor'];same(previous['declaration']['source']['launcher'],cat['source']['launcher'],'OWNER-VALIDATED-LAUNCHER');scope=copy.deepcopy(previous['scope']);sb=previous['session_binding'];mp=previous['marker_path']
  rows.append({'context':row['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(anchor),'predecessor_receipt':identity(basis['saved']),'scope':scope,'session_binding':copy.deepcopy(sb),'marker_path':copy.deepcopy(mp),'descriptor_lineage':basis['fresh']['coverage'].owner_descriptor_lineage(cat,scope,sb,mp),
   'reference_basis':copy.deepcopy(previous['reference_basis']),'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'saved_close_evidence':copy.deepcopy(previous['saved_close_evidence']),'selected_owner_continuity':previous['selected_owner_continuity'],'runtime_finalizer_chain':None,'numeric_descriptor_observation':None,'physical_resource_identity':None,'actual_invocation_count':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'observer_join':None,'separate_observer':copy.deepcopy(previous['separate_observer']),'outer_lifecycle_complete':False,
   'gap':'No runtime descriptor producer/finalizer/close-attempt/completion chain; exception/outer cleanup, physical resource/lock release, continuity, exclusivity and durability remain unestablished.'})
 return rows
def _check_rows(basis,claims):
 exact(claims,'OWNER-SEMANTIC-CLAIMS');require(type(claims) is list and len(claims)==2,'OWNER-CLAIM-CONTEXT-DOMAIN');same(claims,_rows(basis),'OWNER-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'OWNER-EVIDENCE-TYPES');require(candidate==basis['evidence'],'OWNER-VALIDATED-EVIDENCE')
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'OWNER-CATALOGUE');exact(claims,'OWNER-CLAIMS');basis=_basis(data);same(submitted_catalogue,basis['catalogue'],'OWNER-CATALOGUE-SOURCE')
 d=inner(data);fd=inner(basis['fresh']);require(all(type(x) is bytes for x in sources(data)) and type(d['ctx']['c']) is dict and all(type(k) is str and type(v) is bytes for k,v in d['ctx']['c'].items()),'OWNER-CANDIDATE-SOURCE-TYPES');require(sources(data)==sources(basis['fresh']) and d['ctx']['c']==fd['ctx']['c'],'OWNER-CANDIDATE-SOURCE');same(d['ctx']['binding'],fd['ctx']['binding'],'OWNER-CANDIDATE-BINDING');_compare_evidence(basis,d['ctx']['e'] if evidence is None else evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-OWNER-LOCK-FINALIZATION-1';result['prior_normal_exit_components']=result.pop('extension_components');result['prior_normal_exit_receipt']=identity(basis['saved']);result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx['owner_lock_finalization_correspondence']=copy.deepcopy(row)
 result['new_owner_finalization_limits']={'normal_conditional_slice':True,'runtime_finalizer_chain':'UNAVAILABLE','numeric_descriptor_observation':None,'physical_resource_identity':None,'physical_lock_release':False,'runtime_exclusivity':False,'observer_join':None,'outer_lifecycle_complete':False,'selected_owner_continuity':'Explicit conditional premise, not qualification','complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_owner(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'OWNER-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','exit_case','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-OWNER-LOCK-FINALIZATION','OWNER-CONSTRUCTED-CASE');selected=[r for r in _rows(basis) if r['context']==case['context']];require(len(selected)==1,'OWNER-CONSTRUCTED-CONTEXT');anchor=selected[0]['instance_anchor'];same(case['anchor'],anchor,'OWNER-CONSTRUCTED-ANCHOR')
 ec=case['exit_case'];require(type(ec) is dict,'OWNER-EXIT-CASE');same({k:ec.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'OWNER-EXIT-INVOCATION');p=basis['fresh']['prior_module'];previous=p._construct_checked(basis['exit_basis'],ec)['projection'];scope=previous['scope'];sb=previous['session_binding'];mp=previous['marker_path']
 return {'scope':copy.deepcopy(scope),'session_binding':copy.deepcopy(sb),'marker_path':copy.deepcopy(mp),'references':copy.deepcopy(previous['reference_bindings']),'exit_result':previous,'descriptor':basis['fresh']['coverage'].owner_descriptor_lineage(basis['catalogue'],scope,sb,mp),'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.owner_finalization_projection(cat,case['projection'],v);c.validate_owner_finalization_projection(cat,case['projection'],v,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'premises':'Finite constructed normal-route outcomes; same-invocation source-result fd lineage, not observed descriptor/resource identity. Selected-owner continuity remains conditional.','runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'OWNER-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def derive(root=ROOT):
 data=inputs(root);return derive_owner(data,catalogue(data))
def validate(root,saved):
 require(type(saved) is bytes,'OWNER-RECEIPT-BYTES');v=json.loads(saved);require(type(v) is dict and v.get('format')=='I164-OWNER-LOCK-FINALIZATION-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and 'owner_lock_finalization_correspondence' in c for c in v['contexts']),'OWNER-MANDATORY-RELATION');require(saved==enc(derive(root)),'OWNER-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_finalizer_chain':'UNAVAILABLE','actual_admission':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
