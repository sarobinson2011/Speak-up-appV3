"""New focused source/constructed preparation controls, not predecessor authentication."""
from pathlib import Path
import sys,traceback,ast,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
class S(str):pass
try:
 r.save('environment.json',environment());r.save('root.json',verify_root(root))
 m=module(root/'code/correspondence.py');d=m.inputs(root);c=d['coverage'];cat=m.catalogue(d);raws=m.sources(d)
 r.yes('source-independent ordered helper/open plan',lambda:[(s['operation'],s['source']['site']) for s in cat['source']['steps']]==F.plan(raws[0]),'independent defining-source AST oracle')
 r.yes('exact positional signature and xb literal',lambda:[p['name'] for p in cat['source']['parameters']]==['p','x'] and cat['source']['steps'][5]['literal']=='xb','defining-source AST and catalogue')
 old=(root/'retained/write-call/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
 r.yes('reviewed producer prefix exact unchanged',lambda:new[:len(old)]==old,'byte/source preservation')
 r.yes('runtime sources exact unchanged',lambda:all((root/'source-evidence'/n).read_bytes()==(root/'retained/write-call/source-evidence'/n).read_bytes() for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py')),'byte/source preservation')
 r.yes('prepared public JSON receipt shape',lambda:m._receipt_shape((root/'receipts/prepared-helper-open-attempt.json').read_bytes()) is not None,'public shape gate only; no derivation')
 olddefs={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(old).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};newdefs={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(new).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 r.yes('all historical named definitions preserved',lambda:all(newdefs[n]==v for n,v in olddefs.items()),'source AST preservation')
 for idx in (0,1):
  for control in (False,True):
   for origin in ('close','append'):
    tag=f'{idx}-{control}-{origin}';pc=json.loads((root/'fixtures/write-call'/(tag+'.json')).read_bytes());fx=F.make(c,cat,pc)
    r.yes('constructed normal source oracle '+tag,lambda fx=fx,pc=pc:F.oracle(fx['output'],pc['output']),'source/constructed oracle; saved parent not authenticated here')
    bad=D(fx['output']);bad['open_arguments']['mode']['concrete_value']='wb';r.no('wrong mode '+tag,lambda bad=bad,fx=fx:c.validate_helper_open_projection(cat,fx['projection'],fx['projection'],bad),'constructed producer output comparison; no authenticated predecessor','OPEN-OUTPUT-CORRESPONDENCE')
    bad=D(fx['output']);bad['bound_parameters']['p']['name']=S('p');r.no('exact nested parameter type '+tag,lambda bad=bad,fx=fx:c.validate_helper_open_projection(cat,fx['projection'],fx['projection'],bad),'exact-type output gate','OPEN-OUTPUT-TYPE')
 r.save('independent-source-plan.json',F.plan(raws[0]))
except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
finally:r.finish(failure)
if failure:raise SystemExit(1)
