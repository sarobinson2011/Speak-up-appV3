"""New full public entry checks; guarded saved evidence only."""
from pathlib import Path
import sys,copy,json,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class D(dict):pass
class L(list):pass
class B(bytes):pass
try:
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);c=d['coverage'];fixtures=json.loads((root/'original/fixtures/normal-cases.json').read_bytes())['cases'];expected=json.loads((root/'results/primary/corrected-receipt.json').read_bytes());rows=[r['internal_status_return_correspondence'] for r in expected['contexts']]
 out=m.semantic(d,cat,copy.deepcopy(rows));rec.check('public pristine semantic accepts both contexts',lambda:out==rows)
 out[0]['validated_manager_samples'][0]['value']['reason']='mutated';out[1]['conditional_links'].clear();out.clear()
 full=m.derive_status(d,cat,copy.deepcopy(rows));rec.check('public derive after nested semantic output mutations remains pristine',lambda:all(full[k]==v for k,v in expected.items() if k!='extension_components'))
 rec.save('corrected-receipt.json',full);saved=(rec.path/'corrected-receipt.json').read_bytes();full['contexts'][0]['internal_status_return_correspondence']['scope']['instance'].clear();full['contexts'].clear()
 for i,fx in enumerate(fixtures):
  projected=m.constructed_projection(d,cat,copy.deepcopy(fx));rec.check('full constructed entry pristine '+fx['context'],lambda:projected['projection']['completion']=='normal-return' and not projected['runtime_observation'])
  projected['projection']['hops'][0]['value'].clear();projected['anchor']['instance'].clear()
 rec.check('public JSON receipt validation after mutated returned objects',lambda:m.validate(root,saved)['result']=='PASS')
 # Full changed builtin claims must reach independent expected rows, not just preflight.
 claims=copy.deepcopy(rows);claims[0]['validated_manager_samples'][0]['value']['reason']='wrong reason';claims[1]['validated_manager_samples'][0]['value']['reason']='wrong reason'
 rec.reject('full coordinated same-type semantic claims rejected',lambda:m.semantic(d,cat,claims),'STATUS-FORWARD-SAMPLES')
 rec.reject('public exact receipt bytes rejects subclass',lambda:m.validate(root,B(saved)))
 launcher,entry=m.sources(d);fields=m.manager_fields(d);boundary=m.inner(d)['ctx']['binding']
 for producer in [c.status_forward_source,c.compile_status_forward]:
  bad=copy.deepcopy(fields);bad['declarations']=L(bad['declarations']);rec.reject(producer.__name__+' source field container preflight',lambda producer=producer,bad=bad:producer(launcher,entry,bad,boundary))
  bad=copy.deepcopy(boundary);bad['sites']=L(bad['sites']);rec.reject(producer.__name__+' boundary container preflight',lambda producer=producer,bad=bad:producer(launcher,entry,fields,bad))
  rec.reject(producer.__name__+' exact raw source preflight',lambda producer=producer:producer(B(launcher),entry,fields,boundary))
 for fx in fixtures:
  p=copy.deepcopy(fx['projection']);val={k:copy.deepcopy(v) for k,v in p.items() if k!='returned'};bad=copy.deepcopy(val);bad['scope']['context']=S(bad['scope']['context']);rec.reject('validated-only subclass premise '+fx['context'],lambda:c.status_forward_projection(cat,p,bad))
  bad=copy.deepcopy(fx['anchor']);bad['context']=S(bad['context']);rec.reject('scope helper anchor type '+fx['context'],lambda:m.invocation_scope(bad,'legitimate'))
  scope=copy.deepcopy(p['scope']);scope['instance']=D(scope['instance']);rec.reject('reference helper scope type '+fx['context'],lambda:m.reference_premises(scope,True,False))
 # Preserves the guard while checking a root symlink without loading any candidate.
 symlink=Path(sys.argv[3]);symlink.symlink_to(root,target_is_directory=True)
 rec.reject('correction root must be an actual directory',lambda:m.inputs(symlink),'CORRECTION-ROOT-TYPE')
 rec.check('six full calls invoked actual mandatory predecessor',lambda:sum(v['function']=='derive_client_state' for v in CALLS)==6)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering fresh-process public entries; not runtime execution or independent review')
