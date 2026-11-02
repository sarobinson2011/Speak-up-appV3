"""Independent loop fixtures and oracle; no Engineering factory/oracle used.
The retained independent parent factory supplies prerequisite cases, which are
revalidated by the actual unchanged predecessor using the authenticated basis.
"""
from common import *
from loop_expectations import ORDER,NORMAL
import report_cases
def binding(p,a,cat,continuity):
 old=p['binding'];scope=p['scope'];pre=p['validated_parent']
 return {'scope':D(scope),'instance_anchor':D(a),'append_occurrence':D(p['events'][-1]),'handler_origin':D(cat['source']['handler']),'original_constructor_error':D(p['earlier_constructor_exception']),'selected_cleanup_error':D(p['selected_cleanup_error']),'protected_failure_occurrence':D(p['selected_failure_occurrence']),'references':D(old['references']),'selected_name':'managed','selected_object':D(old['selected_object']),'details_role':D(old['details_role']),'cleanup_list':D(old['cleanup_list']),'loop':{'ordered_values':D(pre['binding']['ordered_values']),'entry_count':2,'selected_index':1,'next_index':2,'raw_guard':False,'raw_body_skipped':True,'managed_guard':True,'selected_is_last':True,'iterator_role':scope['invocation']+'/launcher/cleanup-loop/iterator','source':D(cat['source']['loop'])},'continuity':continuity,'premise':cat['source']['continuity'],'physical_identity_observed':None,'runtime_continuation_observed':None}
def make(m,b,idx,control=False,origin='append',invocation=None):
 inv=invocation or f'fl6-loop-{idx}-{int(control)}-{origin}'
 pc=report_cases.make(b['prior_module'],b['prior_basis'],idx,control,origin,invocation=inv)
 p=b['prior_module']._construct_checked(b['prior_basis'],pc)['projection']
 q={'kind':'CONSTRUCTED-CLEANUP-LOOP','context':pc['context'],'anchor':D(pc['anchor']),'invocation':inv,'parent_case':pc,'parent_output':p,'binding':binding(p,pc['anchor'],b['catalogue'],'explicit conditional premise'),'outcomes':[{'stage':s,'outcome':NORMAL[s]} for s in ORDER]}
 return refresh(b,q)
def refresh(b,q):
 q=D(q);q['projection']={'scope':D(q['parent_output']['scope']),'anchor':D(q['anchor']),'parent_result':D(q['parent_output']),'binding':D(q['binding']),'outcomes':D(q['outcomes'])}
 # Generation is not an oracle or authentication. oracle() independently checks it.
 q['output']=b['fresh']['coverage'].cleanup_loop_projection(b['catalogue'],q['projection'],D(q['projection']))
 return q
def frontier(b,q,stage,kind,continuity=None):
 q=D(q);n=ORDER.index(stage);q['outcomes']=q['outcomes'][:n]+[{'stage':stage,'outcome':kind}]
 if continuity:q['binding']['continuity']=continuity
 return refresh(b,q)
