"""New helper-open focused harness; no old campaign replay."""
from pathlib import Path
import os,sys,types,json,hashlib,copy,time,traceback,importlib.metadata,stat,datetime
D=copy.deepcopy
CALLS=[]
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def module(p):
 p=Path(p);m=types.ModuleType('helper_open_focused');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
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
  v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':n,'seconds':time.monotonic()-self.start,**kw}
  with (self.path/'events.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('EVENT',json.dumps(v),flush=True)
 def row(self,n,result,layer,**kw):
  v={'ordinal':len(self.rows)+1,'check':n,'result':result,'layer':layer,**kw};self.save('rows/'+str(v['ordinal']).zfill(5)+'.json',v);self.rows.append(v)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
  print('CHECK '+json.dumps(v,sort_keys=True),flush=True)
 def yes(self,n,fn,layer):
  assert time.monotonic()-self.start<4500,'OPEN-CONTROL-DEADLINE';v=fn();assert v is not False,n;self.row(n,'PASS',layer);return v
 def no(self,n,fn,layer,code=None,exception=ValueError):
  assert time.monotonic()-self.start<4500,'OPEN-CONTROL-DEADLINE'
  try:fn()
  except exception as e:
   if code:assert code in str(e),(n,str(e),code)
   self.row(n,'REJECTED',layer,error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**kw):
  self.save('calls.json',CALLS)
  self.save('RESULT.json',{'result':'PASS' if error is None else 'FAILED-ATTEMPT','checks':len(self.rows),'rows':self.rows,'error':error,'seconds':time.monotonic()-self.start,'environment':environment(),'scope':'Only new helper-entry/open-attempt controls; no old campaign credit','full_public_negative_derivations':0,'independent_closure':'PENDING',**kw})
def guard(root,out,r):
 root=Path(root).resolve();out=Path(out).resolve()
 assert sys.getprofile() is None,'Existing profiler; no replacement'
 apps={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'};protected={};captures=[];target=None
 allowed={'_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>'}
 def audit(e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in apps:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC')
   protected[a[0].co_filename]=True
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();flags=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  if event=='return':
   if target is not None and frame.f_code is target._basis.__code__ and type(arg) is dict:
    captures.append(arg);r.event('actual-authenticated-basis-returned')
  elif event=='call':
   c=frame.f_code
   if c.co_filename in protected and c.co_flags&2 and c.co_name not in allowed:raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
   if c.co_name=='validate' and c.co_filename.endswith('/code/correspondence.py'):CALLS.append({'file':c.co_filename,'function':c.co_name})
 def monitor(m):
  nonlocal target;target=m;sys.setprofile(profile)
 return monitor,captures
