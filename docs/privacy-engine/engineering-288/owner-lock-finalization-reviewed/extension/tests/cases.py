import copy

def normal(m,basis,idx=0,invocation='constructed-finalizer-A',continuity=True,terminal=None,exit_terminal=None,marker='UNKNOWN'):
 p=basis['fresh']['prior_module'];factory=m.module(basis['fresh']['prior_root']/'tests/cases.py','_owner_exit_cases');ec=factory.normal(p,basis['exit_basis'],idx,continuity=continuity,invocation=invocation,terminal=exit_terminal,marker=marker)
 outcomes=[]
 if ec['output']['completion']=='normal-marker-unlink-completion':
  for stage in basis['catalogue']['source']['order']:
   kind=terminal[1] if terminal and terminal[0]==stage else 'normal';outcomes.append({'stage':stage,'outcome':kind})
   if kind!='normal':break
 case={'kind':'CONSTRUCTED-OWNER-LOCK-FINALIZATION','context':ec['context'],'anchor':copy.deepcopy(ec['anchor']),'invocation':invocation,'exit_case':ec,'outcomes':outcomes,'projection':{},'output':{}};return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].owner_finalization_projection(basis['catalogue'],case['projection'],v);return case
def change(value,path,new):
 value=copy.deepcopy(value);p=value
 for k in path[:-1]:p=p[k]
 p[path[-1]]=new;return value
