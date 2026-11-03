"""NEW replacement mandatory line174 evaluation and call-attempt correspondence."""
import copy,hashlib,json,os,stat,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRODUCER_PIN={'bytes': 390668, 'sha256': '275ffd661afa020a33bc2dbf7bd24cd6371ec08d3a81f38af73b087f52377ba3'}
PREDECESSOR_MANIFEST={'bytes': 1551485, 'sha256': '72cf251ceca9dcfbc531967a5db8f891be23aed7720aa67535367c95a79a2de7'}
PREDECESSOR_RECEIPT={'bytes': 16960806, 'sha256': 'f296a50dd9fa74a405c7965662b7594594cc18da454b379bb25cf9c41fe1b842'}
CONTEXTS=('SYMBOLIC-U-ONE', 'SYMBOLIC-U-TWO')
RELATION='write_call_correspondence'
REQUIRED={'cleanup_loop_exhaustion_correspondence','control_exception_revocation_correspondence', 'launcher_initial_details_correspondence', 'callback_stored_failure_correspondence', 'stored_failure_revocation_correspondence', 'client_construction_none_correspondence', 'exceptional_cleanup_append_correspondence', 'control_construction_revocation_correspondence', 'callback_bare_rethrow_correspondence', 'cleanup_error_report_correspondence', 'write_call_correspondence', 'token_registration_correspondence'}
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
 root=Path(root);base=root/'retained/loop'
 for p in (root,root/'retained',base):require(stat.S_ISDIR(p.lstat().st_mode),'WC-ROOT-TYPE')
 mp=base/'MANIFEST.json';require(stat.S_ISREG(mp.lstat().st_mode),'WC-MANIFEST-TYPE');raw=mp.read_bytes();require(identity(raw)==PREDECESSOR_MANIFEST,'WC-PREDECESSOR-MANIFEST')
 manifest=json.loads(raw);expected=set(manifest)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):require(n in dirs,'WC-UNDECLARED-DIRECTORY');seen.add(n);walk(p)
   else:require(stat.S_ISREG(mode) and n in expected,'WC-UNDECLARED-OR-NONREGULAR');files.add(n)
 walk(base);require(files==expected and seen==dirs,'WC-PREDECESSOR-MEMBERSHIP')
 for n,pin in manifest.items():require(identity((base/n).read_bytes())==pin,'WC-PREDECESSOR-BYTES:'+n)
 return base

def inputs(root=ROOT):
 root=Path(root);base=predecessor_root(root);path=root/'code/managed_coverage.py';require(stat.S_ISREG(path.lstat().st_mode) and identity(path.read_bytes())==PRODUCER_PIN,'WC-PRODUCER-PIN')
 saved=(base/'receipts/prepared-cleanup-loop.json').read_bytes();require(identity(saved)==PREDECESSOR_RECEIPT,'WC-PREDECESSOR-RECEIPT-PIN')
 raws=[]
 for name in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):
  p=root/'source-evidence'/name;require(stat.S_ISREG(p.lstat().st_mode),'WC-SOURCE-TYPE');b=p.read_bytes();
  if name=='live_connection.py':require(identity(b)=={k:json.loads(saved)['contexts'][0]['reference_declarations']['source']['source'][k] for k in ('bytes','sha256')},'WC-MANAGER-IDENTITY')
  else:require(b==(base/'source-evidence'/name).read_bytes(),'WC-SOURCE-IDENTITY')
  raws.append(b)
 return {'root':root,'prior_root':base,'prior_module':module(base/'code/correspondence.py','_loop_predecessor'),'prior_saved':saved,'prior':json.loads(saved),'sources':tuple(raws),'coverage':module(path,'_write_call_replacement')}

def sources(data):return data['sources']

