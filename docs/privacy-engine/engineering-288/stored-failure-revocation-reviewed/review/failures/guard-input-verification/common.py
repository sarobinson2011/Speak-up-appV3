from pathlib import Path
import os,sys,types,json,hashlib,copy,stat,time,traceback,importlib.metadata
sys.path.insert(0,str(Path(__file__).parent))
from integrity import root as verify_root,ident
D=copy.deepcopy
CALLS=[]
def module(p,name='reviewed_candidate'):
 p=Path(p);m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def environment():return {'python':sys.version,'cryptography':importlib.metadata.version('cryptography'),'isolated':sys.flags.isolated,'dont_write_bytecode':sys.dont_write_bytecode,'optimization':sys.flags.optimize}
def guard(root,out):
 root=Path(root).resolve();out=Path(out).resolve();sm=sys.monitoring;sm.use_tool_id(4,'Formal-Lab6-stored-failure')
 app={'prospective_entry.py','lab_bootstrap.py','live_connection.py','authority.py','worker.py'}
 def started(c,o):
  if Path(c.co_filename).name in app and c.co_flags & 2:raise AssertionError('PROHIBITED-RUNTIME:'+c.co_name)
  CALLS.append({'file':c.co_filename,'function':c.co_name})
 sm.register_callback(4,sm.events.PY_START,started)
 def protect(c):
  if c.co_flags & 2:sm.set_local_events(4,c,sm.events.PY_START)
  for v in c.co_consts:
   if isinstance(v,types.CodeType):protect(v)
 def audit(e,a):
  if e.startswith('sqlite3.connect') or e in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+e)
  if e=='exec' and Path(a[0].co_filename).name in app:
   if Path(a[0].co_filename).name!='prospective_entry.py':raise AssertionError('PROHIBITED-SOURCE-EXEC:'+a[0].co_filename)
   protect(a[0])
  if e=='open' and isinstance(a[0],(str,bytes)):
   p=Path(os.fsdecode(a[0])).absolute();f=a[2] or 0
   if str(p).startswith('/home/steve/'):raise AssertionError('PROHIBITED-HOST-ACCESS')
   if f&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC) and not p.is_relative_to(out):raise AssertionError('PROHIBITED-WRITE:'+str(p))
 sys.addaudithook(audit)
 def returned(c,o,v):
  if c.co_name=='inputs' and type(v) is dict and 'prior_module' in v:
   pm=v['prior_module']
   for name in ('_checked','_assemble','derive_status','derive_client_state','derive_client','derive_handle'):
    fn=getattr(pm,name,None)
    if fn:sm.set_local_events(4,fn.__code__,sm.events.PY_START)
   if hasattr(pm,'inputs'):sm.set_local_events(4,pm.inputs.__code__,sm.events.PY_RETURN)
 sm.register_callback(4,sm.events.PY_RETURN,returned)
 def monitor(m):
  for n in ('_basis','_checked','_assemble','semantic','derive_stored','constructed_projection','validate'):
   sm.set_local_events(4,getattr(m,n).__code__,sm.events.PY_START)
  sm.set_local_events(4,m.inputs.__code__,sm.events.PY_RETURN)
 return monitor
class Records:
 def __init__(self,p):self.path=Path(p).absolute();self.path.mkdir(parents=True,exist_ok=False);self.rows=[];self.start=time.monotonic()
 def save(self,n,x): (self.path/n).write_bytes(enc(x))
 def row(self,n,r,**kw):
  x={'check':n,'result':r,**kw};self.rows.append(x)
  with (self.path/'progress.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
  print(len(self.rows),n,r,flush=True)
 def yes(self,n,test):
  v=test();assert v is not False,n;self.row(n,'PASS');return v
 def no(self,n,test,reason=None):
  try:test()
  except ValueError as e:
   if reason:assert reason in str(e),(n,str(e),reason)
   self.row(n,'REJECTED',error=str(e));return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+n)
 def finish(self,error=None,**extra):
  self.save('calls.json',CALLS);self.save('RESULT.json',{'checks':len(self.rows),'rows':self.rows,'result':'PASS' if error is None else 'FAILED-ATTEMPT','error':error,'environment':environment(),'seconds':time.monotonic()-self.start,'runtime_calls':0,'session_operations':0,'database_connections':0,'source_only_constructed':True,**extra})
def change(v,path,x):
 v=D(v);w=v
 for k in path[:-1]:w=w[k]
 w[path[-1]]=x;return v
def replace(v,old,new):
 if type(v) is dict:return {k:replace(x,old,new) for k,x in v.items()}
 if type(v) is list:return [replace(x,old,new) for x in v]
 return new if type(v) is type(old) and v==old else v
