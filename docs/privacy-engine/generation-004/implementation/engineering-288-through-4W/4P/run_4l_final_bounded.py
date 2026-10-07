import subprocess,sys,time,json
from pathlib import Path
start=time.monotonic();rows=[]
for operation in ('construct','validate'):
 p=subprocess.run([sys.executable,'run_4l_large.py',operation],capture_output=True,text=True,timeout=max(.1,59-(time.monotonic()-start)))
 rows.append({'operation':operation,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,rows[-1]
Path('results/4L-final-bounded.json').write_text(json.dumps({'result':'PASS','seconds':time.monotonic()-start,'subprocesses':rows},indent=2)+'\n')
