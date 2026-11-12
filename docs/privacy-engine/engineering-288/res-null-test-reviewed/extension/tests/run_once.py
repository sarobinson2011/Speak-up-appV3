"""Bounded single source-check child. No retry. Output lives outside source root."""
import hashlib,json,os,selectors,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve();OUT.mkdir(parents=True,exist_ok=False)
def utc():return datetime.now(timezone.utc).isoformat()
def save(name,x):
 with open(OUT/name,'x') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
deadline=600;started=time.monotonic();cmd=[sys.executable,'-I','-B','-u',str(ROOT/'tests/focused.py'),str(OUT/'raw')]
save('launch.json',{'utc':utc(),'command':cmd,'deadline_seconds':deadline,'deadline_basis':'one new pure-source pass over 48 constructed class/fast-branch combinations from 24 retained variants / eight histories; 600-second hard bound reserves headroom for new pointer-test relations, exact source context checks and larger nested projections; no long public path; no public recursion, instrumentation or application execution','python':sys.version,'source_root':str(ROOT),'source_checkpoint':os.environ.get('I164_SOURCE_CHECKPOINT'),'source_sha256':os.environ.get('I164_SOURCE_SHA256'),'one_attempt':True})
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);save('child.json',{'pid':p.pid,'utc':utc()});sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'stdout');sel.register(p.stderr,selectors.EVENT_READ,'stderr');(OUT/'chunks').mkdir();seq=0;timedout=False
streams={k:open(OUT/(k+'.log'),'xb') for k in ('stdout','stderr')}
try:
 while sel.get_map():
  if time.monotonic()-started>deadline and p.poll() is None:
   timedout=True;p.kill()
  for key,_ in sel.select(0.25):
   data=os.read(key.fileobj.fileno(),65536)
   if not data:sel.unregister(key.fileobj);continue
   seq+=1;path=OUT/'chunks'/('%05d-%s.bin'%(seq,key.data));path.write_bytes(data)
   streams[key.data].write(data);streams[key.data].flush();os.fsync(streams[key.data].fileno())
   save('chunks/%05d.json'%seq,{'utc':utc(),'stream':key.data,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'path':str(path.relative_to(OUT))})
  # No heartbeat is claimed as computation. Durable check rows are the progress.
 rc=p.wait()
finally:
 for f in streams.values():f.close()
save('exit.json',{'utc':utc(),'returncode':rc,'timed_out':timedout,'seconds':time.monotonic()-started,'captured_chunks':seq,'automatic_retry':False})
print(json.dumps({'exit':rc,'timed_out':timedout,'records':str(OUT)}),flush=True)
sys.exit(rc if rc>=0 else 1)
