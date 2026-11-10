"""Formal-Lab[6] independent, finite source/model review of ENTER-RETURN-RES.
No public validator, authenticated constructed core, observer, helper or application call.
Retained eight predecessor fixtures are exact prior reviewer bytes; modeled premises only.
Expected return/assignment/frontier table derives from the inspected C statement.
"""
import ast,copy,hashlib,importlib.metadata,json,os,platform,sys,time,traceback,types
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;ROOT=B/'candidate';OUT=B/'independent';OUT.mkdir(exist_ok=False)
D=copy.deepcopy;ROWS=[];START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def save(n,v):
 p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def row(name,layer,status,detail=None):
 v={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(v);save('rows/%04d.json'%len(ROWS),v)
 with (OUT/'progress.jsonl').open('a') as f:f.write(json.dumps(v,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(v,sort_keys=True),flush=True)
def yes(name,fn,layer='independent source-model oracle; no authentication'):
 try:assert fn() is not False
 except BaseException as e:row(name,layer,'FAIL',repr(e));raise
 row(name,layer,'PASS')
def no(name,fn,layer='source-model input rejection; constructed premises'):
 try:fn()
 except ValueError as e:row(name,layer,'REJECTED',str(e));return
 except BaseException as e:row(name,layer,'HARNESS-FAIL',repr(e));raise
 row(name,layer,'DEFECT-OBSERVED','intended rejection absent');raise AssertionError(name)
def load(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def read(p):return json.loads(p.read_bytes())
def change(v,path,x):
 v=D(v);node=v
 for k in path[:-1]:node=node[k]
 node[path[-1]]=x;return v
class S(str):pass
class I(int):pass
class L(list):pass
class M(dict):pass

def main():
 versions={}
 for name in ('cryptography','cffi','pycparser'):
  try:versions[name]=importlib.metadata.version(name)
  except importlib.metadata.PackageNotFoundError:versions[name]='not installed'
 save('environment.json',{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'installed_metadata':versions,'cryptography_native_monitoring_application_execution':False,'host_equivalence_claim':False})
 c=load(ROOT/'code/managed_coverage.py','reviewed_return_model');a=load(ROOT/'code/correspondence.py','reviewed_return_adapter')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 text=bc.decode();start=text.index('        inst(BEFORE_WITH,');end=text.index('        inst(WITH_EXCEPT_START,',start);body=text[start:end]
 # Independent literal source order, not values copied from the generated catalogue.
 yes('exact C assignment and stop before release/test',lambda:text.splitlines()[2514:2517]==['            res = _PyObject_CallNoArgs(enter);','            Py_DECREF(enter);','            if (res == NULL) {'],'defining source inspection')
 yes('selected enter callable follows both lookup guards and DECREF_INPUTS',lambda:body.index('if (enter == NULL)')<body.index('_Py_ID(__exit__)')<body.index('if (exit == NULL)')<body.index('DECREF_INPUTS();')<body.index('res = _PyObject_CallNoArgs(enter);'),'defining source inspection')
 fn=next(n for n in ast.parse(launcher).body if isinstance(n,ast.FunctionDef) and n.name=='write_new')
 yes('launcher operand and f target remain separate source roles',lambda:fn.lineno==23 and isinstance(fn.body[0],ast.With) and fn.body[0].lineno==24 and ast.unparse(fn.body[0].items[0].context_expr)=="open(p, 'xb')" and ast.unparse(fn.body[0].items[0].optional_vars)=='f','defining source inspection')
 r1=read(ROOT/'fixtures/r1-catalogue.json');lookup=read(ROOT/'fixtures/lookup-catalogue.json');enter=read(ROOT/'fixtures/enter-catalogue.json')
 cat=c.compile_enter_return(launcher,bc,tt,r1,lookup,enter);save('catalogue.json',cat)
 stages=['enter-return:continuation','enter-return:c-return','enter-return:res-assignment']
 yes('three independent stages and exact result classes retained',lambda:cat['source']['order']==stages and cat['source']['target']=='res' and cat['source']['non_NULL_object_cases']==['opaque','Python-None'] and cat['source']['assignment']['line']==2515 and cat['source']['next_operation_excluded']['line']==2516 and c.validate_enter_return(launcher,bc,tt,r1,lookup,enter,D(cat)),'source-derived catalogue comparison')
 for name,mut in [('omit NULL',lambda q:q['source']['steps'][1]['allowed'].remove('NULL')),('omit Python None',lambda q:q['source']['non_NULL_object_cases'].remove('Python-None')),('allow assignment raise',lambda q:q['source']['steps'][2]['allowed'].append('raise')),('reorder coordinated declarations',lambda q:(q['source']['order'].reverse(),q['source']['steps'].reverse(),q['declarations'].reverse()))]:
  q=D(cat);mut(q);no(name,lambda q=q:c.validate_enter_return(launcher,bc,tt,r1,lookup,enter,q),'defining-source catalogue recomputation')
 q=D(enter);q['source']['call_site']['expression']='_PyObject_CallNoArgs(exit)';q['source']['C_argument_expression']='exit'
 no('coordinated predecessor callable substitution',lambda:c.compile_enter_return(launcher,bc,tt,r1,lookup,q),'defining-source predecessor recomputation')
 defs={n.name:ast.unparse(n) for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 yes('actual predecessor basis and receipt comparisons mandatory before new catalogue',lambda:defs['_basis'].index('p._basis(pd)')<defs['_basis'].index("fresh['saved'] == p.enc(p._assemble(pb))")<defs['_basis'].index('compile_enter_return') and 'saved == enc(result)' in defs['validate'],'static public wiring; saved execution inspected separately')
 yes('constructed case checks actual parent output before new source-model validation',lambda:defs['_construct_checked'].index("basis['parent_module']._construct_checked")<defs['_construct_checked'].index("case['parent_output'], parent")<defs['_construct_checked'].index('validate_enter_return_projection'),'static constructed wiring; authenticated execution UNEXECUTED')
 reps=[];ids=set();normal_outputs=[]
 for fixture in sorted((ROOT/'fixtures/retained-enter').glob('*.json')):
  tag=fixture.stem;parent=read(fixture)['output'];binding=c.enter_return_binding(cat,parent,parent['instance_anchor'],'explicit conditional premise')
  base={'scope':D(parent['scope']),'anchor':D(parent['instance_anchor']),'parent_result':D(parent),'binding':binding,'outcomes':[]}
  def case(retclass='opaque',assignment='assigned'):
   v=D(base);ret={'stage':stages[1],'outcome':'NULL'} if retclass=='NULL' else {'stage':stages[1],'outcome':'non-NULL','object_case':retclass}
   v['outcomes']=[{'stage':stages[0],'outcome':'normal'},ret,{'stage':stages[2],'outcome':assignment}];return v
  def oracle(v,completed,assigned,classification,terminal,replacement=False):
   o=c.enter_return_projection(cat,D(v),D(v));k=classification
   assert type(o['helper_c_return_completed_in_model']) is bool and o['helper_c_return_completed_in_model'] is completed
   assert type(o['res_assignment_established']) is bool and o['res_assignment_established'] is assigned
   assert o['terminal_python_exception_in_model'] is terminal
   assert (o['replacement_error_in_model'] is not None)==replacement
   if replacement:
    assert o['last_pending_error_in_model']==o['replacement_error_in_model'] and o['last_pending_error_in_model']!=parent['last_pending_error_in_model']
    assert all(o['replacement_error_in_model'][x]=='UNKNOWN' for x in ('existing_cause','existing_context','existing_suppression'))
   else:assert o['last_pending_error_in_model']==parent['last_pending_error_in_model']
   assert o['last_acknowledged_pending_error_before_call']==parent['last_pending_error_in_model']
   assert o['original_error_pending_in_outer_handler']==parent['original_error_pending_in_outer_handler']
   assert o['retained_cleanup_error_evidence']==parent['retained_cleanup_error_evidence'] and o['cleanup_list_state']==parent['cleanup_list_state']
   assert o['current_partial_effects'].startswith('UNKNOWN') and o['helper_error_indicator']=='UNKNOWN' and o['helper_error_contract_established'] is False and o['C_NULL_implies_python_exception_established'] is False
   assert all(o[x] is False for x in ('helper_dispatch_entry_established','method_body_entry_established','enter_invocation_established','exit_invocation_established','post_call_decref_established','result_test_established','result_error_routing_established','context_manager_entry_established','f_binding_established','actual_admission'))
   if completed:
    value=o['call_result_role'];assert value['C_NULL'] is (k=='NULL') and value['kind']==('C-NULL' if k=='NULL' else 'SYMBOLIC-PYOBJECT')
    assert value['python_value_class']==(None if k=='NULL' else k) and (value['python_object_role'] is None)==(k=='NULL')
    assert value['concrete_value'] is None and value['runtime_identity'] is None and value['runtime_observation'] is False
    assert value['return_occurrence']==o['events'][1]['id'] and value['scope']==v['scope']
    assert o['call_outcome']==('C-return-NULL' if k=='NULL' else 'C-return-non-NULL')
    if assigned:
     assert o['res_assignment']['target']=='res' and o['res_assignment']['value']==value==o['res_value_role']
     assert o['res_assignment']['from_return_occurrence']==value['return_occurrence'] and o['res_assignment']['occurrence']==o['events'][2]['id']
    else:assert o['res_assignment'] is None and o['res_value_role'] is None
   else:assert o['call_result_role'] is None and o['call_outcome'] is None and o['res_assignment'] is None and o['res_value_role'] is None
   assert all(e['selected_attempt']==binding['attempt']['id'] and e['owner']==binding['references']['owner'] and e['token']==binding['references']['token'] and e['scope']==v['scope'] and e['runtime_frame'] is None for e in o['events'])
   assert c.validate_enter_return_projection(cat,D(v),D(v),D(o)) is True
   return o
  for klass in ('opaque','Python-None','NULL'):
   v=case(klass);o=oracle(v,True,True,klass,True)
   yes(tag+'/'+klass+'/completed return forwarded into res',lambda o=o:True)
   normal_outputs.append((tag,klass,v,o));ids.add(o['events'][2]['id'])
   if klass=='opaque':reps.append((tag,D(v),D(o)))
   for frontier in ('process-termination','unobserved'):
    q=case(klass,frontier)
    yes(tag+'/'+klass+'/assignment-'+frontier,lambda q=q,klass=klass:oracle(q,True,False,klass,None))
  for stage in (0,1):
   for frontier in ('raise','catchable-interruption','process-termination','unobserved'):
    q=case();q['outcomes']=q['outcomes'][:stage+1];q['outcomes'][-1]={'stage':stages[stage],'outcome':frontier}
    yes(tag+'/'+stages[stage]+'/'+frontier,lambda q=q,frontier=frontier:oracle(q,False,False,None,None if frontier in ('process-termination','unobserved') else True,frontier in ('raise','catchable-interruption')))
  q=D(base);q['binding']['continuity']='UNESTABLISHED';q['outcomes']=[{'stage':stages[0],'outcome':'unobserved'}]
  yes(tag+'/UNESTABLISHED keeps return absent',lambda:oracle(q,False,False,None,None))
  q['outcomes']=case()['outcomes'];no(tag+'/UNESTABLISHED cannot reach assignment',lambda:c.enter_return_projection(cat,q,D(q)))
 # One source-sensitive negative set per context, with all eight histories above.
 for i in (0,4):
  tag,v,o=reps[i]
  paths=[(('binding','attempt','id'),'other-attempt'),(('binding','references','owner','symbol'),'other-owner'),(('binding','references','token','symbol'),'other-token'),(('scope','invocation'),'other-invocation'),(('scope','acquisition'),'other-acquisition'),(('anchor','instance'),'other-instance'),(('binding','method_results','__enter__'),D(v['binding']['method_results']['__exit__']))]
  for path,value in paths:
   q=change(v,path,value);no(tag+'/input '+repr(path),lambda q=q:c.enter_return_projection(cat,q,D(q)))
  cases=[v['outcomes'][1:],v['outcomes'][:1],v['outcomes'][:2],v['outcomes'][::-1],v['outcomes']+[v['outcomes'][-1]], [v['outcomes'][0],{'stage':stages[1],'outcome':'raise'},v['outcomes'][2]], [v['outcomes'][0],{'stage':stages[1],'outcome':'NULL','object_case':'Python-None'},v['outcomes'][2]], [v['outcomes'][0],{'stage':stages[1],'outcome':'non-NULL'},v['outcomes'][2]], [v['outcomes'][0],v['outcomes'][1],{'stage':stages[2],'outcome':'raise'}]]
  for j,oo in enumerate(cases):
   q=change(v,('outcomes',),oo);no(tag+'/invalid order-or-class %d'%j,lambda q=q:c.enter_return_projection(cat,q,D(q)))
  for path,value in [(('res_assignment','target'),'f'),(('res_assignment','from_return_occurrence'),'other-return'),(('res_value_role','C_NULL'),0),(('res_assignment_established',),1),(('call_result_role','python_value_class'),'Python-None'),(('helper_error_indicator',),'SET'),(('C_NULL_implies_python_exception_established',),True),(('terminal_python_exception_in_model',),False),(('post_call_decref_established',),True),(('cleanup_list_state','earlier_partial_append_effects'),'NONE')]:
   q=change(o,path,value);no(tag+'/output '+repr(path),lambda q=q:c.validate_enter_return_projection(cat,D(v),D(v),q),'source-model output comparison; no authenticated basis')
  q=D(o)
  for key in ('call_result_role','res_value_role'):q[key]['kind']='C-NULL';q[key]['C_NULL']=True;q[key]['python_object_role']=None;q[key]['python_value_class']=None
  q['res_assignment']['value']=D(q['res_value_role']);q['call_outcome']='C-return-NULL';q['completion']='res-assigned-NULL';q['events'][1]['outcome']='NULL';q['events'][1].pop('object_case')
  no(tag+'/coordinated output NULL substitution',lambda:c.validate_enter_return_projection(cat,D(v),D(v),q),'source-model output comparison; fixed selected premises')
  q=D(v);q['scope']['invocation']='other';q['binding']['scope']['invocation']='other';q['parent_result']['scope']['invocation']='other'
  no(tag+'/coordinated inputs versus fixed premise',lambda:c.enter_return_projection(cat,q,D(v)),'source-model selected-input comparison; no authentication')
  for path,value in [(('outcomes',1,'object_case'),S('opaque')),(('outcomes',),L(v['outcomes'])),(('binding',),M(v['binding']))]:
   q=change(v,path,value);no(tag+'/exact input '+repr(path),lambda q=q:c.enter_return_projection(cat,q,D(v)),'exact input type gate before normalization')
  for path,value in [(('call_result_role','kind'),S('SYMBOLIC-PYOBJECT')),(('res_assignment',),M(o['res_assignment'])),(('res_assignment','source','line'),I(2515))]:
   q=change(o,path,value);no(tag+'/exact output '+repr(path),lambda q=q:c.validate_enter_return_projection(cat,D(v),D(v),q),'exact output type gate before normalization')
  q=D(o);value=q['call_result_role'].pop('C_NULL');q['call_result_role'][S('C_NULL')]=value
  no(tag+'/subclassed return-value key',lambda:c.validate_enter_return_projection(cat,D(v),D(v),q),'exact output key gate before normalization')
  q=change(v,('parent_result','enter_call_attempt_established_in_model'),1)
  no(tag+'/integer parent attempt claim',lambda:c.enter_return_projection(cat,q,D(q)),'predecessor source-model binding checks')
 # All new normal fixture cases retained as evidence; test returned copies across three classes.
 for tag,klass,v,o in normal_outputs:
  if tag.startswith('0-control-absent-protected-append') or tag.startswith('1-control-absent-protected-append'):
   prior=D(v);cat_before=D(cat);mut=D(o);mut['res_assignment']['value']['symbol']='changed';mut['binding']['references']['owner']['symbol']='changed';mut['events'].clear()
   no(tag+'/'+klass+'/mutated result',lambda mut=mut,v=v:c.validate_enter_return_projection(cat,D(v),D(v),mut),'source-model output comparison; no authenticated basis')
   yes(tag+'/'+klass+'/pristine repeat isolated',lambda v=v,o=o,prior=prior,cat_before=cat_before:v==prior and cat==cat_before and c.enter_return_projection(cat,D(v),D(v))==o)
 save('constructed-normal-cases.json',[{'name':tag+'/'+klass,'input':v,'output':o,'qualification':'pure constructed, not authenticated or runtime evidence'} for tag,klass,v,o in normal_outputs])
 yes('eight invocation-qualified assignment occurrences distinct across alternatives',lambda:len(ids)==8)
 # Actual receipt is used only for shape and offline copy isolation. No authentication claim.
 receipt=read(B/'host/expected/expected-enter-return-receipt.json');saved=(B/'host/expected/expected-enter-return-receipt.json').read_bytes()
 yes('pristine saved receipt shape',lambda:a._receipt_shape(saved)==receipt,'pre-derivation shape gate only')
 for idx in (0,1):
  q=D(receipt);del q['contexts'][idx]['enter_return_res_correspondence'];no('required relation absent context%d'%idx,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only')
 q=D(receipt);q['contexts'].reverse();no('context order reversed',lambda:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only')
 old=read(ROOT/'reference/enter/actual-receipt.json');basis={'fresh':{'root':ROOT},'prior':D(old),'catalogue':D(cat),'parent_public':D(receipt['contexts'][0]['enter_return_res_correspondence']['predecessor_validation'])}
 pristine=a._assemble(basis);snapcat=D(basis['catalogue']);snapprior=D(basis['prior']);altered=a._assemble(basis);altered['contexts'].reverse();altered['contexts'][0]['enter_return_res_correspondence']['declaration']['source']['steps'].clear();altered['contexts'][0]['enter_return_res_correspondence']['predecessor_receipt']['bytes']=0
 yes('offline assembly nested returns do not alter subsequent expectations',lambda:basis['catalogue']==snapcat and basis['prior']==snapprior and a._assemble(basis)==pristine and a.CONTEXTS==('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'),'offline assembly from saved premises; not authenticated basis')
 return {'public_runs':0,'authenticated_constructed_runs':0,'full_public_negative_derivations':0,'runtime_helper_database_session_runs':0,'retained_fixtures':8,'normal_class_cases':24,'fresh_expectations':'independent statement/order and outcome table; supplied oracle not run','historical_campaign_replays':0}
try:
 q=main();result={'status':'PASS','rows':len(ROWS),'counts':{s:sum(x['status']==s for x in ROWS) for s in ('PASS','REJECTED','FAIL','HARNESS-FAIL','DEFECT-OBSERVED')},'seconds':time.monotonic()-START,'finished_utc':utc(),'qualifications':q};save('RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:save('FAILURE.json',{'exception':repr(e),'rows':len(ROWS),'utc':utc()});traceback.print_exc();raise
