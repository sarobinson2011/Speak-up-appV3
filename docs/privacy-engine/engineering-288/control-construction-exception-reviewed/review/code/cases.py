"""Reviewer-generated cases; no Engineering fixture factory imported."""
from common import *
ORDER=['finally-enter','removal-attempt','removal-complete']
PREFIX=['owner-create','token-create','registry-insert','control-guard','control-create']
def make(m,basis,index,invocation='fl6-construction-selected',continuity=True,owner_none=True,terminal=None):
 anchor=D(basis['prior']['contexts'][index]['token_registration_correspondence']['instance_anchor'])
 scope={'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':D(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
 sb=basis['stored_basis'];tb=sb['token_basis'];tcov=tb['fresh']['coverage'];tcat=tb['catalogue']
 outcomes=[{'stage':s,'outcome':'raise' if s=='control-create' else 'normal'} for s in PREFIX]
 validated={'occurrence':invocation,'scope':scope,'control_present':True,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':outcomes}
 ti={**D(validated),'references':tcov.token_reference_premises(scope,True)}
 prefix=tcov.token_registration_projection(tcat,ti,validated)
 tc={'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':anchor['context'],'anchor':D(anchor),'invocation':invocation,'control_present':True,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':D(outcomes),'projection':ti,'output':prefix}
 steps=[]
 for s in ORDER:
  outcome=terminal[1] if terminal and terminal[0]==s else 'normal';steps.append({'stage':s,'outcome':outcome})
  if outcome!='normal':break
 source=basis['catalogue']['source'];refs=prefix['reference_bindings']
 error={'role':'selected-control-construction-expression-exception','scope':D(scope),'occurrence':invocation+'/control-create/exception','reference':invocation+'/control-create/error','construction_attempt':{'occurrence':invocation+'/control-create','source':D(source['construction_expression']),'argument_token':D(refs['token']),'registered_owner':D(refs['owner'])},'local_handler_binding':None,'exact_type':None,'exact_value_bytes':None,'failure_mechanism':None,'allocation_progress':None,'initializer_progress':None,'completed_object_reference':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}
 q={'kind':'CONSTRUCTED-CONTROL-CONSTRUCTION-EXCEPTION','context':anchor['context'],'anchor':anchor,'invocation':invocation,'token_case':tc,'construction_error':error,'outcomes':steps,'projection':{'scope':D(scope),'references':D(refs),'token_inputs':D(ti),'token_prefix':D(prefix),'construction_error':D(error),'outcomes':D(steps)},'output':None}
 c=basis['fresh']['coverage'];q['output']=c.control_construction_projection(basis['catalogue'],q['projection'],D(q['projection']))
 return q
def oracle(q,result):
 steps=q['outcomes'];normal=[]
 for e in steps:
  if e['outcome']=='normal':normal.append(e['stage'])
  else:break
 popped=len(normal)==3;terminal=steps[-1]['outcome'];p=result['projection']
 assert [e['stage'] for e in p['events']]==[e['stage'] for e in steps]
 assert [e['outcome'] for e in p['events']]==[e['outcome'] for e in steps]
 for flag in ('construction_completed_in_model','control_callback_executed_in_model','subsequent_client_execution_in_model','client_handler_entered_in_model','owner_failure_guard_evaluated_in_model','new_explicit_cause_assignment_established_in_model','runtime_observation','run_success_established','obligations_discharged','authorization_renewed','actual_admission'):assert p[flag] is False,flag
 for field in ('allocation_progress','initializer_progress','completed_control_object_reference','observer_join','outer_cleanup_completion','database_cleanup_completion','retained_failure_record_bytes','physical_reference_identity'):assert p[field] is None,field
 assert p['construction_expression_raised_in_model'] is True and p['validated_token_prefix']['registration_completed_in_model'] is True
 assert p['construction_error']==q['construction_error']
 assert p['finally_entry_completed_in_model']==('finally-enter' in normal)
 assert p['removal_completed_in_model'] is popped
 assert p['construction_outward_after_finally_established_in_model'] is popped
 assert p['selected_owner_removed_in_model'] is (True if popped and q['token_case']['registry_continuity'] else None)
 assert p['slot_after_pop_in_model']==('ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN')
 assert p['outward_error_after_finally_in_model']==(q['construction_error'] if popped else None)
 if terminal=='raise':
  assert p['cleanup_error_in_model']['role']=='conditional-finally-exception' and p['last_pending_error_in_model']==p['cleanup_error_in_model']
 elif terminal in ('unobserved','process-termination'):assert p['terminal_python_exception_in_model'] is None and p['cleanup_error_in_model'] is None
 for k in ('existing_cause','existing_context','existing_suppression','cleanup_context_link'):assert p['exception_chain_observation'][k]=='UNKNOWN'
 assert all(e['scope']==q['projection']['scope'] and e['owner']==q['projection']['references']['owner'] and e['token']==q['projection']['references']['token'] and e['runtime_frame'] is None for e in p['events'])
 return True
