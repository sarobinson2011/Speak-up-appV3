from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);raw=(root/'results/fresh/corrected-receipt.json').read_bytes();obj=json.loads(raw)
 for row in obj['contexts']:
  sample=row['internal_status_return_correspondence']['validated_manager_samples'][0]['value'];sample['reason']=S(sample['reason'])
 normalized=enc(obj);rec.check('JSON cannot encode same-valued str subclass distinction',lambda:normalized==raw and all(type(r['internal_status_return_correspondence']['validated_manager_samples'][0]['value']['reason']) is S for r in obj['contexts']))
 out=m.validate(root,normalized);rec.check('public original canonical receipt accepted',lambda:out['result']=='PASS' and out['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and out['actual_admission'] is False)
 out['contexts'].reverse();out['receipt'].clear();out['actual_admission']=True
 out2=m.validate(root,raw);rec.check('public returned aliases cannot change subsequent validation',lambda:out2=={'result':'PASS','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'receipt':identity(raw),'runtime_status_forwarding':'UNAVAILABLE','actual_admission':False})
 old=(root/'original/results/status-forward-correspondence.json').read_bytes();assert old!=raw
 rec.reject('public stale affected-code receipt rejects',lambda:m.validate(root,old),'STALE-OR-ALTERED')
 obj=json.loads(raw);obj['contexts'][0].pop('internal_status_return_correspondence');rec.reject('public missing mandatory relation rejects',lambda:m.validate(root,enc(obj)),'MANDATORY-RELATION')
 rec.check('three public checks consumed actual current predecessor chain',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==3)
 rec.save('public-result.json',out2)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent public byte-entry checks; normalized bytes remain distinct from in-memory acceptance')
