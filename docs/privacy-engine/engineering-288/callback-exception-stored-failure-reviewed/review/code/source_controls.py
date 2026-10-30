from pathlib import Path
import sys,ast,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER
r=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);err=None
try:
 guard(r,rec.path);c=module(r/'code/managed_coverage.py');receipt=json.loads((r/'results/primary/callback-stored-failure.json').read_bytes());entry=(r/'source-evidence/prospective_entry.py').read_bytes();launcher=(r/'source-evidence/lab_bootstrap.py').read_bytes();tree=ast.parse(entry)
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run');callback=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and len(n.body)==1 and isinstance(n.body[0],ast.Expr) and ast.unparse(n.body[0])=='client(Client(token))');handler=callback.handlers[0];guard_=handler.body[0];raised=guard_.body[0];protected=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and callback in n.body);pop=protected.finalbody[0]
 assert isinstance(handler,ast.ExceptHandler) and ast.unparse(handler.type)=='BaseException' and handler.name=='client_error';assert isinstance(raised,ast.Raise) and ast.unparse(raised.exc)=='owner.failure' and ast.unparse(raised.cause)==handler.name
 def site(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 def swap_pin(v,pin):
  if type(v) is dict:
   if v==ident(entry):return D(pin)
   return {k:swap_pin(x,pin) for k,x in v.items()}
  if type(v) is list:return [swap_pin(x,pin) for x in v]
  return v
 for idx,row in enumerate(receipt['contexts']):
  deps=[row[n]['declaration'] for n in ('stored_failure_revocation_correspondence','token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence')];cat=row['callback_stored_failure_correspondence']['declaration'];s=cat['source']
  rec.yes('source compiler exact context '+str(idx),lambda:c.compile_callback_failure(launcher,entry,*deps)==cat)
  for k,n in [('run',run),('callback_call',callback.body[0]),('handler',handler),('guard',guard_.test),('raise',raised),('bare_raise_outside_slice',handler.body[1])]:
   rec.yes('independent source coordinate '+str(idx)+'/'+k,lambda k=k,n=n:s[k]['site']==site(n) and s[k]['expression']==ast.get_source_segment(entry.decode(),n))
  rec.yes('independent cause direction and catch binding '+str(idx),lambda:s['cause_expression']==handler.name and s['raise_expression']=='owner.failure' and s['explicit_cause_clause_present'] is True and s['catch_family']=='BaseException')
  rec.yes('six stages and source finally pop argument/default '+str(idx),lambda:s['order']==ORDER and s['reused_revocation']['pop']['site']==site(pop) and ast.unparse(pop)=='_OWNERS.pop(token, None)' and s['reused_revocation']['pop_return_consumed'] is False)
  rec.yes('callback exception guard distinct from normal-callback guard '+str(idx),lambda:s['guard']['site']!=deps[0]['source']['guard']['site'] and ast.unparse(guard_.test)==deps[0]['source']['guard_expression'])
  parents={child:(p,f) for p in ast.walk(tree) for f,v in ast.iter_fields(p) for child in (v if isinstance(v,list) else [v]) if isinstance(child,ast.AST)}
  for key,start in [('handler',handler),('guard',guard_.test),('raise',raised)]:
   ancestors=[];n=start
   while n in parents:
    p,f=parents[n]
    if isinstance(p,ast.FunctionDef):break
    if isinstance(p,ast.If):ancestors.append(('if',ast.get_source_segment(entry.decode(),p.test),f))
    elif isinstance(p,ast.Try):ancestors.append(('try',f,tuple(ast.unparse(h.type) for h in p.handlers)))
    elif isinstance(p,ast.ExceptHandler):ancestors.append(('handler',ast.unparse(p.type),p.name))
    elif isinstance(p,ast.With):ancestors.append(('with',tuple(ast.unparse(x.context_expr) for x in p.items)))
    n=p
   actual=[]
   for g in s[key]['guards']:
    k=g['kind']
    if k=='if':actual.append((k,g['test']['expression'],g['arm']))
    elif k=='try':actual.append((k,g['region'],tuple(g['handlers'])))
    elif k=='handler':actual.append((k,g['type'],g['binding']))
    elif k=='with':actual.append((k,tuple(g['contexts'])))
    else:raise AssertionError(k)
   rec.yes('independent guard ancestry '+str(idx)+'/'+key,lambda:actual==list(reversed(ancestors)))
  variants=[('reverse errors',b'raise owner.failure from client_error',b'raise client_error from owner.failure'),('remove cause',b'raise owner.failure from client_error',b'raise owner.failure'),('suppress with None',b'raise owner.failure from client_error',b'raise owner.failure from None'),('wrong catch family',b'except BaseException as client_error:',b'except Exception as client_error:'),('wrong handler guard',b'if owner.failure is not None:\n                        raise owner.failure from client_error',b'if owner.failure is None:\n                        raise owner.failure from client_error'),('wrong pop key',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)')]
  for label,a,b in variants:
   assert entry.count(a)==1;changed=entry.replace(a,b);ds=[swap_pin(d,ident(changed)) for d in deps];rec.no('coordinated source and pins '+str(idx)+'/'+label,lambda changed=changed,ds=ds:c.compile_callback_failure(launcher,changed,*ds),'CLIENT-DEFINING-SHAPE')
  for label,path,value in [('wrong guard origin',('source','guard'),deps[0]['source']['guard']),('cause replacement',('source','cause_expression'),'owner.failure'),('handler omission',('declarations',),cat['declarations'][1:]),('false context suppression',('source','explicit_cause_clause_present'),False)]:
   q=change(cat,path,value);rec.no('source-required catalogue '+str(idx)+'/'+label,lambda q=q:c.validate_callback_failure(launcher,entry,*deps,q))
 rec.save('source-oracle.json',{'source':ident(entry),'source_lines':{'callback':callback.body[0].lineno,'handler':handler.lineno,'guard':guard_.lineno,'raise':raised.lineno,'pop':pop.lineno},'raise_expression':ast.unparse(raised),'pop':ast.unparse(pop),'order':ORDER,'physical_identity_inference':False})
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,scope='Independent source traversal and in-memory source/pin/catalogue mutations; no application execution')
