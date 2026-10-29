"""Fresh public validation of the corrected receipt on a separately recovered root."""
from pathlib import Path
import sys,traceback,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
try:
 verify_root(root);mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m)
 result=m.validate(root,(root/'results/fresh/corrected-receipt.json').read_bytes());rec.check('recovered fresh public JSON validator',lambda:result['result']=='PASS');rec.save('public-result.json',result)
 rec.check('mandatory predecessor actually invoked exactly once',lambda:sum(v['function']=='derive_client_state' for v in CALLS)==1)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering recovered-root fresh public entry, saved inputs only')
