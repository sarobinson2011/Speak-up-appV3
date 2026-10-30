"""Fresh public and recovered focused checks of this new extension only."""
from pathlib import Path
import sys,json,copy,traceback,runpy,io,contextlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);saved=(root/'results/primary/callback-stored-failure.json').read_bytes()
 if mode=='public':
  oldargs=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/callback-stored-failure.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=oldargs
  (rec.path/'CLI.stdout').write_text(out.getvalue());rec.save('CLI-result.json',json.loads(out.getvalue()));rec.check('fresh actual CLI exact callback receipt',lambda:json.loads(out.getvalue())['result']=='PASS')
  for relation in ('callback_stored_failure_correspondence','stored_failure_revocation_correspondence'):
   q=json.loads(saved);del q['contexts'][1][relation];rec.reject('both new and normal relations mandatory '+relation,lambda q=q:m.validate(root,m.enc(q)))
  q=json.loads(saved)
  for ctx in q['contexts']:
   rel=ctx['callback_stored_failure_correspondence'];rel['declaration']['source']['cause_expression']='owner.failure';rel['declaration']['source']['explicit_cause_clause_present']=False
  rec.reject('fresh public coordinated cause substitution in both contexts',lambda:m.validate(root,m.enc(q)))
 elif mode=='recovered':
  rows,basis=m._checked(data,cat);rec.check('recovered canonical receipt exact',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   for route in ('handle','state'):
    tag=str(idx)+route;fx=normal(m,basis,idx,route=route,helper='raise');rec.check('recovered helper-escape provenance '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
    for path,value in [(('callback_error','reference'),'wrong'),(('failure_result','original_exception','reference'),'wrong'),(('projection','references','owner','symbol'),'foreign'),(('projection','references','token','symbol'),'foreign'),(('token_case','invocation'),'other'),(('output','established_explicit_cause','explicit_cause','reference'),'wrong'),(('output','removal_completed_in_model'),1)]:
     q=change(fx,path,value);rec.reject('recovered binding '+tag+str(path),lambda q=q:m._construct_checked(basis,q))
    for terminal in [('callback-failure-guard','raise'),('removal-attempt','raise'),('finally-enter','process-termination')]:
     q=normal(m,basis,idx,route=route,terminal=terminal);rec.check('recovered frontier '+tag+str(terminal),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['failure_storage_previously_completed_in_model']);q['output']['original_outward_after_finally_established_in_model']=True;rec.reject('recovered false original propagation '+tag+str(terminal),lambda q=q:m._construct_checked(basis,q))
    q=copy.deepcopy(fx);q['callback_error']={S(k):v for k,v in q['callback_error'].items()};rec.reject('recovered exact callback keys '+tag,lambda q=q:m._construct_checked(basis,q))
    got=m._construct_checked(basis,fx);got['projection']['established_explicit_cause'].clear();got['projection']['callback_error'].clear();rec.check('recovered nested isolation '+tag,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   q=normal(m,basis,idx,continuity=False);rec.check('recovered unknown owner continuity '+str(idx),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['selected_owner_removed_in_model'] is None)
   claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['cause_expression']='owner.failure';rec.reject('recovered semantic cause '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
  got=m._assemble(data,rows,basis);got['contexts'].clear();rec.check('recovered bundle expectations isolated',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New callback-exception extension only; prior controls/reviews not rerun')
