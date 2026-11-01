"""Independent real-API lease probes; no candidate API/function replacement."""
import ast,sys,traceback

def points(m):
 tree=ast.parse(open(m.__file__,'rb').read());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor')
 capture=next(n for n in ast.walk(f) if isinstance(n,ast.FunctionDef) and n.name=='capture')
 return {'capture':capture.lineno,'function':f.lineno,'tries':[n.lineno for n in ast.walk(f) if isinstance(n,ast.Try)]}

def state(p):
 sm=sys.monitoring;v={'owner':sm.get_tool(2),'global_events':sm.get_events(2),'local_events':sm.get_local_events(2,p._basis.__code__)}
 old=sm.register_callback(2,sm.events.PY_RETURN,None);v['callback_present']=old is not None;v['probe_restored_found_callback']=False
 if old is not None:sm.register_callback(2,sm.events.PY_RETURN,old);v['probe_restored_found_callback']=True
 return v

def clean(v):return v['owner'] is None and v['global_events']==v['local_events']==0 and not v['callback_present']

def interrupt(m,data,mode,exc=None):
 target=m._public_predecessor.__code__;line=points(m)['capture'];seen=[];raised=exc or KeyboardInterrupt('Formal-Lab6 independent '+mode);oldtrace=sys.gettrace();oldprofile=sys.getprofile();sm=sys.monitoring
 def record(frame,event,api=None):
  marker=frame.f_locals.get('lease');owner=sm.get_tool(2);seen.append({'mode':mode,'event':event,'api':api,'file':frame.f_code.co_filename,'line':frame.f_lineno,'offset':frame.f_lasti,'marker_type':type(marker).__name__,'marker_present':marker is not None,'owner_is_marker':owner is marker,'owner':owner,'capture_defined':'capture' in frame.f_locals,'global_events':sm.get_events(2),'local_events':sm.get_local_events(2,data['prior_module']._basis.__code__)})
  raise raised
 def trace(frame,event,arg):
  if frame.f_code is target and event=='line' and frame.f_lineno==line and not seen:record(frame,event)
  return trace
 def profile(frame,event,arg):
  if frame.f_code is target and event=='c_return' and arg is sm.use_tool_id and not seen:record(frame,event,'use_tool_id')
 try:
  if mode=='source-boundary':sys.settrace(trace)
  elif mode=='c-return':sys.setprofile(profile)
  else:raise AssertionError(mode)
  try:m._public_predecessor(data)
  except BaseException as e:
   assert e is raised,(type(e),str(e));tb=traceback.format_exc()
  else:raise AssertionError('INTERRUPTION-NOT-REACHED')
 finally:sys.settrace(oldtrace);sys.setprofile(oldprofile)
 assert len(seen)==1,seen
 return {'observation':seen[0],'traceback':tb,'exception_preserved':True,'constructed':True,'candidate_replaced':False,'reviewer_release':False}
