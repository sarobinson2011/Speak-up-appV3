"""Formal-Lab reviewer cases from defining source; Engineering factories unused."""
from common import *
ORDER=['callback-handler-enter','callback-none-guard','callback-bare-rethrow','finally-enter','removal-attempt','removal-complete']
def steps(overrides=None):
 overrides=overrides or {};out=[];pos=0
 while pos<6:
  s=ORDER[pos];k=overrides.get(s,'reraised-construction' if pos==2 else 'normal');out.append({'stage':s,'outcome':k})
  if k in ('process-termination','unobserved') or (k=='raise' and pos>=3):break
  pos=3 if k=='raise' else pos+1
 return out
def make(m,basis,index,control=False,continuity=True,invocation='fl6-client-construction',overrides=None):
 anchor=D(basis['prior']['contexts'][index]['token_registration_correspondence']['instance_anchor'])
 scope={'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':D(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
 tb=basis['stored_basis']['token_basis'];tcov=tb['fresh']['coverage'];tcat=tb['catalogue']
 prefix=['owner-create','token-create','registry-insert','control-guard']+(['control-create','control-callback'] if control else [])+['client-create']
 before=[{'stage':s,'outcome':'raise' if s=='client-create' else 'normal'} for s in prefix]
 val={'occurrence':invocation,'scope':D(scope),'control_present':control,'owner_failure_none':True,'registry_continuity':continuity,'outcomes':before}
 ti={**D(val),'references':tcov.token_reference_premises(scope,control)}
 token=tcov.token_registration_projection(tcat,ti,val)
 tc={'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':anchor['context'],'anchor':D(anchor),'invocation':invocation,'control_present':control,'owner_failure_none':True,'registry_continuity':continuity,'outcomes':D(before),'projection':D(ti),'output':D(token)}
 source=basis['catalogue']['source'];refs=token['reference_bindings']
 error={'role':'selected-client-construction-expression-exception','scope':D(scope),'occurrence':invocation+'/client-create/exception','reference':invocation+'/client-create/error','construction_attempt':{'occurrence':invocation+'/client-create','source':D(source['construction_expression']),'argument_token':D(refs['token']),'registered_owner':D(refs['owner'])},'handler_binding_name_from_source':'client_error','handler_binding_established_by_this_role':False,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}
 guard={'scope':D(scope),'owner':D(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':'owner.failure is not None','guard_result':False,'guard_source':D(source['guard']),'source':D(source['sources']['entry']),'premise':source['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 outcomes=steps(overrides)
 projection={'scope':D(scope),'references':D(refs),'token_inputs':D(ti),'token_prefix':D(token),'construction_error':D(error),'none_guard_binding':D(guard),'outcomes':D(outcomes)}
 q={'kind':'CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','context':anchor['context'],'anchor':anchor,'invocation':invocation,'token_case':tc,'construction_error':error,'none_guard_binding':guard,'outcomes':outcomes,'projection':projection,'output':None}
 q['output']=basis['fresh']['coverage'].client_construction_projection(basis['catalogue'],projection,D(projection))
 return q
def oracle(q,result):
 p=result['projection'];events=q['outcomes'];done={e['stage'] for e in events if e['outcome'] in ('normal','reraised-construction')}
 evaluation=next((e['stage'] for e in events if e['outcome']=='raise' and e['stage'] in ORDER[:3]),None)
 cleanup=next((e['stage'] for e in events if e['outcome']=='raise' and e['stage'] in ORDER[3:]),None)
 popped='removal-complete' in done;reraised='callback-bare-rethrow' in done;control=q['token_case']['control_present'];terminal=events[-1]['outcome']
 assert [(e['stage'],e['outcome']) for e in p['events']]==[(e['stage'],e['outcome']) for e in events]
 assert p['construction_expression_raised_in_model'] is True and p['validated_token_prefix']['registration_completed_in_model'] is True
 for f in ('construction_completed_in_model','client_callback_executed_in_model','new_explicit_cause_assignment_established_in_model','construction_reaches_launcher_established','run_success_established','runtime_observation','obligations_discharged','authorization_renewed','actual_admission','durability_established','physical_lock_release_established','exclusive_ownership_established'):assert p[f] is False,f
 for f in ('completed_client_object_reference','allocation_progress','initializer_progress','observer_join','runtime_client_construction_revocation_chain','outer_cleanup_completion','database_cleanup_completion','retained_failure_record_bytes','physical_reference_identity'):assert p[f] is None,f
 assert p['earlier_control_present'] is control
 assert p['earlier_control_construction_completed_in_model'] is (True if control else None)
 assert p['earlier_control_callback_completed_in_model'] is (True if control else None)
 for flag,stage in [('handler_entry_completed_in_model',ORDER[0]),('none_guard_completed_in_model',ORDER[1]),('bare_rethrow_effect_established_in_model',ORDER[2]),('finally_entry_completed_in_model',ORDER[3]),('removal_attempt_entered_in_model',ORDER[4]),('removal_completed_in_model',ORDER[5])]:assert p[flag] is (stage in done),flag
 assert p['construction_error']==q['construction_error']
 assert p['caught_error_in_model']==(q['construction_error'] if ORDER[0] in done else None)
 assert p['reraised_error_in_model']==(q['construction_error'] if reraised else None)
 assert (p['handler_evaluation_error_in_model'] is not None)==(evaluation is not None)
 assert (p['cleanup_error_in_model'] is not None)==(cleanup is not None)
 pending=p['cleanup_error_in_model'] or p['handler_evaluation_error_in_model'] or q['construction_error']
 assert p['last_pending_error_in_model']==pending
 assert p['outward_error_after_finally_in_model']==(pending if popped else None)
 assert p['construction_outward_after_finally_established_in_model'] is (popped and reraised)
 assert p['slot_after_pop_in_model']==('ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN')
 assert p['selected_owner_removed_in_model'] is (True if popped and q['token_case']['registry_continuity'] else None)
 assert p['terminal_python_exception_in_model'] is (None if terminal in ('process-termination','unobserved') else True)
 assert p['none_guard_binding']['slot_value'] is None and p['none_guard_binding']['guard_result'] is False
 assert p['bare_raise_semantics']=={'adds_explicit_cause':False,'preserves_active_exception':True,'establishes_absent_existing_cause_or_context':False}
 assert all(p['exception_chain_observation'][k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression','cleanup_context_link'))
 assert p['prior_failure_storage_history']=='UNKNOWN; the exact None guard does not erase earlier established storage or evidence'
 assert all(e['scope']==q['projection']['scope'] and e['token']==q['projection']['references']['token'] and e['owner']==q['projection']['references']['owner'] and e['runtime_frame'] is None for e in p['events'])
 return True
