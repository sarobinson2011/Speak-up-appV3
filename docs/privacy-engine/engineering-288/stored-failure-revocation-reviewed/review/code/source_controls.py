from pathlib import Path
import sys,ast,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
r=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);err=None
try:
 guard(r,rec.path);c=module(r/'code/managed_coverage.py');saved=json.loads((r/'results/correction/stored-failure-revocation.json').read_bytes());launcher=(r/'source-evidence/lab_bootstrap.py').read_bytes();entry=(r/'source-evidence/prospective_entry.py').read_bytes()
 def swap_pin(v,pin):
  if type(v) is dict:
   if v==ident(entry):return D(pin)
   return {k:swap_pin(x,pin) for k,x in v.items()}
  if type(v) is list:return [swap_pin(x,pin) for x in v]
  return v
 for idx,row in enumerate(saved['contexts']):
  ds=[row[n]['declaration'] for n in ('token_registration_correspondence','client_handle_return_correspondence','client_state_return_correspondence')];cat=row['stored_failure_revocation_correspondence']['declaration']
  rec.yes('static compiler source exact context '+str(idx),lambda:c.compile_stored_failure(launcher,entry,*ds)==cat)
  changes=[('stored error replaced',b'raise owner.failure\n            finally:',b'raise RuntimeError("substitute")\n            finally:'),('guard inverted',b'if owner.failure is not None:\n                    raise owner.failure\n',b'if owner.failure is None:\n                    raise owner.failure\n'),('wrong pop key',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(owner, None)'),('wrong pop default',b'_OWNERS.pop(token, None)',b'_OWNERS.pop(token, False)'),('pop result forwarded',b'_OWNERS.pop(token, None)',b'return _OWNERS.pop(token, None)'),('storage substitutes error',b'owner.failure = error',b'owner.failure = None'),('explicit cause inserted',b'raise owner.failure\n            finally:',b'raise owner.failure from None\n            finally:')]
  for label,a,b in changes:
   assert entry.count(a)==1,(label,entry.count(a));altered=entry.replace(a,b);deps=[swap_pin(x,ident(altered)) for x in ds]
   rec.no('source and matching-pin coordinated mutation '+str(idx)+'/'+label,lambda altered=altered,deps=deps:c.compile_stored_failure(launcher,altered,*deps),'CLIENT-DEFINING-SHAPE')
  t=ast.parse(entry);parents={child:(p,f) for p in ast.walk(t) for f,v in ast.iter_fields(p) for child in (v if isinstance(v,list) else [v]) if isinstance(child,ast.AST)}
  lookup={f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}':n for n in ast.walk(t) if hasattr(n,'lineno')}
  for key in ('storage','callback','guard','raise','pop'):
   n=lookup[cat['source'][key]['site']];anc=[]
   while n in parents:
    p,f=parents[n]
    if isinstance(p,ast.FunctionDef):break
    if isinstance(p,ast.If):anc.append(('if',ast.get_source_segment(entry.decode(),p.test),f))
    elif isinstance(p,ast.Try):anc.append(('try',f,tuple(ast.unparse(h.type) for h in p.handlers)))
    elif isinstance(p,ast.ExceptHandler):anc.append(('handler',ast.unparse(p.type),p.name))
    elif isinstance(p,ast.With):anc.append(('with',tuple(ast.unparse(x.context_expr) for x in p.items)))
    n=p
   actual=[]
   for g in cat['source'][key]['guards']:
    k=g['kind']
    if k=='if':actual.append((k,g['test']['expression'],g['arm']))
    elif k=='try':actual.append((k,g['region'],tuple(g['handlers'])))
    elif k=='handler':actual.append((k,g['type'],g['binding']))
    elif k=='with':actual.append((k,tuple(g['contexts'])))
    else:raise AssertionError(k)
   rec.yes('independent guard ancestry '+str(idx)+'/'+key,lambda actual=actual,anc=anc:actual==list(reversed(anc)))
  rec.yes('source finally entry is semantic containing-Try anchor '+str(idx),lambda:cat['source']['stages']['finally-enter']['semantic_region']=='finally-entry' and cat['source']['stages']['finally-enter']['site']==cat['source']['finally']['site'])
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,scope='Pure source compiler; coordinated source mutations are in-memory review copies, implementation files unchanged')
