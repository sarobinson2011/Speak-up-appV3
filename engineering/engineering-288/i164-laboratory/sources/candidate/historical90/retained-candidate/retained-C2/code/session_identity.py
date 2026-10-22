"""Bounded application identity guard. Trusted interpreter, not a Python sandbox."""
import functools,hashlib,inspect,json,sys,types,sqlite3,ast
import cryptography
from pathlib import Path
MAX_FILE=1048576
EXECUTOR_ROOT='retained/executor-basis/retained/kernel/candidate/'
EXECUTOR_FILES=('executor/session.py','executor/abi.py','contract/PetitionRegistryPilot.sol','contract/ABI.json','contract/method-identifiers.json')
class IdentityBlocked(ValueError):pass
def need(value,message):
 if not value:raise IdentityBlocked(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):
 try:
  with path.open('rb') as f:raw=f.read(MAX_FILE+1)
 except OSError as ex:raise IdentityBlocked('IDENTITY-UNAVAILABLE:'+path.name) from ex
 need(len(raw)<=MAX_FILE,'IDENTITY-SIZE');return raw
def read_executable():
 # Linux procfs refers to the executing image, not a possibly replaced pathname.
 try:return Path('/proc/self/exe').read_bytes()
 except OSError as ex:raise IdentityBlocked('EXECUTING-INTERPRETER-IDENTITY-UNAVAILABLE') from ex
def code_value(c):
 # Paths/line numbers are not behavior; source identity is bound separately.
 return (c.co_argcount,c.co_posonlyargcount,c.co_kwonlyargcount,c.co_nlocals,c.co_stacksize,c.co_flags,c.co_code,tuple(code_value(v) if isinstance(v,types.CodeType) else v for v in c.co_consts),c.co_names,c.co_varnames,c.co_freevars,c.co_cellvars,c.co_exceptiontable)
def compiled_functions(raw):
 found={}
 def visit(c):
  found[c.co_qualname]=code_value(c)
  for x in c.co_consts:
   if isinstance(x,types.CodeType):visit(x)
 visit(compile(raw,'<bound-source>','exec',dont_inherit=True));return found
def literal_bindings(raw,module):
 pairs=[]
 def walk(nodes,obj):
  for node in nodes:
   if isinstance(node,ast.Assign):
    try:value=ast.literal_eval(node.value)
    except (ValueError,TypeError):continue
    for target in node.targets:
     if isinstance(target,ast.Name):pairs.append((obj,target.id,value))
   elif isinstance(node,ast.ClassDef):walk(node.body,getattr(obj,node.name))
 walk(ast.parse(raw).body,module);return pairs
def functions(module):
 for name,v in vars(module).items():
  if inspect.isfunction(v) and v.__module__==module.__name__:yield name,inspect.unwrap(v)
  elif inspect.isclass(v) and v.__module__==module.__name__:
   for key,f in vars(v).items():
    if isinstance(f,(staticmethod,classmethod)):f=f.__func__
    if isinstance(f,property):f=f.fget
    if inspect.isfunction(f):yield name+'.'+key,inspect.unwrap(f)
def checked(method):
 @functools.wraps(method)
 def run(self,*args,**kwargs):
  self.identity.check()
  return method(self,*args,**kwargs)
 return run
class Identity:
 def __init__(self,root,bridge,transport,executor,abi):
  self.root=Path(root);self.modules={'code/bridge.py':bridge,'code/session_identity.py':sys.modules[__name__],'retained/transport/transport.py':transport,EXECUTOR_ROOT+'executor/session.py':executor,EXECUTOR_ROOT+'executor/abi.py':abi}
  paths=set(self.modules)|{EXECUTOR_ROOT+n for n in EXECUTOR_FILES}|{'code/lab_cli.py','code/fixtures.py'}
  self.raw={n:read(self.root/n) for n in sorted(paths)}
  self.expected={n:compiled_functions(self.raw[n]) for n in self.modules}
  self.literals=[v for n,m in self.modules.items() for v in literal_bindings(self.raw[n],m)]
  self.function_refs={n:dict(functions(m)) for n,m in self.modules.items()}
  self.abi=abi;self.executor=executor
  self.runtime={'implementation':sys.implementation.name,'python':sys.version,'cache_tag':sys.implementation.cache_tag,'executing_linux_executable_sha256':sha(read_executable()),'sqlite_version':sqlite3.sqlite_version,'cryptography_version':cryptography.__version__,'flags':repr(sys.flags)}
  self.binding={'version':'I164-OPEN-SESSION-IDENTITY-1','files':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in self.raw.items()},'runtime':self.runtime}
  self.check()
 def check(self):
  for obj,key,value in self.literals:need(getattr(obj,key)==value,'LOADED-CONSTANT-SOURCE-MISMATCH:'+key)
  for n,raw in self.raw.items():need(read(self.root/n)==raw,'IDENTITY-CHANGED:'+n)
  for n,m in self.modules.items():
   current=dict(functions(m));need(current.keys()==self.function_refs[n].keys(),'LOADED-MEMBERS-CHANGED:'+n)
   for name,f in current.items():
    need(f is self.function_refs[n][name],'LOADED-FUNCTION-REPLACED:'+name)
    need(code_value(f.__code__)==self.expected[n].get(f.__qualname__),'LOADED-CODE-SOURCE-MISMATCH:'+name)
  need(self.executor.abi_encode is self.abi.encode,'ENCODER-REFERENCE-CHANGED')
  need(self.abi.ABI_BYTES==self.raw[EXECUTOR_ROOT+'contract/ABI.json'],'LOADED-ABI-MISMATCH')
  need(self.abi.SELECTOR_BYTES==self.raw[EXECUTOR_ROOT+'contract/method-identifiers.json'],'LOADED-SELECTOR-MISMATCH')
 def executor_code(self):return {n:sha(self.raw[EXECUTOR_ROOT+n]) for n in EXECUTOR_FILES}
 def digest(self,n):return sha(self.raw[n])
