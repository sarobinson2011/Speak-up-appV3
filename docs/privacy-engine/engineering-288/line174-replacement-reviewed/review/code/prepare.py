"""Prepare immutable reviewer fixtures from saved parents; not authentication."""
from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from integrity import AREA,BASE
from independent_model import *
root=AREA/'recovered';r=Records(BASE/'results/preparation');error=None
try:
 r.save('root.json',verify_root(root));m=module(root/'code/correspondence.py');c=module(root/'code/managed_coverage.py');receipt=json.loads((root/'receipts/prepared-write-call-replacement.json').read_bytes())
 cat=receipt['contexts'][0][m.RELATION]['declaration'];plan=source_plan((root/'source-evidence/lab_bootstrap.py').read_bytes());check_source(cat,plan)
 r.save('independent-source-plan.json',plan);fi=BASE/'fixtures';fi.mkdir(exist_ok=False);index={}
 for path in sorted((root/'fixtures/loop').glob('*.json')):
  pc=json.loads(path.read_bytes());i=list(m.CONTEXTS).index(pc['context']);session=receipt['contexts'][i][m.RELATION]['session_binding'];case=build(c,cat,pc,session);oracle(cat,case,case['output']);q=fi/path.name;q.write_bytes(enc(case))
  index[path.name]={'review_fixture':file_ident(q),'saved_parent':file_ident(path),'context':pc['context'],'invocation':pc['invocation'],'authentication':'NOT YET; saved parent preparation only','runtime_observation':False}
 r.save('fixture-index.json',index);r.event('prepared',fixtures=len(index),source_regions=len(plan),actual_public_validation=False)
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='preparation only; no independently counted candidate controls')
