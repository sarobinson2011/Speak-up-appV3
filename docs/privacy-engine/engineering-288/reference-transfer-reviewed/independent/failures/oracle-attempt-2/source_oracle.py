"""Reviewer-owned AST audit. Does not call either supplied guard extractor."""
import ast,copy,hashlib
def key(n):return ':'.join(map(str,(n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__)))
def audit(raw,catalogue,authority,model):
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
 def attr(n):return n.attr if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' else None
 slots={'_live','_retired'}
 def ordered(ns):return sorted(ns,key=lambda n:(n.lineno,n.col_offset))
 writes=[];reads=[];allocations=[]
 for n in nodes.values():
  if isinstance(n,ast.Assign) and any(attr(t) in slots for t in n.targets):
   assert len(n.targets)==1;writes.append(n)
  elif isinstance(n,(ast.AugAssign,ast.AnnAssign,ast.Delete)):
   assert not any(attr(t) in slots for t in (n.targets if isinstance(n,ast.Delete) else [n.target]))
  if isinstance(n,ast.Attribute) and attr(n) in slots and isinstance(n.ctx,ast.Load):reads.append(n)
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='a' for t in n.targets):allocations.append(n)
 writes=ordered(writes);reads=ordered(reads);allocations=ordered(allocations)
 writers={info[key(n)]['function'] for n in writes}
 # Internal writers are mandatory transfer dependencies. _require is the
 # source's read-only gate over both slots; arguments/receivers also select
 # initialization, validation and close relationships independently.
 gates={name for name,fn in methods.items() if name not in writers and name=='_require' and any(isinstance(n,ast.Raise) for n in ast.walk(fn))}
 assert gates=={'_require'}
 calls=ordered([n for n in nodes.values() if isinstance(n,ast.Call) and (
  attr(n.func) in writers|gates or
  isinstance(n.func,ast.Attribute) and attr(n.func.value) in slots or
  any(isinstance(v,ast.Name) and v.id=='a' for v in n.args))])
 selected=writers|gates|{info[key(n)]['function'] for n in calls}
 actual=catalogue['source']
 assert actual['source']=={'path':'compiler/live_connection.py','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
 def located(row,n):
  expected=info[key(n)]
  assert row['site']==key(n) and row['expression']==ast.get_source_segment(text,n)
  assert row['function']==(n.name if isinstance(n,ast.FunctionDef) else expected['function'])
  assert guards(row['guards'])==expected['guards'],('guards',key(n))
  assert row['continuation']==expected['continuation'],('continuation',key(n))
 def value(n):
  if isinstance(n,ast.Constant):assert n.value is None;return {'kind':'none','expression':ref(n)}
  if isinstance(n,ast.Name):assert n.id=='a';return {'kind':'invocation-local-reference','local':n.id,'expression':ref(n)}
  assert attr(n) in slots;return {'kind':'slot-reference','slot':attr(n),'expression':ref(n)}
 def membership(rows,expected):
  assert [r['site'] for r in rows]==[key(n) for n in expected],('membership/order',[key(n) for n in expected])
  return list(zip(rows,expected))
 for row,n in membership(actual['writes'],writes):
  located(row,n);assert row['target']==attr(n.targets[0]) and row['value']==value(n.value)
  assert row['id']=='managed-reference-write:'+key(n)
 for row,n in membership(actual['reference_reads'],reads):located(row,n);assert row['slot']==attr(n)
 for row,n in membership(actual['local_producers'],allocations):
  located(row,n);assert row['local']=='a' and row['call']==ref(n.value)
  assert ast.unparse(n.value.func)=='self._runtime.Authority.__new__'
  assert [ast.unparse(a) for a in n.value.args]==['self._runtime.Authority'] and not n.value.keywords
 for row,n in membership(actual['calls'],calls):
  located(row,n);assert row['callee']==ast.unparse(n.func)
  bindings=[]
  if isinstance(n.func,ast.Attribute) and attr(n.func.value) in slots:bindings.append({'role':'receiver','value':value(n.func.value)})
  bindings.extend({'role':'argument:'+str(i),'value':value(v)} for i,v in enumerate(n.args) if isinstance(v,ast.Name) and v.id=='a')
  assert row['reference_bindings']==bindings
 for row,n in membership(actual['programs'],[fn for name,fn in methods.items() if name in selected]):
  located(row,n);assert row['ast']==ast.dump(n,include_attributes=False)
 assert [d['slot'] for d in catalogue['declarations']]==['_live','_retired']
 for row in catalogue['declarations']:
  inherited=next(d for d in model['local_declarations'] if d['id']=='managed-local:'+row['slot'][1:])
  assert row['declaration']==inherited and inherited['type']=='optional opaque Authority reference'
  assert row['write_ids']==['managed-reference-write:'+key(n) for n in writes if attr(n.targets[0])==row['slot']]
  assert row['classification']=='UNKNOWN' and row['multiplicity'] is None
 ac=next(n for n in ast.parse(authority).body if isinstance(n,ast.ClassDef) and n.name=='Authority')
 close=next(n for n in ac.body if isinstance(n,ast.FunctionDef) and n.name=='close')
 assert ast.dump(close.body[0],include_attributes=False)==ast.dump(ast.parse('self.db.close()').body[0],include_attributes=False) and len(close.body)==1
 relation=catalogue['connection_relation'];assert relation['site']==key(close) and relation['expression']==ast.get_source_segment(authority.decode(),close)
 assert relation['source']['bytes']==len(authority) and relation['source']['sha256']==hashlib.sha256(authority).hexdigest()
 return {'source_sha256':hashlib.sha256(raw).hexdigest(),
  'counts':{'reference_writes':len(writes),'reference_reads':len(reads),'local_producers':len(allocations),'related_calls':len(calls),'containing_methods':len(selected)},
  'writes':[{'site':key(n),'function':info[key(n)]['function'],'target':attr(n.targets[0]),'value':ref(n.value),'guards':info[key(n)]['guards'],'continuation':info[key(n)]['continuation']} for n in writes],
  'calls':[{'site':key(n),'function':info[key(n)]['function'],'callee':ast.unparse(n.func),'guards':info[key(n)]['guards'],'continuation':info[key(n)]['continuation']} for n in calls],
  'reads':[{'site':key(n),'function':info[key(n)]['function'],'slot':attr(n)} for n in reads],
  'programs':sorted(selected),'authority_close':relation,
  'source_only':True,'candidate_guard_modules_used_by_this_oracle':False}
