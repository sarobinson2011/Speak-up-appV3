"""Conditional special-method lookup extension. No application/protocol execution.

The full public path retains the unchanged R1 authentication and byte comparison.
It requires separate execution authorization; saved receipts are not live bases.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
RELATION='context_special_lookup_correspondence'
PARENT_MANIFEST={'bytes':1783461,'sha256':'e7e6d8ab8aad1697d1556c823a80fbf7f6b5d282a76790e3e52c2cc4254cf45b'}
PARENT_RECEIPT={'bytes':17607505,'sha256':'5c56b5f07619fd566d13f5cb21755915ccb78fb8096617a4ecba0707d214458c'}
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
 root=Path(root);base=root/'retained/r1'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'LOOKUP-ROOT-TYPE')
 raw=(root/'reference/r1/ASSEMBLED-ROOT-MANIFEST.json').read_bytes();require(identity(raw)==PARENT_MANIFEST,'LOOKUP-PARENT-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest);dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};found=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'LOOKUP-UNDECLARED-DIR');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'LOOKUP-UNDECLARED-ENTRY');found.add(n)
 walk(base);require(found==expected and seen==dirs,'LOOKUP-EXACT-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'LOOKUP-PARENT-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=parent_root(root);pins=json.loads((root/'provenance/component-pins.json').read_bytes())
 for n,pin in pins.items():
  p=root/n;require(stat.S_ISREG(p.lstat().st_mode) and identity(p.read_bytes())==pin,'LOOKUP-COMPONENT-PIN:'+n)
 saved=(root/'reference/r1/actual-receipt.json').read_bytes();require(identity(saved)==PARENT_RECEIPT,'LOOKUP-PARENT-RECEIPT')
 p=module(base/'code/correspondence.py','_lookup_reviewed_r1');pd=p.inputs(base)
 return {'root':root,'parent_root':base,'parent_module':p,'parent_data':pd,'saved':saved,'coverage':module(root/'code/managed_coverage.py','_lookup_producer')}
def _basis(data):
 fresh=inputs(data['root']);p=fresh['parent_module'];pd=fresh['parent_data']
 # These are the actual operations of unchanged R1 validate/derive, retaining
 # the returned predecessor basis in this invocation, never a serialized basis.
 p._receipt_shape(fresh['saved']);pb=p._basis(pd)
 require(fresh['saved']==p.enc(p._assemble(pb)),'LOOKUP-R1-STALE-OR-ALTERED-RECEIPT')
 public={'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(fresh['saved']),'actual_admission':False}
 r=fresh['root'];c=fresh['coverage'];cat=c.compile_context_lookup((r/'source-evidence/lab_bootstrap.py').read_bytes(),(r/'reference/cpython-3.12.14/bytecodes.c').read_bytes(),(r/'reference/cpython-3.12.14/typeobject.c').read_bytes(),pb['catalogue'])
 return {'fresh':fresh,'parent_module':p,'parent_basis':pb,'parent_public':public,'prior':json.loads(fresh['saved']),'catalogue':cat}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'LOOKUP-CONTEXTS');rows=[]
 for ctx in basis['prior']['contexts']:
  parent=ctx['open_return_context_operand_correspondence'];cat=basis['catalogue']
  rows.append({'context':ctx['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(parent['session_binding']),'predecessor_receipt':copy.deepcopy(PARENT_RECEIPT),'predecessor_validation':copy.deepcopy(basis['parent_public']),
   'conditional_links':[{'declaration':s['id'],'source':copy.deepcopy(s['source']),'invocation':None,'frame':None,'observed_value':None} for s in cat['declarations']],
   'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'runtime_chain':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),'stop':cat['source']['stop'],'actual_admission':False})
 return rows
def _construct_checked(basis,case):
 exact(case,'LOOKUP-CONSTRUCTED-TYPE');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CONTEXT-SPECIAL-LOOKUP','LOOKUP-CONSTRUCTED-SHAPE')
 require(case['context'] in CONTEXTS,'LOOKUP-CONTEXT');row=next(r for r in basis['prior']['contexts'] if r['context']==case['context']);anchor=row['open_return_context_operand_correspondence']['instance_anchor'];same(case['anchor'],anchor,'LOOKUP-CONSTRUCTED-ANCHOR')
 same({k:case['parent_case'].get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'LOOKUP-PARENT-INVOCATION')
 parent=basis['parent_module']._construct_checked(basis['parent_basis'],case['parent_case'])['projection'];same(case['parent_output'],parent,'LOOKUP-VALIDATED-PARENT')
 c=basis['fresh']['coverage'];cat=basis['catalogue'];binding=c.context_lookup_binding(cat,parent,anchor,case['binding']['continuity']);same(case['binding'],binding,'LOOKUP-BINDING')
 v={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
 c.validate_context_lookup_projection(cat,case['projection'],v,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(anchor),'projection':c.context_lookup_projection(cat,case['projection'],v),'runtime_observation':False}
def constructed_projection(data,case):return _construct_checked(_basis(data),case)
def _assemble(basis):
 out=copy.deepcopy(basis['prior']);out['format']='I164-CONTEXT-SPECIAL-LOOKUP-1';out['prior_open_return_components']=out.pop('extension_components');out['prior_open_return_receipt']=copy.deepcopy(PARENT_RECEIPT)
 out['extension_components']={n:identity((basis['fresh']['root']/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(out['contexts'],_rows(basis)):ctx[RELATION]=copy.deepcopy(row)
 out['new_context_lookup_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','stop':basis['catalogue']['source']['stop'],'protocol_method_invocation_established':False,'context_manager_entry_established':False,'f_binding_established':False,'physical_identity_established':False,'descriptor_effects':'UNKNOWN','file_creation_established':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return out
def derive(root=ROOT):return _assemble(_basis(inputs(root)))
def _receipt_shape(saved):
 require(type(saved) is bytes,'LOOKUP-RECEIPT-BYTES');r=json.loads(saved)
 require(type(r) is dict and r.get('format')=='I164-CONTEXT-SPECIAL-LOOKUP-1' and type(r.get('contexts')) is list and len(r['contexts'])==2,'LOOKUP-RECEIPT-SHAPE')
 require([x.get('context') for x in r['contexts']]==list(CONTEXTS) and all(RELATION in x and 'open_return_context_operand_correspondence' in x for x in r['contexts']),'LOOKUP-MANDATORY-RELATIONS');return r
def validate(root,saved):
 _receipt_shape(saved);result=derive(root);require(saved==enc(result),'LOOKUP-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'actual_admission':False}
