"""Formal-Lab[6]: independent pure-source/model review, no authentication replay.
Retained constructed premises are setup only, never authenticated bases or runtime evidence.
"""
from pathlib import Path
import json,sys,os,copy,types,hashlib,ast,time,traceback,datetime,importlib.metadata
B=Path(__file__).resolve().parent;R=B/'candidate';O=B/'independent';D=copy.deepcopy
O.mkdir(exist_ok=False);rows=[];start=time.monotonic()
def save(p,v):
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def module(p,n):
 m=types.ModuleType(n);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def eq(a,b):assert a==b,(a,b)
def test(name,layer,fn,rejection=None):
 try:
  try:detail=fn()
  except ValueError as e:
   if rejection is None or not str(e).startswith(rejection):raise
   status='REJECTED';detail={'exception':'ValueError','code':str(e)}
  else:
   if rejection is not None:raise AssertionError('UNEXPECTED ACCEPTANCE')
   status='PASS'
 except BaseException as e:status='FAIL';detail={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
 row={'sequence':len(rows)+1,'name':name,'layer':layer,'status':status,'detail':detail,'utc':now()};rows.append(row)
 save(O/f'{len(rows):04d}.json',row)
 with (O/'progress.jsonl').open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(row,sort_keys=True),flush=True)
 if status=='FAIL':raise AssertionError('FAILED: '+name)
def mutate(v,path,value):
 q=D(v);x=q
 for k in path[:-1]:x=x[k]
 x[path[-1]]=value;return q
