from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;witnesses=[]
class S(str):pass
class I(int):pass
class D(dict):pass
try:
 mon=guard(root);m=module(root/'original/code/correspondence.py');mon(m);d=m.inputs(root/'original');cat=m.catalogue(d);c=d['coverage'];cases=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases'];bundle=json.loads((root/'original/results/status-forward-correspondence.json').read_bytes());rows=[x['internal_status_return_correspondence'] for x in bundle['contexts']]
 for idx,fx in enumerate(cases):
  p=copy.deepcopy(fx['projection']);v={k:copy.deepcopy(x) for k,x in p.items() if k!='returned'};expected=c.status_forward_projection(cat,p,v)
  for field,T in [('reason',S),('connection_epoch',I),(None,D)]:
   bad=copy.deepcopy(expected)
   if field is None:bad['hops'][1]['value']=T(bad['hops'][1]['value'])
   else:bad['hops'][1]['value'][field]=T(bad['hops'][1]['value'][field])
   assert enc(bad)==enc(expected)
   rec.check('old submitted-output accepts '+str(field)+' '+fx['context'],lambda:c.validate_status_forward_projection(cat,p,v,bad))
   witnesses.append({'boundary':'submitted-output','context':fx['context'],'field':field,'type':T.__name__,'same_encoded_bytes':True,'accepted':True})
  claims=copy.deepcopy(rows);claims[idx]['validated_manager_samples'][0]['value']['reason']=S(claims[idx]['validated_manager_samples'][0]['value']['reason']);assert enc(claims)==enc(rows);m._check_rows(None,claims,rows);rec.row('old semantic row accepts reason '+fx['context'],'PASS')
  keycase=copy.deepcopy(p);value=keycase['returned'][1]['value'];keycase['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in value.items()};assert enc(keycase)==enc(p)
  rec.check('old return-input accepts literal-key subclass '+fx['context'],lambda:c.status_forward_projection(cat,keycase,v)['completion']=='normal-return')
  witnesses.append({'boundary':'return-input','context':fx['context'],'field':'phase KEY','type':'S(str)','same_encoded_bytes':True,'accepted':True})
 # Both contexts contaminated together: actual full old APIs accept, regenerate builtin strings.
 for api in ('semantic','derive_status'):
  claims=copy.deepcopy(rows)
  for row in claims:row['validated_manager_samples'][0]['value']['reason']=S(row['validated_manager_samples'][0]['value']['reason'])
  assert enc(claims)==enc(rows);out=getattr(m,api)(d,cat,claims);got=out if api=='semantic' else [x['internal_status_return_correspondence'] for x in out['contexts']]
  rec.check('old full '+api+' accepts wrong exact types in both contexts',lambda:all(type(x['validated_manager_samples'][0]['value']['reason']) is str for x in got) and all(type(x['validated_manager_samples'][0]['value']['reason']) is S for x in claims))
  witnesses.append({'boundary':api,'contexts':[r['context'] for r in rows],'field':'reason','type':'S(str)','same_encoded_bytes':True,'accepted':True,'returns_regenerated_builtin_values':True})
 fx=copy.deepcopy(cases[1]);v=fx['projection']['returned'][1]['value'];fx['projection']['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()};out=m.constructed_projection(d,cat,fx)
 rec.check('old full constructed entry accepts literal key',lambda:out['projection']['completion']=='normal-return')
 rec.check('all three old full calls validate actual predecessor',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==3)
 rec.save('witnesses.json',witnesses)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent reproduction of IS-01 only; original acceptances expected, not current acceptance or runtime observation')
