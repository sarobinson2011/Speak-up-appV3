"""Reviewer-owned AST audit. Does not call either supplied guard extractor."""
import ast,copy,hashlib
def key(n):return ':'.join(map(str,(n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__)))
def audit(raw,catalogue):
 text=raw.decode();tree=ast.parse(raw);owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in owner.body if isinstance(n,ast.FunctionDef)};info={};nodes={}
 def ref(n):return {'site':key(n),'expression':ast.get_source_segment(text,n)}
 def block(owner,region,seq,fn,guards,blocks,handlers):
  for i,n in enumerate(seq):walk(n,fn,guards,blocks+[{'owner':key(owner),'region':region,'normal_continuation_of':[ref(p) for p in seq[:i] if isinstance(p,ast.stmt)]}],handlers)
 def walk(n,fn,g,b,h):
  if hasattr(n,'lineno'):info[key(n)]={'function':fn,'guards':g,'continuation':b,'handlers':h};nodes[key(n)]=n
  if isinstance(n,ast.ClassDef):
   for child in n.body:walk(child,fn,g+[('class',key(n))],[],h)
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
   else:raise AssertionError(('unexpected guard',g))
  return out
 def state(n):return n.attr if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' else None
 def expr(n):
  d={**ref(n),'guards':info[key(n)]['guards']}
  if isinstance(n,ast.Constant):d.update(op='literal',type=type(n.value).__name__,value=n.value)
  elif state(n):d.update(op='state',name=state(n))
  elif isinstance(n,ast.Name):d.update(op='local',name=n.id)
  elif isinstance(n,ast.BinOp):assert isinstance(n.op,ast.Add);d.update(op='add',left=expr(n.left),right=expr(n.right))
  elif isinstance(n,ast.IfExp):d.update(op='choice',test=expr(n.test),yes=expr(n.body),no=expr(n.orelse))
  elif isinstance(n,ast.Compare):assert len(n.ops)==1 and isinstance(n.ops[0],ast.In);d.update(op='in',left=expr(n.left),right=expr(n.comparators[0]))
  elif isinstance(n,ast.Tuple):d.update(op='tuple',values=[expr(x) for x in n.elts])
  elif isinstance(n,ast.Call):assert isinstance(n.func,ast.Name) and n.func.id=='str' and len(n.args)==1 and isinstance(n.args[0],ast.Name);d.update(op='exception-text',name=n.args[0].id)
  elif isinstance(n,ast.Attribute):
   assert n.attr=='__name__' and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='type';d.update(op='exception-type-name',name=n.value.args[0].id)
  else:raise AssertionError(ast.dump(n))
  return d
 def normalize(value):
  if isinstance(value,dict):return {k:guards(v) if k=='guards' else normalize(v) for k,v in value.items()}
  if isinstance(value,list):return [normalize(v) for v in value]
  return value
 ret=next(n for n in ast.walk(methods['status']) if isinstance(n,ast.Return));assert isinstance(ret.value,ast.Dict)
 fields=[(ast.literal_eval(k),v) for k,v in zip(ret.value.keys,ret.value.values)];selected={state(v) for _,v in fields if state(v)}
 writes=[];calls=[]
 for fn in methods.values():
  for n in ast.walk(fn):
   if isinstance(n,(ast.Assign,ast.AugAssign)):
    for t in n.targets if isinstance(n,ast.Assign) else [n.target]:
     if state(t) in selected:writes.append((n,state(t),'add' if isinstance(n,ast.AugAssign) else 'set'))
   if isinstance(n,ast.Call) and state(n.func) in methods:calls.append(n)
 params=[]
 for n,target,op in writes:
  fn=info[key(n)]['function'];args=[a.arg for a in methods[fn].args.args]
  if isinstance(n.value,ast.Name) and n.value.id in args:
   pos=args.index(n.value.id)-1
   params.extend((call,fn,n.value.id,call.args[pos]) for call in calls if state(call.func)==fn)
 local_names={a.id for n,_,_ in writes for a in ast.walk(n.value) if isinstance(a,ast.Name)}
 locals_=[n for fn in methods.values() for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in local_names for t in n.targets)]
 transitions=[n for n in calls if state(n.func) in {info[key(w)]['function'] for w,_,_ in writes}]
 actual=catalogue['source']
 assert actual['source']=={'path':'compiler/live_connection.py','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 def located(row,n):
  assert row['site']==key(n) and row['expression']==ast.get_source_segment(text,n)
  assert row['function']==info[key(n)]['function']
  assert guards(row['guards'])==info[key(n)]['guards'],('guards',key(n))
  assert row['continuation']==info[key(n)]['continuation'],('continuation',key(n))
 def membership(rows,wanted):
  assert len(rows)==len(wanted) and {r['site'] for r in rows}=={key(n) for n in wanted}
  return {r['site']:r for r in rows}
 wmap=membership(actual['writes'],[n for n,_,_ in writes])
 for n,target,op in writes:
  row=wmap[key(n)];located(row,n);assert row['target']==target and row['operation']==op and normalize(row['value'])==expr(n.value)
 pmap=membership(actual['parameter_inputs'],[n for n,_,_,_ in params])
 for n,callee,param,value in params:
  row=pmap[key(n)];located(row,n);assert row['callee']==callee and row['parameter']==param and normalize(row['value'])==expr(value)
 lmap=membership(actual['local_captures'],locals_)
 for n in locals_:
  row=lmap[key(n)];located(row,n);assert row['name']==n.targets[0].id and normalize(row['value'])==expr(n.value)
 tmap=membership(actual['transition_calls'],transitions)
 for n in transitions:located(tmap[key(n)],n);assert tmap[key(n)]['callee']==state(n.func)
 for row in actual['writes']+actual['parameter_inputs']+actual['local_captures']:
  names={n.id for n in ast.walk(nodes[row['value']['site']]) if isinstance(n,ast.Name) and n.id=='e'}
  expected=[dict(ref(h),name=h.name,exception_type=ast.unparse(h.type)) for h in reversed(info[row['site']]['handlers']) if h.name in names]
  assert row['exception_bindings']==expected,('exception binding',row['site'])
 located(actual['return'],ret)
 ftypes={target:type(ast.literal_eval(n.value)).__name__ for n,target,op in writes if info[key(n)]['function']=='__init__'}
 assert [f['name'] for f in actual['fields']]==[name for name,_ in fields]
 assert [d['name'] for d in catalogue['declarations']]==[name for name,_ in fields]
 for (name,value),f,d in zip(fields,actual['fields'],catalogue['declarations']):
  assert normalize(f['value'])==expr(value)==normalize(d['value'])
  assert d['type']==f['type']==(ftypes[state(value)] if state(value) else type(ast.literal_eval(value)).__name__)
  assert set(d['origin_ids'])=={'status-write:'+key(n) for n,target,_ in writes if target==state(value)}
  if not state(value):assert type(d['literal_value']) is bool and d['literal_value'] is False
 affected={info[key(n)]['function'] for n,_,_ in writes}|{'status'}
 assert {x['function'] for x in actual['control_programs']}==affected
 for row in actual['control_programs']:assert row['ast']==ast.dump(methods[row['function']],include_attributes=False)
 embeds=[n for n in ast.walk(methods['recover']) if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict)]
 assert len(embeds)==1 and len(actual['recovery_embedding'])==1
 er=actual['recovery_embedding'][0];located(er,embeds[0]);kv=next((k,v) for k,v in zip(embeds[0].value.keys,embeds[0].value.values) if isinstance(v,ast.Call) and state(v.func)=='status')
 assert er['key']==ast.literal_eval(kv[0]) and er['call']==ref(kv[1]) and er['fields']==[name for name,_ in fields]
 return {'source_sha256':hashlib.sha256(raw).hexdigest(),'fields':[{'name':name,'expression':ast.get_source_segment(text,v)} for name,v in fields],
  'writes':[{'site':key(n),'function':info[key(n)]['function'],'target':target,'operation':op,'value':ast.get_source_segment(text,n.value),'guards':info[key(n)]['guards'],'continuation':info[key(n)]['continuation']} for n,target,op in sorted(writes,key=lambda x:(x[0].lineno,x[0].col_offset))],
  'reason_arguments':[{'site':key(n),'function':info[key(n)]['function'],'callee':callee,'parameter':param,'value':ast.get_source_segment(text,value)} for n,callee,param,value in params],
  'counts':{'fields':len(fields),'phase_writes':sum(t=='_phase' for _,t,_ in writes),'reason_writes':sum(t=='_reason' for _,t,_ in writes),'epoch_writes':sum(t=='_epoch' for _,t,_ in writes),'parameter_inputs':len(params),'local_captures':len(locals_),'transition_calls':len(transitions)},
  'source_only':True,'candidate_guard_modules_used_by_this_oracle':False}
