from pathlib import Path
import sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from lease_cases import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);failure=None;sm=sys.monitoring
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');observations={}
 for equal_value in (False,True):
  data,counts,_,_=toy(m,root);seen={};old_profile=sys.getprofile();caught=None
  def callback(*args):return None
  def inject(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='c_call' and getattr(arg,'__name__',None)=='use_tool_id':
    marker=frame.f_locals['lease'];foreign=marker.encode().decode() if equal_value else 'LD01-real-acquisition-race'
    assert foreign is not marker
    sm.use_tool_id(2,foreign);sm.register_callback(2,sm.events.PY_RETURN,callback);sm.set_local_events(2,data['prior_module']._basis.__code__,sm.events.PY_RETURN);sm.set_events(2,sm.events.PY_RETURN)
    seen.update({'marker':marker,'foreign':foreign,'equal_value':foreign==marker,'line':frame.f_lineno,'offset':frame.f_lasti})
  try:
   sys.setprofile(inject)
   try:m._public_predecessor(data)
   except BaseException as e:caught=e
   finally:sys.setprofile(old_profile)
   r.yes('actual reservation call fails before acquisition '+str(equal_value),lambda:type(caught) is ValueError and bool(seen))
   r.yes('failed acquisition does not free foreign marker '+str(equal_value),lambda:sm.get_tool(2) is seen['foreign'])
   r.yes('failed acquisition preserves foreign event masks '+str(equal_value),lambda:sm.get_events(2)==sm.events.PY_RETURN and sm.get_local_events(2,data['prior_module']._basis.__code__)==sm.events.PY_RETURN)
   previous=sm.register_callback(2,sm.events.PY_RETURN,callback);r.yes('failed acquisition preserves foreign callback '+str(equal_value),lambda:previous is callback)
   r.yes('failed acquisition invokes no predecessor '+str(equal_value),lambda:counts=={'public':0,'basis':0})
   observations[str(equal_value)]={'injection':seen,'error':str(caught),'layer':'Real monitoring C API use_tool_id acquisition failure, after preflight; no predecessor validation','foreign_resources_preserved_before_fixture_cleanup':True}
  finally:
   sys.setprofile(old_profile)
   if seen and sm.get_tool(2) is seen['foreign']:
    sm.set_events(2,0);sm.set_local_events(2,data['prior_module']._basis.__code__,0);sm.register_callback(2,sm.events.PY_RETURN,None);sm.free_tool_id(2)
 r.save('observations.json',observations);r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='Separate LD01 actual acquisition-failure races with synthetic predecessor; preserves completed focused group without replay')
