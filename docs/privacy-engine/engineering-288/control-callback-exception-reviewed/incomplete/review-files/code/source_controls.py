from pathlib import Path
import sys,ast,json
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import PREFIX,ORDER
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);error=None
try:
 guard(root,r.path);c=module(root/'code/managed_coverage.py');receipt=json.loads((root/'results/primary/control-exception.json').read_bytes());entry=(root/'source-evidence/prospective_entry.py').read_bytes();launcher=(root/'source-evidence/lab_bootstrap.py').read_bytes();tree=ast.parse(entry)
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 calls=[n for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='control'];assert len(calls)==1;call=calls[0]
 parents={ch:(p,f) for p in ast.walk(tree) for f,v in ast.iter_fields(p) for ch in (v if isinstance(v,list) else [v]) if isinstance(ch,ast.AST)}
 stmt=parents[call][0];guard_if=parents[stmt][0];protected=parents[guard_if][0];client=next(n for n in protected.body if isinstance(n,ast.Try));pop=protected.finalbody[0]
 assert isinstance(guard_if,ast.If) and not guard_if.orelse and isinstance(protected,ast.Try) and not protected.handlers and not protected.orelse
 assert isinstance(guard_if.test,ast.Compare) and type(guard_if.test.ops[0]) is ast.IsNot and guard_if.test.comparators[0].value is None and ast.unparse(guard_if.test.left)=='control'
 assert ast.unparse(call)=='control(_Control(token))' and protected.body.index(guard_if)<protected.body.index(client) and client.lineno>stmt.end_lineno
 assert isinstance(pop,ast.Expr) and ast.unparse(pop)=='_OWNERS.pop(token, None)' and len(protected.finalbody)==1
 def site(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
 def source_guards(start):
  a=[];n=start
  while n in parents:
   p,f=parents[n]
   if isinstance(p,ast.FunctionDef):break
   if isinstance(p,ast.If):a.append(('if',ast.get_source_segment(entry.decode(),p.test),f))
   elif isinstance(p,ast.Try):a.append(('try',f,tuple(ast.unparse(h.type) for h in p.handlers)))
   elif isinstance(p,ast.ExceptHandler):a.append(('handler',ast.unparse(p.type),p.name))
   elif isinstance(p,ast.With):a.append(('with',tuple(ast.unparse(x.context_expr) for x in p.items)))
   n=p
  return list(reversed(a))
 def catalogue_guards(node):
  out=[]
  for g in node['guards']:
   k=g['kind']
   if k=='if':out.append((k,g['test']['expression'],g['arm']))
   elif k=='try':out.append((k,g['region'],tuple(g['handlers'])))
   elif k=='handler':out.append((k,g['type'],g['binding']))
   elif k=='with':out.append((k,tuple(g['contexts'])))
   else:raise AssertionError(k)
  return out
 def repin(v,pin):
  if type(v) is dict:return D(pin) if v==ident(entry) else {k:repin(x,pin) for k,x in v.items()}
  if type(v) is list:return [repin(x,pin) for x in v]
  return v
 for idx,row in enumerate(receipt['contexts']):
  deps=[row[n]['declaration'] for n in ('callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence')];cat=row['control_exception_revocation_correspondence']['declaration'];s=cat['source']
  r.yes('source compiler matches actual declaration '+str(idx),lambda:c.compile_control_exception(launcher,entry,*deps)==cat)
  for key,n in [('run',run),('control_guard',guard_if.test),('control_constructor',call.args[0]),('control_call',stmt),('client_handler',client.handlers[0])]:
   r.yes('independently located source point '+str((idx,key)),lambda key=key,n=n:s[key]['site']==site(n) and s[key]['expression']==ast.get_source_segment(entry.decode(),n))
   r.yes('independent source ancestry '+str((idx,key)),lambda key=key,n=n:catalogue_guards(s[key])==source_guards(n))
  r.yes('control exact non-None guard '+str(idx),lambda:s['guard_expression']==ast.unparse(guard_if.test) and s['selected_guard_result'] is True)
  r.yes('client handler excluded by actual try ancestry '+str(idx),lambda:s['client_handler_applies'] is False and s['owner_failure_guard_applies'] is False and s['local_exception_binding'] is None and all(g[0]!='handler' for g in source_guards(stmt)))
  r.yes('no explicit cause in selected source slice '+str(idx),lambda:s['new_explicit_cause_assignment'] is False and not any(isinstance(n,ast.Raise) for n in ast.walk(guard_if)))
  r.yes('selected prefix and cleanup order '+str(idx),lambda:s['prefix_order']==PREFIX and s['order']==ORDER)
  r.yes('pop uses selected token exact None and discards result '+str(idx),lambda:s['pop_key']=='token' and s['pop_default'] is None and s['pop_return_consumed'] is False)
  for key,n in [('finally-enter',protected),('removal-attempt',pop.value),('removal-complete',pop)]:r.yes('distinct source semantic cleanup point '+str((idx,key)),lambda key=key,n=n:s['stages'][key]['site']==site(n) and catalogue_guards(s['stages'][key])==source_guards(n))
  variants=[('equality guard',b'if control is not None:',b'if control != None:'),('truthy guard',b'if control is not None:',b'if control:'),('wrong callback',b'control(_Control(token))',b'client(_Control(token))'),('wrong capability',b'control(_Control(token))',b'control(Client(token))'),('wrong token',b'control(_Control(token))',b'control(_Control(owner))'),('wrong pop token',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)'),('wrong pop default',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(token, False)'),('invented stored-error cause',b'control(_Control(token))',b'raise owner.failure from client_error')]
  for label,a,bb in variants:
   assert entry.count(a)==1;changed=entry.replace(a,bb);ds=[repin(d,ident(changed)) for d in deps]
   r.no('coordinated defining source and pin changes '+str((idx,label)),lambda changed=changed,ds=ds:c.compile_control_exception(launcher,changed,*ds))
  for label,path,value in [('missing cleanup declaration',('declarations',),cat['declarations'][:-1]),('wrong control origin',('source','control_call'),s['client_handler']),('client handler imported',('source','client_handler_applies'),True),('owner guard imported',('source','owner_failure_guard_applies'),True),('cause imported',('source','new_explicit_cause_assignment'),True),('guard truth type',('source','selected_guard_result'),1),('reordered cleanup',('source','order'),list(reversed(ORDER))),('missing token prefix',('source','prefix_order'),PREFIX[:-1])]:
   q=change(cat,path,value);r.no('source-derived catalogue obligation '+str((idx,label)),lambda q=q:c.validate_control_exception(launcher,entry,*deps,q))
 r.save('source-oracle.json',{'source':ident(entry),'selected_control_call':site(stmt),'control_guard':site(guard_if.test),'control_constructor':site(call.args[0]),'client_handler':site(client.handlers[0]),'finally_region':site(protected),'pop_attempt':site(pop.value),'pop_completion':site(pop),'control_call_ancestry':source_guards(stmt),'selected_source_lines':[176,177,186,188],'client_handler_contains_control':False,'owner_failure_guard_selected':False,'new_explicit_cause_assignment':False,'runtime_observations':False})
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='Independent AST ancestry, selection and coordinated source/pin changes')
