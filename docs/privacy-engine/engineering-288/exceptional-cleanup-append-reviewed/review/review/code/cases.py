"""Independent cases from defining source. Engineering's new factory is unused.
The inherited independent parent factory is reused, not counted as a new review.
Producer-generated submitted output is never the independent oracle.
"""
from common import *
import parent_details
ORDER=['loop-input-evaluation','input-raw-name','input-raw-object','input-raw-pair','input-managed-name','input-managed-object','input-managed-pair','loop-inputs-complete','loop-iterator-attempt','raw-item-next','raw-bind-name','raw-bind-obj','raw-guard-object','raw-guard-none','raw-guard-result','managed-item-next','managed-bind-name','managed-bind-obj','managed-guard-object','managed-guard-none','managed-guard-result','selected-try-entry','close-object-evaluation','close-method-evaluation','close-call-attempt','close-normal-return','append-details-evaluation','append-key-evaluation','append-list-resolution','append-method-evaluation','append-item-name','append-item-message','append-item-complete','append-call-attempt','append-complete']
def close_scope(anchor,invocation):
 return {'acquisition':anchor['record']['acquisition'],'instance':'validated-instance:'+hashlib.sha256((json.dumps(anchor['instance'],sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()).hexdigest(),'invocation':invocation+'/exceptional-managed-close'}
def close_result(b,cc):
 if cc is None:return None
 d=b['inner'];g=d['guards'];return b['fresh']['coverage'].constructed_reference_path(d['manager'],g['guard_relationships'],g['guard_oracle'],cc)
def build(m,b,idx,control=False,terminal=None,continuity='explicit conditional premise',close_kind='normal',invocation=None,initial=None):
 invocation=invocation or 'fl6-exceptional-cleanup-'+str(idx)+'-'+str(int(control))
 p=b['prior_module'];pb=b['prior_basis'];pc=parent_details.make(p,pb,idx,control=control,invocation=invocation);po=p._construct_checked(pb,pc)['projection'];anchor=pc['anchor'];refs=po['delivery_binding']['references'];src=b['catalogue']['source']
 # Bind the role explicitly. Catalogue coordinates were independently source-checked.
 bind={'scope':D(po['scope']),'instance_anchor':D(anchor),'selected_error':D(po['earlier_constructor_exception']),'references':D(refs),'ordered_values':[{'name':'raw','value':None,'exact_type':'NoneType'},{'name':'managed','value':D(refs['manager']),'meaning':'source-qualified manager reference, not an observed Python object'}],'selected_index':1,'name':'managed','object':D(refs['manager']),'guard':{'expression':'obj is not None','left':D(refs['manager']),'right':None,'right_exact_type':'NoneType','result':True},'close_receiver':D(refs['manager']),'method':'close','method_origin':D(src['manager_close']),'cleanup_list':D(po['details_in_model']['cleanup_reference']),'append_item':['managed','close returned'],'continuity':continuity,'premise':src['continuity_premise'],'runtime_object_identity':None}
 if continuity=='UNESTABLISHED':terminal=(ORDER[0],'unobserved')
 rows=[]
 for stage in ORDER:
  outcome=terminal[1] if terminal and stage==terminal[0] else 'normal';rows.append({'stage':stage,'outcome':outcome})
  if outcome!='normal':break
 cc=None;hit=next((x for x in rows if x['stage']=='close-normal-return'),None)
 if hit and (hit['outcome'] in ('normal','raise') or close_kind=='partial-prefix'):
  cc={'kind':'CONSTRUCTED-REFERENCE-PATH','context':pc['context'],'scope':close_scope(anchor,invocation),'method':'close','initial':initial or {'_live':'constructed-connection-A','_retired':None,'_phase':'READY'},'facts':{},'outcomes':{},'stop_after':None}
  if close_kind!='normal':
   normal=close_result(b,cc)
   calls=[e for e in normal['events'] if e.get('kind')=='call:self._retired.close']
   assert len(calls)==1
   cc['outcomes'][calls[0]['address']]='raise' if close_kind=='abrupt' else 'stop'
 cr=close_result(b,cc)
 v={'scope':D(po['scope']),'anchor':D(anchor),'parent_result':D(po),'binding':D(bind),'close_result':D(cr),'outcomes':D(rows)}
 q={'kind':'CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','context':pc['context'],'anchor':D(anchor),'invocation':invocation,'parent_case':pc,'parent_output':po,'binding':bind,'close_case':cc,'outcomes':rows,'projection':v,'output':{}}
 q['output']=b['fresh']['coverage'].cleanup_append_projection(b['catalogue'],v,D(v));return q
def refresh_projection(b,q):
 """For deliberately coordinated mutants; does not authenticate changed fields."""
 v={'scope':D(q['parent_output']['scope']),'anchor':D(q['anchor']),'parent_result':D(q['parent_output']),'binding':D(q['binding']),'close_result':close_result(b,q['close_case']),'outcomes':D(q['outcomes'])};q['projection']=v
 q['output']=b['fresh']['coverage'].cleanup_append_projection(b['catalogue'],v,D(v));return q
def oracle(q,result,known_terminal_defect=False):
 o=result['projection'];po=q['parent_output'];steps=q['outcomes'];done={e['stage'] for e in steps if e['outcome']=='normal'};seen={e['stage'] for e in steps};last=steps[-1]['outcome'];stage=steps[-1]['stage'];error=po['earlier_constructor_exception'];appended=ORDER[-1] in done;closed='close-normal-return' in done
 assert [e['stage'] for e in o['events']]==[e['stage'] for e in steps] and [e['outcome'] for e in o['events']]==[e['outcome'] for e in steps]
 assert o['validated_parent']==po and o['binding']==q['binding'] and o['earlier_constructor_exception']==error
 assert po['last_pending_error_in_model']==po['active_caught_error_in_model']==error and po['terminal_python_exception_in_model'] is True
 assert o['earlier_control_completed_in_model']==po['earlier_control_completed_in_model'] and o['selected_owner_continuity']==po['selected_owner_continuity']
 for field,s in [('raw_guard_false_completed_in_model','raw-guard-result'),('selected_name_bound_in_model','managed-bind-name'),('selected_object_bound_in_model','managed-bind-obj'),('selected_non_none_guard_completed_in_model','managed-guard-result'),('close_method_evaluation_completed_in_model','close-method-evaluation'),('close_normal_return_completed_in_model','close-normal-return'),('append_completed_in_model','append-complete')]:assert o[field] is (s in done),field
 for field,s in [('close_attempt_entered_in_model','close-call-attempt'),('append_evaluation_entered_in_model','append-details-evaluation'),('append_attempt_entered_in_model','append-call-attempt')]:assert o[field] is (s in seen),field
 assert o['managed_close_relation']==q['projection']['close_result']
 expected=D(po['details_in_model'])
 if appended:expected['known_literal_fields']['cleanup'].append(['managed','close returned'])
 assert o['details_after_acknowledged_steps']==expected
 assert expected['known_literal_fields']['nonexecution_established'] is False and expected['known_literal_fields']['new_authorization'] is False
 assert all(f['exact_value'] is f['exact_type'] is f['formatted_bytes'] is None and f['selected_error']==error for f in expected['dynamic_fields'])
 repl=o['replacement_error_in_model'];assert (repl is not None)==(last=='raise');assert o['last_pending_error_in_model']==(repl or error)
 if repl:
  region='protected-append' if stage.startswith('append-') else 'protected-close' if stage.startswith('close-') else 'try-entry' if stage=='selected-try-entry' else 'loop-selection'
  assert repl['failure_region']==region and repl['eligible_inner_handler']==('close_error' if region in ('protected-close','protected-append') else None)
  assert repl['handler_entry_established'] is False and repl['exact_type'] is repl['exact_value_bytes'] is None
  assert all(repl[k]=='UNKNOWN' for k in ('existing_cause','existing_context','existing_suppression'))
 expected_terminal=None if last in ('unobserved','process-termination') else True
 if known_terminal_defect and appended:assert o['terminal_python_exception_in_model'] is False
 else:assert o['terminal_python_exception_in_model'] is expected_terminal
 cr=q['projection']['close_result'];assert o['close_itself_failed_established_in_model'] is (cr is not None and cr['completion']=='abrupt')
 if stage.startswith('append-'):assert closed and o['close_itself_failed_established_in_model'] is False
 if 'append-call-attempt' in seen and not appended:assert o['cleanup_list_after_frontier']=='UNKNOWN partial effects'
 for f in ('inner_handler_entry_established','error_report_append_expanded','later_iteration_established','loop_completion_established','failure_file_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','ACTIVE_unlink_established','runtime_observation','physical_closure_established','durability_established','released_ownership_established','complete_cleanup_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission'):assert o[f] is False,f
 for f in ('close_return_value_observed','runtime_cleanup_append_chain','physical_reference_identity','observer_join'):assert o[f] is None,f
 for e in o['events']:assert e['scope']==q['projection']['scope'] and e['selected_object']==q['binding']['object'] and e['selected_error']==error and e['runtime_frame'] is None
 return True