ORDER=['stored-error-rethrow','finally-enter','removal-attempt','removal-complete']
def token_case(m,b,idx,invocation,control=True,continuity=True):
 row=b['prior']['contexts'][idx]['token_registration_correspondence'];anchor=D(row['instance_anchor']);tb=b['token_basis'];tm=b['routes']['token_module'];scope=tm.invocation_scope(anchor,invocation);c=tb['fresh']['coverage']
 steps=['owner-create','token-create','registry-insert','control-guard']+(['control-create','control-callback'] if control else [])+['client-create','client-callback','owner-failure-guard']
 v={'occurrence':invocation,'scope':scope,'control_present':control,'owner_failure_none':False,'registry_continuity':continuity,'outcomes':[{'stage':s,'outcome':'normal'} for s in steps]}
 p={**D(v),'references':c.token_reference_premises(scope,control)};o=c.token_registration_projection(tb['catalogue'],p,v)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':anchor,'invocation':invocation,'control_present':control,'owner_failure_none':False,'registry_continuity':continuity,'outcomes':D(v['outcomes']),'projection':p,'output':o}
def refresh(m,b,x):
 x['projection']=m._premises(b,x);x['output']=b['fresh']['coverage'].stored_failure_projection(b['catalogue'],D(x['projection']),D(x['projection']));return x
def make(m,b,idx,route='handle',invocation=None,helper='normal',terminal=None,control=True,continuity=True,rethrow='raised-original'):
 inv=invocation or 'FL6-'+str(idx)+'-'+route;tc=token_case(m,b,idx,inv,control,continuity);bb=m.failure_inputs(b,tc['context'],inv,tc['output']);row=b['prior']['contexts'][idx];c=b['fresh']['coverage']
 p={'occurrence':inv+'/client-operation','scope':D(bb[route+'_scope']),'references':D(bb[route+'_references']),'outcomes':{'client-call':'normal','owner-lookup':'normal','owner-guard':'normal'},'manager_case':None,'callback':'returns','cleanup':dict.fromkeys(('revoke','format','cleanup','write','outer_fail'),'unobserved')}
 if route=='handle':
  p['packet']={'type':'str','value':'FL6 invalid packet'};p['outcomes']['packet-check']='normal'
 else:p['detachment']=None;p['outcomes'].update({'operation-check':'normal','session-call':'raise'})
 p['outcomes'].update({'retain-error':'normal','fixed-failure':helper})
 cat=row['client_'+route+'_return_correspondence']['declaration']
 f=c.client_handle_projection(cat,b['verification'],p,D(p)) if route=='handle' else c.client_state_projection(cat,p,{'scope':bb['state_scope'],'state':row['client_state_return_correspondence']['validated_state_anchor']['validated_state']})
 outcomes=[]
 for i,s in enumerate(ORDER):
  val=terminal[1] if terminal and terminal[0]==s else rethrow if i==0 else 'normal';outcomes.append({'stage':s,'outcome':val})
  if val in ('process-termination','unobserved') or i>0 and val=='raise':break
 x={'kind':'CONSTRUCTED-STORED-FAILURE-REVOCATION','context':tc['context'],'anchor':D(tc['anchor']),'invocation':inv,'token_case':tc,'failure_route':route,'failure_input':p,'failure_result':f,'outcomes':outcomes,'projection':{},'output':{}}
 return refresh(m,b,x)
def independent_flags(x):
 o=x['output'];events=x['outcomes'];done={v['stage'] for v in events if v['outcome']=='normal'};orig=events[0]['outcome']=='raised-original';last=events[-1];popped='removal-complete' in done
 assert o['failure_storage_previously_completed_in_model'] is True and o['callback_returned_normally_in_model'] is True and o['run_success_established'] is False
 assert o['source_original_rethrow_completed_in_model'] is orig
 assert o['finally_entry_completed_in_model']==('finally-enter' in done)
 assert o['removal_attempt_entered_in_model']==('removal-attempt' in done)
 assert o['removal_completed_in_model'] is popped
 assert o['original_outward_after_finally_established_in_model']==(popped and orig)
 assert o['selected_owner_removed_in_model'] is (True if popped and x['token_case']['registry_continuity'] else None)
 assert o['original_error']==x['failure_result']['original_exception']
 if last['outcome'] in ('unobserved','process-termination'):
  assert o['terminal_python_exception_in_model'] is None and o['outward_error_after_finally_in_model'] is None
 if last['outcome']=='raise' and last['stage']!='stored-error-rethrow':
  assert o['cleanup_error_in_model']==o['last_pending_error_in_model'] and o['last_pending_error_in_model']!=o['original_error'] and o['outward_error_after_finally_in_model'] is None
 if popped:
  assert o['slot_after_pop_in_model']=='ABSENT-AT-POP-COMPLETION'
  assert o['outward_error_after_finally_in_model']==o['last_pending_error_in_model']
  if orig:assert o['outward_error_after_finally_in_model']==o['original_error']
 for k in ('original_reaches_launcher_established','physical_lock_release_established','exclusive_ownership_established','durability_established','actual_admission','authorization_renewed','obligations_discharged'):assert o[k] is False
 for k in ('observer_join','runtime_rethrow_revocation_chain','database_cleanup_completion','outer_cleanup_completion','retained_failure_record_bytes','physical_reference_identity','revocation_persists','pop_result_observation'):assert o[k] is None
 return True
