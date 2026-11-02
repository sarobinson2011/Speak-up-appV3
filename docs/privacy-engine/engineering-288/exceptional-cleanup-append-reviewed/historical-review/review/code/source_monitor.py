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
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');d=m.inputs(root);cat=m.catalogue(d);raw=d['sources'][0];text=raw.decode();t=ast.parse(raw)
 fn=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='_session');outer=fn.body[-1];tr=outer.body[-1];handler=tr.handlers[0];details,loop=handler.body[:2];guardnode=loop.body[0];shared=guardnode.body[0];close,append=shared.body;call=append.value;sub=call.func.value;item=call.args[0]
 r.yes('defining handler retains active BaseException e',lambda:handler.name=='e' and ast.unparse(handler.type)=='BaseException' and isinstance(handler.body[-1],ast.Raise) and handler.body[-1].exc is None)
 r.yes('ordered loop inputs and tuple target from source',lambda:ast.unparse(loop.iter)=="[('raw', raw), ('managed', managed)]" and ast.unparse(loop.target)=='(name, obj)')
 r.yes('raw exactly None conditional post-yield prefix',lambda:any(ast.unparse(n)=='raw = None' for n in outer.body) and ast.unparse(tr.body[0].body[3])=='raw = None' and ast.unparse(tr.body[0].body[2])=='raw.close()')
 r.yes('selected handoff and manager are source-local bindings',lambda:ast.unparse(tr.body[1])=="managed, _ = open_session(c, db, cfg['config'], ownership_path=owners)" and ast.unparse(tr.body[-4])=='yield ManagedSession(managed)')
 r.yes('exact identity non-None guard, no truthiness',lambda:isinstance(guardnode.test.ops[0],ast.IsNot) and guardnode.test.comparators[0].value is None and ast.unparse(guardnode.test.left)=='obj')
 r.yes('close and append in same try; line172 excluded',lambda:len(shared.body)==2 and shared.handlers[0].name=='close_error' and shared.handlers[0].lineno==172 and close.lineno==append.lineno==171)
 r.yes('append callable evaluated before exact list arguments',lambda:ast.unparse(sub)=="details['cleanup']" and ast.unparse(call.func)=="details['cleanup'].append" and [ast.unparse(n) for n in item.elts]==['name',"'close returned'"])
 r.yes('details dynamic origins and exact False constants preserved',lambda:[ast.unparse(v) for v in details.value.values]==['type(e).__name__','str(e)','traceback.format_exc()','False','False','[]'])
 points=[loop.iter]
 for pair in loop.iter.elts:points.extend([pair.elts[0],pair.elts[1],pair])
 points.extend([loop.iter,loop])
 for _ in loop.iter.elts:points.extend([loop,*loop.target.elts,guardnode.test.left,guardnode.test.comparators[0],guardnode.test])
 points.extend([shared,close.value.func.value,close.value.func,close.value,close,sub.value,sub.slice,sub,call.func,*item.elts,item,call,append])
 assert len(points)==len(ORDER)==35
 locations={}
 for name,node in zip(ORDER,points):
  observed=cat['source']['stages'][name];want={'site':f'{node.lineno}:{node.col_offset}:{node.end_lineno}:{node.end_col_offset}:{type(node).__name__}','expression':ast.get_source_segment(text,node)}
  assert all(observed[k]==v for k,v in want.items());locations[name]=want
  r.yes('source coordinates and evaluation stage '+name,lambda observed=observed:observed['source']==identity(raw))
 r.save('independent-stage-expectations.json',locations)
 r.yes('catalogue order and all UNKNOWN dispositions',lambda:cat['source']['order']==ORDER and [x['id'] for x in cat['declarations']]==ORDER and all(x['classification']=='UNKNOWN' and x['multiplicity'] is x['ordinal'] is None for x in cat['declarations']))
 r.yes('protected-region attribution derived from enclosing AST',lambda:all(cat['source']['stages'][n]['semantic_region']==('protected-close' if n.startswith('close-') else 'protected-append' if n.startswith('append-') else 'try-entry' if n=='selected-try-entry' else 'loop-selection') for n in ORDER))
 r.yes('static compiler accepts exact candidate catalogue',lambda:d['coverage'].validate_cleanup_append(*d['sources'],d['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration'],d['prior']['contexts'][0]['reference_declarations'],cat))
 for field,new in [('guard_expression','bool(obj)'),('selected_name','raw'),('append_message','close failed'),('close_method','state')]:
  bad=change(cat,['source',field],new);r.no('static catalogue mutation '+field,lambda bad=bad:d['coverage'].validate_cleanup_append(*d['sources'],d['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration'],d['prior']['contexts'][0]['reference_declarations'],bad),'CLEANUP-SOURCE-CORRESPONDENCE')
 # Source-level guard mutation with the two immediate catalogue source pins
 # adjusted: rejection must reach source grammar, not only those pins.
 changed=raw.replace(b'if obj is not None:',b'if obj != None:');assert changed!=raw
 parent=D(d['prior']['contexts'][0]['launcher_initial_details_correspondence']['declaration']);parent['source']['sources']['launcher']=identity(changed);parent['source']['stop_before']['source']=identity(changed)
 # Changed source has the same loop start but different end column; derive that
 # one enclosing frontier from AST so the intended guard check is reached.
 ct=ast.parse(changed);cfn=next(n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name=='_session');cl=cfn.body[-1].body[-1].handlers[0].body[1]
 parent['source']['stop_before']['expression']=ast.get_source_segment(changed.decode(),cl)
 parent['source']['stop_before']['site']=f'{cl.lineno}:{cl.col_offset}:{cl.end_lineno}:{cl.end_col_offset}:{type(cl).__name__}'
 # Existing parent guards/continuations are structurally unchanged by this edit.
 r.no('repinned non-identity guard rejected by grammar',lambda:d['coverage'].compile_cleanup_append(changed,*d['sources'][1:],parent,d['prior']['contexts'][0]['reference_declarations']),'CLEANUP-EXACT-NONNONE')
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
