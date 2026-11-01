from pathlib import Path
import sys,ast,traceback,copy
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from lease_probe import *
from synthetic import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);failure=None;sm=sys.monitoring
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');observations={};tree=ast.parse((root/'code/correspondence.py').read_bytes());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');outer=next(n for n in f.body if isinstance(n,ast.Try));acquire=outer.body[0]
 r.yes('try covers use_tool_id before callback construction',lambda:ast.unparse(acquire)=='sm.use_tool_id(2, lease)' and any(isinstance(n,ast.FunctionDef) and n.name=='capture' for n in outer.body))
 pre=f.body[:f.body.index(outer)];r.yes('capture buffer code binding and marker prepared before acquisition',lambda:all(any(isinstance(t,ast.Name) and t.id==name for n in pre for t in ast.walk(n)) for name in ('captures','basis_code','lease')))
 guardnode=outer.finalbody[0];r.yes('release uses exact get_tool marker identity',lambda:ast.unparse(guardnode.test)=='sm.get_tool(2) is lease')
 first=guardnode.body[0];second=first.finalbody[0];r.yes('three cleanup attempts are nested in finally order',lambda:ast.unparse(first.body[0])=='sm.set_local_events(2, basis_code, 0)' and ast.unparse(second.body[0])=='sm.register_callback(2, sm.events.PY_RETURN, None)' and ast.unparse(second.finalbody[0])=='sm.free_tool_id(2)')
 r.yes('actual unchanged public validator and authenticated reassembly retained',lambda:'p.validate(data[\'prior_root\'], data[\'prior_saved\'])' in ast.unparse(outer) and 'DETAILS-AUTHENTICATED-BASIS-RECEIPT' in ast.unparse(f))
 # Normal API behavior and result isolation, using explicit synthetic predecessors.
 data,counts=fixture(m);b,result=m._public_predecessor(data)
 r.yes('synthetic successful one-return monitoring',lambda:counts=={'public':1,'basis':1} and result['result']=='PASS')
 r.yes('synthetic normal completion leaves checked state clean',lambda:clean(state(data['prior_module'])))
 result['contexts'].clear();result['nested']['values'].append('changed');b['payload']['roles'].clear();b2,result2=m._public_predecessor(data)
 r.yes('returned synthetic objects do not alter next expectations',lambda:result2['contexts']==list(m.CONTEXTS) and b2['payload']['roles']==['one','two'])
 # Pre-existing foreign owner: same process, real reservation/events/callback.
 data,counts=fixture(m);foreign=''.join(['FL6','-preexisting-owner']);seen=[]
 def cb(code,offset,value):
  if code is data['prior_module']._basis.__code__:seen.append(value)
 sm.use_tool_id(2,foreign);sm.register_callback(2,sm.events.PY_RETURN,cb);sm.set_events(2,sm.events.PY_RETURN);sm.set_local_events(2,data['prior_module']._basis.__code__,sm.events.PY_RETURN)
 try:
  r.no('pre-existing owner rejects before predecessor work',lambda:m._public_predecessor(data),'DETAILS-MONITORING-CONTENTION')
  r.yes('foreign reservation and exact marker object preserved',lambda:sm.get_tool(2) is foreign)
  r.yes('foreign global and local event masks preserved',lambda:sm.get_events(2)==sm.events.PY_RETURN and sm.get_local_events(2,data['prior_module']._basis.__code__)==sm.events.PY_RETURN)
  old=sm.register_callback(2,sm.events.PY_RETURN,cb);r.yes('foreign callback preserved',lambda:old is cb and counts['public']==0)
 finally:release_fixture(data['prior_module'],foreign)
 # Actual native acquisition races, entered after preflight but before the C call.
 for equal,hook in ((False,'line'),(True,'line'),(False,'c_call'),(True,'c_call')):
  data,counts=fixture(m);seen={};calls=[];profile=sys.getprofile();trace=sys.gettrace();caught=None
  def foreign_cb(*args):return None
  def acquire_foreign(frame):
   lease=frame.f_locals['lease'];owner=('!'+lease)[1:] if equal else 'FL6-racing-other-owner';assert owner is not lease
   sm.use_tool_id(2,owner);sm.register_callback(2,sm.events.PY_RETURN,foreign_cb);sm.set_events(2,sm.events.PY_RETURN);sm.set_local_events(2,data['prior_module']._basis.__code__,sm.events.PY_RETURN)
   seen.update({'marker':lease,'foreign':owner,'equal_value':owner==lease,'distinct_object':owner is not lease,'get_tool_is_foreign':sm.get_tool(2) is owner,'line':frame.f_lineno,'offset':frame.f_lasti,'hook':hook})
  def tr(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='line' and frame.f_lineno==acquire.lineno and not seen:acquire_foreign(frame)
   return tr
  def pr(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='c_call' and arg is sm.use_tool_id and not seen:acquire_foreign(frame)
  try:
   if hook=='line':sys.settrace(tr)
   else:sys.setprofile(pr)
   try:m._public_predecessor(data)
   except BaseException as e:caught=e
   finally:sys.settrace(trace);sys.setprofile(profile)
   label=str((equal,hook));r.yes('native failed acquisition '+label,lambda:type(caught) is ValueError and 'already in use' in str(caught) and bool(seen))
   r.yes('ownership discrimination despite equal values '+label,lambda:seen['equal_value']==equal and seen['distinct_object'] and seen['get_tool_is_foreign'] and sm.get_tool(2) is seen['foreign'])
   r.yes('failed acquisition preserves masks '+label,lambda:sm.get_events(2)==sm.events.PY_RETURN and sm.get_local_events(2,data['prior_module']._basis.__code__)==sm.events.PY_RETURN)
   old=sm.register_callback(2,sm.events.PY_RETURN,foreign_cb);r.yes('failed acquisition preserves callback and skips predecessor '+label,lambda:old is foreign_cb and counts=={'public':0,'basis':0})
   observations['race-'+label]={**seen,'error':str(caught),'layer':'Native use_tool_id failure; not public receipt validation','fixture_cleanup_only_after_preservation':True}
  finally:
   sys.settrace(trace);sys.setprofile(profile)
   if seen and sm.get_tool(2) is seen['foreign']:release_fixture(data['prior_module'],seen['foreign'])
 # Nested ownership: inner candidate must reject while leaving outer capture intact.
 inner,inner_counts=fixture(m);nested={}
 def nested_attempt():
  owner=sm.get_tool(2);old=sm.register_callback(2,sm.events.PY_RETURN,None);assert old is not None;sm.register_callback(2,sm.events.PY_RETURN,old)
  try:m._public_predecessor(inner)
  except ValueError as e:nested['error']=str(e)
  else:raise AssertionError('NESTED-ACCEPTED')
  previous=sm.register_callback(2,sm.events.PY_RETURN,old);nested.update({'owner_same':sm.get_tool(2) is owner,'callback_same':previous is old,'local_preserved':sm.get_local_events(2,outerdata['prior_module']._basis.__code__)==sm.events.PY_RETURN})
 outerdata,counts=fixture(m,on_validate=nested_attempt);_,v=m._public_predecessor(outerdata)
 r.yes('nested invocation rejects without disturbing outer lease',lambda:nested=={'error':'DETAILS-MONITORING-CONTENTION','owner_same':True,'callback_same':True,'local_preserved':True} and inner_counts['public']==0)
 r.yes('outer validator still captures normal return and cleans resources',lambda:v['result']=='PASS' and counts=={'public':1,'basis':1} and clean(state(outerdata['prior_module'])))
 # Native-call setup boundaries with partial callback/event state.
 for api,phase in (('register_callback','c_call'),('register_callback','c_return'),('set_local_events','c_call'),('set_local_events','c_return')):
  data,counts=fixture(m);profile=sys.getprofile();seen={};exc=MemoryError('FL6-partial-setup-'+api+'-'+phase);caught=None
  def interrupt_setup(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event==phase and arg is getattr(sm,api) and not seen:
    seen.update({'api':api,'phase':phase,'line':frame.f_lineno,'offset':frame.f_lasti,'owned':sm.get_tool(2) is frame.f_locals['lease'],'global':sm.get_events(2),'local':sm.get_local_events(2,data['prior_module']._basis.__code__)})
    raise exc
  try:
   sys.setprofile(interrupt_setup)
   try:m._public_predecessor(data)
   except BaseException as e:caught=e
  finally:sys.setprofile(profile)
  label=api+'-'+phase;r.yes('partial setup preserves original error '+label,lambda:caught is exc and seen['owned'])
  r.yes('partial setup cleans checked state '+label,lambda:clean(state(data['prior_module'])) and counts['public']==0)
  observations[label]=seen
 # Errors during real callback observation and synthetic predecessor execution.
 for mode,exc in [('before',RuntimeError('before-basis')),('after',KeyboardInterrupt('after-basis')),('after',SystemExit(17))]:
  exc.__cause__=ValueError('existing-explicit-cause');exc.__suppress_context__=True;cause=exc.__cause__;data,counts=fixture(m,mode,error=exc);caught=None
  try:m._public_predecessor(data)
  except BaseException as e:caught=e
  label=mode+'-'+type(exc).__name__;r.yes('predecessor error identity and existing cause retained '+label,lambda:caught is exc and caught.__cause__ is cause and caught.__suppress_context__ is True)
  r.yes('predecessor failure cleanup '+label,lambda:clean(state(data['prior_module'])))
 for mode,code in [('missing','DETAILS-PUBLIC-PREDECESSOR-RESULT'),('extra','DETAILS-UNEXPECTED-BASIS-RETURN'),('wrong-result','DETAILS-PUBLIC-PREDECESSOR-RESULT'),('wrong-basis','DETAILS-AUTHENTICATED-BASIS-RECEIPT')]:
  data,counts=fixture(m,mode);r.no('synthetic validation failure '+mode,lambda:m._public_predecessor(data),code);r.yes('validation failure releases checked state '+mode,lambda:clean(state(data['prior_module'])))
 r.save('observations.json',observations);r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='Fresh independent source and actual monitoring API controls using synthetic predecessors; no authenticated predecessor or runtime execution claim')
