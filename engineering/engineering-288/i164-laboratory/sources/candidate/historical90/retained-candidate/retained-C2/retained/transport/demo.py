"""Reproducible lab-only crash/recovery CLI demonstration; fresh directory required."""
from pathlib import Path
import subprocess,sys,json
p=Path(__file__).resolve().parent
job=Path(sys.argv[1]).resolve();assert job.name.startswith('LAB-TRANSPORT-') and not job.exists()
records=[]
for action,extra,expected in [('init',[],0),('prepare',[],0),('send',['--request','attempt-1','--mode','ack_loss'],2),('status',['--request','query-1'],0),('send',['--request','attempt-2'],2),('reconcile',['--request','query-2','--outcome','success'],0),('backup',['--request','snapshot-1'],0),('status',['--request','query-3'],0),('reconcile',['--request','query-4'],0)]:
 args=[sys.executable,'-B',str(p/'lab_cli.py'),action,'--job',str(job),*extra];r=subprocess.run(args,capture_output=True,text=True,timeout=10)
 assert r.returncode==expected,(args,r.stdout,r.stderr)
 records.append({'action':action,'arguments':extra,'exit_code':r.returncode,'result':json.loads(r.stdout)})
print(json.dumps(records,indent=2))
