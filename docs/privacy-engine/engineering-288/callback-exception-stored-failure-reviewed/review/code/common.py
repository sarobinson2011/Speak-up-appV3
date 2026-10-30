from pathlib import Path
import os,sys,types,json,hashlib,copy,stat,time,traceback,importlib.metadata
sys.path.insert(0,str(Path(__file__).parent))
from integrity import root as verify_root,ident
D=copy.deepcopy
CALLS=[]
def module(p,name='reviewed_candidate'):
 p=Path(p);m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def environment():return {'python':sys.version,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize}
def guard(root,out):
 root=Path(root).resolve();out=Path(out).resolve();sm=sys.monitoring;sm.use_tool_id(4,'Formal-Lab6-callback')
 app={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'}
 def started(c,o):
  if Path(c.co_filename).name in app and c.co_flags & 2 and c.co_name not in ('_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>'):raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
  CALLS.append({'file':c.co_filename,'function':c.co_name})
 sm.register_callback(4,sm.events.PY_START,started)
 def protect(c):
  if c.co_flags & 2:sm.set_local_events(4,c,sm.events.PY_START)
  for v in c.co_consts:
   if isinstance(v,types.CodeType):protect(v)
 def audit(e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in app:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC:'+a[0].co_filename)
   protect(a[0])
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();f=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if f&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 sys.addaudithook(audit)
 def returned(c,o,v):
  if c.co_name=='inputs' and type(v) is dict and 'prior_module' in v:
   pm=v['prior_module']
   for name in ('_checked','_assemble','derive_status','derive_client_state','derive_client','derive_handle'):
    fn=getattr(pm,name,None)
    if fn:sm.set_local_events(4,fn.__code__,sm.events.PY_START)
   if hasattr(pm,'inputs'):sm.set_local_events(4,pm.inputs.__code__,sm.events.PY_RETURN)
 sm.register_callback(4,sm.events.PY_RETURN,returned)
 def monitor(m):
  for n in ('_basis','_checked','_assemble','semantic','derive_callback','constructed_projection','constructed_normal_callback','validate'):
   sm.set_local_events(4,getattr(m,n).__code__,sm.events.PY_START)
  sm.set_local_events(4,m.inputs.__code__,sm.events.PY_RETURN)
 return monitor
class Records:
 def __init__(self,p):self.path=Path(p).absolute();self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def save(self,n,x): (self.path/n).write_bytes(enc(x))
 def row(self,n,r,**kw):
  x={'check':n,'result':r,**kw};self.rows.append(x)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
  print(len(self.rows),n,r,flush=True)
 def yes(self,n,test):
  v=test();assert v is not False,n;self.row(n,'PASS');return v
 def no(self,n,test,reason=None):
  try:test()
  except ValueError as e:
   if reason:assert reason in str(e),(n,str(e),reason)
   self.row(n,'REJECTED',error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**extra):
  self.save('calls.json',CALLS);self.save('RESULT.json',{'checks':len(self.rows),'rows':self.rows,'result':'PASS' if error is None else 'FAILED-ATTEMPT','error':error,'environment':environment(),'seconds':time.monotonic()-self.start,'runtime_calls':0,'session_operations':0,'database_connections':0,'source_only_constructed':True,**extra})
def change(v,path,x):
 v=D(v);w=v
 for k in path[:-1]:w=w[k]
 w[path[-1]]=x;return v
def replace(v,old,new):
 if type(v) is dict:return {k:replace(x,old,new) for k,x in v.items()}
 if type(v) is list:return [replace(x,old,new) for x in v]
 return new if type(v) is type(old) and v==old else v