class S(str):pass
class L(list):pass
class Q(dict):pass
def main():
 def audit(event,args):
  if event.startswith(('socket.','sqlite3.','subprocess.','os.system','os.exec','os.spawn')):raise RuntimeError('PROHIBITED:'+event)
  if event=='exec' and any(t in str(args[0].co_filename) for t in ('source-evidence/','reference/resolution/source/')):raise RuntimeError('APPLICATION/C-SOURCE-EXECUTION-PROHIBITED')
 sys.addaudithook(audit)
 c=module(R/'code/managed_coverage.py','_review_exit_model');a=module(R/'code/correspondence.py','_review_exit_rows')
 save(O/'environment.json',{'python':sys.version,'executable':sys.executable,'cryptography':importlib.metadata.version('cryptography'),'producer':identity((R/'code/managed_coverage.py').read_bytes()),'adapter':identity((R/'code/correspondence.py').read_bytes()),'public_authentication':'not called','authenticated_constructed_path':'UNEXECUTED'})
 files={n:(R/'reference/resolution/source'/n).read_bytes() for n in read(R/'reference/resolution/source-index.json')}
 bc=files['Python/bytecodes.c'].decode().splitlines();gc=files['Python/generated_cases.c.h'].decode().splitlines()
 def source():
  assert bc[2501].strip()=='exit = _PyObject_LookupSpecial(mgr, &_Py_ID(__exit__));' and bc[2502].strip()=='if (exit == NULL) {'
  assert [x.strip() for x in bc[2514:2520]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','ERROR_IF(true, error);','}']
  assert gc[3497].strip()=='PyObject *exit;' and gc[3513].strip()==bc[2501].strip()
  assert [x.strip() for x in gc[3528:3534]]==['res = _PyObject_CallNoArgs(enter);','Py_DECREF(enter);','if (res == NULL) {','Py_DECREF(exit);','if (true) goto pop_1_error;','}']
  assert [x.strip() for x in gc[3535:3539]]==['STACK_GROW(1);','stack_pointer[-1] = res;','stack_pointer[-2] = exit;','DISPATCH();']
  assert (R/'source-evidence/lab_bootstrap.py').read_text().splitlines()[23].strip()=="with open(p,'xb') as f:"
  return {'true_branch_operation':[2518,3532],'operand_origin':[2502,3514],'excluded_successor':[2519,3533],'excluded_false_branch':[3536,3537,3538,3539],'runtime_execution':False}
 test('independent source order, selected exit origin and stopping boundary','read-only defining source',source)
 cats=[read(R/'fixtures'/n) for n in ('r1-catalogue.json','lookup-catalogue.json','enter-catalogue.json','return-catalogue.json','decref-catalogue.json')]
 args=[(R/'source-evidence/lab_bootstrap.py').read_bytes(),files['Python/bytecodes.c'],(R/'reference/cpython-3.12.14/typeobject.c').read_bytes(),*cats]
 fast=c.compile_decref_fast(*args,files);res=c.compile_res_null(*args,fast,files);cat=c.compile_exit_decref(*args,fast,res,files)
 def catalogue():
  assert cat['order']==['exit-decref:continuation','exit-decref:attempt'] and cat['guard_branches']['comparison_required'] is True
  assert set(cat['required_predecessor_facts'])=={'res_null_test_completed_in_model','res_null_test_outcome','conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established'}
  assert [x['normal'] for x in cat['steps']]==['normal','attempted']
  assert cat['source']['operation']['line']==2518 and cat['source']['generated_operation']['line']==3532
  return {'normal_stage_count':2,'no_completion_stage':True}
 test('independent required guard and two-stage catalogue','source-derived catalogue comparison',catalogue)
 for label,path,v in [('remove-comparison',('guard_branches','comparison_required'),False),('wrong-operand',('source','operation','expression'),'Py_DECREF(enter);'),('remove-continuity-stage',('steps',),cat['steps'][1:]),('wrong-generated-location',('source','generated_operation','line'),3530)]:
  q=mutate(cat,path,v);test(label,'submitted catalogue versus defining source',lambda q=q:c.validate_exit_decref(*args,fast,res,files,q),'EXIT-DECREF')
 def wiring():
  t=(R/'code/correspondence.py').read_text();f={n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
  assert 'fresh=inputs(' in f['_basis'] and 'pb=p._basis(pd)' in f['_basis'] and 'fresh[\'saved\']==p.enc(p._assemble(pb))' in f['_basis']
  assert f['_basis'].index('p._basis(pd)')<f['_basis'].index('compile_exit_decref(')
  assert f['_construct_checked'].index("basis['parent_module']._construct_checked")<f['_construct_checked'].index('c.exit_decref_binding(')<f['_construct_checked'].index('validate_exit_decref_projection(')
  assert 'saved==enc(result)' in f['validate'] and 'derive(root)' in f['validate'] and 'ctx[RELATION]' in f['_assemble']
  return {'mandatory_authentication':'statically verified; saved public run assessed separately','authenticated_constructed_path':'UNEXECUTED'}
 test('mandatory actual-parent and exact receipt wiring','static integration inspection only',wiring)
 fixtures=read(R/'fixtures/retained-decref-cases.json');parents={};normal_cases={};outputs={};coverage=set();setup=[]
 fast_steps={'immortal':[('continuation','normal'),('operand','bound'),('immortal-test','true'),('break','taken'),('macro-end','completed')],'non-immortal-positive-gt-one':[('continuation','normal'),('operand','bound'),('immortal-test','false'),('statistics','no-op'),('decrement-zero-test','nonzero'),('macro-end','completed')]}
 normal=[{'stage':'exit-decref:continuation','outcome':'normal'},{'stage':'exit-decref:attempt','outcome':'attempted'}]
 def project(v):return c.exit_decref_projection(cat,v,v,files)
 def bind(p,cont='explicit conditional premise',continuity='explicit conditional premise'):return c.exit_decref_binding(cat,p,p['instance_anchor'],cont,continuity,files)
 def base(p):return {'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':bind(p),'outcomes':D(normal)}
 for i,f in enumerate(fixtures):
  for branch,order in fast_steps.items():
   p=f['output'];fb=c.decref_fast_binding(fast,p,p['instance_anchor'],'explicit conditional premise',branch,c.decref_fast_envelope(),files)
   v={'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':fb,'outcomes':[{'stage':'decref-fast:'+s,'outcome':o} for s,o in order]}
   fp=c.decref_fast_projection(fast,v,v,files);rb=c.res_null_binding(res,fp,fp['instance_anchor'],'explicit conditional premise','explicit conditional premise',files)
   cname=f['name'].split('/')[-1];is_null=cname=='NULL'
   rv={'scope':D(fp['scope']),'anchor':D(fp['instance_anchor']),'parent_result':fp,'binding':rb,'outcomes':[{'stage':'res-null:continuation','outcome':'normal'},{'stage':'res-null:comparison','outcome':'true' if is_null else 'false'}]}
   parent=c.res_null_projection(res,rv,rv,files);parents[i,branch]=parent;setup.append({'fixture':i,'branch':branch,'identity':identity(c.enc(parent)),'credit':0})
   coverage.add((parent['scope']['context'],parent['scope']['invocation'].split('/')[-2],parent['failure_origin_region'],branch,cname))
   label=f['name']+'/'+branch
   if not is_null:
    test(label+'/false comparison cannot supply attempt','pure selected-true-predecessor gate; source-backed non-NULL premise',lambda parent=parent:bind(parent),'EXIT-DECREF-MISSING-TRUE-PREDECESSOR:res_null_test_outcome');continue
   v=base(parent);normal_cases[i,branch]=v
   def positive(v=v,parent=parent,i=i,branch=branch):
    out=project(v);outputs[i,branch]=out
    assert out['exit_decref_attempt_in_model'] is True and out['completion']=='exit-decref-attempt'
    assert [x['stage'] for x in out['events']]==['exit-decref:continuation','exit-decref:attempt']
    assert out['exit_decref_attempt']['operand_role']==parent['binding']['exit_role'] and out['binding']['operand_role']!=out['binding']['enter_role'] and out['binding']['operand_role']!=out['binding']['res_value_role']
    assert out['binding']['selected_lookup']['id']==out['binding']['operand_role']['lookup_occurrence'] and out['binding']['selected_lookup']['outcome']=='found'
    assert out['exit_decref_attempt']['source']['line']==2518 and out['exit_decref_attempt']['generated_source']['line']==3532
    assert out['predecessor_projection']==parent and out['last_pending_error_in_model']==parent['last_pending_error_in_model'] and out['terminal_python_exception_in_model'] is True
    assert out['original_error_pending_in_outer_handler']==parent['original_error_pending_in_outer_handler'] and out['prior_acknowledged_partial_effects']==parent['current_partial_effects']
    assert out['helper_error_indicator']=='UNKNOWN' and out['current_partial_effects'].startswith('UNKNOWN')
    for k in ('exit_decref_attempt_established','exit_decref_completion_established','exit_macro_expansion_established','exit_refcount_effects_established','exit_destructor_invocation_established','result_error_routing_established','stack_operations_established','dispatch_established','f_binding_established','context_manager_entry_established','actual_admission'):assert out[k] is False,k
    assert out['runtime_exit_decref_arrival'] is None and out['binding']['physical_identity'] is None
    return {'input_identity':identity(c.enc(v)),'output_identity':identity(c.enc(out)),'fixture':i,'branch':branch,'scope':D(parent['scope']),'observation':'constructed conditional model only'}
   test(label+'/selected attempt','pure-model derivation with independent source oracle',positive)
 save(O/'parent-premises.json',setup)
 test('two contexts/prefixes/origins/fast branches and three return classes','conditional matrix coverage, not runtime counts',lambda:eq(len(coverage),48))
 for i,branch in [(2,'immortal'),(23,'non-immortal-positive-gt-one')]:
  v=normal_cases[i,branch];parent=v['parent_result'];pristine=outputs[i,branch];label=parent['scope']['context']
  save(O/f'fixture-{i}.json',{'fixture':i,'fast_branch':branch,'case':v,'expected_output':pristine,'authentication':'NOT AUTHENTICATED; constructed pure-model fixture'})
  test(label+'/pristine output accepted','pure output-comparison validator',lambda:c.validate_exit_decref_projection(cat,v,v,pristine,files))
  for key in ('continuation','exit_role_continuity'):
   q=D(v);q['binding'][key]='UNESTABLISHED';q['outcomes']=[{'stage':'exit-decref:continuation','outcome':'unobserved'}]
   def unknown(q=q):
    o=project(q);assert o['exit_decref_attempt'] is None and o['exit_decref_attempt_in_model'] is False and o['terminal_python_exception_in_model'] is None and o['res_null_test_outcome'] is True
    assert o['last_pending_error_in_model']==parent['last_pending_error_in_model'];return {'frontier':'unobserved','earlier_comparison_preserved':True}
   test(label+'/'+key+' UNESTABLISHED','pure uncertainty derivation',unknown)
   bad=D(q);bad['outcomes']=D(normal);test(label+'/'+key+' UNKNOWN cannot attempt','pure conditional-premise gate',lambda bad=bad:project(bad),'EXIT-DECREF-UNESTABLISHED-PREMISE')
   bad=D(v);bad['binding'].pop(key);test(label+'/'+key+' missing','pure required-premise gate',lambda bad=bad:project(bad),'EXIT-DECREF-MISSING-PREMISE')
   bad=D(v);bad['binding'][key]=True;test(label+'/'+key+' bool is not premise','pure exact premise value gate',lambda bad=bad:project(bad),'EXIT-DECREF')
  for key in ('res_null_test_completed_in_model','res_null_test_outcome','conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established'):
   q=D(parent);q.pop(key);test(label+'/missing '+key,'pure predecessor fact gate',lambda q=q:bind(q),'EXIT-DECREF-MISSING-TRUE-PREDECESSOR')
  for at,frontiers in [(0,('raise','catchable-interruption','process-termination','unobserved')),(1,('interruption','process-termination','unobserved'))]:
   for frontier in frontiers:
    q=D(v);q['outcomes']=q['outcomes'][:at+1];q['outcomes'][-1]['outcome']=frontier
    def nonnormal(q=q,frontier=frontier,at=at):
     out=project(q);assert len(out['events'])==at+1 and out['exit_decref_attempt_in_model'] is False and out['exit_decref_attempt'] is None
     assert out['res_null_test_completed_in_model'] is True and out['res_null_test_outcome'] is True and out['predecessor_projection']==parent
     assert out['original_error_pending_in_outer_handler']==parent['original_error_pending_in_outer_handler'] and out['prior_acknowledged_partial_effects']==parent['current_partial_effects']
     if frontier in ('raise','catchable-interruption'):
      assert out['terminal_python_exception_in_model'] is True and out['last_pending_error_in_model']==out['replacement_error_in_model'] and out['replacement_error_in_model']['kind']==frontier
      assert out['last_pending_error_in_model']!=parent['last_pending_error_in_model']
     else:assert out['terminal_python_exception_in_model'] is None and out['pending_error_at_frontier']=='UNESTABLISHED' and out['last_pending_error_in_model']==parent['last_pending_error_in_model']
     assert out['Python_unwind_established'] is False and out['C_primitive_python_exception_established'] is False
     return {'at':at,'frontier':frontier,'no_attempt':True,'earlier_facts_preserved':True}
    test(label+f'/{at}/{frontier}','pure first-nonnormal/error-lineage derivation',nonnormal)
    bad=D(q);bad['outcomes'].append(D(normal[-1]));test(label+f'/{at}/{frontier}/later claim','pure first-nonnormal/order rejection',lambda bad=bad:project(bad),'EXIT-DECREF-UNREACHED-STEPS')
  changes=[('enter-for-exit',('binding','operand_role'),v['binding']['enter_role']),('res-for-exit',('binding','operand_role'),v['binding']['res_value_role']),('wrong-storage',('binding','exit_storage_role','symbol'),'unrelated'),('wrong-lookup-occurrence',('binding','selected_lookup','id'),'unrelated'),('wrong-compare',('binding','comparison','id'),'unrelated'),('wrong-owner',('binding','references','owner','symbol'),'unrelated'),('wrong-token',('binding','references','token','symbol'),'unrelated'),('wrong-acquisition',('scope','acquisition'),'unrelated'),('wrong-instance',('anchor','instance','binding'),'unrelated'),('missing-continuation',('outcomes',),normal[1:]),('reordered',('outcomes',),normal[::-1]),('attempt-completion',('outcomes',1,'outcome'),'completed'),('invented-C-raise',('outcomes',1,'outcome'),'raise')]
  for name,path,value in changes:
   bad=mutate(v,path,value);test(label+'/'+name,'pure lineage/operand/order comparison',lambda bad=bad:project(bad),'EXIT-DECREF')
  bad=D(v);bad['binding']['operand_role']=D(v['binding']['enter_role']);bad['binding']['selected_lookup']['method']='__enter__';bad['binding']['exit_storage_role']['lookup_occurrence']=bad['binding']['operand_role']['lookup_occurrence']
  test(label+'/coordinated enter role/storage/lookup','pure selected-parent binding comparison',lambda:project(bad),'EXIT-DECREF')
  bad=D(v);bad['scope']['invocation']='other';bad['binding']['scope']['invocation']='other';bad['binding']['operand_role']['scope']['invocation']='other'
  test(label+'/coordinated invocation','pure selected-parent scope comparison',lambda:project(bad),'EXIT-DECREF')
  for path,value in [(('terminal_python_exception_in_model',),False),(('exit_decref_completion_established',),True),(('exit_macro_expansion_established',),True),(('result_error_routing_established',),True),(('runtime_exit_decref_arrival',),True),(('helper_error_indicator',),'CLEAR'),(('last_pending_error_in_model',),None)]:
   bad=mutate(pristine,path,value);test(label+'/output '+repr(path),'pure submitted-output comparison',lambda bad=bad:c.validate_exit_decref_projection(cat,v,v,bad,files),'EXIT-DECREF-OUTPUT-CORRESPONDENCE')
  for path,value in [(('outcomes',),L(normal)),(('outcomes',0,'outcome'),S('normal')),(('binding','references'),Q(v['binding']['references'])),(('binding','comparison_result'),1)]:
   bad=mutate(v,path,value);test(label+'/input-type '+repr(path),'exact input type before normalization / selected binding',lambda bad=bad:project(bad),'EXIT-DECREF')
  bad=D(v);bad['outcomes'][0][S('outcome')]=bad['outcomes'][0].pop('outcome')
  test(label+'/subclassed input key','exact input-key type before normalization',lambda:project(bad),'EXIT-DECREF')
  for path,value in [(('completion',),S(pristine['completion'])),(('events',),L(pristine['events'])),(('exit_decref_attempt_in_model',),1)]:
   bad=mutate(pristine,path,value);test(label+'/output-type '+repr(path),'exact output type/comparison',lambda bad=bad:c.validate_exit_decref_projection(cat,v,v,bad,files),'EXIT-DECREF')
  before=D(v);beforecat=D(cat);changed=project(v);changed['binding']['operand_role'].clear();changed['events'].clear();changed['predecessor_projection']['binding']['exit_role'].clear()
  test(label+'/direct returned nested mutation rejects','pure output comparison after mutating actual returned object',lambda:c.validate_exit_decref_projection(cat,v,v,changed,files),'EXIT-DECREF-OUTPUT-CORRESPONDENCE')
  test(label+'/pristine after mutation','pure model result isolation',lambda:eq((v,cat,project(v)),(before,beforecat,pristine)))
  result=bind(parent);result['operand_role'].clear();result['references'].clear();test(label+'/binding result isolation','pure returned binding isolation',lambda:eq(bind(parent),v['binding']))
 prior=read(R/'reference/res-null/actual-receipt.json');marker={'source':'saved declaration input; not an authenticated returned basis'};rr=a.declaration_rows(prior,cat,marker)
 test('both mandatory declaration rows','pure mandatory-row comparison',lambda:a.validate_declaration_rows(prior,cat,marker,rr))
 for name,path,value in [('missing-context',(),None),('context-order',(),None),('runtime', (0,'runtime_arrival'),True),('zero-multiplicity',(1,'multiplicity'),0),('known',(0,'classification'),'KNOWN'),('admission',(1,'actual_admission'),True),('false-comparison-claim',(0,'comparison_outcome'),False),('completion',(1,'decrement_completion'),True)]:
  bad=rr[:1] if name=='missing-context' else rr[::-1] if name=='context-order' else mutate(rr,path,value)
  test(name,'pure mandatory-row comparison; no authenticated basis',lambda bad=bad:a.validate_declaration_rows(prior,cat,marker,bad),'EXIT-DECREF-MANDATORY-ROW-COMPARISON')
 changed=a.declaration_rows(prior,cat,marker);changed[0]['declaration']['steps'].clear();changed[1]['instance_anchor'].clear()
 test('actual returned rows nested mutation','pure mandatory-row output comparison',lambda:a.validate_declaration_rows(prior,cat,marker,changed),'EXIT-DECREF-MANDATORY-ROW-COMPARISON')
 test('pristine rows after mutation','pure mandatory-row expectation isolation',lambda:eq(a.declaration_rows(prior,cat,marker),rr))
 changed=c.exit_decref_catalogue(res,files);changed['source']['operation'].clear();changed['res_null_catalogue'].clear()
 test('catalogue expectation isolation','pure source-catalogue isolation',lambda:eq(c.exit_decref_catalogue(res,files),cat))
 save(O/'RESULT.json',{'status':'PASS','rows':len(rows),'counts':{s:sum(r['status']==s for r in rows) for s in ('PASS','REJECTED','FAIL')},'seconds':time.monotonic()-start,'finished':now(),'public_calls':0,'authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'candidate_changed':False})
if __name__=='__main__':
 try:main()
 except BaseException as e:save(O/'FAILURE.json',{'type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),'recorded_rows':len(rows)});raise
