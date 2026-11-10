"""One new source/model pass. No public derivation, authenticated core, or C helper execution.
Only the producer, pure constructed projection and pre-derivation shape gate run.
"""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
ROWS=[];D=copy.deepcopy;START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def write(path,value):
 with open(path,'x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 row={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(row)
 write(OUT/('%04d.json'%len(ROWS)),row)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
def check(name,fn,layer='source/model independent oracle; no authentication'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='source/model input constraints; no authentication'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 record(name,layer,'FAIL','expected ValueError');raise AssertionError(name)
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def mutate(v,path,value):
 x=D(v);t=x
 for k in path[:-1]:t=t[k]
 t[path[-1]]=value;return x
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
def main():
 manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
 check('fixed checkpoint exact members and bytes',lambda:{p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==set(manifest)|{'MANIFEST.json'} and all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in manifest.items()),'source artifact identity')
 c=load(ROOT/'code/managed_coverage.py','enter_return_source');a=load(ROOT/'code/correspondence.py','enter_return_adapter')
 old=(ROOT/'reference/enter/code/managed_coverage.py').read_bytes();new=(ROOT/'code/managed_coverage.py').read_bytes()
 check('entire reviewed producer prefix unchanged',lambda:new.startswith(old),'source artifact identity')
 check('five new functions; historical six-function claim not copied',lambda:[x.name for x in ast.parse(new[len(old):]).body if isinstance(x,ast.FunctionDef)]==['compile_enter_return','validate_enter_return','enter_return_binding','enter_return_projection','validate_enter_return_projection'],'source artifact identity')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 lines=bc.decode().splitlines();body=bc.decode().split('        inst(BEFORE_WITH,',1)[1].split('        inst(WITH_EXCEPT_START,',1)[0]
 check('independent exact C call-assignment / excluded release / later test',lambda:lines[2514].strip()=='res = _PyObject_CallNoArgs(enter);' and lines[2515].strip()=='Py_DECREF(enter);' and lines[2516].strip()=='if (res == NULL) {','defining-source oracle')
 check('independent retained enter/exit lookups precede assignment',lambda:body.index('_Py_ID(__enter__)')<body.index('_Py_ID(__exit__)')<body.index('DECREF_INPUTS();')<body.index('res = _PyObject_CallNoArgs(enter);'),'defining-source oracle')
 fn=next(x for x in ast.parse(launcher).body if isinstance(x,ast.FunctionDef) and x.name=='write_new')
 check('launcher line24 with operand source anchor',lambda:fn.lineno==23 and fn.body[0].lineno==24 and ast.unparse(fn.body[0].items[0].context_expr)=="open(p, 'xb')",'defining-source oracle')
 r1=json.loads((ROOT/'fixtures/r1-catalogue.json').read_bytes());lp=json.loads((ROOT/'fixtures/lookup-catalogue.json').read_bytes());parentcat=json.loads((ROOT/'fixtures/enter-catalogue.json').read_bytes())
 cat=c.compile_enter_return(launcher,bc,tt,r1,lp,parentcat)
 write(OUT/'catalogue.json',cat)
 check('fresh catalogue from defining sources',lambda:c.validate_enter_return(launcher,bc,tt,r1,lp,parentcat,D(cat)),'source-derived catalogue comparison')
 check('independent three-stage / return-class oracle',lambda:cat['source']['order']==['enter-return:continuation','enter-return:c-return','enter-return:res-assignment'] and cat['source']['target']=='res' and cat['source']['assignment']['line']==2515 and cat['source']['next_operation_excluded']['line']==2516 and cat['source']['non_NULL_object_cases']==['opaque','Python-None'])
 for path,val in [(('source','order'),['enter-return:c-return','enter-return:continuation','enter-return:res-assignment']),(('source','steps',1,'allowed'),['non-NULL']),(('source','steps',2,'allowed'),['assigned','raise']),(('source','target'),'f'),(('source','assignment','line'),2516),(('source','non_NULL_object_cases'),['opaque']),(('declarations',),cat['declarations'][:-1]),(('parent_catalogue_sha256',),'0'*64)]:
  reject('catalogue mutation '+repr(path),lambda path=path,val=val:c.validate_enter_return(launcher,bc,tt,r1,lp,parentcat,mutate(cat,path,val)),'source-derived catalogue comparison')
 q=D(parentcat);q['source']['order'].reverse();q['declarations'].reverse()
 reject('coordinated parent catalogue mutation',lambda:c.compile_enter_return(launcher,bc,tt,r1,lp,q),'defining-source predecessor catalogue comparison')
 reject('wrong C assignment target source',lambda:c.compile_enter_return(launcher,bc.replace(b'res = _PyObject_CallNoArgs(enter);',b'f = _PyObject_CallNoArgs(enter);'),tt,r1,lp,parentcat),'defining-source identity/semantics')
 defs={n.name:n for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 def has(n,s):return s in ast.unparse(defs[n])
 check('actual predecessor authentication / actual returned basis / exact receipt comparison wired',lambda:has('_basis','p._basis(pd)') and has('_basis',"fresh['saved'] == p.enc(p._assemble(pb))") and has('_basis',"pb['parent_basis']['parent_basis']['catalogue']"),'static adapter audit; authentication UNEXECUTED')
 check('mandatory parent constructed validator then new projection validator wired',lambda:has('_construct_checked',"basis['parent_module']._construct_checked(basis['parent_basis']") and has('_construct_checked','validate_enter_return_projection'),'static adapter audit; authenticated core UNEXECUTED')
 check('mandatory two-context public relation and byte comparison wired',lambda:has('_rows','== CONTEXTS') and has('_assemble','ctx[RELATION]') and has('derive','_assemble(_basis(inputs(root)))') and has('validate','saved == enc(result)'),'static adapter audit; public validation UNEXECUTED')
 minimal={'format':'I164-ENTER-RETURN-RES-1','contexts':[{'context':ctx,'enter_return_res_correspondence':{},'enter_call_attempt_correspondence':{}} for ctx in a.CONTEXTS]}
 check('synthetic shape admitted',lambda:a._receipt_shape(a.enc(minimal))==minimal,'pre-derivation shape gate only; not public positive')
 for i in range(2):
  for relation in ('enter_return_res_correspondence','enter_call_attempt_correspondence'):
   q=D(minimal);del q['contexts'][i][relation]
   reject('mandatory relation omitted '+str(i)+'/'+relation,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only; not public negative')
 normal=[{'stage':'enter-return:continuation','outcome':'normal'},{'stage':'enter-return:c-return','outcome':'non-NULL','object_case':'opaque'},{'stage':'enter-return:res-assignment','outcome':'assigned'}]
 outputs=[]
 for path in sorted((ROOT/'fixtures/retained-enter').glob('*.json')):
  fixture=json.loads(path.read_bytes());p=fixture['output'];tag=path.stem
  b=c.enter_return_binding(cat,p,p['instance_anchor'],'explicit conditional premise')
  v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':D(normal)}
  out=c.enter_return_projection(cat,D(v),D(v));outputs.append(D(out))
  write(OUT/(tag+'-constructed.json'),{'input':v,'output':out,'qualification':'new pure constructed model; saved parent fixture is not an authenticated basis or runtime observation'})
  for valueclass in ('opaque','Python-None','NULL'):
   q=D(v);q['outcomes'][1]={'stage':'enter-return:c-return','outcome':'NULL'} if valueclass=='NULL' else {'stage':'enter-return:c-return','outcome':'non-NULL','object_case':valueclass}
   r=c.enter_return_projection(cat,D(q),D(q));isnull=valueclass=='NULL'
   check(tag+'/'+valueclass+'/accepted',lambda q=q,r=r:c.validate_enter_return_projection(cat,D(q),D(q),D(r)))
   check(tag+'/'+valueclass+'/independent C return and res oracle',lambda r=r,isnull=isnull,valueclass=valueclass:r['helper_c_return_completed_in_model'] is True and r['res_assignment_established'] is True and r['res_assignment']['target']=='res' and r['res_assignment']['source']['line']==2515 and r['res_assignment']['from_return_occurrence']==r['events'][1]['id'] and r['res_value_role']==r['call_result_role']==r['res_assignment']['value'] and r['res_value_role']['C_NULL'] is isnull and r['res_value_role']['python_value_class']==(None if isnull else valueclass) and (r['res_value_role']['python_object_role'] is None)==isnull)
   check(tag+'/'+valueclass+'/outer error and deeper C contract qualification',lambda r=r:r['terminal_python_exception_in_model'] is True and r['last_pending_error_in_model']==p['original_error_pending_in_outer_handler'] and r['helper_error_indicator']=='UNKNOWN' and r['helper_error_contract_established'] is False and r['C_NULL_implies_python_exception_established'] is False and r['no_replacement_inferred_from_C_result'] is True)
   reject(tag+'/'+valueclass+'/opposite NULL claim',lambda q=q,r=r,isnull=isnull:c.validate_enter_return_projection(cat,D(q),D(q),mutate(r,('res_value_role','C_NULL'),not isnull)),'source/model output comparison; no authenticated basis')
  check(tag+'/prior lineage, prefix, origins, effects retained',lambda:out['predecessor_projection']==p and out['cleanup_list_state']==p['cleanup_list_state'] and out['retained_cleanup_error_evidence']==p['retained_cleanup_error_evidence'] and out['failure_origin_region']==p['failure_origin_region'] and out['earlier_control_completed_in_model']==p['earlier_control_completed_in_model'] and out['prior_acknowledged_partial_effects']==p['current_partial_effects'] and out['binding']['attempt']==p['events'][-1])
  check(tag+'/strict stop and no runtime claims',lambda:all(out[k] is False for k in ('helper_dispatch_entry_established','method_body_entry_established','enter_invocation_established','exit_invocation_established','post_call_decref_established','result_test_established','result_error_routing_established','context_manager_entry_established','f_binding_established','actual_admission')) and out['runtime_enter_return_chain'] is None and out['call']['callability']=='UNKNOWN')
  for stage in (0,1,2):
   for frontier in (('raise','catchable-interruption','process-termination','unobserved') if stage<2 else ('process-termination','unobserved')):
    q=D(v);q['outcomes']=D(normal[:stage])+[{'stage':normal[stage]['stage'],'outcome':frontier}];r=c.enter_return_projection(cat,D(q),D(q));abrupt=frontier in ('process-termination','unobserved')
    check(tag+'/'+str(stage)+'/'+frontier,lambda q=q,r=r,abrupt=abrupt,stage=stage:c.validate_enter_return_projection(cat,D(q),D(q),D(r)) and r['helper_c_return_completed_in_model'] is (stage==2) and r['res_assignment_established'] is False and (r['call_result_role'] is None)==(stage<2) and r['terminal_python_exception_in_model'] is (None if abrupt else True) and (r['replacement_error_in_model'] is None)==abrupt)
    reject(tag+'/'+str(stage)+'/'+frontier+'/invented assignment',lambda q=q,r=r:c.validate_enter_return_projection(cat,D(q),D(q),mutate(r,('res_assignment_established',),True)),'source/model output comparison; no authenticated basis')
  q=D(v);q['binding']['continuity']='UNESTABLISHED';q['outcomes']=[{'stage':'enter-return:continuation','outcome':'unobserved'}]
  check(tag+'/unestablished continuation cannot yield value',lambda:c.enter_return_projection(cat,D(q),D(q))['call_result_role'] is None)
  q=D(v);q['binding']['continuity']='UNESTABLISHED'
  reject(tag+'/no implicit continuation',lambda:c.enter_return_projection(cat,D(q),D(q)))
  input_changes=[(('scope','invocation'),'other-invocation'),(('anchor','context'),'other-context'),(('binding','references','owner','symbol'),'other-owner'),(('binding','references','token','symbol'),'other-token'),(('binding','method_results','__enter__','symbol'),'other-enter'),(('binding','method_results','__exit__','symbol'),'other-exit'),(('binding','attempt','id'),'other-attempt'),(('binding','original_constructor_error','symbol'),'other-error'),(('binding','call','source','line'),2516),(('outcomes',),normal[:1]),(('outcomes',),normal[:2]),(('outcomes',),[normal[0],normal[2]]),(('outcomes',),normal[::-1]),(('outcomes',),normal+[normal[-1]]),(('outcomes',1),{'stage':'enter-return:c-return','outcome':'NULL','object_case':'Python-None'}),(('outcomes',2,'outcome'),'raise'),(('outcomes',),[{'stage':'enter-return:continuation','outcome':'process-termination'},normal[1],normal[2]])]
  for path2,val in input_changes:
   q=mutate(v,path2,val);reject(tag+'/input '+repr(path2),lambda q=q:c.enter_return_projection(cat,D(q),D(q)))
  for path2,val in [(('completion',),'unobserved-frontier'),(('enter_call_attempt_established_in_model',),False),(('call_outcome',),'C-return-NULL'),(('call_result_role',),{}),(('res_assignment_established',),True),(('events',1,'outcome'),'raise')]:
   q=mutate(p,path2,val);reject(tag+'/predecessor '+repr(path2),lambda q=q:c.enter_return_binding(cat,q,q['instance_anchor'],'explicit conditional premise'),'pure predecessor source-model constraints; no authentication')
  for path2,val in [(('res_assignment','from_return_occurrence'),'other-return'),(('res_assignment','target'),'f'),(('res_assignment','source','line'),2516),(('res_value_role','kind'),'C-NULL'),(('res_value_role','runtime_identity'),'observed-id'),(('helper_error_indicator',),'SET'),(('helper_error_contract_established',),True),(('terminal_python_exception_in_model',),False),(('terminal_python_exception_in_model',),1),(('last_pending_error_in_model','symbol'),'replacement'),(('post_call_decref_established',),True),(('result_test_established',),True),(('context_manager_entry_established',),True),(('f_binding_established',),True),(('current_partial_effects',),'NONE')]:
   reject(tag+'/output '+repr(path2),lambda path2=path2,val=val:c.validate_enter_return_projection(cat,D(v),D(v),mutate(out,path2,val)),'source/model output comparison; no authenticated basis')
  q=D(out)
  for role in (q['call_result_role'],q['res_value_role'],q['res_assignment']['value']):role['C_NULL']=True;role['kind']='C-NULL';role['python_object_role']=None;role['python_value_class']=None
  q['events'][1]['outcome']='NULL';q['call_outcome']='C-return-NULL';q['completion']='res-assigned-NULL'
  reject(tag+'/coordinated output return substitution',lambda:c.validate_enter_return_projection(cat,D(v),D(v),q),'source/model output comparison; no authenticated basis')
  q=D(v);q['outcomes'][1]={'stage':'enter-return:c-return','outcome':'NULL'}
  reject(tag+'/coordinated input differs from independent selected premises',lambda:c.enter_return_projection(cat,D(q),D(v)),'source/model selected-input comparison; no authenticated basis')
  for path2,val in [(('outcomes',0,'outcome'),S('normal')),(('outcomes',),L(normal)),(('binding','references',),Q(b['references']))]:
   q=mutate(v,path2,val);reject(tag+'/input exact type '+repr(path2),lambda q=q:c.enter_return_projection(cat,q,D(v)),'exact-type input gate before serialization')
  for path2,val in [(('completion',),S('res-assigned-non-NULL')),(('res_assignment','source','line'),I(2515)),(('res_value_role',),Q(out['res_value_role'])),(('events',),L(out['events']))]:
   q=mutate(out,path2,val);reject(tag+'/output exact type '+repr(path2),lambda q=q:c.validate_enter_return_projection(cat,D(v),D(v),q),'exact-type submitted-output gate before serialization')
  q=D(out);q['res_assignment'][S('target')]=q['res_assignment'].pop('target')
  reject(tag+'/nested subclass literal key',lambda:c.validate_enter_return_projection(cat,D(v),D(v),q),'exact-type submitted-output key gate')
  q=D(cat);q['source']['target']=S('res')
  reject(tag+'/semantic catalogue exact type',lambda:c.enter_return_projection(q,D(v),D(v)),'exact-type semantic-claim gate before serialization')
  before=D(v);beforecat=D(cat);out['res_value_role']['scope']['context']='MUTATED';out['binding']['references']['owner']['symbol']='MUTATED';out['events'].clear()
  pristine=c.enter_return_projection(cat,D(v),D(v))
  check(tag+'/nested returned mutations leave premises and expectations isolated',lambda:v==before and cat==beforecat and c.validate_enter_return_projection(cat,D(v),D(v),D(pristine)))
  reject(tag+'/mutated returned result rejected',lambda:c.validate_enter_return_projection(cat,D(v),D(v),out),'source/model output comparison; no authenticated basis')
 check('eight distinct assignment occurrences across contexts/prefixes/origins',lambda:len(outputs)==8 and len({o['events'][-1]['id'] for o in outputs})==8)
 return {'source_only':True,'public_runs':0,'full_public_negative_derivations':0,'authenticated_core_runs':0,'predecessor_authentication':'UNEXECUTED for new bytes; only static wiring inspected','application_runs':0,'helper_runs':0,'runtime_return_assignment_observations':'UNAVAILABLE','independent_acceptance':'PENDING','previous_groups':'147 independent / 489 Engineering / one Ubuntu public positive preserved separately'}
try:
 details=main();result={'result':'PASS','finished_utc':utc(),'seconds':time.monotonic()-START,'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'rows':len(ROWS),'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
