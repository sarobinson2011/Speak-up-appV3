from pathlib import Path
import sys,copy,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/control-construction.json').read_bytes()
 if mode=='public':
  old=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/control-construction.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=old
  (rec.path/'CLI.stdout').write_text(out.getvalue());rec.save('CLI-result.json',json.loads(out.getvalue()));rec.check('fresh public CLI exact receipt',lambda:json.loads(out.getvalue())['result']=='PASS')
  for relation in ('control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'):
   q=json.loads(saved);del q['contexts'][1][relation];rec.reject('mandatory relation '+relation,lambda q=q:m.validate(root,m.enc(q)))
  q=json.loads(saved)
  for ctx in q['contexts']:
   r=ctx['control_construction_revocation_correspondence'];r['declaration']['source']['completed_control_object_established']=True;r['construction_completed']=True;r['control_callback_execution']=True
  rec.reject('public coordinated completed construction and callback claim',lambda:m.validate(root,m.enc(q)))
 elif mode=='recovered':
  data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);rec.check('recovered exact derived receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
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
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New construction-exception extension only; prior campaigns not rerun')
