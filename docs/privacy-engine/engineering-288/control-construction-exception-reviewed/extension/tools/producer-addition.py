# Additive construction-expression exceptional continuation; inherited functions unchanged.
def control_construction_source(launcher,entry,control,bare,callback,stored,token,handle,state):
 validate_control_exception(launcher,entry,bare,callback,stored,token,handle,state,control)
 tree,loc=_client_locate(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 protected=run.body[2].body[0].body[-1];guard,client,post=protected.body;statement=guard.body[0];call=statement.value;construction=call.args[0];pop=protected.finalbody[0]
 need(isinstance(protected,ast.Try) and not protected.handlers and not protected.orelse and len(protected.finalbody)==1,'CONSTRUCTION-PROTECTED-TRY')
 need(ast.unparse(guard.test)=='control is not None' and ast.unparse(call)=='control(_Control(token))' and isinstance(construction,ast.Call) and ast.unparse(construction.func)=='_Control' and not construction.keywords,'CONSTRUCTION-EXPRESSION')
 need(isinstance(client,ast.Try) and client.lineno>statement.end_lineno and ast.unparse(client.body[0])=='client(Client(token))','CONSTRUCTION-OUTSIDE-CLIENT-HANDLER')
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='_Control');init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
 need([n.arg for n in init.args.args]==['self','token'] and len(init.body)==1 and ast.unparse(init.body[0])=='self.__token = token','CONSTRUCTION-INITIALIZER-SOURCE')
 pin={'bytes':len(entry),'sha256':digest(entry)}
 points=[('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]
 prefix=token['source']['order'][:token['source']['order'].index('control-create')+1]
 need(prefix==['owner-create','token-create','registry-insert','control-guard','control-create'],'CONSTRUCTION-PREFIX-ORDER')
 status_typed_same(token['source']['stages']['control-create'],{**loc(construction),'source':copy.deepcopy(pin)},'CONSTRUCTION-REUSED-ATTEMPT')
 for name,node in points:
  status_typed_same(control['source']['stages'][name],{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'finally-entry' if name=='finally-enter' else 'source-statement'},'CONSTRUCTION-REUSED-REVOCATION:'+name)
 return {'sources':copy.deepcopy(control['source']['sources']),'run':loc(run),'control_guard':loc(guard.test),'guard_expression':ast.unparse(guard.test),'selected_guard_result':True,
  'construction_expression':loc(construction),'constructor_expression':ast.unparse(construction.func),'argument_expression':ast.unparse(construction.args[0]),'initializer_source':loc(init),'initializer_assignment_source':loc(init.body[0]),
  'control_call_not_reached':loc(statement),'client_handler_not_reached':loc(client.handlers[0]),'prefix_order':prefix,
  'order':[n for n,_ in points],'stages':{n:copy.deepcopy(control['source']['stages'][n]) for n,_ in points},
  'evaluation_order':['evaluate control callable expression','evaluate _Control(token) argument expression','invoke control only after argument evaluation returns normally'],
  'selected_frontier':'Exception escapes the selected _Control(token) expression; no concrete failure mechanism or constructor substep is asserted',
  'allocation_progress_established':False,'initializer_entry_established':False,'initializer_assignment_established':False,'completed_control_object_established':False,
  'control_callback_execution_established':False,'client_callback_execution_established':False,'client_handler_applies':False,'owner_failure_guard_applies':False,'new_explicit_cause_assignment':False,
  'pop_key':ast.unparse(pop.value.args[0]),'pop_default':ast.literal_eval(pop.value.args[1]),'pop_return_consumed':False,
  'continuation':'Ordinary exceptional continuation from argument construction enters the enclosing finally. Later cleanup may replace pending propagation. Termination is not exception unwind.',
  'continuity':copy.deepcopy(control['source']['continuity'])}

def compile_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state):
 source=control_construction_source(launcher,entry,control,bare,callback,stored,token,handle,state)
 return {'format':'I164-CONTROL-CONSTRUCTION-STATIC-1','source':source,'token_relation':copy.deepcopy(token),
  'declarations':[{'id':n,'source_origin':copy.deepcopy(source['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in source['order']],
  'guard_branches':{'prefix':'control is not None; selected _Control(token) argument expression raises before control invocation','continuation':'Ordinary continuation enters finally; later stages require preceding normal completion','cleanup_raise':'Separate cleanup exception may supersede pending construction error','termination_or_unobserved':'Stop without inferred unwind, completed removal or outward propagation','callbacks':'Neither selected control nor subsequent client callback executes on this route','constructor_progress':'No allocation, initializer entry, assignment or completed object inferred'},
  'preserved_relations':['control_exception_revocation_correspondence',*control['preserved_relations']],
  'reference_meaning':'Inherited control/client symbols are conditional role names, not completed or observed objects on this branch',
  'limits':['Static constructed scope; runtime construction/finally/removal observations unavailable','Existing cause/context/suppression UNKNOWN','Failure mechanism and constructor substep history unavailable','Full outer cleanup remains unexpanded','No owner.failure condition or history inferred'],
  'runtime_construction_exception_revocation_chain':None,'actual_admission':False}

def validate_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state,submitted):
 status_exact_tree(submitted,'CONSTRUCTION-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_control_construction(launcher,entry,control,bare,callback,stored,token,handle,state),'CONSTRUCTION-SOURCE-CORRESPONDENCE');return True

def control_construction_binding(catalogue,scope):
 status_exact_tree(scope,'CONSTRUCTION-ERROR-SCOPE');refs=token_reference_premises(scope,True)
 return {'role':'selected-control-construction-expression-exception','scope':copy.deepcopy(scope),'occurrence':scope['invocation']+'/control-create/exception','reference':scope['invocation']+'/control-create/error',
  'construction_attempt':{'occurrence':scope['invocation']+'/control-create','source':copy.deepcopy(catalogue['source']['construction_expression']),'argument_token':copy.deepcopy(refs['token']),'registered_owner':copy.deepcopy(refs['owner'])},
  'local_handler_binding':None,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,
  'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}

def control_construction_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'CONSTRUCTION-EXACT-TYPE')
 keys={'scope','references','token_inputs','token_prefix','construction_error','outcomes'}
 need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'CONSTRUCTION-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'CONSTRUCTION-VALIDATED:'+k)
 scope=case['scope'];refs=case['references'];prefix=case['token_prefix'];ti=case['token_inputs'];error=case['construction_error'];source=catalogue['source']
 status_typed_same(refs,token_reference_premises(scope,True),'CONSTRUCTION-REFERENCE-ROLES');status_typed_same(scope,ti['scope'],'CONSTRUCTION-TOKEN-SCOPE');need(ti['control_present'] is True,'CONSTRUCTION-REQUIRES-CONTROL')
 expected=[{'stage':n,'outcome':'raise' if n=='control-create' else 'normal'} for n in source['prefix_order']]
 status_typed_same(ti['outcomes'],expected,'CONSTRUCTION-SELECTED-PREFIX')
 tv={k:copy.deepcopy(v) for k,v in ti.items() if k!='references'}
 status_typed_same(prefix,token_registration_projection(catalogue['token_relation'],ti,tv),'CONSTRUCTION-VALIDATED-TOKEN-PREFIX')
 status_typed_same(refs,prefix['reference_bindings'],'CONSTRUCTION-PREFIX-REFERENCES')
 need(prefix['registration_completed_in_model'] is True and prefix['completion']=='unexpected-raise' and prefix['events'][-1]['stage']=='control-create' and prefix['events'][-1]['outcome']=='raise' and prefix['control_callback_completed_in_model'] is False and prefix['client_callback_completed_in_model'] is False,'CONSTRUCTION-REGISTERED-RAISE-FRONTIER')
 status_typed_same(error,control_construction_binding(catalogue,scope),'CONSTRUCTION-SELECTED-ERROR')
 outcomes=case['outcomes'];need(type(outcomes) is list and bool(outcomes),'CONSTRUCTION-OUTCOMES');events=[];done=set();pending=copy.deepcopy(error);cleanup=None;terminal=None;completion=None
 for i,stage in enumerate(source['order']):
  need(i<len(outcomes),'CONSTRUCTION-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and row['stage']==stage,'CONSTRUCTION-STEP-ORDER');kind=row['outcome'];need(type(kind) is str and kind in ('normal','raise','process-termination','unobserved'),'CONSTRUCTION-STAGE-OUTCOME');terminal=kind
  events.append({'id':scope['invocation']+'/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(source['stages'][stage]),'outcome':kind,'owner':copy.deepcopy(refs['owner']),'token':copy.deepcopy(refs['token']),'pending_error_on_entry':copy.deepcopy(pending),'runtime_frame':None})
  if kind in ('process-termination','unobserved'):completion=kind;break
  if kind=='raise':
   cleanup={'role':'conditional-finally-exception','reference':scope['invocation']+'/'+stage+'/error','scope':copy.deepcopy(scope),'source':copy.deepcopy(source['stages'][stage]),'exact_type':None,'physical_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN'};pending=copy.deepcopy(cleanup);completion='cleanup-exceptional-frontier';break
  done.add(stage)
  if stage=='removal-complete':completion='normal-removal-pending-construction-error'
 need(len(events)==len(outcomes),'CONSTRUCTION-UNREACHED-STEPS');popped='removal-complete' in done;continuity=copy.deepcopy(prefix['selected_slot_before_removal']);removed=True if popped and continuity['continuity']=='explicit constructed premise' else None
 return {'kind':'CONSTRUCTED-CONTROL-CONSTRUCTION-EXCEPTION','scope':copy.deepcopy(scope),'reference_bindings':copy.deepcopy(refs),'reference_meaning':catalogue['reference_meaning'],'validated_token_prefix':copy.deepcopy(prefix),'construction_error':copy.deepcopy(error),'events':events,'completion':completion,
  'construction_expression_raised_in_model':True,'construction_completed_in_model':False,'completed_control_object_reference':None,'allocation_progress':None,'initializer_progress':None,'control_callback_executed_in_model':False,'subsequent_client_execution_in_model':False,'client_handler_entered_in_model':False,'owner_failure_guard_evaluated_in_model':False,'new_explicit_cause_assignment_established_in_model':False,
  'exception_chain_observation':{'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None},'cleanup_error_in_model':cleanup,
  'finally_entry_completed_in_model':'finally-enter' in done,'removal_attempt_entered_in_model':'removal-attempt' in done,'removal_completed_in_model':popped,'selected_slot_before_removal':continuity,'selected_owner_removed_in_model':removed,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','pop_result_observation':None,'revocation_persists':None,
  'last_pending_error_in_model':copy.deepcopy(pending),'outward_error_after_finally_in_model':copy.deepcopy(error) if popped else None,'construction_outward_after_finally_established_in_model':popped,'construction_reaches_launcher_established':False,'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True,
  'prior_failure_storage_history':'UNKNOWN; no selected owner.failure guard here; previously established evidence is retained unchanged','role_relationship':'Separate semantic error roles and invocation-qualified occurrences; no physical equality or inequality inference','run_success_established':False,'runtime_observation':False,'runtime_construction_exception_revocation_chain':None,'runtime_unwind_evidence':'UNAVAILABLE','physical_reference_identity':None,'outer_cleanup_completion':None,'database_cleanup_completion':None,'retained_failure_record_bytes':None,'physical_lock_release_established':False,'exclusive_ownership_established':False,'durability_established':False,'observer_join':None,
  'completion_flags_mean':'Only conditional acknowledged completions; no allocation or initializer substep inferred. Earlier registration and selected construction-expression raise survive later uncertainty. Pending propagation is not observed outward propagation.',
  'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}

def validate_control_construction_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'CONSTRUCTION-SUBMITTED-OUTPUT');status_typed_same(submitted,control_construction_projection(catalogue,case,validated),'CONSTRUCTION-OUTPUT-CORRESPONDENCE');return True
