"""Complete unfinished fresh/recovered validation with unchanged public entry and observed basis return.
No prior 285 controls rerun. Python monitoring retains the actual _basis return for
focused recovered controls, without replacing or bypassing any validator function.
"""
from pathlib import Path
import sys,copy,json,traceback,gc
root=Path(sys.argv[1]).absolute();sys.path.insert(0,str(root/'tests'))
from offline import *
from cases import *
rec=Record(sys.argv[2]);error=None
class S(str):pass
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/control-construction.json').read_bytes()
 captures=[];sm=sys.monitoring;assert sm.get_tool(3) is None;sm.use_tool_id(3,'construction-test-basis-observer')
 def capture(code,offset,value):
  if code is m._basis.__code__:captures.append(value)
 sm.register_callback(3,sm.events.PY_RETURN,capture);sm.set_local_events(3,m._basis.__code__,sm.events.PY_RETURN)
 print('Fresh public validation against recovered immutable root; no checker replacement',flush=True)
 rec.check('fresh recovered public validator accepts pristine receipt',lambda:m.validate(root,saved)['result']=='PASS')
 assert len(captures)==1;basis=captures.pop();sm.set_local_events(3,m._basis.__code__,0);sm.register_callback(3,sm.events.PY_RETURN,None);sm.free_tool_id(3)
 public_pristine_rows=len(rec.rows)
 data=basis['fresh'];cat=basis['catalogue'];rows=m._rows(basis);rec.check('recovered exact derived receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 for idx in (0,1):
  fx=normal(m,basis,idx);rec.check('recovered legitimate selected control '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  for path,value in [(('construction_error','reference'),'other'),(('construction_error','construction_attempt','occurrence'),'other'),(('projection','references','owner','symbol'),'other'),(('projection','references','token','symbol'),'other'),(('token_case','invocation'),'other'),(('output','subsequent_client_execution_in_model'),True),(('output','exception_chain_observation','existing_cause'),None),(('output','new_explicit_cause_assignment_established_in_model'),True),(('construction_error',),{S(k):v for k,v in fx['construction_error'].items()})]:
   q=change(fx,path,value);rec.reject('recovered altered binding/type '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));rec.check('recovered legitimate frontier '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q)['projection']==q['output']);q['output']['removal_completed_in_model']=True;rec.reject('recovered false completion '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q))
  q=normal(m,basis,idx,continuity=False,owner_none=False);rec.check('recovered continuity without client-slot guard '+str(idx),lambda q=q:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is None)
  got=m._construct_checked(basis,fx);got['projection']['construction_error'].clear();got['projection']['events'].clear();rec.check('recovered nested mutable result isolation '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  q=copy.deepcopy(rows);q[idx]['declaration']['source']['new_explicit_cause_assignment']=True;rec.reject('recovered semantic invented cause',lambda q=q:m._check_rows(basis,q))
 got=m._assemble(data,rows,basis);got['contexts'].clear();rec.check('recovered receipt expectations isolated',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 recovered_end=len(rec.rows)
 for relation in ('control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'):
  q=json.loads(saved);del q['contexts'][1][relation];rec.reject('public mandatory relation '+relation,lambda q=q:m.validate(root,m.enc(q)))
 q=json.loads(saved)
 for ctx in q['contexts']:
  r=ctx['control_construction_revocation_correspondence'];r['declaration']['source']['completed_control_object_established']=True;r['construction_completed']=True;r['control_callback_execution']=True
 # Release the first validation's retained basis before the final fresh derivation.
 del basis,data,cat,rows,got,fx
 gc.collect()
 print('One unfinished public both-context coordinated-claim rejection',flush=True)
 rec.reject('public coordinated completed construction and callback claim',lambda:m.validate(root,m.enc(q)),reason='CONSTRUCTION-STALE-OR-ALTERED-RECEIPT')
 rec.save('row-partitions.json',{'fresh_public_pristine':[1,public_pristine_rows],'focused_recovered':[public_pristine_rows+1,recovered_end],'public_rejections':[recovered_end+1,len(rec.rows)],'one_fresh_process_on_recovered_root':True,'public_entry_unmodified':True,'basis_capture':'sys.monitoring PY_RETURN; no validation replacement','CLI_execution_claimed':False})
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Only unfinished fresh/recovered checks; no previous 285-row campaign replay; actual public validator, no CLI claim')
