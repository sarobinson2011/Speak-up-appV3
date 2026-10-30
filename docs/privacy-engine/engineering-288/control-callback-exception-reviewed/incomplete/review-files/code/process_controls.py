from pathlib import Path
import sys,json,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);mode=sys.argv[3];error=None
try:
 r.save('input-verification.json',verify_root(root));monitor=guard(root,r.path);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/primary/control-exception.json').read_bytes()
 if mode=='public':
  args=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/control-exception.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=args
  (r.path/'CLI.stdout').write_text(out.getvalue());v=json.loads(out.getvalue());r.save('CLI-result.json',v)
  r.yes('actual fresh public CLI accepts exact receipt and both contexts',lambda:v['result']=='PASS' and v['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and v['receipt']==ident(saved) and v['actual_admission'] is False)
  v['contexts'].reverse();v['receipt']['bytes']=0
  r.yes('mutated public result preserves context constants and fresh identity',lambda:m.CONTEXTS==('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO') and type(m.CONTEXTS) is tuple and m.identity(saved)==ident(saved))
  for rel in ('control_exception_revocation_correspondence','callback_bare_rethrow_correspondence','callback_stored_failure_correspondence','stored_failure_revocation_correspondence','token_registration_correspondence'):
   q=json.loads(saved);del q['contexts'][1][rel];r.no('public mandatory '+rel,lambda q=q:m.validate(root,m.enc(q)),'MANDATORY')
  q=json.loads(saved);q['contexts'].pop();r.no('public missing context',lambda:m.validate(root,m.enc(q)),'MANDATORY')
  r.no('public previous receipt cannot substitute',lambda:m.validate(root,(root/'retained/bare/results/primary/callback-bare-rethrow.json').read_bytes()),'MANDATORY')
  q=json.loads(saved)
  for row in q['contexts']:
   c=row['control_exception_revocation_correspondence'];c['exception_chain_observation']={'existing_cause':None};c['client_handler_applicable']=True;c['declaration']['source']['new_explicit_cause_assignment']=True
  r.no('public coordinated client-handler and cause invention',lambda:m.validate(root,m.enc(q)),'CONTROL-STALE-OR-ALTERED-RECEIPT')
 elif mode=='semantic':
  data=m.inputs(root);cat=m.catalogue(data);e=D(m.inner(data)['ctx']['e']);key=next(k for k,v in e.items() if v);old=e[key];e[key]=old+b'\n';r.yes('fresh evidence mutation is not a no-op',lambda:e[key]!=old)
  r.no('fresh semantic API rejects altered authenticated evidence',lambda:m.semantic(data,cat,evidence=e),'CONTROL-VALIDATED-EVIDENCE')
 else:raise ValueError('MODE')
 r.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,mode=mode)
