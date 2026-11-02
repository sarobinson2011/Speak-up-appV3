"""Independent line172 constructors/oracle. Reuse only reviewed parent prerequisites."""
from common import *
from source_expectations import ORDER
import cleanup_cases
def parent(m,b,idx,control,origin,invocation):
 stage,kind={'close':('close-normal-return','abrupt'),'append':('append-call-attempt','normal'),'lookup':('close-method-evaluation','normal'),'append-lookup':('append-method-evaluation','normal')}.get(origin,(origin,'normal'))
 q=cleanup_cases.build(m,b,idx,control,terminal=(stage,'raise'),close_kind=kind,invocation=invocation)
 o=m._construct_checked(b,q)['projection'];assert cleanup_cases.oracle(q,{'projection':o});return q,o
def binding(parent,anchor,cat,continuity):
 details=parent['details_after_acknowledged_steps'];old=parent['binding']
 return {'scope':D(parent['scope']),'instance_anchor':D(anchor),'selected_failure':D(parent['replacement_error_in_model']),'failure_occurrence':D(parent['events'][-1]),'constructor_error':D(parent['earlier_constructor_exception']),'references':D(old['references']),'selected_name':'managed','selected_object':D(old['object']),'details_role':{k:D(details[k]) for k in ('role','reference','scope')},'cleanup_list':D(details['cleanup_reference']),'caught_name':'close_error','handler_origin':D(cat['source']['handler']),'continuity':continuity,'premise':cat['source']['continuity'],'physical_identity_observed':None,'runtime_delivery_observed':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}
def make(m,b,idx,control=False,origin='append',terminal=None,continuity='explicit conditional premise',invocation=None):
 inv=invocation or f'fl6-line172-{idx}-{int(control)}-{origin}';pc,po=parent(b['prior_module'],b['prior_basis'],idx,control,origin,inv);a=pc['anchor'];bind=binding(po,a,b['catalogue'],continuity)
 if continuity=='UNESTABLISHED':terminal=(ORDER[0],'unobserved')
 outcomes=[]
 for s in ORDER:
  o=terminal[1] if terminal and s==terminal[0] else 'normal';outcomes.append({'stage':s,'outcome':o})
  if o!='normal':break
 v={'scope':D(po['scope']),'anchor':D(a),'parent_result':D(po),'binding':D(bind),'outcomes':D(outcomes)}
 q={'kind':'CONSTRUCTED-CLEANUP-ERROR-REPORT','context':pc['context'],'anchor':D(a),'invocation':inv,'parent_case':pc,'parent_output':po,'binding':bind,'outcomes':outcomes,'projection':v,'output':{}}
 q['output']=b['fresh']['coverage'].error_report_projection(b['catalogue'],v,D(v));return q
