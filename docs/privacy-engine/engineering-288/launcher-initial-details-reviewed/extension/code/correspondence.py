"""Mandatory bounded launcher-handler/initial-details correspondence. Saved inputs only."""
import copy,hashlib,json,os,stat,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 322999, 'sha256': 'c34c8fef0cd16d04622027689f40dcbe058c0c4faa41ac4e50a96ab7cf63737b'}
PREDECESSOR_MANIFEST={'bytes':1157393,'sha256':'1a8349ecee728a16c2e5c5d9806b5eeb09f301f1d817ce1a282b14af317e4134'}
PREDECESSOR_RECEIPT={'bytes':8723742,'sha256':'23004fec192169630993d1290c5c205126d1457d2deae08f3b0d21ef5c960454'}
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
RELATION='launcher_initial_details_correspondence'
REQUIRED={RELATION,'client_construction_none_correspondence','control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'}
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
 root=Path(root);base=root/'retained/client-construction'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'DETAILS-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'DETAILS-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'DETAILS-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'DETAILS-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'DETAILS-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'DETAILS-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'DETAILS-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode) and identity(path.read_bytes())==PRODUCER_PIN,'DETAILS-PRODUCER-PIN')
 saved=(base/'results/primary/client-construction-none.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT,'DETAILS-PREDECESSOR-RECEIPT-PIN')
 raws=[]
 for name in ('lab_bootstrap.py','prospective_entry.py'):
  p=root/'source-evidence'/name;require(stat.S_ISREG(p.lstat().st_mode),'DETAILS-SOURCE-TYPE');b=p.read_bytes();require(b==(base/'source-evidence'/name).read_bytes(),'DETAILS-SOURCE-IDENTITY');raws.append(b)
 return {'root':root,'prior_root':base,'prior_module':module(base/'code/correspondence.py','_client_construction_predecessor'),'prior_saved':saved,'prior':json.loads(saved),'sources':tuple(raws),'coverage':module(path,'_launcher_details_coverage')}
def sources(data):return data['sources']
def catalogue(data):return data['coverage'].compile_launcher_details(*sources(data),data['prior']['contexts'][0]['client_construction_none_correspondence']['declaration'])
def _public_predecessor(data):
 """One actual unmodified public validation; passive return observation only.
 No predecessor function, source, output or validation expectation is replaced.
 A busy monitoring slot or missing return is a conflict, not a fallback route.
 """
 p=data['prior_module'];sm=getattr(sys,'monitoring',None);require(sm is not None,'DETAILS-MONITORING-UNAVAILABLE');require(sm.get_tool(2) is None,'DETAILS-MONITORING-CONTENTION')
 captures=[];basis_code=p._basis.__code__
 # Private live name object identifies this invocation even if interruption
 # occurs after C-level reservation but before another Python statement.
 lease='launcher-details-authenticated-predecessor:'+str(id(captures))
 try:
  sm.use_tool_id(2,lease)
  def capture(code,offset,value):
   require(code is p._basis.__code__ and len(captures)==0,'DETAILS-UNEXPECTED-BASIS-RETURN');captures.append(value)
  sm.register_callback(2,sm.events.PY_RETURN,capture)
  sm.set_local_events(2,basis_code,sm.events.PY_RETURN)
  result=p.validate(data['prior_root'],data['prior_saved'])
 finally:
  # Do not release a foreign reservation, including a failed acquisition race.
  # CPython's recorded name object is the lease marker; no value-only match.
  if sm.get_tool(2) is lease:
   try:
    sm.set_local_events(2,basis_code,0)
   finally:
    try:
     sm.register_callback(2,sm.events.PY_RETURN,None)
    finally:
     sm.free_tool_id(2)
 require(result.get('result')=='PASS' and result.get('contexts')==list(CONTEXTS) and result.get('receipt')==PREDECESSOR_RECEIPT and len(captures)==1,'DETAILS-PUBLIC-PREDECESSOR-RESULT')
 basis=captures[0];require(p.enc(p._assemble(basis['fresh'],p._rows(basis),basis))==data['prior_saved'],'DETAILS-AUTHENTICATED-BASIS-RECEIPT')
 return basis,copy.deepcopy(result)
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh'])[:2],'DETAILS-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_launcher_details(*sources(fresh),pb['catalogue'])
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'DETAILS-CONTEXT-DOMAIN');out=[]
 for old in basis['prior']['contexts']:
  parent=old['client_construction_none_correspondence'];cat=basis['catalogue']
  out.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),
   'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Original constructor error remains pending after reviewed exact-None bare rethrow and normal removal; pop completion alone does not suffice',
   'runtime_handler_details_chain':None,'exact_generated_error_name':None,'exact_generated_message':None,'exact_generated_traceback':None,'exact_details_bytes':None,'physical_reference_observation':None,
   'exception_delivery_continuity':'Explicit conditional premise; no runtime arrival established','selected_owner_continuity':'Preserved conditional premise; not exclusivity','existing_cause_context_suppression':'UNKNOWN',
   'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'cleanup_loop_coverage':False,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'gap':'No runtime constructor-to-handler/details chain, exact generated strings or cleanup/evidence-write completion.'})
 return out
def _check_rows(basis,claims):exact(claims,'DETAILS-SEMANTIC-CLAIMS');same(claims,_rows(basis),'DETAILS-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'DETAILS-EVIDENCE-TYPES');require(candidate==basis['evidence'],'DETAILS-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'DETAILS-CATALOGUE');exact(claims,'DETAILS-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'DETAILS-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'DETAILS-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'DETAILS-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'DETAILS-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'DETAILS-CATALOGUE');exact(claims,'DETAILS-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-LAUNCHER-INITIAL-DETAILS-CORRESPONDENCE-1';result['prior_client_construction_components']=result.pop('extension_components');result['prior_client_construction_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_launcher_details_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','exact_generated_strings_bytes':None,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'cleanup_loop_entered':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_launcher_details(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'DETAILS-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','delivery_binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-LAUNCHER-INITIAL-DETAILS','DETAILS-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'DETAILS-CONSTRUCTED-CONTEXT');anchor=rows[0]['client_construction_none_correspondence']['instance_anchor'];same(case['anchor'],anchor,'DETAILS-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'DETAILS-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'DETAILS-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'DETAILS-VALIDATED-PARENT-OUTPUT')
 binding=case['delivery_binding'];require(type(binding) is dict and 'continuity' in binding,'DETAILS-DELIVERY-INPUT')
 expected=basis['fresh']['coverage'].launcher_delivery_binding(basis['catalogue'],parent,anchor,binding['continuity']);same(binding,expected,'DETAILS-EXPECTED-DELIVERY')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'delivery_binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.launcher_details_projection(cat,case['projection'],v);c.validate_launcher_details_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'DETAILS-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'DETAILS-PRIOR-INPUT');require(type(branch) is str and branch in ('client-construction','control-construction','control','bare','stored-client','stored-normal','normal-token'),'DETAILS-PRIOR-BRANCH')
 if branch=='client-construction':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_launcher_details(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'DETAILS-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-LAUNCHER-INITIAL-DETAILS-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'DETAILS-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'DETAILS-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_handler_details_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
