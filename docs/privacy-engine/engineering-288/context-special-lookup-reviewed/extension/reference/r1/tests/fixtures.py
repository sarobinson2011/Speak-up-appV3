"""Compact SOURCE-CONSTRUCTED fixtures. Never authenticated public basis data.
Anchors are byte-derived from the pinned retained receipt; invocation/error/reference
symbols below are constructed premises, not observations or historical records.
"""
import copy,json
D=copy.deepcopy
EXCLUDED=('open_return_established','file_creation_established','context_manager_entry_established','f_binding_established','encoding_established','file_write_established','file_flush_established','file_fsync_established','context_manager_exit_established','helper_return_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission')
def parent(c,cat,row,prefix,origin):
 scope=D(row['scope']);scope['invocation']='CONSTRUCTED-R1/'+row['context']+'/'+prefix+'/'+origin
 anchor=D(row['anchor']);inv=scope['invocation']
 def role(name):return {'symbol':inv+'/'+name,'scope':D(scope),'runtime_identity':None}
 refs={'owner':role('owner'),'token':role('token')};details=role('details');cleanup=role('cleanup-list');error=role('selected-constructor-error')
 b={'continuity':'explicit conditional premise','references':refs,'details_role':details,'cleanup_list':cleanup,'callable':{'source':D(cat['source']['helper'])}}
 event={'id':inv+'/line174/write:call-attempt','stage':'write:call-attempt','outcome':'attempted','source':D(cat['source']['parent_call']),'scope':D(scope),'owner':D(refs['owner']),'token':D(refs['token'])}
 write={'kind':'CONSTRUCTED-WRITE-CALL-REPLACEMENT','scope':scope,'instance_anchor':anchor,'binding':b,'events':[event],'completion':'write_new-call-attempt','call_attempt_established':True,'replacement_error_in_model':None,'terminal_python_exception_in_model':True,'write_new_body_entry_established':False,'original_error_pending_in_outer_handler':error,'last_pending_error_in_model':D(error),'call_arguments':{'p':{'symbol':inv+'/symbolic-path','concrete_value':None,'runtime_identity':None},'x':D(details)},'exact_path_value':None,
  'retained_cleanup_error_evidence':{'symbol':inv+'/selected-cleanup-error','origin':origin,'runtime_observation':False},'last_acknowledged_inner_caught_error':role('selected-cleanup-error'),'last_acknowledged_active_caught_error_in_model':D(error),'earlier_control_completed_in_model':prefix=='control-normal','selected_owner_continuity':'explicit conditional premise','failure_origin_region':origin,'close_normal_return_completed_in_model':origin=='protected-append','close_itself_failed_established_in_model':origin=='protected-close','managed_close_relation':{'conditional':True,'physical_closure':None},'cleanup_list_state':{'role':D(cleanup),'earlier_partial_append_effects':'UNKNOWN','complete_contents':None},'details_after_predecessor_acknowledged_steps':{'role':D(details),'cleanup':D(cleanup)},'known_false_flags_preserved':True,'dynamic_details_origins_preserved':True}
 hb=c.helper_open_binding(cat,write,anchor,'explicit conditional premise')
 v={'scope':D(scope),'anchor':D(anchor),'parent_result':write,'binding':hb,'outcomes':[{'stage':s['id'],'outcome':s['normal_outcome']} for s in cat['source']['steps']]}
 return c.helper_open_projection(cat,v,v)
def projection_case(c,cat,p,frontier=None,continuity='explicit conditional premise'):
 outcomes=[{'stage':'open-return:continuation','outcome':'normal'},{'stage':'open-return:outcome','outcome':'normal-return'}]
 if frontier:
  stage,outcome=frontier;i=0 if stage=='open-return:continuation' else 1;outcomes=outcomes[:i+1];outcomes[-1]['outcome']=outcome
 b=c.open_return_binding(cat,p,p['instance_anchor'],continuity)
 return {'scope':D(p['scope']),'anchor':D(p['instance_anchor']),'parent_result':D(p),'binding':b,'outcomes':outcomes}
