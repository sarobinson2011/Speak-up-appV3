"""Verify a fresh extracted ZIP and run a fresh small CLI recovery smoke."""
import hashlib,json,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    target=ROOT.with_suffix('.zip');started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='cp4f-restore-') as d:
        with zipfile.ZipFile(target) as z:z.extractall(d)
        restored=Path(d)/ROOT.name;rows=[]
        for args in (['verify_package.py'],['prepare_retained.py'],['run_4f_cli.py']):
            p=subprocess.run([sys.executable,*args],cwd=restored,capture_output=True,text=True,timeout=60)
            rows.append({'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,rows[-1]
    receipt={'result':'PASS','zip_tested_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'commands':rows,'seconds':time.monotonic()-started,'full_retained_stream_processed':False,'profile_admitted':False}
    (ROOT/'results/4F-fresh-restore.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'result':'PASS','seconds':receipt['seconds']}))
if __name__=='__main__':main()
