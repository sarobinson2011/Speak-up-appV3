from common import *
PREFIX=['owner-create','token-create','registry-insert','control-guard','control-create','control-callback']
ORDER=['finally-enter','removal-attempt','removal-complete']
def token(b,idx,inv,none=True,continuity=True):
 row=b['prior']['contexts'][idx]['token_registration_correspondence'];anchor=D(row['instance_anchor']);sb=b['stored_basis'];tb=sb['token_basis'];tm=sb['routes']['token_module'];scope=tm.invocation_scope(anchor,inv);c=tb['fresh']['coverage']
 v={'occurrence':inv,'scope':scope,'control_present':True,'owner_failure_none':none,'registry_continuity':continuity,'outcomes':[{'stage':s,'outcome':'raise' if s=='control-callback' else 'normal'} for s in PREFIX]}
 p={**D(v),'references':c.token_reference_premises(scope,True)};out=c.token_registration_projection(tb['catalogue'],p,v)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':anchor,'invocation':inv,**{k:D(v[k]) for k in ('control_present','owner_failure_none','registry_continuity','outcomes')},'projection':p,'output':out}
def normal(m,b,idx,inv=None,none=True,continuity=True,terminal=None):
 inv=inv or 'FL6-control-'+str(idx);tc=token(b,idx,inv,none,continuity);scope=tc['output']['scope'];refs=tc['output']['reference_bindings'];cat=b['catalogue']
 # Independently express the invocation-qualified error role, without calling
 # the new implementation's role factory or premise reconstruction.
 err={'role':'selected-control-callback-exception','scope':D(scope),'occurrence':inv+'/control-callback/exception','reference':inv+'/control-callback/error','callback_occurrence':inv+'/control-callback','callback_argument_reference':D(refs['control']),'source':D(cat['source']['control_call']),
      'callee':'selected control argument of this _run invocation','local_handler_binding':None,'exact_type':None,'exact_value_bytes':None,'producer_history':'UNAVAILABLE','existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','runtime_reference_observation':None}
 path=ORDER[:] if terminal is None else ORDER[:ORDER.index(terminal[0])+1]
 outcomes=[{'stage':s,'outcome':terminal[1] if terminal and terminal[0]==s else 'normal'} for s in path]
 x={'kind':'CONSTRUCTED-CONTROL-EXCEPTION','context':tc['context'],'anchor':D(tc['anchor']),'invocation':inv,'token_case':tc,'control_error':err,'outcomes':outcomes,'projection':{},'output':{}}
 p={'scope':D(scope),'references':D(refs),'token_inputs':D(tc['projection']),'token_prefix':D(tc['output']),'control_error':D(err),'outcomes':D(outcomes)}
 x['projection']=p;x['output']=b['fresh']['coverage'].control_exception_projection(cat,D(p),D(p));independently_check(x);return x
def independently_check(x):
 o=x['output'];steps=x['outcomes'];ack=[e['stage'] for e in steps if e['outcome']=='normal'];pop=ORDER[-1] in ack;end=steps[-1];raised=end['outcome']=='raise';uncertain=end['outcome'] in ('process-termination','unobserved')
 assert o['control_error']==x['control_error'] and o['validated_token_prefix']==x['token_case']['output']
 assert o['control_callback_raised_in_model'] is True and o['control_callback_returned_normally_in_model'] is False
 for flag,s in zip(('finally_entry_completed_in_model','removal_attempt_entered_in_model','removal_completed_in_model'),ORDER):assert o[flag] is (s in ack),flag
 assert [e['stage'] for e in o['events']]==[e['stage'] for e in steps]
 for i,e in enumerate(o['events']):
  assert e['id']==x['invocation']+'/'+steps[i]['stage'] and e['outcome']==steps[i]['outcome']
  assert e['scope']==o['scope'] and e['owner']==o['reference_bindings']['owner'] and e['token']==o['reference_bindings']['token'] and e['control']==o['reference_bindings']['control']
  assert e['pending_error_on_entry']==x['control_error'] and e['runtime_frame'] is None
 if raised:
  cleanup=o['cleanup_error_in_model'];assert cleanup['role']=='conditional-finally-exception' and cleanup['scope']==o['scope']
  assert cleanup['reference']==x['invocation']+'/'+end['stage']+'/error'
  assert cleanup['exact_type'] is None and cleanup['physical_identity'] is None and cleanup['existing_cause']==cleanup['existing_context']=='UNKNOWN'
  assert o['last_pending_error_in_model']==cleanup and o['completion']=='cleanup-exceptional-frontier'
 else:
  assert o['cleanup_error_in_model'] is None and o['last_pending_error_in_model']==x['control_error']
  assert o['completion']==(end['outcome'] if uncertain else 'normal-removal-pending-control-error')
 assert o['outward_error_after_finally_in_model']==(x['control_error'] if pop else None)
 assert o['control_outward_after_finally_established_in_model'] is pop
 assert o['terminal_python_exception_in_model'] is (None if uncertain else True)
 assert o['selected_owner_removed_in_model'] is (True if pop and x['token_case']['registry_continuity'] else None)
 assert o['slot_after_pop_in_model']==('ABSENT-AT-POP-COMPLETION' if pop else 'UNKNOWN')
 assert o['exception_chain_observation']=={'existing_cause':'UNKNOWN','existing_context':'UNKNOWN','existing_suppression':'UNKNOWN','cleanup_context_link':'UNKNOWN','physical_reference_observation':None}
 for k in ('subsequent_client_execution_in_model','client_handler_entered_in_model','owner_failure_guard_evaluated_in_model','new_explicit_cause_assignment_established_in_model','control_reaches_launcher_established','run_success_established','runtime_observation','physical_lock_release_established','exclusive_ownership_established','durability_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert o[k] is False,k
 for k in ('runtime_control_exception_revocation_chain','physical_reference_identity','outer_cleanup_completion','database_cleanup_completion','retained_failure_record_bytes','observer_join','revocation_persists','pop_result_observation'):assert o[k] is None,k
 assert o['validated_token_prefix']['registration_completed_in_model'] is True
 assert o['control_error']['exact_type'] is None and o['control_error']['exact_value_bytes'] is None and o['control_error']['producer_history']=='UNAVAILABLE'
 assert o['prior_failure_storage_history'].startswith('UNKNOWN;')
 return True
def outcomes_mutation(x,fn):
 q=D(x);fn(q['outcomes']);q['projection']['outcomes']=D(q['outcomes']);return q
