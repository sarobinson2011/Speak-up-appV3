# Additive Client construction / exact-None continuation. Inherited definitions unchanged.
def client_construction_source(launcher,entry,construction,control,bare,callback,stored,token,handle,state):
 validate_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state,construction)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 protected=run.body[2].body[0].body[-1];control_guard,client_try,post=protected.body;statement=client_try.body[0];call=statement.value;attempt=call.args[0];handler=client_try.handlers[0];guard=handler.body[0];raise_=handler.body[1];pop=protected.finalbody[0]
 need(isinstance(client_try,ast.Try) and len(client_try.body)==len(client_try.handlers)==1 and not client_try.orelse and not client_try.finalbody,'CLIENT-CONSTRUCTION-INNER-TRY')
 need(ast.unparse(call)=='client(Client(token))' and isinstance(attempt,ast.Call) and ast.unparse(attempt.func)=='Client' and len(attempt.args)==1 and not attempt.keywords,'CLIENT-CONSTRUCTION-EXPRESSION')
 need(ast.unparse(handler.type)=='BaseException' and handler.name=='client_error' and len(handler.body)==2,'CLIENT-CONSTRUCTION-HANDLER')
 need(ast.unparse(guard.test)=='owner.failure is not None' and not guard.orelse and isinstance(raise_,ast.Raise) and raise_.exc is None and raise_.cause is None,'CLIENT-CONSTRUCTION-NONE-BARE')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Client');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need([n.arg for n in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token','CLIENT-CONSTRUCTION-INITIALIZER-SOURCE')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 prefix=['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create']
 need(token['source']['order'][:len(prefix)]==prefix,'CLIENT-CONSTRUCTION-PREFIX-ORDER')
 status_typed_same(token['source']['stages']['client-create'],{**loc(attempt),'source':copy.deepcopy(pin)},'CLIENT-CONSTRUCTION-ATTEMPT-ORIGIN')
 points=[('callback-handler-enter',handler),('callback-none-guard',guard.test),('callback-bare-rethrow',raise_),('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 for name,node in points:
  region='handler-entry' if name=='callback-handler-enter' else ('finally-entry' if name=='finally-enter' else 'source-statement')
  status_typed_same(bare['source']['stages'][name],{**loc(node),'source':copy.deepcopy(pin),'semantic_region':region},'CLIENT-CONSTRUCTION-REUSED-STAGE:'+name)
 return {'sources':copy.deepcopy(construction['source']['sources']),'run':loc(run),'construction_expression':loc(attempt),'constructor_expression':ast.unparse(attempt.func),'argument_expression':ast.unparse(attempt.args[0]),'initializer_source':loc(init),'initializer_assignment_source':loc(init.body[0]),
  'client_call_not_reached':loc(statement),'handler':loc(handler),'exception_binding':handler.name,'catch_family':ast.unparse(handler.type),'guard':loc(guard.test),'guard_expression':ast.unparse(guard.test),'selected_guard_result':False,'selected_slot_expression':'owner.failure','selected_slot_value':None,'selected_slot_exact_type':'NoneType','raise':loc(raise_),'raise_syntax':ast.unparse(raise_),'bare_raise_has_explicit_cause_clause':False,
  'prefix_order_control_present':prefix,'prefix_order_control_absent':[n for n in prefix if n not in ('control-create','control-callback')],'control_guard':loc(control_guard.test),'control_guard_expression':ast.unparse(control_guard.test),
  'order':[n for n,_ in points],'stages':{n:copy.deepcopy(bare['source']['stages'][n]) for n,_ in points},'guard_slot_premise':bare['source']['guard_slot_premise'],'reused_revocation':copy.deepcopy(bare['source']['reused_revocation']),
  'evaluation_order':['Earlier selected control path completes normally or is absent','Evaluate client callable expression','Evaluate Client(token) argument expression inside the client try','Invoke client only if argument construction returns normally'],
  'selected_frontier':'Exception escapes selected Client(token) expression; ordinary continuation binds it as client_error. No allocation/initializer substep or failure mechanism inferred.',
  'allocation_progress_established':False,'initializer_entry_established':False,'initializer_assignment_established':False,'completed_client_object_established':False,'client_callback_execution_established':False,'new_explicit_cause_assignment':False,
  'error_continuity':'The construction error is the selected caught error; bare raise reraises that active error under the exact-None guard. Handler evaluation or cleanup can replace pending propagation. Existing cause/context/suppression remain UNKNOWN.',
  'stage_names':'Reused callback-handler/guard/rethrow stage names identify the existing source handler; they do not assert client-callback invocation.',
  'continuity':copy.deepcopy(construction['source']['continuity'])}

def compile_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state):
 source=client_construction_source(launcher,entry,construction,control,bare,callback,stored,token,handle,state)
 return {'format':'I164-CLIENT-CONSTRUCTION-NONE-STATIC-1','source':source,'token_relation':copy.deepcopy(token),
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'prefix_control_absent':'control is None; selected client construction raises','prefix_control_present':'control is not None; its construction and callback completed normally before selected client construction raises','slot':'Selected same-owner failure slot is exactly None under explicit guard-slot continuity; no historical absence inferred','bare_raise':'Reraise the active construction exception, adding no explicit cause','handler_evaluation':'A raise in handler/guard/rethrow evaluation skips remaining handler stages and conditionally proceeds to finally with replacement error','cleanup':'Later finally/pop raise can replace propagation, without completed removal','termination_or_unobserved':'No inferred Python unwind, continuation, cleanup or outward propagation','client':'No completed Client or selected client-callback execution established'},
  'preserved_relations':['control_construction_revocation_correspondence',*construction['preserved_relations']],
  'reference_meaning':'Inherited client symbol denotes a conditional role, not a completed or observed Client; earlier control progress is preserved separately when established in the selected prefix',
  'limits':['Static constructed scope; runtime construction/handler/rethrow/removal chain unavailable','Exact None is a guard-slot premise, not proof of no earlier storage','Existing cause/context/suppression UNKNOWN','No concrete failure mechanism or allocation/initializer progress','Non-None constructor branch and full outer cleanup remain outside this slice'],
  'runtime_client_construction_revocation_chain':None,'actual_admission':False}

