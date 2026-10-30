"""New control-callback slice only; prior campaigns are not invoked."""
from pathlib import Path
import sys,copy,json,ast,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data)
 print('Validating mandatory saved predecessor evidence once for the new slice',flush=True);rows,basis=m._checked(data,cat);c=basis['fresh']['coverage'];receipt=m._assemble(data,rows,basis);rec.save('control-exception.json',receipt)
 rec.check('both contexts mandatory',lambda:[x['context'] for x in rows]==list(m.CONTEXTS))
 prior=json.loads(basis['saved']);rec.check('all reviewed context relations byte-value preserved',lambda:all(all(receipt['contexts'][i][k]==v for k,v in prior['contexts'][i].items()) for i in (0,1)))
 entry=m.sources(data)[1];tree=ast.parse(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');protected=run.body[2].body[0].body[-1];control,client,post=protected.body;pop=protected.finalbody[0]
 rec.check('independent source control call outside client handler',lambda:control.body[0].lineno==177 and isinstance(client,ast.Try) and client.lineno>control.end_lineno and not protected.handlers and pop.lineno==188 and ast.unparse(control.test)=='control is not None')
 rec.check('source-derived stages and excluded client guards',lambda:cat['source']['order']==ORDER and cat['source']['client_handler_applies'] is False and cat['source']['owner_failure_guard_applies'] is False and cat['source']['new_explicit_cause_assignment'] is False)
 fixtures=[]
 for idx in (0,1):
  fx=normal(m,basis,idx);fixtures.append(fx);out=fx['output'];rec.check('legitimate control raise and normal removal '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  rec.check('selected error pending after normal finally '+str(idx),lambda out=out:out['control_error']==out['outward_error_after_finally_in_model'] and out['removal_completed_in_model'] and not out['subsequent_client_execution_in_model'])
  for continuity,owner_none in ((False,True),(True,False),(False,False)):
   q=normal(m,basis,idx,continuity=continuity,owner_none=owner_none);rec.check('no client guard imported and owner continuity conditional '+str((idx,continuity,owner_none)),lambda q=q,continuity=continuity:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is (True if continuity else None))
  other=normal(m,basis,idx,invocation='constructed-control-B');rec.check('distinct control/error occurrences '+str(idx),lambda:other['output']['control_error']['occurrence']!=out['control_error']['occurrence'])
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));z=q['output'];rec.check('legitimate frontier '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'])
    rec.check('earlier prefix facts survive '+str((idx,stage,outcome)),lambda z=z:z['control_callback_raised_in_model'] and z['validated_token_prefix']['registration_completed_in_model'] and z['control_error']==out['control_error'] and z['outward_error_after_finally_in_model'] is None)
    if outcome=='raise':rec.check('cleanup error distinct role without physical inequality '+str((idx,stage)),lambda z=z:z['cleanup_error_in_model']['reference']!=z['control_error']['reference'] and z['last_pending_error_in_model']==z['cleanup_error_in_model'] and not z['removal_completed_in_model'])
    else:rec.check('termination supplies no terminal exception/unwind '+str((idx,stage,outcome)),lambda z=z:z['terminal_python_exception_in_model'] is None and z['cleanup_error_in_model'] is None and z['runtime_unwind_evidence']=='UNAVAILABLE')
    for field in ('removal_completed_in_model','control_outward_after_finally_established_in_model','run_success_established'):
     bad=change(q,('output',field),True);rec.reject('false frontier completion '+str((idx,stage,outcome,field)),lambda bad=bad:m._construct_checked(basis,bad))
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'removal-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('continuation after stopped frontier '+str((idx,stage,outcome)),lambda bad=bad:m._construct_checked(basis,bad))
  for path,value in [
   (('control_error','reference'),'other/error'),(('control_error','callback_occurrence'),'other/callback'),(('control_error','callee'),'client'),(('control_error','scope','invocation'),'other'),(('control_error','callback_argument_reference','symbol'),'other'),(('control_error','local_handler_binding'),'client_error'),(('control_error','source','site'),'179:0:179:1:Expr'),(('token_case','invocation'),'other'),(('anchor',),{}),(('context',),'SYMBOLIC-U-OTHER'),(('projection','references','owner','symbol'),'other'),(('projection','references','token','symbol'),'other'),(('projection','references','control','symbol'),'other'),(('projection','scope','invocation'),'other'),
   (('output','subsequent_client_execution_in_model'),True),(('output','client_handler_entered_in_model'),True),(('output','owner_failure_guard_evaluated_in_model'),True),(('output','new_explicit_cause_assignment_established_in_model'),True),(('output','exception_chain_observation','existing_cause'),None),(('output','exception_chain_observation','existing_context'),None),(('output','exception_chain_observation','existing_suppression'),False),(('output','exception_chain_observation','cleanup_context_link'),'control-error'),(('output','outward_error_after_finally_in_model','reference'),'other'),(('output','control_reaches_launcher_established'),True),(('output','run_success_established'),True),(('output','prior_failure_storage_history'),'NO-EARLIER-STORAGE'),(('output','observer_join'),{'frame':1}),(('output','revocation_persists'),True),(('output','physical_lock_release_established'),True),(('output','authorization_renewed'),True)]:
   q=change(fx,path,value);rec.reject('wrong binding or unsupported claim '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  for n in range(len(ORDER)):
   q=copy.deepcopy(fx);del q['outcomes'][n];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('coordinated missing stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['outcomes'].insert(n,copy.deepcopy(q['outcomes'][n]));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('duplicate stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['outcomes'][0:2]=reversed(q['outcomes'][0:2]);q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('reordered entry and attempt '+str(idx),lambda q=q:m._construct_checked(basis,q))
  q=change(fx,('output',),other['output']);rec.reject('cross-invocation result '+str(idx),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx)
  for loc in (q['control_error'],q['projection']['control_error'],q['output']['control_error'],q['output']['outward_error_after_finally_in_model'],q['output']['last_pending_error_in_model']):loc['reference']='coordinated/wrong'
  rec.reject('coordinated error substitution '+str(idx),lambda q=q:m._construct_checked(basis,q))
  for path,value in [(('context',),S(fx['context'])),(('control_error',),D(fx['control_error'])),(('outcomes',),L(fx['outcomes'])),(('outcomes',0,'stage'),S(ORDER[0])),(('output','removal_completed_in_model'),1),(('control_error',),{S(k):v for k,v in fx['control_error'].items()}),(('output','control_error'),{S(k):v for k,v in out['control_error'].items()}),(('projection','token_inputs','control_present'),1),(('output','events',0,'source','source','bytes'),I(out['events'][0]['source']['source']['bytes']))]:
   q=change(fx,path,value);rec.reject('exact nested type/key '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  v=m._premises(basis,fx);q=copy.deepcopy(fx['projection']);v['control_error']['reference']='wrong';q['control_error']['reference']='wrong';rec.reject('projector rejects mutually consistent wrong exception '+str(idx),lambda q=q,v=v:c.control_exception_projection(cat,q,v))
  q=copy.deepcopy(fx['projection']);q['token_prefix']['control_callback_completed_in_model']=True;v=copy.deepcopy(q);rec.reject('projector recomputes prefix instead of trusting paired reports '+str(idx),lambda q=q,v=v:c.control_exception_projection(cat,q,v))
  q=copy.deepcopy(out);q['client_handler_entered_in_model']=True;rec.reject('submitted-output boundary '+str(idx),lambda q=q:c.validate_control_exception_projection(cat,fx['projection'],m._premises(basis,fx),q))
  got=m._construct_checked(basis,fx);got['projection']['control_error'].clear();got['projection']['reference_bindings']['owner'].clear();got['projection']['events'].clear();rec.check('nested result mutations cannot change expectations '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  q=copy.deepcopy(rows);q[idx]['declaration']['source']['client_handler_applies']=True;rec.reject('semantic client-handler substitution '+str(idx),lambda q=q:m._check_rows(basis,q))
 rec.save('fixtures.json',fixtures)
 for label,mut in [('omit-context',lambda q:q.pop()),('omit-declaration',lambda q:q[0]['declaration']['declarations'].pop()),('omit-guard',lambda q:q[1]['declaration']['guard_branches'].pop('client')),('both-wrong-order',lambda q:[r['declaration']['source']['order'].reverse() for r in q]),('subclass-key',lambda q:q[0].update({'declaration':{S(k):v for k,v in q[0]['declaration'].items()}}))]:
  q=copy.deepcopy(rows);mut(q);rec.reject('semantic claim '+label,lambda q=q:m._check_rows(basis,q))
 got=m._assemble(data,rows,basis);got['contexts'].clear();got=m._rows(basis);got[0]['declaration']['source'].clear();rec.reject('mutated returned rows rejected',lambda:m._check_rows(basis,got));rec.check('pristine receipt after mutable returned objects',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==m.enc(receipt))
 bad=dict(basis['evidence']);key=next(iter(bad));bad[key]=bad[key]+b' ';rec.reject('stale/mixed predecessor evidence',lambda:m._compare_evidence(basis,bad))
 # Narrow new-entry preservation controls, not old campaigns.
 bb=basis['bare_basis'];sb=basis['stored_basis'];cb=bb['callback_basis']
 factories={'bare':(basis['bare_module'],bb,basis['fresh']['prior_root']),'stored-client':(bb['callback_module'],cb,bb['fresh']['prior_root']),'stored-normal':(cb['stored_module'],sb,cb['fresh']['prior_root']),'normal-token':(sb['routes']['token_module'],sb['token_basis'],sb['token_basis']['fresh']['root'])}
 for branch,(pm,pb,pr) in factories.items():
  factory=m.module(pr/'tests/cases.py','_prior_case_factory')
  for idx in (0,1):
   fx=factory.normal(pm,pb,idx);rec.check('existing branch preserved by new mandatory entry '+str((branch,idx)),lambda fx=fx,branch=branch:m._construct_prior(basis,branch,fx)['projection']==fx['output'])
 for label,new in [('wrong-control-guard',entry.replace(b'if control is not None:',b'if control is None:')),('wrong-callback',entry.replace(b'control(_Control(token))',b'client(_Control(token))')),('wrong-token',entry.replace(b'control(_Control(token))',b'control(_Control(owner))')),('wrong-pop',entry.replace(b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)')),('invented-cause',entry.replace(b'control(_Control(token))',b'raise owner.failure from client_error'))]:
  rec.reject('source independently rejects '+label,lambda new=new:c.compile_control_exception(m.sources(data)[0],new,*m.dependencies(data)))
 for kind in ('declaration','guard','source','token'):
  q=copy.deepcopy(cat)
  if kind=='declaration':q['declarations'].pop()
  elif kind=='guard':del q['guard_branches']['client']
  elif kind=='source':q['source']['owner_failure_guard_applies']=True
  else:q['token_relation']['source']['order'].remove('control-callback')
  rec.reject('catalogue coordinated omission '+kind,lambda q=q:c.validate_control_exception(*m.sources(data)[:2],*m.dependencies(data),q))
 rec.reject('public semantic exact types before normalization',lambda:m.semantic(data,D(cat)))
 rec.reject('public constructed exact types before normalization',lambda:m.constructed_projection(data,cat,D(fixtures[0])))
 rec.reject('public derivation exact types before normalization',lambda:m.derive_control(data,D(cat)))
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New control-callback slice only; independent prior results and campaigns remain separate')
