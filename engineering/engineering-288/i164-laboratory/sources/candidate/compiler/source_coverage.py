"""Independent source census: source AST, not generated expected-list counts."""
import ast,json
from pathlib import Path

def inspect(root,catalogue,groups):
 import compiler as m
 def source(path):
  raw=(root/path).read_bytes();return raw,ast.parse(raw)
 raw,tree=source('tools/baseline.py')
 required=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RULES' for t in n.targets)))
 m.same(sorted(a['id'] for a in catalogue),sorted(r[0] for r in required),'SOURCE-ASSOCIATION-COVERAGE')
 for name,endpoints,path,fn,guard in required:
  a=next(a for a in catalogue if a['id']==name)
  m.same([e['template'] for e in a['endpoints']],endpoints,'SOURCE-ASSOCIATION-ENDPOINTS')
  m.same(a['guard'],guard,'SOURCE-ASSOCIATION-GUARD')
  raw2,tr=source('support/'+path);nodes=[n for n in ast.walk(tr) if isinstance(n,ast.FunctionDef) and n.name==fn]
  m.same(a['source'],m.ident('support/'+path),'SOURCE-ASSOCIATION-IDENTITY')
  m.same(a['anchors'],[{'function':fn,'first_line':n.lineno,'last_line':n.end_lineno} for n in nodes],'SOURCE-ASSOCIATION-ANCHOR')
 # Independently enumerate the supported family naming constructs from defining schemas source.
 raw,tr=source('support/code/static_declarations.py');fn=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='schemas')
 names=set();dynamic=[]
 for n in ast.walk(fn):
  expr=None
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='add':expr=n.args[0]
  if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='groups':expr=n.slice
  if expr is None:continue
  if isinstance(expr,ast.Constant) and type(expr.value) is str:names.add(expr.value)
  elif isinstance(expr,ast.Name) and expr.id in ['record_name','n']:continue # add destination; recursive lookup, not constructor
  elif isinstance(expr,ast.BinOp) and isinstance(expr.op,ast.Add) and isinstance(expr.left,ast.Constant) and expr.left.value in ['BODY-','ABI-'] and isinstance(expr.right,ast.Name) and expr.right.id=='method':dynamic.append(expr.left.value)
  else:raise m.Invalid('UNSUPPORTED-SOURCE-FAMILY-CONSTRUCT:'+ast.unparse(expr))
 from correspondence import BODIES
 # Runtime method census is already independently checked against actual exact() source by compiler.
 names.update('BODY-'+k for k in BODIES);names.update('ABI-'+k for k in ['signPetition','signPetitionWithZKProof'])
 m.same(sorted(groups),sorted(names),'SOURCE-FAMILY-COVERAGE')
 # Every literal object emission and each admitted dynamic emission is classified explicitly.
 raw,tr=source('support/code/ingest.py');fn=next(n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='validate_export');emitted=set();dynamic_emissions=[]
 def emission(e):
  if isinstance(e,ast.Constant) and type(e.value) is str:emitted.add(e.value)
  elif isinstance(e,ast.BinOp) and isinstance(e.op,ast.Add) and isinstance(e.left,ast.Constant) and e.left.value in ['BODY-','ABI-ARGUMENTS-']:
   dynamic_emissions.append(ast.unparse(e));emitted.update(('BODY-'+k for k in BODIES) if e.left.value=='BODY-' else ('ABI-'+k for k in ['signPetition','signPetitionWithZKProof']))
  elif isinstance(e,ast.IfExp) and all(isinstance(x,ast.Constant) and type(x.value) is str for x in [e.body,e.orelse]):emitted.update([e.body.value,e.orelse.value]);dynamic_emissions.append(ast.unparse(e))
  else:raise m.Invalid('UNSUPPORTED-OBJECT-EMISSION:'+ast.unparse(e))
 def objects_expr(expr,many):
  if many:
   m.need(isinstance(expr,ast.List),'UNSUPPORTED-OBJECT-DIRECTORY')
   for x in expr.elts:objects_expr(x,False)
  else:
   m.need(isinstance(expr,ast.Tuple) and len(expr.elts)==2,'UNSUPPORTED-OBJECT-CONSTRUCTOR');emission(expr.elts[0])
 for n in ast.walk(fn):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets):objects_expr(n.value,True)
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='objects':
   m.need(n.func.attr in ['append','extend'] and len(n.args)==1,'UNSUPPORTED-OBJECT-OPERATION');objects_expr(n.args[0],n.func.attr=='extend')
 m.need(emitted<=names,'UNDECLARED-EMITTED-FAMILY')
 # Exact source constructor fields, tied to specific assignment locations rather than arbitrary subset matching.
 bindings={('runtime/accounting.py','record','x'):'ATTEMPT',('runtime/accounting.py','query',"p['query']"):'QUERY',('runtime/authority.py','__init__','s'):'HEAD',('runtime/authority.py','apply',"s['u'][u]"):'U-ENTRY',('runtime/authority.py','apply',"v['stage']"):'STAGE',('runtime/authority.py','apply','template'):'TEMPLATE',('runtime/authority.py','apply','action'):'ACTION',('runtime/authority.py','apply',"st['pending']"):'PENDING',('runtime/authority.py','apply',"st['last']"):'LAST'}
 constructors=[];found=set();inventory=[]
 for path in ['runtime/authority.py','runtime/accounting.py','runtime/ownership.py']:
  raw,tr=source('support/reference/'+path)
  for fn in [n for n in ast.walk(tr) if isinstance(n,ast.FunctionDef)]:
   for n in ast.walk(fn):
    if not isinstance(n,ast.Assign) or not isinstance(n.value,ast.Dict):continue
    for target in n.targets:
     key=(path,fn.name,ast.unparse(target))
     if key not in bindings:continue
     name=bindings[key];m.need(all(isinstance(k,ast.Constant) and type(k.value) is str for k in n.value.keys),'UNSUPPORTED-CONSTRUCTOR-KEY')
     fields={k.value for k in n.value.keys};expected=set(groups[name])-({'stage'} if name=='U-ENTRY' else {'result'} if name=='PENDING' else set())
     m.same(sorted(fields),sorted(expected),'SOURCE-CONSTRUCTOR-FIELDS:'+name)
     constructors.append({'family':name,'source':'support/reference/'+path,'sha256':m.sha(raw),'function':fn.name,'line':n.lineno,'fields':sorted(fields),'expression':ast.get_source_segment(raw.decode(),n)})
     found.add(key)
 from runtime_inventory import inventory as full_inventory,validate as validate_inventory
 inventory=full_inventory(root);validate_inventory(root,inventory)
 m.same(sorted(found),sorted(bindings),'SOURCE-CONSTRUCTOR-ANCHORS')
 return {'source_associations':[r[0] for r in required],'source_families':sorted(names),'emitted_families':sorted(emitted),'dynamic_emissions':dynamic_emissions,'constructors':constructors,'runtime_inventory':inventory,'supported_domain':'pinned schemas family naming, prior independent nested DSL/ABI/framing traversal, all literal and enumerated dynamic saved-export family emissions, explicit immutable/state constructor field sets, twelve source-anchored association obligations; runtime guards inventoried, not formally proved','unsupported_or_excluded':['arbitrary Python control-flow equivalence','qualified dependency/equality/actor classifications','unbounded external JSON schema beyond recursive JSON-VALUE','lifetime occurrence cardinalities','complete graph closure and ledger allocation'],'full_runtime_completeness':False}
