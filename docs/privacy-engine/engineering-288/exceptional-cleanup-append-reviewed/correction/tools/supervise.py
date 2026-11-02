"""One bounded EC01 validation process, durable incremental streams, no automatic retry."""
from pathlib import Path
import datetime,json,os,selectors,subprocess,sys,time
T=Path(__file__).resolve().parents[1];root=Path(sys.argv[1]).resolve();label=sys.argv[2];a=T/'processes'/label;o=T/'results'/label;a.mkdir(parents=True,exist_ok=False);limit=3600
def save(n,v):
 p=a/n;q=a/(n+'.partial')
 with q.open('xb') as f:f.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
 q.replace(p)
def append(n,b):
 with (a/n).open('ab') as f:f.write(b);f.flush();os.fsync(f.fileno())
cmd=[sys.executable,'-I','-B',str(root/'ec01/tests/focused.py'),str(root),str(o)]
save('launch.json',{'command':cmd,'soft_control_deadline_seconds':3150,'hard_timeout_seconds':limit,'reserved_finalization_seconds':450,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'automatic_retries':0})
start=time.monotonic();p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);save('process.json',{'pid':p.pid,'supervisor_pid':os.getpid()})
sel=selectors.DefaultSelector()
for name,pipe in [('stdout.log',p.stdout),('stderr.log',p.stderr)]:(a/name).touch(exist_ok=False);os.set_blocking(pipe.fileno(),False);sel.register(pipe,selectors.EVENT_READ,name)
last=start;timed=False;streams={'stdout.log':0,'stderr.log':0}
print(label,'started; hard limit 3600s; controls deadline 3150s; finalization reserve 450s',flush=True)
while sel.get_map() or p.poll() is None:
 now=time.monotonic()
 if now-start>=limit and p.poll() is None and not timed:timed=True;p.terminate()
 if timed and now-start>=limit+15 and p.poll() is None:p.kill()
 for key,mask in sel.select(timeout=1):
  b=os.read(key.fileobj.fileno(),65536)
  if b:append(key.data,b);streams[key.data]+=len(b)
  else:sel.unregister(key.fileobj);key.fileobj.close()
 if now-last>=30:
  v={'seconds':round(now-start,1),'running':p.poll() is None,'stdout_bytes_observed':streams['stdout.log'],'stderr_bytes_observed':streams['stderr.log']}
  append('supervisor-progress.jsonl',(json.dumps(v)+'\n').encode());print(label,json.dumps(v),flush=True);last=now
code=p.wait();save('exit-status.json',{'returncode':code,'timed_out':timed,'seconds':time.monotonic()-start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'streams_bytes_observed':streams,'automatic_retries':0})
print(label,'EXIT',code,'TIMEOUT',timed,flush=True);sys.exit(code if code else (1 if timed else 0))
