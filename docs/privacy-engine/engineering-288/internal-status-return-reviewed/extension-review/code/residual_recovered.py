from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;findings=[]
class S(str):pass
class I(int):pass
class D(dict):pass
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];bundle=json.loads((root/'results/status-forward-correspondence.json').read_bytes());rows=[x['internal_status_return_correspondence'] for x in bundle['contexts']];cases=json.loads((root/'fixtures/normal-cases.json').read_bytes())['cases']
 for idx,fx in enumerate(cases):
  p=copy.deepcopy(fx['projection']);val={k:copy.deepcopy(v) for k,v in p.items() if k!='returned'};out=c.status_forward_projection(cat,p,val)
  for label,T in [('reason',S),('connection_epoch',I),('dictionary',D)]:
   bad=copy.deepcopy(out)
   if label=='dictionary':bad['hops'][1]['value']=D(bad['hops'][1]['value'])
   else:bad['hops'][1]['value'][label]=T(bad['hops'][1]['value'][label])
   assert enc(bad)==enc(out)
   try:r=c.validate_status_forward_projection(cat,p,val,bad)
   except ValueError as e:rec.row('recovered output exact type '+label+' '+fx['context'],'REJECTED',error=str(e))
   else:
    assert r is True;rec.row('recovered output accepts subclass '+label+' '+fx['context'],'DEFECT-ACCEPTED');findings.append({'id':'IS-01','API':'validate_status_forward_projection','context':fx['context'],'field':label,'class_name':T.__name__,'accepted':True,'serialization_equal':True})
  wrong=copy.deepcopy(p);wrong['returned'][1]['value']['reason']=S(wrong['returned'][1]['value']['reason']);rec.reject('same arbitrary subclass correctly rejects as return-input '+fx['context'],lambda wrong=wrong:c.status_forward_projection(cat,wrong,val),'RETURN-FIELD-TYPE:reason')
  # Full recovered semantic/derivation checks use arbitrary subclass name, not a builtin-name spoof.
  claims=copy.deepcopy(rows);claims[idx]['validated_manager_samples'][0]['value']['reason']=S(claims[idx]['validated_manager_samples'][0]['value']['reason']);api='semantic' if idx==0 else 'derive_status'
  try:result=getattr(m,api)(d,cat,claims)
  except ValueError as e:rec.row('recovered full exact type '+api,'REJECTED',error=str(e))
  else:
   rec.row('recovered full '+api+' accepts arbitrary str subclass','DEFECT-ACCEPTED');findings.append({'id':'IS-01','API':api,'context':fx['context'],'field':'one sample value.reason','class_name':'S','accepted':True,'exact_type_wrong':True})
 rec.check('both full checks invoked actual predecessor',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==2)
 rec.save('residual-witnesses.json',findings)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,findings=findings)
