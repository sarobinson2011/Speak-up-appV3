"""One bounded child; exact incremental chunks, live heartbeat, explicit exit, no retry."""
from pathlib import Path
import sys,subprocess,selectors,os,time,json,datetime,signal,hashlib
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 out=Path(sys.argv[1]);limit=float(sys.argv[2]);cmd=sys.argv[3:];out.mkdir(parents=True,exist_ok=False)
 for n in ('stdout','stderr'):(out/(n+'-chunks')).mkdir();(out/(n+'.log')).write_bytes(b'')
 (out/'launch.json').write_bytes(enc({'command':cmd,'started_utc':now(),'timeout_seconds':limit,'automatic_retries':0,'NEW_REPLACEMENT_ATTEMPT':True}))
 start=time.monotonic();last=0;timed=False;p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);sel=selectors.DefaultSelector();chunks={'stdout':[],'stderr':[]};failure=None
 (out/'process.json').write_bytes(enc({'pid':p.pid,'supervisor':os.getpid(),'utc':now()}))
 for name,f in (('stdout',p.stdout),('stderr',p.stderr)):os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,name)
 try:
  while sel.get_map() or p.poll() is None:
   elapsed=time.monotonic()-start
   if elapsed>=limit and not timed:timed=True;os.killpg(p.pid,signal.SIGTERM)
   if timed and elapsed>=limit+15 and p.poll() is None:os.killpg(p.pid,signal.SIGKILL)
   for key,_ in sel.select(timeout=1):
    b=os.read(key.fileobj.fileno(),65536);name=key.data
    if not b:sel.unregister(key.fileobj);key.fileobj.close();continue
    f=out/(name+'-chunks')/(str(len(chunks[name])+1).zfill(6)+'.bin')
    with f.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
    chunks[name].append({'path':f.relative_to(out).as_posix(),'identity':ident(b)})
    with (out/(name+'.log')).open('ab') as h:h.write(b);h.flush();os.fsync(h.fileno())
    stream=sys.stdout if name=='stdout' else sys.stderr;stream.buffer.write(b);stream.buffer.flush()
   if elapsed-last>=15:
    v={'utc':now(),'seconds':elapsed,'pid':p.pid,'stdout_bytes':sum(x['identity']['bytes'] for x in chunks['stdout']),'stderr_bytes':sum(x['identity']['bytes'] for x in chunks['stderr'])}
    with (out/'heartbeat.jsonl').open('ab') as h:h.write((json.dumps(v)+'\n').encode());h.flush();os.fsync(h.fileno())
    print('HEARTBEAT '+json.dumps(v),flush=True);last=elapsed
  rc=p.wait(timeout=10)
 except BaseException as e:
  failure={'type':type(e).__name__,'message':str(e)}
  if p.poll() is None:os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=15)
  raise
 finally:
  streams={}
  for name,parts in chunks.items():
   raw=b''.join((out/x['path']).read_bytes() for x in parts)
   for x in parts:assert ident((out/x['path']).read_bytes())==x['identity']
   streams[name]=ident(raw);(out/(name+'-captured.bin')).write_bytes(raw)
  (out/'capture.json').write_bytes(enc({'chunks':chunks,'streams':streams,'new_capture_only':True,'old_missing_records_reconstructed':False}))
  result={'utc':now(),'seconds':time.monotonic()-start,'exit':p.poll(),'timed_out':timed,'failure':failure,'streams':streams,'automatic_retries':0};(out/'exit.json').write_bytes(enc(result));print('EXIT '+json.dumps(result),flush=True)
 return rc
if __name__=='__main__':sys.exit(main())
