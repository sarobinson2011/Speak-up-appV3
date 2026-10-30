from pathlib import Path
import sys,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);mode=sys.argv[3];err=None
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/callback-stored-failure.json').read_bytes()
 if mode=='public':
  args=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/callback-stored-failure.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=args
  (rec.path/'CLI.stdout').write_text(out.getvalue());v=json.loads(out.getvalue());rec.save('CLI-result.json',v)
  rec.yes('fresh actual public CLI receipt and both contexts',lambda:v['result']=='PASS' and v['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and v['receipt']==ident(saved) and v['actual_admission'] is False)
  for rel in ('callback_stored_failure_correspondence','stored_failure_revocation_correspondence'):
   q=json.loads(saved);del q['contexts'][1][rel];rec.no('public mandatory relation '+rel,lambda q=q:m.validate(root,m.enc(q)))
  q=json.loads(saved);q['contexts'].pop();rec.no('public mandatory second context',lambda:m.validate(root,m.enc(q)))
  rec.no('legacy stored-only receipt cannot substitute',lambda:m.validate(root,(root/'retained/stored/results/correction/stored-failure-revocation.json').read_bytes()))
  q=json.loads(saved)
  for row in q['contexts']:
   s=row['callback_stored_failure_correspondence']['declaration']['source'];s['cause_expression']='owner.failure';s['raise_expression']='client_error'
  rec.no('public coordinated reversed cause in both contexts',lambda:m.validate(root,m.enc(q)),'CALLBACK-STALE-OR-ALTERED-RECEIPT')
 elif mode=='normal-bridge':
  data=m.inputs(root);cat=m.catalogue(data);fixture=json.loads((root/'retained/stored/results/correction/fixtures.json').read_bytes())['cases'][3]
  got=m.constructed_normal_callback(data,cat,fixture);rec.yes('new public bridge accepts exact reviewed normal-callback state case',lambda:got['projection']==fixture['output'])
  got['projection']['original_error'].clear();got['projection']['reference_bindings'].clear();rec.yes('normal-branch returned result leaves input unchanged',lambda:fixture['output']['original_error']==fixture['failure_result']['original_exception'] and len(fixture['output']['reference_bindings'])>0)
  # A fresh semantic call must rebuild expectations after arbitrary returned-result changes.
  e=dict(m.inner(data)['ctx']['e']);name=sorted(e)[0];rec.save('evidence-mutation.json',{'member':name,'original':ident(e[name]),'changed':ident(e[name]+b'\n')});e[name]+=b'\n'
  rec.no('fresh semantic rejects stale/altered evidence after returned mutation',lambda:m.semantic(data,cat,evidence=e),'CALLBACK-VALIDATED-EVIDENCE')
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,mode=mode)
