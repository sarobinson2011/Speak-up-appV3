import copy

def forward_result(m,basis,case,token):
 p=case['failure_input'];row=m._selected(basis,case['context']);c=basis['fresh']['coverage'];route=case['failure_route'];cat=row['client_'+route+'_return_correspondence']['declaration']
 if route=='state':return c.client_state_projection(cat,p,{'scope':p['scope'],'state':row['client_state_return_correspondence']['validated_state_anchor']['validated_state']})
 return c.client_handle_projection(cat,basis['verification'],p,copy.deepcopy(p))
def normal(m,basis,idx=0,route='handle',invocation='constructed-stored-A',control=True,continuity=True,terminal=None,origin=None):
 tm=basis['routes']['token_module'];tb=basis['token_basis'];factory=m.module(tb['fresh']['root']/'tests/cases.py','_stored_token_factory');tc=factory.normal(tm,tb,idx,control=control,continuity=continuity,invocation=invocation,owner_none=False);token=tc['output'];b=m.failure_inputs(basis,tc['context'],invocation,token)
 p={'occurrence':b['child'],'scope':copy.deepcopy(b[route+'_scope']),'references':copy.deepcopy(b[route+'_references']),'outcomes':{'client-call':'normal','owner-lookup':'normal','owner-guard':'normal'},'manager_case':None,'callback':'returns','cleanup':dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')}
 if route=='handle':
  p['packet']={'type':'str','value':'constructed invalid packet'};p['outcomes']['packet-check']='normal'
  if origin=='session-call':p['packet']={'type':'bytes','value':{'bytes_hex':''}};p['outcomes']['session-call']='raise'
 else:p['detachment']=None;p['outcomes'].update({'operation-check':'normal','session-call':'raise'})
 p['outcomes'].update({'retain-error':'normal','fixed-failure':'normal'})
 outcomes=[]
 for i,stage in enumerate(basis['catalogue']['source']['order']):
  result=terminal[1] if terminal and stage==terminal[0] else 'raised-original' if i==0 else 'normal';outcomes.append({'stage':stage,'outcome':result})
  if result in ('process-termination','unobserved') or result=='raise' and i>0:break
 case={'kind':'CONSTRUCTED-STORED-FAILURE-REVOCATION','context':tc['context'],'anchor':copy.deepcopy(tc['anchor']),'invocation':invocation,'token_case':tc,'failure_route':route,'failure_input':p,'failure_result':None,'outcomes':outcomes,'projection':{},'output':{}}
 case['failure_result']=forward_result(m,basis,case,token);return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].stored_failure_projection(basis['catalogue'],case['projection'],v);return case
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
