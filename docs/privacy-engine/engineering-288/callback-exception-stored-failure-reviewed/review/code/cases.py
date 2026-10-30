from common import *
ORDER=['callback-handler-enter','callback-failure-guard','callback-stored-rethrow','finally-enter','removal-attempt','removal-complete']
def token_case(m,b,idx,inv,control=True,continuity=True):
 row=b['prior']['contexts'][idx]['token_registration_correspondence'];anchor=D(row['instance_anchor']);sb=b['stored_basis'];tb=sb['token_basis'];tm=sb['routes']['token_module'];scope=tm.invocation_scope(anchor,inv);c=tb['fresh']['coverage']
 stages=['owner-create','token-create','registry-insert','control-guard']+(['control-create','control-callback'] if control else [])+['client-create','client-callback']
 v={'occurrence':inv,'scope':scope,'control_present':control,'owner_failure_none':False,'registry_continuity':continuity,'outcomes':[{'stage':s,'outcome':'raise' if s=='client-callback' else 'normal'} for s in stages]}
 p={**D(v),'references':c.token_reference_premises(scope,control)};o=c.token_registration_projection(tb['catalogue'],p,v)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':anchor,'invocation':inv,'control_present':control,'owner_failure_none':False,'registry_continuity':continuity,'outcomes':D(v['outcomes']),'projection':p,'output':o}
def normal(m,b,idx,route='handle',inv=None,control=True,continuity=True,helper='normal',terminal=None):
 inv=inv or 'FL6-callback-'+str(idx)+'-'+route;tc=token_case(m,b,idx,inv,control,continuity);bindings=m.failure_inputs(b,tc['context'],inv,tc['output']);row=b['prior']['contexts'][idx];c=b['fresh']['coverage'];scope=bindings[route+'_scope']
 p={'occurrence':inv+'/client-operation','scope':D(scope),'references':D(bindings[route+'_references']),'outcomes':{'client-call':'normal','owner-lookup':'normal','owner-guard':'normal'},'manager_case':None,'callback':'raises','cleanup':dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')}
 if route=='handle':p['packet']={'type':'str','value':'FL6 source-TypeError fixture'};p['outcomes']['packet-check']='normal'
 else:p['detachment']=None;p['outcomes'].update({'operation-check':'normal','session-call':'raise'})
 p['outcomes'].update({'retain-error':'normal','fixed-failure':helper});cat=row['client_'+route+'_return_correspondence']['declaration']
 failure=c.client_handle_projection(cat,b['verification'],p,D(p)) if route=='handle' else c.client_state_projection(cat,p,{'scope':scope,'state':row['client_state_return_correspondence']['validated_state_anchor']['validated_state']})
 path=ORDER[:]
 if terminal and terminal[1]=='raise' and terminal[0] in ORDER[:3]:path=ORDER[:ORDER.index(terminal[0])+1]+ORDER[3:]
 elif terminal and terminal[1] in ('raise','process-termination','unobserved'):path=ORDER[:ORDER.index(terminal[0])+1]
 outcomes=[{'stage':s,'outcome':terminal[1] if terminal and terminal[0]==s else 'raised-stored-from-client' if s=='callback-stored-rethrow' else 'normal'} for s in path]
 x={'kind':'CONSTRUCTED-CALLBACK-STORED-FAILURE','context':tc['context'],'anchor':D(tc['anchor']),'invocation':inv,'token_case':tc,'failure_route':route,'failure_input':p,'failure_result':failure,'callback_error':c.callback_error_binding(b['catalogue'],tc['output']['scope']),'outcomes':outcomes,'projection':{},'output':{}}
 return refresh(m,b,x)
def refresh(m,b,x):
 x['projection']=m._premises(b,x);x['output']=b['fresh']['coverage'].callback_failure_projection(b['catalogue'],D(x['projection']),D(x['projection']));return x

def independently_check(x):
 out=x['output'];ev=x['outcomes'];ack={v['stage'] for v in ev if v['outcome'] in ('normal','raised-stored-from-client')};cause='callback-stored-rethrow' in ack;pop='removal-complete' in ack;orig=x['failure_result']['original_exception'];client=x['callback_error'];last=ev[-1]
 assert out['failure_storage_previously_completed_in_model'] is True
 assert out['callback_returned_normally_in_model'] is False and out['callback_raised_in_model'] is True and out['run_success_established'] is False
 for field,stage in [('callback_handler_entry_completed_in_model',ORDER[0]),('non_none_guard_completed_in_model',ORDER[1]),('source_stored_rethrow_with_cause_completed_in_model',ORDER[2]),('finally_entry_completed_in_model',ORDER[3]),('removal_attempt_entered_in_model',ORDER[4]),('removal_completed_in_model',ORDER[5])]:assert out[field]==(stage in ack),(field,out[field])
 assert out['original_error']==orig and out['callback_error']==client
 if cause:
  rel=out['established_explicit_cause'];assert rel['raised_error']==orig and rel['explicit_cause']==client and rel['suppress_context_in_model'] is True and rel['implicit_context_observation'] is None and rel['physical_identity_relative_to_stored']=='UNKNOWN'
 else:assert out['established_explicit_cause'] is None
 errors=[v for v in ev if v['outcome']=='raise'];pre=[v for v in errors if v['stage'] in ORDER[:3]];clean=[v for v in errors if v['stage'] in ORDER[3:]]
 assert (out['handler_evaluation_error_in_model'] is not None)==bool(pre)
 assert (out['cleanup_error_in_model'] is not None)==bool(clean)
 if clean:assert out['last_pending_error_in_model']==out['cleanup_error_in_model'] and out['last_pending_error_in_model']!=orig
 elif pre:assert out['last_pending_error_in_model']==out['handler_evaluation_error_in_model'] and not cause
 elif cause:assert out['last_pending_error_in_model']==orig
 else:assert out['last_pending_error_in_model']==client
 assert out['outward_error_after_finally_in_model']==(out['last_pending_error_in_model'] if pop else None)
 assert out['original_outward_after_finally_established_in_model']==(pop and cause)
 assert out['selected_owner_removed_in_model'] is (True if pop and x['token_case']['registry_continuity'] else None)
 assert out['slot_after_pop_in_model']==('ABSENT-AT-POP-COMPLETION' if pop else 'UNKNOWN')
 assert out['terminal_python_exception_in_model'] is (None if last['outcome'] in ('unobserved','process-termination') else True)
 for k in ('original_reaches_launcher_established','physical_lock_release_established','exclusive_ownership_established','durability_established','runtime_observation','actual_admission','authorization_renewed','obligations_discharged'):assert out[k] is False
 for k in ('observer_join','runtime_callback_cause_revocation_chain','database_cleanup_completion','outer_cleanup_completion','retained_failure_record_bytes','physical_reference_identity','revocation_persists','pop_result_observation','implicit_context_observation'):assert out[k] is None
 assert out['callback_error']['producer_history']=='UNAVAILABLE' and out['callback_error']['exact_type'] is None and out['callback_error']['exact_value_bytes'] is None
 return True