def _public_predecessor(data):
 """One actual unmodified public validation; passive return observation only.
 No predecessor function, source, output or validation expectation is replaced.
 A busy monitoring slot or missing return is a conflict, not a fallback route.
 """
 p=data['prior_module'];sm=getattr(sys,'monitoring',None);require(sm is not None,'WC-MONITORING-UNAVAILABLE');require(sm.get_tool(1) is None,'WC-MONITORING-CONTENTION')
 captures=[];basis_code=p._basis.__code__
 # Private live name object identifies this invocation even if interruption
 # occurs after C-level reservation but before another Python statement.
 lease='write-call-replacement-authenticated-predecessor:'+str(id(captures))
 try:
  sm.use_tool_id(1,lease)
  def capture(code,offset,value):
   require(code is p._basis.__code__ and len(captures)==0,'WC-UNEXPECTED-BASIS-RETURN');captures.append(value)
  sm.register_callback(1,sm.events.PY_RETURN,capture)
  sm.set_local_events(1,basis_code,sm.events.PY_RETURN)
  result=p.validate(data['prior_root'],data['prior_saved'])
 finally:
  # Do not release a foreign reservation, including a failed acquisition race.
  # CPython's recorded name object is the lease marker; no value-only match.
  if sm.get_tool(1) is lease:
   try:
    sm.set_local_events(1,basis_code,0)
   finally:
    try:
     sm.register_callback(1,sm.events.PY_RETURN,None)
    finally:
     sm.free_tool_id(1)
 require(result.get('result')=='PASS' and result.get('contexts')==list(CONTEXTS) and result.get('receipt')==PREDECESSOR_RECEIPT and len(captures)==1,'WC-PUBLIC-PREDECESSOR-RESULT')
 basis=captures[0];require(p.enc(p._assemble(basis['fresh'],p._rows(basis),basis))==data['prior_saved'],'WC-AUTHENTICATED-BASIS-RECEIPT')
 return basis,copy.deepcopy(result)
def catalogue(data):
 row=data['prior']['contexts'][0]
 return data['coverage'].compile_write_call(*sources(data),row['cleanup_loop_exhaustion_correspondence']['declaration'],row['cleanup_error_report_correspondence']['declaration'],row['exceptional_cleanup_append_correspondence']['declaration'])
def _basis(data):
 fresh=inputs(data['root']);pb,public=_public_predecessor(fresh);p=fresh['prior_module']
 require(sources(fresh)==p.sources(pb['fresh']),'WC-AUTHENTICATED-SOURCES')
 cat=fresh['coverage'].compile_write_call(*sources(fresh),pb['catalogue'],pb['prior_basis']['catalogue'],pb['prior_basis']['prior_basis']['catalogue'])
 basis={'fresh':fresh,'prior':copy.deepcopy(fresh['prior']),'prior_basis':pb,'prior_module':p,'public_predecessor':public,'catalogue':cat,'evidence':dict(pb['evidence'])}
 basis['session_bindings']=[_session_binding(basis,row) for row in basis['prior']['contexts']]
 return basis
def _rows(basis):
 require(tuple(x['context'] for x in basis['prior']['contexts'])==CONTEXTS,'WC-CONTEXTS');rows=[]
 for i,old in enumerate(basis['prior']['contexts']):
  parent=old['cleanup_loop_exhaustion_correspondence'];cat=basis['catalogue']
  rows.append({'context':old['context'],'declaration':copy.deepcopy(cat),'instance_anchor':copy.deepcopy(parent['instance_anchor']),'scope':copy.deepcopy(parent['scope']),'reference_basis':copy.deepcopy(parent['reference_basis']),'session_binding':copy.deepcopy(basis['session_bindings'][i]),'predecessor_receipt':PREDECESSOR_RECEIPT.copy(),'predecessor_public_validation':copy.deepcopy(basis['public_predecessor']),
   'conditional_links':[{'declaration':d['id'],'source':copy.deepcopy(d['source']),'invocation':None,'frame':None,'observed_value':None} for d in cat['declarations']],
   'required_parent':'Actual validated completed loop; original constructor pending, no replacement; explicit continuation and conditional owner/lookup/reference/error continuity',
   'partial_effects':'Acknowledged close/reporting facts and UNKNOWN earlier append effects retained','runtime_write_call_chain':None,'classification':'UNKNOWN','multiplicity':None,'ordinal':None,'actual_invocation_count':None,'observer_join':None,'separate_observer':copy.deepcopy(parent['separate_observer']),
   'pid_value':None,'directory_count_value':None,'filename_value':None,'write_call_attempt_observed':False,'write_new_body_established':False,'outer_cleanup_complete':False,'gap':'Static conditional correspondence only; no helper body, suppression, final rethrow or physical cleanup'})
 return rows
