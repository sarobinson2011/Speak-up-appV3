import copy
ORDER=['callback-handler-enter','callback-failure-guard','callback-stored-rethrow','finally-enter','removal-attempt','removal-complete']
def normal(m,basis,idx=0,route='handle',invocation='constructed-callback-A',control=True,continuity=True,terminal=None,helper='normal',origin=None):
 sb=basis['stored_basis'];tm=sb['routes']['token_module'];tb=sb['token_basis'];factory=m.module(tb['fresh']['root']/'tests/cases.py','_callback_token_factory');tc=factory.normal(tm,tb,idx,control=control,continuity=continuity,invocation=invocation,owner_none=False,terminal=('client-callback','raise'));token=tc['output'];b=m.failure_inputs(basis,tc['context'],invocation,token)
 p={'occurrence':b['child'],'scope':copy.deepcopy(b[route+'_scope']),'references':copy.deepcopy(b[route+'_references']),'outcomes':{'client-call':'normal','owner-lookup':'normal','owner-guard':'normal'},'manager_case':None,'callback':'raises','cleanup':dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')}
 if route=='handle':
  p['packet']={'type':'str','value':'constructed invalid packet'};p['outcomes']['packet-check']='normal'
  if origin=='session-call':p['packet']={'type':'bytes','value':{'bytes_hex':''}};p['outcomes']['session-call']='raise'
 else:p['detachment']=None;p['outcomes'].update({'operation-check':'normal','session-call':'raise'})
 p['outcomes'].update({'retain-error':'normal','fixed-failure':helper})
 steps=[];skip_handler=False
 for i,stage in enumerate(ORDER):
  if skip_handler and i<3:continue
  outcome=terminal[1] if terminal and stage==terminal[0] else 'raised-stored-from-client' if i==2 else 'normal';steps.append({'stage':stage,'outcome':outcome})
  if outcome in ('process-termination','unobserved') or outcome=='raise' and i>=3:break
  if outcome=='raise' and i<3:skip_handler=True
 row=m._selected(basis,tc['context']);c=basis['fresh']['coverage'];cat=row['client_'+route+'_return_correspondence']['declaration']
 result=c.client_state_projection(cat,p,{'scope':p['scope'],'state':row['client_state_return_correspondence']['validated_state_anchor']['validated_state']}) if route=='state' else c.client_handle_projection(cat,basis['verification'],p,copy.deepcopy(p))
 case={'kind':'CONSTRUCTED-CALLBACK-STORED-FAILURE','context':tc['context'],'anchor':copy.deepcopy(tc['anchor']),'invocation':invocation,'token_case':tc,'failure_route':route,'failure_input':p,'failure_result':result,'callback_error':c.callback_error_binding(basis['catalogue'],token['scope']),'outcomes':steps,'projection':{},'output':{}}
 return refresh(m,basis,case)
def refresh(m,basis,case):
 v=m._premises(basis,case);case['projection']=copy.deepcopy(v);case['output']=basis['fresh']['coverage'].callback_failure_projection(basis['catalogue'],case['projection'],v);return case
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
