"""Conditional selected local Py_DECREF fast-branch source completion. No application/protocol execution.

The full public path retains the unchanged enter-decref authentication and byte comparison.
It requires separate execution authorization; saved receipts are not live bases.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
RELATION='decref_fast_completion_correspondence'
PARENT_MANIFEST={'bytes':2054744,'sha256':'2ee47edee356daa2f4f004c7688381e1bd1cc1291bf02813df20f97ddf39799f'}
PARENT_RECEIPT={'bytes':18414683,'sha256':'8bceed6d70faa689c9ab3cfabe41d996c1637c238a49808e1c524073921fb0eb'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def require(ok,code):
 if not ok:raise ValueError(code)
def module(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def exact(v,code):
 active=set()
 def walk(x):
  t=type(x)
  if t is dict or t is list:
   require(id(x) not in active,code+':CYCLE');active.add(id(x))
   if t is dict:
    for k,v in x.items():require(type(k) is str,code+':KEY-TYPE');walk(v)
   else:
    for v in x:walk(v)
   active.remove(id(x))
  else:require(t in (str,int,bool,float,type(None)),code+':VALUE-TYPE')
 walk(v)
def same(a,b,code):exact(a,code);exact(b,code);require(enc(a)==enc(b),code)
def parent_root(root):
 root=Path(root);base=root/'retained/decref'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'DECREF-FAST-ROOT-TYPE')
 raw=(root/'reference/decref/ASSEMBLED-ROOT-MANIFEST.json').read_bytes();require(identity(raw)==PARENT_MANIFEST,'DECREF-FAST-PARENT-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest);dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};found=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'DECREF-FAST-UNDECLARED-DIR');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'DECREF-FAST-UNDECLARED-ENTRY');found.add(n)
 walk(base);require(found==expected and seen==dirs,'DECREF-FAST-EXACT-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'DECREF-FAST-PARENT-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=parent_root(root);pins=json.loads((root/'provenance/component-pins.json').read_bytes())
 for n,pin in pins.items():
  p=root/n;require(stat.S_ISREG(p.lstat().st_mode) and identity(p.read_bytes())==pin,'DECREF-FAST-COMPONENT-PIN:'+n)
 saved=(root/'reference/decref/actual-receipt.json').read_bytes();require(identity(saved)==PARENT_RECEIPT,'DECREF-FAST-PARENT-RECEIPT')
 p=module(base/'code/correspondence.py','_decref_fast_reviewed_attempt');pd=p.inputs(base)
 return {'root':root,'parent_root':base,'parent_module':p,'parent_data':pd,'saved':saved,'coverage':module(root/'code/managed_coverage.py','_decref_fast_producer')}
def source_files(root):
 root=Path(root);names=json.loads((root/'reference/resolution/source-index.json').read_bytes())
 return {n:(root/'reference/resolution/source'/n).read_bytes() for n in names}
def _basis(data):
 fresh=inputs(data['root']);p=fresh['parent_module'];pd=fresh['parent_data']
 # Unchanged parent's substantive authentication and actual returned basis, then
 # exact parent receipt comparison. No saved dictionary substitutes for this call.
 p._receipt_shape(fresh['saved']);pb=p._basis(pd)
 require(fresh['saved']==p.enc(p._assemble(pb)),'DECREF-FAST-PREDECESSOR-STALE-OR-ALTERED-RECEIPT')
 public={'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(fresh['saved']),'actual_admission':False}
 r=fresh['root'];c=fresh['coverage'];ss=source_files(r)
 returned=pb['parent_basis'];enter=returned['parent_basis'];lookup=enter['parent_basis'];r1=lookup['parent_basis']
 cat=c.compile_decref_fast((r/'source-evidence/lab_bootstrap.py').read_bytes(),(r/'reference/cpython-3.12.14/bytecodes.c').read_bytes(),(r/'reference/cpython-3.12.14/typeobject.c').read_bytes(),r1['catalogue'],lookup['catalogue'],enter['catalogue'],returned['catalogue'],pb['catalogue'],ss)
 return {'fresh':fresh,'parent_module':p,'parent_basis':pb,'parent_public':public,'prior':json.loads(fresh['saved']),'catalogue':cat,'source_files':ss}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'DECREF-FAST-CONTEXTS');rows=[]
 for ctx in basis['prior']['contexts']:
  parent=ctx['enter_decref_attempt_correspondence'];cat=basis['catalogue']
  rows.append({'context':ctx['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(parent['session_binding']),'predecessor_receipt':copy.deepcopy(PARENT_RECEIPT),'predecessor_validation':copy.deepcopy(basis['parent_public']),
   'conditional_links':[{'declaration':s['id'],'source':copy.deepcopy(s['source']),'invocation':None,'frame':None,'observed_value':None} for s in cat['declarations']],
   'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'runtime_chain':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'stop':cat['stop'],'branch_state':'UNOBSERVED; no branch chosen for actual instance','qualified_binary_correspondence':False,'actual_admission':False})
 return rows
def _construct_checked(basis,case):
 exact(case,'DECREF-FAST-CONSTRUCTED-TYPE');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-DECREF-FAST-COMPLETION','DECREF-FAST-CONSTRUCTED-SHAPE')
 require(case['context'] in CONTEXTS,'DECREF-FAST-CONTEXT');row=next(r for r in basis['prior']['contexts'] if r['context']==case['context']);anchor=row['enter_decref_attempt_correspondence']['instance_anchor'];same(case['anchor'],anchor,'DECREF-FAST-CONSTRUCTED-ANCHOR')
 same({k:case['parent_case'].get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'DECREF-FAST-PARENT-INVOCATION')
 parent=basis['parent_module']._construct_checked(basis['parent_basis'],case['parent_case'])['projection'];same(case['parent_output'],parent,'DECREF-FAST-VALIDATED-PARENT')
 c=basis['fresh']['coverage'];cat=basis['catalogue'];ss=basis['source_files'];b=case['binding']
 binding=c.decref_fast_binding(cat,parent,anchor,b['continuity'],b['branch'],b['envelope'],ss);same(b,binding,'DECREF-FAST-BINDING')
 v={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
 c.validate_decref_fast_projection(cat,case['projection'],v,case['output'],ss)
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(anchor),'projection':c.decref_fast_projection(cat,case['projection'],v,ss),'runtime_observation':False}
def constructed_projection(data,case):return _construct_checked(_basis(data),case)
def _assemble(basis):
 out=copy.deepcopy(basis['prior']);out['format']='I164-DECREF-FAST-COMPLETION-1';out['prior_enter_decref_components']=out.pop('extension_components');out['prior_enter_decref_receipt']=copy.deepcopy(PARENT_RECEIPT)
 out['extension_components']={n:identity((basis['fresh']['root']/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(out['contexts'],_rows(basis)):ctx[RELATION]=copy.deepcopy(row)
 out['new_decref_fast_completion_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','stop':basis['catalogue']['stop'],'effective_macro':'ceval.c:56-68 local override','branches':['immortal','non-immortal-positive-gt-one'],
  'branch_state_from_res':False,'runtime_arrival':'UNAVAILABLE','actual_completion_established':False,'physical_effects_established':False,'zero_count_destructor_completion':'UNRESOLVED','qualified_binary_correspondence':False,'deeper_helper_error_indicator':'UNKNOWN',
  'result_test_established':False,'context_manager_entry_established':False,'f_binding_established':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return out
def derive(root=ROOT):return _assemble(_basis(inputs(root)))
def _receipt_shape(saved):
 require(type(saved) is bytes,'DECREF-FAST-RECEIPT-BYTES');r=json.loads(saved)
 require(type(r) is dict and r.get('format')=='I164-DECREF-FAST-COMPLETION-1' and type(r.get('contexts')) is list and len(r['contexts'])==2,'DECREF-FAST-RECEIPT-SHAPE')
 require([x.get('context') for x in r['contexts']]==list(CONTEXTS) and all(RELATION in x and 'enter_decref_attempt_correspondence' in x for x in r['contexts']),'DECREF-FAST-MANDATORY-RELATIONS');return r
def validate(root,saved):
 _receipt_shape(saved);result=derive(root);require(saved==enc(result),'DECREF-FAST-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'actual_admission':False}
