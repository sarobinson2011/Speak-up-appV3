"""Focused new construction-exception controls; no prior campaigns or runtime entry."""
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
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m)
 print('Loading mandatory predecessor input chain',flush=True);data=m.inputs(root)
 print('Deriving construction declarations from defining source',flush=True);cat=m.catalogue(data)
 print('Validating predecessor evidence for this new slice once',flush=True);rows,basis=m._checked(data,cat);c=basis['fresh']['coverage'];receipt=m._assemble(data,rows,basis);rec.save('control-construction.json',receipt)
 rec.check('both required symbolic contexts',lambda:[r['context'] for r in rows]==list(m.CONTEXTS))
 prior=json.loads(basis['saved']);rec.check('all predecessor context relations unchanged',lambda:all(all(receipt['contexts'][i][k]==v for k,v in prior['contexts'][i].items()) for i in (0,1)))
 entry=m.sources(data)[1];tree=ast.parse(entry);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');pt=run.body[2].body[0].body[-1];guard,client,post=pt.body;call=guard.body[0].value;pop=pt.finalbody[0]
 rec.check('independent AST argument construction precedes control invocation',lambda:ast.unparse(call)=='control(_Control(token))' and call.lineno==177 and call.args[0].lineno==177 and isinstance(call.args[0],ast.Call) and client.lineno==178 and not pt.handlers and pop.lineno==188)
 rec.check('independent exact guarded prefix and continuation coverage',lambda:cat['source']['prefix_order']==['owner-create','token-create','registry-insert','control-guard','control-create'] and cat['source']['order']==ORDER and ast.unparse(guard.test)=='control is not None')
 fixtures=[]
 for idx in (0,1):
  fx=normal(m,basis,idx);fixtures.append(fx);out=fx['output']
  rec.check('legitimate construction raise through normal removal '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  rec.check('no completed capability or callback execution '+str(idx),lambda out=out:out['construction_expression_raised_in_model'] and not out['construction_completed_in_model'] and out['completed_control_object_reference'] is None and out['allocation_progress'] is None and out['initializer_progress'] is None and not out['control_callback_executed_in_model'] and not out['subsequent_client_execution_in_model'])
  rec.check('normal finally leaves construction error pending '+str(idx),lambda out=out:out['construction_error']==out['outward_error_after_finally_in_model'] and out['removal_completed_in_model'] and not out['construction_reaches_launcher_established'])
  for continuity,owner_none in ((False,True),(True,False),(False,False)):
   q=normal(m,basis,idx,continuity=continuity,owner_none=owner_none);rec.check('conditional continuity and unreached owner guard '+str((idx,continuity,owner_none)),lambda q=q,continuity=continuity:m._construct_checked(basis,q)['projection']['selected_owner_removed_in_model'] is (True if continuity else None))
  other=normal(m,basis,idx,invocation='constructed-construction-B');rec.check('distinct selected attempts despite equal source '+str(idx),lambda:other['output']['construction_error']['occurrence']!=out['construction_error']['occurrence'])
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));z=q['output'];rec.check('legitimate frontier '+str((idx,stage,outcome)),lambda q=q:m._construct_checked(basis,q)['projection']==q['output'])
    rec.check('earlier registration and error survive uncertainty '+str((idx,stage,outcome)),lambda z=z:z['construction_expression_raised_in_model'] and z['validated_token_prefix']['registration_completed_in_model'] and z['construction_error']==out['construction_error'] and z['outward_error_after_finally_in_model'] is None)
    if outcome=='raise':rec.check('cleanup role can replace pending construction error '+str((idx,stage)),lambda z=z:z['cleanup_error_in_model']['reference']!=z['construction_error']['reference'] and z['last_pending_error_in_model']==z['cleanup_error_in_model'] and not z['removal_completed_in_model'])
    else:rec.check('termination is not terminal exception or unwind '+str((idx,stage,outcome)),lambda z=z:z['terminal_python_exception_in_model'] is None and z['cleanup_error_in_model'] is None and z['runtime_unwind_evidence']=='UNAVAILABLE')
    for field in ('removal_completed_in_model','construction_outward_after_finally_established_in_model','run_success_established'):
     bad=change(q,('output',field),True);rec.reject('false cleanup or propagation completion '+str((idx,stage,outcome,field)),lambda bad=bad:m._construct_checked(basis,bad))
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'removal-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('no later stage after stopped frontier '+str((idx,stage,outcome)),lambda bad=bad:m._construct_checked(basis,bad))
  for path,value in [
   (('construction_error','reference'),'other/error'),(('construction_error','construction_attempt','occurrence'),'other/attempt'),(('construction_error','scope','invocation'),'other'),(('construction_error','construction_attempt','argument_token','symbol'),'other'),(('construction_error','construction_attempt','registered_owner','symbol'),'other'),(('construction_error','local_handler_binding'),'client_error'),(('construction_error','failure_mechanism'),'MemoryError'),(('construction_error','initializer_progress'),'entered'),(('construction_error','completed_object_reference'),out['reference_bindings']['control']),
   (('token_case','invocation'),'other'),(('anchor',),{}),(('context',),'SYMBOLIC-U-OTHER'),(('projection','references','owner','symbol'),'other'),(('projection','references','token','symbol'),'other'),(('projection','scope','invocation'),'other'),
   (('output','construction_completed_in_model'),True),(('output','completed_control_object_reference'),out['reference_bindings']['control']),(('output','allocation_progress'),'allocated'),(('output','initializer_progress'),'assignment complete'),(('output','control_callback_executed_in_model'),True),(('output','subsequent_client_execution_in_model'),True),(('output','client_handler_entered_in_model'),True),(('output','owner_failure_guard_evaluated_in_model'),True),(('output','new_explicit_cause_assignment_established_in_model'),True),
   (('output','exception_chain_observation','existing_cause'),None),(('output','exception_chain_observation','existing_context'),None),(('output','exception_chain_observation','existing_suppression'),False),(('output','exception_chain_observation','cleanup_context_link'),'construction-error'),(('output','outward_error_after_finally_in_model','reference'),'other'),(('output','construction_reaches_launcher_established'),True),(('output','prior_failure_storage_history'),'NO-STORAGE'),(('output','observer_join'),{'frame':1}),(('output','revocation_persists'),True),(('output','physical_lock_release_established'),True),(('output','authorization_renewed'),True)]:
   q=change(fx,path,value);rec.reject('wrong binding or invented execution '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  for n in range(len(ORDER)):
   q=copy.deepcopy(fx);del q['outcomes'][n];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('coordinated missing stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
   q=copy.deepcopy(fx);q['outcomes'].insert(n,copy.deepcopy(q['outcomes'][n]));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('duplicate stage '+str((idx,n)),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx);q['outcomes'][:2]=reversed(q['outcomes'][:2]);q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('reordered finally and removal '+str(idx),lambda q=q:m._construct_checked(basis,q))
  q=change(fx,('output',),other['output']);rec.reject('cross invocation result '+str(idx),lambda q=q:m._construct_checked(basis,q))
  q=copy.deepcopy(fx)
  for v in (q['construction_error'],q['projection']['construction_error'],q['output']['construction_error'],q['output']['last_pending_error_in_model'],q['output']['outward_error_after_finally_in_model']):v['reference']='coordinated/wrong'
  rec.reject('coordinated exception substitution '+str(idx),lambda q=q:m._construct_checked(basis,q))
  for path,value in [(('context',),S(fx['context'])),(('construction_error',),D(fx['construction_error'])),(('outcomes',),L(fx['outcomes'])),(('outcomes',0,'stage'),S(ORDER[0])),(('output','removal_completed_in_model'),1),(('construction_error',),{S(k):v for k,v in fx['construction_error'].items()}),(('output','construction_error'),{S(k):v for k,v in out['construction_error'].items()}),(('projection','token_inputs','control_present'),1),(('output','events',0,'source','source','bytes'),I(out['events'][0]['source']['source']['bytes']))]:
   q=change(fx,path,value);rec.reject('exact nested type or key '+str((idx,path)),lambda q=q:m._construct_checked(basis,q))
  for field in ('reference','failure_mechanism','completed_object_reference'):
   v=m._premises(basis,fx);q=copy.deepcopy(fx['projection']);v['construction_error'][field]='coordinated';q['construction_error'][field]='coordinated';rec.reject('direct projector coordinated error '+str((idx,field)),lambda q=q,v=v:c.control_construction_projection(cat,q,v))
  q=copy.deepcopy(fx['projection']);q['token_prefix']['control_callback_completed_in_model']=True;rec.reject('projector recomputes prefix '+str(idx),lambda q=q:c.control_construction_projection(cat,q,copy.deepcopy(q)))
  q=copy.deepcopy(out);q['construction_completed_in_model']=True;rec.reject('submitted output invented completion '+str(idx),lambda q=q:c.validate_control_construction_projection(cat,fx['projection'],m._premises(basis,fx),q))
  got=m._construct_checked(basis,fx);got['projection']['construction_error'].clear();got['projection']['events'].clear();got['projection']['reference_bindings']['owner'].clear();rec.check('nested result mutations isolated '+str(idx),lambda fx=fx:m._construct_checked(basis,fx)['projection']==fx['output'])
  q=copy.deepcopy(rows);q[idx]['construction_completed']=True;q[idx]['declaration']['source']['completed_control_object_established']=True;rec.reject('coordinated semantic completion claim '+str(idx),lambda q=q:m._check_rows(basis,q))
 rec.save('fixtures.json',fixtures)
 for label,mut in [('missing-context',lambda q:q.pop()),('missing-declaration',lambda q:q[0]['declaration']['declarations'].pop()),('missing-guard',lambda q:q[1]['declaration']['guard_branches'].pop('constructor_progress')),('reordered-both',lambda q:[r['declaration']['source']['order'].reverse() for r in q]),('subclass-key',lambda q:q[0].update({'declaration':{S(k):v for k,v in q[0]['declaration'].items()}}))]:
  q=copy.deepcopy(rows);mut(q);rec.reject('semantic '+label,lambda q=q:m._check_rows(basis,q))
 got=m._assemble(data,rows,basis);got['contexts'].clear();got=m._rows(basis);got[0]['declaration']['source'].clear();rec.reject('mutated returned rows reject',lambda:m._check_rows(basis,got));rec.check('pristine receipt after output mutations',lambda:m.enc(m._assemble(data,m._rows(basis),basis))==m.enc(receipt))
 mixed=dict(basis['evidence']);k=next(iter(mixed));mixed[k]+=b' ';rec.reject('mixed predecessor evidence',lambda:m._compare_evidence(basis,mixed))
 # One preservation connection per prior branch/context, not historical campaigns.
 cb=basis['control_basis'];bb=cb['bare_basis'];sb=basis['stored_basis'];client=bb['callback_basis']
 routes={'control':(basis['control_module'],cb,cb['fresh']['root']),'bare':(cb['bare_module'],bb,bb['fresh']['root']),'stored-client':(bb['callback_module'],client,client['fresh']['root']),'stored-normal':(client['stored_module'],sb,sb['fresh']['root']),'normal-token':(sb['routes']['token_module'],sb['token_basis'],sb['token_basis']['fresh']['root'])}
 for branch,(pm,pb,pr) in routes.items():
  factory=m.module(pr/'tests/cases.py','_prior_case')
  for idx in (0,1):
   fx=factory.normal(pm,pb,idx);rec.check('new mandatory entry preserves branch '+str((branch,idx)),lambda fx=fx,branch=branch:m._construct_prior(basis,branch,fx)['projection']==fx['output'])
 rec.reject('public semantic exact type before normalization',lambda:m.semantic(data,D(cat)))
 rec.reject('public constructed exact type before normalization',lambda:m.constructed_projection(data,cat,D(fixtures[0])))
 rec.reject('public derivation exact type before normalization',lambda:m.derive_construction(data,D(cat)))
 print('Checking independently source-derived rejection of altered construction argument',flush=True)
 rec.reject('altered defining construction token',lambda:c.compile_control_construction(m.sources(data)[0],entry.replace(b'control(_Control(token))',b'control(_Control(owner))'),*m.dependencies(data)))
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New construction-exception slice only; preceding results remain separate')
