from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class L(list):pass
class M(dict):pass
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m)
 saved=(root/'results/primary/client-construction-none.json').read_bytes();r.event('full-public-validation-start',timeout_owned_by_supervisor=True)
 result=m.validate(root,saved);r.save('public-result.json',result)
 r.yes('fresh recovered public validation accepts current receipt in both contexts',lambda:result['result']=='PASS' and result['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and result['actual_admission'] is False)
 assert len(captures)==1;basis=captures.pop();data=basis['fresh'];cat=basis['catalogue'];c=data['coverage'];rows=m._rows(basis);before=m.enc(rows)
 r.event('focused-checked-cores-start',basis='Actual mandatory validator basis passively observed; no validator replacement')
 r.yes('authenticated derivation exactly reproduces saved receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 r.save('source-catalogue.json',cat);r.save('semantic-rows.json',rows);fixtures=[]
 for idx in (0,1):
  for control in (False,True):
   label=str((idx,control));q=make(m,basis,idx,control=control);fixtures.append(q)
   r.yes('source-derived case and independent oracle '+label,lambda q=q:oracle(q,m._construct_checked(basis,q)))
   x=make(m,basis,idx,control=control,continuity=False);r.yes('selected owner removal remains conditional '+label,lambda x=x:oracle(x,m._construct_checked(basis,x)))
   x=make(m,basis,idx,control=control,invocation='fl6-distinct-client-construction');r.yes('distinct invocation does not collapse equal modeled values '+label,lambda x=x:oracle(x,m._construct_checked(basis,x)) and x['output']['scope']!=q['output']['scope'])
   for stage in ORDER:
    for kind in ('raise','process-termination','unobserved'):
     x=make(m,basis,idx,control=control,overrides={stage:kind});key=str((idx,control,stage,kind))
     r.yes('failure or uncertainty oracle '+key,lambda x=x:oracle(x,m._construct_checked(basis,x)))
     flag='bare_rethrow_effect_established_in_model' if stage in ORDER[:3] else 'removal_completed_in_model'
     bad=change(x,('output',flag),True)
     r.no('unestablished continuation rejects '+key,lambda bad=bad:m._construct_checked(basis,bad),'CLIENT-CONSTRUCTION-OUTPUT-CORRESPONDENCE')
   for handler in ORDER[:3]:
    x=make(m,basis,idx,control=control,overrides={handler:'raise','removal-attempt':'raise'})
    r.yes('handler replacement followed by cleanup replacement '+str((idx,control,handler)),lambda x=x:oracle(x,m._construct_checked(basis,x)))
   # Both prefix variants retain distinct source-required history.
   x=change(q,('output','earlier_control_callback_completed_in_model'),None if control else True)
   r.no('control history cannot be erased or invented '+label,lambda x=x:m._construct_checked(basis,x))
  q=fixtures[-1]
  paths=[(('invocation',),'foreign-invocation'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('anchor','recovery_occurrence'),'stale-frontier'),(('construction_error','scope','acquisition'),'foreign-acquisition'),(('construction_error','reference'),'foreign-error'),(('construction_error','construction_attempt','argument_token','symbol'),'foreign-token'),(('construction_error','construction_attempt','registered_owner','symbol'),'foreign-owner'),(('none_guard_binding','owner','symbol'),'foreign-owner'),(('none_guard_binding','slot_value'),False),(('none_guard_binding','slot_value'),0),(('none_guard_binding','guard_result'),True),(('none_guard_binding','guard_result'),0),(('none_guard_binding','prior_storage_history'),'ABSENT'),(('token_case','owner_failure_none'),False),(('token_case','owner_failure_none'),1),(('none_guard_binding','slot'),S('owner.failure')),(('construction_error',),M(q['construction_error'])),(('outcomes',),L(q['outcomes'])),(('construction_error','failure_mechanism'),'MemoryError'),(('construction_error','initializer_progress'),True),(('construction_error','completed_object_reference'),'client-object')]
  for path,value in paths:
   x=change(q,path,value);r.no('binding exact-type or unsupported mechanism '+str((idx,path,value))[:220],lambda x=x:m._construct_checked(basis,x))
  for role in ('owner','token'):
   x=substitute(q,q['projection']['references'][role]['symbol'],'coordinated-foreign-'+role)
   r.no('coordinated reference substitution '+str((idx,role)),lambda x=x:m._construct_checked(basis,x))
  x=substitute(q,q['construction_error']['reference'],'coordinated-error');r.no('coordinated construction error substitution '+str(idx),lambda x=x:m._construct_checked(basis,x),'CLIENT-CONSTRUCTION-EXPRESSION-ERROR')
  x=D(q);x['none_guard_binding']['slot_value']='None';x['projection']['none_guard_binding']=D(x['none_guard_binding']);x['output']['none_guard_binding']=D(x['none_guard_binding']);r.no('coordinated exact-None substitution '+str(idx),lambda x=x:m._construct_checked(basis,x),'CLIENT-CONSTRUCTION-SELECTED-GUARD-BINDING')
  x=D(q);x['construction_error']={S(k):v for k,v in x['construction_error'].items()};r.no('literal-key subclasses reject before normalization '+str(idx),lambda x=x:m._construct_checked(basis,x),'KEY-TYPE')
  for badsteps in (q['outcomes'][:-1],q['outcomes'][1:],list(reversed(q['outcomes'])),[q['outcomes'][0],*q['outcomes']],[],[{'stage':'client-callback','outcome':'normal'},*q['outcomes']]):
   x=D(q);x['outcomes']=D(badsteps);x['projection']['outcomes']=D(badsteps);r.no('omitted duplicated reordered or invented stage '+str((idx,badsteps))[:220],lambda x=x:m._construct_checked(basis,x))
  x=make(m,basis,idx,overrides={'finally-enter':'raise'});x['outcomes'].append({'stage':'removal-attempt','outcome':'normal'});x['projection']['outcomes']=D(x['outcomes']);r.no('no continuation after cleanup failure '+str(idx),lambda x=x:m._construct_checked(basis,x),'CLIENT-CONSTRUCTION-UNREACHED-STEPS')
  for field in ('construction_completed_in_model','client_callback_executed_in_model','new_explicit_cause_assignment_established_in_model','construction_reaches_launcher_established','run_success_established','runtime_observation','obligations_discharged','authorization_renewed','actual_admission'):
   x=change(q,('output',field),True);r.no('unsupported output escalation '+str((idx,field)),lambda x=x:m._construct_checked(basis,x))
  x=change(q,('output','exception_chain_observation','existing_cause'),None);r.no('bare rethrow cannot erase existing-cause uncertainty '+str(idx),lambda x=x:m._construct_checked(basis,x))
  got=m._construct_checked(basis,q);got['projection']['events'].clear();got['projection']['construction_error']['construction_attempt'].clear();got['projection']['none_guard_binding']['owner'].clear()
  r.yes('nested returned projection mutation leaves expectations intact '+str(idx),lambda q=q:oracle(q,m._construct_checked(basis,q)))
  for field,value in [('construction_completed',True),('client_callback_execution',True),('exception_chain_observation',{'existing_cause':None}),('prior_failure_storage_history','ABSENT'),('classification','PASS'),('multiplicity',0)]:
   x=D(rows);x[idx][field]=value;x[idx]['declaration']['source']['completed_client_object_established']=True
   r.no('semantic coordinated unsupported claim '+str((idx,field)),lambda x=x:m._check_rows(basis,x),'CLIENT-CONSTRUCTION-SEMANTIC-CORRESPONDENCE')
  x=D(rows);x[idx]['instance_anchor']['recovery_occurrence']='wrong';r.no('semantic wrong-instance predecessor '+str(idx),lambda x=x:m._check_rows(basis,x))
  x=D(rows);x[idx]['conditional_links'].pop();r.no('semantic omitted link '+str(idx),lambda x=x:m._check_rows(basis,x))
 r.save('independent-fixtures.json',fixtures)
 for x,label in [(rows[::-1],'context order'),(rows[:-1],'missing context'),([rows[0],rows[0]],'duplicate context')]:r.no('semantic '+label,lambda x=x:m._check_rows(basis,x))
 r.yes('returned semantic rows cannot alter new expectations',lambda:m.enc(m._rows(basis))==before)
 got=m._assemble(data,rows,basis);got['contexts'].reverse();got['contexts'][0]['client_construction_none_correspondence']['declaration']['source'].clear();got['extension_components'].clear()
 r.yes('nested derived receipt mutation cannot alter expectations',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==saved)
 e=D(basis['evidence']);key=next(k for k,v in e.items() if v);e[key]+=b'\n';r.no('altered authenticated evidence',lambda:m._compare_evidence(basis,e),'CLIENT-CONSTRUCTION-VALIDATED-EVIDENCE')
 e=D(basis['evidence']);del e[key];r.no('omitted authenticated evidence',lambda:m._compare_evidence(basis,e),'CLIENT-CONSTRUCTION-VALIDATED-EVIDENCE')
 for idx in (0,1):
  for relation in ('client_construction_none_correspondence','control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'):
   x=json.loads(saved);del x['contexts'][idx][relation];r.no('public mandatory relation '+str((idx,relation)),lambda x=x:m.validate(root,m.enc(x)),'CLIENT-CONSTRUCTION-MANDATORY-RELATIONS')
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error)
 if 'x' in globals():r.save('last-case.json',x)
 raise
finally:r.finish(error,public_full_derivations=1 if 'basis' in globals() else 0,CLI_execution_claimed=False,scope='Fresh recovered public positive plus bounded checked cores using its actual authenticated basis; no separate full-public negative derivation per mutant')
