from pathlib import Path
import sys,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);mode=sys.argv[3];err=None
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/callback-bare-rethrow.json').read_bytes()
 if mode=='public':
  args=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/callback-bare-rethrow.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=args
  (rec.path/'CLI.stdout').write_text(out.getvalue());v=json.loads(out.getvalue());rec.save('CLI-result.json',v)
  rec.yes('fresh actual CLI accepts exact current receipt and both contexts',lambda:v['result']=='PASS' and v['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and v['receipt']==ident(saved) and v['actual_admission'] is False)
  for rel in ('callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence'):
   q=json.loads(saved);del q['contexts'][1][rel];rec.no('public mandatory relation '+rel,lambda q=q:m.validate(root,m.enc(q)))
  q=json.loads(saved);q['contexts'].pop();rec.no('public missing second context',lambda:m.validate(root,m.enc(q)))
  rec.no('public legacy predecessor cannot substitute',lambda:m.validate(root,(root/'retained/callback/results/primary/callback-stored-failure.json').read_bytes()))
  q=json.loads(saved)
  for row in q['contexts']:
   rel=row['callback_bare_rethrow_correspondence'];rel['exception_chain_observation']={'existing_cause':None};rel['declaration']['source']['bare_raise_has_explicit_cause_clause']=True
  rec.no('public coordinated invented cause in both contexts',lambda:m.validate(root,m.enc(q)),'BARE-STALE-OR-ALTERED-RECEIPT')
 elif mode=='bridges':
  data=m.inputs(root);cat=m.catalogue(data)
  fixtures=json.loads((root/'retained/review/results/primary/fixtures.json').read_bytes());x=fixtures[0]
  got=m.constructed_stored_callback(data,cat,x);rec.yes('fresh mandatory public stored-callback bridge preserves prior handle case',lambda:got['projection']==x['output'])
  got['projection']['original_error'].clear();got['projection']['callback_error']['scope'].clear();rec.yes('stored-callback returned mutation leaves exact fixture untouched',lambda:bool(x['output']['original_error']) and bool(x['output']['callback_error']['scope']))
  y=json.loads((root/'retained/callback/retained/stored/results/correction/fixtures.json').read_bytes())['cases'][3]
  after=m.constructed_normal_callback(data,cat,y);rec.yes('fresh mandatory public normal-callback bridge after nested mutation preserves second context',lambda:after['projection']==y['output'])
  after['projection']['reference_bindings'].clear();rec.yes('normal-callback returned references leave source fixture untouched',lambda:bool(y['output']['reference_bindings']))
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,mode=mode)
