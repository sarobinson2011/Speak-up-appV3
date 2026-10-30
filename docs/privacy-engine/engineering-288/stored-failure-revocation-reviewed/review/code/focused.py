from pathlib import Path
import sys,ast,json,copy,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);mode=sys.argv[3] if len(sys.argv)>3 else 'primary';error=None
class S(str):pass
class I(int):pass
class L(list):pass
class M(dict):pass
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data)
 print('Validating predecessor dependencies for new mandatory relation',flush=True)
 rows,b=m._checked(data,cat);c=b['fresh']['coverage'];saved=(root/'results/correction/stored-failure-revocation.json').read_bytes();assembled=m._assemble(data,rows,b)
 rec.yes('current mandatory two-context derivation equals exact saved receipt',lambda:m.enc(assembled)==saved and [r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.save('derived-receipt-identity.json',ident(m.enc(assembled)))
 source=m.sources(data)[1];t=ast.parse(source);run=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_run');dispatch=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_dispatch')
 guards=[n for n in ast.walk(run) if isinstance(n,ast.If) and ast.unparse(n.test)=='owner.failure is not None'];g=next(n for n in guards if isinstance(n.body[0],ast.Raise) and n.body[0].cause is None)
 tr=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and g in n.body);callback=next(n for n in ast.walk(run) if isinstance(n,ast.Expr) and ast.unparse(n)=='client(Client(token))');pop=tr.finalbody[0];storage=next(n for n in ast.walk(dispatch) if isinstance(n,ast.Assign) and ast.unparse(n)=='owner.failure = error')
 def location(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 locs={'run':run,'callback':callback,'guard':g.test,'raise':g.body[0],'finally':tr,'pop':pop,'storage':storage}
 rec.yes('independent AST guards sequence and discarded pop return',lambda:tr.body[-1] is g and ast.unparse(pop)=='_OWNERS.pop(token, None)' and not tr.handlers and len(tr.finalbody)==1 and g.body[0].cause is None and isinstance(pop,ast.Expr) and len(pop.value.args)==2 and not pop.value.keywords)
 rec.yes('source selected callback normal branch and handler distinct cause',lambda:callback.lineno<g.lineno and any(n.body[0].cause is not None for n in guards if n is not g))
 for k,n in locs.items():rec.yes('source AST location '+k,lambda k=k,n=n:cat['source'][k]['site']==location(n) and cat['source'][k]['expression']==ast.get_source_segment(source.decode(),n))
 rec.yes('source four-stage order and exact pop semantics',lambda:cat['source']['order']==ORDER and cat['source']['pop_key']=='token' and cat['source']['pop_default'] is None and cat['source']['pop_return_consumed'] is False)
 rec.save('source-oracle.json',{'source':ident(source),'locations':{k:location(n) for k,n in locs.items()},'order':ORDER,'guard':ast.unparse(g.test),'raise':ast.unparse(g.body[0]),'pop':ast.unparse(pop)})
 fixtures=[]
 for idx in range(2):
  for route in ('handle','state'):
   label=str(idx)+'/'+route
   fx=make(m,b,idx,route);fixtures.append(fx)
   rec.yes('legitimate fixed failure '+label,lambda fx=fx:m._construct_checked(b,fx)['projection']==fx['output'] and independent_flags(fx))
   helper=make(m,b,idx,route,helper='raise');rec.yes('stored original survives caught helper escape '+label,lambda x=helper:m._construct_checked(b,x)['projection']==x['output'] and independent_flags(x))
   unknown=make(m,b,idx,route,control=False,continuity=False);rec.yes('no control and unknown registry continuity '+label,lambda x=unknown:m._construct_checked(b,x)['projection']==x['output'] and independent_flags(x))
   other=make(m,b,idx,route,invocation='FL6-distinct-'+label);rec.yes('equal error values remain distinct occurrences '+label,lambda x=other,y=fx:x['output']['original_error']['reference']!=y['output']['original_error']['reference'] and x['output']['reference_bindings']!=y['output']['reference_bindings'])
   stages=ORDER if mode=='primary' else ['removal-attempt','removal-complete']
   for s in stages:
    kinds=['raise','process-termination','unobserved'] if mode=='primary' else ['raise']
    for kind in kinds:
     q=make(m,b,idx,route,terminal=(s,kind));rec.yes('frontier '+label+'/'+s+'/'+kind,lambda q=q:m._construct_checked(b,q)['projection']==q['output'] and independent_flags(q))
     wrong=change(q,('output','original_outward_after_finally_established_in_model'),True)
     if q['output']['original_outward_after_finally_established_in_model'] is False:rec.no('false original propagation '+label+'/'+s+'/'+kind,lambda q=wrong:m._construct_checked(b,q),'STORED-OUTPUT')
   for path,value in [(('failure_result','original_exception','reference'),'another-error'),(('failure_input','references','owner','symbol'),'another-owner'),(('failure_input','references','token','symbol'),'another-token'),(('token_case','invocation'),'another-invocation'),(('anchor','instance','binding'),'stale-binding'),(('output','removal_completed_in_model'),False), (('output','run_success_established'),True)]:
    q=change(fx,path,value);rec.no('binding/false completion '+label+str(path),lambda q=q:m._construct_checked(b,q))
   if mode=='primary':
    for field in ('outcomes','projection','failure_result','token_case'):
     q=D(fx);del q[field];rec.no('missing field '+label+'/'+field,lambda q=q:m._construct_checked(b,q))
    for action in ('omit','duplicate','reverse'):
     q=D(fx)
     if action=='omit':q['outcomes'].pop(1)
     elif action=='duplicate':q['outcomes'].insert(2,D(q['outcomes'][1]))
     else:q['outcomes'].reverse()
     q['projection']['outcomes']=D(q['outcomes']);rec.no('coordinated step '+label+'/'+action,lambda q=q:m._construct_checked(b,q))
    for p,val in [(('output','source_original_rethrow_completed_in_model'),1),(('failure_result','retained_original'),1),(('projection','outcomes',0,'stage'),S('stored-error-rethrow')),(('token_case','registry_continuity'),1),(('failure_result','original_exception','reference'),S(fx['failure_result']['original_exception']['reference']))]:
     q=change(fx,p,val);rec.no('exact types '+label+str(p),lambda q=q:m._construct_checked(b,q))
    for p,typ in [(('output','events'),L),(('projection','references'),M)]:
     q=D(fx);v=q
     for k in p[:-1]:v=v[k]
     v[p[-1]]=typ(v[p[-1]]);rec.no('container subclasses '+label+str(p),lambda q=q:m._construct_checked(b,q))
    q=D(fx);v=q['output'];v[S('original_error')]=v.pop('original_error');rec.no('literal-key subclass '+label,lambda q=q:m._construct_checked(b,q))
    old=fx['failure_result']['original_exception']['reference'];q=replace(fx,old,'coordinated-foreign-error');rec.no('coordinated error substitution '+label,lambda q=q:m._construct_checked(b,q),'STORED-FAILURE-RESULT')
    q=replace(fx,fx['anchor']['instance']['binding'],'0'*64);rec.no('coordinated instance substitution '+label,lambda q=q:m._construct_checked(b,q),'STORED-CONSTRUCTED-ANCHOR')
    q=change(fx,('failure_input','outcomes','fixed-failure'),'process-termination');rec.no('helper termination cannot return callback '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('failure_input','outcomes','retain-error'),'raise');rec.no('unestablished storage cannot become stored failure '+label,lambda q=q:m._construct_checked(b,q))
    q=change(fx,('failure_input','callback'),'raises');rec.no('callback exception is outside normal-callback slice '+label,lambda q=q:m._construct_checked(b,q),'STORED-FAILURE-INVOCATION-CALLBACK')
    q=change(fx,('failure_input','cleanup','revoke'),'normal');rec.no('opaque cleanup substitution '+label,lambda q=q:m._construct_checked(b,q),'STORED-NO-OPAQUE-CLEANUP-JOIN')
    q=change(fx,('outcomes',0,'outcome'),'normal');q['projection']['outcomes']=D(q['outcomes']);rec.no('rethrow cannot be normal run completion '+label,lambda q=q:m._construct_checked(b,q),'STORED-STAGE-OUTCOME')
   out=m._construct_checked(b,fx);out['projection']['reference_bindings']['owner'].clear();out['projection']['stored_error_binding']['error'].clear();out['projection']['events'].reverse()
   rec.yes('nested constructed output isolation '+label,lambda fx=fx:m._construct_checked(b,fx)['projection']==fx['output'])
  cl=D(rows);cl[idx]['classification']='COMPLETE';rec.no('semantic status escalation '+str(idx),lambda cl=cl:m._check_rows(b,cl))
  cl=D(rows);cl[idx]['declaration']['declarations'].pop();rec.no('semantic omitted mandatory stage '+str(idx),lambda cl=cl:m._check_rows(b,cl))
 for mut in ('missing','duplicate','reorder'):
  cl=D(rows)
  if mut=='missing':cl.pop()
  elif mut=='duplicate':cl[1]=D(cl[0])
  else:cl.reverse()
  rec.no('semantic context '+mut,lambda cl=cl:m._check_rows(b,cl))
 cl=D(rows);cl[0]['classification']=S('UNKNOWN');rec.no('semantic exact value boundary',lambda:m._check_rows(b,cl))
 detached=m._assemble(data,rows,b);detached['contexts'].reverse();detached['contexts'][0]['stored_failure_revocation_correspondence']['declaration']['source']['order'].clear();rows[0]['reference_basis'].clear()
 rec.yes('returned receipt and rows cannot alter expectations',lambda:m.enc(m._assemble(data,m._rows(b),b))==saved)
 if mode=='primary':
  deps=m.dependencies(data);src=m.sources(data)
  for fld,val in [('order',list(reversed(ORDER))),('pop_key','foreign'),('pop_default',0)]:
   bad=change(cat,('source',fld),val);rec.no('source-derived catalogue '+fld,lambda bad=bad:c.validate_stored_failure(*src[:2],*deps,bad))
  old=module(root/'failures/helper-escape-gap/managed_coverage.py','old_stored')
  for idx in range(2):
   for route in ('handle','state'):
    fx=make(m,b,idx,route,helper='raise');rec.no('reproduced old helper escape omission '+str(idx)+route,lambda fx=fx:old.stored_failure_projection(cat,fx['projection'],D(fx['projection'])),'STORED-VALIDATED-STORAGE')
  rec.save('constructed-fixtures.json',fixtures)
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode)
