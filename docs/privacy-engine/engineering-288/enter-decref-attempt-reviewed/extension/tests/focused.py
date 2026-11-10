"""One new focused source/model pass. No public or authenticated-core execution."""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
D=copy.deepcopy;ROWS=[];START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def write(path,value):
 with open(path,'x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 row={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(row);write(OUT/('%04d.json'%len(ROWS)),row)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
def check(name,fn,layer='new pure source/model oracle; no authentication'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='new pure model input constraints; no authenticated basis'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 record(name,layer,'FAIL','expected ValueError');raise AssertionError(name)
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def change(v,path,value):
 q=D(v);p=q
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return q
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
def main():
 manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
 check('fixed source manifest exact files and hashes',lambda:{p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==set(manifest)|{'MANIFEST.json'} and all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in manifest.items()),'source checkpoint identity')
 old=(ROOT/'reference/return/code/managed_coverage.py').read_bytes();new=(ROOT/'code/managed_coverage.py').read_bytes()
 check('exact reviewed 452888-byte producer prefix preserved',lambda:len(old)==452888 and hashlib.sha256(old).hexdigest()=='a3e41b8c14c8c1c25d26b45eb0645b3222bd6a6afb60f7ccc44f7a655ae79a37' and new.startswith(old),'source checkpoint identity')
 check('exact five-function appended slice',lambda:[n.name for n in ast.parse(new[len(old):]).body if isinstance(n,ast.FunctionDef)]==['compile_enter_decref','validate_enter_decref','enter_decref_binding','enter_decref_projection','validate_enter_decref_projection'],'source checkpoint identity')
 c=load(ROOT/'code/managed_coverage.py','decref_pure_producer');a=load(ROOT/'code/correspondence.py','decref_adapter_definitions')
 launcher=(ROOT/'source-evidence/lab_bootstrap.py').read_bytes();bc=(ROOT/'reference/cpython-3.12.14/bytecodes.c').read_bytes();tt=(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes();lines=bc.decode().splitlines()
 fn=next(x for x in ast.parse(launcher).body if isinstance(x,ast.FunctionDef) and x.name=='write_new')
 check('independent source line24 with operand',lambda:fn.lineno==23 and fn.body[0].lineno==24 and ast.unparse(fn.body[0].items[0].context_expr)=="open(p, 'xb')",'defining-source oracle')
 check('independent assignment then unconditional enter decrement then result test',lambda:[x.strip() for x in lines[2514:2517]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {'],'defining-source oracle')
 check('earlier failed-lookup decrement and DECREF_INPUTS are distinct',lambda:lines[2510].strip()=='Py_DECREF(enter);' and lines[2513].strip()=='DECREF_INPUTS();','defining-source oracle')
 r1,lookup,enter,parentcat=[json.loads((ROOT/'fixtures'/n).read_bytes()) for n in ['r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json']]
 args=(launcher,bc,tt,r1,lookup,enter,parentcat);cat=c.compile_enter_decref(*args);write(OUT/'catalogue.json',cat)
 check('source-derived catalogue admitted',lambda:c.validate_enter_decref(*args,D(cat)),'source-derived catalogue comparison')
 check('independent two-stage and no non-NULL guard oracle',lambda:cat['source']['order']==['enter-decref:continuation','enter-decref:attempt'] and cat['source']['operation']['line']==2516 and cat['source']['operation']['expression']=='Py_DECREF(enter);' and cat['source']['operand_expression']=='enter' and cat['source']['res_non_NULL_guard'] is False and cat['source']['next_operation_excluded']['line']==2517)
 for path,val in [(('source','order'),['enter-decref:attempt','enter-decref:continuation']),(('source','operation','line'),2511),(('source','operand_expression'),'res'),(('source','res_non_NULL_guard'),True),(('source','res_classes'),['non-NULL/opaque']),(('source','steps',1,'allowed'),['attempted','completed','raise']),(('source','steps',0,'allowed'),['normal']),(('declarations',),cat['declarations'][:-1]),(('source','next_operation_excluded','line'),2518),(('parent_catalogue_sha256',),'0'*64)]:
  reject('catalogue altered '+repr(path),lambda path=path,val=val:c.validate_enter_decref(*args,change(cat,path,val)),'source-derived catalogue comparison')
 q=D(cat);q['source']['order'].reverse();q['source']['steps'].reverse();q['declarations'].reverse()
 reject('coordinated declaration and stage reorder',lambda:c.validate_enter_decref(*args,q),'source-derived catalogue comparison')
 q=D(parentcat);q['source']['target']='other';q['source']['assignment']['expression']='other = _PyObject_CallNoArgs(enter);'
 reject('coordinated parent catalogue substitution',lambda:c.compile_enter_decref(launcher,bc,tt,r1,lookup,enter,q),'defining-source predecessor catalogue recomputation')
 changed=bc.replace(b'res = _PyObject_CallNoArgs(enter);\n            Py_DECREF(enter);',b'res = _PyObject_CallNoArgs(enter);\n            Py_DECREF(res);')
 reject('wrong selected operation defining bytes',lambda:c.compile_enter_decref(launcher,changed,tt,r1,lookup,enter,parentcat),'defining-source identity/order')
 defs={n.name:n for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 def has(n,s):return s in ast.unparse(defs[n])
 check('unchanged actual parent authentication and returned basis wired',lambda:has('_basis','p._basis(pd)') and has('_basis',"fresh['saved'] == p.enc(p._assemble(pb))") and has('_basis','compile_enter_decref'),'static adapter inspection; new authentication UNEXECUTED')
 check('parent constructed validator before new binding and mandatory output validator',lambda:has('_construct_checked',"basis['parent_module']._construct_checked(basis['parent_basis']") and has('_construct_checked','validate_enter_decref_projection') and has('_construct_checked','enter_decref_binding'),'static adapter inspection; authenticated constructed path UNEXECUTED')
 check('both contexts public relation and exact byte comparison wired',lambda:has('_rows','== CONTEXTS') and has('_assemble','ctx[RELATION]') and has('derive','_assemble(_basis(inputs(root)))') and has('validate','saved == enc(result)'),'static public integration inspection; no public invocation')
 minimal={'format':'I164-ENTER-DECREF-ATTEMPT-1','contexts':[{'context':ctx,'enter_decref_attempt_correspondence':{},'enter_return_res_correspondence':{}} for ctx in a.CONTEXTS]}
 check('JSON shape only accepts both relation keys',lambda:a._receipt_shape(a.enc(minimal))==minimal,'pre-derivation shape gate only; not public positive')
 for i in range(2):
  for relation in ('enter_decref_attempt_correspondence','enter_return_res_correspondence'):
   q=D(minimal);del q['contexts'][i][relation];reject('shape missing '+str(i)+'/'+relation,lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate only; not full public negative')
 fixtures=json.loads((ROOT/'fixtures/retained-return-cases.json').read_bytes());normal=[{'stage':'enter-decref:continuation','outcome':'normal'},{'stage':'enter-decref:attempt','outcome':'attempted'}]
 cases=[];occurrences=[]
 for num,fixture in enumerate(fixtures):
  p=fixture['output'];tag=str(num)+'/'+fixture['name'];b=c.enter_decref_binding(cat,p,p['instance_anchor'],'explicit conditional premise')
  v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':D(normal)};out=c.enter_decref_projection(cat,D(v),D(v));cases.append({'name':tag,'input':D(v),'output':D(out),'qualification':'new pure source/model case over saved reviewed premises, not authenticated basis or runtime observation'});occurrences.append(out['events'][-1]['id'])
  check(tag+'/normal source attempt accepted',lambda:c.validate_enter_decref_projection(cat,D(v),D(v),D(out)))
  check(tag+'/independent enter-operand and occurrence oracle',lambda:out['post_call_decref_attempt_established_in_model'] is True and out['decref_operation']['source']['line']==2516 and out['decref_operation']['operand_expression']=='enter' and out['decref_operation']['operand_role']==p['binding']['method_results']['__enter__'] and out['binding']['exit_role']==p['binding']['method_results']['__exit__'] and out['binding']['res_value_role']==p['res_value_role'] and out['events'][-1]['selected_assignment']==p['events'][-1]['id'])
  check(tag+'/result classes and original error survive attempt',lambda:out['res_assignment']==p['res_assignment'] and out['res_value_role']==p['res_value_role'] and out['call_result_role']==p['call_result_role'] and out['helper_error_indicator']=='UNKNOWN' and out['helper_error_contract_established'] is False and out['C_NULL_implies_python_exception_established'] is False and out['terminal_python_exception_in_model'] is True and out['last_pending_error_in_model']==p['last_pending_error_in_model'])
  check(tag+'/prior effects and cleanup evidence retained',lambda:out['predecessor_projection']==p and out['prior_acknowledged_partial_effects']==p['current_partial_effects'] and out['cleanup_list_state']==p['cleanup_list_state'] and out['retained_cleanup_error_evidence']==p['retained_cleanup_error_evidence'] and out['failure_origin_region']==p['failure_origin_region'] and out['earlier_control_completed_in_model']==p['earlier_control_completed_in_model'])
  flags=['post_call_decref_established','decref_completion_established','decref_effects_established','macro_expansion_established','reference_count_change_established','finalization_established','decref_callback_execution_established','physical_release_established','result_test_established','result_error_routing_established','context_manager_entry_established','f_binding_established','actual_admission']
  check(tag+'/attempt stops before all completion and effect claims',lambda:all(out[k] is False for k in flags) and out['runtime_enter_decref_chain'] is None and out['decref_operation']['concrete_reference_count'] is None)
  q=D(v);q['binding']['continuity']='UNESTABLISHED';q['outcomes']=[{'stage':'enter-decref:continuation','outcome':'unobserved'}]
  check(tag+'/unestablished continuation preserves assignment but no attempt',lambda:c.enter_decref_projection(cat,D(q),D(q))['post_call_decref_attempt_established_in_model'] is False)
  q=D(v);q['binding']['continuity']='UNESTABLISHED';reject(tag+'/assignment cannot supply continuation',lambda:c.enter_decref_projection(cat,D(q),D(q)))
  # Full mutation set once per context/prefix/origin; all three C classes above.
  if p['res_value_role']['python_value_class']!='opaque':continue
  for stage,frontier in [(0,x) for x in ('raise','catchable-interruption','process-termination','unobserved')]+[(1,x) for x in ('process-termination','unobserved')]:
   q=D(v);q['outcomes']=D(normal[:stage])+[{'stage':normal[stage]['stage'],'outcome':frontier}];z=c.enter_decref_projection(cat,D(q),D(q));abrupt=frontier in ('process-termination','unobserved')
   check(tag+'/'+str(stage)+'/'+frontier,lambda q=q,z=z,abrupt=abrupt:c.validate_enter_decref_projection(cat,D(q),D(q),D(z)) and z['post_call_decref_attempt_established_in_model'] is False and z['res_assignment']==p['res_assignment'] and z['terminal_python_exception_in_model'] is (None if abrupt else True) and (z['replacement_error_in_model'] is None)==abrupt and z['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'])
   reject(tag+'/'+str(stage)+'/'+frontier+'/false arrival',lambda q=q,z=z:c.validate_enter_decref_projection(cat,D(q),D(q),change(z,('post_call_decref_attempt_established_in_model',),True)),'pure model output comparison; no authenticated basis')
  changes=[(('scope','invocation'),'other'),(('anchor','context'),'other'),(('binding','references','owner','symbol'),'other'),(('binding','references','token','symbol'),'other'),(('binding','operand_role',),b['exit_role']),
   (('binding','operand_role',),b['res_value_role']),(('binding','operand_role','symbol'),'other'),(('binding','exit_role','symbol'),'other'),(('binding','assignment_occurrence','id'),'stale'),(('binding','original_constructor_error','symbol'),'other'),(('binding','details_role','symbol'),'other'),
   (('outcomes',),normal[:1]),(('outcomes',),normal[1:]),(('outcomes',),normal[::-1]),(('outcomes',),normal+[normal[-1]]),(('outcomes',1,'outcome'),'completed'),(('outcomes',1,'outcome'),'raise'),(('outcomes',),[{'stage':'enter-decref:continuation','outcome':'process-termination'},normal[1]])]
  for path,val in changes:
   q=change(v,path,val);reject(tag+'/input '+repr(path),lambda q=q:c.enter_decref_projection(cat,D(q),D(q)))
  for path,val in [(('res_assignment_established',),False),(('helper_c_return_completed_in_model',),False),(('res_assignment','target'),'other'),(('events',2,'outcome'),'unobserved'),(('res_value_role','C_NULL'),True),(('post_call_decref_established',),True),(('result_test_established',),True)]:
   q=change(p,path,val);reject(tag+'/predecessor '+repr(path),lambda q=q:c.enter_decref_binding(cat,q,q['instance_anchor'],'explicit conditional premise'),'pure predecessor model correspondence; no authentication')
  for path,val in [(('decref_operation','source','line'),2511),(('decref_operation','operand_role',),b['exit_role']),(('events',1,'selected_assignment'),'other'),(('post_call_decref_attempt_established_in_model',),1),(('terminal_python_exception_in_model',),False),(('helper_error_indicator',),'SET'),(('current_partial_effects',),'NONE')]+[((k,),True) for k in flags[:-1]]:
   reject(tag+'/output '+repr(path),lambda path=path,val=val:c.validate_enter_decref_projection(cat,D(v),D(v),change(out,path,val)),'pure model output comparison; no authenticated basis')
  q=D(out);q['decref_operation']['operand_role']=D(b['exit_role']);q['binding']['operand_role']=D(b['exit_role'])
  for e in q['events']:e['operand_role']=D(b['exit_role'])
  reject(tag+'/coordinated output operand substitution',lambda:c.validate_enter_decref_projection(cat,D(v),D(v),q),'pure model output comparison; fixed selected premises')
  q=D(v);q['binding']['references']['owner']['symbol']='coordinated'
  reject(tag+'/selected premises cannot change with submission',lambda:c.enter_decref_projection(cat,D(q),D(v)),'pure model selected-input comparison; no authenticated basis')
  for path,val in [(('outcomes',0,'outcome'),S('normal')),(('outcomes',),L(normal)),(('binding','references',),Q(b['references']))]:
   q=change(v,path,val);reject(tag+'/input exact type '+repr(path),lambda q=q:c.enter_decref_projection(cat,q,D(v)),'exact input type gate before normalization')
  for path,val in [(('completion',),S('enter-decref-attempt')),(('decref_operation','source','line'),I(2516)),(('decref_operation',),Q(out['decref_operation'])),(('events',),L(out['events']))]:
   q=change(out,path,val);reject(tag+'/output exact type '+repr(path),lambda q=q:c.validate_enter_decref_projection(cat,D(v),D(v),q),'exact output type gate before normalization')
  q=D(out);q['decref_operation'][S('spelling')]=q['decref_operation'].pop('spelling')
  reject(tag+'/subclassed literal key',lambda:c.validate_enter_decref_projection(cat,D(v),D(v),q),'exact output key gate before normalization')
  q=D(cat);q['source']['operand_expression']=S('enter');reject(tag+'/semantic claim exact type',lambda:c.enter_decref_projection(q,D(v),D(v)),'exact semantic claim type gate before normalization')
  old_v=D(v);old_cat=D(cat);q=out;q['binding']['operand_role']['symbol']='mutated';q['events'].clear();q['res_assignment']['value']['C_NULL']=True
  reject(tag+'/nested result mutations rejected',lambda:c.validate_enter_decref_projection(cat,D(v),D(v),q),'pure model output comparison; no authenticated basis')
  check(tag+'/pristine expectations isolated after returned mutation',lambda:v==old_v and cat==old_cat and c.validate_enter_decref_projection(cat,D(v),D(v),c.enter_decref_projection(cat,D(v),D(v))))
 write(OUT/'constructed-cases.json',cases)
 check('24 class variants over eight distinct occurrences, not 24 runtime calls',lambda:len(cases)==24 and len(set(occurrences))==8)
 return {'public_runs':0,'new_authentication_path':'UNEXECUTED; static mandatory wiring only','authenticated_constructed_runs':0,'full_public_negative_derivations':0,'application_helper_execution':0,'runtime_operation_arrival':'UNAVAILABLE','historical_campaign_replays':0,'independent_acceptance':'PENDING','separate_prior_groups':'253 independent; 723 Engineering; one completed Ubuntu public positive; all older groups unchanged'}
try:
 details=main();result={'result':'PASS','rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'finished_utc':utc(),'seconds':time.monotonic()-START,'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
