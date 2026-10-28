"""Reviewer-owned AST audit. Does not call either supplied guard extractor."""
import ast,copy,hashlib
def key(n):return ':'.join(map(str,(n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__)))
def index(raw,class_name,selected):
 text=raw.decode();tree=ast.parse(raw);owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==class_name);methods={n.name:n for n in owner.body if isinstance(n,ast.FunctionDef)};info={};nodes={}
 def ref(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def block(owner,region,seq,fn,guards,blocks,handlers):
  for i,n in enumerate(seq):walk(n,fn,guards,blocks+[{'owner':key(owner),'region':region,'normal_continuation_of':[ref(p) for p in seq[:i] if isinstance(p,ast.stmt)]}],handlers)
 def walk(n,fn,g,b,h):
  if hasattr(n,'lineno'):info[key(n)]={'function':fn,'guards':g,'continuation':b,'handlers':h};nodes[key(n)]=n
  if isinstance(n,ast.ClassDef):
   for child in n.body:
    if isinstance(child,ast.FunctionDef) and child.name in selected:walk(child,fn,g+[('class',key(n))],[],h)
  elif isinstance(n,ast.FunctionDef):block(n,'body',n.body,n.name,g+[('invoke',key(n))],[],[])
  elif isinstance(n,ast.With):
   for item in n.items:walk(item.context_expr,fn,g,b,h)
   block(n,'body',n.body,fn,g+[('enter',key(n),tuple(ast.unparse(i.context_expr) for i in n.items))],b,h)
  elif isinstance(n,ast.Try):
   block(n,'body',n.body,fn,g+[('try',key(n))],b,h)
   for i,handler in enumerate(n.handlers):walk(handler,fn,g+[('dispatch',key(n),i)],b,h)
   assert not n.orelse and not n.finalbody,'new source form needs review'
  elif isinstance(n,ast.ExceptHandler):
   block(n,'body',n.body,fn,g+[('handler',key(n),ast.unparse(n.type))],b,h+[n])
  elif isinstance(n,(ast.If,ast.IfExp)):
   walk(n.test,fn,g,b,h)
   for region,truth in [('body','truthy'),('orelse','falsy')]:
    sub=getattr(n,region);gg=g+[('predicate',key(n),ast.unparse(n.test),truth)]
    if isinstance(sub,list):block(n,region,sub,fn,gg,b,h)
    else:walk(sub,fn,gg,b,h)
  elif isinstance(n,ast.BoolOp):
   for i,operand in enumerate(n.values):
    prefix=[] if i==0 else [('bool-prefix',key(n),type(n.op).__name__,i,tuple((key(v),ast.unparse(v),'truthy' if isinstance(n.op,ast.And) else 'falsy') for v in n.values[:i]))]
    walk(operand,fn,g+prefix,b,h)
  else:
   for child in ast.iter_child_nodes(n):walk(child,fn,g,b,h)
 walk(owner,None,[],[],[])
 def guards(row):
  out=[]
  for g in row:
   kind,site,region,req=g['kind'],g['site'],g['region'],g['requires']
   if kind=='ClassDef':assert region=='class-body' and req==[{'event':'class-definition-executed'}];out.append(('class',site))
   elif kind=='FunctionDef':
    assert region=='invocation-boundary' and req==[{'event':'invocation-or-generator-resumption-required'}] and 'definition-time only' in g['outer_conditions'];out.append(('invoke',site))
   elif kind=='With':
    assert region=='body' and all(r['event']=='context-enter-completed' and r['item']==i for i,r in enumerate(req));out.append(('enter',site,tuple(r['expression'] for r in req)))
   elif kind=='Try' and region=='try-body':assert req==[{'event':'try-entered'}];out.append(('try',site))
   elif kind=='Try' and region=='handler-dispatch':
    assert req[0]=={'event':'exception-from-try-body'} and req[1]['event']=='earlier-handlers-not-selected' and len(req)==2;out.append(('dispatch',site,req[1]['count']))
   elif kind=='ExceptHandler':
    assert region=='handler-body' and len(req)==1 and req[0]['event']=='handler-selected';out.append(('handler',site,req[0]['exception_type']))
   elif kind in ('If','IfExp'):
    assert len(req)==1 and req[0]['predicate']==('truthy' if region=='body' else 'falsy') and req[0]['expression']==g['test'];out.append(('predicate',site,g['test'],req[0]['predicate']))
   elif kind=='BoolOp':
    i=int(region.removeprefix('operand-'));assert i>0 and len(req)==i and g['operator'] in ('And','Or')
    out.append(('bool-prefix',site,g['operator'],i,tuple((r['site'],r['expression'],r['predicate']) for r in req)))
   else:raise AssertionError(('unexpected guard',g))
  return out
 def check(row,n):
  q=info[key(n)];assert row["site"]==key(n) and row["expression"]==ast.get_source_segment(text,n)
  assert row["function"]==(n.name if isinstance(n,ast.FunctionDef) else q["function"])
  assert guards(row["guards"])==q["guards"],("guards",key(n))
  assert row["continuation"]==q["continuation"],("continuation",key(n))
  return True
 return methods,info,nodes,check

def audit(manager,authority,observations,cat,model,producer,refs):
 mm,_,_,mc=index(manager,'ManagedAuthority',{'state','_run','_require'});am,_,_,ac=index(authority,'Authority',{'state'})
 def same_ast(node,text):assert ast.dump(node,include_attributes=False)==ast.dump(ast.parse(text,mode='eval').body,include_attributes=False),(ast.unparse(node),text)
 def one(seq):
  seq=list(seq);assert len(seq)==1;return seq[0]
 wrapper=mm['state'];assert ast.unparse(wrapper.args)=='self' and not wrapper.decorator_list and len(wrapper.body)==1
 wr=wrapper.body[0];assert isinstance(wr,ast.Return);same_ast(wr.value,"self._run('state')")
 run=mm['_run'];assert ast.unparse(run.args)=='self, method, *args' and len(run.body)==1;lock=run.body[0]
 assert isinstance(lock,ast.With) and len(lock.items)==1 and lock.items[0].optional_vars is None;same_ast(lock.items[0].context_expr,'self._lock')
 assert len(lock.body)==2;ready,region=lock.body;assert isinstance(ready,ast.Expr);same_ast(ready.value,'self._require()')
 assert isinstance(region,ast.Try) and not region.orelse and not region.finalbody and len(region.handlers)==1 and len(region.body)==4
 pre,assignment,post,ret=region.body
 for node,message in [(pre,'UNEXPECTED-ACTIVE-TRANSACTION'),(post,'UNCOMMITTED-STATE')]:
  assert isinstance(node,ast.If) and not node.orelse and len(node.body)==1 and isinstance(node.body[0],ast.Raise)
  same_ast(node.test,'self._live.db.in_transaction');same_ast(node.body[0].exc,'RecoveryBlocked('+repr(message)+')')
 assert isinstance(assignment,ast.Assign) and len(assignment.targets)==1 and ast.unparse(assignment.targets[0])=='result';same_ast(assignment.value,'getattr(self._live,method)(*args)')
 writes=[n for n in ast.walk(run) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store) and n.id=='result'];assert len(writes)==1
 assert isinstance(ret,ast.Return);same_ast(ret.value,'result')
 handler=region.handlers[0];assert ast.unparse(handler.type)=='BaseException' and handler.name=='e' and len(handler.body)==2
 quarantine=handler.body[0].value;same_ast(quarantine,"self._quarantine(type(e).__name__+':'+str(e))")
 rer=handler.body[1];assert isinstance(rer,ast.Raise) and rer.exc is None and rer.cause is None
 req=mm['_require'];assert len(req.body)==1 and isinstance(req.body[0],ast.If);same_ast(req.body[0].test,"self._phase!='READY' or self._live is None or self._retired is not None")
 assert not req.body[0].orelse and len(req.body[0].body)==1 and isinstance(req.body[0].body[0],ast.Raise)
 backend=am['state'];expected=ast.parse('''def state(self):
 s=parse(self.db.execute('SELECT raw FROM head WHERE id=1').fetchone()[0],MAX_STATE)
 need(s['binding']==self.binding,'VERSION-BINDING')
 if s['seq']:
  e=self.db.execute('SELECT raw FROM events WHERE seq=?',(s['seq'],)).fetchone()
  need(e is not None and sha(e[0])==s['head'],'HEAD-EVENT')
  x=parse(e[0],MAX_EVENT)
  need(enc(x['after'])==enc({k:v for k,v in s.items() if k!='head'}),'HEAD-EVENT-TYPED')
 accounting.validate(s)
 return s
''').body[0]
 assert ast.dump(backend,include_attributes=False)==ast.dump(expected,include_attributes=False)
 load,bind,event,account,br=backend.body
 source=cat['source'];manager_map={'wrapper':wrapper,'wrapper_return':wr,'wrapper_call':wr.value,'run':run,'result_assignment':assignment,'run_return':ret,'dispatch':assignment.value,'dispatch_receiver':assignment.value.func.args[0],'readiness_program':req,'readiness_call':ready.value,'try_region':region,'handler':handler}
 stages={'lock_enter':lock.items[0].context_expr,'readiness':ready,'pre_transaction':pre,'dispatch':assignment.value,'post_transaction':post,'return_expression':ret,'handler_reason':quarantine.args[0],'quarantine':quarantine,'reraise':rer,'lock_exit':lock}
 for k,n in manager_map.items():mc(source[k],n)
 for k,n in stages.items():mc(source['stages'][k],n)
 backend_map={'backend':backend,'backend_load':load,'backend_return':br,'binding_check':bind,'event_guard':event,'accounting_check':account}
 for k,n in backend_map.items():ac(source[k],n)
 needs=[n for n in ast.walk(event) if isinstance(n,ast.Call) and ast.unparse(n.func)=='need'];assert len(needs)==len(source['event_checks'])==2
 for row,n in zip(source['event_checks'],needs):ac(row,n)
 assert source['method']=='state' and source['args']==[] and source['result_local']=='result' and source['ready_phase']=='READY'
 assert source['normal_path']==['lock_enter','readiness','pre_transaction','dispatch','post_transaction','return_expression','lock_exit']
 assert source['caught_stages']==['pre_transaction','dispatch','post_transaction','return_expression'] and source['outside_handler']==['lock_enter','readiness','lock_exit']
 head=one(x for x in model['existing_declarations'] if x['template_id']=='HEAD:');assert cat['inherited_head']==head
 expected_fields={'active','binding','counts','head','partitions','resources','seq','u'};assert set(head['native_template']['type']['object'])==expected_fields
 assert head['native_template']['type']['object']=={'active':{'union':['NULL','STRING']},'binding':'STRING','counts':{'ref':'COUNTS'},'head':'STRING','partitions':{'ref':'PARTITIONS'},'resources':{'ref':'RESOURCES'},'seq':'INTEGER','u':{'directory':{'ref':'U-ENTRY'},'key_type':'STRING'}}
 for row,name,origin in zip(cat['declarations'],['underlying-state','run-result','wrapper-return'],['backend_return','result_assignment','wrapper_return']):
  assert row['id']==name and row['type']==head['native_template']['type'] and row['origin']==source[origin] and row['classification']=='UNKNOWN' and all(row[k] is None for k in ('canonical_class','ordinal','multiplicity'))
 assert len(cat['declarations'])==3 and len(cat['links'])==2
 assert cat['links'][0]['from']==source['backend_return'] and cat['links'][0]['to']==source['result_assignment'] and cat['links'][1]['from']==source['run_return'] and cat['links'][1]['to']==source['wrapper_return']
 assert cat['delegation']==one(x for x in producer['delegations'] if x['from']=='ManagedAuthority.state -> _run') and cat['delegation']['to']=='Authority.state'
 assert cat['reference_links']['ready']==one(x for x in refs['source']['calls'] if x['site']==key(ready.value)) and cat['reference_links']['live_read']==one(x for x in refs['source']['reference_reads'] if x['site']==key(assignment.value.func.args[0]))
 inventory={x['site']:x for x in producer['source_inventory']['sites']}
 for k in ('wrapper_return','wrapper_call','result_assignment','run_return','readiness_call'):assert inventory[source[k]['site']]['guards']==source[k]['guards']
 ot=ast.parse(observations);prop=one(n for n in ast.walk(ot) if isinstance(n,ast.FunctionDef) and n.name=='propagate');p_call=one(n for n in ast.walk(ot) if isinstance(n,ast.Call) and ast.unparse(n)=='propagate(f, run)')
 assert ast.unparse(prop.body[0])=="need(parent['normal'] == child['normal'], 'WRAPPER-COMPLETION')"
 assert isinstance(prop.body[1],ast.If) and ast.unparse(prop.body[1].test)=="parent['normal']"
 same_ast(prop.body[1].body[0].value,"same(parent['return']['value'],child['return']['value'],'RETURN-EDGE')")
 assert source['existing_wrapper_check']['line']==p_call.lineno and source['existing_wrapper_check']['expression']==ast.get_source_segment(observations.decode(),p_call)
 assert source['existing_wrapper_check']['source']['sha256']==hashlib.sha256(observations).hexdigest()
 assert cat['actual_runtime_links'] is None and all(cat[k] is False for k in ('complete_repetition_coverage','full_model_binding','actual_admission'))
 return {'result':'PASS','source_derived_wrapper':ast.unparse(wr),'source_derived_assignment':ast.unparse(assignment),'backend_program':ast.get_source_segment(authority.decode(),backend),'caught_and_outside_regions_independently_derived':True,'source_locations':{k:key(n) for k,n in manager_map.items()},'stages':{k:key(n) for k,n in stages.items()},'backend_locations':{k:key(n) for k,n in backend_map.items()},'inherited_HEAD':copy.deepcopy(head),'wrapper_checker_propagate_source':ast.get_source_segment(observations.decode(),prop),'no_runtime_execution':True}
