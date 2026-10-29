from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;findings=[];witnesses=[]
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];old=module(root/'failures/type-acceptance-precorrection/managed_coverage.py');fixtures=json.loads((root/'fixtures/normal-cases.json').read_bytes())['cases']
 for fx in fixtures:
  ctx=fx['context'];case=copy.deepcopy(fx['projection']);val={k:copy.deepcopy(v) for k,v in case.items() if k!='returned'};baseline=c.status_forward_projection(cat,case,val)
  rec.check('legitimate typed forwarding '+ctx,lambda:baseline['completion']=='normal-return')
  for field,base in [('_phase',str),('_reason',str),('_epoch',int)]:
   T=type(base.__name__,(base,),{});snap=copy.deepcopy(case['manager_snapshot']);snap[field]=T(snap[field]);accepted=old.status_snapshot_value(cat,snap)
   rec.check('old snapshot accepts same-named subclass '+field+' '+ctx,lambda:bool(accepted) and type(snap[field]) is not base)
   rec.reject('current snapshot rejects same-named subclass '+field+' '+ctx,lambda snap=snap:c.status_snapshot_value(cat,snap),'VALUE-TYPE')
   witnesses.append({'context':ctx,'kind':'original snapshot','field':field,'class_name':type(snap[field]).__name__,'exact_builtin':False,'old_accepted':True,'current_rejected':True})
  for kind,base in [('container',dict),('reason',str),('epoch',int)]:
   q=copy.deepcopy(case);T=type(base.__name__,(base,),{});value=q['returned'][1]['value']
   if kind=='container':q['returned'][1]['value']=T(value)
   elif kind=='reason':value['reason']=T(value['reason'])
   else:value['connection_epoch']=T(value['connection_epoch'])
   oldresult=old.status_forward_projection(cat,q,val);rec.check('old returned representation accepts subclass '+kind+' '+ctx,lambda:oldresult['completion']=='normal-return')
   rec.reject('current returned representation rejects subclass '+kind+' '+ctx,lambda q=q:c.status_forward_projection(cat,q,val),'RETURN-')
   witnesses.append({'context':ctx,'kind':'original return representation','substitution':kind,'old_accepted':True,'current_rejected':True})
  # Adjacent output-validation API: it must validate the submitted forwarded values too.
  T=type('str',(str,),{});submitted=copy.deepcopy(baseline);submitted['hops'][1]['value']['reason']=T(submitted['hops'][1]['value']['reason'])
  assert type(submitted['hops'][1]['value']['reason']) is not str and enc(submitted)==enc(baseline)
  try:accepted=c.validate_status_forward_projection(cat,case,val,submitted)
  except ValueError as e:rec.row('derived-output exact reason type '+ctx,'REJECTED',error=str(e))
  else:
   assert accepted is True;rec.row('derived-output accepts wrong exact reason type '+ctx,'DEFECT-ACCEPTED');findings.append({'id':'IS-01','context':ctx,'API':'validate_status_forward_projection','mutation':"submitted['hops'][1]['value']['reason'] = type('str',(str,),{})(original_reason)",'one_value_changed':True,'wrong_exact_type':True,'serialization_equal':True,'result':True})
  # Probe semantic row checker against an exact current expected row (not a runtime operation).
  receipt=json.loads((root/'results/status-forward-correspondence.json').read_bytes());rows=[x['internal_status_return_correspondence'] for x in receipt['contexts']];claims=copy.deepcopy(rows);idx=0 if ctx=='SYMBOLIC-U-ONE' else 1;claims[idx]['validated_manager_samples'][0]['value']['reason']=T(claims[idx]['validated_manager_samples'][0]['value']['reason'])
  try:m._check_rows(None,claims,rows)
  except ValueError as e:rec.row('semantic helper exact reason type '+ctx,'REJECTED',error=str(e))
  else:rec.row('semantic helper accepts wrong exact reason type '+ctx,'DEFECT-ACCEPTED');findings.append({'id':'IS-01','context':ctx,'API':'_check_rows','mutation':'one saved manager sample value.reason -> str subclass with same contents','serialization_equal':True,'exact_type_wrong':True})
 rec.save('original-witnesses.json',witnesses);rec.save('residual-witnesses.json',findings)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,findings=findings,original_witness_reproductions=len(witnesses))
