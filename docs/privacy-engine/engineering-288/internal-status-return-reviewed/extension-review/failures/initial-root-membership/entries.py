from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None;findings=[]
try:
 monitor=guard(root);m=module(root/'code/correspondence.py');monitor(m);raw=(root/'results/status-forward-correspondence.json').read_bytes();receipt=json.loads(raw)
 if mode=='public':
  r=rec.check('current public receipt accepted',lambda:m.validate(root,raw));rec.check('public result preserves contexts and disabled admission',lambda:r['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and r['actual_admission'] is False and r['runtime_status_forwarding']=='UNAVAILABLE')
  r['contexts'].reverse();r['receipt'].clear();r['actual_admission']=True
  rec.check('public pristine acceptance after nested return mutation',lambda:m.validate(root,raw)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 elif mode=='semantic':
  d=m.inputs(root);cat=m.catalogue(d);rows=rec.check('semantic returns exact mandatory two-context rows',lambda:m.semantic(d,cat));want=[r['internal_status_return_correspondence'] for r in receipt['contexts']];rec.check('semantic rows match exact current receipt',lambda:enc(rows)==enc(want))
  rows.reverse();rows[0]['declaration']['declarations'].clear();rows[1]['validated_manager_samples'][0]['snapshot']['_epoch']=913;rows[1]['instance_anchor']['instance']['binding']='f'*64
  rec.check('nested semantic mutations do not change future expectations',lambda:enc(m.semantic(d,cat))==enc(want))
 elif mode=='coordinated':
  d=m.inputs(root);cat=m.catalogue(d);claims=copy.deepcopy([x['internal_status_return_correspondence'] for x in receipt['contexts']]);ev=dict(m.inner(d)['ctx']['e']);path='evidence/execution-trace.json';tr=json.loads(ev[path])
  for e in tr['events']:
   if e.get('function')=='ManagedAuthority.status' and e.get('event')=='return' and e.get('normal_return'):e['state']['_reason']='substituted';e['value']['reason']='substituted'
  ev[path]=enc(tr)
  for r in claims:
   for s in r['validated_manager_samples']:s['snapshot']['_reason']='substituted';s['value']['reason']='substituted'
  rec.reject('full semantic rejects coordinated trace and all sample reasons',lambda:m.semantic(d,cat,claims,ev),'STATUS-FORWARD-VALIDATED-STATUS-VALUE')
 elif mode=='derive':
  d=m.inputs(root);cat=m.catalogue(d);claims=copy.deepcopy([x['internal_status_return_correspondence'] for x in receipt['contexts']]);badcat=copy.deepcopy(cat);badcat['guard_semantics']['READY_required']=True
  for r in claims:r['declaration']=copy.deepcopy(badcat)
  rec.reject('full derivation rejects coordinated invented READY guards',lambda:m.derive_status(d,badcat,claims),'STATUS-FORWARD-CATALOGUE')
 elif mode=='public-negative':
  bad=copy.deepcopy(receipt)
  for r in bad['contexts']:
   for s in r['internal_status_return_correspondence']['validated_manager_samples']:s['value']['actual_admission']=0
  rec.reject('public wrong exact bool constants reject',lambda:m.validate(root,enc(bad)),'STALE-OR-ALTERED')
  bad=copy.deepcopy(receipt);bad['contexts'][1].pop('internal_status_return_correspondence');rec.reject('public mandatory relation omission rejects',lambda:m.validate(root,enc(bad)),'MANDATORY-RELATION')
 else:raise AssertionError(mode)
 rec.check('actual reviewed predecessor derive_client_state invoked',lambda:any(c['function']=='derive_client_state' for c in CALLS))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,findings=findings)