def oracle(q,result,source):
 o=result['projection'];p=q['parent_output'];steps=q['outcomes'];done={x['stage'] for x in steps if x['outcome']=='normal'};seen={x['stage'] for x in steps};last=steps[-1]['outcome'];original=p['earlier_constructor_exception'];selected=p['replacement_error_in_model'];scope=p['scope'];bound='caught-error-binding-complete' in done;entered='handler-entry' in done;appended=ORDER[-1] in done
 assert o['validated_parent']==p and o['binding']==q['binding'] and o['scope']==scope and o['instance_anchor']==q['anchor']
 assert o['earlier_constructor_exception']==o['original_error_pending_in_outer_handler']==original
 assert o['selected_cleanup_error']==selected and o['selected_failure_occurrence']==p['events'][-1]
 assert selected!=original and selected['scope']==scope and selected['origin']==p['events'][-1]['source']
 assert o['failure_origin_region']==selected['failure_region'] and selected['failure_region'] in ('protected-close','protected-append')
 assert o['close_normal_return_completed_in_model'] is p['close_normal_return_completed_in_model'] and o['close_itself_failed_established_in_model'] is p['close_itself_failed_established_in_model']
 if selected['failure_region']=='protected-append':assert o['close_normal_return_completed_in_model'] is True and o['close_itself_failed_established_in_model'] is False
 assert o['managed_close_relation']==p['managed_close_relation'] and o['earlier_control_completed_in_model'] is p['earlier_control_completed_in_model']
 assert o['handler_eligible_in_model'] is True
 for field,s in [('handler_match_completed_in_model','handler-match'),('handler_selected_in_model','handler-selection'),('handler_entry_completed_in_model','handler-entry'),('caught_binding_completed_in_model','caught-error-binding-complete'),('report_append_completed_in_model','report-append-complete'),('error_item_completed_in_model','report-item-complete')]:assert o[field] is (s in done),field
 assert o['caught_binding_attempted_in_model'] is ('caught-error-binding-attempt' in seen)
 assert o['caught_name_in_model']==('close_error' if bound else None) and o['caught_error_in_model']==(selected if bound else None)
 # Last ACKNOWLEDGED source boundary is not an observation of terminal interpreter state.
 assert o['last_acknowledged_active_caught_error_in_model']==(selected if entered else original) and o['active_at_terminal_observed'] is None
 replacement=o['replacement_error_in_model'];assert (replacement is not None)==(last=='raise')
 if replacement:
  assert replacement['reference']==scope['invocation']+'/error-report/'+steps[-1]['stage']+'/error' and replacement['scope']==scope
  for k,v in source['stages'][steps[-1]['stage']].items():assert replacement['origin'][k]==v
  assert replacement['exact_type'] is replacement['exact_value_bytes'] is None
  assert all(replacement[k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression'))
 assert o['last_pending_error_in_model']==(replacement or selected)
 assert o['terminal_python_exception_in_model'] is (None if last in ('process-termination','unobserved') else True)
 assert [e['stage'] for e in o['events']]==[s['stage'] for s in steps]
 for e,s in zip(o['events'],steps):
  assert e['scope']==scope and e['outcome']==s['outcome'] and e['id']==scope['invocation']+'/error-report/'+s['stage']
  assert e['selected_error']==selected and e['selected_failure_occurrence']==p['events'][-1] and e['owner']==q['binding']['references']['owner'] and e['token']==q['binding']['references']['token'] and e['runtime_frame'] is None
  for k,v in source['stages'][s['stage']].items():assert e['source'][k]==v
 details=p['details_after_acknowledged_steps'];assert o['details_after_predecessor_acknowledged_steps']==details
 assert o['dynamic_details_origins_preserved']==details['dynamic_fields']
 assert o['known_false_flags_preserved']=={'nonexecution_established':False,'new_authorization':False} and all(type(v) is bool for v in o['known_false_flags_preserved'].values())
 item=o['error_item_in_model']
 if 'report-item-complete' in done:
  assert type(item) is list and len(item)==3 and item[0]=='managed'
  for x,which,expr in zip(item[1:],('error_name','message'),('type(close_error).__name__','str(close_error)')):
   assert x['argument']==selected and x['caught_name']=='close_error' and x['expression']==expr
   assert x['exact_type'] is x['exact_value'] is x['formatted_bytes'] is None and x['runtime_observation'] is False
   for k,v in source['dynamic_origins'][which].items():assert x['origin'][k]==v
 else:assert item is None
 state=o['cleanup_list_state'];prior_unknown=p['cleanup_list_after_frontier']=='UNKNOWN partial effects';attempt='report-append-attempt' in seen
 assert state['target']==q['binding']['cleanup_list'] and state['last_predecessor_acknowledged_literals']==details['known_literal_fields']['cleanup']
 assert state['prior_partial_effects']==('UNKNOWN' if prior_unknown else 'No earlier append call reached in validated prefix')
 assert state['current_partial_effects']==('UNKNOWN' if attempt and not appended else 'Acknowledged selected error-item append' if appended else 'No error-item append call reached')
 assert state['any_unresolved_partial_effects'] is (prior_unknown or (attempt and not appended))
 assert state['complete_contents_established'] is False and state['exact_runtime_contents'] is None
 assert o['report_append_attempted_in_model'] is attempt
 if appended:assert state['acknowledged_append']=={'item':item,'target':q['binding']['cleanup_list'],'occurrence':scope['invocation']+'/error-report/report-append-complete'}
 else:assert state['acknowledged_append'] is None
 for k in ('normal_overall_return_established','handler_exit_established','later_iteration_established','loop_completion_established','failure_file_established','final_rethrow_established','owner_finalization_established','complete_cleanup_established','runtime_observation','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert o[k] is False,k
 for k in ('runtime_error_report_chain','observer_join','physical_reference_identity'):assert o[k] is None,k
 return True
