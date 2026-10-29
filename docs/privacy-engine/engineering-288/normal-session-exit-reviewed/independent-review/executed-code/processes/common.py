"""Formal-Lab[6] independent saved-input review infrastructure; no application execution."""
import collections,hashlib,importlib.metadata,json,os,stat,sys,time,traceback,types
from pathlib import Path

def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p):
 m=types.ModuleType('formal_lab6_normal_exit');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def environment():return {'python':sys.version,'implementation':sys.implementation.name,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'optimization':sys.flags.optimize,'dont_write_bytecode':sys.dont_write_bytecode}
CALLS=collections.Counter()
def guard(root):
 root=Path(root).resolve();sm=sys.monitoring;assert sm.get_tool(4) is None;sm.use_tool_id(4,'Formal-Lab6-normal-exit')
 forbidden={'main','run','run_controlled','_run','_dispatch','__init__','state','handle','status','_load_launcher','_fail','_data'}
 watched={'_checked','_assemble','_basis','derive_status','derive_token','derive_exit','semantic','constructed_projection','validate'}
 def start(code,offset):
  if code.co_filename.rsplit('/',1)[-1]=='prospective_entry.py' and code.co_name in forbidden:raise AssertionError('PROHIBITED-APPLICATION:'+code.co_name)
  CALLS[(code.co_filename,code.co_name)]+=1
 sm.register_callback(4,sm.events.PY_START,start)
 def instrument(code):
  file=code.co_filename.rsplit('/',1)[-1]
  if file=='prospective_entry.py' and code.co_name in forbidden or file=='correspondence.py' and code.co_name in watched:sm.set_local_events(4,code,sm.events.PY_START)
  for v in code.co_consts:
   if isinstance(v,types.CodeType):instrument(v)
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec':
   if args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PROHIBITED-SOURCE-EXECUTION')
   instrument(args[0])
  if event=='open' and isinstance(args[0],(str,bytes)):
   p=Path(os.fsdecode(args[0])).absolute();flags=args[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-PATH')
   if flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT) and not p.is_relative_to(Path(__file__).resolve().parents[1]):raise AssertionError('PROHIBITED-NONREVIEW-WRITE:'+str(p))
 sys.addaudithook(audit)
def verify_root(root):
 root=Path(root);manifest=json.loads((root/'MANIFEST.json').read_bytes());expected=set(manifest)|{'MANIFEST.json'};dirs={str(p) for n in expected for p in Path(n).parents if str(p)!='.'};files=set();actual_dirs=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);actual_dirs.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
 assert files==expected and actual_dirs==dirs
 for n,pin in manifest.items():assert ident((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'membership_types_and_hashes':'PASS'}
class Record:
 def __init__(self,p):self.path=Path(p);self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.started=time.monotonic()
 def save(self,n,v):(self.path/n).write_bytes(enc(v))
 def row(self,label,result,**kw):
  row={'check':label,'result':result,**kw};self.rows.append(row)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(len(self.rows),label,result,flush=True)
 def check(self,label,fn):
  v=fn();assert v is not False,label;self.row(label,'PASS');return v
 def reject(self,label,fn):
  try:fn()
  except ValueError as e:self.row(label,'REJECTED',error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 def finish(self,error=None,**kw):
  self.save('calls.json',[{'file':f,'function':n,'calls':v} for (f,n),v in sorted(CALLS.items())])
  self.save('RESULT.json',{'result':'PASS' if error is None else 'FAIL','checks':len(self.rows),'rows':self.rows,'outcomes':dict(collections.Counter(x['result'] for x in self.rows)),'error':error,'seconds':time.monotonic()-self.started,'environment':environment(),'runtime_session_operations':0,'database_connections':0,'saved_inputs_only':True,**kw})
