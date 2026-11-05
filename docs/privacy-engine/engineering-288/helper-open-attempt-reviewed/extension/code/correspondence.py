"""Bounded mandatory helper-entry and exclusive-binary open call-attempt correspondence."""
import copy,hashlib,json,os,stat,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 405785, 'sha256': 'ebe179920f8051ff259648a0ec3b0bedbee61352a078865098f0a034a22538b6'}
PREDECESSOR_MANIFEST={'bytes': 1610560, 'sha256': '219e8b5acb24abf708c04bb3824a3e259f7b808b213d92ab566b2d4e00d4213d'}
PREDECESSOR_RECEIPT={'bytes': 17227133, 'sha256': '6d27fa6e1bc6acb56b492f959efea87f15b3febb3d9e299e7f42275178bc1579'}
CONTEXTS=('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO')
RELATION='helper_open_attempt_correspondence'
REQUIRED={'cleanup_loop_exhaustion_correspondence', 'callback_stored_failure_correspondence', 'launcher_initial_details_correspondence', 'token_registration_correspondence', 'control_exception_revocation_correspondence', 'cleanup_error_report_correspondence', 'stored_failure_revocation_correspondence', 'helper_open_attempt_correspondence', 'client_construction_none_correspondence', 'callback_bare_rethrow_correspondence', 'write_call_correspondence', 'exceptional_cleanup_append_correspondence', 'control_construction_revocation_correspondence'}
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
 root=Path(root);base=root/'retained/write-call'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'OPEN-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'OPEN-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'OPEN-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'OPEN-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'OPEN-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'OPEN-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'OPEN-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode) and identity(path.read_bytes())==PRODUCER_PIN,'OPEN-PRODUCER-PIN')
 saved=(base/'receipts/prepared-write-call-replacement.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT,'OPEN-PREDECESSOR-RECEIPT-PIN')
 raws=[]
 for name in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):
  p=root/'source-evidence'/name;require(stat.S_ISREG(p.lstat().st_mode),'OPEN-SOURCE-TYPE');b=p.read_bytes();
  if name=='live_connection.py':require(identity(b)=={k:json.loads(saved)['contexts'][0]['reference_declarations']['source']['source'][k] for k in ('bytes','sha256')},'OPEN-MANAGER-IDENTITY')
  else:require(b==(base/'source-evidence'/name).read_bytes(),'OPEN-SOURCE-IDENTITY')
  raws.append(b)
 return {'root':root,'prior_root':base,'prior_module':module(base/'code/correspondence.py','_write_call_predecessor'),'prior_saved':saved,'prior':json.loads(saved),'sources':tuple(raws),'coverage':module(path,'_helper_open_attempt')}

def sources(data):return data['sources']

def _public_predecessor(data):
 """One actual unmodified public validation; passive return observation only.
 No predecessor function, source, output or validation expectation is replaced.
 A busy monitoring slot or missing return is a conflict, not a fallback route.
 """
 p=data['prior_module'];sm=getattr(sys,'monitoring',None);require(sm is not None,'OPEN-MONITORING-UNAVAILABLE');require(sm.get_tool(0) is None,'OPEN-MONITORING-CONTENTION')
 captures=[];basis_code=p._basis.__code__
 # Private live name object identifies this invocation even if interruption
 # occurs after C-level reservation but before another Python statement.
 lease='helper-open-authenticated-predecessor:'+str(id(captures))
 try:
  sm.use_tool_id(0,lease)
  def capture(code,offset,value):
   require(code is p._basis.__code__ and len(captures)==0,'OPEN-UNEXPECTED-BASIS-RETURN');captures.append(value)
  sm.register_callback(0,sm.events.PY_RETURN,capture)
  sm.set_local_events(0,basis_code,sm.events.PY_RETURN)
  result=p.validate(data['prior_root'],data['prior_saved'])
 finally:
  # Do not release a foreign reservation, including a failed acquisition race.
  # CPython's recorded name object is the lease marker; no value-only match.
  if sm.get_tool(0) is lease:
   try:
    sm.set_local_events(0,basis_code,0)
   finally:
    try:
     sm.register_callback(0,sm.events.PY_RETURN,None)
    finally:
     sm.free_tool_id(0)
 require(result.get('result')=='PASS' and result.get('contexts')==list(CONTEXTS) and result.get('receipt')==PREDECESSOR_RECEIPT and len(captures)==1,'OPEN-PUBLIC-PREDECESSOR-RESULT')
 basis=captures[0];require(p.enc(p._assemble(basis['fresh'],p._rows(basis),basis))==data['prior_saved'],'OPEN-AUTHENTICATED-BASIS-RECEIPT')
 return basis,copy.deepcopy(result)
