"""Focused new-slice controls, never application execution or a prior suite."""
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
 print('Validating mandatory predecessor evidence once for the new primary controls',flush=True);rows,basis=m._checked(data,cat);c=basis['fresh']['coverage'];receipt=m._assemble(data,rows,basis);rec.save('callback-bare-rethrow.json',receipt);rec.save('receipt-identity.json',identity(m.enc(receipt)));rec.check('both contexts independently present',lambda:[x['context'] for x in rows]==list(m.CONTEXTS))
 prior=json.loads(basis['saved']);rec.check('both reviewed stored-failure relations exact in new receipt',lambda:all(receipt['contexts'][i][k]==prior['contexts'][i][k] for i in (0,1) for k in ('stored_failure_revocation_correspondence','callback_stored_failure_correspondence')))
 entry=m.sources(data)[1];tree=ast.parse(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');handlers=[n for n in ast.walk(run) if isinstance(n,ast.ExceptHandler) and n.name=='client_error'];assert len(handlers)==1
 h=handlers[0];g=h.body[0];b=h.body[1];rec.check('independent defining AST selects exact None false branch and expression-free raise',lambda:isinstance(g.test,ast.Compare) and type(g.test.comparators[0].value) is type(None) and isinstance(g.test.ops[0],ast.IsNot) and isinstance(b,ast.Raise) and b.exc is b.cause is None and not g.orelse)
 rec.check('source-derived order not supplied catalogue expectation',lambda:cat['source']['order']==ORDER and cat['source']['raise']['site'].startswith(str(b.lineno)+':') and cat['source']['guard']['site'].startswith(str(g.test.lineno)+':'))
 fixtures=[]
 for idx in (0,1):
  fx=normal(m,basis,idx);fixtures.append(fx);out=fx['output'];rec.check('legitimate bare rethrow '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output']);rec.check('same callback semantic error and unknown pre-existing chain '+str(idx),lambda out=out:out['reraised_error_in_model']==out['callback_error']==out['outward_error_after_finally_in_model'] and out['bare_rethrow_completed_in_model'] and out['new_explicit_cause_assignment_established_in_model'] is False and out['exception_chain_observation']['existing_cause']=='UNKNOWN' and out['exception_chain_observation']['existing_context']=='UNKNOWN')
  for ctrl,continuity in ((False,True),(True,False),(False,False)):
   q=normal(m,basis,idx,control=ctrl,continuity=continuity);rec.check('admitted optional control/continuity '+str((idx,ctrl,continuity)),lambda q=q,continuity=continuity:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['selected_owner_removed_in_model'] is (True if continuity else None))
  other=normal(m,basis,idx,invocation='constructed-bare-B');rec.check('distinct invocation occurrences with same None and unknown fields '+str(idx),lambda:other['output']['callback_error']['reference']!=out['callback_error']['reference'] and other['output']['scope']!=out['scope'])
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));z=q['output'];rec.check('legitimate frontier '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'])
    if outcome in ('process-termination','unobserved'):
     rec.check('no inferred unwind/completion '+str((idx,stage,outcome)),lambda z=z:z['terminal_python_exception_in_model'] is None and not z['removal_completed_in_model'] and z['outward_error_after_finally_in_model'] is None)
    elif ORDER.index(stage)<3:
     rec.check('evaluation error pending after conditional normal cleanup '+str((idx,stage)),lambda z=z:z['handler_evaluation_error_in_model'] is not None and z['removal_completed_in_model'] and not z['bare_rethrow_completed_in_model'] and not z['callback_outward_after_finally_established_in_model'])
    else:
     rec.check('cleanup replacement without original callback guarantee '+str((idx,stage)),lambda z=z:z['cleanup_error_in_model'] is not None and not z['removal_completed_in_model'] and z['callback_error']==out['callback_error'] and not z['callback_outward_after_finally_established_in_model'])
    changed=copy.deepcopy(q);changed['output']['callback_outward_after_finally_established_in_model']=True;rec.reject('reject frontier propagation invention '+str((idx,stage,outcome)),lambda q=changed:m._construct_checked(basis,q))
    if not z['removal_completed_in_model']:
     changed=change(q,('output','removal_completed_in_model'),True);rec.reject('reject false removal completion '+str((idx,stage,outcome)),lambda q=changed:m._construct_checked(basis,q))
     changed=copy.deepcopy(q);changed['outcomes'].append({'stage':'removal-complete','outcome':'normal'});changed['projection']['outcomes']=copy.deepcopy(changed['outcomes']);rec.reject('reject continuation after stopped frontier '+str((idx,stage,outcome)),lambda q=changed:m._construct_checked(basis,q))
  for path,value in [
   (('callback_error','reference'),'other/error'),(('callback_error','scope','invocation'),'foreign'),(('none_guard_binding','owner','symbol'),'foreign'),(('none_guard_binding','slot_value'),False),(('none_guard_binding','slot_value'),0),(('none_guard_binding','guard_result'),True),(('none_guard_binding','slot_exact_type'),'bool'),(('none_guard_binding','guard_source','line'),184),(('token_case','invocation'),'other'),(('anchor',),{}),(('projection','references','token','symbol'),'foreign'),(('projection','scope','invocation'),'foreign'),(('context',),'SYMBOLIC-U-OTHER'),
   (('output','reraised_error_in_model','reference'),'replacement'),(('output','new_explicit_cause_assignment_established_in_model'),True),(('output','exception_chain_observation','existing_cause'),None),(('output','exception_chain_observation','existing_context'),None),(('output','exception_chain_observation','existing_suppression'),False),(('output','bare_raise_semantics','adds_explicit_cause'),True),(('output','run_success_established'),True),(('output','prior_failure_storage_history'),'NO-EARLIER-STORAGE'),(('output','callback_reaches_launcher_established'),True),(('output','observer_join'),{'frame':1})]:
   q=change(fx,path,value);rec.reject('altered binding/claim '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  for n in range(len(ORDER)):
   q=copy.deepcopy(fx);del q['outcomes'][n];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('coordinated missing stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['outcomes'].insert(n,copy.deepcopy(q['outcomes'][n]));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('duplicate stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['outcomes'][1:3]=reversed(q['outcomes'][1:3]);q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('reordered guard and raise '+str(idx),lambda:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['outcomes'][2]['outcome']='normal';q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('bare raise is not normal return '+str(idx),lambda:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['output']=copy.deepcopy(other['output']);rec.reject('cross-invocation result substitution '+str(idx),lambda:m._construct_checked(basis,q))
  q=copy.deepcopy(fx)
  for loc in (q['callback_error'],q['projection']['callback_error'],q['output']['callback_error'],q['output']['reraised_error_in_model'],q['output']['outward_error_after_finally_in_model']):loc['reference']='coordinated/foreign'
  rec.reject('coordinated callback substitution '+str(idx),lambda:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['token_case']['owner_failure_none']=False;rec.reject('stored branch cannot select None relation '+str(idx),lambda:m._construct_checked(basis,q))
  for path,value in [(('context',),S(fx['context'])),(('none_guard_binding','slot_exact_type'),S('NoneType')),(('none_guard_binding',),D(fx['none_guard_binding'])),(('outcomes',),L(fx['outcomes'])),(('outcomes',0,'stage'),S(ORDER[0])),(('output','none_guard_completed_in_model'),1),(('callback_error',),{S(k):v for k,v in fx['callback_error'].items()}),(('output','callback_error'),{S(k):v for k,v in out['callback_error'].items()})]:
   q=change(fx,path,value);rec.reject('exact input/output nested type '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['projection']['outcomes']=L(q['projection']['outcomes']);v=m._premises(basis,fx);rec.reject('direct projector container type '+str(idx),lambda:c.callback_bare_projection(cat,q['projection'],v))
  v=m._premises(basis,fx);q=copy.deepcopy(fx['projection']);v['callback_error']['reference']='coordinated';q['callback_error']['reference']='coordinated';rec.reject('direct projector rejects mutually matching wrong error '+str(idx),lambda:c.callback_bare_projection(cat,q,v))
  q=copy.deepcopy(out);q['exception_chain_observation']['existing_cause']=False;rec.reject('direct submitted output rejects absent cause claim '+str(idx),lambda:c.validate_callback_bare_projection(cat,fx['projection'],m._premises(basis,fx),q))
  got=m._construct_checked(basis,fx);got['projection']['callback_error'].clear();got['projection']['none_guard_binding']['owner'].clear();got['projection']['events'].clear();rec.check('returned nested output cannot mutate expectations '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==out)
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['selected_slot_value']=False;rec.reject('semantic claims wrong guard '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
  claims=copy.deepcopy(rows);claims[idx]={S(k):v for k,v in claims[idx].items()};rec.reject('semantic exact literal keys '+str(idx),lambda claims=claims:m._check_rows(basis,claims))
 rec.save('fixtures.json',fixtures)
 for mut in ('omit-context','omit-declaration','omit-guard','wrong-raise','invented-cause'):
  q=copy.deepcopy(rows)
  if mut=='omit-context':q.pop()
  else:
   for r in q:
    if mut=='omit-declaration':r['declaration']['declarations'].pop(2)
    elif mut=='omit-guard':del r['declaration']['guard_branches']['slot']
    elif mut=='wrong-raise':r['declaration']['source']['raise_expression']='client_error'
    else:r['declaration']['source']['bare_raise_has_explicit_cause_clause']=True
  rec.reject('coordinated catalogue/claim '+mut,lambda q=q:m._check_rows(basis,q))
 out=m._assemble(data,rows,basis);out['contexts'].clear();rows[0]['conditional_links'].clear();rec.reject('mutated returned rows do not become expectations',lambda:m._check_rows(basis,rows));rows=m._rows(basis);rec.check('pristine bundle survives returned nested mutation',lambda:m.enc(m._assemble(data,rows,basis))==m.enc(receipt))
 bad=dict(basis['evidence']);key=next(iter(bad));bad[key]=bad[key]+b' ';rec.reject('predecessor evidence mutation',lambda:m._compare_evidence(basis,bad))
 cb=basis['callback_basis'];prior_module=basis['callback_module'];prior_factory=m.module(basis['fresh']['prior_root']/'tests/cases.py','_prior_callback_cases')
 normal_factory=m.module(cb['fresh']['prior_root']/'tests/cases.py','_prior_normal_cases')
 for idx in (0,1):
  prior_case=prior_factory.normal(prior_module,cb,idx,route='state');rec.check('adjacent stored-callback relation preserved '+str(idx),lambda prior_case=prior_case:prior_module._construct_checked(cb,prior_case)['projection']==prior_case['output'])
  normal_case=normal_factory.normal(cb['stored_module'],cb['stored_basis'],idx);rec.check('adjacent normal-callback stored failure preserved '+str(idx),lambda normal_case=normal_case:cb['stored_module']._construct_checked(cb['stored_basis'],normal_case)['projection']==normal_case['output'])
 # Every expected source point originates in the defining AST. These are new source variants, not a prior suite.
 deps=m.dependencies(data);launcher=m.sources(data)[0]
 for label,new in [('explicit-callback',entry.replace(b'                    raise\n',b'                    raise client_error\n',1)),('new-cause',entry.replace(b'                    raise\n',b'                    raise client_error from None\n',1)),('equality-guard',entry.replace(b'if owner.failure is not None:',b'if owner.failure != None:',1)),('wrong-pop',entry.replace(b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)'))]:
  rec.reject('defining source independent '+label,lambda new=new:c.compile_callback_bare(launcher,new,*deps))
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New callback bare-rethrow construction only; no prior suite or review rerun')
