from pathlib import Path
import sys,json,os,time,subprocess,signal,datetime
base=Path('/workspace/scratch/ace5c9b2f18b');label=sys.argv[1];script=sys.argv[2];limit=int(sys.argv[3]);args=sys.argv[4:]
out=base/'cln-review/processes'/label;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):(out/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def note(**v):
 v={'utc':now(),'seconds':time.monotonic()-start,**v}
 with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
cmd=[sys.executable,'-I','-B','-u',str(base/'cln-review/code'/script),*args];save('launch.json',{'command':cmd,'timeout_seconds':limit,'retries':0})
with (out/'stdout.log').open('xb') as stdout,(out/'stderr.log').open('xb') as stderr:
 p=subprocess.Popen(cmd,stdout=stdout,stderr=stderr,start_new_session=True);save('process.json',{'pid':p.pid,'started_utc':now()});expired=False;note(event='launched',pid=p.pid)
 while p.poll() is None:
  left=limit-(time.monotonic()-start)
  if left<=0:
   expired=True;note(event='timeout');os.killpg(p.pid,signal.SIGTERM)
   try:p.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
   break
  try:p.wait(timeout=min(30,left))
  except subprocess.TimeoutExpired:note(event='running',pid=p.pid)
 save('exit-status.json',{'pid':p.pid,'returncode':p.returncode,'timed_out':expired,'seconds':time.monotonic()-start,'finished_utc':now()});note(event='exited',returncode=p.returncode,timed_out=expired)
sys.exit(124 if expired else (p.returncode if p.returncode>=0 else 1))