def catalogue(data):
 row=data['prior']['contexts'][0]
 return data['coverage'].compile_helper_open(*sources(data),*[row[k]['declaration'] for k in ('write_call_correspondence','cleanup_loop_exhaustion_correspondence','cleanup_error_report_correspondence','exceptional_cleanup_append_correspondence')])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh']),'OPEN-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_helper_open(*sources(fresh),pb['catalogue'],pb['prior_basis']['catalogue'],pb['prior_basis']['prior_basis']['catalogue'],pb['prior_basis']['prior_basis']['prior_basis']['catalogue'])
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'OPEN-CONTEXTS');rows=[]
 for old in basis['prior']['contexts']:
  parent=old['write_call_correspondence'];cat=basis['catalogue']
  rows.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(parent['session_binding']),'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source':copy.deepcopy(d['source']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Actual validated write_new call attempt; original constructor pending, no replacement; explicit conditional helper entry and invocation/owner/token/callable/argument/reference continuity',
   'parameter_semantics':cat['source']['parameter_contract'],'partial_effects':'Acknowledged prior facts and UNKNOWN append effects preserved','runtime_helper_open_chain':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'pid_value':None,'directory_count_value':None,'filename_value':None,'concrete_path':None,'helper_entry_observed':False,'open_call_observed':False,'open_return_established':False,'outer_cleanup_complete':False,'gap':'Static conditional source relation only; runtime arrival, parameter/reference forwarding and open effects unobserved'})
 return rows
def _check_rows(basis,claims):exact(claims,'OPEN-SEMANTIC-CLAIMS');same(claims,_rows(basis),'OPEN-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'OPEN-EVIDENCE-TYPES');require(candidate==basis['evidence'],'OPEN-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'OPEN-CATALOGUE');exact(claims,'OPEN-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'OPEN-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'OPEN-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'OPEN-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'OPEN-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'OPEN-CATALOGUE');exact(claims,'OPEN-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-HELPER-OPEN-ATTEMPT-1';result['prior_write_call_components']=result.pop('extension_components');result['prior_write_call_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_helper_open_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','explicit_entry_required':True,'source_reference_forwarding_not_observed_identity':True,'pid_count_filename':None,'earlier_partial_effects_preserved':True,'stop':'open call attempt; before return or effects','open_return_established':False,'file_creation_established':False,'context_manager_entry_established':False,'f_binding_established':False,'line175_suppression_established':False,'final_rethrow_established':False,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_helper_open(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'OPEN-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-HELPER-OPEN-ATTEMPT','OPEN-CONSTRUCTED-CASE')
 indices=[i for i,r in enumerate(basis['prior']['contexts']) if r['context']==case['context']];require(len(indices)==1,'OPEN-CONTEXT');i=indices[0];anchor=basis['prior']['contexts'][i]['write_call_correspondence']['instance_anchor'];same(case['anchor'],anchor,'OPEN-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'OPEN-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'OPEN-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'OPEN-VALIDATED-PARENT')
 b=case['binding'];require(type(b) is dict and 'continuity' in b,'OPEN-BINDING');expected=basis['fresh']['coverage'].helper_open_binding(basis['catalogue'],parent,anchor,b['continuity']);same(b,expected,'OPEN-EXPECTED-BINDING')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.helper_open_projection(cat,case['projection'],v);c.validate_helper_open_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'OPEN-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'OPEN-PRIOR-INPUT');require(type(branch) is str,'OPEN-PRIOR-BRANCH')
 if branch=='write-call':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_helper_open(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'OPEN-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-HELPER-OPEN-ATTEMPT-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'OPEN-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'OPEN-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_helper_open_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
