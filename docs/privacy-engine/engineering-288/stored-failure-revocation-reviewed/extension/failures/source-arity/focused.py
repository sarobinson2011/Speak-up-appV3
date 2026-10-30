"""New focused supplied controls only; no prior suite or application method."""
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
 if '--write' not in sys.argv:rec.save('input-verification.json',verify_root(root))
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];bundle=m._assemble(data,rows,basis)
 rec.check('mandatory prior chain and both contexts',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and any(x['function']=='derive_status' for x in CALLS))
 rec.check('prior receipt and all prior context fields preserved',lambda:all(all(bundle['contexts'][i][k]==v for k,v in ctx.items()) for i,ctx in enumerate(basis['prior']['contexts'])))
 tree=ast.parse(m.sources(data)[1]);run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');tr=run.body[2].body[0].body[-1];callback=tr.body[1];guard_=tr.body[2];raise_=guard_.body[0];pop=tr.finalbody[0]
 order=['stored-error-rethrow','finally-enter','removal-attempt','removal-complete']
 rec.check('independent source guard and cause semantics',lambda:ast.unparse(guard_.test)=='owner.failure is not None' and ast.unparse(raise_)=='raise owner.failure' and raise_.cause is None and ast.unparse(callback.body[0])=='client(Client(token))')
 rec.check('independent finally pop AST and exact coverage',lambda:ast.unparse(pop)=='_OWNERS.pop(token, None)' and not tr.handlers and len(tr.finalbody)==1 and cat['source']['order']==order and [d['id'] for d in cat['declarations']]==order)
 rec.save('source-oracle.json',{'guard':ast.dump(guard_,include_attributes=False),'finally':ast.dump(pop,include_attributes=False),'order':order,'source':identity(m.sources(data)[1])})
 fixtures=[]
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx);st=normal(m,basis,idx,route='state');fixtures.extend([fx,st])
  def ok(label,q):return rec.check(label+' '+tag,lambda:m._construct_checked(basis,q)['projection']==q['output'])
  def no(label,q):return rec.reject(label+' '+tag,lambda:m._construct_checked(basis,q))
  ok('source TypeError provenance handle',fx);ok('conditional session-call failure provenance state',st);ok('conditional session-call failure handle',normal(m,basis,idx,origin='session-call'));ok('without optional control',normal(m,basis,idx,control=False))
  un=normal(m,basis,idx,continuity=False);ok('unknown registry continuity admitted',un)
  rec.check('unknown continuity cannot establish selected owner removal '+tag,lambda:un['output']['selected_owner_removed_in_model'] is None and un['output']['removal_completed_in_model'])
  rec.check('normal pop preserves pending original without run success '+tag,lambda:fx['output']['outward_error_after_finally_in_model']==fx['failure_result']['original_exception'] and not fx['output']['run_success_established'] and not fx['output']['original_reaches_launcher_established'])
  for stage in order:
   for out in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,out));ok(stage+' '+out,q)
    rec.check('prior storage survives '+stage+out+' '+tag,lambda q=q:q['output']['failure_storage_previously_completed_in_model'] is True and q['output']['original_error']==q['failure_result']['original_exception'] and not q['output']['run_success_established'])
    if stage=='stored-error-rethrow' and out=='raise':
     rec.check('evaluation exception normal pop is not original propagation '+tag,lambda q=q:q['output']['removal_completed_in_model'] and not q['output']['source_original_rethrow_completed_in_model'] and not q['output']['original_outward_after_finally_established_in_model'])
    else:
     rec.check('frontier supplies no removal completion '+stage+out+' '+tag,lambda q=q:not q['output']['removal_completed_in_model'] and q['output']['outward_error_after_finally_in_model'] is None)
    if out in ('process-termination','unobserved'):rec.check('no terminal Python exception inference '+stage+out+' '+tag,lambda q=q:q['output']['terminal_python_exception_in_model'] is None)
    for field in ('run_success_established','original_reaches_launcher_established','database_cleanup_completion','authorization_renewed'):
     no('false '+field+' '+stage+out,change(q,('output',field),True))
    if not q['output']['removal_completed_in_model']:no('false completed removal '+stage+out,change(q,('output','removal_completed_in_model'),True))
    if stage!='stored-error-rethrow' and out=='raise':
     no('cleanup failure cannot guarantee original propagation '+stage,change(q,('output','original_outward_after_finally_established_in_model'),True))
    if out in ('process-termination','unobserved') or stage!='stored-error-rethrow':
     bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'removal-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('false continuation '+stage+out,bad)
  for stage in order:
   bad=copy.deepcopy(fx);bad['outcomes']=[x for x in bad['outcomes'] if x['stage']!=stage];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('missing '+stage,bad)
   bad=copy.deepcopy(fx);bad['outcomes'].insert(0,copy.deepcopy(next(x for x in bad['outcomes'] if x['stage']==stage)));bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('duplicate '+stage,bad)
  bad=copy.deepcopy(fx);bad['outcomes'].reverse();bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('reordered steps',bad)
  bad=copy.deepcopy(fx);bad['outcomes'][0]['outcome']='normal';bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);no('source raise cannot become normal return',bad)
  for path,value in [(('failure_result','original_exception','reference'),'foreign/error'),(('projection','stored_error_binding','error','reference'),'foreign/error'),(('projection','stored_error_binding','owner','symbol'),'foreign'),(('projection','references','token','symbol'),'foreign'),(('failure_input','references','owner','symbol'),'foreign'),(('failure_input','references','token','symbol'),'foreign'),(('failure_input','occurrence'),'foreign'),(('token_case','invocation'),'foreign'),(('projection','scope','acquisition'),'stale'),(('projection','scope','instance','binding'),'0'*64), (('anchor','instance','binding'),'0'*64), (('failure_input','callback'),'raises'),(('failure_input','cleanup','revoke'),'normal'),(('projection','stored_error_binding','guard_slot_premise'),'unconditional runtime continuity')]:no('binding '+str(path),change(fx,path,value))
  for routecase in (fx,st):
   bad=copy.deepcopy(routecase);bad['failure_input']['outcomes']['retain-error']='process-termination';no('no invented stored failure after termination '+bad['failure_route'],bad)
   bad=copy.deepcopy(routecase);bad['failure_input']['references']['owner']['symbol']='foreign';bad['failure_result']['reference_bindings' if bad['failure_route']=='handle' else 'references']=copy.deepcopy(bad['failure_input']['references']);bad['projection']['failure_provenance']=copy.deepcopy(bad['failure_result']);no('coordinated owner substitution '+bad['failure_route'],bad)
  bad=copy.deepcopy(fx);bad['failure_result']['original_exception']['reference']='foreign';bad['projection']['failure_provenance']=copy.deepcopy(bad['failure_result']);bad['projection']['stored_error_binding']['error']=copy.deepcopy(bad['failure_result']['original_exception']);bad['output']['original_error']=copy.deepcopy(bad['failure_result']['original_exception']);no('coordinated original error reports',bad)
  other=normal(m,basis,idx,invocation='constructed-stored-B');bad=copy.deepcopy(fx);bad['failure_input']=copy.deepcopy(other['failure_input']);bad['failure_result']=copy.deepcopy(other['failure_result']);bad['projection']=copy.deepcopy(other['projection']);bad['output']=copy.deepcopy(other['output']);no('coordinated cross invocation',bad)
  rec.check('equal error contents distinct occurrences '+tag,lambda:fx['failure_result']['original_exception']['message']==other['failure_result']['original_exception']['message'] and fx['output']['original_error']['reference']!=other['output']['original_error']['reference'])
  no('unknown continuity does not repair selected owner removal',change(un,('output','selected_owner_removed_in_model'),True))
  for label,path,T in [('input str',('failure_input','occurrence'),S),('input container',('failure_input',),D),('nested list',('projection','outcomes'),L),('output bool as int',('output','removal_completed_in_model'),int),('output string',('output','completion'),S),('output nested dict',('output','original_error'),D),('failure type',('failure_result','original_exception','reference'),S)]:
   q=copy.deepcopy(fx);p=q
   for k in path[:-1]:p=p[k]
   p[path[-1]]=T(p[path[-1]]);no('exact type '+label,q)
  q=copy.deepcopy(fx);q['failure_input']={S(k):v for k,v in q['failure_input'].items()};no('literal key subclass pre-normalization',q)
  q=copy.deepcopy(fx);q['output']['original_error']={S(k):v for k,v in q['output']['original_error'].items()};no('nested output key subclass',q)
  for path,value in [(('conditional_links',),[]),(('classification',),'KNOWN'),(('original_exception_observation',),{}),(('guard_slot_premise',),'established'),(('scope','invocation'),'invented'),(('context',),rows[1-idx]['context'])]:
   claims=copy.deepcopy(rows);p=claims[idx]
   for k in path[:-1]:p=p[k]
   p[path[-1]]=value;rec.reject('semantic '+str(path)+' '+tag,lambda claims=claims:m._check_rows(basis,claims))
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['sources']['entry']['bytes']=I(claims[idx]['declaration']['source']['sources']['entry']['bytes']);rec.reject('semantic type before JSON '+tag,lambda:m._check_rows(basis,claims))
  got=m._construct_checked(basis,fx);got['projection']['original_error'].clear();got['projection']['validated_token_prefix'].clear();got['anchor'].clear();ok('nested mutable output isolation',fx)
  v=m._premises(basis,fx);got=c.stored_failure_projection(cat,fx['projection'],v);rec.check('direct validator pristine '+tag,lambda:c.validate_stored_failure_projection(cat,fx['projection'],v,got));got['events'].clear();rec.reject('direct validator missing events '+tag,lambda:c.validate_stored_failure_projection(cat,fx['projection'],v,got))
  got=c.stored_failure_projection(cat,fx['projection'],v);got['stored_error_binding']['error'].clear();rec.check('direct returned alias isolation '+tag,lambda:c.validate_stored_failure_projection(cat,fx['projection'],v,c.stored_failure_projection(cat,fx['projection'],v)))
 for label,edit in [('declaration omission',lambda x:x['declarations'].pop()),('guard omission',lambda x:x['guard_branches'].pop('rethrow')),('order substitution',lambda x:x['source']['order'].reverse()),('wrong pop key',lambda x:x['source'].update(pop_key='foreign')),('wrong guard',lambda x:x['source'].update(guard_expression='True')),('stale source',lambda x:x['source']['sources']['entry'].update(sha256='0'*64))]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('independent source validator '+label,lambda bad=bad:c.validate_stored_failure(*m.sources(data),*m.dependencies(data),bad))
 e=dict(basis['evidence']);e.pop('evidence/execution-trace.json');rec.reject('missing evidence binding',lambda:m._compare_evidence(basis,e));e=dict(basis['evidence']);e['evidence/smoke.stdout']+=b'altered';rec.reject('mixed evidence bytes',lambda:m._compare_evidence(basis,e))
 before=m.enc(m._assemble(data,rows,basis));bundle['contexts'][0]['stored_failure_revocation_correspondence']['declaration'].clear();bundle['contexts'].clear();rec.check('bundle mutation isolation',lambda:m.enc(m._assemble(data,rows,basis))==before)
 rec.check('unknowns observers and obligations unchanged',lambda:all(r['observer_join'] is None and r['runtime_stored_failure_chain'] is None for r in rows) and json.loads(before)['new_stored_failure_limits']['inventory_unknown_totals']==4 and json.loads(before)['new_stored_failure_limits']['lifetime_unknown_totals']==14)
 rec.save('fixtures.json',{'cases':fixtures});rec.save('receipt-identity.json',identity(before));rec.save('stored-failure-revocation.json',json.loads(before))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New Engineering supplied stored-failure controls only; historical independent/supplied counts separate')
