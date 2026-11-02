
# Bounded post-line172 continuation. The entire reviewed producer above is unchanged.
def cleanup_loop_source(launcher,entry,manager,report,cleanup):
 for raw in (launcher,entry,manager):need(type(raw) is bytes,'LOOP-SOURCE-BYTES')
 for value in (report,cleanup):status_exact_tree(value,'LOOP-PARENT-CATALOGUES')
 validate_error_report(launcher,entry,manager,cleanup,report)
 tree,loc=_client_locate(launcher);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 outer=fn.body[-1].body[-1].handlers[0];loop=outer.body[1];guard=loop.body[0];protected=guard.body[0];handler=protected.handlers[0]
 need(outer.name=='e' and isinstance(loop,ast.For) and not loop.orelse and len(loop.body)==1 and len(guard.body)==1 and not guard.orelse,'LOOP-EXACT-BODY')
 need(isinstance(loop.iter,ast.List) and len(loop.iter.elts)==2 and ast.unparse(loop.target)=='(name, obj)','LOOP-FINITE-INPUTS')
 pairs=[[p.elts[0].value,p.elts[1].id] for p in loop.iter.elts];status_typed_same(pairs,[['raw','raw'],['managed','managed']],'LOOP-ORDERED-INPUTS')
 need(ast.unparse(guard.test)=='obj is not None' and handler.name=='close_error' and len(handler.body)==1 and not protected.finalbody and not protected.orelse,'LOOP-HANDLER-TAIL')
 need(not any(isinstance(n,(ast.Break,ast.Continue,ast.Return,ast.Yield,ast.YieldFrom)) for n in ast.walk(handler)),'LOOP-NORMAL-DEPARTURE-SHAPE')
 pin=report['source']['sources']['launcher'];status_typed_same({**loc(handler),'source':pin},report['source']['handler'],'LOOP-EXACT-HANDLER')
 need(report['source']['order'][-1]=='report-append-complete','LOOP-PREDECESSOR-FRONTIER')
 status_typed_same([[x['name'],x['slot']] for x in cleanup['source']['ordered_inputs']],pairs,'LOOP-PREDECESSOR-INPUTS')
 following=outer.body[2];need(isinstance(following,ast.Try) and following.lineno==174,'LOOP-STOP-BEFORE-WRITE')
 # These are semantic acknowledgments, not a claimed sequence of hidden opcodes.
 # Name clearing and handled-error restoration form one normal departure boundary.
 points=[('inner-handler-departure-attempt',handler),('inner-handler-exit-complete',handler),('selected-loop-body-complete',guard),('final-iterator-advance-attempt',loop),('ordinary-iterator-exhaustion',loop.iter),('cleanup-loop-complete',loop)]
 return {'sources':copy.deepcopy(report['source']['sources']),'handler':copy.deepcopy(report['source']['handler']),'outer_caught_name':outer.name,'caught_name':handler.name,
  'loop':{**loc(loop),'source':copy.deepcopy(pin)},'ordered_inputs':copy.deepcopy(cleanup['source']['ordered_inputs']),'entry_count':len(pairs),'selected_index':len(pairs)-1,'next_index':len(pairs),
  'guard_expression':ast.unparse(guard.test),'required_guard_results':{'raw':False,'managed':True},'target_names':[n.id for n in loop.target.elts],
  'order':[n for n,_ in points],'stages':{n:{**loc(node),'source':copy.deepcopy(pin),'semantic_region':'post-error-report-loop-continuation'} for n,node in points},
  'normal_outcomes':{n:('exhausted' if n=='ordinary-iterator-exhaustion' else 'normal') for n,_ in points},
  'selection_prefix':[{ 'stage':n,'source':copy.deepcopy(s)} for n in cleanup['source']['order'] for s in [cleanup['source']['stages'][n]] if s['semantic_region']=='loop-selection'],
  'language_contract':{'reference':'https://docs.python.org/3.12/reference/compound_stmts.html','sections':['8.3 for','8.4.1 except'],
   'scope':'Retained CPython 3.12.14 conditional semantics; family language rules, not runtime qualification or exact opcode observation',
   'rules':['Normal handler departure clears its as-target and restores the previously handled exception; no assertion of physical destruction or internal substep order',
    'A for iterable expression is evaluated once; yielded entries bind targets in order; ordinary exhaustion ends the loop without a new propagating error',
    'For target names remain bound after loop completion; caught-name clearing is a different lifetime rule'],
   'premises':'Explicit continuity of the exact source-created two-entry list/iterator and selected locals, references, exception and details/list roles; no hostile replacement, extra entry or mutation inferred absent'},
  'continuity':'explicit conditional selected-owner, invocation, exception, local, handler, details/list and finite-loop iterator continuity; not observed identity or exclusivity',
  'stop_before':{**loc(following.body[0].value),'source':copy.deepcopy(pin)}}

