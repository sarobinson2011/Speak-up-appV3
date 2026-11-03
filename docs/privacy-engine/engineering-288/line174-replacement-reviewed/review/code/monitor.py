"""New slot1 real CPython API tests with expressly synthetic predecessors.
These checks authenticate no receipt and execute no application/session source.
"""
from pathlib import Path
import sys,ast,types,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);error=None;sm=sys.monitoring
class Injected(RuntimeError):pass
def main():
 r.save('input-verification.json',verify_root(root));m=module(root/'code/correspondence.py');layer='real CPython3.12 monitoring API; synthetic predecessor, not authentication'
 def fake(mode='normal'):
  p=types.SimpleNamespace();assembled={'synthetic':'not authenticated evidence'}
  def basis(data):return {'fresh':{},'marker':'synthetic'}
  p._basis=basis;p.enc=m.enc;p._rows=lambda b:[];p._assemble=lambda d,rows,b:({'wrong':True} if mode=='wrong-assembly' else assembled)
  data={'prior_module':p,'prior_root':root,'prior_saved':m.enc(assembled)}
  def validate(root,saved):
   if mode=='validation-failure':raise Injected('predecessor failure')
   if mode=='nested':
    marker=sm.get_tool(1)
    try:m._public_predecessor(data)
    except ValueError as e:assert str(e)=='WC-MONITORING-CONTENTION' and sm.get_tool(1) is marker
    else:raise AssertionError('nested ownership accepted')
   if mode!='missing':p._basis({})
   if mode=='extra':p._basis({})
   return {'result':'PASS','contexts':list(m.CONTEXTS),'receipt':m.PREDECESSOR_RECEIPT.copy()}
  p.validate=validate;return data
 def state(p):
  result={'owner':sm.get_tool(1),'global':sm.get_events(1),'local':sm.get_local_events(1,p._basis.__code__)}
  cb=sm.register_callback(1,sm.events.PY_RETURN,None)
  if cb is not None:sm.register_callback(1,sm.events.PY_RETURN,cb)
  result['callback']=cb;return result
 def clean(p):return state(p)=={'owner':None,'global':0,'local':0,'callback':None}
 def expect(fn,typ,part=None):
  try:fn()
  except typ as e:
   if part:assert part in str(e),(part,str(e))
   return str(e)
  raise AssertionError('expected intended exception')
 for mode in ('normal','nested','missing','extra','wrong-assembly','validation-failure'):
  d=fake(mode);p=d['prior_module']
  def trial(d=d,p=p,mode=mode):
   if mode in ('normal','nested'):assert m._public_predecessor(d)[0]['marker']=='synthetic'
   else:expect(lambda:m._public_predecessor(d),Injected if mode=='validation-failure' else ValueError,{'missing':'WC-PUBLIC-PREDECESSOR-RESULT','extra':'WC-UNEXPECTED-BASIS-RETURN','wrong-assembly':'WC-AUTHENTICATED-BASIS-RECEIPT'}.get(mode))
   assert clean(p);return True
  r.yes(mode+' path releases own monitoring state',trial,layer)
 # Interrupt after successful C returns, before the next Python statement.
 for api in (sm.use_tool_id,sm.register_callback,sm.set_local_events):
  d=fake();p=d['prior_module'];hit=[]
  def profile(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='c_return' and arg is api:
    sys.setprofile(None);hit.append(api.__name__);raise Injected('after '+api.__name__)
  def trial():
   sys.setprofile(profile)
   try:expect(lambda:m._public_predecessor(d),Injected,'after '+api.__name__)
   finally:sys.setprofile(None)
   assert hit==[api.__name__] and clean(p)
   # Mechanism reuse only. Actual authenticated public validation is separate.
   assert m._public_predecessor(d)[0]['marker']=='synthetic' and clean(p)
   return True
  r.yes('C-return interruption after '+api.__name__+' and synthetic reuse',trial,layer)
 # Failed acquisition must preserve foreign ownership, events and callback.
 for mode in ('preexisting','race-different','race-equal-distinct'):
  d=fake();p=d['prior_module'];foreign=[];hit=[]
  def cb(*args):return None
  def install(marker):
   sm.use_tool_id(1,marker);sm.register_callback(1,sm.events.PY_RETURN,cb);sm.set_events(1,sm.events.PY_RETURN);sm.set_local_events(1,p._basis.__code__,sm.events.PY_RETURN);foreign.append(marker)
  def profile(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='c_call' and arg is sm.use_tool_id:
    sys.setprofile(None);lease=frame.f_locals['lease'];marker=('!'+lease)[1:] if mode=='race-equal-distinct' else 'foreign-race'
    if mode=='race-equal-distinct':assert marker==lease and marker is not lease
    install(marker);hit.append(True)
  def trial():
   if mode=='preexisting':install('foreign-preexisting')
   else:sys.setprofile(profile)
   try:
    expect(lambda:m._public_predecessor(d),ValueError)
    st=state(p);assert st['owner'] is foreign[0] and st['global']==st['local']==sm.events.PY_RETURN and st['callback'] is cb
    if mode!='preexisting':assert hit==[True]
    return True
   finally:
    sys.setprofile(None)
    if foreign and sm.get_tool(1) is foreign[0]:sm.set_local_events(1,p._basis.__code__,0);sm.set_events(1,0);sm.register_callback(1,sm.events.PY_RETURN,None);sm.free_tool_id(1)
  r.yes(mode+' leaves foreign reservation and monitoring state intact',trial,layer)
 # One qualified cleanup-interruption observation: do not call a free slot complete cleanup.
 d=fake('validation-failure');p=d['prior_module'];lines=(root/'code/correspondence.py').read_text().splitlines();line=next(i+1 for i,s in enumerate(lines) if 'sm.set_local_events(1,basis_code,0)' in s);hits=[]
 def trace(frame,event,arg):
  if frame.f_code is m._public_predecessor.__code__ and event=='line' and frame.f_lineno==line:
   sys.settrace(None);hits.append(line);raise Injected('cleanup local reset interrupted')
  return trace
 sys.settrace(trace)
 try:observed=expect(lambda:m._public_predecessor(d),Injected,'cleanup local reset interrupted')
 finally:sys.settrace(None)
 st=state(p);assert hits==[line] and st['owner'] is None and st['callback'] is None and st['local']==sm.events.PY_RETURN
 r.save('qualified-cleanup-interruption.json',{'result':'QUALIFIED-OBSERVATION','error':observed,'owner_free':True,'callback_cleared':True,'local_events_remain':st['local'],'successful_complete_cleanup':False,'synthetic_predecessor':True,'actual_authentication':False,'reviewer_clears_remaining_test_local_events_after_observation':False})
 r.row('cleanup interruption leaves local monitoring state despite free slot','QUALIFIED',layer=layer)
 # Deliberately retain qualified local bits until this isolated process ends.
 # No reviewer release or same-process authenticated reuse is claimed.
 r.save('final-verification.json',verify_root(root))
 r.save('limits.json',{'actual_authenticated_public_validation':False,'real_monitoring_API':True,'synthetic_predecessors':True,'slots2_3_4_5_campaigns_replayed':False,'qualified_cleanup_rows':1,'repeated_cleanup_interruption':'UNESTABLISHED','termination_cleanup':'UNESTABLISHED','alternate_interpreters':'UNQUALIFIED','hostile_replacement':'OUTSIDE cooperative contract'})
try:main()
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='New slot1 mechanism only; qualified cleanup interruption remains separate')
