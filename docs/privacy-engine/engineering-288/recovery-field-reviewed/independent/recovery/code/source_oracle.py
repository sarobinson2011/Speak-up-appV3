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

def audit(manager,authority,catalogue,model):
 mm,mi,mn,mc=index(manager,'ManagedAuthority',{'recover','_validate'})
 am,ai,an,ac=index(authority,'Authority',{'state'})
 def unique(seq):
  seq=list(seq);assert len(seq)==1;return seq[0]
 def assign(fn,name):return unique(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name)
 ret=unique(n for n in ast.walk(mm['recover']) if isinstance(n,ast.Return));assert isinstance(ret.value,ast.Dict)
 values=[(ast.literal_eval(k),k,v) for k,v in zip(ret.value.keys,ret.value.values)]
 source=catalogue['source'];assert source['keys']==[k for k,_,_ in values];mc(source['return'],ret)
 fields=[(name,k,v) for name,k,v in values if not isinstance(v,ast.Call)]
 assert [v['name'] for v in source['fields']]==[name for name,_,_ in fields]
 assert [v['name'] for v in catalogue['declarations']]==[name for name,_,_ in fields]
 heads=[]
 for (name,k,v),row,declaration in zip(fields,source['fields'],catalogue['declarations']):
  mc(row['key'],k);mc(row['origin'],v);mc(row['return_site'],ret)
  assert declaration['origin']==row and declaration['name']==name
  if isinstance(v,ast.Constant):
   assert type(v.value) is bool and row['kind']=='literal' and row['type']==declaration['type']=='bool' and type(row['value']) is bool and row['value'] is v.value
   assert declaration['inherited_head'] is None
  else:
   assert isinstance(v,ast.Name);origin=assign(mm['recover'],v.id);mc(row['assignment'],origin);mc(row['call'],origin.value)
   assert ast.unparse(origin.value.func)=='self._validate' and len(origin.value.args)==1 and not origin.value.keywords
   assert row['kind']=='validated-state-head' and row['local']==v.id;heads.append((row,origin,declaration))
  assert declaration['classification']=='UNKNOWN' and declaration['canonical_class'] is None and declaration['ordinal'] is None and declaration['multiplicity'] is None
 assert len(heads)==1;head,origin,declaration=heads[0]
 vr=unique(n for n in ast.walk(mm['_validate']) if isinstance(n,ast.Return));lookup=vr.value;assert isinstance(lookup,ast.Subscript)
 selector=ast.literal_eval(lookup.slice);state=assign(mm['_validate'],lookup.value.id)
 assert ast.unparse(state.value.func)=='a.state' and not state.value.args and not state.value.keywords
 assert [a.arg for a in mm['_validate'].args.args]==['self','a'] and ast.unparse(origin.value.args[0])=='a'
 export=unique(n for n in ast.walk(mm['_validate']) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Dict));pairs={ast.literal_eval(k):v for k,v in zip(export.value.keys,export.value.values)}
 assert ast.dump(pairs['expected_head'],include_attributes=False)==ast.dump(lookup,include_attributes=False)
 ingest=unique(n for n in ast.walk(mm['_validate']) if isinstance(n,ast.Call) and ast.unparse(n.func)=='self._ingest.validate_export')
 assert [ast.unparse(v) for v in ingest.args]==[export.targets[0].id] and not ingest.keywords
 ar=unique(n for n in ast.walk(am['state']) if isinstance(n,ast.Return));load=assign(am['state'],ar.value.id)
 assert ast.unparse(load.value.func)=='parse'
 def query(n):return unique(c for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='execute')
 aq=query(load);eq=query(pairs['head']);assert [ast.literal_eval(v) for v in aq.args]==[ast.literal_eval(v) for v in eq.args]==['SELECT raw FROM head WHERE id=1']
 mapping={'validator_call':origin.value,'argument':origin.value.args[0],'state_assignment':state,'state_call':state.value,'validator_return':vr,'lookup':lookup,'export_assignment':export,'expected_head_expression':pairs['expected_head'],'ingest_call':ingest,'raw_head_expression':pairs['head'],'export_head_query':eq}
 amapping={'authority_state_return':ar,'authority_state_load':load,'authority_head_query':aq}
 chain=source['head_chain'];assert set(chain)==set(mapping)|set(amapping)|{'parameter','selector'}
 for k,n in mapping.items():mc(chain[k],n)
 for k,n in amapping.items():ac(chain[k],n)
 assert chain['parameter']=='a' and chain['selector']==head['head_selector']==selector
 inherited=unique(d for d in model['existing_declarations'] if d.get('template_id')=='HEAD:/'+selector)
 assert declaration['inherited_head']==inherited and inherited['native_template']['type']=='STRING' and head['type']==declaration['type']=='str'
 owner=unique(d for d in model['local_declarations'] if d['id']=='managed-local:recovery-result');assert catalogue['owner']==owner
 embedding=[(name,v) for name,k,v in values if isinstance(v,ast.Call)];assert len(embedding)==1
 name,call=embedding[0];assert ast.unparse(call.func)=='self.status' and not call.args and not call.keywords
 assert len(source['status_embedding'])==1 and source['status_embedding'][0]['name']==name;mc(source['status_embedding'][0]['call'],call)
 programs={'ManagedAuthority.recover':(mm['recover'],mc),'ManagedAuthority._validate':(mm['_validate'],mc),'Authority.state':(am['state'],ac)}
 assert [r['owner'] for r in source['programs']]==list(programs)
 for row in source['programs']:
  node,checker=programs[row['owner']];checker(row,node);assert row['ast']==ast.dump(node,include_attributes=False)
 assert source['source']['sha256']==hashlib.sha256(manager).hexdigest() and source['authority_source']['sha256']==hashlib.sha256(authority).hexdigest()
 return {'result':'PASS','fields':[{'name':name,'source_expression':ast.get_source_segment(manager.decode(),n),'type':type(n.value).__name__ if isinstance(n,ast.Constant) else 'inherited HEAD string'} for name,k,n in fields],
  'return':source['return'],'head_chain':copy.deepcopy(chain),'programs':list(programs),'selected_field_count':len(fields),'head_chain_entries':len(chain),'guard_extraction_independent_of_candidate':True,'source_only_not_execution':True}
