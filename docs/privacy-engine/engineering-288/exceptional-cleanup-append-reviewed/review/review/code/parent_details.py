from common import *
from parent_cases import make as make_parent
FIELDS=['error','message','traceback','nonexecution_established','new_authorization','cleanup']
ROUTE=['run-with-exception-exit','session-yield-delivery','session-inner-with-exception-exit','private-yield-delivery','launcher-handler-entry']
ORDER=ROUTE+['details-evaluation-attempt']+[s+'-'+f for f in FIELDS for s in ('details-key','details-value')]+['details-dict-completion','details-assignment-attempt','details-assignment-complete']
def make(m,b,idx,control=False,terminal=None,continuity='explicit conditional premise',owner_continuity=True,invocation='fl6-launcher-details',parent_overrides=None,invalid_parent=False):
 p=b['prior_module'];pb=b['prior_basis'];pc=make_parent(p,pb,idx,control=control,continuity=owner_continuity,invocation=invocation,overrides=parent_overrides)
 parent=p._construct_checked(pb,pc)['projection'];scope=parent['scope'];anchor=pc['anchor'];error=parent['construction_error'];src=b['catalogue']['source'];outcomes=[]
 if continuity=='UNESTABLISHED':terminal=(ORDER[0],'unobserved')
 for s in ORDER:
  k=terminal[1] if terminal and terminal[0]==s else 'normal';outcomes.append({'stage':s,'outcome':k})
  if k!='normal':break
 delivery={'scope':D(scope),'instance_anchor':D(anchor),'selected_error':D(error),'references':{n:D(parent['reference_bindings'][n]) for n in ('owner','token','session','manager')},'route':[{'stage':n,'source':D(src['stages'][n])} for n in ROUTE],'launcher_name':'e','continuity':continuity,'active_exception_continuity':'Conditional same selected error across ordinary delivery and normal evaluation; no observation','runtime_delivery':None,'physical_object_identity':None,'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN'}
 v={'scope':D(scope),'anchor':D(anchor),'parent_result':D(parent),'delivery_binding':D(delivery),'outcomes':D(outcomes)}
 q={'kind':'CONSTRUCTED-LAUNCHER-INITIAL-DETAILS','context':pc['context'],'anchor':D(anchor),'invocation':invocation,'parent_case':pc,'parent_output':parent,'delivery_binding':delivery,'outcomes':outcomes,'projection':v,'output':{}}
 if not invalid_parent:q['output']=b['fresh']['coverage'].launcher_details_projection(b['catalogue'],v,D(v))
 return q
def oracle(q,result):
 p=result['projection'];steps=q['outcomes'];done={s['stage'] for s in steps if s['outcome']=='normal'};assigned=ORDER[-1] in done;entered=ROUTE[-1] in done;error=q['parent_output']['construction_error'];control=q['parent_case']['token_case']['control_present'];terminal=steps[-1]['outcome']
 assert [(e['stage'],e['outcome']) for e in p['events']]==[(e['stage'],e['outcome']) for e in steps]
 assert p['validated_parent']==q['parent_output'] and p['earlier_constructor_exception']==error
 assert p['earlier_control_completed_in_model'] is (True if control else None)
 for flag,stage in [('handler_entry_completed_in_model',ROUTE[-1]),('details_evaluation_attempt_in_model','details-evaluation-attempt'),('details_dictionary_completed_in_model','details-dict-completion'),('details_assignment_attempt_in_model','details-assignment-attempt'),('details_assignment_completed_in_model',ORDER[-1])]:assert p[flag] is (stage in done),flag
 assert p['launcher_e_in_model']==(error if entered else None) and p['active_caught_error_in_model']==(error if entered else None)
 assert (p['replacement_error_in_model'] is not None)==(terminal=='raise')
 assert p['last_pending_error_in_model']==(p['replacement_error_in_model'] or error)
 assert p['terminal_python_exception_in_model'] is (None if terminal in ('process-termination','unobserved') else True)
 assert p['selected_owner_continuity']==q['parent_output']['selected_slot_before_removal']
 for flag in ('new_explicit_cause_assignment_established','cleanup_loop_entered','normal_managed_close_spliced','managed_clear_spliced','ACTIVE_unlink_spliced','failure_file_established','outward_propagation_established','physical_closure_established','physical_lock_release_established','durability_established','outer_cleanup_complete','runtime_observation','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert p[flag] is False,flag
 for flag in ('runtime_handler_arrival','runtime_handler_details_chain','physical_reference_identity','retained_failure_record_bytes','observer_join'):assert p[flag] is None,flag
 assert p['existing_cause_context_suppression']=='UNKNOWN; no new chain observation'
 if assigned:
  d=p['details_in_model'];assert d['known_literal_fields']['nonexecution_established'] is False and d['known_literal_fields']['new_authorization'] is False and type(d['known_literal_fields']['cleanup']) is list and d['known_literal_fields']['cleanup']==[]
  assert [(f['name'],f['expression']) for f in d['dynamic_fields']]==list(zip(FIELDS[:3],['type(e).__name__','str(e)','traceback.format_exc()']))
  for f in d['dynamic_fields']:assert f['selected_error']==error and f['exact_value'] is f['exact_type'] is f['formatted_bytes'] is None and f['observation']=='UNAVAILABLE'
  assert d['complete_runtime_dictionary_observed'] is False and d['exact_serialized_bytes'] is None
 else:assert p['details_in_model'] is None
 assert all(e['scope']==q['projection']['scope'] and e['selected_error']==error and e['owner']==q['delivery_binding']['references']['owner'] and e['token']==q['delivery_binding']['references']['token'] and e['runtime_frame'] is None for e in p['events'])
 return True
