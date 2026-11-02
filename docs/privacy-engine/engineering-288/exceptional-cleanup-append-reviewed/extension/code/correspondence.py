"""Mandatory bounded exceptional cleanup/normal append correspondence. Saved inputs only."""
import copy,hashlib,json,os,stat,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 342189, 'sha256': 'a0e8bc4a3486e7c6e128ff2e2f707e5830cb967570189d39d5073011512f9c55'}
PREDECESSOR_MANIFEST={'bytes': 1313785, 'sha256': 'a0a0f40e02254798c0e5b8e3e35d8b46850fa9ac0721e32f3043ab211c28a679'}
PREDECESSOR_RECEIPT={'bytes': 10456658, 'sha256': 'd5b11ed9c09fa335c05c8a2f26201a71bc263466d5a1d48ad51b4994bd1c50cd'}
CONTEXTS=('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')
RELATION='exceptional_cleanup_append_correspondence'
REQUIRED={RELATION,'launcher_initial_details_correspondence','client_construction_none_correspondence','control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'}
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
 root=Path(root);base=root/'retained/details'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'CLEANUP-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'CLEANUP-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'CLEANUP-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'CLEANUP-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'CLEANUP-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'CLEANUP-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'CLEANUP-PREDECESSOR-BYTES:'+n)
 return base
def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode) and identity(path.read_bytes())==PRODUCER_PIN,'CLEANUP-PRODUCER-PIN')
 saved=(base/'ld01/receipts/corrected-launcher-details.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT,'CLEANUP-PREDECESSOR-RECEIPT-PIN')
 raws=[]
 for name in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):
  p=root/'source-evidence'/name;require(stat.S_ISREG(p.lstat().st_mode),'CLEANUP-SOURCE-TYPE');b=p.read_bytes();
  if name=='live_connection.py':require(identity(b)=={k:json.loads(saved)['contexts'][0]['reference_declarations']['source']['source'][k] for k in ('bytes','sha256')},'CLEANUP-MANAGER-IDENTITY')
  else:require(b==(base/'source-evidence'/name).read_bytes(),'CLEANUP-SOURCE-IDENTITY')
  raws.append(b)
 return {'root':root,'prior_root':base,'prior_module':module(base/'code/correspondence.py','_launcher_details_predecessor'),'prior_saved':saved,'prior':json.loads(saved),'sources':tuple(raws),'coverage':module(path,'_cleanup_append_coverage')}
def sources(data):return data['sources']
def catalogue(data):return data['coverage'].compile_cleanup_append(*sources(data),data['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration'],data['prior']['contexts'][0]['reference_declarations'])
def _public_predecessor(data):
 """One actual unmodified public validation; passive return observation only.
 No predecessor function, source, output or validation expectation is replaced.
 A busy monitoring slot or missing return is a conflict, not a fallback route.
 """
 p=data['prior_module'];sm=getattr(sys,'monitoring',None);require(sm is not None,'CLEANUP-MONITORING-UNAVAILABLE');require(sm.get_tool(3) is None,'CLEANUP-MONITORING-CONTENTION')
 captures=[];basis_code=p._basis.__code__
 # Private live name object identifies this invocation even if interruption
 # occurs after C-level reservation but before another Python statement.
 lease='cleanup-append-authenticated-predecessor:'+str(id(captures))
 try:
  sm.use_tool_id(3,lease)
  def capture(code,offset,value):
   require(code is p._basis.__code__ and len(captures)==0,'CLEANUP-UNEXPECTED-BASIS-RETURN');captures.append(value)
  sm.register_callback(3,sm.events.PY_RETURN,capture)
  sm.set_local_events(3,basis_code,sm.events.PY_RETURN)
  result=p.validate(data['prior_root'],data['prior_saved'])
 finally:
  # Do not release a foreign reservation, including a failed acquisition race.
  # CPython's recorded name object is the lease marker; no value-only match.
  if sm.get_tool(3) is lease:
   try:
    sm.set_local_events(3,basis_code,0)
   finally:
    try:
     sm.register_callback(3,sm.events.PY_RETURN,None)
    finally:
     sm.free_tool_id(3)
 require(result.get('result')=='PASS' and result.get('contexts')==list(CONTEXTS) and result.get('receipt')==PREDECESSOR_RECEIPT and len(captures)==1,'CLEANUP-PUBLIC-PREDECESSOR-RESULT')
 basis=captures[0];require(p.enc(p._assemble(basis['fresh'],p._rows(basis),basis))==data['prior_saved'],'CLEANUP-AUTHENTICATED-BASIS-RECEIPT')
 return basis,copy.deepcopy(result)