def validate_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CLIENT-CONSTRUCTION-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_client_construction(launcher,entry,construction,control,bare,callback,stored,token,handle,state),'CLIENT-CONSTRUCTION-SOURCE-CORRESPONDENCE');return True

def client_construction_binding(catalogue,scope,control_present):
 status_exact_tree(scope,'CLIENT-CONSTRUCTION-ERROR-SCOPE');refs=token_reference_premises(scope,control_present)
 return {'role':'selected-client-construction-expression-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/client-create/exception','reference':scope['invocation']+'/client-create/error',
  'construction_attempt':{'occurrence':scope['invocation']+'/client-create','source':copy.deepcopy(catalogue['source']['construction_expression']),'argument_token':copy.deepcopy(refs['token']),'registered_owner':copy.deepcopy(refs['owner'])},
  'handler_binding_name_from_source':catalogue['source']['exception_binding'],'handler_binding_established_by_this_role':False,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}

def client_construction_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CLIENT-CONSTRUCTION-EXACT-TYPE')
 keys={'scope','references','token_inputs','token_prefix','none_guard_binding','construction_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CLIENT-CONSTRUCTION-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CLIENT-CONSTRUCTION-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];ti=case['token_inputs'];binding=case['none_guard_binding'];error=case['construction_error'];source=catalogue['source']
 need(type(ti['control_present']) is bool and ti['owner_failure_none'] is True,'CLIENT-CONSTRUCTION-SELECTED-PREMISES');control=ti['control_present']
 status_typed_same(refs,token_reference_premises(scope,control),'CLIENT-CONSTRUCTION-REFERENCE-ROLES');status_typed_same(scope,ti['scope'],'CLIENT-CONSTRUCTION-TOKEN-SCOPE')
 order=source['prefix_order_control_present' if control else 'prefix_order_control_absent'];expected=[{'stage':n,'outcome':'raise' if n=='client-create' else 'normal'} for n in order]
 status_typed_same(ti['outcomes'],expected,'CLIENT-CONSTRUCTION-SELECTED-PREFIX');tv={k:copy.deepcopy(v) for k,v in ti.items() if k!='references'}
 status_typed_same(prefix,token_registration_projection(catalogue['token_relation'],ti,tv),'CLIENT-CONSTRUCTION-VALIDATED-TOKEN-PREFIX');status_typed_same(refs,prefix['reference_bindings'],'CLIENT-CONSTRUCTION-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['events'][-1]['stage']=='client-create' and prefix['events'][-1]['outcome']=='raise' and prefix['client_callback_completed_in_model'] is False,'CLIENT-CONSTRUCTION-REGISTERED-RAISE-FRONTIER')
 need(prefix['control_callback_completed_in_model'] is (True if control else None),'CLIENT-CONSTRUCTION-EARLIER-CONTROL')
 status_typed_same(error,client_construction_binding(catalogue,scope,control),'CLIENT-CONSTRUCTION-SELECTED-ERROR')
 expected_guard={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':source['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(source['guard']),'source':copy.deepcopy(source['sources']['entry']),'premise':source['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 status_typed_same(binding,expected_guard,'CLIENT-CONSTRUCTION-NONE-GUARD')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CLIENT-CONSTRUCTION-OUTCOMES');order=source['order'];cursor=0;index=0;events=[];done=set();pending=copy.deepcopy(error);evaluation=None;cleanup=None;completion=None;terminal=None
 while cursor<len(order):
  stage=order[cursor];need(index<len(outcomes),'CLIENT-CONSTRUCTION-MISSING-STEP:'+stage);row=outcomes[index];index+=1
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CLIENT-CONSTRUCTION-STEP-ORDER');kind=row['outcome']
  allowed=('reraised-construction','raise','process-termination','unobserved') if stage=='callback-bare-rethrow' else ('normal','raise','process-termination','unobserved')
  need(type(kind) is str and kind in allowed,'CLIENT-CONSTRUCTION-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if cursor<3:
   if kind=='raise':
    evaluation={'role':'conditional-handler-evaluation-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'};pending=copy.deepcopy(evaluation);cursor=3;continue
   done.add(stage)
   if stage=='callback-bare-rethrow':pending=copy.deepcopy(error)
  elif kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  else:done.add(stage)
  cursor+=1
  if stage=='removal-complete':completion='normal-removal-pending-construction-error' if 'callback-bare-rethrow' in done else 'normal-removal-pending-evaluation-error'
 need(index==len(outcomes),'CLIENT-CONSTRUCTION-UNREACHED-STEPS');popped='removal-complete' in done;reraised='callback-bare-rethrow' in done;caught='callback-handler-enter' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'reference_meaning':catalogue['reference_meaning'],'validated_token_prefix':copy.deepcopy(prefix),'construction_error':copy.deepcopy(error),'none_guard_binding':copy.deepcopy(binding),'events':events,'completion':completion,
  'construction_expression_raised_in_model':True,'construction_completed_in_model':False,'completed_client_object_reference':None,'allocation_progress':None,'initializer_progress':None,'client_callback_executed_in_model':False,
  'earlier_control_present':control,'earlier_control_construction_completed_in_model':True if control else None,'earlier_control_callback_completed_in_model':prefix['control_callback_completed_in_model'],
  'handler_entry_completed_in_model':caught,'caught_error_in_model':copy.deepcopy(error) if caught else None,'caught_name_in_model':source['exception_binding'] if caught else None,'none_guard_completed_in_model':'callback-none-guard' in done,'bare_rethrow_effect_established_in_model':reraised,'reraised_error_in_model':copy.deepcopy(error) if reraised else None,
  'bare_raise_semantics':{'adds_explicit_cause':False,'preserves_active_exception':True,'establishes_absent_existing_cause_or_context':False},'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None},'new_explicit_cause_assignment_established_in_model':False,'handler_evaluation_error_in_model':evaluation,'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(pending) if popped else None,'construction_outward_after_finally_established_in_model':popped and reraised,'construction_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; the exact None guard does not erase earlier established storage or evidence','role_relationship':'Construction and caught-error roles share the selected error; later evaluation/cleanup roles do not prove physical inequality','run_success_established':False,'runtime_observation':False,'runtime_client_construction_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Conditional acknowledged model progress only. Earlier registration, construction-error and selected control completion survive later uncertainty. No allocation/initializer progress or guaranteed outward propagation.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_client_construction_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CLIENT-CONSTRUCTION-SUBMITTED-OUTPUT');status_typed_same(submitted,client_construction_projection(catalogue,case,validated),'CLIENT-CONSTRUCTION-OUTPUT-CORRESPONDENCE');return True
