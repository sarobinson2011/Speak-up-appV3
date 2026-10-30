from pathlib import Path
import sys,copy,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/callback-bare-rethrow.json').read_bytes()
 if mode=='public':
  old=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/callback-bare-rethrow.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=old
  (rec.path/'CLI.stdout').write_text(out.getvalue());rec.save('CLI-result.json',json.loads(out.getvalue()));rec.check('fresh public CLI exact receipt',lambda:json.loads(out.getvalue())['result']=='PASS')
  for relation in ('callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence'):
   q=json.loads(saved);del q['contexts'][1][relation];rec.reject('all three relations mandatory '+relation,lambda q=q:m.validate(root,m.enc(q)))
  q=json.loads(saved)
  for ctx in q['contexts']:
   rel=ctx['callback_bare_rethrow_correspondence'];rel['declaration']['source']['bare_raise_has_explicit_cause_clause']=True;rel['declaration']['source']['cause_expression']='None';rel['declaration']['guard_branches']['bare_raise']='No pre-existing cause or context'
  rec.reject('fresh public coordinated invented cause and absence claims',lambda:m.validate(root,m.enc(q)))
 elif mode=='recovered':
  data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);rec.check('recovered exact receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   fx=normal(m,basis,idx);rec.check('recovered legitimate bare callback '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   for path,value in [(('callback_error','reference'),'other'),(('none_guard_binding','slot_value'),False),(('none_guard_binding','guard_result'),True),(('none_guard_binding','owner','symbol'),'other'),(('projection','references','token','symbol'),'other'),(('token_case','invocation'),'other'),(('output','exception_chain_observation','existing_cause'),None),(('output','new_explicit_cause_assignment_established_in_model'),True),(('output','reraised_error_in_model','reference'),'other'),(('callback_error',),{S(k):v for k,v in fx['callback_error'].items()})]:
    q=change(fx,path,value);rec.reject('recovered binding/type '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
   for stage in ORDER:
    for outcome in ('raise','process-termination'):
     q=normal(m,basis,idx,terminal=(stage,outcome));rec.check('recovered legitimate frontier '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q)['projection']==q['output']);q['output']['callback_outward_after_finally_established_in_model']=True;rec.reject('recovered false callback propagation '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q))
   q=normal(m,basis,idx,continuity=False);rec.check('recovered conditional selected-owner removal '+str(idx),lambda q=q:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is None)
   got=m._construct_checked(basis,fx);got['projection']['callback_error'].clear();got['projection']['events'].clear();rec.check('recovered nested mutable output isolation '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['selected_guard_result']=True;rec.reject('recovered semantic guard substitution '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
  got=m._assemble(data,rows,basis);got['contexts'].clear();rec.check('recovered bundle expectations isolated',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New bare-rethrow extension only; prior completed campaigns not rerun')
