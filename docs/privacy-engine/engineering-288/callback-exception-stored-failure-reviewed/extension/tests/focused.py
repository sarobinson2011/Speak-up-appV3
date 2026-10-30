"""New bounded callback-exception controls, not a historical suite rerun."""
from pathlib import Path
import sys,copy,json,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
class D(dict):pass
class L(list):pass
class I(int):pass
try:
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];bundle=m._assemble(data,rows,basis)
 rec.check('mandatory predecessor chain and both contexts',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and any(x['function']=='derive_status' for x in CALLS))
 rec.check('all prior context fields including normal callback preserved',lambda:all(all(bundle['contexts'][i][k]==v for k,v in ctx.items()) for i,ctx in enumerate(basis['prior']['contexts'])))
 tree=ast.parse(m.sources(data)[1]);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');calltry=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and any(isinstance(h,ast.ExceptHandler) and h.name=='client_error' for h in n.handlers));handler=calltry.handlers[0];guard_=handler.body[0];raise_=guard_.body[0]
 rec.check('independent handler guard raise and explicit cause',lambda:ast.unparse(handler.type)=='BaseException' and ast.unparse(guard_.test)=='owner.failure is not None' and ast.unparse(raise_)=='raise owner.failure from client_error' and raise_.lineno==182)
 rec.check('independent coverage and excluded bare rethrow',lambda:cat['source']['order']==ORDER and [d['id'] for d in cat['declarations']]==ORDER and handler.body[1].exc is None)
 rec.save('source-oracle.json',{'handler':ast.dump(handler,include_attributes=False),'guard':ast.dump(guard_.test,include_attributes=False),'order':ORDER,'source':identity(m.sources(data)[1])})
 fixtures=[]
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx);st=normal(m,basis,idx,route='state');fixtures.extend([fx,st])
  def ok(label,q):return rec.check(label+' '+tag,lambda:m._construct_checked(basis,q)['projection']==q['output'])
  def no(label,q):return rec.reject(label+' '+tag,lambda:m._construct_checked(basis,q))
  for route in ('handle','state'):
   ok('validated stored provenance '+route,normal(m,basis,idx,route=route));ok('stored error survives helper escape '+route,normal(m,basis,idx,route=route,helper='raise'))
  ok('handle underlying-call conditional failure',normal(m,basis,idx,origin='session-call'));ok('optional control omitted',normal(m,basis,idx,control=False))
  un=normal(m,basis,idx,continuity=False);ok('unknown registry continuity',un);rec.check('unknown owner cannot establish selected removal '+tag,lambda:un['output']['selected_owner_removed_in_model'] is None and un['output']['removal_completed_in_model'])
  rec.check('caught error is explicit cause of stored original only '+tag,lambda:fx['output']['established_explicit_cause']['raised_error']==fx['failure_result']['original_exception'] and fx['output']['established_explicit_cause']['explicit_cause']==fx['callback_error'] and fx['output']['outward_error_after_finally_in_model']==fx['failure_result']['original_exception'] and not fx['output']['callback_returned_normally_in_model'] and not fx['output']['run_success_established'])
  rec.check('separate roles do not assert physical inequality '+tag,lambda:fx['output']['established_explicit_cause']['physical_identity_relative_to_stored']=='UNKNOWN' and fx['callback_error']['exact_type'] is None and fx['output']['implicit_context_observation'] is None)
  for stage in ORDER:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));ok(stage+' '+outcome,q)
    rec.check('storage survives '+stage+outcome+' '+tag,lambda q=q:q['output']['failure_storage_previously_completed_in_model'] and q['output']['original_error']==fx['output']['original_error'] and not q['output']['run_success_established'])
    pre=ORDER.index(stage)<3
    if pre and outcome=='raise':rec.check('handler evaluation error goes to finally '+stage+' '+tag,lambda q=q:q['output']['removal_completed_in_model'] and q['output']['established_explicit_cause'] is None and q['output']['outward_error_after_finally_in_model']==q['output']['handler_evaluation_error_in_model'])
    else:rec.check('no inferred completed removal '+stage+outcome+' '+tag,lambda q=q:not q['output']['removal_completed_in_model'] and q['output']['outward_error_after_finally_in_model'] is None)
    if outcome in ('process-termination','unobserved'):rec.check('no terminal Python unwind '+stage+outcome+' '+tag,lambda q=q:q['output']['terminal_python_exception_in_model'] is None and q['output']['runtime_unwind_evidence']=='UNAVAILABLE')
    if not pre:
     rec.check('completed cause assignment survives cleanup frontier '+stage+outcome+' '+tag,lambda q=q:q['output']['established_explicit_cause']==fx['output']['established_explicit_cause']);no('no guarantee original propagation '+stage+outcome,change(q,('output','original_outward_after_finally_established_in_model'),True))
    if not q['output']['removal_completed_in_model']:no('false completed removal '+stage+outcome,change(q,('output','removal_completed_in_model'),True))
    no('no successful run '+stage+outcome,change(q,('output','run_success_established'),True))
    if outcome in ('process-termination','unobserved') or not pre:
     bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'removal-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('false continuation '+stage+outcome,bad)
  for stage in ORDER:
   q=copy.deepcopy(fx);q['outcomes']=[r for r in q['outcomes'] if r['stage']!=stage];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);no('missing '+stage,q)
   q=copy.deepcopy(fx);q['outcomes'].insert(0,copy.deepcopy(next(r for r in q['outcomes'] if r['stage']==stage)));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);no('duplicate '+stage,q)
  q=copy.deepcopy(fx);q['outcomes'].reverse();q['projection']['outcomes']=copy.deepcopy(q['outcomes']);no('reordered stages',q)
  q=copy.deepcopy(fx);q['outcomes'][2]['outcome']='normal';q['projection']['outcomes']=copy.deepcopy(q['outcomes']);no('raise becomes normal return',q)
  for path,value in [(('callback_error','reference'),'foreign'),(('output','established_explicit_cause','explicit_cause','reference'),'foreign'),(('output','established_explicit_cause','raised_error','reference'),'foreign'),(('projection','stored_error_binding','owner','symbol'),'foreign'),(('projection','references','token','symbol'),'foreign'),(('token_case','invocation'),'foreign'),(('failure_input','references','owner','symbol'),'foreign'),(('failure_input','occurrence'),'foreign'),(('failure_input','callback'),'returns'),(('failure_input','cleanup','revoke'),'normal'),(('anchor','instance','binding'),'0'*64),(('projection','scope','acquisition'),'stale'),(('projection','stored_error_binding','guard_slot_premise'),'established runtime fact'),(('output','authorization_renewed'),True),(('output','original_reaches_launcher_established'),True),(('output','database_cleanup_completion'),True),(('output','established_explicit_cause','suppress_context_in_model'),False),(('output','callback_error','physical_identity_relative_to_stored'),'DISTINCT')]:no('binding '+str(path),change(fx,path,value))
  for routecase in (fx,st):
   q=copy.deepcopy(routecase);q['failure_input']['outcomes']['retain-error']='process-termination';no('no storage after termination '+q['failure_route'],q)
   q=copy.deepcopy(routecase);q['failure_input']['outcomes']['fixed-failure']='process-termination';no('termination cannot become caught callback raise '+q['failure_route'],q)
  q=copy.deepcopy(fx);q['callback_error']['reference']='foreign';q['projection']['callback_error']=copy.deepcopy(q['callback_error']);q['output']['callback_error']=copy.deepcopy(q['callback_error']);q['output']['established_explicit_cause']['explicit_cause']=copy.deepcopy(q['callback_error']);no('coordinated cause substitution',q)
  q=copy.deepcopy(fx);q['failure_result']['original_exception']['reference']='foreign';q['projection']['failure_provenance']=copy.deepcopy(q['failure_result']);q['projection']['stored_error_binding']['error']=copy.deepcopy(q['failure_result']['original_exception']);q['output']['original_error']=copy.deepcopy(q['failure_result']['original_exception']);q['output']['established_explicit_cause']['raised_error']=copy.deepcopy(q['failure_result']['original_exception']);no('coordinated original substitution',q)
  other=normal(m,basis,idx,invocation='constructed-callback-B');q=copy.deepcopy(fx)
  for k in ('failure_input','failure_result','callback_error','projection','output'):q[k]=copy.deepcopy(other[k])
  no('coordinated cross invocation',q);rec.check('equal original messages distinct occurrence roles '+tag,lambda:fx['output']['original_error']['message']==other['output']['original_error']['message'] and fx['output']['callback_error']['reference']!=other['output']['callback_error']['reference'])
  no('unknown continuity cannot establish selected owner removal',change(un,('output','selected_owner_removed_in_model'),True))
  for label,path,T in [('callback string',('callback_error','reference'),S),('cause dict',('output','established_explicit_cause'),D),('nested list',('projection','outcomes'),L),('output bool as int',('output','removal_completed_in_model'),int),('failure string',('failure_result','original_exception','reference'),S),('input dict',('failure_input',),D)]:
   q=copy.deepcopy(fx);p=q
   for k in path[:-1]:p=p[k]
   p[path[-1]]=T(p[path[-1]]);no('exact type '+label,q)
  q=copy.deepcopy(fx);q['callback_error']={S(k):v for k,v in q['callback_error'].items()};no('input key subclass',q)
  q=copy.deepcopy(fx);q['output']['established_explicit_cause']={S(k):v for k,v in q['output']['established_explicit_cause'].items()};no('output key subclass',q)
  for path,value in [(('conditional_links',),[]),(('classification',),'KNOWN'),(('declaration','source','cause_expression'),'owner.failure'),(('declaration','guard_branches','callback'),'normal'),(('guard_slot_premise',),'unconditional'),(('context',),rows[1-idx]['context'])]:
   claims=copy.deepcopy(rows);p=claims[idx]
   for k in path[:-1]:p=p[k]
   p[path[-1]]=value;rec.reject('semantic '+str(path)+' '+tag,lambda claims=claims:m._check_rows(basis,claims))
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['sources']['entry']['bytes']=I(claims[idx]['declaration']['source']['sources']['entry']['bytes']);rec.reject('semantic nested exact type '+tag,lambda:m._check_rows(basis,claims))
  got=m._construct_checked(basis,fx);got['projection']['callback_error'].clear();got['projection']['established_explicit_cause']['raised_error'].clear();got['anchor'].clear();ok('nested return mutation isolation',fx)
  v=m._premises(basis,fx);got=c.callback_failure_projection(cat,fx['projection'],v);rec.check('direct pristine '+tag,lambda:c.validate_callback_failure_projection(cat,fx['projection'],v,got));got['established_explicit_cause']['explicit_cause'].clear();rec.reject('direct changed cause',lambda:c.validate_callback_failure_projection(cat,fx['projection'],v,got));rec.check('direct expectations isolated '+tag,lambda:c.validate_callback_failure_projection(cat,fx['projection'],v,c.callback_failure_projection(cat,fx['projection'],v)))
  # One adjacent normal-callback case checks preservation; no old suite is run.
  oldfactory=m.module(basis['fresh']['prior_root']/'tests/cases.py','_prior_normal_factory');oldfx=oldfactory.normal(basis['stored_module'],basis['stored_basis'],idx);rec.check('adjacent reviewed normal callback remains accepted '+tag,lambda:basis['stored_module']._construct_checked(basis['stored_basis'],oldfx)['projection']==oldfx['output'])
 for label,edit in [('declaration omission',lambda x:x['declarations'].pop()),('guard omission',lambda x:x['guard_branches'].pop('rethrow')),('order substitution',lambda x:x['source']['order'].reverse()),('wrong cause',lambda x:x['source'].update(cause_expression='owner.failure')),('cause absent',lambda x:x['source'].update(explicit_cause_clause_present=False))]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('independent catalogue '+label,lambda bad=bad:c.validate_callback_failure(*m.sources(data)[:2],*m.dependencies(data),bad))
 for original,replacement in [(b'raise owner.failure from client_error',b'raise client_error from owner.failure'),(b'except BaseException as client_error:',b'except Exception as client_error:'),(b'raise owner.failure from client_error',b'raise owner.failure from None')]:
  src=m.sources(data)[1];assert src.count(original)==1;src=src.replace(original,replacement);rec.reject('source-defined branch substitution '+replacement.decode(),lambda src=src:c.compile_callback_failure(m.sources(data)[0],src,*m.dependencies(data)),reason='CLIENT-DEFINING-SHAPE:_run')
 e=dict(basis['evidence']);e.pop('evidence/execution-trace.json');rec.reject('missing predecessor evidence',lambda:m._compare_evidence(basis,e));e=dict(basis['evidence']);e['evidence/smoke.stdout']+=b'changed';rec.reject('mixed predecessor evidence',lambda:m._compare_evidence(basis,e))
 before=m.enc(m._assemble(data,rows,basis));bundle['contexts'][0]['callback_stored_failure_correspondence']['declaration'].clear();bundle['contexts'].clear();rec.check('bundle expectations isolated',lambda:m.enc(m._assemble(data,rows,basis))==before)
 claims=copy.deepcopy(rows);claims.pop();rec.reject('both contexts mandatory',lambda:m._check_rows(basis,claims))
 rec.check('unknowns obligations and unjoined observer unchanged',lambda:json.loads(before)['new_callback_failure_limits']['inventory_unknown_totals']==4 and json.loads(before)['new_callback_failure_limits']['lifetime_unknown_totals']==14 and all(r['observer_join'] is None for r in rows))
 rec.save('fixtures.json',{'cases':fixtures});rec.save('receipt-identity.json',identity(before));rec.save('callback-stored-failure.json',json.loads(before))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New Engineering supplied callback-exception controls only; historical review/supplied counts separate')
