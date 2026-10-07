"""Fresh extraction, identity/bootstrap and small CLI recovery test; no full stream."""
import hashlib,json,subprocess,sys,tempfile,time,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    target=ROOT.with_suffix('.zip');start=time.monotonic();rows=[]
    with tempfile.TemporaryDirectory(prefix='cp4k-restore-') as d:
        with zipfile.ZipFile(target) as z:z.extractall(d)
        restored=Path(d)/ROOT.name
        for args in (['verify_package.py'],['prepare_retained.py'],['run_4k_cli.py'],['-m','unittest','tests.test_schedule']):
            p=subprocess.run([sys.executable,*args],cwd=restored,capture_output=True,text=True,timeout=60);rows.append({'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,rows[-1]
    r={'result':'PASS','preseal_zip_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'commands':rows,'seconds':time.monotonic()-start,'full_retained_stream_processed':False,'profile_admitted':False};(ROOT/'results/4K-fresh-restore.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','seconds':r['seconds']}))
if __name__=='__main__':main()
