"""Formal-Lab[6] independent line2516 controls. Pure source/model only; never authentication.
Oracle: pinned BEFORE_WITH has completed res assignment; a separate continuation
must reach the following enter decrement, before any test of res. NULL is allowed.
No macro body, decref completion, context entry, physical effect or runtime identity.
Retained parent fixtures are premises with prior scoped support, NOT live bases.
"""
from pathlib import Path
import sys,types,json,copy,ast,hashlib,os,time,traceback,platform,importlib.metadata,collections
B=Path(__file__).resolve().parent;R=B/'candidate';O=B/'independent';O.mkdir(exist_ok=False)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def ident(x):return {'bytes':len(x),'sha256':hashlib.sha256(x).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def save(p,x):
 with p.open('xb') as f:f.write(enc(x));f.flush();os.fsync(f.fileno())
def load(p,name):
 m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
rows=[];start=time.monotonic();failures=[]
def record(name,layer,status,detail=None):
 row={'sequence':len(rows)+1,'name':name,'layer':layer,'status':status,'detail':detail};rows.append(row)
 save(O/('%04d.json'%len(rows)),row)
 with (O/'progress.jsonl').open('ab') as f:f.write(enc(row));f.flush();os.fsync(f.fileno())
 print(enc(row).decode(),end='',flush=True)
def check(name,fn,layer='independent pure-source/model assertions; no authentication'):
 try:
  value=fn();assert value is not False;record(name,layer,'PASS')
 except BaseException as e:
  record(name,layer,'FAIL',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()});failures.append(name)
def reject(name,fn,layer,code=None):
 try:fn()
 except ValueError as e:
  if code is not None and code not in str(e):record(name,layer,'FAIL',{'unexpected_rejection':str(e),'expected_contains':code});failures.append(name)
  else:record(name,layer,'REJECTED',{'exception':'ValueError','code':str(e)})
 except BaseException as e:record(name,layer,'FAIL',{'harness_or_unexpected_exception':repr(e)});failures.append(name)
 else:record(name,layer,'DEFECT-OBSERVED','invalid claim accepted');failures.append(name)
def need(x):assert x
class S(str):pass
class D(dict):pass
class L(list):pass
class I(int):pass

