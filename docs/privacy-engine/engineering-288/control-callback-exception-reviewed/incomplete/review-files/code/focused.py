from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import *
def run(root,out,mode):
 r=Records(out);error=None
 try:
  r.save('input-verification.json',verify_root(root));monitor=guard(root,r.path);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data)
  rows,b=m._checked(data,cat);r.yes('fresh mandatory validation of actual predecessor chain',lambda:len(rows)==2)
  receipt=m._assemble(data,rows,b);saved=(root/'results/primary/control-exception.json').read_bytes();r.yes('fresh derived receipt matches all saved bytes',lambda:enc(receipt)==saved);r.save('receipt-identity.json',ident(saved))
  for idx in (0,1):
   for rel in ('token_registration_correspondence','stored_failure_revocation_correspondence','callback_stored_failure_correspondence','callback_bare_rethrow_correspondence'):
    r.yes('preserved mandatory relation '+str((idx,rel)),lambda idx=idx,rel=rel:receipt['contexts'][idx][rel]==b['prior']['contexts'][idx][rel])
  fixtures=[]
  for idx in (0,1):
   x=normal(m,b,idx);fixtures.append(x)
   def good(label,q):r.yes(label,lambda:m._construct_checked(b,q)['projection']==q['output'] and independently_check(q))
   def bad(label,q):r.no(label,lambda:m._construct_checked(b,q))
   good('normal control exceptional continuation '+str(idx),x)
   for none,continuity in ((False,True),(True,False),(False,False)):
    good('no selected owner failure guard '+str((idx,none,continuity)),normal(m,b,idx,none=none,continuity=continuity))
   y=normal(m,b,idx,inv='FL6-control-distinct-'+str(idx));good('distinct invocation with equal kinds '+str(idx),y)
   r.yes('equal error role does not merge occurrences '+str(idx),lambda:x['control_error']['occurrence']!=y['control_error']['occurrence'])
   for stage in ORDER:
    for kind in ('raise','process-termination','unobserved'):
     q=normal(m,b,idx,terminal=(stage,kind));good('frontier '+str((idx,stage,kind)),q)
     bad('false completion '+str((idx,stage,kind)),change(q,('output','removal_completed_in_model'),True))
     if mode=='primary':bad('false outward control propagation '+str((idx,stage,kind)),change(q,('output','control_outward_after_finally_established_in_model'),True))
   for j in range(3):
    bad('coordinated missing stage '+str((idx,j)),outcomes_mutation(x,lambda v,j=j:v.pop(j)))
    bad('coordinated duplicate stage '+str((idx,j)),outcomes_mutation(x,lambda v,j=j:v.insert(j,D(v[j]))))
   for j in range(2):
    def swap(v,j=j):v[j],v[j+1]=v[j+1],v[j]
    bad('coordinated reordered stage '+str((idx,j)),outcomes_mutation(x,swap))
   for p,v in [(('control_error','local_handler_binding'),'client_error'),(('control_error','existing_cause'),None),(('control_error','existing_context'),None),(('control_error','existing_suppression'),False),(('control_error','reference'),'wrong/error'),(('control_error','callback_occurrence'),'wrong/callback'),(('invocation',),'wrong/invocation'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('anchor','context'),'wrong'),(('token_case','control_present'),False)]:bad('wrong binding '+str((idx,p)),change(x,p,v))
   for label,old,new in [('owner',x['projection']['references']['owner']['symbol'],'foreign/owner'),('token',x['projection']['references']['token']['symbol'],'foreign/token'),('control',x['projection']['references']['control']['symbol'],'foreign/control'),('error',x['control_error']['reference'],'foreign/error'),('acquisition',x['projection']['scope']['acquisition'],'foreign-acquisition')]:bad('coordinated binding '+str((idx,label)),replace(x,old,new))
   q=replace(x,x['control_error']['occurrence'],'foreign/occurrence');bad('coordinated wrong callback-error occurrence '+str(idx),q)
   for k in ('subsequent_client_execution_in_model','client_handler_entered_in_model','owner_failure_guard_evaluated_in_model','new_explicit_cause_assignment_established_in_model','runtime_observation','control_reaches_launcher_established','actual_admission','obligations_discharged','run_success_established'):bad('unsupported claim '+str((idx,k)),change(x,('output',k),True))
   for k,v in [('existing_cause',None),('existing_context',None),('existing_suppression',False),('cleanup_context_link','control-error'),('physical_reference_observation','same-object')]:bad('invented chain evidence '+str((idx,k)),change(x,('output','exception_chain_observation',k),v))
   class S(str):pass
   class I(int):pass
   class L(list):pass
   class M(dict):pass
   for p,v in [(('control_error','role'),S(x['control_error']['role'])),(('outcomes',),L(x['outcomes'])),(('control_error',),M(x['control_error'])),(('output','control_callback_raised_in_model'),I(1)),(('output','subsequent_client_execution_in_model'),0)]:bad('exact nested type '+str((idx,p)),change(x,p,v))
   q=D(x);v=q['control_error'].pop('role');q['control_error'][S('role')]=v;bad('subclassed literal key '+str(idx),q)
   ret=m._construct_checked(b,x);ret['projection']['events'].reverse();ret['projection']['control_error']['scope']['instance'].clear();good('returned result does not alter pristine expectations '+str(idx),x)
   v=m._premises(b,x);r.no('producer output boundary '+str(idx),lambda:b['fresh']['coverage'].validate_control_exception_projection(cat,x['projection'],v,change(x['output'],('completion',),'normal-return')))
  r.save('fixtures.json',fixtures)
  badrows=m._rows(b);badrows.reverse();badrows[0]['declaration']['source']['order'].reverse();r.no('mutated returned contexts and nested order',lambda:m._check_rows(b,badrows));r.yes('fresh rows unaffected by result mutations',lambda:m._rows(b)==rows)
  for label,q in [('omitted context',rows[:1]),('duplicated context',[rows[0],rows[0]]),('invented runtime frames',change(rows,(0,'runtime_control_exception_revocation_chain'),[])),('imported owner failure guard',change(rows,(1,'owner_failure_guard_applicable'),True))]:r.no('semantic '+label,lambda q=q:m._check_rows(b,q))
  for label,fn in [('missing evidence',lambda d:d.pop(next(iter(d)))),('altered evidence',lambda d:d.__setitem__(next(iter(d)),next(iter(d.values()))+b'\n'))]:
   e=D(b['evidence']);fn(e);r.no('authenticated '+label,lambda e=e:m._compare_evidence(b,e))
  if mode=='primary':
   # Newly integrated routes only; reuse the reviewed fixture bytes, not suites.
   prior_cases=json.loads((root/'retained/review/results/primary/fixtures.json').read_bytes())
   for i,q in enumerate(prior_cases):r.yes('preserved bare public bridge core '+str(i),lambda q=q:m._construct_prior(b,'bare',q)['projection']==q['output'])
   stored_cases=json.loads((root/'retained/bare/retained/review/results/primary/fixtures.json').read_bytes())
   for i in (0,3):
    q=stored_cases[i];r.yes('preserved stored-client bridge core '+str(i),lambda q=q:m._construct_prior(b,'stored-client',q)['projection']==q['output'])
   normal_cases=json.loads((root/'retained/bare/retained/callback/retained/stored/results/correction/fixtures.json').read_bytes())['cases']
   for i in (0,3):
    q=normal_cases[i];r.yes('preserved stored-normal bridge core '+str(i),lambda q=q:m._construct_prior(b,'stored-normal',q)['projection']==q['output'])
   for idx in (0,1):
    tc=token(b,idx,'FL6-control-normal-bridge-'+str(idx));tb=b['stored_basis']['token_basis'];c=tb['fresh']['coverage']
    steps=PREFIX+['client-create','client-callback','owner-failure-guard']+ORDER
    tc['outcomes']=[{'stage':s,'outcome':'normal'} for s in steps];tc['projection']['outcomes']=D(tc['outcomes'])
    v={k:D(w) for k,w in tc['projection'].items() if k!='references'};tc['output']=c.token_registration_projection(tb['catalogue'],tc['projection'],v)
    r.yes('preserved normal-token bridge core '+str(idx),lambda tc=tc:m._construct_prior(b,'normal-token',tc)['projection']==tc['output'])
  r.save('final-verification.json',verify_root(root))
 except BaseException:
  error=traceback.format_exc();r.save('failure.txt',error);raise
 finally:r.finish(error,mode=mode)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);p.add_argument('mode',choices=['primary','recovered']);a=p.parse_args();run(a.root,a.out,a.mode)
