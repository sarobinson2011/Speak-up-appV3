"""Reproducible CLI recovery for all declared occurrence phases."""
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 rows=[]
 with tempfile.TemporaryDirectory(prefix='cp4l-cli-') as folder:
  base=Path(folder)
  def call(args,expected):
   p=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
   rows.append({'command':args,'exit_code':p.returncode,'expected_exit':expected,'stdout':p.stdout,'stderr':p.stderr,'pass':p.returncode==expected});assert p.returncode==expected,rows[-1]
  call(['-m','integrated_auth','keygen','--key',str(base/'key')],0)
  for phase in ('E','PRE-EXECUTION','PRE-COMMITMENT'):
   folder=base/phase;call(['-m','fixtures.occurrence',str(folder),'--phase',phase,'--disconnected'],0)
   common=['--manifest',str(folder/'manifest.json'),'--trusted',str(folder/'trusted.json'),'--checkpoint',str(folder/'journal'),'--key',str(base/'key')]
   call(['-m','integrated_auth','start',*common,'--new-bytes','53','--chunk-bytes','7'],3)
   call(['-m','integrated_auth','resume',*common,'--new-bytes','10000000'],0)
   call(['-m','integrated_auth','resume',*common],0)
   ck=folder/'journal';ck.write_bytes(b'{}\n');call(['-m','integrated_auth','resume',*common],2)
 r={'result':'PASS','cases':len(rows),'commands':rows,'profile_admitted':False,'full_retained_stream_processed':False}
 (ROOT/'results/4L-cli-recovery.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','cases':len(rows)}))
if __name__=='__main__':main()
