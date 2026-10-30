"""Final guard-domain correction checks; no completed baseline suite rerun."""
from pathlib import Path
import sys,json,copy,traceback,contextlib,io,runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);saved=(root/'results/correction/stored-failure-revocation.json').read_bytes();fixtures=json.loads((root/'results/correction/fixtures.json').read_bytes())['cases']
 if mode=='fresh':
  fx=fixtures[0];got=m.constructed_projection(data,cat,fx);rec.check('fresh public helper-escape continuation accepted',lambda:got['projection']==fx['output']);got['projection']['original_error'].clear();got['projection']['validated_failure_provenance'].clear()
  oldargs=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/correction/stored-failure-revocation.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=oldargs
  (rec.path/'CLI.stdout').write_text(out.getvalue());rec.save('CLI-result.json',json.loads(out.getvalue()));rec.check('final offline CLI exact corrected receipt after returned mutation',lambda:json.loads(out.getvalue())['result']=='PASS')
  q=json.loads(saved);del q['contexts'][1]['stored_failure_revocation_correspondence'];rec.reject('corrected public missing mandatory context',lambda:m.validate(root,m.enc(q)))
 elif mode=='recovered':
  rows,basis=m._checked(data,cat);rec.check('corrected recovered exact canonical receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   for route in ('handle','state'):
    label=str(idx)+route;fx=normal(m,basis,idx,route=route,helper='raise');rec.check('recovered helper escape '+label,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
    for path,value in [(('failure_result','original_exception','reference'),'wrong'),(('failure_input','references','owner','symbol'),'foreign'),(('token_case','invocation'),'other'),(('output','run_success_established'),True)]:
     q=change(fx,path,value);rec.reject('recovered corrected binding '+label+str(path),lambda q=q:m._construct_checked(basis,q))
    q=normal(m,basis,idx,route=route,helper='raise',terminal=('removal-complete','raise'));rec.check('recovered helper plus cleanup raise preserves storage '+label,lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['failure_storage_previously_completed_in_model'] and not q['output']['original_outward_after_finally_established_in_model'])
    q['output']['original_outward_after_finally_established_in_model']=True;rec.reject('recovered cleanup cannot guarantee original '+label,lambda q=q:m._construct_checked(basis,q))
    got=m._construct_checked(basis,fx);got['projection']['original_error'].clear();got['projection']['reference_bindings'].clear();rec.check('recovered corrected isolation '+label,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   q=normal(m,basis,idx,helper='raise',continuity=False,terminal=('finally-enter','process-termination'));rec.check('recovered corrected termination and unknown continuity '+str(idx),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['selected_owner_removed_in_model'] is None and q['output']['terminal_python_exception_in_model'] is None)
   claims=copy.deepcopy(rows);claims[idx]['declaration']['guard_branches']['failure_provenance'].pop(1);rec.reject('recovered corrected branch omission '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
 else:raise ValueError('MODE')
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='Final helper-escape correction only; prior 366/75/7 campaigns and prior review controls not rerun')
