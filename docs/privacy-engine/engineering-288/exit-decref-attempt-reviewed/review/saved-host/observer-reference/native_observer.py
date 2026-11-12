"""Filtered delivery to original guard/accounting/capture semantics. Harness only."""
from pathlib import Path
import sys,time,importlib.util,hashlib
HERE=Path(__file__).resolve().parent
binary=HERE/'_event_filter.cpython-312-x86_64-linux-gnu.so'
assert hashlib.sha256(binary.read_bytes()).hexdigest()=='36d7f88ac907b39dab2576d3122e6038afc2f7803b5fd6abe7f92e4b7ae29e3f','FILTER-BINARY-IDENTITY'
spec=importlib.util.spec_from_file_location('_event_filter',binary);native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
spec2=importlib.util.spec_from_file_location('_observer_support',HERE/'observer.py');support=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(support)

class Observer(support.Observer):
 def __init__(self,*args):
  super().__init__(*args);self.lease=None;self.callback=self.profile;self.closed=False
  self.phase_names={'validate','inputs','catalogue','dependencies','_basis','_public_predecessor','_construct_checked','derive','expected'}
 def start(self,m):
  assert sys.version_info[:3]==(3,12,14),'Retained CPython 3.12.14 required'
  assert sys.getprofile() is None and sys.gettrace() is None,'Observer conflict'
  self.target=m;self.target_code=m._basis.__code__;self.cache.clear()
  self.lease=native.install(self.callback,self.target_code,self.protected,self.phase_names,self.root+'/')
 def profile(self,frame,event,arg):
  # These three consumers preserve the original tests/common.py predicates.
  if event=='return':
   if self.target is not None and frame.f_code is self.target._basis.__code__ and type(arg) is dict:
    self.captures.append(arg);self.r.event('actual-authenticated-basis-returned',capture_count=len(self.captures),meaning='Exact returned object; public receipt comparison still required')
  elif event=='call':
   c=frame.f_code
   if c.co_filename in self.protected and c.co_flags&2 and c.co_name not in self.allowed:raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
   if c.co_name=='validate' and c.co_filename.endswith('/code/correspondence.py'):self.calls.append({'file':c.co_filename,'function':c.co_name})
  c=frame.f_code
  if c.co_filename.startswith(self.root+'/') and c.co_name in self.phase_names:
   key=c.co_filename[len(self.root)+1:]+'::'+c.co_name+':'+str(c.co_firstlineno)
   if event=='call':
    self.entered[key]=self.entered.get(key,0)+1;self.frames[id(frame)]=(key,False)
    if c.co_name=='validate':self.r.event('public-validator-entered',source=key,entry_count=self.entered[key],meaning='Entry only; not acceptance')
   elif event=='return':
    self.frames.pop(id(frame),None);dest=self.abrupt if arg is None else self.returned;dest[key]=dest.get(key,0)+1
    if c.co_name=='validate':self.r.event('public-validator-departed',source=key,departure='None-or-exception-qualified' if arg is None else 'returned-value',result=arg.get('result') if type(arg) is dict else None)
   self.progress()
 def close(self):
  if self.closed:return
  if self.lease is not None:
   removed=native.stop(self.lease);self.r.event('native-observer-stop',owned_hook_removed=removed,qualification='False means hook already absent; not complete cleanup or reuse proof')
  self.progress(force=True);self.closed=True
