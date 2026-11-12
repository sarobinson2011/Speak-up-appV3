"""Proposed harness observer: Python call guards, selected local returns, no monitoring lease."""
from pathlib import Path
import os,sys,time

class Observer:
 def __init__(self,root,out,records,calls):
  assert sys.getprofile() is None,'Existing profiler; no replacement'
  assert sys.gettrace() is None,'Existing tracer; no replacement'
  self.root=str(Path(root).resolve());self.out=Path(out).resolve();self.r=records;self.calls=calls
  self.apps={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'}
  self.allowed={'_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>'}
  self.protected={};self.cache={};self.captures=[];self.target=None;self.target_code=None
  self.entered={};self.returned={};self.abrupt={};self.last_emit=time.monotonic();self.sequence=0
  self.trace_fn=self.trace;self.local_fn=self.local;self.frames={}
  sys.addaudithook(self.audit)
 def audit(self,e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in self.apps:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC')
   self.protected[a[0].co_filename]=True;self.cache.clear()
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();flags=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(self.out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 def classify(self,c):
  blocked=c.co_filename in self.protected and c.co_flags&2 and c.co_name not in self.allowed
  accounting=c.co_name=='validate' and c.co_filename.endswith('/code/correspondence.py')
  # Count actual computation, not timer heartbeats. Return/unwind records are not acceptance claims.
  selected=c.co_filename.startswith(self.root+'/') and (c.co_filename.endswith('/code/correspondence.py') and c.co_name in ('validate','inputs','catalogue','dependencies','_basis','_public_predecessor','_construct_checked') or c.co_filename.endswith('/guard_relationships.py') and c.co_name=='derive' or c.co_filename.endswith('/guard_oracle.py') and c.co_name=='expected')
  kind=(bool(blocked),accounting,selected,c is self.target_code)
  self.cache[id(c)]=(c,kind);return kind
 def trace(self,frame,event,arg):
  if event!='call':return None
  c=frame.f_code;cached=self.cache.get(id(c))
  kind=self.classify(c) if cached is None else cached[1]
  if kind[0]:raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
  if kind[1]:self.calls.append({'file':c.co_filename,'function':c.co_name})
  if not(kind[2] or kind[3]):return None
  key=c.co_filename[len(self.root)+1:]+'::'+c.co_name+':'+str(c.co_firstlineno)
  self.entered[key]=self.entered.get(key,0)+1;self.frames[id(frame)]=(key,False)
  frame.f_trace_lines=False;frame.f_trace_opcodes=False
  if kind[1]:self.r.event('public-validator-entered',source=key,entry_count=self.entered[key],meaning='Entry only; no validation outcome established')
  self.progress();return self.local_fn
 def local(self,frame,event,arg):
  state=self.frames.get(id(frame))
  if state is None:return self.local_fn
  key,exception=state
  if event=='exception':self.frames[id(frame)]=(key,True)
  elif event=='return':
   self.frames.pop(id(frame),None)
   # None following an exception is conservatively an abrupt/qualified departure.
   dest=self.abrupt if exception and arg is None else self.returned
   dest[key]=dest.get(key,0)+1
   if frame.f_code is self.target_code and type(arg) is dict:
    self.captures.append(arg);self.r.event('actual-authenticated-basis-returned',capture_count=len(self.captures),source=key,meaning='Exact object returned by the selected unchanged candidate _basis; public receipt comparison remains required')
   if frame.f_code.co_name=='validate':self.r.event('public-validator-departed',source=key,departure='exception-or-None-qualified' if exception and arg is None else 'return',result=arg.get('result') if type(arg) is dict else None)
   self.progress()
  return self.local_fn
 def progress(self,force=False):
  now=time.monotonic()
  if force or now-self.last_emit>=15:
   self.last_emit=now;self.sequence+=1
   self.r.event('computation-progress',sequence=self.sequence,entered=sum(self.entered.values()),returned=sum(self.returned.values()),abrupt_or_None_qualified=sum(self.abrupt.values()),active=len(self.frames),meaning='Actual selected source-function events; return is not acceptance or runtime execution evidence')
   self.r.save('phase-counts-%05d.json'%self.sequence,{'entered':self.entered,'returned':self.returned,'abrupt_or_None_qualified':self.abrupt,'active':list(self.frames.values())})
 def start(self,m):
  assert sys.getprofile() is None and sys.gettrace() is None,'Observer conflict'
  self.target=m;self.target_code=m._basis.__code__;self.cache.clear();sys.settrace(self.trace_fn)
 def close(self):
  current=sys.gettrace()
  if current is self.trace_fn:sys.settrace(None)
  elif current is not None:raise AssertionError('Observer replaced; foreign tracer preserved')
  assert sys.getprofile() is None,'Unexpected profiler; not removed'
  self.progress(force=True)