def _check_rows(basis,claims):exact(claims,'WC-SEMANTIC-CLAIMS');same(claims,_rows(basis),'WC-SEMANTIC-CORRESPONDENCE')
def _compare_evidence(basis,candidate):
 require(type(candidate) is dict and all(type(k) is str and type(v) is bytes for k,v in candidate.items()),'WC-EVIDENCE-TYPES');require(candidate==basis['evidence'],'WC-VALIDATED-EVIDENCE')
def _check_candidate(basis,data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'WC-CATALOGUE');exact(claims,'WC-CLAIMS')
 same(submitted_catalogue,basis['catalogue'],'WC-CATALOGUE-SOURCE');require(sources(data)==sources(basis['fresh']) and all(type(x) is bytes for x in sources(data)),'WC-CANDIDATE-SOURCE');same(data['prior'],basis['prior'],'WC-CANDIDATE-PREDECESSOR')
 require(type(data['prior_saved']) is bytes and data['prior_saved']==basis['fresh']['prior_saved'],'WC-CANDIDATE-RECEIPT')
 if evidence is not None:_compare_evidence(basis,evidence)
 if claims is not None:_check_rows(basis,claims)
 return _rows(basis)
def _checked(data,submitted_catalogue,claims=None,evidence=None):
 exact(submitted_catalogue,'WC-CATALOGUE');exact(claims,'WC-CLAIMS');basis=_basis(data)
 return _check_candidate(basis,data,submitted_catalogue,claims,evidence),basis
def semantic(data,submitted_catalogue,claims=None,evidence=None):
 rows,_=_checked(data,submitted_catalogue,claims,evidence);return copy.deepcopy(rows)
