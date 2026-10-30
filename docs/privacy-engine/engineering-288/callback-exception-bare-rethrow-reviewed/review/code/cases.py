from common import *
ORDER=['callback-handler-enter','callback-none-guard','callback-bare-rethrow','finally-enter','removal-attempt','removal-complete']
def token(b,idx,inv,control=True,continuity=True):
 row=b['prior']['contexts'][idx]['token_registration_correspondence'];anchor=D(row['instance_anchor']);sb=b['stored_basis'];tb=sb['token_basis'];tm=sb['routes']['token_module'];scope=tm.invocation_scope(anchor,inv);c=tb['fresh']['coverage']
 # Independent finite prefix: selected creation/registration, optional control,
 # then client construction and callback raise. No inference beyond that raise.
 steps=['owner-create','token-create','registry-insert','control-guard']+(['control-create','control-callback'] if control else [])+['client-create','client-callback']
 v={'occurrence':inv,'scope':scope,'control_present':control,'owner_failure_none':True,'registry_continuity':continuity,'outcomes':[{'stage':s,'outcome':'raise' if s=='client-callback' else 'normal'} for s in steps]}
 p={**D(v),'references':c.token_reference_premises(scope,control)};out=c.token_registration_projection(tb['catalogue'],p,v)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':anchor,'invocation':inv,**{k:D(v[k]) for k in ('control_present','owner_failure_none','registry_continuity','outcomes')},'projection':p,'output':out}
def normal(m,b,idx,inv=None,control=True,continuity=True,terminal=None):
 inv=inv or 'FL6-bare-'+str(idx);tc=token(b,idx,inv,control,continuity);cat=b['catalogue'];scope=tc['output']['scope'];refs=tc['output']['reference_bindings'];c=b['fresh']['coverage']
 guard={'scope':D(scope),'owner':D(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':'owner.failure is not None','guard_result':False,'guard_source':D(cat['source']['guard']),'source':D(cat['source']['sources']['entry']),'premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 path=ORDER[:]
 if terminal:
  i=ORDER.index(terminal[0]);path=ORDER[:i+1]+(ORDER[3:] if terminal[1]=='raise' and i<3 else [])
 outcomes=[{'stage':s,'outcome':terminal[1] if terminal and terminal[0]==s else 'reraised-callback' if s==ORDER[2] else 'normal'} for s in path]
 x={'kind':'CONSTRUCTED-CALLBACK-BARE-RETHROW','context':tc['context'],'anchor':D(tc['anchor']),'invocation':inv,'token_case':tc,'none_guard_binding':guard,'callback_error':c.callback_error_binding(cat,scope),'outcomes':outcomes,'projection':{},'output':{}}
 return refresh(m,b,x)
def refresh(m,b,x):
 x['projection']=m._premises(b,x);x['output']=b['fresh']['coverage'].callback_bare_projection(b['catalogue'],D(x['projection']),D(x['projection']));return x
def independently_check(x):
 o=x['output'];ev=x['outcomes'];ack={e['stage'] for e in ev if e['outcome'] in ('normal','reraised-callback')};rethrow=ORDER[2] in ack;pop=ORDER[5] in ack
 assert o['callback_raised_in_model'] is True and o['callback_returned_normally_in_model'] is False
 for field,stage in zip(('callback_handler_entry_completed_in_model','none_guard_completed_in_model','bare_rethrow_completed_in_model','finally_entry_completed_in_model','removal_attempt_entered_in_model','removal_completed_in_model'),ORDER):assert o[field] is (stage in ack),(field,o[field])
 assert o['none_guard_binding']['slot_value'] is None and o['none_guard_binding']['guard_result'] is False
 assert o['none_guard_binding']['owner']==o['reference_bindings']['owner']
 assert o['callback_error']==x['callback_error'] and o['reraised_error_in_model']==(x['callback_error'] if rethrow else None)
 assert o['bare_raise_semantics']=={'adds_explicit_cause':False,'preserves_active_exception':True,'establishes_absent_existing_cause_or_context':False}
 assert o['exception_chain_observation']=={'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','physical_reference_observation':None}
 assert o['new_explicit_cause_assignment_established_in_model'] is False
 pre=[e for e in ev if e['outcome']=='raise' and e['stage'] in ORDER[:3]];cleanup=[e for e in ev if e['outcome']=='raise' and e['stage'] in ORDER[3:]]
 assert (o['handler_evaluation_error_in_model'] is not None)==bool(pre) and (o['cleanup_error_in_model'] is not None)==bool(cleanup)
 expected=o['cleanup_error_in_model'] if cleanup else o['handler_evaluation_error_in_model'] if pre else x['callback_error']
 assert o['last_pending_error_in_model']==expected
 assert o['outward_error_after_finally_in_model']==(expected if pop else None) and o['callback_outward_after_finally_established_in_model']==(pop and rethrow)
 assert o['terminal_python_exception_in_model'] is (None if ev[-1]['outcome'] in ('process-termination','unobserved') else True)
 assert o['selected_owner_removed_in_model'] is (True if pop and x['token_case']['registry_continuity'] else None)
 assert o['slot_after_pop_in_model']==('ABSENT-AT-POP-COMPLETION' if pop else 'UNKNOWN')
 assert o['validated_token_prefix']==x['token_case']['output'] and o['validated_token_prefix']['registration_completed_in_model'] is True
 for k in ('run_success_established','callback_reaches_launcher_established','runtime_observation','physical_lock_release_established','exclusive_ownership_established','durability_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert o[k] is False,k
 for k in ('runtime_callback_bare_revocation_chain','physical_reference_identity','outer_cleanup_completion','database_cleanup_completion','retained_failure_record_bytes','observer_join','revocation_persists','pop_result_observation'):assert o[k] is None,k
 assert o['callback_error']['exact_type'] is None and o['callback_error']['exact_value_bytes'] is None and o['callback_error']['producer_history']=='UNAVAILABLE'
 assert o['prior_failure_storage_history'].startswith('UNKNOWN;')
 return True
