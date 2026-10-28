"""Run only new bounded entry checks, recording each fresh process."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,sys,json,time
b=Path(__file__).resolve().parents[1];w=b.parent
jobs=[('primary',n) for n in ('semantic-contract','derive-contract','claims','public-old','public-coordinated','public-missing','semantic-alias','public-alias')]+[('recovered',n) for n in ('legitimate','semantic-contract','public-old','public-alias')]
def one(job):
 mode,name=job;p=b/'processes'/(mode+'-'+name);p.mkdir(parents=True,exist_ok=False);root=w/('oc-input' if mode=='primary' else 'oc-recovered');out=b/('independent-'+mode)/name;cmd=[sys.executable,'-I','-B',str(b/'code/entries.py'),str(root),str(out),name];start=time.monotonic()
 with (p/'stdout').open('xb') as so,(p/'stderr').open('xb') as se:r=subprocess.run(cmd,stdout=so,stderr=se)
 v={'exit_code':r.returncode,'seconds':time.monotonic()-start,'mode':mode,'case':name,'command':cmd};(p/'RESULT.json').write_text(json.dumps(v,indent=2)+'\n');print(mode,name,r.returncode,flush=True);return v
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,jobs))
(b/'results/entry-processes.json').write_text(json.dumps(results,indent=2)+'\n');assert all(x['exit_code']==0 for x in results)
