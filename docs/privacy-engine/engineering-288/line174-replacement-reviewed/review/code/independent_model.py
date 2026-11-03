"""Source-derived review expectations; no imports from Engineering's tests."""
import ast,copy
D=copy.deepcopy
def source_plan(raw):
 t=ast.parse(raw);fn=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='_session')
 call=next(x for x in ast.walk(fn) if isinstance(x,ast.Call) and x.lineno==174 and isinstance(x.func,ast.Name) and x.func.id=='write_new')
 region=next(x for x in ast.walk(fn) if isinstance(x,ast.Try) and x.lineno==174)
 assert len(call.args)==2 and not call.keywords and ast.unparse(call.args[1])=='details'
 assert ast.unparse(call.args[0])=="dest / 'evidence' / ('failure-' + str(os.getpid()) + '-' + str(len(list((dest / 'evidence').iterdir()))) + '.json')"
 result=[]
 def push(n,operation,dependencies=(),**facts):
  result.append({'site':[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__],'expression':ast.get_source_segment(raw.decode(),n),'operation':operation,'dependencies':list(dependencies),**facts});return len(result)-1
 def walk(n):
  if isinstance(n,ast.Name):return push(n,'name lookup',name=n.id)
  if isinstance(n,ast.Constant):assert type(n.value) is str;return push(n,'literal',literal=n.value)
  if isinstance(n,ast.Attribute):return push(n,'attribute lookup',[walk(n.value)],attribute=n.attr)
  if isinstance(n,ast.BinOp):
   left=walk(n.left);right=walk(n.right);return push(n,'binary operation',[left,right],operator=type(n.op).__name__)
  if isinstance(n,ast.Call):
   callable_index=walk(n.func);arguments=[walk(a) for a in n.args];a=push(n,'nested call attempt',[callable_index,*arguments]);return push(n,'nested normal return',[a])
  raise AssertionError(type(n))
 push(region,'explicit continuation into selected protecting try');c=walk(call.func);a=[walk(x) for x in call.args];push(call,'write_new call attempt; body excluded',[c,*a])
 assert [x['expression'] for x in result if x['operation']=='nested call attempt']==['os.getpid()','str(os.getpid())',"(dest/'evidence').iterdir()","list((dest/'evidence').iterdir())","len(list((dest/'evidence').iterdir()))","str(len(list((dest/'evidence').iterdir())))"]
 return result
def check_source(cat,plan):
 steps=cat['source']['steps'];assert len(steps)==len(plan)
 for i,(actual,want) in enumerate(zip(steps,plan)):
  assert actual['source']['site']==want['site'] and actual['source']['expression']==want['expression']
  assert actual['operation']==want['operation'] and actual['inputs']==[steps[j]['id'] for j in want['dependencies']]
  for k in ('name','literal','attribute','operator'):
   if k in want:assert actual[k]==want[k]
  normal='attempted' if 'call attempt' in want['operation'] else 'normal';assert actual['normal_outcome']==normal
 assert cat['source']['order']==[x['id'] for x in steps] and cat['source']['callee_parameters']==['p','x']
 assert len({x['id'] for x in steps})==len(steps) and cat['runtime_chain'] is None and cat['actual_admission'] is False
 return True
def build(coverage,cat,parent,session,frontier=None,continuity='explicit conditional premise'):
 p=D(parent['output']);anchor=D(parent['anchor']);binding=coverage.write_call_binding(cat,p,anchor,session,continuity)
 oo=[]
 for step in cat['source']['steps']:
  status=frontier[1] if frontier and step['id']==frontier[0] else step['normal_outcome'];oo.append({'stage':step['id'],'outcome':status})
  if frontier and step['id']==frontier[0]:break
 v={'scope':D(p['scope']),'anchor':anchor,'parent_result':p,'session_binding':D(session),'binding':binding,'outcomes':oo}
 case={'kind':'CONSTRUCTED-WRITE-CALL-REPLACEMENT','context':parent['context'],'anchor':D(anchor),'invocation':parent['invocation'],'parent_case':D(parent),'parent_output':D(p),'session_binding':D(session),'binding':D(binding),'outcomes':D(oo),'projection':v}
 case['output']=coverage.write_call_projection(cat,v,v);return case
