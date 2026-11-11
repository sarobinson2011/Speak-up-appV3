"""One new pure source/model campaign. No public or authenticated-core calls."""
import ast,copy,hashlib,json,os,sys,time,traceback,types
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
D=copy.deepcopy;ROWS=[];START=time.monotonic()
def utc():return datetime.now(timezone.utc).isoformat()
def write(path,value):
 with open(path,'x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def record(name,layer,status,detail=None):
 row={'sequence':len(ROWS)+1,'utc':utc(),'name':name,'layer':layer,'status':status,'detail':detail};ROWS.append(row);write(OUT/('%04d.json'%len(ROWS)),row)
 with open(OUT/'progress.jsonl','a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
def check(name,fn,layer='pure source/model oracle; no authentication'):
 try:
  if fn() is False:raise AssertionError(name)
 except BaseException as e:record(name,layer,'FAIL',type(e).__name__+': '+str(e));raise
 record(name,layer,'PASS')
def reject(name,fn,layer='pure model constraints; no authenticated basis'):
 try:fn()
 except ValueError as e:record(name,layer,'REJECTED',str(e));return
 record(name,layer,'FAIL','expected ValueError');raise AssertionError(name)
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def change(v,path,val):
 q=D(v);p=q
 for k in path[:-1]:p=p[k]
 p[path[-1]]=val;return q
class S(str):pass
class I(int):pass
class L(list):pass
class Q(dict):pass
class B(bytes):pass
NORMAL={
 'immortal':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')]],
 'non-immortal-positive-gt-one':[{'stage':'decref-fast:'+a,'outcome':b} for a,b in [('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]]}
def main():
 m=json.loads((ROOT/'MANIFEST.json').read_bytes());check('fixed source membership and hashes',lambda:{p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==set(m)|{'MANIFEST.json'} and all({'bytes':len((ROOT/n).read_bytes()),'sha256':hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}==v for n,v in m.items()),'fixed source checkpoint identity')
 old=(ROOT/'reference/decref/code/managed_coverage.py').read_bytes();new=(ROOT/'code/managed_coverage.py').read_bytes();check('464085-byte producer prefix exact',lambda:len(old)==464085 and hashlib.sha256(old).hexdigest()=='99505e660a0adf32cdda6c45e9469ca849282914675afb5678eb52eab399388c' and new.startswith(old),'source preservation')
 names=[n.name for n in ast.parse(new[len(old):]).body if isinstance(n,ast.FunctionDef)]
 check('actual eight appended functions',lambda:names==['decref_fast_sources','decref_fast_envelope','decref_fast_catalogue','compile_decref_fast','validate_decref_fast','decref_fast_binding','decref_fast_projection','validate_decref_fast_projection'],'source preservation')
 c=load(ROOT/'code/managed_coverage.py','fast_pure_producer');a=load(ROOT/'code/correspondence.py','fast_adapter_definitions')
 files={n:(ROOT/'reference/resolution/source'/n).read_bytes() for n in json.loads((ROOT/'reference/resolution/source-index.json').read_bytes())}
 ceval=files['Python/ceval.c'].decode().splitlines();generated=files['Python/generated_cases.c.h'].decode().splitlines();bc=files['Python/bytecodes.c'].decode().splitlines()
 check('independent local override guard and exact selected occurrence',lambda:ceval[48]=='#if !defined(Py_DEBUG) && !defined(Py_TRACE_REFS)' and ceval[55]=='#undef Py_DECREF' and generated[3529].strip()==bc[2515].strip()=='Py_DECREF(enter);' and generated[3527].strip()=='#line 2515 "Python/bytecodes.c"','defining-source oracle independent of catalogue')
 check('independent fast order and direct tp_dealloc dependency',lambda:[x.strip().rstrip('\\').rstrip() for x in ceval[58:68]]==['PyObject *op = _PyObject_CAST(arg);','if (_Py_IsImmortal(op)) {','break;','}','_Py_DECREF_STAT_INC();','if (--op->ob_refcnt == 0) {','destructor dealloc = Py_TYPE(op)->tp_dealloc;','(*dealloc)(op);','}','} while (0)'],'defining-source oracle independent of catalogue')
 check('independent source bound stops before res test',lambda:bc[2516].strip()==generated[3530].strip()=='if (res == NULL) {' and '_Py_Dealloc' not in '\n'.join(ceval[55:68]),'defining-source oracle independent of catalogue')
 cats=[json.loads((ROOT/'fixtures'/n).read_bytes()) for n in ['r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json']]
 args=((ROOT/'source-evidence/lab_bootstrap.py').read_bytes(),files['Python/bytecodes.c'],(ROOT/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats,files)
 cat=c.compile_decref_fast(*args);write(OUT/'catalogue.json',cat)
 check('source-derived catalogue accepted',lambda:c.validate_decref_fast(*args,D(cat)),'independent source-derived catalogue comparison')
 check('both independent branch orders and no res prerequisite',lambda:cat['branch_orders']=={k:[r['stage'] for r in v] for k,v in NORMAL.items()} and cat['res_non_NULL_guard'] is False and cat['zero_count_route']['completion']=='UNRESOLVED')
 for path,val in [(('source','macro_definition','file'),'Include/object.h'),(('source','selected_operation','line'),2511),(('source','generated_operation','line'),3523),(('branch_guards','immortal','immortal_predicate'),False),(('branch_guards','non-immortal-positive-gt-one','starting_count'),'positive count >= 1'),(('configuration_and_C_premises','configuration','Py_DEBUG'),True),(('source','destructor_call','expression'),'_Py_Dealloc(op);'),(('res_non_NULL_guard',),True),(('zero_count_route','accepted_as_fast_branch'),True),(('declarations',),cat['declarations'][:-1]),(('branch_orders','immortal'),cat['branch_orders']['non-immortal-positive-gt-one']),(('steps',1,'allowed'),['bound','raise'])]:
  reject('catalogue alteration '+repr(path),lambda path=path,val=val:c.validate_decref_fast(*args,change(cat,path,val)),'independent source-derived catalogue comparison')
 q=D(cat);q['steps'].reverse();q['declarations'].reverse();q['branch_orders']['immortal'].reverse()
 reject('coordinated source/order/declaration substitution',lambda:c.validate_decref_fast(*args,q),'independent source-derived catalogue comparison')
 for name,oldtext,newtext in [('Python/ceval.c',b'!defined(Py_DEBUG) && !defined(Py_TRACE_REFS)',b'!defined(Py_DEBUG) || !defined(Py_TRACE_REFS)'),('Python/ceval.c',b'            break;',b'            return;'),('Python/ceval.c',b'if (--op->ob_refcnt == 0)',b'if (op->ob_refcnt-- == 0)'),('Python/generated_cases.c.h',b'res = _PyObject_CallNoArgs(enter);\n            Py_DECREF(enter);',b'res = _PyObject_CallNoArgs(enter);\n            Py_DECREF(res);')]:
  fs=dict(files);fs[name]=fs[name].replace(oldtext,newtext);reject('altered defining bytes '+name+'/'+newtext.decode(),lambda fs=fs:c.decref_fast_sources(fs),'defining-source contract/identity gate')
 fs=dict(files);fs['Python/ceval.c']=B(fs['Python/ceval.c']);reject('source bytes subclass',lambda:c.decref_fast_sources(fs),'exact source input type before decoding')
 fs=dict(files);fs[S('Python/ceval.c')]=fs.pop('Python/ceval.c');reject('source key subclass',lambda:c.decref_fast_sources(fs),'exact source input key before lookup')
 for k in ('source_identities','selected_operation'):
  q=D(cat);q['source'].pop(k);reject('omitted source selection '+k,lambda q=q:c.validate_decref_fast(*args,q),'independent source-derived catalogue comparison')
 defs={n.name:n for n in ast.parse((ROOT/'code/correspondence.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
 def has(n,s):return s in ast.unparse(defs[n])
 check('actual parent authentication and exact parent receipt comparison wired',lambda:has('_basis','p._receipt_shape') and has('_basis','p._basis(pd)') and has('_basis',"fresh['saved'] == p.enc(p._assemble(pb))") and has('_basis','compile_decref_fast'),'static mandatory wiring; public authentication UNEXECUTED')
 check('mandatory authenticated constructed parent and new output validation wired',lambda:has('_construct_checked',"basis['parent_module']._construct_checked(basis['parent_basis']") and has('_construct_checked','validate_decref_fast_projection') and has('_construct_checked','decref_fast_binding'),'static mandatory wiring; authenticated constructed path UNEXECUTED')
 check('public relation in both contexts and exact new receipt comparison wired',lambda:has('_rows','== CONTEXTS') and has('_assemble','ctx[RELATION]') and has('derive','_assemble(_basis(inputs(root)))') and has('validate','saved == enc(result)'),'static mandatory wiring; public path UNEXECUTED')
 shape={'format':'I164-DECREF-FAST-COMPLETION-1','contexts':[{'context':ctx,'decref_fast_completion_correspondence':{},'enter_decref_attempt_correspondence':{}} for ctx in a.CONTEXTS]}
 check('new receipt shape gate only',lambda:a._receipt_shape(a.enc(shape))==shape,'pre-derivation shape gate; not public positive')
 for i in range(2):
  q=D(shape);del q['contexts'][i]['decref_fast_completion_correspondence'];reject('missing mandatory context relation '+str(i),lambda q=q:a._receipt_shape(a.enc(q)),'pre-derivation shape gate; not full public negative')
 fixtures=json.loads((ROOT/'fixtures/retained-decref-cases.json').read_bytes());summaries=[];representatives={};occurrences=set();coverage=set()
 for num,f in enumerate(fixtures):
  p=f['output'];ctx=p['scope']['context'];coverage.add((ctx,p['earlier_control_completed_in_model'],p['failure_origin_region'],p['res_value_role']['C_NULL'],p['res_value_role']['python_value_class']))
  for branch in NORMAL:
   b=c.decref_fast_binding(cat,p,p['instance_anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),files)
   v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':D(NORMAL[branch])};out=c.decref_fast_projection(cat,v,v,files);label=str(num)+'/'+f['name']+'/'+branch
   check(label+'/normal accepted',lambda:c.validate_decref_fast_projection(cat,v,v,out,files),'pure model output comparison; no authenticated basis')
   check(label+'/independent branch and inherited-evidence oracle',lambda:out['conditional_fast_completion_in_model'] is True and out['new_model_claims']['macro_completion_in_model'] is True and out['new_model_claims']['break_from_do_while_in_model'] is (branch=='immortal') and out['new_model_claims']['decrement_and_nonzero_test_in_model'] is (branch!='immortal') and out['new_model_claims']['destructor_skipped_by_completed_fast_branch'] is True and out['new_model_claims']['destructor_invocation_in_model'] is False and out['new_model_claims']['interpreter_return_established'] is False and out['predecessor_projection']==p and out['res_value_role']==p['res_value_role'] and out['last_pending_error_in_model']==p['last_pending_error_in_model'] and out['helper_error_indicator']=='UNKNOWN' and out['terminal_python_exception_in_model'] is True and out['current_partial_effects'].startswith('UNKNOWN') and all(out[k] is False for k in ['result_test_established','physical_release_established','reference_count_change_established','finalization_established','context_manager_entry_established','f_binding_established','qualified_binary_correspondence','actual_admission']))
   occurrences.add(out['events'][-1]['id']);summaries.append({'name':label,'input_fixture':num,'branch':branch,'output_identity':a.identity(c.enc(out)),'qualification':'constructed source/model only, never authenticated basis or runtime observation'})
   if p['res_value_role']['python_value_class']=='opaque' and ctx not in representatives:representatives[ctx]=(D(v),D(out))
 write(OUT/'normal-model-identities.json',summaries)
 check('24 saved class variants across both contexts/prefixes/origins and three res classes; eight occurrence identities',lambda:len(fixtures)==24 and len(coverage)==24 and len(occurrences)==8)
 # Frontiers on both branches, in both contexts. Prefix/origin coverage above is separate.
 for ctx,(base,_) in representatives.items():
  for branch in NORMAL:
   v=D(base);p=v['parent_result'];v['binding']=c.decref_fast_binding(cat,p,v['anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),files);v['outcomes']=D(NORMAL[branch]);normal_out=c.decref_fast_projection(cat,v,v,files)
   for index,step in enumerate(NORMAL[branch]):
    frontiers=('raise','catchable-interruption','process-termination','unobserved') if index==0 else ('interruption','process-termination','unobserved')
    for frontier in frontiers:
     q=D(v);q['outcomes']=D(v['outcomes'][:index])+[{'stage':step['stage'],'outcome':frontier}];z=c.decref_fast_projection(cat,q,q,files);uncertain=frontier in ('interruption','process-termination','unobserved');tag=ctx+'/'+branch+'/'+str(index)+'/'+frontier
     check(tag,lambda q=q,z=z,uncertain=uncertain:c.validate_decref_fast_projection(cat,q,q,z,files) and z['conditional_fast_completion_in_model'] is False and z['terminal_python_exception_in_model'] is (None if uncertain else True) and z['C_primitive_python_exception_established'] is False and z['Python_unwind_established'] is False and z['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler'] and z['current_partial_effects'].startswith('UNKNOWN'))
     reject(tag+'/false completion',lambda q=q,z=z:c.validate_decref_fast_projection(cat,q,q,change(z,('conditional_fast_completion_in_model',),True),files),'pure model output comparison; no authenticated basis')
   # Confirm a later nonnormal frontier does not erase earlier acknowledged modeled decrement.
   if branch!='immortal':
    q=D(v);q['outcomes'][-1]['outcome']='unobserved';z=c.decref_fast_projection(cat,q,q,files)
    check(ctx+'/decrement acknowledged before incomplete macro-end',lambda:z['new_model_claims']['decrement_and_nonzero_test_in_model'] is True and z['new_model_claims']['count_relation']['nonzero'] is True and z['conditional_fast_completion_in_model'] is False and z['physical_reference_count_effects'] is None)
   for state in ('continuity','branch'):
    q=D(v);q['binding'][state]='UNESTABLISHED'
    if state=='branch':q['binding']['state_premise']['guard']=None
    q['outcomes']=[{'stage':'decref-fast:continuation','outcome':'unobserved'}]
    check(ctx+'/'+branch+'/'+state+' unknown accepted without completion',lambda q=q:c.decref_fast_projection(cat,q,q,files)['conditional_fast_completion_in_model'] is False)
    q['outcomes']=D(NORMAL[branch]);reject(ctx+'/'+branch+'/'+state+' unknown cannot complete',lambda q=q:c.decref_fast_projection(cat,q,q,files))
  v,out=base,representatives[ctx][1];p=v['parent_result']
  # Binding, selection, first-frontier, exact-type and coordinated substitutions.
  mutations=[(('scope','invocation'),'wrong'),(('anchor','context'),'wrong'),(('binding','references','owner','symbol'),'wrong'),(('binding','references','token','symbol'),'wrong'),(('binding','enter_role',),v['binding']['exit_role']),
   (('binding','enter_role',),v['binding']['res_value_role']),(('binding','selected_attempt','id'),'stale'),(('binding','helper_invocation','symbol'),'wrong'),(('binding','original_constructor_error','symbol'),'wrong'),(('binding','state_premise','derived_from_res'),True),
   (('binding','state_premise','guard','immortal_predicate'),False),(('binding','branch'),'non-immortal-count-one'),(('binding','state_premise','concrete_count'),1),(('binding','envelope','configuration','Py_DEBUG'),True),
   (('binding','envelope','configuration','Py_STATS'),True),(('binding','envelope','valid_selected_non_NULL_PyObject_pointer'),'UNKNOWN'),(('binding','envelope','defined_C_evaluation_and_integer_semantics'),'UNKNOWN'),
   (('binding','envelope','external_macro_and_include_overrides_absent'),'UNKNOWN'),(('outcomes',),v['outcomes'][:-1]),(('outcomes',),v['outcomes'][1:]),(('outcomes',),v['outcomes'][::-1]),(('outcomes',),v['outcomes']+[v['outcomes'][-1]]),
   (('outcomes',2,'outcome'),'false'),(('outcomes',1,'outcome'),'raise'),(('outcomes',1,'outcome'),'catchable-interruption'),(('outcomes',),[{'stage':'decref-fast:continuation','outcome':'process-termination'},*v['outcomes'][1:]])]
  for path,val in mutations:
   q=change(v,path,val);reject(ctx+'/input '+repr(path),lambda q=q:c.decref_fast_projection(cat,q,q,files))
  q=D(v);del q['binding']['envelope']['configuration']['Py_TRACE_REFS'];reject(ctx+'/omitted selector',lambda:c.decref_fast_projection(cat,q,q,files))
  q=D(v);q['binding']['references']['owner']['symbol']='coordinated';q['binding']['state_premise']['scope']['invocation']='coordinated'
  reject(ctx+'/coordinated input versus selected premises',lambda:c.decref_fast_projection(cat,q,v,files),'pure selected-input comparison; no authenticated basis')
  q=D(v);q['parent_result']['post_call_decref_attempt_established_in_model']=False;reject(ctx+'/false predecessor completion',lambda:c.decref_fast_projection(cat,q,q,files),'pure predecessor model constraints; no authentication')
  for path,val in [(('conditional_fast_completion_in_model',),False),(('terminal_python_exception_in_model',),False),(('new_model_claims','interpreter_return_established'),True),(('new_model_claims','destructor_invocation_in_model'),True),(('new_model_claims','zero_count_completion'),True),(('result_test_established',),True),(('physical_reference_count_effects',),0),(('runtime_macro_arrival',),True),(('helper_error_indicator',),'CLEAR'),(('current_partial_effects',),'NONE')]:
   reject(ctx+'/output '+repr(path),lambda path=path,val=val:c.validate_decref_fast_projection(cat,v,v,change(out,path,val),files),'pure model output comparison; no authenticated basis')
  q=D(out);q['binding']['enter_role']=D(v['binding']['exit_role'])
  for e in q['events']:e['enter_role']=D(v['binding']['exit_role'])
  reject(ctx+'/coordinated returned role substitution',lambda:c.validate_decref_fast_projection(cat,v,v,q,files),'pure model output comparison; fixed premises')
  for path,val in [(('outcomes',),L(v['outcomes'])),(('outcomes',0,'outcome'),S('normal')),(('binding','envelope','configuration','SIZEOF_VOID_P'),I(8)),(('binding','references',),Q(v['binding']['references']))]:
   q=change(v,path,val);reject(ctx+'/input type '+repr(path),lambda q=q:c.decref_fast_projection(cat,q,v,files),'exact input type before normalization')
  for path,val in [(('completion',),S(out['completion'])),(('events',),L(out['events'])),(('new_model_claims',),Q(out['new_model_claims'])),(('conditional_fast_completion_in_model',),1)]:
   q=change(out,path,val);reject(ctx+'/output type '+repr(path),lambda q=q:c.validate_decref_fast_projection(cat,v,v,q,files),'exact output type / exact typed comparison before normalization')
  q=D(out);q['new_model_claims'][S('macro_completion_in_model')]=q['new_model_claims'].pop('macro_completion_in_model');reject(ctx+'/literal-key subclass',lambda:c.validate_decref_fast_projection(cat,v,v,q,files),'exact output key before normalization')
  q=D(cat);q['branch_guards']['immortal']=Q(q['branch_guards']['immortal']);reject(ctx+'/semantic claim subclass',lambda:c.decref_fast_projection(q,v,v,files),'exact semantic claim before normalization')
  # Mutate actual returned objects, not copied stand-ins, with pristine input snapshots.
  before_v=D(v);before_cat=D(cat);returned=c.decref_fast_projection(cat,v,v,files);returned['binding']['enter_role']['symbol']='mutated';returned['events'].clear();returned['predecessor_projection']['res_value_role']['C_NULL']=not returned['predecessor_projection']['res_value_role']['C_NULL']
  reject(ctx+'/actual returned projection mutated',lambda:c.validate_decref_fast_projection(cat,v,v,returned,files),'pure model output comparison after direct returned mutation')
  check(ctx+'/fresh pristine result and expectations isolated',lambda:v==before_v and cat==before_cat and c.decref_fast_projection(cat,v,v,files)==out)
  b=c.decref_fast_binding(cat,p,v['anchor'],'explicit conditional premise','immortal',c.decref_fast_envelope(),files);b['state_premise']['enter_role']['symbol']='mutated';b['references'].clear()
  check(ctx+'/returned binding isolated',lambda:v==before_v and cat==before_cat and c.decref_fast_binding(cat,p,v['anchor'],'explicit conditional premise','immortal',c.decref_fast_envelope(),files)==v['binding'])
  isolated=c.decref_fast_catalogue(cats[-1],files);isolated['configuration_and_C_premises']['configuration'].clear();isolated['source']['source_identities'].clear()
  check(ctx+'/returned catalogue isolated',lambda:c.decref_fast_catalogue(cats[-1],files)==cat)
 check('source file bytes unchanged after controls',lambda:all((ROOT/'reference/resolution/source'/n).read_bytes()==v for n,v in files.items()),'source preservation')
 return {'new_public_authentication':'UNEXECUTED','new_authenticated_constructed_path':'UNEXECUTED','public_runs':0,'full_public_negative_derivations':0,'runtime_source_execution':0,'historical_campaign_replays':0,'independent_acceptance':'PENDING','prior_groups':'184 primary; eight supplement; 750 Engineering; one saved public positive, all separate'}
try:
 details=main();result={'result':'PASS','rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')},'finished_utc':utc(),'seconds':time.monotonic()-START,'qualifications':details};write(OUT/'RESULT.json',result);print(json.dumps({'event':'RESULT','result':result},sort_keys=True),flush=True)
except BaseException as e:
 traceback.print_exc();write(OUT/'FAILURE.json',{'utc':utc(),'exception':type(e).__name__,'message':str(e),'completed_rows':len(ROWS),'counts':{s:sum(r['status']==s for r in ROWS) for s in ('PASS','REJECTED','FAIL')}});raise
