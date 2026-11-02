"""Mandatory bounded selected-cleanup-error handler and error-item append correspondence."""
import copy,hashlib,json,os,stat,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 359095, 'sha256': '9ff824c19f06f6077e2b6cf0bb3ac613c4193d96a6457ec6c02b85440f205793'}
PREDECESSOR_MANIFEST={'bytes': 1415643, 'sha256': 'dd11a30a719b7058ed084ad700c27cf66abd9040d37235f2b6ad9a5152c44e53'}
PREDECESSOR_RECEIPT={'bytes': 13408039, 'sha256': '4b84be0804b2a0a5dd0cef421403fa2e608a703899c97196f4063b11b04df952'}
CONTEXTS=('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO')
RELATION='cleanup_error_report_correspondence'
REQUIRED={'control_exception_revocation_correspondence', 'launcher_initial_details_correspondence', 'callback_stored_failure_correspondence', 'stored_failure_revocation_correspondence', 'client_construction_none_correspondence', 'exceptional_cleanup_append_correspondence', 'control_construction_revocation_correspondence', 'callback_bare_rethrow_correspondence', 'cleanup_error_report_correspondence', 'token_registration_correspondence'}
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
 root=Path(root);base=root/'retained/cleanup'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'REPORT-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'REPORT-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'REPORT-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'REPORT-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'REPORT-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'REPORT-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'REPORT-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode) and identity(path.read_bytes())==PRODUCER_PIN,'REPORT-PRODUCER-PIN')
 saved=(base/'ec01/receipts/prepared-cleanup-append.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT,'REPORT-PREDECESSOR-RECEIPT-PIN')
 raws=[]
 for name in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):
  p=root/'source-evidence'/name;require(stat.S_ISREG(p.lstat().st_mode),'REPORT-SOURCE-TYPE');b=p.read_bytes();
  if name=='live_connection.py':require(identity(b)=={k:json.loads(saved)['contexts'][0]['reference_declarations']['source']['source'][k] for k in ('bytes','sha256')},'REPORT-MANAGER-IDENTITY')
  else:require(b==(base/'source-evidence'/name).read_bytes(),'REPORT-SOURCE-IDENTITY')
  raws.append(b)
 return {'root':root,'prior_root':base,'prior_module':module(base/'code/correspondence.py','_cleanup_append_predecessor'),'prior_saved':saved,'prior':json.loads(saved),'sources':tuple(raws),'coverage':module(path,'_error_report_coverage')}

def sources(data):return data['sources']

def _public_predecessor(data):
 """One actual unmodified public validation; passive return observation only.
 No predecessor function, source, output or validation expectation is replaced.
 A busy monitoring slot or missing return is a conflict, not a fallback route.
 """
 p=data['prior_module'];sm=getattr(sys,'monitoring',None);require(sm is not None,'REPORT-MONITORING-UNAVAILABLE');require(sm.get_tool(4) is None,'REPORT-MONITORING-CONTENTION')
 captures=[];basis_code=p._basis.__code__
 # Private live name object identifies this invocation even if interruption
 # occurs after C-level reservation but before another Python statement.
 lease='error-report-authenticated-predecessor:'+str(id(captures))
 try:
  sm.use_tool_id(4,lease)
  def capture(code,offset,value):
   require(code is p._basis.__code__ and len(captures)==0,'REPORT-UNEXPECTED-BASIS-RETURN');captures.append(value)
  sm.register_callback(4,sm.events.PY_RETURN,capture)
  sm.set_local_events(4,basis_code,sm.events.PY_RETURN)
  result=p.validate(data['prior_root'],data['prior_saved'])
 finally:
  # Do not release a foreign reservation, including a failed acquisition race.
  # CPython's recorded name object is the lease marker; no value-only match.
  if sm.get_tool(4) is lease:
   try:
    sm.set_local_events(4,basis_code,0)
   finally:
    try:
     sm.register_callback(4,sm.events.PY_RETURN,None)
    finally:
     sm.free_tool_id(4)
 require(result.get('result')=='PASS' and result.get('contexts')==list(CONTEXTS) and result.get('receipt')==PREDECESSOR_RECEIPT and len(captures)==1,'REPORT-PUBLIC-PREDECESSOR-RESULT')
 basis=captures[0];require(p.enc(p._assemble(basis['fresh'],p._rows(basis),basis))==data['prior_saved'],'REPORT-AUTHENTICATED-BASIS-RECEIPT')
 return basis,copy.deepcopy(result)
def catalogue(data):
 return data['coverage'].compile_error_report(*sources(data),data['prior']['contexts'][0]['exceptional_cleanup_append_correspondence']['declaration'])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh']),'REPORT-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_error_report(*sources(fresh),pb['catalogue'])
 return {'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'REPORT-CONTEXT-DOMAIN');rows=[]
 for old in basis['prior']['contexts']:
  parent=old['exceptional_cleanup_append_correspondence'];cat=basis['catalogue']
  rows.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),
   'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source_origin':copy.deepcopy(d['source_origin']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Validated selected raise in protected close/normal-append try; exact occurrence and pending selected error',
   'selected_error_continuity':'Explicit conditional delivery and owner/local/name/details/list/method continuity; not observed reference identity',
   'partial_effects':'An earlier uncertain append remains uncertain even after error-item append completes',
   'runtime_error_report_chain':None,'physical_reference_observation':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'handler_exit_established':False,'later_iterations_complete':False,'outer_cleanup_complete':False,'gap':'No runtime selected-error catch/evaluation/append chain; later cleanup and physical effects remain unestablished'})
 return rows
def _check_rows(basis,claims):exact(claims,'REPORT-SEMANTIC-CLAIMS');same(claims,_rows(basis),'REPORT-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'REPORT-EVIDENCE-TYPES');require(candidate==basis['evidence'],'REPORT-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'REPORT-CATALOGUE');exact(claims,'REPORT-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'REPORT-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'REPORT-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'REPORT-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'REPORT-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'REPORT-CATALOGUE');exact(claims,'REPORT-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-CLEANUP-ERROR-REPORT-CORRESPONDENCE-1';result['prior_cleanup_append_components']=result.pop('extension_components');result['prior_cleanup_append_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_error_report_limits']={'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','exact_generated_strings_bytes':None,'earlier_partial_effects_preserved':True,'handler_exit_established':False,'non_none_constructor_branch_complete':False,'outer_cleanup_complete':False,'later_iterations_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_error_report(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'REPORT-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-CLEANUP-ERROR-REPORT','REPORT-CONSTRUCTED-CASE')
 rows=[r for r in basis['prior']['contexts'] if r['context']==case['context']];require(len(rows)==1,'REPORT-CONSTRUCTED-CONTEXT');anchor=rows[0]['exceptional_cleanup_append_correspondence']['instance_anchor'];same(case['anchor'],anchor,'REPORT-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'REPORT-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'REPORT-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'REPORT-VALIDATED-PARENT-OUTPUT')
 binding=case['binding'];require(type(binding) is dict and 'continuity' in binding,'REPORT-BINDING-INPUT')
 expected=basis['fresh']['coverage'].error_report_binding(basis['catalogue'],parent,anchor,binding['continuity']);same(binding,expected,'REPORT-EXPECTED-BINDING')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.error_report_projection(cat,case['projection'],v);c.validate_error_report_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'REPORT-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'REPORT-PRIOR-INPUT');require(type(branch) is str,'REPORT-PRIOR-BRANCH')
 if branch=='cleanup':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_error_report(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'REPORT-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-CLEANUP-ERROR-REPORT-CORRESPONDENCE-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'REPORT-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'REPORT-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_error_report_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
