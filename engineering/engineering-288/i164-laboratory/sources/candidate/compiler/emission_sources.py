"""Source-derived emission/guard obligations; no runtime execution."""
import ast,hashlib,json
from pathlib import Path
INGEST='support/code/ingest.py'
RUNTIME=('support/reference/runtime/authority.py','support/reference/runtime/accounting.py','support/reference/runtime/ownership.py')
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def ident(root,path):
 b=(Path(root)/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pos(n):return [n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]
def key(n):return ':'.join(map(str,pos(n)))
def tree_info(raw):
 tree=ast.parse(raw);parents={c:n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
 def context(n):
  controls=[];scope=[];child=n
  while child in parents:
   p=parents[child]
   if isinstance(p,(ast.FunctionDef,ast.ClassDef)):scope.append(p.name)
   if isinstance(p,ast.If):controls.append({'site':key(p),'test':ast.unparse(p.test),'arm':'body' if child in p.body else 'else' if child in p.orelse else 'test'})
   if isinstance(p,ast.For):controls.append({'site':key(p),'target':ast.unparse(p.target),'iterable':ast.unparse(p.iter),'arm':'body' if child in p.body else 'else' if child in p.orelse else 'expression'})
   if isinstance(p,ast.With):controls.append({'site':key(p),'with':[ast.unparse(x.context_expr) for x in p.items]})
   if isinstance(p,ast.Try):controls.append({'site':key(p),'try_region':'body' if child in p.body else 'else' if child in p.orelse else 'finally' if child in p.finalbody else 'handler'})
   child=p
  return list(reversed(scope)),list(reversed(controls))
 return tree,context

def projection_source(root):
 raw=(Path(root)/INGEST).read_bytes();tree,ctx=tree_info(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_export');sites=[]
 for n in ast.walk(fn):
  operation=None;value=None
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='objects' for t in n.targets):operation='initialize';value=n.value
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and ast.unparse(n.func.value)=='objects':
   if n.func.attr not in ['append','extend'] or len(n.args)!=1 or n.keywords:raise ValueError('UNSUPPORTED-EMISSION-OPERATION')
   operation=n.func.attr;value=n.args[0]
  if operation:
   scope,controls=ctx(n);sites.append({'site':key(n),'operation':operation,'value_expression':ast.unparse(value),'source_expression':ast.get_source_segment(raw.decode(),n),'guards_and_loops':controls,'scope':scope})
 # Independent physical obligation set; no generated catalogue or fixture count.
 required={key(n) for n in ast.walk(fn) if (isinstance(n,ast.Assign) and any(ast.unparse(t)=='objects' for t in n.targets)) or (isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and ast.unparse(n.func.value)=='objects')}
 if {x['site'] for x in sites}!=required:raise ValueError('SOURCE-EMISSION-COVERAGE')
 return {'control_sites':[{'site':key(n),'kind':type(n).__name__,'expression':ast.unparse(n.test if isinstance(n,ast.If) else n.iter)} for n in ast.walk(fn) if isinstance(n,(ast.If,ast.For))],'source':ident(root,INGEST),'sites':sorted(sites,key=lambda x:[int(a) if a.isdigit() else a for a in x['site'].split(':')])}

def runtime_source(root):
 result=[];functions=[];excluded=[]
 for path in RUNTIME:
  raw=(Path(root)/path).read_bytes();tree,ctx=tree_info(raw)
  for fn in [n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]:
   scope,_=ctx(fn);qualified='.'.join(scope+[fn.name])
   admitted=(path.endswith('/authority.py') and qualified in ['Authority.__init__','Authority.transaction','Authority.blob','Authority.state','Authority.save','Authority.handle','Authority.apply','Authority.sign','Authority.require_ownership','Authority.charge','Authority.stage']) or (path.endswith('/accounting.py')) or (path.endswith('/ownership.py') and qualified in ['attach','claim','require','row'])
   if not admitted:excluded.append({'source':path,'function':qualified,'reason':'outside producer/persistence slice; retained source/inventory support only'});continue
   functions.append({'source':ident(root,path),'function':qualified,'site':key(fn),'exact_body':ast.get_source_segment(raw.decode(),fn)})
   for n in ast.walk(fn):
    if not isinstance(n,ast.Call):continue
    name=ast.unparse(n.func);families=[];role=None
    if name.endswith('.execute') and n.args and isinstance(n.args[0],ast.Constant) and type(n.args[0].value) is str:
     sql=n.args[0].value;upper=sql.upper()
     if upper.startswith(('INSERT','UPDATE')):
      table=upper.split()[2] if upper.startswith('INSERT') else upper.split()[1]
      table=table.replace('OWNERSHIP.','');family={'HEAD':'HEAD','EVENTS':'EVENT','BLOBS':'BLOB-STORE','JOURNAL':'JOURNAL','META':'OWNERSHIP-META','COORDINATES':'OWNERSHIP-ROW-SQL'}.get(table)
      if not family:raise ValueError('UNSUPPORTED-PERSISTENCE-TABLE:'+table)
      families=[family];role='PERSISTENCE-SITE; durable only if enclosing transaction commits'
     elif upper in ['BEGIN IMMEDIATE','COMMIT','ROLLBACK']:role='TRANSACTION-BOUNDARY'
    elif name=='self.save':families=['EVENT','HEAD'];role='EVENT-AND-STATE-CONSTRUCTION; save is not commit'
    elif name=='self.blob':families=['BLOB-STORE'];role='EXACT-BLOB-CONSTRUCTION; commit conditional'
    elif name in ['need','exact','integer','digest','label','verify','fault','signed_eth.validate','accounting.validate','accounting.ready','self.require_ownership','ownership.require']:
     role='FAULT-CUT' if name=='fault' else 'VALIDATION-GATE; ordered control flow, not unconditional conjunction'
    elif name in ['accounting.reserve','self.charge']:families=['COUNTS','PARTITIONS','RESOURCES','STAGE'];role='IN-MEMORY-ACCOUNTING; persisted via subsequent save/commit'
    elif name=='accounting.record':families=['ATTEMPT','TRANSPORT-ENTRY'];role='ATTEMPT-BLOB-AND-STATE-CONSTRUCTION'
    elif name=='accounting.query':families=['QUERY','COUNTS','PARTITIONS','RESOURCES','TRANSPORT-ENTRY'];role='QUERY-AND-ACCOUNTING-CONSTRUCTION'
    elif name=='accounting.settle':families=['RESOURCES','TRANSPORT-ENTRY'];role='ONCE-ONLY-DISPOSITION-CONSTRUCTION'
    elif name=='ownership.claim':families=['OWNERSHIP-ROW','OWNERSHIP-ROW-SQL'];role='OWNERSHIP-CLAIM; shared transaction required'
    if role:
     scope,controls=ctx(n);result.append({'source':path,'site':key(n),'function':qualified,'call':name,'expression':ast.get_source_segment(raw.decode(),n),'guards_and_loops':controls,'families':families,'role':role})
 return {'functions':functions,'sites':result,'excluded_functions':excluded,'boundary':'exact selected call sites and function control bodies; not SSA alias proof or full program control-flow qualification'}

def event_origins(root):
 path=RUNTIME[0];tree,ctx=tree_info((Path(root)/path).read_bytes());apply=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='apply')
 branches=[]
 for n in ast.walk(apply):
  if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and ast.unparse(n.test.left)=='m' and len(n.test.comparators)==1 and isinstance(n.test.comparators[0],ast.Constant):
   method=n.test.comparators[0].value
   branches.append({'method':method,'site':key(n),'test':ast.unparse(n.test),'has_return':any(isinstance(x,ast.Return) for st in n.body for x in ast.walk(st))})
 fallthrough=sorted(x['method'] for x in branches if not x['has_return'])
 origins=[]
 for fn in [n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name in ['apply','sign']]:
  for n in ast.walk(fn):
   if isinstance(n,ast.Call) and ast.unparse(n.func)=='self.save':
    k=n.args[2]
    if isinstance(k,ast.Constant) and type(k.value) is str:kinds=[k.value]
    elif isinstance(k,ast.Name) and k.id=='m' and fn.name=='apply':kinds=fallthrough
    else:raise ValueError('UNSUPPORTED-EVENT-KIND')
    origins.append({'source':path,'site':key(n),'function':fn.name,'event_kinds':kinds,'guards_and_loops':ctx(n)[1],'meaning':'committed event corresponds to this save site; construction alone is not commit'})
 return {'dispatch':branches,'common_save_methods':fallthrough,'origins':origins}
def source_map(root):return {'projection':projection_source(root),'runtime':runtime_source(root),'event_origins':event_origins(root)}
def validate(root,value):
 if enc(value)!=enc(source_map(root)):raise ValueError('SOURCE-GUARD-EMISSION-SUBSTITUTION')
 return True
