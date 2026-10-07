"""Reproducible CLI start/resume/terminal and corruption checks in temporary space."""
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='cp4h-cli-') as d:
        d=Path(d)
        def call(args,expected):
            p=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
            rows.append({'command':args,'exit_code':p.returncode,'expected_exit':expected,'pass':p.returncode==expected,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==expected,rows[-1]
        call(['-m','fixtures.integrated',str(d/'input')],0)
        call(['-m','integrated_auth','keygen','--key',str(d/'key')],0)
        common=['--manifest',str(d/'input/manifest.json'),'--trusted',str(d/'input/trusted.json'),'--checkpoint',str(d/'journal'),'--key',str(d/'key'),'--chunk-bytes','17']
        call(['-m','integrated_auth','start',*common,'--new-bytes','83'],3)
        call(['-m','integrated_auth','resume',*common,'--new-bytes','127'],3)
        call(['-m','integrated_auth','resume',*common,'--new-bytes','10000000'],0)
        call(['-m','integrated_auth','resume',*common,'--new-bytes','10000000'],0)
        p=d/'journal';p.write_bytes(p.read_bytes().replace(b'CONDITIONAL-BINDING',b'CORRUPTED--BINDING'))
        call(['-m','integrated_auth','resume',*common],2)
    r={'result':'PASS','cases':len(rows),'commands':rows,'profile_admitted':False,'full_retained_stream_processed':False}
    (ROOT/'results/4H-cli-recovery.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','cases':len(rows)}))
if __name__=='__main__':main()
