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

def audit(manager,authority,catalogue,model,references,inventory):
 mm,_,_,mc=index(manager,'ManagedAuthority',{'binding','_require'})
 am,_,_,ac=index(authority,'Authority',{'__init__','state'})
 def unique(seq):
  seq=list(seq);assert len(seq)==1;return seq[0]
 getter=mm['binding'];assert [ast.unparse(n) for n in getter.decorator_list]==['property'] and ast.unparse(getter.args)=='self'
 assert len(getter.body)==1 and isinstance(getter.body[0],ast.With);lock=getter.body[0]
 assert len(lock.items)==1 and ast.unparse(lock.items[0].context_expr)=='self._lock' and lock.items[0].optional_vars is None
 assert len(lock.body)==2;call=lock.body[0].value;ret=lock.body[1];assert ast.unparse(call)=='self._require()' and isinstance(ret,ast.Return)
 value=ret.value;assert isinstance(value,ast.Attribute) and ast.unparse(value)=='self._live.binding'
 require=mm['_require'];assert len(require.body)==1 and isinstance(require.body[0],ast.If);branch=require.body[0]
 assert not branch.orelse and len(branch.body)==1 and isinstance(branch.body[0],ast.Raise)
 assert isinstance(branch.test,ast.BoolOp) and isinstance(branch.test.op,ast.Or)
 assert [ast.unparse(n) for n in branch.test.values]==["self._phase != 'READY'",'self._live is None','self._retired is not None']
 source=catalogue['source'];mapping={'getter':getter,'lock':lock,'return':ret,'value':value,'receiver':value.value,'readiness_call':call,'readiness_program':require,'readiness_test':branch.test}
 for k,n in mapping.items():mc(source[k],n)
 assert source['field']==source['state_selector']=='binding' and source['slot']=='_live' and source['ready_phase']=='READY'
 atree=ast.parse(authority);owner=unique(n for n in atree.body if isinstance(n,ast.ClassDef) and n.name=='Authority')
 writers=[]
 for n in ast.walk(owner):
  ts=n.targets if isinstance(n,(ast.Assign,ast.Delete)) else [n.target] if isinstance(n,(ast.AnnAssign,ast.AugAssign)) else []
  if any(ast.unparse(t)=='self.binding' for t in ts):writers.append(n)
 writer=unique(writers);assert key(writer) in {key(n) for n in ast.walk(am['__init__']) if hasattr(n,'lineno')} and isinstance(writer,ast.Assign)
 assert ast.unparse(writer.value.func)=='sha' and len(writer.value.args)==1 and not writer.value.keywords
 inner=writer.value.args[0];assert ast.unparse(inner.func)=='enc' and len(inner.args)==1 and not inner.keywords and isinstance(inner.args[0],ast.Dict)
 equality=unique(n for n in ast.walk(am['state']) if isinstance(n,ast.Compare) and ast.unparse(n)=="s['binding'] == self.binding")
 enforcement=unique(n for n in ast.walk(am['state']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='need' and n.args and n.args[0] is equality)
 for k,n in {'underlying_writer':writer,'underlying_value':writer.value,'state_equality':equality,'state_check':enforcement}.items():ac(source[k],n)
 inherited=unique(d for d in model['existing_declarations'] if d.get('template_id')=='HEAD:/binding')
 assert inherited['native_template']['type']=='STRING' and catalogue['declaration']['inherited_binding']==inherited and catalogue['declaration']['type']=='str'
 assert catalogue['declaration']['origin']==source['value'] and catalogue['declaration']['owner']=='ManagedAuthority.binding'
 assert catalogue['declaration']['classification']=='UNKNOWN' and all(catalogue['declaration'][k] is None for k in ('canonical_class','ordinal','multiplicity'))
 rs=references['source'];links={'live_read':unique(r for r in rs['reference_reads'] if r['function']=='binding' and r['site']==key(value.value)), 'ready_call':unique(r for r in rs['calls'] if r['function']=='binding' and r['site']==key(call)), 'ready_program':unique(r for r in rs['programs'] if r['function']=='_require')}
 assert catalogue['reference_links']==links
 inv={r['site']:r for r in inventory['sites']}
 for n in (lock,call,ret):assert inv[key(n)]['guards']==source[{'With':'lock','Call':'readiness_call','Return':'return'}[type(n).__name__]]['guards']
 assert source['normal_return_requires']==['lock context enter completes','_require returns normally','receiver and attribute evaluation complete','lock context exit completes without error']
 assert catalogue['actual_getter_observations'] is None and all(catalogue[k] is False for k in ('complete_repetition_coverage','full_model_binding','actual_admission'))
 return {'result':'PASS','independent_AST_guards_and_continuations':True,'manager':{'bytes':len(manager),'sha256':hashlib.sha256(manager).hexdigest()},'authority':{'bytes':len(authority),'sha256':hashlib.sha256(authority).hexdigest()},'return':'self._live.binding','type':'str under retained initialized Authority/HEAD premise','normal_readiness':{'phase':'READY','live_present':True,'retired_absent':True},'authority_binding_expression':ast.get_source_segment(authority.decode(),writer.value),'constructor_input_keys':[ast.literal_eval(k) for k in inner.args[0].keys],'source_locations':{k:key(v) for k,v in mapping.items()},'not_runtime_execution':True}

