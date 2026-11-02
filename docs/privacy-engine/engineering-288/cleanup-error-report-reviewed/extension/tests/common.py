"""New line172 focused harness. No historical campaign replay."""
from pathlib import Path
import os,sys,types,json,hashlib,copy,time,traceback,importlib.metadata,stat
D=copy.deepcopy
CALLS=[]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def module(p):
 p=Path(p);m=types.ModuleType('error_report_focused');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode);mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode)
 m=json.loads(mp.read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs
 for n,pin in m.items():assert identity((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'membership_types_hashes':'PASS','manifest':identity(mp.read_bytes())}
def environment():return {'python':sys.version,'implementation':sys.implementation.name,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize}
class Records:
 def __init__(self,p):self.path=Path(p).resolve();self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def save(self,n,v):
  p=self.path/n;t=self.path/(n+'.partial');p.parent.mkdir(parents=True,exist_ok=True)
  with t.open('xb') as f:f.write(enc(v));f.flush();os.fsync(f.fileno())
  t.replace(p)
 def event(self,n,**kw):
  v={'event':n,'seconds':time.monotonic()-self.start,**kw}
  with (self.path/'events.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('EVENT',json.dumps(v),flush=True)
 def row(self,n,result,layer,**kw):
  v={'check':n,'result':result,'layer':layer,**kw};self.rows.append(v)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print(len(self.rows),n,result,flush=True)
 def yes(self,n,fn,layer):
  assert time.monotonic()-self.start<3900,'REPORT-CONTROL-DEADLINE';v=fn();assert v is not False,n;self.row(n,'PASS',layer);return v
 def no(self,n,fn,layer,code=None,exception=ValueError):
  assert time.monotonic()-self.start<3900,'REPORT-CONTROL-DEADLINE'
  try:fn()
  except exception as e:
   if code:assert code in str(e),(n,str(e),code)
   self.row(n,'REJECTED',layer,error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**kw):
  self.save('calls.json',CALLS)
  self.save('RESULT.json',{'result':'PASS' if error is None else 'FAILED-ATTEMPT','checks':len(self.rows),'rows':self.rows,'error':error,'seconds':time.monotonic()-self.start,'environment':environment(),'scope':'Only new selected cleanup error-report correspondence controls; source/constructed correspondence, not runtime observation','full_public_negative_derivations':0,'independent_closure':'PENDING',**kw})
def guard(root,out,r):
 root=Path(root).resolve();out=Path(out).resolve();sm=sys.monitoring
 assert sm.get_tool(5) is None;sm.use_tool_id(5,'Engineering-error-report-focused')
 apps={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'}
 def started(c,o):
  if Path(c.co_filename).name in apps and c.co_flags&2 and c.co_name not in ('_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>'):raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
  CALLS.append({'file':c.co_filename,'function':c.co_name})
 sm.register_callback(5,sm.events.PY_START,started)
 def protect(c):
  if c.co_flags&2:sm.set_local_events(5,c,sm.events.PY_START)
  for x in c.co_consts:
   if isinstance(x,types.CodeType):protect(x)
 def audit(e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in apps:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC')
   protect(a[0])
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();flags=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 sys.addaudithook(audit)
 captures=[];target=None
 def returned(c,o,v):
  if target is not None and c is target._basis.__code__:captures.append(v);r.event('actual-authenticated-basis-returned')
  if c.co_name=='inputs' and type(v) is dict and 'prior_module' in v:
   pm=v['prior_module']
   for n in ('validate','_basis','_checked','_assemble','derive_status','derive_client_state','derive_client','derive_handle'):
    f=getattr(pm,n,None)
    if f:sm.set_local_events(5,f.__code__,sm.events.PY_START)
   if hasattr(pm,'inputs'):sm.set_local_events(5,pm.inputs.__code__,sm.events.PY_RETURN)
 sm.register_callback(5,sm.events.PY_RETURN,returned)
 def monitor(m):
  nonlocal target;target=m
  for n in ('_basis','_checked','_assemble','semantic','derive_error_report','constructed_projection','validate'):sm.set_local_events(5,getattr(m,n).__code__,sm.events.PY_START)
  sm.set_local_events(5,m._basis.__code__,sm.events.PY_START|sm.events.PY_RETURN);sm.set_local_events(5,m.inputs.__code__,sm.events.PY_RETURN)
 return monitor,captures
