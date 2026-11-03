from pathlib import Path
import os,sys,types,json,hashlib,copy,time,traceback,importlib.metadata
from intake import verify_root,identity,enc
D=copy.deepcopy
CALLS=[]
def module(p):
 p=Path(p);m=types.ModuleType('fl6_reviewed');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def environment():return {'python':sys.version,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize}
class Records:
 def __init__(self,p):self.path=Path(p).resolve();self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def save(self,n,x):(self.path/n).write_bytes(enc(x))
 def event(self,kind,**kw):
  v={'event':kind,'seconds':time.monotonic()-self.start,**kw}
  with (self.path/'events.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('EVENT',json.dumps(v),flush=True)
 def row(self,n,result,**kw):
  v={'ordinal':len(self.rows)+1,'check':n,'result':result,**kw};self.rows.append(v)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  self.save('ROW-%04d.json'%len(self.rows),v);print('ROW '+json.dumps(v),flush=True)
 def yes(self,n,fn,layer="independent constructed check"):
  assert time.monotonic()-self.start<4400,'REVIEW-SOFT-DEADLINE';v=fn();assert v is not False,n;self.row(n,'PASS',layer=layer);return v
 def no(self,n,fn,code=None,layer="authenticated-basis comparison core"):
  try:
   assert time.monotonic()-self.start<4400,'REVIEW-SOFT-DEADLINE';fn()
  except ValueError as e:
   if code:assert code in str(e),(n,str(e),code)
   self.row(n,'REJECTED',error=str(e),layer=layer);return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**kw):self.save('calls.json',CALLS);self.save('RESULT.json',{'result':'PASS' if error is None else 'FAILED-ATTEMPT','checks':len(self.rows),'rows':self.rows,'error':error,'seconds':time.monotonic()-self.start,'environment':environment(),'runtime_operations':0,'database_connections':0,'session_operations':0,'constructed_not_runtime':True,**kw})
def guard(root,out,r):
 root=Path(root).resolve();out=Path(out).resolve();sm=sys.monitoring;sm.use_tool_id(0,'Formal-Lab6-loop')
 app={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'}
 def started(c,o):
  if Path(c.co_filename).name in app and c.co_flags&2 and c.co_name not in ('_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>'):raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
  CALLS.append({'file':c.co_filename,'function':c.co_name})
 sm.register_callback(0,sm.events.PY_START,started)
 def protect(c):
  if c.co_flags&2:sm.set_local_events(0,c,sm.events.PY_START)
  for x in c.co_consts:
   if isinstance(x,types.CodeType):protect(x)
 def audit(e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in app:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC')
   protect(a[0])
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();flags=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 sys.addaudithook(audit)
 captures=[];target=None
 def returned(c,o,v):
  if target is not None and c is target._basis.__code__:
   captures.append(v);r.event('actual_basis_return_observed',catalogue_format=v['catalogue']['format'])
  if c.co_name=='inputs' and type(v) is dict and 'prior_module' in v:
   pm=v['prior_module']
   for n in ('validate','_basis','_checked','_assemble','derive_status','derive_client_state','derive_client','derive_handle'):
    f=getattr(pm,n,None)
    if f:sm.set_local_events(0,f.__code__,sm.events.PY_START)
   if hasattr(pm,'inputs'):sm.set_local_events(0,pm.inputs.__code__,sm.events.PY_RETURN)
 sm.register_callback(0,sm.events.PY_RETURN,returned)
 def monitor(m):
  nonlocal target;target=m
  for n in ('_basis','_checked','_assemble','semantic','derive_cleanup_loop','constructed_projection','validate'):sm.set_local_events(0,getattr(m,n).__code__,sm.events.PY_START)
  sm.set_local_events(0,m._basis.__code__,sm.events.PY_START|sm.events.PY_RETURN);sm.set_local_events(0,m.inputs.__code__,sm.events.PY_RETURN)
 return monitor,captures
def change(v,path,x):
 v=D(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=x;return v
def substitute(v,a,b):
 if type(v) is dict:return {k:substitute(x,a,b) for k,x in v.items()}
 if type(v) is list:return [substitute(x,a,b) for x in v]
 return b if type(v) is type(a) and v==a else v