def _assemble(data,rows,basis):
 _check_rows(basis,rows);result=copy.deepcopy(basis['prior']);result['format']='I164-WRITE-CALL-REPLACEMENT-1';result['prior_cleanup_loop_components']=result.pop('extension_components');result['prior_cleanup_loop_receipt']=PREDECESSOR_RECEIPT.copy();result['extension_components']={n:identity((Path(data['root'])/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')}
 for ctx,row in zip(result['contexts'],rows):ctx[RELATION]=copy.deepcopy(row)
 result['new_write_call_limits']={'NEW_REPLACEMENT_CONSTRUCTION':True,'unavailable_attempts_not_recovered':True,'static_conditional_slice':True,'runtime_chain':'UNAVAILABLE','pid_count_filename':None,'earlier_partial_effects_preserved':True,'write_new_body_established':False,'line175_suppression_established':False,'final_rethrow_established':False,'outer_cleanup_complete':False,'complete_repetition_coverage':False,'all_eleven_obligations_preserved':True,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False};return result
def derive_write_call(data,submitted_catalogue,claims=None,evidence=None):
 rows,basis=_checked(data,submitted_catalogue,claims,evidence);return _assemble(data,rows,basis)
def _premises(basis,case):
 exact(case,'WC-CONSTRUCTED-INPUT');require(type(case) is dict and set(case)=={'kind','context','anchor','invocation','parent_case','parent_output','session_binding','binding','outcomes','projection','output'} and case['kind']=='CONSTRUCTED-WRITE-CALL-REPLACEMENT','WC-CONSTRUCTED-CASE')
 indices=[i for i,r in enumerate(basis['prior']['contexts']) if r['context']==case['context']];require(len(indices)==1,'WC-CONTEXT');i=indices[0];anchor=basis['prior']['contexts'][i]['cleanup_loop_exhaustion_correspondence']['instance_anchor'];same(case['anchor'],anchor,'WC-CONSTRUCTED-ANCHOR')
 pc=case['parent_case'];require(type(pc) is dict,'WC-PARENT-CASE');same({k:pc.get(k) for k in ('context','anchor','invocation')},{k:case[k] for k in ('context','anchor','invocation')},'WC-PARENT-INVOCATION')
 parent=basis['prior_module']._construct_checked(basis['prior_basis'],pc)['projection'];same(case['parent_output'],parent,'WC-VALIDATED-PARENT')
 sb=basis['session_bindings'][i];same(case['session_binding'],sb,'WC-VALIDATED-DESTINATION');b=case['binding'];require(type(b) is dict and 'continuity' in b,'WC-BINDING')
 expected=basis['fresh']['coverage'].write_call_binding(basis['catalogue'],parent,anchor,sb,b['continuity']);same(b,expected,'WC-EXPECTED-BINDING')
 return {'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':parent,'session_binding':copy.deepcopy(sb),'binding':expected,'outcomes':copy.deepcopy(case['outcomes'])}
def _construct_checked(basis,case):
 v=_premises(basis,case);c=basis['fresh']['coverage'];cat=basis['catalogue'];out=c.write_call_projection(cat,case['projection'],v);c.validate_write_call_projection(cat,case['projection'],v,case['output']);return {'kind':case['kind'],'context':case['context'],'anchor':copy.deepcopy(case['anchor']),'projection':out,'runtime_observation':False}
def constructed_projection(data,submitted_catalogue,case):
 exact(case,'WC-CONSTRUCTED-INPUT');_,basis=_checked(data,submitted_catalogue);return _construct_checked(basis,case)
def _construct_prior(basis,branch,case):
 exact(case,'WC-PRIOR-INPUT');require(type(branch) is str,'WC-PRIOR-BRANCH')
 if branch=='cleanup-loop':return basis['prior_module']._construct_checked(basis['prior_basis'],case)
 return basis['prior_module']._construct_prior(basis['prior_basis'],branch,case)
def constructed_prior(data,submitted_catalogue,branch,case):
 _,basis=_checked(data,submitted_catalogue);return _construct_prior(basis,branch,case)
def derive(root=ROOT):
 data=inputs(root);return derive_write_call(data,catalogue(data))
def _receipt_shape(saved):
 require(type(saved) is bytes,'WC-RECEIPT-BYTES');v=json.loads(saved)
 require(type(v) is dict and v.get('format')=='I164-WRITE-CALL-REPLACEMENT-1' and type(v.get('contexts')) is list and len(v['contexts'])==2 and all(type(c) is dict and REQUIRED<=set(c) for c in v['contexts']),'WC-MANDATORY-RELATIONS');return v
def _receipt_checked(basis,saved):
 _receipt_shape(saved);require(saved==enc(_assemble(basis['fresh'],_rows(basis),basis)),'WC-STALE-OR-ALTERED-RECEIPT');return {'result':'PASS','contexts':list(CONTEXTS),'receipt':identity(saved),'runtime_write_call_chain':'UNAVAILABLE','actual_admission':False}
def validate(root,saved):
 _receipt_shape(saved);data=inputs(root);_,basis=_checked(data,catalogue(data));return _receipt_checked(basis,saved)

def _session_binding(basis,row):
 anchor=row['cleanup_loop_exhaustion_correspondence']['instance_anchor'];e=basis['evidence'];sp='evidence/SMOKE-ABOUT-TO-START.json';bp='evidence/session-records/binding.json';s=json.loads(e[sp]);b=json.loads(e[bp])
 require(type(s['destination']) is str and b['configuration']['config']['session']==anchor['instance']['session_label'],'WC-DESTINATION-INSTANCE');same(b['launcher'],basis['catalogue']['source']['sources']['launcher'],'WC-DESTINATION-SOURCE')
 value={'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'recorded_destination':s['destination'],'start_record':{'path':sp,'identity':identity(e[sp]),'pointer':'/destination'},'binding_record':{'path':bp,'identity':identity(e[bp]),'pointer':'/configuration/config/session'},'source_owner_lock':copy.deepcopy(basis['catalogue']['source']['owner_lock']),'physical_resolved_destination':None,'resolution':'owner_lock yields dest after parent.resolve(); recorded destination is nominal, no host resolution performed'}
 same(value,row['normal_session_exit_correspondence']['session_binding'],'WC-INHERITED-SESSION');same(value,row['owner_lock_finalization_correspondence']['session_binding'],'WC-INHERITED-OWNER');return value

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();print(json.dumps(validate(a.root,a.receipt.read_bytes()),sort_keys=True))
