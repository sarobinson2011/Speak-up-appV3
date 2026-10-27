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

def audit(manager,authority,cat,model,references,inventory):
 mm,_,_,mc=index(manager,'ManagedAuthority',{'__init__','config','_require','recover','_validate'})
 am,_,_,ac=index(authority,'Authority',{'__init__'})
 def one(rows):
  rows=list(rows);assert len(rows)==1;return rows[0]
 def walk(fn,kind):return [n for n in ast.walk(fn) if isinstance(n,kind)]
 fn=mm['config'];assert ast.unparse(fn.args)=='self' and [ast.unparse(x) for x in fn.decorator_list]==['property']
 assert len(fn.body)==1 and isinstance(fn.body[0],ast.With);lock=fn.body[0]
 assert len(lock.items)==1 and ast.unparse(lock.items[0].context_expr)=='self._lock' and lock.items[0].optional_vars is None
 assert len(lock.body)==2 and isinstance(lock.body[0],ast.Expr) and isinstance(lock.body[1],ast.Return)
 call=lock.body[0].value;ret=lock.body[1];assert ast.unparse(call)=='self._require()'
 assert ast.unparse(ret.value)=='copy.deepcopy(self._config)' and not ret.value.keywords and len(ret.value.args)==1
 owner=one(n for n in ast.parse(manager).body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority')
 writers=[]
 for n in ast.walk(owner):
  ts=n.targets if isinstance(n,(ast.Assign,ast.Delete)) else [n.target] if isinstance(n,(ast.AugAssign,ast.AnnAssign)) else []
  if any(ast.unparse(t)=='self._config' for t in ts):writers.append(n)
 store=one(writers);assert isinstance(store,ast.Assign) and key(store) in {key(n) for n in walk(mm['__init__'],ast.Assign)}
 assert ast.unparse(store.value)=='copy.deepcopy(config)' and len(store.targets)==1 and not store.value.keywords
 req=mm['_require'];assert len(req.body)==1 and isinstance(req.body[0],ast.If);branch=req.body[0]
 assert not branch.orelse and len(branch.body)==1 and isinstance(branch.body[0],ast.Raise)
 assert ast.unparse(branch.body[0].exc)=="RecoveryBlocked('CONNECTION-' + self._phase)"
 assert isinstance(branch.test,ast.BoolOp) and isinstance(branch.test.op,ast.Or)
 assert [ast.unparse(n) for n in branch.test.values]==["self._phase != 'READY'",'self._live is None','self._retired is not None']
 recovery=one(n for n in walk(mm['recover'],ast.Call) if ast.unparse(n.func)=='copy.deepcopy' and ast.unparse(n.args[0])=='self._config')
 export=one(n for n in walk(mm['_validate'],ast.Call) if ast.unparse(n.func)=='copy.deepcopy' and ast.unparse(n.args[0])=='self._config')
 mapping={'constructor_storage':store,'constructor_input':store.value.args[0],'constructor_copy':store.value,'getter':fn,'lock':lock,'return':ret,'copy_call':ret.value,'origin':ret.value.args[0],'readiness_call':call,'readiness_program':req,'readiness_test':branch.test,'recovery_copy':recovery,'export_copy':export}
 for k,n in mapping.items():mc(cat['source'][k],n)
 ai=am['__init__'];member=one(n for n in walk(ai,ast.Call) if ast.unparse(n.func)=='exact' and ast.unparse(n.args[0])=='config')
 fields=ast.literal_eval(member.args[1]);assert fields==['version','pilot','session','start_nonce','manager','model','profile','config']
 separate=one(n for n in walk(ai,ast.Assign) if any(ast.unparse(t)=='self.config' for t in n.targets));assert ast.unparse(separate.value)=='parse(enc(config))'
 ac(cat['source']['authority_membership'],member);ac(cat['source']['authority_storage'],separate)
 expressions={ast.unparse(n) for n in walk(ai,ast.Call)}
 assert "integer(config['start_nonce'], 0, 2 ** 64 - 1)" in expressions
 assert "label(config['pilot'])" in expressions and "label(config['session'])" in expressions and "digest(config[k])" in expressions
 assert "need(config['version'] == VERSION, 'NO-MIGRATION')" in expressions
 manager_check=ast.parse("need(type(config['manager']) is str and len(config['manager']) == 40 and bytes.fromhex(config['manager']).hex() == config['manager'], 'MANAGER')",mode='eval').body
 assert ast.dump(manager_check,include_attributes=False) in {ast.dump(n,include_attributes=False) for n in walk(ai,ast.Call)}
 # The imported validators provide exact-type restrictions. They are read,
 # not executed, separately in controls.py's retained-helper audit.
 expected_types={k:'INTEGER' if k=='start_nonce' else 'STRING' for k in fields}
 decls={x['template_id']:x for x in model['existing_declarations']}
 inherited=decls['CONFIG:'];assert inherited['native_template']['type']=={'object':expected_types}
 assert cat['declaration']['inherited_config']==inherited and cat['source']['fields']==fields
 for k in fields:
  d=decls['CONFIG:/'+k];assert d['native_template']['type']==expected_types[k] and d['parent']==inherited['id'] and cat['declaration']['fields'][k]==d
 assert cat['declaration']['origin']==cat['source']['copy_call'] and cat['declaration']['storage_origin']==cat['source']['constructor_copy']
 assert cat['declaration']['classification']=='UNKNOWN' and all(cat['declaration'][k] is None for k in ('canonical_class','ordinal','multiplicity'))
 assert cat['source']['normal_return_requires']==['lock context enter completes','_require returns normally','copy.deepcopy of stored _config completes','lock context exit completes without error']
 assert cat['source']['ready_phase']=='READY'
 rs=references['source'];links={'ready_call':one(r for r in rs['calls'] if r['function']=='config' and r['site']==key(call)),'ready_program':one(r for r in rs['programs'] if r['function']=='_require')};assert cat['reference_links']==links
 inv={x['site']:x for x in inventory['sites']}
 for k in ('constructor_storage','constructor_copy','return','copy_call','lock','readiness_call','recovery_copy','export_copy'):assert inv[key(mapping[k])]['guards']==cat['source'][k]['guards']
 assert cat['actual_getter_observations'] is None and all(cat[k] is False for k in ('complete_repetition_coverage','full_model_binding','actual_admission'))
 return {'result':'PASS','source_derived_storage':'copy.deepcopy(config)','source_derived_getter':'copy.deepcopy(self._config)','readiness':ast.unparse(branch.test),'exact_types':expected_types,'locations':{k:key(v) for k,v in mapping.items()},'source':{'manager':hashlib.sha256(manager).hexdigest(),'authority':hashlib.sha256(authority).hexdigest()},'constructor_failure_after_storage_does_not_undo_assignment':True,'no_getter_execution':True,'no_getter_state_or_ingest_call':True}
