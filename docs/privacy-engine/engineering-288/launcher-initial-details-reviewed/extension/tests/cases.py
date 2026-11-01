"""Constructed cases only; none of these values are runtime observations."""
import copy,ast
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
def outcomes(cat,terminal=None):
 out=[]
 for stage in cat['source']['order']:
  kind=terminal[1] if terminal and terminal[0]==stage else 'normal';out.append({'stage':stage,'outcome':kind})
  if kind!='normal':break
 return out
def producer_case(c,cat,parent,anchor,terminal=None,continuity='explicit conditional premise'):
 if continuity=='UNESTABLISHED':terminal=(cat['source']['order'][0],'unobserved')
 v={'scope':copy.deepcopy(parent['scope']),'anchor':copy.deepcopy(anchor),'parent_result':copy.deepcopy(parent),'delivery_binding':c.launcher_delivery_binding(cat,parent,anchor,continuity),'outcomes':outcomes(cat,terminal)}
 return v,c.launcher_details_projection(cat,v,v)
def normal(m,basis,idx=0,control=False,invocation='constructed-launcher-details-A',terminal=None,continuity='explicit conditional premise',owner_continuity=True,parent_terminal=None):
 p=basis['prior_module'];pb=basis['prior_basis'];factory=m.module(pb['fresh']['root']/'tests/cases.py','_client_construction_cases')
 parent_case=factory.normal(p,pb,idx,control=control,invocation=invocation,continuity=owner_continuity,terminal=parent_terminal)
 parent=p._construct_checked(pb,parent_case)['projection'];c=basis['fresh']['coverage'];cat=basis['catalogue']
 v,out=producer_case(c,cat,parent,parent_case['anchor'],terminal,continuity)
 return {'kind':'CONSTRUCTED-LAUNCHER-INITIAL-DETAILS','context':parent_case['context'],'anchor':copy.deepcopy(parent_case['anchor']),'invocation':invocation,'parent_case':parent_case,'parent_output':parent,'delivery_binding':copy.deepcopy(v['delivery_binding']),'outcomes':copy.deepcopy(v['outcomes']),'projection':v,'output':out}
def oracle(out,source,control,terminal=None):
 order=source['order'];end=order.index(terminal[0]) if terminal else len(order)-1;completed=order[:end] if terminal else order
 assert [e['stage'] for e in out['events']]==order[:end+1]
 assert out['earlier_control_completed_in_model'] is (True if control else None)
 assert out['handler_entry_completed_in_model']==('launcher-handler-entry' in completed)
 assert out['details_assignment_completed_in_model']==('details-assignment-complete' in completed)
 assert out['details_evaluation_attempt_in_model']==('details-evaluation-attempt' in completed)
 assert out['details_assignment_attempt_in_model']==('details-assignment-attempt' in completed)
 assert out['details_dictionary_completed_in_model']==('details-dict-completion' in completed)
 if out['details_assignment_completed_in_model']:
  d=out['details_in_model'];assert d['known_literal_fields']=={'nonexecution_established':False,'new_authorization':False,'cleanup':[]}
  assert [x['name'] for x in d['dynamic_fields']]==['error','message','traceback']
  assert all(x['exact_value'] is x['exact_type'] is x['formatted_bytes'] is None and x['selected_error']==out['earlier_constructor_exception'] for x in d['dynamic_fields'])
 else:assert out['details_in_model'] is None
 assert out['runtime_handler_arrival'] is None and out['runtime_observation'] is False
 assert not any(out[k] for k in ('cleanup_loop_entered','normal_managed_close_spliced','managed_clear_spliced','ACTIVE_unlink_spliced','failure_file_established','outward_propagation_established','physical_closure_established','authorization_renewed','actual_admission'))
 assert out['retained_failure_record_bytes'] is None
 if terminal:
  assert (out['replacement_error_in_model'] is not None)==(terminal[1]=='raise')
  if terminal[1] in ('unobserved','process-termination'):assert out['terminal_python_exception_in_model'] is None
 return True
