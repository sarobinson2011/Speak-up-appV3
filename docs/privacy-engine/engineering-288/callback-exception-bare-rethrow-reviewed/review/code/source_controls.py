from pathlib import Path
import sys,ast,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);err=None
try:
 guard(root,rec.path);c=module(root/'code/managed_coverage.py');receipt=json.loads((root/'results/primary/callback-bare-rethrow.json').read_bytes());entry=(root/'source-evidence/prospective_entry.py').read_bytes();launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();tree=ast.parse(entry)
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 callback=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and len(n.body)==1 and isinstance(n.body[0],ast.Expr) and ast.unparse(n.body[0])=='client(Client(token))')
 handler=callback.handlers[0];conditional=handler.body[0];bare=handler.body[1];protected=next(n for n in ast.walk(run) if isinstance(n,ast.Try) and callback in n.body);pop=protected.finalbody[0]
 assert len(handler.body)==2 and isinstance(conditional,ast.If) and not conditional.orelse and isinstance(bare,ast.Raise) and bare.exc is None and bare.cause is None
 assert ast.unparse(conditional.test)=='owner.failure is not None' and isinstance(conditional.test.ops[0],ast.IsNot) and conditional.test.comparators[0].value is None
 assert ast.unparse(conditional.body[0])=='raise owner.failure from client_error'
 assert ast.unparse(handler.type)=='BaseException' and handler.name=='client_error'
 def site(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 def swap(v,pin):
  if type(v) is dict:return D(pin) if v==ident(entry) else {k:swap(x,pin) for k,x in v.items()}
  if type(v) is list:return [swap(x,pin) for x in v]
  return v
 parents={child:(p,f) for p in ast.walk(tree) for f,v in ast.iter_fields(p) for child in (v if isinstance(v,list) else [v]) if isinstance(child,ast.AST)}
 for idx,row in enumerate(receipt['contexts']):
  deps=[row[n]['declaration'] for n in ('callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence')];cat=row['callback_bare_rethrow_correspondence']['declaration'];s=cat['source']
  rec.yes('compiler matches current declaration '+str(idx),lambda:c.compile_callback_bare(launcher,entry,*deps)==cat)
  for key,n in [('run',run),('callback_call',callback.body[0]),('handler',handler),('guard',conditional.test),('raise',bare)]:rec.yes('independently selected source coordinate '+str((idx,key)),lambda key=key,n=n:s[key]['site']==site(n) and s[key]['expression']==ast.get_source_segment(entry.decode(),n))
  rec.yes('exact None false guard independent AST '+str(idx),lambda:s['selected_slot_value'] is None and s['selected_guard_result'] is False and s['selected_slot_exact_type']=='NoneType' and s['guard_expression']==ast.unparse(conditional.test))
  rec.yes('bare syntax has no expression or new cause '+str(idx),lambda:s['raise_syntax']=='raise' and s['raise_expression'] is None and s['cause_expression'] is None and s['bare_raise_has_explicit_cause_clause'] is False)
  rec.yes('normal stored branch and bare branch distinct '+str(idx),lambda:s['raise']['site']!=deps[1]['source']['raise']['site'] and s['guard']['site']!=deps[1]['source']['guard']['site'])
  rec.yes('six ordered points and discarded pop result '+str(idx),lambda:s['order']==ORDER and ast.unparse(pop)=='_OWNERS.pop(token, None)' and s['reused_revocation']['pop']['site']==site(pop) and s['reused_revocation']['pop_return_consumed'] is False)
  for key,start in [('handler',handler),('guard',conditional.test),('raise',bare)]:
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
   rec.yes('independent ancestor guards '+str((idx,key)),lambda:actual==list(reversed(ancestors)))
  variants=[('new cause',b'                    raise\n',b'                    raise client_error from None\n'),('explicit expression',b'                    raise\n',b'                    raise client_error\n'),('wrong error',b'                    raise\n',b'                    raise owner.failure\n'),('equality guard',b'if owner.failure is not None:\n                        raise owner.failure from client_error',b'if owner.failure != None:\n                        raise owner.failure from client_error'),('truthiness guard',b'if owner.failure is not None:\n                        raise owner.failure from client_error',b'if owner.failure:\n                        raise owner.failure from client_error'),('wrong pop token',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)')]
  for label,a,b in variants:
   assert entry.count(a)==1;changed=entry.replace(a,b);ds=[swap(d,ident(changed)) for d in deps]
   rec.no('coordinated source/pins '+str((idx,label)),lambda changed=changed,ds=ds:c.compile_callback_bare(launcher,changed,*ds),'CLIENT-DEFINING-SHAPE')
  for label,path,value in [('omitted source point',('declarations',),cat['declarations'][1:]),('false guard result',('source','selected_guard_result'),True),('wrong guard origin',('source','guard'),deps[1]['source']['guard']),('new cause declaration',('source','cause_expression'),'client_error'),('wrong None type',('source','selected_slot_exact_type'),'bool')]:
   q=change(cat,path,value);rec.no('source required declaration '+str((idx,label)),lambda q=q:c.validate_callback_bare(launcher,entry,*deps,q))
 rec.save('source-oracle.json',{'source':ident(entry),'lines':{'callback':callback.body[0].lineno,'handler':handler.lineno,'guard':conditional.lineno,'bare_raise':bare.lineno,'finally':pop.lineno-2,'pop':pop.lineno},'selection':'Same handler, false exact-None test, expression-free raise; source-selected ancestry and order','bare_raise_has_new_cause':False,'existing_chain_evidence':'UNKNOWN','runtime_executed':False})
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,scope='Independent AST source selection and in-memory coordinated source/pin changes')
