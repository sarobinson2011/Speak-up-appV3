"""Engineering focused offline control infrastructure. Saved inputs only; no operational entry calls."""
from pathlib import Path
import hashlib,json,os,sys,types,importlib.metadata,time,traceback

def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(path):
 m=types.ModuleType('independent_client_state');m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
CALLS=[]
def guard(root,output=None):
 root=Path(root).resolve();output=Path(output).resolve() if output is not None else None;sm=sys.monitoring;assert sm.get_tool(4) is None;sm.use_tool_id(4,'engineering-token-correspondence')
 forbidden={'main','run','run_controlled','_run','_dispatch','__init__','state','handle','status','_load_launcher','_fail','_data'}
 def start(code,offset):
  if code.co_filename.rsplit('/',1)[-1]=='prospective_entry.py' and code.co_name in forbidden:raise AssertionError('PROHIBITED-APPLICATION-CALL:'+code.co_name)
  CALLS.append({'function':code.co_name,'file':code.co_filename})
 sm.register_callback(4,sm.events.PY_START,start)
 def protect(code):
  if code.co_name in forbidden:sm.set_local_events(4,code,sm.events.PY_START)
  for v in code.co_consts:
   if isinstance(v,types.CodeType):protect(v)
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PROHIBITED-SOURCE-EXECUTION')
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1]=='prospective_entry.py':protect(args[0])
  if event=='open' and isinstance(args[0],(str,bytes)):
   p=str(Path(os.fsdecode(args[0])).absolute());flags=args[2] or 0
   if p.startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if p.startswith(str(root)+'/') and not (output is not None and p.startswith(str(output)+'/')) and flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('PROHIBITED-INPUT-WRITE')
 sys.addaudithook(audit)
 def returned(code,offset,value):
  if code.co_name=='inputs' and type(value) is dict and 'prior_module' in value:
   for name in ('derive_status','derive_client_state','derive_client','derive_handle'):
    fn=getattr(value['prior_module'],name,None)
    if fn:sm.set_local_events(4,fn.__code__,sm.events.PY_START)
 sm.register_callback(4,sm.events.PY_RETURN,returned)
 def monitor(m):
  for name in ('semantic','derive_token','validate','_checked','_basis','constructed_projection'):
   sm.set_local_events(4,getattr(m,name).__code__,sm.events.PY_START)
  sm.set_local_events(4,m.inputs.__code__,sm.events.PY_RETURN)
 return monitor

def env():return {'python':sys.version,'implementation':sys.implementation.name,'optimization':sys.flags.optimize,'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'cryptography':importlib.metadata.version('cryptography')}
class Record:
 def __init__(self,p):self.path=Path(p);self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def check(self,label,fn):
  v=fn();assert v is not False,label;self.row(label,'PASS');return v
 def row(self,label,result,**kw):
  d={'check':label,'result':result,**kw};self.rows.append(d)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
  print(len(self.rows),label,result,flush=True)
 def reject(self,label,fn,reason=None):
  try:fn()
  except ValueError as e:
   if reason is not None:assert reason in str(e),(label,str(e),reason)
   self.row(label,'REJECTED',error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 def save(self,n,v): (self.path/n).write_bytes(enc(v))
 def finish(self,error=None,**extra):
  self.save('calls.json',CALLS)
  self.save('RESULT.json',{'result':('COMPLETED_WITH_FINDINGS' if extra.get('findings') else 'PASS') if error is None else 'FAIL','checks':len(self.rows),'rows':self.rows,'error':error,'seconds':time.monotonic()-self.start,'environment':env(),'requests':0,'database_connections':0,'session_operations':0,'runtime_session_methods_invoked':False,'constructed_not_runtime':True,**extra})

def verify_root(root):
 """Exact recovered filesystem membership before consuming candidate code."""
 import stat
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode)
 p=root/'MANIFEST.json';assert stat.S_ISREG(p.lstat().st_mode);manifest=json.loads(p.read_bytes());expected=set(manifest)|{'MANIFEST.json'}
 dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
 assert files==expected and seen==dirs
 for n,pin in manifest.items():assert identity((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'membership_and_types':'PASS','all_hashes':'PASS'}
