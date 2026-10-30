import copy
ORDER=['finally-enter','removal-attempt','removal-complete']
def normal(m,basis,idx=0,invocation='constructed-control-A',continuity=True,owner_none=True,terminal=None):
 sb=basis['stored_basis'];tm=sb['routes']['token_module'];tb=sb['token_basis'];factory=m.module(tb['fresh']['root']/'tests/cases.py','_control_token_factory');tc=factory.normal(tm,tb,idx,control=True,continuity=continuity,invocation=invocation,owner_none=owner_none,terminal=('control-callback','raise'));prefix=tc['output'];steps=[]
 for stage in ORDER:
  outcome=terminal[1] if terminal and stage==terminal[0] else 'normal';steps.append({'stage':stage,'outcome':outcome})
  if outcome!='normal':break
 case={'kind':'CONSTRUCTED-CONTROL-EXCEPTION','context':tc['context'],'anchor':copy.deepcopy(tc['anchor']),'invocation':invocation,'token_case':tc,'control_error':basis['fresh']['coverage'].control_exception_binding(basis['catalogue'],prefix['scope']),'outcomes':steps,'projection':{},'output':{}}
 return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].control_exception_projection(basis['catalogue'],case['projection'],v);return case
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
