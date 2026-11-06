"""NEW reconstruction. Public authentication requires separately recovered parent root.
Focused source fixtures do not supply an authenticated basis. Full public validation
of these reconstructed bytes is pending; this module never runs an application.
"""
import copy,hashlib,json,os,stat,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
RELATION='open_return_context_operand_correspondence'
PARENT_MANIFEST={'bytes':1694211,'sha256':'5852ec258fbf3543215754c5fdac3d01d475a0e2bd190da4493b07f1ac91071b'}
PARENT_RECEIPT={'bytes':17426465,'sha256':'5780038e972c1360e0b67f2f7f3a1bb5a9a2d5551fd2c3b9c14a81250d1224ee'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def require(ok,code):
 if not ok:raise ValueError(code)
def module(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def exact(v,code):
 active=set()
 def walk(n):
  t=type(n)
  if t is dict or t is list:
   require(id(n) not in active,code+':CYCLE');active.add(id(n))
   if t is dict:
    for k,x in n.items():require(type(k) is str,code+':KEY-TYPE');walk(x)
   else:
    for x in n:walk(x)
   active.remove(id(n))
  else:require(any(t is typ for typ in (str,int,bool,float,type(None))),code+':VALUE-TYPE')
 walk(v)
def same(a,b,code):exact(a,code);exact(b,code);require(enc(a)==enc(b),code)
def parent_root(root):
 base=Path(root)/'retained/helper-open'
 for p in (Path(root),Path(root)/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'OR-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'OR-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PARENT_MANIFEST,'OR-PARENT-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};found=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'OR-UNDECLARED-DIR');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'OR-UNDECLARED-ENTRY');found.add(n)
 walk(base);require(found==expected and seen==dirs,'OR-EXACT-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'OR-PARENT-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=parent_root(root);pins=json.loads((root/'provenance/component-pins.json').read_bytes())
 for n in ('managed_coverage.py','correspondence.py'):
  p=root/'code'/n;require(stat.S_ISREG(p.lstat().st_mode) and identity(p.read_bytes())==pins['code/'+n],'OR-COMPONENT-PIN')
 saved=(base/'receipts/prepared-helper-open-attempt.json').read_bytes();require(identity(saved)==PARENT_RECEIPT,'OR-PARENT-RECEIPT')
 p=module(base/'code/correspondence.py','_or_reviewed_helper_parent');data=p.inputs(base)
 return {'root':root,'parent_root':base,'parent_module':p,'parent_data':data,'saved':saved,'coverage':module(root/'code/managed_coverage.py','_or_reconstructed_producer')}
def _basis(data):
 fresh=inputs(data['root']);p=fresh['parent_module'];pd=fresh['parent_data']
 # Exact semantic/authenticated-basis and receipt-comparison operations from
 # the unchanged parent validate body. No synthetic basis or saved PASS input.
 # Parent _checked still invokes its actual unchanged public predecessor.
 p._receipt_shape(fresh['saved']);_,pb=p._checked(pd,p.catalogue(pd));public=p._receipt_checked(pb,fresh['saved'])
 require(public['result']=='PASS' and public['contexts']==list(CONTEXTS) and public['receipt']==PARENT_RECEIPT,'OR-AUTHENTICATED-PARENT')
 launcher=p.sources(pb['fresh'])[0];cat=fresh['coverage'].compile_open_return(launcher,pb['catalogue'])
 return {'fresh':fresh,'parent_module':p,'parent_basis':pb,'parent_public':copy.deepcopy(public),'prior':json.loads(fresh['saved']),'catalogue':cat}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'OR-CONTEXTS');rows=[]
 for ctx in basis['prior']['contexts']:
  parent=ctx['helper_open_attempt_correspondence'];cat=basis['catalogue']
  rows.append({'context':ctx['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(parent['session_binding']),'predecessor_receipt':copy.deepcopy(PARENT_RECEIPT),'predecessor_validation':copy.deepcopy(basis['parent_public']),
   'conditional_links':[{'declaration':s['id'],'source':copy.deepcopy(s['source']),'invocation':None,'frame':None,'observed_value':None} for s in cat['declarations']],
   'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'runtime_chain':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),'stop':cat['stop'],'actual_admission':False})
 return rows
def _construct_checked(basis,case):
 exact(case,'OR-CONSTRUCTED-TYPE');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-OPEN-RETURN-RECONSTRUCTION','OR-CONSTRUCTED-SHAPE')
 require(case['context'] in CONTEXTS,'OR-CONTEXT');row=next(r for r in basis['prior']['contexts'] if r['context']==case['context']);anchor=row['helper_open_attempt_correspondence']['instance_anchor'];same(case['anchor'],anchor,'OR-CONSTRUCTED-ANCHOR')
 same({k:case['parent_case'].get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'OR-PARENT-INVOCATION')
 parent=basis['parent_module']._construct_checked(basis['parent_basis'],case['parent_case'])['projection'];same(case['parent_output'],parent,'OR-VALIDATED-PARENT')
 c=basis['fresh']['coverage'];cat=basis['catalogue'];binding=c.open_return_binding(cat,parent,anchor,case['binding']['continuity']);same(case['binding'],binding,'OR-BINDING')
 v={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':binding,'outcomes':copy.deepcopy(case['outcomes'])}
 c.validate_open_return_projection(cat,case['projection'],v,case['output'])
 return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(anchor),'projection':c.open_return_projection(cat,case['projection'],v),'runtime_observation':False}
def constructed_projection(data,case):return _construct_checked(_basis(data),case)
def _assemble(basis):
 rows=_rows(basis);out=copy.deepcopy(basis['prior']);out['format']='I164-OPEN-RETURN-RECONSTRUCTION-1';out['prior_helper_open_components']=out.pop('extension_components');out['prior_helper_open_receipt']=copy.deepcopy(PARENT_RECEIPT)
 out['extension_components']={n:identity((basis['fresh']['root']/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(out['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 out['new_open_return_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','stop':basis['catalogue']['stop'],'context_protocol_lookup_established':False,'context_manager_entry_established':False,'f_binding_established':False,'physical_identity_established':False,'file_creation_established':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}
 return out
def derive(root=ROOT):return _assemble(_basis(inputs(root)))
def _receipt_shape(saved):
 require(type(saved) is bytes,'OR-RECEIPT-BYTES');r=json.loads(saved)
 require(type(r) is dict and r.get('format')=='I164-OPEN-RETURN-RECONSTRUCTION-1' and type(r.get('contexts')) is list and len(r['contexts'])==2,'OR-RECEIPT-SHAPE')
 require([x.get('context') for x in r['contexts']]==list(CONTEXTS) and all(RELATION in x and 'helper_open_attempt_correspondence' in x for x in r['contexts']),'OR-MANDATORY-RELATIONS');return r
def validate(root,saved):
 _receipt_shape(saved);result=derive(root);require(saved==enc(result),'OR-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'actual_admission':False}