def oracle(q,result,source):
 o=result['projection'];p=q['parent_output'];binding=q['binding'];scope=p['scope'];steps=q['outcomes'];last=steps[-1]['outcome'];i=ORDER.index(steps[-1]['stage'])
 assert [s['stage'] for s in steps]==ORDER[:i+1]
 normal=last==NORMAL[steps[-1]['stage']];ack=set(ORDER[:i+(1 if normal else 0)])
 exited=ORDER[1] in ack;complete=ORDER[-1] in ack;seen={s['stage'] for s in steps}
 selected=p['selected_cleanup_error'];original=p['earlier_constructor_exception']
 assert o['scope']==scope and o['instance_anchor']==q['anchor'] and o['binding']==binding and o['validated_parent']==p
 assert o['completion']==('normal-cleanup-loop-exhaustion' if complete else {'raise':'replacement-exception-frontier','catchable-interruption':'interruption-frontier','process-termination':'process-termination','unobserved':'unobserved-continuation'}[last])
 for f,s in [('handler_exit_established',ORDER[1]),('selected_body_complete',ORDER[2]),('ordinary_exhaustion_established',ORDER[4]),('loop_completion_established',ORDER[5])]:assert o[f] is (s in ack),f
 assert o['final_advance_attempted'] is (ORDER[3] in seen)
 assert o['caught_name_lifetime']=={'name':'close_error','last_acknowledged_binding':'CLEARED' if exited else 'BOUND selected cleanup error','normal_departure_clears_name':True,'state_at_nonnormal_frontier':'CONDITIONAL normal completion' if complete else 'UNOBSERVED','physical_destruction_established':False}
 assert o['retained_cleanup_error_evidence']==o['last_acknowledged_inner_caught_error']==selected
 assert o['last_acknowledged_active_caught_error_in_model']==(original if exited else selected)
 assert o['active_error_at_terminal_observed'] is None and o['original_error_pending_in_outer_handler']==original
 replacement=o['replacement_error_in_model'];assert (replacement is not None)==(last in ('raise','catchable-interruption'))
 if replacement:
  assert replacement['role']=='conditional-loop-continuation-replacement' and replacement['reference']==scope['invocation']+'/cleanup-loop/'+steps[-1]['stage']+'/error' and replacement['scope']==scope and replacement['mode']==last
  assert all(replacement['origin'][k]==v for k,v in source['stages'][steps[-1]['stage']].items())
  assert replacement['exact_type'] is replacement['exact_value_bytes'] is None and replacement['runtime_observation'] is False
  assert all(replacement[k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression'))
 assert o['last_pending_error_in_model']==(replacement or (original if exited else selected))
 assert o['terminal_python_exception_in_model'] is (None if last in ('process-termination','unobserved') else True)
 assert o['ordinary_exhaustion_is_new_propagating_error'] is False
 assert o['loop_target_bindings_retained']=={'name':'managed','obj':binding['selected_object'],'conditional_continuity':binding['continuity']}
 assert [e['stage'] for e in o['events']]==[s['stage'] for s in steps]
 for e,s in zip(o['events'],steps):
  assert e['id']==scope['invocation']+'/cleanup-loop/'+s['stage'] and e['scope']==scope and e['outcome']==s['outcome']
  assert e['owner']==binding['references']['owner'] and e['token']==binding['references']['token'] and e['append_occurrence']==p['events'][-1]['id'] and e['runtime_frame'] is None
  assert all(e['source'][k]==v for k,v in source['stages'][s['stage']].items())
 for f in ('earlier_control_completed_in_model','selected_owner_continuity','failure_origin_region','close_normal_return_completed_in_model','close_itself_failed_established_in_model','managed_close_relation','cleanup_list_state','details_after_predecessor_acknowledged_steps','known_false_flags_preserved','dynamic_details_origins_preserved'):assert o[f]==p[f],f
 assert o['report_append_completed_in_model'] is True
 assert o['cleanup_list_state']['complete_contents_established'] is False and o['cleanup_list_state']['exact_runtime_contents'] is None
 assert all(type(v) is bool and v is False for v in o['known_false_flags_preserved'].values())
 if p['failure_origin_region']=='protected-append':
  assert o['close_normal_return_completed_in_model'] is True and o['close_itself_failed_established_in_model'] is False
  assert o['cleanup_list_state']['prior_partial_effects']=='UNKNOWN' and o['cleanup_list_state']['any_unresolved_partial_effects'] is True
 for f in ('normal_overall_return_established','additional_body_execution_established','line174_evaluation_established','failure_file_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','runtime_observation','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert o[f] is False,f
 for f in ('runtime_loop_chain','observer_join','physical_reference_identity'):assert o[f] is None,f
 assert o['existing_cause_context_suppression'].startswith('UNKNOWN;')
 return True
