"""Only IS-01 reproductions; not the independent review or historical controls."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];cases=json.loads((root/'fixtures/normal-cases.json').read_bytes())['cases'];receipt=json.loads((root/'results/status-forward-correspondence.json').read_bytes());rows=[x['internal_status_return_correspondence'] for x in receipt['contexts']]
 for idx,fx in enumerate(cases):
  tag=fx['context'];p=copy.deepcopy(fx['projection']);val={k:copy.deepcopy(v) for k,v in p.items() if k!='returned'};out=c.status_forward_projection(cat,p,val)
  for label,T in [('reason',S),('connection_epoch',I),('dictionary',D)]:
   bad=copy.deepcopy(out)
   if label=='dictionary':bad['hops'][1]['value']=D(bad['hops'][1]['value'])
   else:bad['hops'][1]['value'][label]=T(bad['hops'][1]['value'][label])
   assert enc(bad)==enc(out)
   rec.check('ORIGINAL IS-01 submitted-output accepts '+label+' '+tag,lambda bad=bad:c.validate_status_forward_projection(cat,p,val,bad))
  claims=copy.deepcopy(rows);claims[idx]['validated_manager_samples'][0]['value']['reason']=S(claims[idx]['validated_manager_samples'][0]['value']['reason']);assert enc(claims)==enc(rows)
  m._check_rows(None,claims,rows);rec.row('ORIGINAL IS-01 _check_rows accepts same-valued reason '+tag,'PASS')
  bad=copy.deepcopy(p);v=bad['returned'][1]['value'];bad['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()};assert enc(bad)==enc(p)
  rec.check('ORIGINAL IS-01 return-input accepts subclass literal key '+tag,lambda bad=bad:c.status_forward_projection(cat,bad,val)['completion']=='normal-return')
 # Reproduce full semantic/derive and constructed acceptances; exact reviewed API/context selection.
 for idx,api in [(0,'semantic'),(1,'derive_status')]:
  claims=copy.deepcopy(rows);claims[idx]['validated_manager_samples'][0]['value']['reason']=type('str',(str,),{})(claims[idx]['validated_manager_samples'][0]['value']['reason']);assert enc(claims)==enc(rows)
  result=getattr(m,api)(d,cat,claims);out=result[idx] if api=='semantic' else result['contexts'][idx]['internal_status_return_correspondence']
  rec.check('ORIGINAL IS-01 full '+api+' accepts and normalizes claim',lambda:type(out['validated_manager_samples'][0]['value']['reason']) is str and type(claims[idx]['validated_manager_samples'][0]['value']['reason']) is not str)
 fx=copy.deepcopy(cases[1]);v=fx['projection']['returned'][1]['value'];fx['projection']['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()}
 out=m.constructed_projection(d,cat,fx);rec.check('ORIGINAL IS-01 full constructed_projection accepts literal key',lambda:out['projection']['completion']=='normal-return')
 rec.check('original full calls invoke mandatory predecessor',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==3)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering reproductions of IS-01 only; independent review results retained separately')
