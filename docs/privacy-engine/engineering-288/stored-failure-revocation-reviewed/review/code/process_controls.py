from pathlib import Path
import sys,traceback,json,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();rec=Records(sys.argv[2]);mode=sys.argv[3];err=None
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);saved=(root/'results/correction/stored-failure-revocation.json').read_bytes()
 if mode=='public':
  args=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/correction/stored-failure-revocation.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=args
  (rec.path/'CLI.stdout').write_text(out.getvalue());v=json.loads(out.getvalue());rec.save('CLI-result.json',v)
  rec.yes('fresh actual public CLI exact receipt both contexts',lambda:v['result']=='PASS' and v['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and v['receipt']==ident(saved) and v['actual_admission'] is False)
  q=json.loads(saved);del q['contexts'][1]['stored_failure_revocation_correspondence'];rec.no('public mandatory relation omission',lambda:m.validate(root,m.enc(q)),'STORED-MANDATORY-RELATION')
  q=json.loads(saved);q['contexts'].pop();rec.no('public missing second context',lambda:m.validate(root,m.enc(q)),'STORED-MANDATORY-RELATION')
  rec.no('public receipt byte type',lambda:m.validate(root,bytearray(saved)),'STORED-RECEIPT-BYTES')
  # Original stale build includes the old narrower helper-escape catalogue.
  old=(root/'results/primary/stored-failure-revocation.json').read_bytes();rec.no('public stale pre-correction receipt',lambda:m.validate(root,old),'STORED-STALE-OR-ALTERED-RECEIPT')
 elif mode=='semantic':
  data=m.inputs(root);cat=m.catalogue(data);e=dict(m.inner(data)['ctx']['e']);name=sorted(e)[0];before=ident(e[name]);e[name]=e[name]+b'\n';rec.save('mutation.json',{'evidence':name,'original':before,'changed':ident(e[name]),'other_fields_unchanged':True})
  rec.no('fresh semantic rejects altered authenticated evidence',lambda:m.semantic(data,cat,evidence=e),'STORED-VALIDATED-EVIDENCE')
  # Returned pure catalogue aliases are not validation authorities.
  q=m.catalogue(data);q['source']['order'].reverse();q['declarations'][0]['source_origin'].clear()
  rec.yes('fresh catalogue detached after nested mutation',lambda:m.catalogue(data)==cat)
 else:raise ValueError('MODE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,mode=mode)
