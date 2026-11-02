"""Independent defining-source traversal and new-slot real API controls.
Synthetic predecessor checks are explicitly not source authentication.
"""
from pathlib import Path
import sys,ast,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None;sm=sys.monitoring
def fixture(m,mode='normal',hook=None):
 p=types.SimpleNamespace();counts={'validate':0,'basis':0};payload={'role':'synthetic-slot3-basis','nested':[1,2]};raw=m.enc(payload)
 def basis():counts['basis']+=1;return {'fresh':{},'payload':D(payload)}
 def validate(path,saved):
  counts['validate']+=1
  if hook:hook()
  if mode=='before':raise MemoryError('synthetic-predecessor-failure')
  if mode!='missing':basis()
  if mode=='extra':basis()
  if mode=='after':raise KeyboardInterrupt('synthetic-after-return')
  return {'result':'PASS','contexts':list(m.CONTEXTS),'receipt':D(m.PREDECESSOR_RECEIPT)}
 p._basis=basis;p.validate=validate;p._rows=lambda b:D(b['payload']);p._assemble=lambda f,rows,b:({'wrong':True} if mode=='altered' else rows);p.enc=m.enc
 return {'prior_module':p,'prior_root':'SYNTHETIC-NOT-AUTHENTICATED','prior_saved':raw},counts
def checked_clean(p):
 state={'owner':sm.get_tool(3),'global':sm.get_events(3),'local':sm.get_local_events(3,p._basis.__code__)}
 cb=sm.register_callback(3,sm.events.PY_RETURN,None)
 if cb is not None:sm.register_callback(3,sm.events.PY_RETURN,cb)
 state['callback_present']=cb is not None;return state=={'owner':None,'global':0,'local':0,'callback_present':False}