def run():
 c=load(R/'code/managed_coverage.py','review_only_pure_producer');a=load(R/'code/correspondence.py','review_only_adapter_definitions')
 src=[(R/'source-evidence/lab_bootstrap.py').read_bytes(),(R/'reference/cpython-3.12.14/bytecodes.c').read_bytes(),(R/'reference/cpython-3.12.14/typeobject.c').read_bytes()]
 cats=[read(R/'fixtures'/n) for n in ('r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json')]
 cat=c.compile_enter_decref(*src,*cats);save(O/'independent-catalogue.json',cat)
 lines=src[1].decode().splitlines();launch=ast.parse(src[0]);withnode=next(n for n in ast.walk(launch) if isinstance(n,ast.With) and n.lineno==24)
 check('governing statement and four distinct source occurrences',lambda:need([lines[i-1].strip() for i in (2511,2514,2515,2516,2517)]==['Py_DECREF(enter);','DECREF_INPUTS();','res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {'] and ast.unparse(withnode.items[0].context_expr)=="open(p, 'xb')"),'defining-source inspection')
 check('independently derived catalogue boundary/no res guard',lambda:need(cat['source']['operation']['line']==2516 and cat['source']['assignment']['line']==2515 and cat['source']['next_operation_excluded']['line']==2517 and cat['source']['operand_expression']=='enter' and cat['source']['res_non_NULL_guard'] is False and cat['source']['order']==['enter-decref:continuation','enter-decref:attempt'] and cat['source']['res_classes']==['C-NULL','non-NULL/opaque','non-NULL/Python-None']))
 check('canonical source catalogue accepted',lambda:c.validate_enter_decref(*src,*cats,cat),'source-derived catalogue comparison')
 for name,edit in [
  ('operand res',lambda x:x['source'].__setitem__('operand_expression','res')),
  ('wrong failed-lookup occurrence',lambda x:x['source']['operation'].__setitem__('line',2511)),
  ('inputs decrement substitution',lambda x:x['source'].__setitem__('operation_spelling','DECREF_INPUTS')),
  ('invented nonNULL guard coordinated',lambda x:(x['source'].__setitem__('res_non_NULL_guard',True),x['guard_branches'].__setitem__('res_non_NULL_guard',True))),
  ('reordered declarations and steps',lambda x:(x['source']['steps'].reverse(),x['source']['order'].reverse(),x['declarations'].reverse())),
  ('invented operation completion',lambda x:x['source']['steps'][1]['allowed'].append('completed')),
  ('missing mandatory declaration',lambda x:x['declarations'].pop()),
  ('operation line bool',lambda x:x['source']['operation'].__setitem__('line',True)),
  ('same-valued subclass key',lambda x:x['source'].__setitem__(S('operand_expression'),x['source'].pop('operand_expression'))),
 ]:
  bad=copy.deepcopy(cat);edit(bad);reject(name,lambda bad=bad:c.validate_enter_decref(*src,*cats,bad),'source-derived catalogue/type comparison')
 adapter=ast.parse((R/'code/correspondence.py').read_bytes());fn={n.name:n for n in adapter.body if isinstance(n,ast.FunctionDef)}
 calls=lambda name:[ast.unparse(n.func) for n in ast.walk(fn[name]) if isinstance(n,ast.Call)]
 check('mandatory public chain; no skipped receipt comparison',lambda:need(all(x in calls('_basis') for x in ('inputs','p._receipt_shape','p._basis','p._assemble','c.compile_enter_decref')) and 'derive' in calls('validate') and '_receipt_shape' in calls('validate') and 'require' in calls('validate') and '_basis' in calls('derive')),'static mandatory public wiring; not invoked')
 text=ast.unparse(fn['_construct_checked'])
 check('mandatory constructed parent then binding then comparison',lambda:need(text.index('._construct_checked(')<text.index('c.enter_decref_binding(')<text.index('c.validate_enter_decref_projection(') and 'parent_output' in text and 'parent_case' in text and 'invocation' in text),'static constructed wiring; UNTESTED execution')
 fixtures=read(R/'fixtures/retained-return-cases.json');assert enc(fixtures)==enc(read(B/'prior-review/independent/constructed-normal-cases.json'))
 cases=[];outs=[]
 false_fields=['post_call_decref_established','decref_completion_established','decref_effects_established','macro_expansion_established','reference_count_change_established','finalization_established','decref_callback_execution_established','physical_release_established','result_test_established','result_error_routing_established','context_manager_entry_established','f_binding_established','actual_admission','normal_overall_return_established','final_rethrow_established','helper_error_contract_established','C_NULL_implies_python_exception_established']
 preserved=['original_error_pending_in_outer_handler','retained_cleanup_error_evidence','cleanup_list_state','details_after_predecessor_acknowledged_steps','res_assignment','res_value_role','helper_c_return_completed_in_model','res_assignment_established','close_normal_return_completed_in_model','failure_origin_region','known_false_flags_preserved','existing_cause_context_suppression','helper_error_indicator']
 def make(p,continuity='explicit conditional premise',outcomes=None):
  binding=c.enter_decref_binding(cat,p,p['instance_anchor'],continuity)
  return {'scope':copy.deepcopy(p['scope']),'anchor':copy.deepcopy(p['instance_anchor']),'parent_result':copy.deepcopy(p),'binding':binding,'outcomes':copy.deepcopy(outcomes if outcomes is not None else [{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'attempted'}])}
 def oracle(o,q,attempt,terminal,replacement=False):
  p=q['parent_result'];assert o['post_call_decref_attempt_established_in_model'] is attempt and o['terminal_python_exception_in_model'] is terminal
  assert all(o[k] is False for k in false_fields)
  assert all(o[k]==p[k] for k in preserved)
  assert o['prior_acknowledged_partial_effects']==p['current_partial_effects'] and 'UNKNOWN' in o['current_partial_effects']
  assert o['binding']['operand_role']==p['binding']['method_results']['__enter__'] and o['binding']['exit_role']==p['binding']['method_results']['__exit__']
  assert o['binding']['operand_role']!=o['binding']['exit_role'] and o['binding']['operand_role']!=p['res_value_role']
  assert o['binding']['assignment_occurrence']==p['events'][-1]
  assert o['runtime_enter_decref_chain'] is None and o['observer_join'] is None
  if attempt:
   assert len(o['events'])==2 and o['decref_operation']['operand_expression']=='enter' and o['decref_operation']['source']['line']==2516
   assert o['decref_operation']['operand_role']==q['binding']['operand_role'] and o['decref_operation']['macro_expansion'] is None and o['decref_operation']['concrete_reference_count'] is None and o['decref_operation']['runtime_observation'] is False
  else:assert o['decref_operation'] is None
  if replacement:
   e=o['replacement_error_in_model'];assert e is not None and e['role']=='conditional-enter-decref-continuation-error' and e['frontier_stage']=='enter-decref:continuation'
   assert o['last_pending_error_in_model']==e and e!=p['last_pending_error_in_model'] and all(e[k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression'))
  else:assert o['last_pending_error_in_model']==p['last_pending_error_in_model'] and o['replacement_error_in_model']==p['replacement_error_in_model']
 for f in fixtures:
  q=make(f['output']);o=c.enter_decref_projection(cat,q,copy.deepcopy(q));cases.append(q);outs.append(o)
  check('attempt/'+f['name'],lambda o=o,q=q:(oracle(o,q,True,True),c.validate_enter_decref_projection(cat,q,copy.deepcopy(q),o)))
 save(O/'normal-case-index.json',[{'index':i,'parent_fixture':f['name'],'case_identity':ident(enc(q)),'output_identity':ident(enc(o))} for i,(f,q,o) in enumerate(zip(fixtures,cases,outs))])
 # Each base covers distinct context/control-prefix/failure-origin, using the NULL premise.
 for j in range(2,24,3):
  p=fixtures[j]['output'];name=fixtures[j]['name']
  for outcome,terminal,replacement in [('raise',True,True),('catchable-interruption',True,True),('process-termination',None,False),('unobserved',None,False)]:
   q=make(p,outcomes=[{'stage':'enter-decref:continuation','outcome':outcome}]);o=c.enter_decref_projection(cat,q,copy.deepcopy(q));check(name+'/continuation/'+outcome,lambda o=o,q=q,t=terminal,r=replacement:oracle(o,q,False,t,r))
  for outcome in ('process-termination','unobserved'):
   q=make(p,outcomes=[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':outcome}]);o=c.enter_decref_projection(cat,q,copy.deepcopy(q));check(name+'/operation/'+outcome,lambda o=o,q=q:oracle(o,q,False,None))
  q=make(p,'UNESTABLISHED',[{'stage':'enter-decref:continuation','outcome':'unobserved'}]);o=c.enter_decref_projection(cat,q,copy.deepcopy(q));check(name+'/UNESTABLISHED',lambda o=o,q=q:oracle(o,q,False,None))
 # Invalid sequence/premise controls run in each symbolic context, not a campaign replay.
 for j in (2,14):
  q=cases[j];o=outs[j];name=fixtures[j]['name'];layer='pure model input constraints; retained premises NOT authenticated'
  badrows=[[],q['outcomes'][1:],list(reversed(q['outcomes'])),q['outcomes']+[q['outcomes'][-1]],[{'stage':'enter-decref:continuation','outcome':'unobserved'},q['outcomes'][1]],[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'completed'}],[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'raise'}],[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'catchable-interruption'}]]
  for k,oo in enumerate(badrows):
   bad=copy.deepcopy(q);bad['outcomes']=oo;reject(name+'/bad-sequence-'+str(k),lambda b=bad:c.enter_decref_projection(cat,b,copy.deepcopy(b)),layer)
  for continuity in ('UNESTABLISHED',True,S('explicit conditional premise')):
   bad=copy.deepcopy(q);bad['binding']['continuity']=continuity;reject(name+'/invalid-continuity-'+repr(continuity),lambda b=bad:c.enter_decref_projection(cat,b,copy.deepcopy(b)),layer)
  bad=copy.deepcopy(q);del bad['binding'];reject(name+'/omitted-binding',lambda:c.enter_decref_projection(cat,bad,bad),layer)
  for field,value in [('res_assignment_established',False),('helper_c_return_completed_in_model',False),('res_assignment_established',1)]:
   p=copy.deepcopy(q['parent_result']);p[field]=value;reject(name+'/parent-'+field+'-'+repr(value),lambda p=p:c.enter_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise'),'pure parent completion/type gate; no authentication')
  for field,new in [('operand_role',q['binding']['res_value_role']),('operand_role',q['binding']['exit_role']),('assignment_occurrence',dict(q['binding']['assignment_occurrence'],id='wrong occurrence')),('references',dict(q['binding']['references'],token=q['binding']['references']['owner']))]:
   bad=copy.deepcopy(q);bad['binding'][field]=copy.deepcopy(new);reject(name+'/wrong-binding-'+field+'-'+str(len(rows)),lambda b=bad:c.enter_decref_projection(cat,b,copy.deepcopy(b)),layer)
  for key in ('context','acquisition','invocation','instance'):
   bad=copy.deepcopy(q);bad['scope'][key]='wrong';bad['binding']['scope'][key]='wrong';reject(name+'/coordinated-scope-'+key,lambda b=bad:c.enter_decref_projection(cat,b,copy.deepcopy(b)),layer)
  # Same-valued subclasses at input, output, semantic-catalogue boundaries.
  for key in ('stage','outcome'):
   bad=copy.deepcopy(q);bad['outcomes'][0][key]=S(bad['outcomes'][0][key]);reject(name+'/subclass-input-'+key,lambda b=bad:c.enter_decref_projection(cat,b,b),'exact input type before normalization','EXACT-TYPE')
  for kind in (D,L):
   bad=copy.deepcopy(q)
   if kind is D:bad['scope']=D(bad['scope'])
   else:bad['outcomes']=L(bad['outcomes'])
   reject(name+'/subclass-container-'+kind.__name__,lambda b=bad:c.enter_decref_projection(cat,b,b),'exact input container type before normalization','EXACT-TYPE')
  for key,value in [('terminal_python_exception_in_model',False),('terminal_python_exception_in_model',1),('last_pending_error_in_model',None),('original_error_pending_in_outer_handler',None),('res_value_role',None),('physical_release_established',True),('result_test_established',True),('decref_completion_established',True),('post_call_decref_attempt_established_in_model',1)]:
   bad=copy.deepcopy(o);bad[key]=value;reject(name+'/output-'+key+'-'+repr(value),lambda b=bad:c.validate_enter_decref_projection(cat,q,copy.deepcopy(q),b),'pure model output comparison; fixed selected premises','OUTPUT-CORRESPONDENCE')
  bad=copy.deepcopy(o);bad['binding']['operand_role']=copy.deepcopy(q['binding']['exit_role']);bad['decref_operation']['operand_role']=copy.deepcopy(q['binding']['exit_role']);[e.__setitem__('operand_role',copy.deepcopy(q['binding']['exit_role'])) for e in bad['events']]
  reject(name+'/coordinated-enter-exit-output-substitution',lambda:c.validate_enter_decref_projection(cat,q,copy.deepcopy(q),bad),'pure model output comparison; no archive-pin-only rejection','OUTPUT-CORRESPONDENCE')
  for path in ('value','key'):
   bad=copy.deepcopy(o)
   if path=='value':bad['decref_operation']['operand_expression']=S('enter')
   else:bad['decref_operation'][S('operand_expression')]=bad['decref_operation'].pop('operand_expression')
   reject(name+'/subclass-output-'+path,lambda b=bad:c.validate_enter_decref_projection(cat,q,q,b),'exact output types before normalization','OUTPUT-TYPE')
  # Nested returned mutation must not mutate either selected premises or future outputs.
  before=enc(q);catbefore=enc(cat);bad=copy.deepcopy(o);bad['binding']['references']['owner']['symbol']='changed';bad['predecessor_projection']['res_assignment']['target']='other'
  reject(name+'/nested-return-mutation',lambda:c.validate_enter_decref_projection(cat,q,q,bad),'pure model output comparison','OUTPUT-CORRESPONDENCE')
  check(name+'/pristine-after-return-mutation',lambda:need(enc(q)==before and enc(cat)==catbefore and enc(c.enter_decref_projection(cat,q,copy.deepcopy(q)))==enc(o)))
 # Cross-context supplied claims cannot replace fixed selected-input expectations.
 reject('whole different-context input against fixed expectation',lambda:c.enter_decref_projection(cat,cases[14],cases[2]),'pure selected-input comparison; not authentication','VALIDATED')
 # No auth: offline rows/receipt used strictly to test output alias isolation and shape.
 prior=read(R/'reference/return/actual-receipt.json');pub={'result':'PASS','contexts':list(a.CONTEXTS),'receipt':a.PARENT_RECEIPT,'actual_admission':False}
 basis={'prior':copy.deepcopy(prior),'catalogue':cat,'parent_public':pub,'fresh':{'root':R}}
 actual=a._assemble(basis);baseline=enc(actual);expected=(B/'host/expected/expected-enter-decref-receipt.json').read_bytes()
 check('offline receipt assembly matches saved actual bytes in two contexts',lambda:need(baseline==expected),'offline pure assembly from saved premises; NOT authenticated basis')
 qout=a._assemble(basis);qout['contexts'].reverse();qout['contexts'][0][a.RELATION]['declaration']['source']['operand_expression']='res';qout['contexts'][1][a.RELATION]['reference_basis'].clear()
 check('offline assembly nested alias isolation and context ordering',lambda:need(enc(a._assemble(basis))==baseline and tuple(x['context'] for x in a._assemble(basis)['contexts'])==a.CONTEXTS),'offline pure assembly copy isolation; no authentication')
 check('legitimate public receipt shape',lambda:need(a._receipt_shape(expected)['format']=='I164-ENTER-DECREF-ATTEMPT-1'),'pre-derivation shape only; not public validation')
 for name,change in [('missing relation',lambda x:x['contexts'][0].pop(a.RELATION)),('missing context',lambda x:x['contexts'].pop()),('reordered contexts',lambda x:x['contexts'].reverse()),('missing predecessor',lambda x:x['contexts'][1].pop('enter_return_res_correspondence'))]:
  bad=copy.deepcopy(actual);change(bad);reject(name,lambda b=bad:a._receipt_shape(enc(b)),'pre-derivation shape rejection only; no public negative derivation')
 save(O/'environment.json',{'python':sys.version,'platform':platform.platform(),'executable':sys.executable,'installed_metadata':{x:importlib.metadata.version(x) for x in ('cryptography','cffi','pycparser')},'cryptography_or_monitoring_executed':False,'runtime_application_execution':False,'host_equivalence_claim':False})
 save(O/'pure-scope.json',{'source':ident((R/'code/managed_coverage.py').read_bytes()),'adapter':ident((R/'code/correspondence.py').read_bytes()),'public_authentication_runs':0,'authenticated_constructed_runs':0,'full_public_negative_derivations':0,'application_helper_runtime_execution':0,'replayed_completed_campaigns':0,'parent_fixtures':'exact prior independent constructed model outputs; NOT live authenticated bases'})
try:run()
except BaseException as e:
 record('unhandled reviewer harness failure','harness','FAIL',{'exception':repr(e),'traceback':traceback.format_exc()});failures.append('harness')
finally:
 result={'result':'PASS' if not failures else 'INCOMPLETE-OR-DEFECT','rows':len(rows),'counts':dict(collections.Counter(r['status'] for r in rows)),'failures':failures,'seconds':time.monotonic()-start,'public_runs':0,'authenticated_constructed_runs':0}
 save(O/'RESULT.json',result);print(enc({'event':'RESULT','result':result}).decode(),end='',flush=True)
if failures:raise SystemExit(1)
