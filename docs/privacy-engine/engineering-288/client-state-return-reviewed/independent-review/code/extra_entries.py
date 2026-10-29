from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);raw=(root/'results/client-state-correspondence.json').read_bytes();saved=json.loads(raw);claims=[copy.deepcopy(v['client_state_return_correspondence']) for v in saved['contexts']]
 badcat=copy.deepcopy(cat);badcat['copy_semantics']['algorithm']='deepcopy memo preserves aliases'
 for r in claims:r['declaration']=copy.deepcopy(badcat)
 rec.reject('full derivation coordinated alias semantics and both context declarations reject',lambda:m.derive_client_state(d,badcat,claims),'CLIENT-STATE-SOURCE-CATALOGUE')
 ev=dict(m.inner(d)['ctx']['e']);ev.pop('evidence/recovery-export-0.json')
 rec.reject('full semantic mandatory HEAD evidence omission rejects',lambda:m.semantic(d,cat,evidence=ev),'CLIENT-STATE-MISSING-EXPORT')
 rec.check('predecessor was invoked by both checks',lambda:sum(x['function']=='derive_client' for x in CALLS)==2)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error)
