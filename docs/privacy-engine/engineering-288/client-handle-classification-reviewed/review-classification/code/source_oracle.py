"""Independent dynamic catch-location oracle from the defining ASTs."""
import ast,hashlib

def audit(launcher,entry,catalogue,producer):
 et=ast.parse(entry);lt=ast.parse(launcher)
 def fun(tree,name,cls=None):
  body=tree.body if cls is None else next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls).body
  return next(n for n in body if isinstance(n,ast.FunctionDef) and n.name==name)
 d=fun(et,'_dispatch');client=fun(et,'handle','Client');session=fun(lt,'handle','ManagedSession');fail=fun(et,'_fail');tr=next(n for n in d.body if isinstance(n,ast.Try));branch=tr.body[0];handler=tr.handlers[0]
 assert d.body.index(tr)==2 and len(tr.handlers)==1 and ast.unparse(handler.type)=='BaseException'
 assert ast.unparse(branch.test)=="operation == 'handle'" and ast.unparse(handler.body[0])=='owner.failure = error'
 assert ast.unparse(client.body[0])=="return _dispatch(self.__token, 'handle', authenticated_packet)"
 assert len(session.body)==1 and ast.unparse(session.body[0])=='return self.__managed.handle(authenticated_packet)'
 assert ast.unparse(branch.body[1])=='result = owner.wrapper.handle(packet)'
 assert ast.unparse(d.body[-1])=='_fail()' and ast.unparse(d.body[1].body[0])=='_fail()'
 assert isinstance(fail.body[0],ast.Raise) and fail.body[0].exc.func.id=='ClientFailure' and ast.literal_eval(fail.body[0].cause) is None
 protected={id(n) for statement in tr.body for n in ast.walk(statement)}
 assert id(d.body[0]) not in protected and id(d.body[1]) not in protected and id(handler.body[0]) not in protected
 assert id(branch.body[1]) in protected
 specs={
 'client-call':(client.body[0],entry,'caller-outside-dispatch',False),
 'owner-lookup':(d.body[0],entry,'dispatch-before-try',False),
 'owner-guard':(d.body[1],entry,'dispatch-before-try',False),
 'packet-check':(branch.body[0],entry,'dispatch-protected-try',True),
 'session-call':(branch.body[1],entry,'dispatch-protected-try',True),
 'manager-call':(session.body[0],launcher,'callee-under-dispatch-protected-call',True),
 'session-return':(session.body[0],launcher,'callee-under-dispatch-protected-call',True),
 'response-check':(branch.body[2],entry,'dispatch-protected-try',True),
 'dispatch-return':(branch.body[3],entry,'dispatch-protected-try',True),
 'client-return':(client.body[0],entry,'caller-outside-dispatch',False),
 'retain-error':(handler.body[0],entry,'dispatch-handler-body',False),
 'fixed-failure':(fail.body[0],entry,'fixed-helper-outside-protected-region',False)}
 info={}
 for stage,(n,raw,location,inside) in specs.items():
  anchor={'site':f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}','expression':ast.get_source_segment(raw.decode(),n)}
  actual=catalogue['source']['stages'][stage];assert all(actual[k]==v for k,v in anchor.items()),stage
  # Independent AST membership, with explicit dynamic call propagation for the
  # session's unhandled direct return through the protected dispatcher call.
  if raw is entry and stage not in ('client-call','client-return','fixed-failure'):assert inside==(id(n) in protected)
  info[stage]={'location':location,'protected':inside,'anchor':anchor,'source':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}}
 # Current flag is assigned from the terminal classifier exactly once. It has
 # no direct conditional operational consumer in the current producer.
 pt=ast.parse(producer);project=fun(pt,'client_handle_projection');helper=fun(pt,'_client_outcome_classification');validator=fun(pt,'validate_client_handle_projection')
 pairs=[(k,v) for n in ast.walk(project) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='outside_catch_failure']
 assert len(pairs)==1 and ast.unparse(pairs[0][1])=="classification['unexpected_raise_outside_dispatch_catch']"
 assert not any(isinstance(n,ast.Name) and n.id=='outside' for n in ast.walk(project))
 assert 'client_handle_projection' in {n.func.id for n in ast.walk(validator) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
 assert 'same' in {n.func.id for n in ast.walk(validator) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
 consumers=[]
 for fn in [n for n in pt.body if isinstance(n,ast.FunctionDef)]:
  for n in ast.walk(fn):
   if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Constant) and n.slice.value in ('outside_catch_failure','unexpected_raise_outside_dispatch_catch'):
    consumers.append({'function':fn.name,'line':n.lineno,'expression':ast.unparse(n)})
 assert consumers==[{'function':'client_handle_projection','line':pairs[0][1].lineno,'expression':"classification['unexpected_raise_outside_dispatch_catch']"}]
 return {'result':'PASS','stages':info,'normal_order':list(specs)[:10],'source_intended_fixed_failure':{'type':'ClientFailure','message':ast.literal_eval(fail.body[0].exc.args[0]),'cause':None},'dynamic_callee_protection_basis':'ManagedSession.handle directly calls manager and returns without a handler; its dispatcher call is in the protected try body','direct_consumers':consumers,'regenerated_whole_result_validation':True,'runtime_or_authority_decisions_consume_flag':False,'not_a_new_runtime_observation':True}
