"""Replacement bytes only; pure source/constructed checks, no predecessor authentication."""
from pathlib import Path
import sys,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
import cases as F
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
try:
 r.save('environment.json',environment());r.save('root.json',verify_root(root));m=module(root/'code/correspondence.py');d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];saved=m._receipt_shape((root/'receipts/prepared-write-call-replacement.json').read_bytes())
 expected=F.source_oracle((root/'source-evidence/lab_bootstrap.py').read_bytes())
 r.yes('independent defining-source evaluation order',lambda:[(s['operation'],s['source']['site']) for s in cat['source']['steps']]==expected,'independent source AST oracle')
 r.yes('complete retained producer prefix unchanged',lambda:(root/'code/managed_coverage.py').read_bytes().startswith((root/'retained/loop/code/managed_coverage.py').read_bytes()),'byte identity')
 for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):r.yes('runtime source unchanged '+n,lambda n=n:(root/'source-evidence'/n).read_bytes()==(root/'retained/loop/source-evidence'/n).read_bytes(),'byte identity')
 for idx in (0,1):
  for control in (False,True):
   for origin in ('close','append'):
    tag=f'{idx}-{control}-{origin}';pc=json.loads((root/'fixtures/loop'/(tag+'.json')).read_bytes());fx=F.make(d,cat,pc,d['prior']['contexts'][idx]['normal_session_exit_correspondence']['session_binding'])
    r.yes('normal source-constructed '+tag,lambda fx=fx:F.oracle(fx['output'],fx['parent_output']),'saved-parent constructed source oracle; not authenticated')
    for key in ('terminal_python_exception_in_model','write_new_body_entry_established'):
     bad=D(fx['output']);bad[key]=not bad[key];r.no('reject contradictory '+key+' '+tag,lambda bad=bad,fx=fx:c.validate_write_call_projection(cat,fx['projection'],fx['projection'],bad),'source-constructed output comparison; not authenticated','WC-OUTPUT-CORRESPONDENCE')
 r.save('source-order.json',expected)
except BaseException as e:failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
finally:r.finish(failure)
if failure:raise SystemExit(1)
