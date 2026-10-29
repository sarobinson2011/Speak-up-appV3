"""Focused full entries in a fresh process, saved evidence only."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
class B(bytes):pass
try:
 if '--recovered' in sys.argv:rec.save('recovered-input-verification.json',verify_root(root))
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);saved=(root/'results/primary/token-registration-correspondence.json').read_bytes();bundle=json.loads(saved);rows=[ctx['token_registration_correspondence'] for ctx in bundle['contexts']];fixtures=json.loads((root/'results/primary/fixtures.json').read_bytes())['cases']
 out=m.semantic(d,cat,copy.deepcopy(rows));rec.check('fresh actual semantic relation accepts both contexts',lambda:out==rows)
 out[0]['instance_anchor']['instance'].clear();out[1]['conditional_links'].clear();out.clear()
 got=m.derive_token(d,cat,copy.deepcopy(rows));rec.check('fresh derive after nested result mutations exact receipt',lambda:m.enc(got)==saved)
 got['contexts'][0]['token_registration_correspondence']['scope']['instance'].clear();got['contexts'].clear()
 rec.check('public JSON validation remains pristine',lambda:m.validate(root,saved)['result']=='PASS')
 for fx in fixtures:
  got=m.constructed_projection(d,cat,fx);rec.check('full constructed entry '+fx['context'],lambda:got['projection']['removal_completed_in_model'] and not got['runtime_observation'])
 # Coordinated claims must be checked against the same actual predecessor.
 claims=copy.deepcopy(rows)
 for r in claims:r['declaration']['source']['remove']['key']='substituted-token'
 rec.reject('full semantic rejects coordinated source claims',lambda:m.semantic(d,cat,claims))
 claims=copy.deepcopy(rows);claims[0]['instance_anchor']['instance']['binding']='substituted'
 rec.reject('full derive rejects stale instance binding',lambda:m.derive_token(d,cat,claims))
 bad=copy.deepcopy(fixtures[1]);bad['projection']['scope']=copy.deepcopy(fixtures[0]['projection']['scope']);bad['projection']['references']=copy.deepcopy(fixtures[0]['projection']['references']);bad['output']=copy.deepcopy(fixtures[0]['output'])
 rec.reject('full constructed rejects cross-context coordinated references',lambda:m.constructed_projection(d,cat,bad))
 altered=json.loads(saved);del altered['contexts'][0]['token_registration_correspondence'];rec.reject('public receipt requires new relation in both contexts',lambda:m.validate(root,m.enc(altered)))
 altered=json.loads(saved)
 for ctx in altered['contexts']:ctx['token_registration_correspondence']['conditional_links'].clear()
 rec.reject('public receipt rejects coordinated omission',lambda:m.validate(root,m.enc(altered)))
 rec.reject('public exact bytes contract retained',lambda:m.validate(root,B(saved)))
 bad=copy.deepcopy(rows);bad[0]['context']=S(bad[0]['context']);rec.reject('semantic exact type before fresh construction',lambda:m.semantic(d,cat,bad))
 bad=copy.deepcopy(fixtures[0]);bad['output']['completion']=S(bad['output']['completion']);rec.reject('constructed exact type before fresh construction',lambda:m.constructed_projection(d,cat,bad))
 rec.check('all accepted and value-mutated entries mandatorily invoked predecessor',lambda:sum(x['function']=='derive_status' for x in CALLS)==9)
 rec.save('receipt-identity.json',identity(saved))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering fresh full-entry controls; no runtime or prior-suite execution')
