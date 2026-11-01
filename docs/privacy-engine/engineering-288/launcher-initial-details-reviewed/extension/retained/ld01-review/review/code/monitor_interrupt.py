"""One new adversarial monitoring-setup witness; no implementation replacement."""
from pathlib import Path
import sys,ast,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);failure=None;old_trace=sys.gettrace();sm=sys.monitoring
try:
 r.save('input-verification.json',verify_root(root));monitor,_=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root)
 tree=ast.parse((root/'code/correspondence.py').read_bytes());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');capture=next(n for n in f.body if isinstance(n,ast.FunctionDef) and n.name=='capture');region=next(n for n in f.body if isinstance(n,ast.Try))
 assert capture.lineno<region.lineno and sm.get_tool(2) is None
 observed={}
 def inject(frame,event,arg):
  if frame.f_code is m._public_predecessor.__code__ and event=='line' and frame.f_lineno==capture.lineno:
   observed.update({'function':frame.f_code.co_name,'file':frame.f_code.co_filename,'line':frame.f_lineno,'offset':frame.f_lasti,'tool_owner_before_interrupt':sm.get_tool(2)})
   raise KeyboardInterrupt('REVIEWER-CONSTRUCTED-INTERRUPTION-AFTER-MONITOR-RESERVATION')
  return inject
 sys.settrace(inject)
 try:m._public_predecessor(data)
 except KeyboardInterrupt:
  (r.path/'interruption.traceback.txt').write_text(traceback.format_exc())
 else:raise AssertionError('INJECTION-NOT-REACHED')
 finally:sys.settrace(old_trace)
 owner=sm.get_tool(2);assert observed and observed['tool_owner_before_interrupt']=='launcher-details-authenticated-predecessor'
 r.save('after-interruption.json',{'observed':observed,'tool_owner_after_interruption':owner,'global_events':sm.get_events(2),'basis_local_events':sm.get_local_events(2,data['prior_module']._basis.__code__),'injection':'Constructed KeyboardInterrupt before inner callback definition; implementation bytes unchanged; no runtime/session operation'})
 if owner is None:
  r.row('monitor lease released after setup interruption','PASS')
  r.save('FINDING.json',{'finding':None,'cleanup_supported':True})
 else:
  r.row('monitor lease survives setup interruption','DEFECT-OBSERVED',owner=owner)
  saved=(root/'results/primary/launcher-details.json').read_bytes()
  try:m.validate(root,saved)
  except ValueError as e:
   assert str(e)=='DETAILS-MONITORING-CONTENTION';(r.path/'subsequent-public.traceback.txt').write_text(traceback.format_exc())
   r.row('subsequent pristine public validation blocked by leaked lease','DEFECT-CORROBORATED',error=str(e))
  else:raise AssertionError('LEAKED-LEASE-DID-NOT-BLOCK')
  r.save('FINDING.json',{'finding':'LD-01','scope':'Monitoring setup failure cleanup','verdict':'NOT-CLOSED','source':identity((root/'code/correspondence.py').read_bytes()),'target':'I164-launcher-initial-details-correspondence-1.zip','witness':'Reserve monitoring slot2, then inject KeyboardInterrupt at source-derived callback-definition line before try/finally. The lease remains owned; unchanged pristine public validation then rejects DETAILS-MONITORING-CONTENTION.','observed':observed,'subsequent_rejection_layer':'Monitoring contention gate before predecessor public validation; not receipt comparison','effect':'Fail-closed process-local reuse failure; no false receipt acceptance or admission','constructed_not_runtime_observation':True,'candidate_code_changed':False,'original_trace_preserved':True,'minimal_repair_direction':'Extend guaranteed release to the whole successful-lease lifetime, including setup before callback registration; implementation not changed here.'})
 # Reviewer cleanup only after preserving the actual leaked state and subsequent rejection.
 if sm.get_tool(2)=='launcher-details-authenticated-predecessor':
  sm.set_local_events(2,data['prior_module']._basis.__code__,0);sm.register_callback(2,sm.events.PY_RETURN,None);sm.free_tool_id(2)
 r.save('reviewer-cleanup.json',{'tool_owner_after_explicit_reviewer_cleanup':sm.get_tool(2),'not_candidate_cleanup':True});r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:
 sys.settrace(old_trace)
 if sm.get_tool(2)=='launcher-details-authenticated-predecessor':
  sm.set_events(2,0);sm.register_callback(2,sm.events.PY_RETURN,None);sm.free_tool_id(2)
 r.finish(failure,scope='One new bounded constructed interruption witness; observed defect rows are not passing acceptance controls; no full predecessor review replay')
