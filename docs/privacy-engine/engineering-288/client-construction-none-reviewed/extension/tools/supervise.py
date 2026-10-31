"""Finite single-launch supervisor; records attempts and exits without retry."""
from pathlib import Path
import datetime,json,os,subprocess,sys,time
task=Path(__file__).resolve().parents[1];name=sys.argv[1];root=Path(sys.argv[2]);script=sys.argv[3];mode=sys.argv[4:];out=task/'results'/name
attempt=task/'processes'/name;attempt.mkdir(parents=True,exist_ok=False)
cmd=[sys.executable,'-I','-B',str(root/'tests'/script),str(root),str(out),*mode]
def save(n,v):(attempt/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
save('launch.json',{'command':cmd,'root':str(root),'timeout_seconds':3600,'retries':0,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
start=time.monotonic();timedout=False
with (attempt/'stdout.log').open('xb') as stdout,(attempt/'stderr.log').open('xb') as stderr:
 p=subprocess.Popen(cmd,stdout=stdout,stderr=stderr);save('process.json',{'pid':p.pid,'supervisor_pid':os.getpid()});print(name,'PID',p.pid,flush=True)
 while p.poll() is None:
  if time.monotonic()-start>3600:timedout=True;p.terminate();break
  try:p.wait(timeout=30)
  except subprocess.TimeoutExpired:
   progress={'seconds':round(time.monotonic()-start,1),'pid':p.pid,'running':True}
   with (attempt/'supervisor-progress.jsonl').open('a') as f:f.write(json.dumps(progress)+'\n')
   print(name,'running',progress['seconds'],'seconds; no retry',flush=True)
 if p.poll() is None:
  try:p.wait(timeout=10)
  except subprocess.TimeoutExpired:p.kill();p.wait()
save('exit-status.json',{'returncode':p.returncode,'timed_out':timedout,'seconds':time.monotonic()-start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retries':0})
print(name,'EXIT',p.returncode,'TIMEOUT',timedout,flush=True)
sys.exit(p.returncode if p.returncode else (1 if timedout else 0))
