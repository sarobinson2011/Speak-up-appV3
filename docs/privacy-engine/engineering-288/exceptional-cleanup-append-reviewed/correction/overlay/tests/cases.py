import copy
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
def outcomes(cat,terminal=None,continuity='explicit conditional premise'):
 if continuity=='UNESTABLISHED':return [{'stage':cat['source']['order'][0],'outcome':'unobserved'}]
 rows=[]
 for stage in cat['source']['order']:
  kind=terminal[1] if terminal and terminal[0]==stage else 'normal';rows.append({'stage':stage,'outcome':kind})
  if kind!='normal':break
 return rows
def normal(m,basis,idx=0,control=False,invocation='constructed-cleanup-A',terminal=None,continuity='explicit conditional premise',phase='READY',live='connection-A',retired=None,close_outcomes=None):
 p=basis['prior_module'];pb=basis['prior_basis'];factory=m.module(pb['fresh']['root']/'tests/cases.py','_details_cases')
 pc=factory.normal(p,pb,idx,control=control,invocation=invocation);po=p._construct_checked(pb,pc)['projection'];cat=basis['catalogue'];c=basis['fresh']['coverage'];o=outcomes(cat,terminal,continuity);binding=c.cleanup_append_binding(cat,po,pc['anchor'],continuity)
 hit=next((x for x in o if x['stage']=='close-normal-return'),None)
 cc={'kind':'CONSTRUCTED-REFERENCE-PATH','context':pc['context'],'scope':m.close_scope(pc['anchor'],invocation),'method':'close','initial':{'_live':live,'_retired':retired,'_phase':phase},'facts':{},'outcomes':close_outcomes or {},'stop_after':None} if hit and hit['outcome'] not in ('unobserved','process-termination') else None
 case={'kind':'CONSTRUCTED-EXCEPTIONAL-CLEANUP-APPEND','context':pc['context'],'anchor':copy.deepcopy(pc['anchor']),'invocation':invocation,'parent_case':pc,'parent_output':po,'binding':binding,'close_case':cc,'outcomes':o,'projection':{},'output':{}}
 return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].cleanup_append_projection(basis['catalogue'],v,v);return case
def oracle(out,source,control,terminal=None):
 order=source['order'];end=order.index(terminal[0]) if terminal else len(order)-1;done=set(order[:end] if terminal else order)
 assert [e['stage'] for e in out['events']]==order[:end+1]
 assert out['earlier_control_completed_in_model'] is (True if control else None)
 assert out['close_normal_return_completed_in_model']==('close-normal-return' in done)
 assert out['append_completed_in_model']==('append-complete' in done)
 assert out['details_after_acknowledged_steps']['dynamic_fields']==out['validated_parent']['details_in_model']['dynamic_fields']
 known=out['details_after_acknowledged_steps']['known_literal_fields'];assert known['nonexecution_established'] is known['new_authorization'] is False
 assert known['cleanup']==([['managed','close returned']] if 'append-complete' in done else [])
 assert out['details_after_acknowledged_steps']['cleanup_reference']==out['validated_parent']['details_in_model']['cleanup_reference']
 assert all(out[k] is False for k in ('runtime_observation','inner_handler_entry_established','error_report_append_expanded','later_iteration_established','loop_completion_established','failure_file_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','ACTIVE_unlink_established','physical_closure_established','released_ownership_established','durability_established','complete_cleanup_established','authorization_renewed','actual_admission'))
 # EC-01: lab_bootstrap.py:167-171 remains in the constructor-error handler.
 # A normal cleanup append does not establish normal overall return.
 if terminal is None:assert out['terminal_python_exception_in_model'] is True
 if terminal:
  assert (out['replacement_error_in_model'] is not None)==(terminal[1]=='raise')
  if terminal[1]=='raise':
   region=source['stages'][terminal[0]]['semantic_region'];assert out['replacement_error_in_model']['failure_region']==region
   assert out['replacement_error_in_model']['eligible_inner_handler']==('close_error' if region in ('protected-close','protected-append') else None)
   if region=='protected-append':assert out['close_normal_return_completed_in_model'] and not out['close_itself_failed_established_in_model']
  else:assert out['terminal_python_exception_in_model'] is None
 return True