def release_foreign(p,owner):
 assert sm.get_tool(3) is owner;sm.set_events(3,0);sm.set_local_events(3,p._basis.__code__,0);sm.register_callback(3,sm.events.PY_RETURN,None);sm.free_tool_id(3)
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');d=m.inputs(root);raw=d['sources'][0]
 changed=raw.replace(b'if obj is not None:',b'if obj != None:');assert changed!=raw
 parent=D(d['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration'])
 def replace_excerpt(v):
  if type(v) is str:return v.replace('if obj is not None:', 'if obj != None:')
  if type(v) is list:return [replace_excerpt(x) for x in v]
  if type(v) is dict:return {k:replace_excerpt(x) for k,x in v.items()}
  return v
 parent['source']['stop_before']=replace_excerpt(parent['source']['stop_before'])
 parent['source']['sources']['launcher']=identity(changed);parent['source']['stop_before']['source']=identity(changed)
 r.no('unfinished repinned non-identity guard reaches grammar',lambda:d['coverage'].compile_cleanup_append(changed,*d['sources'][1:],parent,d['prior']['contexts'][0]['reference_declarations']),'CLEANUP-EXACT-NONNONE')
 # Only the new observer slot is exercised; closed slot2 campaign is reused.
 src=ast.parse((root/'code/correspondence.py').read_bytes());f=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');lease=next(n for n in f.body if isinstance(n,ast.Try));cleanup=lease.finalbody[0]
 r.yes('new outer slot3 lease starts inside try',lambda:ast.unparse(lease.body[0])=='sm.use_tool_id(3, lease)' and ast.unparse(cleanup.test)=='sm.get_tool(3) is lease')
 r.yes('nested cleanup covers masks callback reservation',lambda:ast.unparse(cleanup.body[0].body[0])=='sm.set_local_events(3, basis_code, 0)' and ast.unparse(cleanup.body[0].finalbody[0].body[0])=='sm.register_callback(3, sm.events.PY_RETURN, None)' and ast.unparse(cleanup.body[0].finalbody[0].finalbody[0])=='sm.free_tool_id(3)')
 observations={}
 data,counts=fixture(m);_,out=m._public_predecessor(data);r.yes('real slot3 normal synthetic capture',lambda:counts=={'validate':1,'basis':1} and checked_clean(data['prior_module']))
 for api,phase in [('use_tool_id','c_return'),('register_callback','c_return'),('set_local_events','c_return')]:
  data,counts=fixture(m);hit={};exc=MemoryError('FL6-slot3-'+api);caught=None;old=sys.getprofile()
  def profile(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event==phase and arg is getattr(sm,api) and not hit:
    hit.update(api=api,event=phase,line=frame.f_lineno,offset=frame.f_lasti,owner_is_marker=sm.get_tool(3) is frame.f_locals['lease']);raise exc
  try:
   sys.setprofile(profile)
   try:m._public_predecessor(data)
   except BaseException as e:caught=e
  finally:sys.setprofile(old)
  r.yes('slot3 interruption '+api,lambda:caught is exc and hit['owner_is_marker'] and counts['validate']==0 and checked_clean(data['prior_module']))
  observations[api]=hit
  _,out=m._public_predecessor(data);r.yes('same process synthetic reuse without reviewer release '+api,lambda:out['result']=='PASS' and checked_clean(data['prior_module']))
 # Real C-call race, including equal-valued distinct marker identity.
 for equal in (False,True):
  data,counts=fixture(m);hit={};old=sys.getprofile();caught=None
  def foreign_callback(*args):return None
  def race(frame,event,arg):
   if frame.f_code is m._public_predecessor.__code__ and event=='c_call' and arg is sm.use_tool_id and not hit:
    candidate=frame.f_locals['lease'];foreign=(candidate+'!')[:-1] if equal else 'FL6-foreign-slot3';assert foreign is not candidate;sm.use_tool_id(3,foreign);sm.set_events(3,sm.events.PY_RETURN);sm.set_local_events(3,data['prior_module']._basis.__code__,sm.events.PY_RETURN);sm.register_callback(3,sm.events.PY_RETURN,foreign_callback);hit.update(owner=foreign,equal_value=foreign==candidate)
  try:
   sys.setprofile(race)
   try:m._public_predecessor(data)
   except BaseException as e:caught=e
   finally:sys.setprofile(old)
   cb=sm.register_callback(3,sm.events.PY_RETURN,foreign_callback)
   r.yes('failed acquisition preserves foreign state equal='+str(equal),lambda:type(caught) is ValueError and 'already in use' in str(caught) and hit['equal_value']==equal and sm.get_tool(3) is hit['owner'] and cb is foreign_callback and sm.get_events(3)==sm.events.PY_RETURN and sm.get_local_events(3,data['prior_module']._basis.__code__)==sm.events.PY_RETURN and counts['validate']==0)
  finally:
   sys.setprofile(old)
   if hit:release_foreign(data['prior_module'],hit['owner'])
 # Distinct inner slot2 ownership must be unaffected by outer slot3 cleanup.
 foreign2='FL6-live-inner-slot2';sm.use_tool_id(2,foreign2)
 try:
  data,counts=fixture(m);m._public_predecessor(data);r.yes('outer slot3 preserves reserved slot2',lambda:sm.get_tool(2) is foreign2 and checked_clean(data['prior_module']))
 finally:assert sm.get_tool(2) is foreign2;sm.free_tool_id(2)
 for mode,code in [('missing','CLEANUP-PUBLIC-PREDECESSOR-RESULT'),('extra','CLEANUP-UNEXPECTED-BASIS-RETURN'),('altered','CLEANUP-AUTHENTICATED-BASIS-RECEIPT')]:
  data,counts=fixture(m,mode);r.no('synthetic missing extra or altered return '+mode,lambda:m._public_predecessor(data),code);r.yes('failed return binding cleanup '+mode,lambda:checked_clean(data['prior_module']))
 for mode in ('before','after'):
  data,counts=fixture(m,mode);caught=None
  try:m._public_predecessor(data)
  except BaseException as e:caught=e
  r.yes('synthetic predecessor exception cleanup '+mode,lambda:caught is not None and checked_clean(data['prior_module']))
 r.save('monitor-observations.json',observations);r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='Independent source/AST controls and real slot3 API checks with synthetic predecessors; not actual predecessor authentication; inherited LD01 controls not replayed')
