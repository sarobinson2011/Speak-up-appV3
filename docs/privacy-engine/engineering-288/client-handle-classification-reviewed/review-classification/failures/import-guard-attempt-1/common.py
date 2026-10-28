"""Reviewer-only recording and nonexecuting-input guards."""
from pathlib import Path
import hashlib,json,os,sys,types,importlib.metadata

def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(path):
 m=types.ModuleType('independent_outside_classification');m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m

def guards(root):
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1].lower() in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py','prospective_entry.py'):raise AssertionError('APPLICATION-SOURCE-EXECUTION')
  if event=='open' and isinstance(args[0],(str,bytes)):
   p=os.fsdecode(args[0]);flags=args[2] or 0
   if p.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if p.startswith(str(root)+'/') and flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)

def monitor(adapter):
 # Local CPython events avoid tracing unrelated predecessor computation.
 calls=[];tool=4;sm=sys.monitoring;assert sm.get_tool(tool) is None;sm.use_tool_id(tool,'independent-correspondence-review')
 def start(code,offset):
  calls.append({'function':code.co_name,'file':code.co_filename})
 def returned(code,offset,value):
  if code.co_name=='inputs' and type(value) is dict:
   sm.set_local_events(tool,value['prior_module'].derive_handle.__code__,sm.events.PY_START)
 sm.register_callback(tool,sm.events.PY_START,start);sm.register_callback(tool,sm.events.PY_RETURN,returned)
 for name in ('semantic','derive_client','validate','_checked','_basis'):
  sm.set_local_events(tool,getattr(adapter,name).__code__,sm.events.PY_START)
 sm.set_local_events(tool,adapter.inputs.__code__,sm.events.PY_RETURN)
 return calls,lambda:sm.free_tool_id(tool)

def environment():return {'python':sys.version,'implementation':sys.implementation.name,'optimization':sys.flags.optimize,'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'cryptography':importlib.metadata.version('cryptography')}
class Record:
 def __init__(self,path):self.path=path;path.mkdir(parents=True,exist_ok=False);self.rows=[]
 def record(self,label,result,kind,**extra):
  row={'check':label,'result':result,'kind':kind,**extra};self.rows.append(row)
  with (self.path/'progress.jsonl').open('a') as h:h.write(json.dumps(row)+'\n')
 def check(self,label,fn,kind='independent'):
  v=fn();assert v is not False,label;self.record(label,'PASS',kind);return v
 def reject(self,label,fn,reason=None,kind='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError,IndexError) as e:
   if reason is not None:assert str(e)==reason,(label,str(e),reason)
   self.record(label,'REJECTED',kind,error={'type':type(e).__name__,'message':str(e)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 def finish(self,error=None,**extra):
  data={'result':'PASS' if error is None else 'FAIL','checks':len(self.rows),'rows':self.rows,'error':error,'environment':environment(),'requests':0,'database_connections':0,'session_operations':0,'runtime_sources_executed':False,'constructed_not_runtime':True,**extra};(self.path/'RESULT.json').write_text(json.dumps(data,indent=2)+'\n');return data
