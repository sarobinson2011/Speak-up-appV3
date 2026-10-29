from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;findings=[]
class S(str):pass
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);case=copy.deepcopy(json.loads((root/'fixtures/normal-cases.json').read_bytes())['cases'][1]);v=case['projection']['returned'][1]['value'];case['projection']['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()};assert type(next(k for k in case['projection']['returned'][1]['value'] if k=='phase')) is S
 try:out=m.constructed_projection(d,cat,case)
 except ValueError as e:rec.row('full constructed projection exact literal key','REJECTED',error=str(e))
 else:
  assert out['projection']['completion']=='normal-return';rec.row('full constructed projection accepts wrong literal-key type','DEFECT-ACCEPTED');findings.append({'id':'IS-01','API':'constructed_projection','context':case['context'],'mutation':'single session-return phase key is S(str), same text','actual_full_predecessor_validation':True,'accepted':True})
 rec.check('actual reviewed predecessor invoked',lambda:any(x['function']=='derive_client_state' for x in CALLS));rec.save('key-type-full-witness.json',findings)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,findings=findings)
