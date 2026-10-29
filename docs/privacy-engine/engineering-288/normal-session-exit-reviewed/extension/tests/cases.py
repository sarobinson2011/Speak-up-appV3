import copy

def normal(m,basis,idx=0,continuity=True,invocation='constructed-exit-A',terminal=None,marker='UNKNOWN',phase='READY',live='connection-A',retired=None,token_terminal=None,close_outcomes=None):
 p=basis['fresh']['prior_module'];root=basis['fresh']['prior_root'];factory=m.module(root/'tests/cases.py','_exit_token_fixtures')
 tc=factory.normal(p,basis['token_basis'],idx,continuity=continuity,invocation=invocation,terminal=token_terminal);anchor=tc['anchor'];outcomes=[]
 if tc['output']['completion']=='normal-pop-completion':
  for stage in basis['catalogue']['source']['order']:
   kind=terminal[1] if terminal and stage==terminal[0] else 'normal';outcomes.append({'stage':stage,'outcome':kind})
   if kind!='normal':break
 reached=next((r for r in outcomes if r['stage']=='close-complete'),None)
 cc={'kind':'CONSTRUCTED-REFERENCE-PATH','context':tc['context'],'scope':m.close_scope(anchor,invocation),'method':'close','initial':{'_live':live,'_retired':retired,'_phase':phase},'facts':{},'outcomes':close_outcomes or {},'stop_after':None} if reached else None
 if reached and reached['outcome'] in ('unobserved','process-termination'):cc=None
 case={'kind':'CONSTRUCTED-NORMAL-SESSION-EXIT','context':tc['context'],'anchor':copy.deepcopy(anchor),'invocation':invocation,'token_case':tc,'close_case':cc,'outcomes':outcomes,'marker_at_unlink':marker,'projection':{},'output':{}}
 refresh(m,basis,case);return case

def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].session_exit_projection(basis['catalogue'],case['projection'],v);return case

def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
