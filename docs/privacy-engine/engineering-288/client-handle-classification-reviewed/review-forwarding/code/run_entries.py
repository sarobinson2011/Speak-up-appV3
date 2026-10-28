"""Schedule new bounded saved-input checks; each has its own fresh interpreter."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess,sys,json,time
base=Path(__file__).resolve().parents[1];cwd=base.parent
jobs=[('primary',x) for x in ['wrong-instance-0','wrong-instance-1','catalogue','journal-semantic','journal-derivation','mutable-input','missing-export','stale-output','public-omission','public-status','public-contexts','public-stale','semantic-alias','public-alias']]+[('recovered',x) for x in ['wrong-instance-1','journal-derivation','missing-export','public-omission','public-alias']]
def job(pair):
 mode,case=pair;root=cwd/('ch-input' if mode=='primary' else 'ch-recovered-2')
 r=subprocess.run([sys.executable,'-I','-B',str(base/'code/job_runner.py'),str(root),mode,case],capture_output=True)
 rec={'mode':mode,'case':case,'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}
 with (base/'results/entry-scheduler-progress.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(mode,case,r.returncode,flush=True);return rec
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(job,jobs))
(base/'results/entry-scheduler.json').write_text(json.dumps(results,indent=2)+'\n');assert all(r['exit_code']==0 for r in results)
