"""New source and producer controls only; not a predecessor-validation claim."""
from pathlib import Path
import sys,ast,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]);rec=Record(sys.argv[2]);error=None
class S(str):pass
try:
 rec.save('input-verification.json',verify_root(root));guard(root,rec.path);m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);c=data['coverage'];parent=data['prior']['contexts'][0]['client_construction_none_correspondence']['declaration']
 src=cat['source'];lt=ast.parse(data['sources'][0]);et=ast.parse(data['sources'][1]);session=next(n for n in lt.body if isinstance(n,ast.FunctionDef) and n.name=='session');private=next(n for n in lt.body if isinstance(n,ast.FunctionDef) and n.name=='_session');run=next(n for n in et.body if isinstance(n,ast.FunctionDef) and n.name=='_run')
 handler=next(n for n in ast.walk(private) if isinstance(n,ast.ExceptHandler) and n.name=='e');assign=handler.body[0];names=[k.value for k in assign.value.keys]
 rec.check('source fields independently selected from actual dictionary',lambda:[x['name'] for x in src['fields']]==names)
 rec.check('field expression order independently selected',lambda:[x['expression'] for x in src['fields']]==[ast.unparse(v) for v in assign.value.values])
 for field,node in zip(src['fields'],assign.value.values):rec.check('source expression coordinate '+field['name'],lambda field=field,node=node:field['value_source']['site']==f'{node.lineno}:{node.col_offset}:{node.end_lineno}:{node.end_col_offset}:{type(node).__name__}')
 expected=['run-with-exception-exit','session-yield-delivery','session-inner-with-exception-exit','private-yield-delivery','launcher-handler-entry','details-evaluation-attempt']
 for name in names:expected+=['details-key-'+name,'details-value-'+name]
 expected+=['details-dict-completion','details-assignment-attempt','details-assignment-complete']
 rec.check('complete independent source-stage order',lambda:src['order']==expected)
 rec.check('actual two generator decorators',lambda:all(ast.unparse(n.decorator_list[0])=='contextlib.contextmanager' for n in (session,private)))
 rec.check('actual public bridge call/yield',lambda:ast.unparse(session.body[-1].items[0].context_expr)=='_session(*args, **kwargs)' and ast.unparse(session.body[-1].body[0])=='yield managed')
 rec.check('stops before source cleanup loop',lambda:src['stop_before']['site'].startswith(str(handler.body[1].lineno)+':') and isinstance(handler.body[1],ast.For))
 before=ast.parse((root/'retained/client-construction/code/managed_coverage.py').read_bytes());after=ast.parse((root/'code/managed_coverage.py').read_bytes())
 rec.check('all inherited AST nodes preserved; six additive definitions',lambda:len(after.body)==len(before.body)+6 and all(ast.dump(a,include_attributes=True)==ast.dump(b,include_attributes=True) for a,b in zip(before.body,after.body)))
 for name in ('lab_bootstrap.py','prospective_entry.py'):rec.check('runtime source unchanged '+name,lambda name=name:(root/'source-evidence'/name).read_bytes()==(root/'retained/client-construction/source-evidence'/name).read_bytes())
 for path,value in [(('source','fields'),src['fields'][::-1]),(('source','catch_binding'),'wrong'),(('source','order'),src['order'][:-1]),(('guard_branches','parent'),'pop alone'),(('source','fields',0,'expression'),'str(e)'),(('source','stages','private-yield-delivery','source','sha256'),'0'*64),(('source','fields',0,'name'),S('error'))]:
  bad=change(cat,path,value);rec.reject('source-derived catalogue mismatch '+str(path),lambda bad=bad:c.validate_launcher_details(*data['sources'],parent,bad))
 for n in range(len(cat['declarations'])):
  bad=copy.deepcopy(cat);del bad['declarations'][n];del bad['source']['order'][n];rec.reject('coordinated omitted declaration/order '+str(n),lambda bad=bad:c.validate_launcher_details(*data['sources'],parent,bad))
 for old,new in [(b"traceback.format_exc()",b"traceback.format_exception(e)"),(b"'new_authorization':False",b"'new_authorization':True"),(b"with _session(*args,**kwargs)",b"with other_session(*args,**kwargs)")]:
  altered=data['sources'][0].replace(old,new);assert altered!=data['sources'][0]
  adjusted=copy.deepcopy(parent);adjusted['source']['sources']['launcher']=identity(altered)
  rec.reject('defining source changed '+old.decode(),lambda altered=altered,adjusted=adjusted:c.compile_launcher_details(altered,data['sources'][1],adjusted))
 # Pure producer examples use exact retained constructed fixtures, not new runtime facts.
 fixtures=json.loads((root/'retained/client-construction/results/primary/fixtures.json').read_bytes())
 for i,fx in enumerate(fixtures):
  v,out=producer_case(c,cat,fx['output'],fx['anchor']);control=fx['output']['earlier_control_present']
  rec.check('conditional producer legitimate retained prefix '+str(i),lambda out=out,control=control:oracle(out,src,control))
  for field in ('error','message','traceback'):
   term=('details-value-'+field,'raise');v,out=producer_case(c,cat,fx['output'],fx['anchor'],term)
   rec.check('conditional formatting failure '+str((i,field)),lambda out=out,term=term,control=control:oracle(out,src,control,term))
  v,out=producer_case(c,cat,fx['output'],fx['anchor'],continuity='UNESTABLISHED')
  rec.check('unknown delivery is not arrival '+str(i),lambda out=out:out['launcher_e_in_model'] is None and out['details_in_model'] is None)
 rec.save('source-catalogue.json',cat);rec.save('independent-source-order.json',expected);rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New source/producer controls; no current predecessor public validation in this group',public_predecessor_calls=0,CLI_execution_claimed=False)