def compile_cleanup_loop(launcher,entry,manager,report,cleanup):
 s=cleanup_loop_source(launcher,entry,manager,report,cleanup)
 return {'format':'I164-CLEANUP-LOOP-STATIC-1','source':s,'parent_catalogue_identity':{'sha256':digest((json.dumps(report,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode())},
  'declarations':[{'id':n,'source_origin':copy.deepcopy(s['stages'][n]),'classification':'UNKNOWN','multiplicity':None,'ordinal':None} for n in s['order']],
  'guard_branches':{'parent':'Actual validated completed selected line172 append, bound error, original constructor pending; no replacement',
   'continuity':'Explicit conditional premise or UNESTABLISHED; append completion alone establishes no continuation',
   'prefixes':['control absent','earlier control construction and callback completed normally'],'origins':['protected-close','protected-append'],
   'normal':'Explicit stage outcomes through ordinary exhaustion of exact two-entry loop; original constructor remains pending in outer handler',
   'nonnormal':'First raise, catchable interruption, process termination or unobserved frontier stops; no inferred later completion',
   'name_lifetime':'Cleared local caught-name is separate from retained error evidence and last acknowledged caught error',
   'partial_effects':'Carry acknowledged reporting/close facts and UNKNOWN earlier append effects unchanged'},
  'preserved_relations':['cleanup_error_report_correspondence',*report['preserved_relations']],'runtime_loop_chain':None,'actual_admission':False}

def validate_cleanup_loop(launcher,entry,manager,report,cleanup,submitted):
 status_exact_tree(submitted,'LOOP-SUBMITTED-CATALOGUE');status_typed_same(submitted,compile_cleanup_loop(launcher,entry,manager,report,cleanup),'LOOP-SOURCE-CORRESPONDENCE');return True

def cleanup_loop_binding(catalogue,parent,anchor,continuity):
 for v in (catalogue,parent,anchor,continuity):status_exact_tree(v,'LOOP-BINDING-TYPES')
 need(type(continuity) is str and continuity in ('explicit conditional premise','UNESTABLISHED'),'LOOP-CONTINUITY-DOMAIN')
 s=catalogue['source'];need(parent['kind']=='CONSTRUCTED-CLEANUP-ERROR-REPORT' and parent['completion']=='selected-error-item-append' and parent['report_append_completed_in_model'] is True and parent['caught_binding_completed_in_model'] is True,'LOOP-COMPLETED-PREDECESSOR')
 need(parent['terminal_python_exception_in_model'] is True and parent['replacement_error_in_model'] is None and parent['handler_exit_established'] is False and parent['loop_completion_established'] is False,'LOOP-PARENT-FRONTIER')
 status_typed_same(parent['instance_anchor'],anchor,'LOOP-INSTANCE');b=parent['binding'];scope=parent['scope'];pre=parent['validated_parent'];pb=pre['binding']
 status_typed_same(parent['original_error_pending_in_outer_handler'],parent['earlier_constructor_exception'],'LOOP-ORIGINAL-PENDING')
 status_typed_same(parent['last_pending_error_in_model'],parent['selected_cleanup_error'],'LOOP-CAUGHT-PENDING-ROLE')
 status_typed_same(parent['caught_error_in_model'],parent['selected_cleanup_error'],'LOOP-CAUGHT-ERROR');status_typed_same(b['handler_origin'],s['handler'],'LOOP-HANDLER')
 need(parent['caught_name_in_model']==s['caught_name'] and b['selected_name']=='managed' and pb['ordered_values'][0]=={'name':'raw','value':None,'exact_type':'NoneType'},'LOOP-SELECTION')
 status_typed_same(pb['ordered_values'][1]['value'],b['selected_object'],'LOOP-SELECTED-OBJECT');need(pb['guard']['result'] is True and pb['guard']['right'] is None,'LOOP-SELECTED-GUARD')
 prefix=s['selection_prefix'];need(len(pre['events'])>len(prefix),'LOOP-SELECTION-EVENTS')
 for expected,event in zip(prefix,pre['events']):
  need(event['stage']==expected['stage'] and event['outcome']=='normal','LOOP-SELECTION-PREFIX');status_typed_same(event['source'],expected['source'],'LOOP-SELECTION-ORIGIN');status_typed_same(event['scope'],scope,'LOOP-SELECTION-SCOPE')
 event=parent['events'][-1];need(event['stage']=='report-append-complete' and event['outcome']=='normal' and event['id']==scope['invocation']+'/error-report/report-append-complete','LOOP-APPEND-OCCURRENCE')
 status_typed_same(event['scope'],scope,'LOOP-APPEND-SCOPE');status_typed_same(event['owner'],b['references']['owner'],'LOOP-APPEND-OWNER');status_typed_same(event['token'],b['references']['token'],'LOOP-APPEND-TOKEN')
 status_typed_same(parent['cleanup_list_state']['acknowledged_append']['target'],b['cleanup_list'],'LOOP-APPEND-LIST')
 return {'scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(anchor),'append_occurrence':copy.deepcopy(event),'handler_origin':copy.deepcopy(s['handler']),
  'original_constructor_error':copy.deepcopy(parent['earlier_constructor_exception']),'selected_cleanup_error':copy.deepcopy(parent['selected_cleanup_error']),'protected_failure_occurrence':copy.deepcopy(parent['selected_failure_occurrence']),
  'references':copy.deepcopy(b['references']),'selected_name':b['selected_name'],'selected_object':copy.deepcopy(b['selected_object']),'details_role':copy.deepcopy(b['details_role']),'cleanup_list':copy.deepcopy(b['cleanup_list']),
  'loop':{'ordered_values':copy.deepcopy(pb['ordered_values']),'entry_count':s['entry_count'],'selected_index':s['selected_index'],'next_index':s['next_index'],'raw_guard':False,'raw_body_skipped':True,'managed_guard':True,'selected_is_last':True,'iterator_role':scope['invocation']+'/launcher/cleanup-loop/iterator','source':copy.deepcopy(s['loop'])},
  'continuity':continuity,'premise':s['continuity'],'physical_identity_observed':None,'runtime_continuation_observed':None}

def cleanup_loop_projection(catalogue,case,validated):
 for v in (catalogue,case,validated):status_exact_tree(v,'LOOP-EXACT-TYPE')
 keys={'scope','anchor','parent_result','binding','outcomes'};need(type(case) is dict and type(validated) is dict and set(case)==set(validated)==keys,'LOOP-CASE-FIELDS')
 for k in keys:status_typed_same(case[k],validated[k],'LOOP-VALIDATED:'+k)
 s=catalogue['source'];p=case['parent_result'];scope=case['scope'];binding=case['binding'];outcomes=case['outcomes']
 status_typed_same(scope,p['scope'],'LOOP-PARENT-SCOPE');status_typed_same(binding,cleanup_loop_binding(catalogue,p,case['anchor'],binding['continuity']),'LOOP-EXPECTED-BINDING')
 need(type(outcomes) is list and bool(outcomes),'LOOP-EXPLICIT-CONTINUATION')
 if binding['continuity']=='UNESTABLISHED':status_typed_same(outcomes,[{'stage':s['order'][0],'outcome':'unobserved'}],'LOOP-UNKNOWN-CONTINUITY')
 events=[];done=set();replacement=None;terminal=None
 for i,stage in enumerate(s['order']):
  need(i<len(outcomes),'LOOP-MISSING-STEP:'+stage);row=outcomes[i]
  need(type(row) is dict and set(row)=={'stage','outcome'} and type(row['stage']) is str and row['stage']==stage,'LOOP-STEP-ORDER')
  terminal=row['outcome'];normal=s['normal_outcomes'][stage];need(type(terminal) is str and terminal in (normal,'raise','catchable-interruption','process-termination','unobserved'),'LOOP-OUTCOME')
  origin=s['stages'][stage];events.append({'id':scope['invocation']+'/cleanup-loop/'+stage,'scope':copy.deepcopy(scope),'stage':stage,'source':copy.deepcopy(origin),'outcome':terminal,'append_occurrence':binding['append_occurrence']['id'],'owner':copy.deepcopy(binding['references']['owner']),'token':copy.deepcopy(binding['references']['token']),'runtime_frame':None})
  if terminal!=normal:
   if terminal in ('raise','catchable-interruption'):replacement={'role':'conditional-loop-continuation-replacement','reference':scope['invocation']+'/cleanup-loop/'+stage+'/error','scope':copy.deepcopy(scope),'origin':copy.deepcopy(origin),'mode':terminal,'exact_type':None,'exact_value_bytes':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_observation':False}
   break
  done.add(stage)
 need(len(outcomes)==len(events),'LOOP-UNREACHED-STEPS')
 exited='inner-handler-exit-complete' in done;complete='cleanup-loop-complete' in done;original=binding['original_constructor_error'];selected=binding['selected_cleanup_error'];uncertain=terminal in ('process-termination','unobserved')
 return {'kind':'CONSTRUCTED-CLEANUP-LOOP','scope':copy.deepcopy(scope),'instance_anchor':copy.deepcopy(case['anchor']),'validated_parent':copy.deepcopy(p),'binding':copy.deepcopy(binding),'events':events,
  'completion':'normal-cleanup-loop-exhaustion' if complete else {'raise':'replacement-exception-frontier','catchable-interruption':'interruption-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[terminal],
  'handler_exit_established':exited,'selected_body_complete':'selected-loop-body-complete' in done,'final_advance_attempted':any(e['stage']=='final-iterator-advance-attempt' for e in events),'ordinary_exhaustion_established':'ordinary-iterator-exhaustion' in done,'loop_completion_established':complete,
  'caught_name_lifetime':{'name':s['caught_name'],'last_acknowledged_binding':'CLEARED' if exited else 'BOUND selected cleanup error','normal_departure_clears_name':True,'state_at_nonnormal_frontier':'UNOBSERVED' if not complete else 'CONDITIONAL normal completion','physical_destruction_established':False},
  'retained_cleanup_error_evidence':copy.deepcopy(selected),'last_acknowledged_inner_caught_error':copy.deepcopy(selected),'last_acknowledged_active_caught_error_in_model':copy.deepcopy(original if exited else selected),'active_error_at_terminal_observed':None,
  'original_error_pending_in_outer_handler':copy.deepcopy(original),'last_pending_error_in_model':copy.deepcopy(replacement or (original if exited else selected)),'replacement_error_in_model':replacement,
  'terminal_python_exception_in_model':None if uncertain else True,'ordinary_exhaustion_is_new_propagating_error':False,'normal_overall_return_established':False,
  'loop_target_bindings_retained':{'name':binding['selected_name'],'obj':copy.deepcopy(binding['selected_object']),'conditional_continuity':binding['continuity']},'additional_body_execution_established':False,
  'earlier_control_completed_in_model':p['earlier_control_completed_in_model'],'selected_owner_continuity':copy.deepcopy(p['selected_owner_continuity']),'failure_origin_region':p['failure_origin_region'],
  'close_normal_return_completed_in_model':p['close_normal_return_completed_in_model'],'close_itself_failed_established_in_model':p['close_itself_failed_established_in_model'],'managed_close_relation':copy.deepcopy(p['managed_close_relation']),
  'report_append_completed_in_model':True,'cleanup_list_state':copy.deepcopy(p['cleanup_list_state']),'details_after_predecessor_acknowledged_steps':copy.deepcopy(p['details_after_predecessor_acknowledged_steps']),'known_false_flags_preserved':copy.deepcopy(p['known_false_flags_preserved']),'dynamic_details_origins_preserved':copy.deepcopy(p['dynamic_details_origins_preserved']),
  'existing_cause_context_suppression':'UNKNOWN; no new explicit cause/context/suppression evidence or assignment; all error roles retained',
  'line174_evaluation_established':False,'failure_file_established':False,'line175_suppression_established':False,'final_rethrow_established':False,'owner_finalization_established':False,'managed_local_clear_established':False,'active_removal_established':False,'complete_cleanup_established':False,
  'runtime_loop_chain':None,'runtime_observation':False,'observer_join':None,'physical_reference_identity':None,'physical_closure_established':False,'durability_established':False,'released_ownership_established':False,'obligations_discharged':False,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False,
  'completion_flags_mean':'Explicit conditional acknowledgments; false does not establish absence of partial effects; no physical object or interpreter execution observed'}

def validate_cleanup_loop_projection(catalogue,case,validated,submitted):
 status_exact_tree(submitted,'LOOP-SUBMITTED-OUTPUT');status_typed_same(submitted,cleanup_loop_projection(catalogue,case,validated),'LOOP-OUTPUT-CORRESPONDENCE');return True