def oracle(cat,case,out):
 p=case['parent_output'];oo=case['outcomes'];steps=cat['source']['steps'];complete=len(oo)==len(steps) and oo[-1]['outcome']=='attempted';last=oo[-1]['outcome'];scope=p['scope']
 assert out['scope']==scope and out['instance_anchor']==case['anchor'] and out['binding']==case['binding']
 assert out['call_attempt_established'] is complete and out['completion']==('write_new-call-attempt' if complete else last+'-frontier')
 assert len(out['events'])==len(oo)
 for i,(event,ob) in enumerate(zip(out['events'],oo)):
  assert event['stage']==ob['stage'] and event['outcome']==ob['outcome'] and event['source']==steps[i]['source']
  assert event['id']==scope['invocation']+'/line174/'+ob['stage'] and event['scope']==scope and event['runtime_frame'] is None
  for k in ('owner','token'):assert event[k]==case['binding']['references'][k]
 assert out['terminal_python_exception_in_model'] is (None if last in ('unobserved','process-termination') else True)
 assert out['original_error_pending_in_outer_handler']==p['original_error_pending_in_outer_handler']
 replacement=out['replacement_error_in_model']
 if last in ('raise','catchable-interruption'):
  assert replacement['role']=='conditional-line174-replacement' and replacement['scope']==scope and replacement['origin']==steps[len(oo)-1]['source']
  assert replacement['reference']==out['events'][-1]['id']+'/error' and replacement['kind']==last
  assert replacement['exact_type'] is None and replacement['exact_value'] is None and replacement['runtime_observation'] is False
  assert all(replacement[k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression'))
  assert out['last_pending_error_in_model']==replacement
 else:assert replacement is None and out['last_pending_error_in_model']==p['last_pending_error_in_model']
 for k in ('retained_cleanup_error_evidence','last_acknowledged_inner_caught_error','last_acknowledged_active_caught_error_in_model','earlier_control_completed_in_model','selected_owner_continuity','failure_origin_region','close_normal_return_completed_in_model','close_itself_failed_established_in_model','managed_close_relation','cleanup_list_state','details_after_predecessor_acknowledged_steps','known_false_flags_preserved','dynamic_details_origins_preserved'):assert out[k]==p[k],k
 values=out['values'];expected=[]
 for step,ob in zip(steps,oo):
  if ob['outcome']!=step['normal_outcome']:break
  if step['operation'] in ('explicit continuation into selected protecting try','nested call attempt','write_new call attempt; body excluded'):continue
  expected.append(step['id']);v=values[step['id']];assert v['source']==step['source'] and v['runtime_identity'] is None and v['concrete_value']==step.get('literal')
  assert v['symbol']==scope['invocation']+'/line174/'+step['id']+'/value'
  for dep,link in zip(step['inputs'],v['inputs']):
   assert link['occurrence']==scope['invocation']+'/line174/'+dep
   assert link['value']==(values[dep]['symbol'] if dep in values else None)
  role={'dest':'destination','details':'details_role','write_new':'callable'}.get(step.get('name'))
  assert v['bound_role']==(case['binding'][role] if role else None)
 assert set(values)==set(expected)
 if complete:
  assert out['call_arguments']['p']==values[cat['source']['arguments'][0]] and out['call_arguments']['x']==case['binding']['details_role']
 else:assert out['call_arguments'] is None
 for k in ('pid_value','directory_count_value','filename_value','exact_path_value','runtime_chain','observer_join','physical_reference_identity'):assert out[k] is None
 for k in ('write_new_body_entry_established','write_new_return_established','file_open_established','file_write_established','file_flush_established','file_fsync_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission','runtime_observation'):assert out[k] is False,k
 return True
