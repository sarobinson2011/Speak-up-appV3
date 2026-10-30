import copy
ORDER=['callback-handler-enter','callback-none-guard','callback-bare-rethrow','finally-enter','removal-attempt','removal-complete']
def normal(m,basis,idx=0,invocation='constructed-bare-A',control=True,continuity=True,terminal=None):
 sb=basis['stored_basis'];tm=sb['routes']['token_module'];tb=sb['token_basis'];factory=m.module(tb['fresh']['root']/'tests/cases.py','_bare_token_factory');tc=factory.normal(tm,tb,idx,control=control,continuity=continuity,invocation=invocation,owner_none=True,terminal=('client-callback','raise'));token=tc['output'];cat=basis['catalogue'];scope=token['scope'];refs=token['reference_bindings']
 binding={'scope':copy.deepcopy(scope),'owner':copy.deepcopy(refs['owner']),'slot':'owner.failure','slot_value':None,'slot_exact_type':'NoneType','guard_expression':cat['source']['guard_expression'],'guard_result':False,'guard_source':copy.deepcopy(cat['source']['guard']),'source':copy.deepcopy(cat['source']['sources']['entry']),'premise':cat['source']['guard_slot_premise'],'runtime_reference_observation':None,'prior_storage_history':'UNKNOWN; no retained evidence is erased'}
 steps=[];skip=False
 for i,stage in enumerate(ORDER):
  if skip and i<3:continue
  outcome=terminal[1] if terminal and stage==terminal[0] else 'reraised-callback' if i==2 else 'normal';steps.append({'stage':stage,'outcome':outcome})
  if outcome in ('process-termination','unobserved') or outcome=='raise' and i>=3:break
  if outcome=='raise' and i<3:skip=True
 case={'kind':'CONSTRUCTED-CALLBACK-BARE-RETHROW','context':tc['context'],'anchor':copy.deepcopy(tc['anchor']),'invocation':invocation,'token_case':tc,'callback_error':basis['fresh']['coverage'].callback_error_binding(cat,scope),'none_guard_binding':binding,'outcomes':steps,'projection':{},'output':{}}
 return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].callback_bare_projection(basis['catalogue'],case['projection'],v);return case
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
