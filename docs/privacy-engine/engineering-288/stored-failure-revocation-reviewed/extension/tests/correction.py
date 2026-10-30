"""Focused added guard-domain controls; completed baseline campaigns are not rerun."""
from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
try:
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m)
 # Reproduce the original pure-checker restriction with unchanged source and
 # saved constructed inputs. This is not a rerun of the completed baseline.
 old=module(root/'failures/helper-escape-gap/managed_coverage.py');before=json.loads((root/'results/primary/stored-failure-revocation.json').read_bytes());fixtures=json.loads((root/'results/primary/fixtures.json').read_bytes())['cases'];witnesses=[]
 for idx in (0,1):
  for route in ('handle','state'):
   fx=copy.deepcopy(fixtures[2*idx+(route=='state')]);p=fx['failure_input'];p['outcomes']['fixed-failure']='raise';row=before['contexts'][idx];cat=row['client_'+route+'_return_correspondence']['declaration']
   f=old.client_handle_projection(cat,{},p,copy.deepcopy(p)) if route=='handle' else old.client_state_projection(cat,p,{'scope':p['scope'],'state':fx['anchor']['validated_state']})
   rec.check('original source admits stored error after helper raise '+str(idx)+route,lambda f=f:f['retained_original'] is True and f['completion']=='unqualified-escape')
   proj=copy.deepcopy(fx['projection']);proj['failure_provenance']=f;proj['stored_error_binding']['error']=copy.deepcopy(f['original_exception']);oc=row['stored_failure_revocation_correspondence']['declaration'];rec.reject('original pure checker rejects source-admitted continuation '+str(idx)+route,lambda proj=proj,oc=oc:old.stored_failure_projection(oc,proj,copy.deepcopy(proj)),reason='STORED-VALIDATED-STORAGE');witnesses.append({'context':row['context'],'route':route,'failure_input':p,'validated_failure_result':f,'projection':proj,'old_error':'STORED-VALIDATED-STORAGE'})
 rec.save('original-witnesses.json',{'scope':'Pure-checker source-admitted omission, not a claim of original public validation or runtime execution','witnesses':witnesses})
 data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);receipt=m.enc(m._assemble(data,rows,basis));newfixtures=[]
 rec.check('corrected mandatory both contexts and original prerequisite',lambda:len(rows)==2 and all('failure_provenance' in r['declaration']['guard_branches'] for r in rows))
 for idx in (0,1):
  for route in ('handle','state'):
   label=str(idx)+route;fx=normal(m,basis,idx,route=route,helper='raise');newfixtures.append(fx)
   rec.check('helper unexpected raise then callback return '+label,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
   rec.check('original storage and original rethrow survive helper error '+label,lambda fx=fx:fx['output']['original_error']==fx['failure_result']['original_exception'] and fx['output']['outward_error_after_finally_in_model']==fx['failure_result']['original_exception'] and fx['output']['failure_storage_previously_completed_in_model'] and not fx['output']['run_success_established'])
   un=normal(m,basis,idx,route=route,helper='raise',continuity=False);rec.check('helper escape unknown continuity '+label,lambda un=un:m._construct_checked(basis,un)['projection']==un['output'] and un['output']['selected_owner_removed_in_model'] is None)
   for stage,outcome in [('removal-attempt','raise'),('removal-complete','raise'),('finally-enter','process-termination')]:
    q=normal(m,basis,idx,route=route,helper='raise',terminal=(stage,outcome));rec.check('corrected cleanup frontier '+label+stage+outcome,lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['failure_storage_previously_completed_in_model'] and not q['output']['original_outward_after_finally_established_in_model']);q['output']['removal_completed_in_model']=True;rec.reject('false corrected revocation '+label+stage+outcome,lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['failure_input']['outcomes']['fixed-failure']='process-termination';rec.reject('helper termination cannot yield normal callback '+label,lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['failure_result']['original_exception']['reference']='helper-error-substitution';q['projection']['stored_error_binding']['error']=copy.deepcopy(q['failure_result']['original_exception']);q['projection']['failure_provenance']=copy.deepcopy(q['failure_result']);rec.reject('helper exception cannot replace stored original '+label,lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['failure_result']['completion']=S(q['failure_result']['completion']);rec.reject('corrected exact-type boundary '+label,lambda q=q:m._construct_checked(basis,q))
   got=m._construct_checked(basis,fx);got['projection']['validated_failure_provenance'].clear();got['projection']['original_error'].clear();rec.check('corrected result isolation '+label,lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  normalcase=normal(m,basis,idx);rec.check('adjacent fixed failure remains admitted '+str(idx),lambda q=normalcase:m._construct_checked(basis,q)['projection']==q['output'])
  claims=copy.deepcopy(rows);claims[idx]['declaration']['guard_branches']['failure_provenance'].pop(1);rec.reject('corrected semantic omission '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
 bad=copy.deepcopy(cat);bad['guard_branches']['failure_provenance'].pop(1);rec.reject('corrected independent source catalogue omission',lambda:basis['fresh']['coverage'].validate_stored_failure(*m.sources(data)[:2],*m.dependencies(data),bad))
 rec.save('fixtures.json',{'cases':newfixtures});rec.save('receipt-identity.json',identity(receipt));rec.save('stored-failure-revocation.json',json.loads(receipt))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Added helper-escape omission witnesses and focused correction only; initial 366/75/7 campaigns preserved, not rerun')
