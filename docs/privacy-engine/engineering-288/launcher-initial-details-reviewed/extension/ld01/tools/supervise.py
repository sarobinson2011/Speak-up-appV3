"""One bounded process, incremental heartbeat and explicit exit; no retry."""
from pathlib import Path
import datetime,json,os,subprocess,sys,time
T=Path(__file__).resolve().parents[1];name=sys.argv[1];limit=int(sys.argv[2]);program=Path(sys.argv[3]);root=Path(sys.argv[4]);out=T/'results'/name;attempt=T/'processes'/name;attempt.mkdir(parents=True,exist_ok=False)
cmd=[sys.executable,'-I','-B',str(program),str(root),str(out),*sys.argv[5:]]
def save(n,v):(attempt/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
save('launch.json',{'command':cmd,'root':str(root),'limit_seconds':limit,'retries':0,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
start=time.monotonic();timedout=False
with (attempt/'stdout.log').open('xb') as stdout,(attempt/'stderr.log').open('xb') as stderr:
 p=subprocess.Popen(cmd,stdout=stdout,stderr=stderr);save('process.json',{'pid':p.pid,'supervisor_pid':os.getpid()});print(name,'PID',p.pid,flush=True)
 while p.poll() is None:
  if time.monotonic()-start>limit:timedout=True;p.terminate();break
  try:p.wait(timeout=min(30,max(1,limit-(time.monotonic()-start))))
  except subprocess.TimeoutExpired:
   v={'seconds':round(time.monotonic()-start,1),'pid':p.pid,'running':True}
   with (attempt/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush()
   print(name,'running',v['seconds'],'seconds; no retry',flush=True)
 if p.poll() is None:
  try:p.wait(timeout=10)
  except subprocess.TimeoutExpired:p.kill();p.wait()
save('exit-status.json',{'returncode':p.returncode,'timed_out':timedout,'seconds':time.monotonic()-start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retries':0})
print(name,'EXIT',p.returncode,'TIMEOUT',timedout,flush=True);sys.exit(p.returncode if p.returncode else (1 if timedout else 0))
