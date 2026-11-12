"""One reserved bounded batch; never retries."""
import hashlib,json,os,selectors,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent;bid=sys.argv[1]
spec=next(x for x in json.loads((H/'BATCH-PLAN.json').read_bytes())['batches'] if x['id']==bid)
OUT=P/'batches'/bid;OUT.mkdir(parents=True,exist_ok=False)
def utc():return datetime.now(timezone.utc).isoformat()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):
 with open(OUT/n,'x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
manifest=json.loads((H/'HARNESS-MANIFEST.json').read_bytes())
for n,pin in manifest.items():assert identity((H/n).read_bytes())==pin,n
deadline=spec['deadline_seconds'];started=time.monotonic();cmd=[sys.executable,'-I','-B','-u',str(H/'continue_batch.py'),bid]
save('launch.json',{'utc':utc(),'batch':bid,'command':cmd,'deadline_seconds':deadline,'deadline_basis':spec['basis'],'original_sequences':spec['sequences'],'python':sys.version,'harness_manifest':identity((H/'HARNESS-MANIFEST.json').read_bytes()),'source_zip':{'bytes':3779700,'sha256':'280bf68065066e3da79f86ef85d68ea7f03a98e93ec02b078077a63eb1507667'},'automatic_retries':0})
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);save('child.json',{'pid':p.pid,'utc':utc()});sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'stdout');sel.register(p.stderr,selectors.EVENT_READ,'stderr');(OUT/'chunks').mkdir();seq=0;timedout=False
streams={k:open(OUT/(k+'.log'),'xb') for k in ('stdout','stderr')}
try:
 while sel.get_map():
  if time.monotonic()-started>deadline and p.poll() is None:timedout=True;p.kill()
  for key,_ in sel.select(0.25):
   b=os.read(key.fileobj.fileno(),65536)
   if not b:sel.unregister(key.fileobj);continue
   seq+=1;path='chunks/%05d-%s.bin'%(seq,key.data)
   with open(OUT/path,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
   streams[key.data].write(b);streams[key.data].flush();os.fsync(streams[key.data].fileno())
   save('chunks/%05d.json'%seq,{'utc':utc(),'stream':key.data,'path':path,**identity(b)})
 rc=p.wait()
finally:
 for f in streams.values():f.close()
save('exit.json',{'utc':utc(),'returncode':rc,'timed_out':timedout,'seconds':time.monotonic()-started,'captured_chunks':seq,'automatic_retry':False})
print(json.dumps({'batch':bid,'exit':rc,'timed_out':timedout,'records':str(OUT)}),flush=True);sys.exit(rc if rc>=0 else 1)
