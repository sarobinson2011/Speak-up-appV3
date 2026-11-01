"""Real monitoring API, explicitly synthetic predecessor; no application calls."""
import ast,copy,sys,types,traceback
from pathlib import Path

def toy(m,root,mode='normal',error=None):
 counts={'public':0,'basis':0};value={'fresh':{},'marker':'LD01-synthetic-basis'}
 def basis():
  counts['basis']+=1
  if mode=='basis-failure':raise error
  return value
 public={'result':'PASS','contexts':list(m.CONTEXTS),'receipt':copy.deepcopy(m.PREDECESSOR_RECEIPT)}
 def validate(root,saved):
  counts['public']+=1
  if mode=='predecessor-failure':raise error
  if mode!='missing-basis':basis()
  return public
 p=types.SimpleNamespace(_basis=basis,validate=validate,_rows=lambda b:[],_assemble=lambda f,r,b:b'LD01-toy',enc=lambda x:x)
 return {'prior_module':p,'prior_root':root,'prior_saved':b'LD01-toy'},counts,public,value

def boundaries(m):
 tree=ast.parse(Path(m.__file__).read_bytes());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor')
 region=next(n for n in fn.body if isinstance(n,ast.Try));capture=next(n for n in region.body if isinstance(n,ast.FunctionDef))
 def call_line(name):
  return next(n.lineno for n in region.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr==name)
 return {'captures':next(n.lineno for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='captures' for t in n.targets)),
  'lease':next(n.lineno for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='lease' for t in n.targets)),
  'try':region.lineno,'acquire':call_line('use_tool_id'),'capture':capture.lineno,'register':call_line('register_callback'),'local':call_line('set_local_events'),
  'predecessor':next(n.lineno for n in region.body if isinstance(n,ast.Assign))}

def interrupt(m,data,*,line=None,c_event=None,c_name=None,occurrence=1,before_raise=None,error=None):
 """One source-line or C API call boundary; restores only reviewer hooks."""
 error=error or KeyboardInterrupt('LD01-CONSTRUCTED-INTERRUPTION');seen={};count=0;old_trace=sys.gettrace();old_profile=sys.getprofile()
 def inject(frame,event,arg):
  nonlocal count
  match=frame.f_code is m._public_predecessor.__code__ and ((line is not None and event=='line' and frame.f_lineno==line) or (c_event is not None and event==c_event and getattr(arg,'__name__',None)==c_name))
  if match:
   count+=1
   if count==occurrence:
    if before_raise:before_raise(frame)
    seen.update({'line':frame.f_lineno,'offset':frame.f_lasti,'event':event,'c_function':getattr(arg,'__name__',None) if c_event else None,'owner_before':sys.monitoring.get_tool(2),'lease_in_frame':frame.f_locals.get('lease'),'owner_is_invocation_marker':sys.monitoring.get_tool(2) is frame.f_locals.get('lease') and 'lease' in frame.f_locals})
    raise error
  return inject
 caught=None
 try:
  if line is not None:sys.settrace(inject)
  else:sys.setprofile(inject)
  try:m._public_predecessor(data)
  except BaseException as e:caught=e;seen['traceback']=traceback.format_exc()
 finally:
  sys.settrace(old_trace);sys.setprofile(old_profile)
 assert seen and caught is error,(seen,caught)
 return seen

def state(data,probe=True):
 sm=sys.monitoring;v={'owner':sm.get_tool(2),'global_events':sm.get_events(2),'local_events':sm.get_local_events(2,data['prior_module']._basis.__code__)}
 if probe:
  previous=sm.register_callback(2,sm.events.PY_RETURN,None)
  v['callback_was_absent']=previous is None
  v['probe_changed_callback']=previous is not None
  if previous is not None:sm.register_callback(2,sm.events.PY_RETURN,previous)
 return v

def clean(v):return v['owner'] is None and v['global_events']==v['local_events']==0 and v['callback_was_absent'] is True and v['probe_changed_callback'] is False
