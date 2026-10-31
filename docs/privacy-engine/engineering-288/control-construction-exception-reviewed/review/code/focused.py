from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
class I(int):pass
class L(list):pass
class M(dict):pass
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m)
 saved=(root/'results/primary/control-construction.json').read_bytes();r.event('public-validation-start',mode=mode)
 if mode=='primary':
  result=m.validate(root,saved);r.save('public-result.json',result)
  r.yes('fresh public accepts actual current receipt in both contexts',lambda:result['result']=='PASS' and result['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and result['actual_admission'] is False)
 elif mode=='recovered':
  q=json.loads(saved)
  for row in q['contexts']:
   x=row['control_construction_revocation_correspondence'];assert x['construction_completed'] is False and x['control_callback_execution'] is False and x['exception_chain_observation'] is None
   x['construction_completed']=True;x['control_callback_execution']=True;x['exception_chain_observation']={'existing_cause':None};x['declaration']['source']['completed_control_object_established']=True
  mutated=m.enc(q);assert mutated!=saved;(r.path/'coordinated-receipt.json').write_bytes(mutated)
  r.save('public-witness.json',{'original':identity(saved),'mutated':identity(mutated),'contexts':2,'changes_each':['construction_completed','control_callback_execution','exception_chain_observation','declaration.source.completed_control_object_established']})
  try:m.validate(root,mutated)
  except ValueError as e:
   text=traceback.format_exc();(r.path/'public-rejection.traceback.txt').write_text(text);tb=e.__traceback__;frames=[]
   while tb:frames.append({'function':tb.tb_frame.f_code.co_name,'file':tb.tb_frame.f_code.co_filename,'line':tb.tb_lineno});tb=tb.tb_next
   assert type(e) is ValueError and str(e)=='CONSTRUCTION-STALE-OR-ALTERED-RECEIPT' and [f['function'] for f in frames[-2:]]==['validate','require']
   r.save('public-rejection.json',{'type':type(e).__name__,'error':str(e),'frames':frames,'layer':'public post-derivation receipt comparison'})
   r.row('fresh recovered public coordinated claims reject at receipt comparison','REJECTED',error=str(e))
  else:raise AssertionError('UNEXPECTED-PUBLIC-ACCEPTANCE')
 else:raise AssertionError('UNKNOWN-MODE')
 assert len(captures)==1;basis=captures.pop();data=basis['fresh'];cat=basis['catalogue'];c=data['coverage'];rows=m._rows(basis)
 r.event('focused-cores-start',basis='Actual unchanged public validator return observed; no function replacement')
 r.yes('fresh authenticated derivation equals exact saved receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
 r.save('source-catalogue.json',cat);r.save('semantic-rows.json',rows)
 before=m.enc(rows);fixtures=[]
 for index in (0,1):
  q=make(m,basis,index);fixtures.append(q)
  r.yes('independently assembled construction case and oracle '+str(index),lambda q=q:oracle(q,m._construct_checked(basis,q)))
  r.yes('distinct invocation remains source-admitted '+str(index),lambda index=index:oracle((x:=make(m,basis,index,invocation='fl6-distinct-occurrence')),m._construct_checked(basis,x)))
  for continuity in (False,True):
   for owner_none in (False,True):
    x=make(m,basis,index,continuity=continuity,owner_none=owner_none);r.yes('unreached owner guard and conditional continuity '+str((index,continuity,owner_none)),lambda x=x:oracle(x,m._construct_checked(basis,x)))
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    x=make(m,basis,index,terminal=(stage,outcome));r.yes('independent terminal oracle '+str((index,stage,outcome)),lambda x=x:oracle(x,m._construct_checked(basis,x)))
    bad=change(x,('output','removal_completed_in_model'),True);r.no('terminal cannot claim completed removal '+str((index,stage,outcome)),lambda bad=bad:m._construct_checked(basis,bad),'CONSTRUCTION-OUTPUT-CORRESPONDENCE')
  paths=[(('construction_error','reference'),'foreign-error'),(('construction_error','construction_attempt','occurrence'),'other-attempt'),(('construction_error','construction_attempt','registered_owner','symbol'),'other-owner'),(('construction_error','construction_attempt','argument_token','symbol'),'other-token'),(('invocation',),'foreign-call'),(('context',),'SYMBOLIC-U-TWO' if index==0 else 'SYMBOLIC-U-ONE'),(('anchor','recovery_occurrence'),'stale-frontier'),(('construction_error','scope','acquisition'),'mixed-acquisition')]
  if mode=='primary':
   paths += [(('construction_error','exact_type'),'MemoryError'),(('construction_error','failure_mechanism'),'allocation'),(('construction_error','initializer_progress'),True),(('construction_error','completed_object_reference'),'control-object'),(('projection','references','control'),None),(('token_case','control_present'),False),(('projection','scope','invocation'),S(q['invocation'])),(('token_case','registry_continuity'),1),(('output','events'),L(q['output']['events'])),(('construction_error',),M(q['construction_error']))]
  for path,value in paths:
   x=change(q,path,value);r.no('binding or exact-type rejection '+str((index,path)),lambda x=x:m._construct_checked(basis,x))
  for role in ('owner','token'):
   old=q['projection']['references'][role]['symbol'];x=substitute(q,old,'coordinated-foreign-'+role)
   r.no('coordinated references cannot authenticate each other '+str((index,role)),lambda x=x:m._construct_checked(basis,x))
  x=substitute(q,q['construction_error']['reference'],'coordinated-error')
  r.no('coordinated construction-error substitution '+str(index),lambda x=x:m._construct_checked(basis,x),'CONSTRUCTION-EXPRESSION-ERROR')
  for badsteps in (q['outcomes'][:-1],list(reversed(q['outcomes'])),[q['outcomes'][0],q['outcomes'][0],*q['outcomes'][1:]],q['outcomes'][1:],[] ):
   x=D(q);x['outcomes']=D(badsteps);x['projection']['outcomes']=D(badsteps)
   r.no('source continuation order '+str((index,badsteps)),lambda x=x:m._construct_checked(basis,x))
  x=make(m,basis,index,terminal=('finally-enter','raise'));x['outcomes'].append({'stage':'removal-attempt','outcome':'normal'});x['projection']['outcomes']=D(x['outcomes']);r.no('no continuation after cleanup failure '+str(index),lambda x=x:m._construct_checked(basis,x),'CONSTRUCTION-UNREACHED-STEPS')
  fields=['construction_completed_in_model','control_callback_executed_in_model','subsequent_client_execution_in_model','client_handler_entered_in_model','new_explicit_cause_assignment_established_in_model','authorization_renewed','actual_admission']
  for field in fields:
   x=change(q,('output',field),True);r.no('unsupported output '+str((index,field)),lambda x=x:m._construct_checked(basis,x),'CONSTRUCTION-OUTPUT-CORRESPONDENCE')
  x=change(q,('output','exception_chain_observation','existing_cause'),None);r.no('no absence of existing cause '+str(index),lambda x=x:m._construct_checked(basis,x))
  x=D(q);x['construction_error']={S(k):v for k,v in x['construction_error'].items()};r.no('subclass literal keys '+str(index),lambda x=x:m._construct_checked(basis,x),'KEY-TYPE')
  got=m._construct_checked(basis,q);got['projection']['events'].clear();got['projection']['construction_error']['construction_attempt'].clear()
  r.yes('nested returned results cannot alter expectation '+str(index),lambda q=q:oracle(q,m._construct_checked(basis,q)))
  for field,value in [('construction_completed',True),('control_callback_execution',True),('client_callback_execution',True),('exception_chain_observation',{'existing_cause':None}),('classification','PASS'),('multiplicity',0)]:
   x=D(rows);x[index][field]=value;x[index]['declaration']['source']['completed_control_object_established']=True
   r.no('semantic coordinated unobserved claim '+str((index,field)),lambda x=x:m._check_rows(basis,x),'CONSTRUCTION-SEMANTIC-CORRESPONDENCE')
  x=D(rows);x[index]['instance_anchor']['recovery_occurrence']='other';r.no('semantic wrong-instance anchor '+str(index),lambda x=x:m._check_rows(basis,x))
  x=D(rows);x[index]['conditional_links'].pop();r.no('semantic omitted mandatory link '+str(index),lambda x=x:m._check_rows(basis,x))
  if mode=='recovered':break
 r.save('independent-fixtures.json',fixtures)
 for case,label in [(rows[::-1],'context reversal'),(rows[:-1],'missing context'),([rows[0],rows[0]],'duplicate context')]:r.no('semantic '+label,lambda case=case:m._check_rows(basis,case))
 r.yes('semantic expectations remain unchanged',lambda:m.enc(m._rows(basis))==before)
 got=m._assemble(data,rows,basis);got['contexts'].clear();got['extension_components'].clear();r.yes('derived receipt alias isolation',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==saved)
 e=D(basis['evidence']);key=next(k for k,v in e.items() if v);e[key]+=b'\n';r.no('authenticated evidence alteration',lambda:m._compare_evidence(basis,e),'CONSTRUCTION-VALIDATED-EVIDENCE')
 e=D(basis['evidence']);del e[key];r.no('authenticated evidence omission',lambda:m._compare_evidence(basis,e),'CONSTRUCTION-VALIDATED-EVIDENCE')
 for i in (0,1):
  for relation in ('control_construction_revocation_correspondence','control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'):
   x=json.loads(saved);del x['contexts'][i][relation];r.no('public mandatory '+str((i,relation)),lambda x=x:m.validate(root,m.enc(x)),'CONSTRUCTION-MANDATORY-RELATIONS')
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,mode=mode,public_basis_calls_observed=1 if 'basis' in globals() else 0,CLI_execution_claimed=False)
