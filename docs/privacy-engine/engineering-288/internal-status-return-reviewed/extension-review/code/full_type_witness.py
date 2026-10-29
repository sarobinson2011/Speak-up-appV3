from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;findings=[]
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);d=m.inputs(root);cat=m.catalogue(d);raw=(root/'results/status-forward-correspondence.json').read_bytes();bundle=json.loads(raw);original=[r['internal_status_return_correspondence'] for r in bundle['contexts']]
 for idx,api in [(0,'semantic'),(1,'derive_status')]:
  claims=copy.deepcopy(original);x=claims[idx]['validated_manager_samples'][0]['value'];T=type('str',(str,),{});x['reason']=T(x['reason']);assert type(x['reason']) is not str and enc(claims)==enc(original)
  try:out=getattr(m,api)(d,cat,claims)
  except ValueError as e:rec.row('full '+api+' rejects wrong exact reason type','REJECTED',error=str(e))
  else:
   row=out[idx] if api=='semantic' else out['contexts'][idx]['internal_status_return_correspondence']
   assert type(row['validated_manager_samples'][0]['value']['reason']) is str
   findings.append({'id':'IS-01','API':api,'context':original[idx]['context'],'mutation_path':f'claims/{idx}/validated_manager_samples/0/value/reason','mutation':'str subclass with exact same characters','accepted':True,'fresh_result_has_builtin_str':True,'supplied_wrong_type_still_present':type(x['reason']) is not str,'serialization_equal':True,'input_evidence_or_sources_changed':False})
   rec.row('full '+api+' accepts wrong exact reason type','DEFECT-ACCEPTED')
 # This contrasts an actual value change, which is rejected against fresh evidence.
 claims=copy.deepcopy(original);claims[0]['validated_manager_samples'][0]['value']['reason']='altered-reason'
 rec.reject('full semantic rejects changed reason characters',lambda:m.semantic(d,cat,claims),'STATUS-FORWARD-SAMPLES')
 rec.check('actual predecessor validation invoked for every full call',lambda:sum(v['function']=='derive_client_state' for v in CALLS)==3)
 rec.save('full-type-witnesses.json',findings)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,findings=findings)
