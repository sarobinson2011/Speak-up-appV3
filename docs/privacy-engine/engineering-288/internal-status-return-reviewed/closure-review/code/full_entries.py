from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class B(bytes):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);raw=(root/'results/fresh/corrected-receipt.json').read_bytes();bundle=json.loads(raw);expected=[r['internal_status_return_correspondence'] for r in bundle['contexts']];fixtures=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases']
 before=sum(x['function']=='derive_client_state' for x in CALLS)
 for idx in range(2):
  claims=copy.deepcopy(expected);sample=claims[idx]['validated_manager_samples'][0]['value'];sample['reason']=S(sample['reason']);assert enc(claims)==enc(expected)
  for api in ('semantic','derive_status'):
   rec.reject('current full '+api+' rejects original reason witness '+expected[idx]['context'],lambda api=api:getattr(m,api)(data,cat,claims),'VALUE-TYPE')
  case=copy.deepcopy(fixtures[idx]);v=case['projection']['returned'][1]['value'];case['projection']['returned'][1]['value']={S(k) if k=='phase' else k:x for k,x in v.items()}
  rec.reject('current full constructed entry rejects literal key '+expected[idx]['context'],lambda:m.constructed_projection(data,cat,case),'KEY-TYPE')
 rec.check('incorrect exact types rejected before predecessor or normalization',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==before)
 result=m.derive_status(data,cat,copy.deepcopy(expected));rec.check('full current derivation exact receipt both contexts',lambda:enc(result)==raw)
 result['contexts'].reverse();result['contexts'][0]['internal_status_return_correspondence']['validated_manager_samples'][0]['value']['reason']='returned-object-mutation';result['contexts'][1]['internal_status_return_correspondence']['declaration']['reference_edges'].clear()
 rows=m.semantic(data,cat,copy.deepcopy(expected));rec.check('pristine full semantic after nested derived-result mutation',lambda:enc(rows)==enc(expected))
 # Change both reported values and supplied raw evidence, keeping their types legitimate.
 claims=copy.deepcopy(expected);ev=dict(m.inner(data)['ctx']['e']);tr=json.loads(ev['evidence/execution-trace.json'])
 for event in tr['events']:
  if event.get('function')=='ManagedAuthority.status' and event.get('event')=='return' and event.get('normal_return'):
   event['value']['reason']='coordinated-false-reason';event['state']['_reason']='coordinated-false-reason'
 ev['evidence/execution-trace.json']=enc(tr)
 for row in claims:
  for sample in row['validated_manager_samples']:
   sample['value']['reason']='coordinated-false-reason';sample['snapshot']['_reason']='coordinated-false-reason'
 rec.reject('full semantic rejects coordinated trace and claims against fresh evidence',lambda:m.semantic(data,cat,claims,ev),'STATUS-FORWARD-VALIDATED-STATUS-VALUE')
 rec.reject('public bytes subclass is not an exact byte receipt',lambda:m.validate(root,B(raw)),'RECEIPT-BYTES')
 missing=copy.deepcopy(bundle);missing['contexts'][1].pop('internal_status_return_correspondence')
 rec.reject('public relation omission is not optional',lambda:m.validate(root,enc(missing)),'MANDATORY-RELATION')
 # Already validated expected rows give targeted shape/binding controls, not detached success claims.
 for label,fn in [('missing context',lambda x:x.pop()),('duplicated context',lambda x:x.__setitem__(1,copy.deepcopy(x[0]))),('reversed contexts',lambda x:x.reverse()),('wrong instance',lambda x:x[0]['instance_anchor']['instance'].update(binding='0'*64)),('stale frontier',lambda x:x[1]['scope'].update(frontier='stale')),('unsupported qualification',lambda x:x[0].update(classification='QUALIFIED'))]:
  wrong=copy.deepcopy(rows);fn(wrong);assert enc(wrong)!=enc(rows);rec.reject('semantic row '+label,lambda:m._check_rows(None,wrong,rows))
 rec.check('three full current calls execute actual predecessor',lambda:sum(x['function']=='derive_client_state' for x in CALLS)==3)
 rec.save('fresh-valid-receipt.json',bundle)
 rec.check('source-only observation and obligation boundaries retained',lambda:bundle['new_internal_status_limits']==json.loads((root/'original/results/status-forward-correspondence.json').read_bytes())['new_internal_status_limits'])
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent corrected full-entry validation with exact saved inputs; no runtime forwarding')
