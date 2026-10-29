"""Reviewer source oracle; no application code execution or candidate helpers."""
import ast,copy,hashlib

def source_oracle(raw):
 tree=ast.parse(raw);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');parents={child:node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
 def one(kind,predicate):
  hits=[n for n in ast.walk(run) if isinstance(n,kind) and predicate(n)];assert len(hits)==1;return hits[0]
 owner=one(ast.Assign,lambda n:any(isinstance(t,ast.Name) and t.id=='owner' for t in n.targets));token=one(ast.Assign,lambda n:any(isinstance(t,ast.Name) and t.id=='token' for t in n.targets));store=one(ast.Assign,lambda n:any(isinstance(t,ast.Subscript) and ast.unparse(t.value)=='_OWNERS' for t in n.targets))
 assert ast.unparse(owner)=='owner = _Owner(wrapper)' and ast.unparse(token)=='token = object()' and ast.unparse(store)=='_OWNERS[token] = owner'
 with_=parents[owner];assert isinstance(with_,ast.With) and parents[token] is with_ and parents[store] is with_
 assert list(with_.body[:3])==[owner,token,store]
 control=one(ast.Call,lambda n:ast.unparse(n.func)=='control');client=one(ast.Call,lambda n:ast.unparse(n.func)=='client');pop=one(ast.Call,lambda n:ast.unparse(n.func)=='_OWNERS.pop')
 assert ast.unparse(control)=='control(_Control(token))' and ast.unparse(client)=='client(Client(token))' and ast.unparse(pop)=='_OWNERS.pop(token, None)'
 controlstmt=parents[control];controlif=parents[controlstmt];clientstmt=parents[client];clienttry=parents[clientstmt];popstmt=parents[pop];protected=parents[popstmt]
 assert isinstance(controlif,ast.If) and ast.unparse(controlif.test)=='control is not None' and not controlif.orelse
 assert isinstance(protected,ast.Try) and protected.finalbody==[popstmt] and protected.handlers==[] and parents[protected] is with_
 assert isinstance(clienttry,ast.Try) and parents[clienttry] is protected and parents[controlif] is protected
 normalguard=[n for n in protected.body if isinstance(n,ast.If) and ast.unparse(n.test)=='owner.failure is not None'];assert len(normalguard)==1;failure=normalguard[0]
 assert protected.body==[controlif,clienttry,failure] and ast.unparse(failure.body[0])=='raise owner.failure' and isinstance(popstmt,ast.Expr)
 assert isinstance(clientstmt,ast.Expr) and isinstance(controlstmt,ast.Expr) and not any(isinstance(n,ast.Return) for n in ast.walk(run))
 globals_=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_OWNERS' for t in n.targets)];assert len(globals_)==1 and isinstance(globals_[0].value,ast.Dict) and not globals_[0].value.keys
 for cls,attr,arg in [('_Owner','wrapper','wrapper'),('Client','__token','token'),('_Control','__token','token')]:
  class_=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls);init=next(n for n in class_.body if isinstance(n,ast.FunctionDef) and n.name=='__init__');assert ast.unparse(init.body[0])==f'self.{attr} = {arg}'
 mapping=[('owner-create',owner),('token-create',token),('registry-insert',store),('control-guard',controlif.test),('control-create',control.args[0]),('control-callback',controlstmt),('client-create',client.args[0]),('client-callback',clientstmt),('owner-failure-guard',failure.test),('finally-enter',protected),('removal-attempt',pop),('removal-complete',popstmt)]
 nodes={n:node for n,node in mapping};sites={n:f'{x.lineno}:{x.col_offset}:{x.end_lineno}:{x.end_col_offset}:{type(x).__name__}' for n,x in mapping}
 return {'order':[n for n,x in mapping],'sites':sites,'expressions':{n:ast.unparse(x) for n,x in mapping},'entry':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'normal_guard':ast.unparse(failure.test),'control_guard':ast.unparse(controlif.test),'registry_initialized_exact_dict':True,'callback_results_discarded':True,'finally_anchor_is_containing_try_not_runtime_observation':True}

def references(scope,control):
 r={k:{'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/'+k+'-symbol'} for k in ['token','owner','session','manager','client']}
 r['control']={'scope':copy.deepcopy(scope),'symbol':scope['invocation']+'/control-symbol'} if control else None
 for a,b in [('client.token','token'),('owners[token]','owner'),('owner.wrapper','session'),('session.managed','manager')]:r[a]=copy.deepcopy(r[b])
 r['control.token']=copy.deepcopy(r['token']) if control else None
 return r

def make_case(row,oracle,coverage,catalogue,invocation,control=True,continuity=True,owner_none=True,stop=None):
 anchor=copy.deepcopy(row['instance_anchor']);scope={'context':row['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':invocation}
 sequence=[s for s in oracle['order'] if control or s not in ('control-create','control-callback')];outcomes=[]
 for stage in sequence:
  kind=stop[1] if stop and stop[0]==stage else 'normal';outcomes.append({'stage':stage,'outcome':kind})
  if kind!='normal' or stage=='owner-failure-guard' and not owner_none:break
 validated={'occurrence':invocation,'scope':copy.deepcopy(scope),'control_present':control,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':copy.deepcopy(outcomes)}
 projection={**copy.deepcopy(validated),'references':references(scope,control)}
 output=coverage.token_registration_projection(catalogue,projection,validated)
 # Independent state expectations derive from the acknowledged source-ordered prefix.
 completed={r['stage'] for r in outcomes if r['outcome']=='normal'};last=outcomes[-1];popped='removal-complete' in completed
 expected={'registration_completed_in_model':'registry-insert' in completed,'control_callback_completed_in_model':('control-callback' in completed) if control else None,'client_callback_completed_in_model':'client-callback' in completed,'finally_entered_in_model':'finally-enter' in completed,'removal_attempt_entered_in_model':'removal-attempt' in completed,'removal_completed_in_model':popped,'selected_owner_removed_in_model':True if popped and continuity else None,'slot_after_pop_in_model':'ABSENT-AT-POP-COMPLETION' if popped else 'UNKNOWN','revocation_persists':None,'callback_return_destination':None,'pop_return_value':None,'physical_object_identity_observed':False,'runtime_observation':False,'retained_error':None,'database_cleanup_completion':None,'external_nonexecution_established':False,'authorization_renewed':False,'actual_admission':False}
 assert all(output[k] is v if type(v) in (bool,type(None)) else output[k]==v for k,v in expected.items())
 exceptional_frontier=last['stage']=='owner-failure-guard' and not owner_none and last['outcome']=='normal'
 exception=None if last['outcome'] in ('process-termination','unobserved') or exceptional_frontier else last['outcome']=='raise'
 assert output['outcome_classification']['terminal_python_exception_in_model'] is exception
 assert [x['stage'] for x in output['events']]==[x['stage'] for x in outcomes]
 assert all(x['scope']==scope and x['id']==invocation+'/'+x['stage'] and x['frame'] is None for x in output['events'])
 assert output['reference_bindings']==references(scope,control)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':anchor,'invocation':invocation,'control_present':control,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':outcomes,'projection':projection,'output':output},validated,expected