def _inner(pb):return pb['prior_module'].inner(pb['prior_basis']['fresh'])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module'];inner=_inner(pb)
 require(sources(fresh)==(*p.sources(pb['fresh'])[:2],inner['manager']),'CLEANUP-AUTHENTICATED-SOURCES')
 reference=pb['prior']['contexts'][0]['reference_declarations']
 for row in pb['prior']['contexts']:same(row['reference_declarations'],reference,'CLEANUP-AUTHENTICATED-REFERENCE-CONTEXTS')
 cat=fresh['coverage'].compile_cleanup_append(*sources(fresh),pb['catalogue'],reference)
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence']),'inner':inner}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'CLEANUP-CONTEXT-DOMAIN');out=[]
 for old in basis['prior']['contexts']:
  parent=old['launcher_initial_details_correspondence'];cat=basis['catalogue']
  out.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),
   'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Completed details assignment with selected original constructor error pending and no replacement',
   'local_reference_continuity':'Explicit conditional premise; selected raw None and handoff manager, not an arbitrary object or observed identity',
   'close_return_vs_append':'Separate operations in one try; later append failure preserves established normal close return',
   'runtime_cleanup_append_chain':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'error_report_append_expanded':False,'later_iterations_complete':False,'outer_cleanup_complete':False,'gap':'No runtime selected-object close/append chain or physical cleanup/retention proof; line172 and later remain unexpanded.'})
 return out
def _check_rows(basis,claims):exact(claims,'CLEANUP-SEMANTIC-CLAIMS');same(claims,_rows(basis),'CLEANUP-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'CLEANUP-EVIDENCE-TYPES');require(candidate==basis['evidence'],'CLEANUP-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'CLEANUP-CATALOGUE');exact(claims,'CLEANUP-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'CLEANUP-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'CLEANUP-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'CLEANUP-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'CLEANUP-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'CLEANUP-CATALOGUE');exact(claims,'CLEANUP-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-EXCEPTIONAL-CLEANUP-APPEND-CORRESPONDENCE-1';result['prior_launcher_details_components']=result.pop('extension_components');result['prior_launcher_details_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_cleanup_append_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','exact_generated_strings_bytes':None,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'error_report_append_expanded':False,'later_iterations_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_cleanup_append(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def close_scope(anchor,invocation):return {'acquisition':anchor['record']['acquisition'],'instance':'validated-instance:'+hashlib.sha256(enc(anchor['instance'])).hexdigest(),'invocation':invocation+'/exceptional-managed-close'}
def _premises(basis,case):
 exact(case,'CLEANUP-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','close_case','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','CLEANUP-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'CLEANUP-CONSTRUCTED-CONTEXT');anchor=rows[0]['launcher_initial_details_correspondence']['instance_anchor'];same(case['anchor'],anchor,'CLEANUP-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'CLEANUP-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'CLEANUP-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'CLEANUP-VALIDATED-PARENT-OUTPUT')
 binding=case['binding'];require(type(binding) is dict and 'continuity' in binding,'CLEANUP-BINDING-INPUT')
 expected=basis['fresh']['coverage'].cleanup_append_binding(basis['catalogue'],parent,anchor,binding['continuity']);same(binding,expected,'CLEANUP-EXPECTED-BINDING')
 cc=case['close_case'];cr=None
 if cc is not None:
  exact(cc,'CLEANUP-CLOSE-CASE');require(type(cc) is dict,'CLEANUP-CLOSE-CASE');same(cc.get('scope'),close_scope(anchor,case['invocation']),'CLEANUP-CLOSE-SCOPE');require(cc.get('context')==case['context'] and cc.get('method')=='close','CLEANUP-CLOSE-RECEIVER-METHOD')
  d=basis['inner'];g=d['guards'];cr=basis['fresh']['coverage'].constructed_reference_path(d['manager'],g['guard_relationships'],g['guard_oracle'],cc)
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':expected,'close_result':cr,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.cleanup_append_projection(cat,case['projection'],v);c.validate_cleanup_append_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'CLEANUP-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'CLEANUP-PRIOR-INPUT');require(type(branch) is str and branch in ('details','client-construction','control-construction','control','bare','stored-client','stored-normal','normal-token'),'CLEANUP-PRIOR-BRANCH')
 if branch=='details':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_cleanup_append(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'CLEANUP-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-EXCEPTIONAL-CLEANUP-APPEND-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'CLEANUP-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'CLEANUP-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_cleanup_append_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
