from pathlib import Path
import sys,ast,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from lease_cases import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);failure=None;sm=sys.monitoring
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');points=boundaries(m);r.save('source-boundaries.json',points)
 old=(root/'retained/ld01-original/code/correspondence.py').read_bytes();new=(root/'code/correspondence.py').read_bytes();a=ast.parse(old);b=ast.parse(new)
 fa=next(n for n in a.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');fb=next(n for n in b.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor')
 r.yes('only _public_predecessor AST changed',lambda:[ast.dump(n) for n in a.body if n is not fa]==[ast.dump(n) for n in b.body if n is not fb])
 al=old.splitlines(keepends=True);bl=new.splitlines(keepends=True)
 r.yes('all bytes outside changed function unchanged',lambda:al[:fa.lineno-1]==bl[:fb.lineno-1] and al[fa.end_lineno:]==bl[fb.end_lineno:])
 old_try=next(n for n in fa.body if isinstance(n,ast.Try));new_try=next(n for n in fb.body if isinstance(n,ast.Try))
 r.yes('unchanged actual predecessor public call',lambda:ast.dump(old_try.body[-1])==ast.dump(new_try.body[-1]))
 r.yes('unchanged public result basis and receipt checks',lambda:[ast.dump(n) for n in fa.body[fa.body.index(old_try)+1:]]==[ast.dump(n) for n in fb.body[fb.body.index(new_try)+1:]])
 old_capture=next(n for n in fa.body if isinstance(n,ast.FunctionDef));new_capture=next(n for n in new_try.body if isinstance(n,ast.FunctionDef))
 r.yes('unchanged passive basis-return callback',lambda:ast.dump(old_capture)==ast.dump(new_capture))
 r.yes('reservation and callback setup inside protecting try',lambda:points['try']<points['acquire']<points['capture']<points['register']<points['local']<points['predecessor'])
 r.yes('marker and basis-code bookkeeping before acquisition',lambda:points['captures']<points['lease']<points['try'])
 # Check the recorded CPython profile's identity-preserving name API directly.
 marker='LD01-profile-name-'+str(id(r));sm.use_tool_id(2,marker)
 try:r.yes('recorded monitoring API returns identical reserved name object',lambda:sm.get_tool(2) is marker)
 finally:sm.free_tool_id(2)
 observations={}
 plans=[('line-'+k,{'line':v}) for k,v in points.items()]+[(event+'-'+name,{'c_event':event,'c_name':name}) for name in ('use_tool_id','register_callback','set_local_events') for event in ('c_call','c_return')]
 for label,kw in plans:
  data,counts,_,_=toy(m,root);seen=interrupt(m,data,**kw);after=state(data);observations[label]={'injection':seen,'after':after,'synthetic_calls':counts}
  r.yes('same interruption escapes after cleanup '+label,lambda seen=seen:bool(seen['traceback']))
  r.yes('candidate released lease callback and events '+label,lambda after=after:clean(after))
  r.yes('no synthetic predecessor execution before interrupted frontier '+label,lambda counts=counts:counts=={'public':0,'basis':0})
 for mode,exc in [('predecessor-failure',ValueError('LD01-TOY-FAILURE')),('predecessor-failure',KeyboardInterrupt('LD01-TOY-INTERRUPT')),('predecessor-failure',SystemExit('LD01-TOY-EXIT')),('basis-failure',KeyboardInterrupt('LD01-TOY-BASIS-INTERRUPT'))]:
  data,counts,_,_=toy(m,root,mode,exc);caught=None
  try:m._public_predecessor(data)
  except BaseException as e:caught=e
  after=state(data);r.yes('exact synthetic predecessor exception preserved '+mode+type(exc).__name__,lambda caught=caught,exc=exc:caught is exc);r.yes('release after synthetic predecessor exception '+mode+type(exc).__name__,lambda after=after:clean(after))
 data,counts,_,_=toy(m,root,'missing-basis');r.no('missing synthetic basis remains fail-closed',lambda:m._public_predecessor(data),'DETAILS-PUBLIC-PREDECESSOR-RESULT');r.yes('missing basis rejection releases lease',lambda:clean(state(data)))
 data,counts,public,value=toy(m,root);got=m._public_predecessor(data);r.yes('synthetic normal return captures exact basis',lambda:got[0] is value and counts=={'public':1,'basis':1});got[1]['contexts'].clear();r.yes('returned public metadata remains detached',lambda:public['contexts']==list(m.CONTEXTS));r.yes('normal synthetic completion releases lease',lambda:clean(state(data)))
 # Foreign ownership is measured before the harness releases its own fixture.
 def foreign_callback(*args):return None
 for label in ('existing','before-acquisition','equal-valued-marker'):
  data,counts,_,_=toy(m,root);foreign={}
  def reserve(frame=None):
   name='LD01-foreign-owner' if label!='equal-valued-marker' else frame.f_locals['lease'].encode().decode()
   if frame is not None and label=='equal-valued-marker':assert name==frame.f_locals['lease'] and name is not frame.f_locals['lease']
   foreign['name']=name;sm.use_tool_id(2,name);sm.register_callback(2,sm.events.PY_RETURN,foreign_callback);sm.set_local_events(2,data['prior_module']._basis.__code__,sm.events.PY_RETURN);sm.set_events(2,sm.events.PY_RETURN)
  try:
   if label=='existing':reserve();r.no('genuine contention preserves gate',lambda:m._public_predecessor(data),'DETAILS-MONITORING-CONTENTION')
   else:observations[label]={'injection':interrupt(m,data,c_event='c_call',c_name='use_tool_id',before_raise=reserve)}
   r.yes('foreign lease survives '+label,lambda:sm.get_tool(2) is foreign['name'])
   r.yes('foreign global and local events unchanged '+label,lambda:sm.get_events(2)==sm.events.PY_RETURN and sm.get_local_events(2,data['prior_module']._basis.__code__)==sm.events.PY_RETURN)
   previous=sm.register_callback(2,sm.events.PY_RETURN,foreign_callback);r.yes('foreign callback unchanged '+label,lambda:previous is foreign_callback)
   r.yes('foreign reservation prevents predecessor call '+label,lambda:counts=={'public':0,'basis':0})
  finally:
   if 'name' in foreign and sm.get_tool(2) is foreign['name']:
    sm.set_events(2,0);sm.set_local_events(2,data['prior_module']._basis.__code__,0);sm.register_callback(2,sm.events.PY_RETURN,None);sm.free_tool_id(2)
 # Reentrancy: the inner invocation rejects, preserving the outer marker.
 data,counts,_,_=toy(m,root);original=data['prior_module'].validate;seen={}
 def nested(root_,saved):
  marker=sm.get_tool(2)
  try:m._public_predecessor(data)
  except ValueError as e:seen.update({'error':str(e),'owner_preserved':sm.get_tool(2) is marker})
  return original(root_,saved)
 data['prior_module'].validate=nested;m._public_predecessor(data)
 r.yes('nested invocation cannot release outer lease',lambda:seen=={'error':'DETAILS-MONITORING-CONTENTION','owner_preserved':True});r.yes('outer owner releases normally',lambda:clean(state(data)))
 r.save('observations.json',observations);r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='LD01 source wiring and real-monitoring controls with synthetic predecessor only; no full predecessor authentication',candidate_cleanup_required=True,prior_campaigns_replayed=False)
