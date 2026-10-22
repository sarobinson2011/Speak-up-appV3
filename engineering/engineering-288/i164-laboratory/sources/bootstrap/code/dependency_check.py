"""Read installed distribution requirements without depending on pip being installed.
Narrow supported syntax fails closed. Extras are not requested by this lock.
Not wheel-byte authentication or a replacement for lock provenance verification.
"""
import ast,importlib.metadata,platform,re,sys

def normalize(n):return re.sub('[-_.]+','-',n).lower()
def version(s):
 if not re.fullmatch(r'\d+(?:\.\d+)*',s):raise ValueError('UNSUPPORTED-VERSION:'+s)
 return tuple(int(v) for v in s.split('.'))
def compare(a,b,op):
 av,bv=version(a),version(b);n=max(len(av),len(bv));av+= (0,)*(n-len(av));bv+=(0,)*(n-len(bv))
 return {'==':av==bv,'!=':av!=bv,'>=':av>=bv,'<=':av<=bv,'>':av>bv,'<':av<bv}[op]
def marker(s):
 env={'extra':'','implementation_name':sys.implementation.name,'platform_python_implementation':platform.python_implementation(),'python_version':'.'.join(platform.python_version_tuple()[:2]),'python_full_version':platform.python_version(),'sys_platform':sys.platform,'platform_system':platform.system()}
 def ev(n):
  if isinstance(n,ast.Name) and n.id in env:return env[n.id]
  if isinstance(n,ast.Constant) and type(n.value) is str:return n.value
  if isinstance(n,ast.BoolOp) and isinstance(n.op,(ast.And,ast.Or)):
   vs=[ev(v) for v in n.values]
   if not all(type(v) is bool for v in vs):raise ValueError('MARKER-BOOLEAN')
   return all(vs) if isinstance(n.op,ast.And) else any(vs)
  if isinstance(n,ast.Compare) and len(n.ops)==len(n.comparators)==1:
   a,b=ev(n.left),ev(n.comparators[0]);op=n.ops[0]
   if isinstance(n.left,ast.Name) and n.left.id in ['python_version','python_full_version']:
    symbol={ast.Eq:'==',ast.NotEq:'!=',ast.GtE:'>=',ast.LtE:'<=',ast.Gt:'>',ast.Lt:'<'}
    if type(op) not in symbol:raise ValueError('VERSION-MARKER')
    return compare(a,b,symbol[type(op)])
   if isinstance(op,ast.Eq):return a==b
   if isinstance(op,ast.NotEq):return a!=b
   if isinstance(op,ast.In):return a in b
   if isinstance(op,ast.NotIn):return a not in b
  raise ValueError('UNSUPPORTED-REQUIREMENT-MARKER')
 r=ev(ast.parse(s.strip(),mode='eval').body)
 if type(r) is not bool:raise ValueError('MARKER-NOT-BOOLEAN')
 return r

def check():
 ds={normalize(d.metadata['Name']):d for d in importlib.metadata.distributions()};rows=[]
 for name,d in ds.items():
  for raw in d.requires or []:
   req,sep,condition=raw.partition(';')
   if sep and not marker(condition):rows.append({'owner':name,'requirement':raw,'applicable':False});continue
   m=re.fullmatch(r'\s*([A-Za-z0-9_.-]+)\s*(.*?)\s*',req)
   if not m:raise ValueError('UNSUPPORTED-DEPENDENCY')
   target=normalize(m[1]);spec=m[2].strip()
   if spec.startswith('(') and spec.endswith(')'):spec=spec[1:-1].strip()
   if target not in ds:raise ValueError('MISSING-DEPENDENCY:'+target)
   for term in spec.split(',') if spec else []:
    sm=re.fullmatch(r'\s*(==|!=|>=|<=|>|<)\s*(\d+(?:\.\d+)*)\s*',term)
    if not sm:raise ValueError('UNSUPPORTED-SPECIFIER:'+term)
    if not compare(ds[target].version,sm[2],sm[1]):raise ValueError('DEPENDENCY-VERSION:'+target)
   rows.append({'owner':name,'requirement':raw,'applicable':True,'installed':ds[target].version})
 return rows
