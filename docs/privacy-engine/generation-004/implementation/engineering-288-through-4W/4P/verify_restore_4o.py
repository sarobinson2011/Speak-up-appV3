"""Fresh extraction and exact saved-package execution checks; no full stream."""
import zipfile,tempfile,subprocess,time,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;start=time.monotonic();archive=ROOT.with_suffix('.zip');rows=[]
with tempfile.TemporaryDirectory(prefix='cp4o-restore-') as td:
 with zipfile.ZipFile(archive) as z:z.extractall(td)
 root=Path(td)/ROOT.name
 for args in ([sys.executable,'verify_package.py'],[sys.executable,'prepare_retained.py'],[sys.executable,'verify_4o_inputs.py'],[sys.executable,'-m','unittest','tests.test_projections'],[sys.executable,'run_4o_cli.py'],[sys.executable,'coverage_4o.py']):
  t=time.monotonic();p=subprocess.run(args,cwd=root,capture_output=True,text=True,timeout=110);rows.append({'args':args,'exit':p.returncode,'seconds':time.monotonic()-t,'stdout':p.stdout[-3000:],'stderr':p.stderr[-3000:]})
  if p.returncode:break
with archive.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
r={'result':'PASS' if len(rows)==6 and all(x['exit']==0 for x in rows) else 'FAIL','preseal_zip_sha256':h,'steps':rows,'seconds':time.monotonic()-start,'full_stream_processed':False,'actual_admission':False}
(ROOT/'results/4O-fresh-extraction.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));sys.exit(0 if r['result']=='PASS' else 1)
