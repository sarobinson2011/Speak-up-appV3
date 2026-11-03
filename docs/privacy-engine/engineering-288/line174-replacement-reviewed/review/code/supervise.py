"""One bounded process; immutable stream chunks and explicit exit. No retries."""
from pathlib import Path
import os,sys,subprocess,selectors,time,signal,json,datetime,hashlib
base=Path(__file__).resolve().parents[1];label,script,limit=sys.argv[1:4];limit=int(limit);out=base/'processes'/label;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.partial')
 with q.open('xb') as f:f.write((json.dumps(v,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
 q.replace(p)
def note(**kw):
 v={'utc':now(),'seconds':time.monotonic()-start,**kw}
 with (out/'supervisor.jsonl').open('a') as f:f.write(json.dumps(v)+'\n');f.flush();os.fsync(f.fileno())
cmd=[sys.executable,'-I','-B','-u',str(base/'code'/script),*sys.argv[4:]];save('launch.json',{'command':cmd,'timeout_seconds':limit,'retries':0})
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);save('process.json',{'pid':p.pid,'started_utc':now()});note(event='launched',pid=p.pid)
sel=selectors.DefaultSelector();logs={};index=[]
for name,pipe in [('stdout',p.stdout),('stderr',p.stderr)]:sel.register(pipe,selectors.EVENT_READ,name);logs[name]=(out/(name+'.log')).open('xb')
expired=False;last=time.monotonic()
while sel.get_map() or p.poll() is None:
 if time.monotonic()-start>limit and p.poll() is None:
  expired=True;note(event='timeout');os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
 for key,_ in sel.select(timeout=1):
  data=os.read(key.fileobj.fileno(),65536)
  if not data:sel.unregister(key.fileobj);continue
  name=key.data;n='chunks/%06d-%s.bin'%(len(index)+1,name);q=out/n;q.parent.mkdir(exist_ok=True)
  with q.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  logs[name].write(data);logs[name].flush();os.fsync(logs[name].fileno());index.append({'file':n,'stream':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});save('capture.json',index)
 if time.monotonic()-last>=30:note(event='running',pid=p.pid);last=time.monotonic()
for f in logs.values():f.close()
p.wait();save('exit-status.json',{'pid':p.pid,'returncode':p.returncode,'timed_out':expired,'seconds':time.monotonic()-start,'finished_utc':now()});note(event='exited',returncode=p.returncode,timed_out=expired)
sys.exit(124 if expired else (p.returncode if p.returncode>=0 else 1))
