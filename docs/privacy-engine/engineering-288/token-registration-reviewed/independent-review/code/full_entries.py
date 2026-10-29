from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
class S(str):pass
class B(bytes):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);raw=(root/'results/primary/token-registration-correspondence.json').read_bytes();receipt=json.loads(raw);rows=[x['token_registration_correspondence'] for x in receipt['contexts']]
 if mode=='semantic':
  out=m.semantic(data,cat,copy.deepcopy(rows));rec.check('full semantic accepts exact two-context relation',lambda:enc(out)==enc(rows))
  out.reverse();out[0]['declaration']['source']['stages'].clear();out[1]['instance_anchor']['instance'].clear();out[0]['scope']['invocation']='mutated-result'
  out=m.derive_token(data,cat,copy.deepcopy(rows));rec.check('full derivation after nested alias mutation matches saved bytes',lambda:enc(out)==raw)
  badcat=copy.deepcopy(cat);badcat['source']['remove']['key']='foreign-token';claims=copy.deepcopy(rows)
  for row in claims:row['declaration']=copy.deepcopy(badcat)
  rec.reject('full semantic rejects coordinated generated catalogue and claims',lambda:m.semantic(data,badcat,claims),'TOKEN-CATALOGUE-SOURCE')
  for idx in range(2):
   claims=copy.deepcopy(rows);claims[idx]['context']=S(claims[idx]['context']);rec.reject('full exact-type preflight '+rows[idx]['context'],lambda:m.derive_token(data,cat,claims),'VALUE-TYPE')
  rec.check('three full current entries validate actual predecessor',lambda:sum(x['function']=='derive_status' for x in CALLS)==3)
 elif mode=='constructed':
  # Use independently built source-oracle cases, not supplied output summaries.
  fixtures=json.loads(Path(sys.argv[4]).read_bytes())['cases'];assert [x['context'] for x in fixtures]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
  normal=copy.deepcopy(fixtures[0]);got=m.constructed_projection(data,cat,normal);rec.check('full constructed selected invocation accepted',lambda:got['projection']==normal['output'] and got['projection']['removal_completed_in_model'] is True and got['runtime_observation'] is False)
  got['projection']['reference_bindings']['owner'].clear();got['anchor'].clear()
  bad=copy.deepcopy(fixtures[1]);bad['projection']=copy.deepcopy(fixtures[0]['projection']);bad['output']=copy.deepcopy(fixtures[0]['output']);rec.reject('full constructed coordinated cross-context and instance substitution',lambda:m.constructed_projection(data,cat,bad),'TOKEN-PREMISE')
  for idx in range(2):
   bad=copy.deepcopy(fixtures[idx]);bad['output']['completion']=S(bad['output']['completion']);rec.reject('constructed exact type before reconstruction '+bad['context'],lambda:m.constructed_projection(data,cat,bad),'VALUE-TYPE')
  for idx in range(2):
   bad=copy.deepcopy(receipt);bad['contexts'][idx].pop('token_registration_correspondence');rec.reject('public mandatory relation '+rows[idx]['context'],lambda:m.validate(root,enc(bad)),'TOKEN-MANDATORY-RELATION')
  old=(root/'retained/status/results/fresh/corrected-receipt.json').read_bytes();rec.reject('public cannot substitute partial predecessor validation',lambda:m.validate(root,old),'TOKEN-MANDATORY-RELATION')
  rec.reject('public exact bytes gate',lambda:m.validate(root,B(raw)),'TOKEN-RECEIPT-BYTES')
  rec.check('two full constructed entries validate actual predecessor',lambda:sum(x['function']=='derive_status' for x in CALLS)==2)
 else:raise AssertionError(mode)
 rec.check('all obligations and observation boundaries retained',lambda:receipt['new_token_registration_limits']['all_eleven_obligations_preserved'] is True and receipt['new_token_registration_limits']['actual_admission'] is False and all(r['observer_join'] is None and r['runtime_registration_revocation_links'] is None for r in rows))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='Independent mandatory full entries; saved evidence only')
