import copy
ORDER=['callback-handler-enter','callback-none-guard','callback-bare-rethrow','finally-enter','removal-attempt','removal-complete']
def normal(m,basis,idx=0,invocation='constructed-client-construction-A',control=False,continuity=True,terminal=None,cleanup_terminal=None):
 sb=basis['stored_basis'];tm=sb['routes']['token_module'];tb=sb['token_basis'];factory=m.module(tb['fresh']['root']/'tests/cases.py','_token_case_factory');tc=factory.normal(tm,tb,idx,control=control,continuity=continuity,invocation=invocation,owner_none=True,terminal=('client-create','raise'));prefix=tc['output'];steps=[];cursor=0
 while cursor<len(ORDER):
  stage=ORDER[cursor];t=terminal if cursor<3 or cleanup_terminal is None else cleanup_terminal
  kind=t[1] if t and t[0]==stage else ('reraised-construction' if stage=='callback-bare-rethrow' else 'normal');steps.append({'stage':stage,'outcome':kind})
  if kind in ('process-termination','unobserved') or (kind=='raise' and cursor>=3):break
  if kind=='raise':cursor=3;continue
  cursor+=1
 cat=basis['catalogue'];scope=prefix['scope'];refs=prefix['reference_bindings'];source=cat['source']
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':source['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(source['guard']),'source':copy.deepcopy(source['sources']['entry']),'premise':source['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 case={'kind':'CONSTRUCTED-CLIENT-CONSTRUCTION-NONE','context':tc['context'],'anchor':copy.deepcopy(tc['anchor']),'invocation':invocation,'token_case':tc,'construction_error':basis['fresh']['coverage'].client_construction_binding(cat,scope,control),'none_guard_binding':binding,'outcomes':steps,'projection':{},'output':{}}
 return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].client_construction_projection(basis['catalogue'],case['projection'],v);return case
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
def oracle(out,control,terminal=None,cleanup_terminal=None):
 assert out['construction_expression_raised_in_model'] is True and out['construction_completed_in_model'] is False and out['client_callback_executed_in_model'] is False
 assert out['earlier_control_construction_completed_in_model'] is (True if control else None) and out['earlier_control_callback_completed_in_model'] is (True if control else None)
 assert out['allocation_progress'] is out['initializer_progress'] is out['completed_client_object_reference'] is None
 assert out['new_explicit_cause_assignment_established_in_model'] is False and out['exception_chain_observation']['existing_cause']=='UNKNOWN' and out['exception_chain_observation']['existing_context']=='UNKNOWN'
 assert out['construction_reaches_launcher_established'] is False and out['runtime_observation'] is False and out['outer_cleanup_completion'] is None
 reached=[];done=[];evaluation=False;stopped=None;cursor=0
 while cursor<6:
  stage=ORDER[cursor];t=terminal if cursor<3 or cleanup_terminal is None else cleanup_terminal;kind=t[1] if t and t[0]==stage else ('reraised-construction' if cursor==2 else 'normal');reached.append(stage)
  if kind in ('process-termination','unobserved'):stopped=kind;break
  if kind=='raise':
   if cursor<3:evaluation=True;cursor=3;continue
   stopped='cleanup';break
  done.append(stage);cursor+=1
 assert [r['stage'] for r in out['events']]==reached
 assert out['handler_entry_completed_in_model']==('callback-handler-enter' in done)
 assert out['none_guard_completed_in_model']==('callback-none-guard' in done)
 assert out['bare_rethrow_effect_established_in_model']==('callback-bare-rethrow' in done)
 assert out['removal_completed_in_model']==('removal-complete' in done)
 assert (out['handler_evaluation_error_in_model'] is not None)==evaluation
 assert (out['cleanup_error_in_model'] is not None)==(stopped=='cleanup')
 if stopped in ('process-termination','unobserved'):assert out['terminal_python_exception_in_model'] is None and out['outward_error_after_finally_in_model'] is None
 if out['handler_entry_completed_in_model']:assert out['caught_error_in_model']==out['construction_error'] and out['caught_name_in_model']=='client_error'
 if out['bare_rethrow_effect_established_in_model']:assert out['reraised_error_in_model']==out['construction_error']
 if out['removal_completed_in_model']:
  assert out['outward_error_after_finally_in_model']==(out['handler_evaluation_error_in_model'] if evaluation else out['construction_error'])
 return True
