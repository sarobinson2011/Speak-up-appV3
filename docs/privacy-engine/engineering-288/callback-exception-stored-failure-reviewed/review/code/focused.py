from pathlib import Path
import sys,ast,traceback,json
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import *
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);mode=sys.argv[3];err=None
class S(str):pass
class I(int):pass
class L(list):pass
class M(dict):pass
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data);print('Validate current mandatory predecessor chain',flush=True)
 rows,b=m._checked(data,cat);c=b['fresh']['coverage'];saved=(root/'results/primary/callback-stored-failure.json').read_bytes()
 rec.yes('exact canonical two-context derivation',lambda:m.enc(m._assemble(data,rows,b))==saved and [r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.save('derived-receipt-identity.json',ident(saved));fixtures=[]
 for idx in (0,1):
  for route in ('handle','state'):
   label=str(idx)+'/'+route;fx=normal(m,b,idx,route);fixtures.append(fx)
   rec.yes('valid source raise with explicit cause '+label,lambda x=fx:m._construct_checked(b,x)['projection']==x['output'] and independently_check(x))
   q=normal(m,b,idx,route,helper='raise',control=False,continuity=False);rec.yes('helper escape unknown continuity no control '+label,lambda q=q:m._construct_checked(b,q)['projection']==q['output'] and independently_check(q))
   alt=normal(m,b,idx,route,inv='FL6-other-'+label);rec.yes('distinct equal-error occurrences and callback roles '+label,lambda x=alt:x['output']['original_error']['reference']!=fx['output']['original_error']['reference'] and x['callback_error']['reference']!=fx['callback_error']['reference'])
   points=ORDER if mode=='primary' else ['callback-failure-guard','callback-stored-rethrow','removal-complete']
   for stage in points:
    for outcome in (('raise','process-termination','unobserved') if mode=='primary' else ('raise','process-termination')):
     q=normal(m,b,idx,route,terminal=(stage,outcome));rec.yes('source frontier '+label+'/'+stage+'/'+outcome,lambda q=q:m._construct_checked(b,q)['projection']==q['output'] and independently_check(q))
     q['output']['original_outward_after_finally_established_in_model']=True;rec.no('false original propagation '+label+'/'+stage+'/'+outcome,lambda q=q:m._construct_checked(b,q))
   for p,v in [(('callback_error','reference'),'wrong'),(('failure_result','original_exception','reference'),'wrong'),(('failure_input','references','owner','symbol'),'wrong'),(('failure_input','references','token','symbol'),'wrong'),(('token_case','invocation'),'other'),(('anchor','instance','binding'),'0'*64),(('output','run_success_established'),True),(('output','removal_completed_in_model'),1)]:
    q=change(fx,p,v);rec.no('wrong binding or false completion '+label+str(p),lambda q=q:m._construct_checked(b,q))
   rel=fx['output']['established_explicit_cause'];q=change(fx,('output','established_explicit_cause'),{**D(rel),'raised_error':D(rel['explicit_cause']),'explicit_cause':D(rel['raised_error'])});rec.no('cause direction reversal '+label,lambda q=q:m._construct_checked(b,q))
   q=replace(fx,fx['callback_error']['reference'],'coordinated-foreign-callback');rec.no('coordinated callback substitution '+label,lambda q=q:m._construct_checked(b,q))
   q=replace(fx,fx['failure_result']['original_exception']['reference'],'coordinated-foreign-original');rec.no('coordinated stored-original substitution '+label,lambda q=q:m._construct_checked(b,q))
   if mode=='primary':
    for action in ('omit-handler','omit-guard','omit-finally','duplicate-pop','reverse'):
     q=D(fx)
     if action.startswith('omit-'):q['outcomes'].pop({'omit-handler':0,'omit-guard':1,'omit-finally':3}[action])
     elif action=='duplicate-pop':q['outcomes'].append(D(q['outcomes'][-1]))
     else:q['outcomes'].reverse()
     q['projection']['outcomes']=D(q['outcomes']);rec.no('coordinated missing/reordered stages '+label+'/'+action,lambda q=q:m._construct_checked(b,q))
    for field in ('callback_error','failure_result','token_case','projection'):
     q=D(fx);del q[field];rec.no('missing required field '+label+'/'+field,lambda q=q:m._construct_checked(b,q))
    for p,v in [(('callback_error','binding_name'),S('client_error')),(('callback_error','catch_family'),S('BaseException')),(('projection','outcomes',2,'outcome'),S('raised-stored-from-client')),(('failure_result','retained_original'),1),(('token_case','owner_failure_none'),0),(('output','established_explicit_cause','suppress_context_in_model'),1)]:
     q=change(fx,p,v);rec.no('exact type '+label+str(p),lambda q=q:m._construct_checked(b,q))
    q=D(fx);q['callback_error']={S(k):v for k,v in q['callback_error'].items()};rec.no('literal key subclass '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('output','established_explicit_cause'),M(fx['output']['established_explicit_cause']));rec.no('dict subclass '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('outcomes',),L(fx['outcomes']));rec.no('list subclass '+label,lambda q=q:m._construct_checked(b,q))
    for p,v in [(('callback_error','exact_type'),'ClientFailure'),(('callback_error','physical_identity_relative_to_stored'),'DISTINCT'),(('output','established_explicit_cause','physical_identity_relative_to_stored'),'SAME'),(('output','established_explicit_cause','suppress_context_in_model'),False),(('output','established_explicit_cause','implicit_context_observation'),{}),(('output','database_cleanup_completion'),True)]:
     q=change(fx,p,v);rec.no('unsupported observation or semantics '+label+str(p),lambda q=q:m._construct_checked(b,q))
    q=change(fx,('failure_input','callback'),'returns');rec.no('normal-callback evidence cannot substitute '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('failure_input','outcomes','fixed-failure'),'process-termination');rec.no('helper termination cannot become caught callback error '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('failure_input','cleanup','revoke'),'normal');rec.no('opaque cleanup cannot supply revocation '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('outcomes',2,'outcome'),'normal');q['projection']['outcomes']=D(q['outcomes']);rec.no('source raise cannot become normal completion '+label,lambda q=q:m._construct_checked(b,q))
    q=normal(m,b,idx,route,terminal=('callback-failure-guard','raise'));q['outcomes'].insert(2,{'stage':'callback-stored-rethrow','outcome':'raised-stored-from-client'});q['projection']['outcomes']=D(q['outcomes']);rec.no('handler failure must skip later handler points '+label,lambda q=q:m._construct_checked(b,q))
    q=normal(m,b,idx,route,terminal=('finally-enter','process-termination'));q['output']['established_explicit_cause']=None;rec.no('later termination cannot erase established cause '+label,lambda q=q:m._construct_checked(b,q))
   got=m._construct_checked(b,fx);got['projection']['established_explicit_cause']['raised_error'].clear();got['projection']['callback_error'].clear();got['projection']['events'].reverse()
   rec.yes('nested result mutations leave expectations intact '+label,lambda:m._construct_checked(b,fx)['projection']==fx['output'])
  q=D(rows);q[idx]['declaration']['source']['cause_expression']='owner.failure';rec.no('semantic wrong cause '+str(idx),lambda q=q:m._check_rows(b,q))
  q=D(rows);q[idx]['declaration']['declarations'].pop();rec.no('semantic coverage omission '+str(idx),lambda q=q:m._check_rows(b,q))
  # Reuse exact reviewed finite input only, never execute its completed suite.
  original=json.loads((root/'retained/stored/results/correction/fixtures.json').read_bytes())['cases'][2*idx]
  rec.yes('reviewed normal-callback case still accepted through validated basis '+str(idx),lambda original=original:b['stored_module']._construct_checked(b['stored_basis'],original)['projection']==original['output'])
 for action in ('omit','duplicate','reverse'):
  q=D(rows)
  if action=='omit':q.pop()
  elif action=='duplicate':q[1]=D(q[0])
  else:q.reverse()
  rec.no('semantic contexts '+action,lambda q=q:m._check_rows(b,q))
 q=D(rows);q[0]['classification']=S('UNKNOWN');rec.no('semantic exact types before normalization',lambda:m._check_rows(b,q))
 q=D(rows);q[0]['outer_cleanup_complete']=True;rec.no('semantic cleanup escalation',lambda:m._check_rows(b,q))
 returned=m._assemble(data,rows,b);returned['contexts'].reverse();returned['contexts'][0]['callback_stored_failure_correspondence']['declaration']['source']['stages'].clear();rows[0]['reference_basis'].clear()
 rec.yes('returned contexts and nested rows cannot change canonical receipt',lambda:m.enc(m._assemble(data,m._rows(b),b))==saved)
 rec.save('fixtures.json',fixtures);rec.save('final-verification.json',verify_root(root))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,mode=mode)
