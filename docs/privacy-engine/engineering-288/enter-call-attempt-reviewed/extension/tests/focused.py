"""One new ENTER-CALL SOURCE-CONSTRUCTED pass. No public derivation or authenticated basis.
The C-source oracle reads the defining BEFORE_WITH code independently of the catalogue.
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
def check(name,fn,layer='source-constructed projector / independent oracle'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='source-constructed projector input'):
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
 check('exact source checkpoint members',lambda:all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in manifest.items()),'source artifact identity')
 c=load(ROOT/'code/managed_coverage.py','enter_source');a=load(ROOT/'code/correspondence.py','enter_adapter');f=load(ROOT/'reference/r1/tests/fixtures.py','retained_fixture_builder')
 old=(ROOT/'reference/lookup/code/managed_coverage.py').read_bytes()
 check('reviewed lookup producer prefix unchanged',lambda:(ROOT/'code/managed_coverage.py').read_bytes().startswith(old),'source artifact identity')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes()
 text=bc.decode();body=text.split('        inst(BEFORE_WITH,',1)[1].split('        inst(WITH_EXCEPT_START,',1)[0]
 check('independent source oracle ordered lookups / DECREF / call',lambda:body.index('_Py_ID(__enter__)')<body.index('_Py_ID(__exit__)')<body.index('DECREF_INPUTS();')<body.index('_PyObject_CallNoArgs(enter)'), 'independent defining-source oracle')
 check('independent source oracle exact C target / zero explicit Python arguments',lambda:text.splitlines()[2513].strip()=='DECREF_INPUTS();' and text.splitlines()[2514].strip()=='res = _PyObject_CallNoArgs(enter);','independent defining-source oracle')
 check('independent source oracle excludes call outcome and later release',lambda:body.index('_PyObject_CallNoArgs(enter)')<body.index('Py_DECREF(enter);',body.index('_PyObject_CallNoArgs(enter)'))<body.index('if (res == NULL)'), 'independent defining-source oracle')
 tree=ast.parse(launcher);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='write_new')
 check('independent launcher oracle',lambda:fn.lineno==23 and fn.body[0].lineno==24 and ast.unparse(fn.body[0].items[0].context_expr)=="open(p, 'xb')",'independent defining-source oracle')
 r1=json.loads((ROOT/'fixtures/r1-catalogue.json').read_bytes());hc=json.loads((ROOT/'fixtures/helper-catalogue.json').read_bytes());lp=json.loads((ROOT/'fixtures/lookup-catalogue.json').read_bytes());anchors=json.loads((ROOT/'fixtures/anchors.json').read_bytes())
 cat=c.compile_enter_call(launcher,bc,tt,r1,lp)
 check('new catalogue exact defining-source correspondence',lambda:c.validate_enter_call(launcher,bc,tt,r1,lp,D(cat)))
 check('catalogue exact independently expected stage order',lambda:cat['source']['order']==['enter-call:continuation','enter-call:attempt'] and cat['source']['call_site']['line']==2515 and cat['source']['intervening_operation']['line']==2514)
 for path,val in [(('source','order'),['enter-call:attempt','enter-call:continuation']),(('source','steps',0,'allowed'),['normal']),(('source','C_argument_expression'),'exit'),(('source','python_explicit_argument_count'),1),(('declarations',1,'source','line'),2516),(('parent_catalogue_sha256',),'0'*64)]:
  reject('catalogue '+repr(path),lambda path=path,val=val:c.validate_enter_call(launcher,bc,tt,r1,lp,mutate(cat,path,val)),'source-derived catalogue comparison')
 q=D(lp);q['source']['steps'].pop();q['declarations'].pop()
 reject('coordinated predecessor catalogue omission',lambda:c.compile_enter_call(launcher,bc,tt,r1,q),'independent defining-source predecessor comparison')
 reject('altered C call target',lambda:c.compile_enter_call(launcher,bc.replace(b'_PyObject_CallNoArgs(enter)',b'_PyObject_CallNoArgs(exit)'),tt,r1,lp),'exact defining-source input pin')
 defs={n.name:n for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 def has(n,s):return s in ast.unparse(defs[n])
 check('mandatory unchanged predecessor authentication and bytes comparison wired',lambda:has('_basis','p._basis(pd)') and has('_basis',"fresh['saved'] == p.enc(p._assemble(pb))"),'static adapter audit; authentication UNEXECUTED')
 check('mandatory actual returned predecessor construction check wired',lambda:has('_construct_checked',"basis['parent_module']._construct_checked(basis['parent_basis']") and has('_construct_checked','validate_enter_call_projection'),'static adapter audit; authenticated core UNEXECUTED')
 check('mandatory two-context output and public comparison wired',lambda:has('_rows',"basis['prior']['contexts']") and has('_rows','== CONTEXTS') and has('_assemble','ctx[RELATION]') and has('derive','_assemble(_basis(inputs(root)))') and has('validate','saved == enc(result)'),'static adapter audit; public validation UNEXECUTED')
 minimal={'format':'I164-ENTER-CALL-ATTEMPT-1','contexts':[{'context':ctx,'enter_call_attempt_correspondence':{},'context_special_lookup_correspondence':{}} for ctx in a.CONTEXTS]}
 check('synthetic receipt shape accepted',lambda:a._receipt_shape(a.enc(minimal))==minimal,'pre-derivation shape gate only; not public positive')
 for i in range(2):
  for relation in ('enter_call_attempt_correspondence','context_special_lookup_correspondence'):
   q=D(minimal);del q['contexts'][i][relation]
   reject('missing required relation '+str(i)+'/'+relation,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only; not public negative')
 lookup_outcomes=[{'stage':'lookup:continuation','outcome':'normal'},{'stage':'lookup:__enter__','outcome':'found'},{'stage':'lookup:__exit__','outcome':'found'}]
 normal=[{'stage':'enter-call:continuation','outcome':'normal'},{'stage':'enter-call:attempt','outcome':'attempted'}]
 outputs=[]
 for row in anchors:
  for prefix in ('control-absent','control-normal'):
   for origin in ('protected-close','protected-append'):
    tag=row['context']+'/'+prefix+'/'+origin
    hp=f.parent(c,hc,row,prefix,origin)
    if prefix=='control-absent':hp['earlier_control_completed_in_model']=None
    rv=f.projection_case(c,r1,hp);rp=c.open_return_projection(r1,rv,rv)
    lb=c.context_lookup_binding(lp,rp,rp['instance_anchor'],'explicit conditional premise')
    lv={'scope':D(rp['scope']),'anchor':D(rp['instance_anchor']),'parent_result':rp,'binding':lb,'outcomes':D(lookup_outcomes)}
    p=c.context_lookup_projection(lp,lv,lv)
    b=c.enter_call_binding(cat,p,p['instance_anchor'],'explicit conditional premise')
    v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':D(normal)}
    out=c.enter_call_projection(cat,D(v),D(v));outputs.append(out)
    check(tag+'/normal accepted',lambda:c.validate_enter_call_projection(cat,D(v),D(v),D(out)))
    check(tag+'/source-grounded call target / arguments / pending error',lambda:out['completion']=='enter-call-attempt' and out['enter_call_attempt_established_in_model'] is True and out['call']['target_role']==p['method_roles']['__enter__'] and out['call']['retained_exit_role']==p['method_roles']['__exit__'] and out['call']['python_explicit_arguments']==[] and out['terminal_python_exception_in_model'] is True and out['last_pending_error_in_model']==p['original_error_pending_in_outer_handler'] and out['replacement_error_in_model'] is None)
    check(tag+'/source operation acknowledged without physical effects',lambda:out['source_operation_acknowledged']['expression']=='DECREF_INPUTS();' and out['source_operation_effects'].startswith('UNKNOWN') and out['call']['callability']=='UNKNOWN' and out['call']['runtime_identity'] is None)
    check(tag+'/stop before call outcome, entry, res and f',lambda:out['call_outcome'] is None and out['call_result_role'] is None and all(out[k] is False for k in ('helper_dispatch_entry_established','method_body_entry_established','res_assignment_established','enter_invocation_established','exit_invocation_established','context_manager_entry_established','f_binding_established','actual_admission')))
    check(tag+'/earlier facts and uncertainty retained',lambda:out['predecessor_projection']==p and out['cleanup_list_state']==p['cleanup_list_state'] and out['retained_cleanup_error_evidence']==p['retained_cleanup_error_evidence'] and out['failure_origin_region']==origin and out['earlier_control_completed_in_model']==(True if prefix=='control-normal' else None))
    for outcome in ('raise','catchable-interruption','process-termination','unobserved'):
     q=D(v);q['outcomes']=[{'stage':'enter-call:continuation','outcome':outcome}];r=c.enter_call_projection(cat,D(q),D(q));abrupt=outcome in ('process-termination','unobserved')
     check(tag+'/'+outcome,lambda q=q,r=r,abrupt=abrupt:c.validate_enter_call_projection(cat,D(q),D(q),D(r)) and r['call'] is None and r['enter_call_attempt_established_in_model'] is False and r['terminal_python_exception_in_model'] is (None if abrupt else True) and (r['replacement_error_in_model'] is None)==abrupt and r['predecessor_projection']==p)
     reject(tag+'/'+outcome+'/false call completion',lambda q=q,r=r:c.validate_enter_call_projection(cat,D(q),D(q),mutate(r,('enter_call_attempt_established_in_model',),True)),'source-constructed output comparison; no authenticated basis')
    q=D(v);q['binding']['continuity']='UNESTABLISHED';q['outcomes']=[{'stage':'enter-call:continuation','outcome':'unobserved'}]
    check(tag+'/UNESTABLISHED remains unobserved',lambda:c.enter_call_projection(cat,D(q),D(q))['call'] is None)
    q=D(v);q['binding']['continuity']='UNESTABLISHED'
    reject(tag+'/no implicit continuation',lambda:c.enter_call_projection(cat,D(q),D(q)))
    changes=[(('scope','invocation'),'wrong-invocation'),(('anchor','context'),'wrong-context'),(('binding','references','owner','symbol'),'other-owner'),(('binding','references','token','symbol'),'other-token'),(('binding','method_results','__enter__','symbol'),'other-enter'),(('binding','method_results','__exit__','symbol'),'other-exit'),(('binding','lookup_occurrences',1,'id'),'other-occurrence'),(('binding','original_constructor_error','symbol'),'other-error'),(('binding','intervening_operation','line'),2513),(('outcomes',),normal[:1]),(('outcomes',),normal[::-1]),(('outcomes',),normal+[normal[-1]]),(('outcomes',1,'outcome'),'normal-return'),(('outcomes',),[{'stage':'enter-call:continuation','outcome':'raise'},normal[-1]])]
    for path,val in changes:
     q=mutate(v,path,val);reject(tag+'/input '+repr(path),lambda q=q:c.enter_call_projection(cat,D(q),D(q)))
    for path,val in [(('completion',),'missing-method-frontier'),(('replacement_error_in_model',),{}),(('last_pending_error_in_model','symbol'),'different-error'),(('method_roles','__enter__','symbol'),'substituted-result'),(('events',1,'outcome'),'raise'),(('lookup_completed_in_model','__exit__'),False)]:
     q=mutate(p,path,val);reject(tag+'/predecessor '+repr(path),lambda q=q:c.enter_call_binding(cat,q,q['instance_anchor'],'explicit conditional premise'),'source/model predecessor constraints; not authenticated-core validation')
    for path,val in [(('call','target_role'),p['method_roles']['__exit__']),(('call','python_explicit_arguments'),[p['binding']['operand_role']]),(('call','callability'),'ESTABLISHED'),(('call','runtime_identity'),'invented'),(('call','source','line'),2516),(('call_outcome',),'normal-return'),(('method_body_entry_established',),True),(('res_assignment_established',),True),(('terminal_python_exception_in_model',),False),(('terminal_python_exception_in_model',),1),(('current_partial_effects',),'NONE'),(('completion',),'normal-overall-return')]:
     reject(tag+'/output '+repr(path),lambda path=path,val=val:c.validate_enter_call_projection(cat,D(v),D(v),mutate(out,path,val)),'source-constructed output comparison; no authenticated basis')
    q=D(out);q['call']['target_role']=D(p['method_roles']['__exit__']);q['binding']['method_results']['__enter__']=D(p['method_roles']['__exit__']);q['events'][-1]['method_results']['__enter__']=D(p['method_roles']['__exit__'])
    reject(tag+'/coordinated target-output substitutions',lambda:c.validate_enter_call_projection(cat,D(v),D(v),q),'source-constructed output comparison; no authenticated basis')
    for path,val in [(('outcomes',0,'outcome'),S('normal')),(('outcomes',),L(normal)),(('binding','references',),Q(b['references']))]:
     q=mutate(v,path,val);reject(tag+'/input exact type '+repr(path),lambda q=q:c.enter_call_projection(cat,q,D(v)),'exact-type input gate before serialization')
    for path,val in [(('completion',),S('enter-call-attempt')),(('call','python_explicit_arguments'),L()),(('call',),Q(out['call'])),(('source_operation_acknowledged','line'),I(2514))]:
     q=mutate(out,path,val);reject(tag+'/output exact type '+repr(path),lambda q=q:c.validate_enter_call_projection(cat,D(v),D(v),q),'exact-type submitted-output gate before serialization')
    q=D(out);q['call'][S('target_role')]=q['call'].pop('target_role')
    reject(tag+'/nested subclass literal key',lambda:c.validate_enter_call_projection(cat,D(v),D(v),q),'exact-type submitted-output key gate')
    snapshot=D(v);beforecat=D(cat);out['call']['target_role']['scope']['context']='MUTATED';out['binding']['references']['owner']['symbol']='MUTATED';out['events'].clear()
    pristine=c.enter_call_projection(cat,D(v),D(v))
    check(tag+'/nested returned result cannot alter expectations',lambda:v==snapshot and cat==beforecat and c.validate_enter_call_projection(cat,D(v),D(v),D(pristine)))
    reject(tag+'/mutated returned result rejected',lambda:c.validate_enter_call_projection(cat,D(v),D(v),out),'source-constructed output comparison; no authenticated basis')
    outputs[-1]=pristine
 check('eight distinct occurrence identities despite same source call',lambda:len({o['events'][-1]['id'] for o in outputs})==8)
 return {'source_only':True,'full_public_runs':0,'full_public_negative_derivations':0,'authenticated_basis_core_runs':0,'application_runs':0,'runtime_protocol_invocations':0,'predecessor_authentication':'UNEXECUTED for new bytes; static wiring checked only','historical_groups':'117 independent / 421 Engineering / one Ubuntu public positive remain separate'}

try:
 details=main();result={'result':'PASS','finished_utc':utc(),'seconds':time.monotonic()-START,'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'rows':len(ROWS),'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
