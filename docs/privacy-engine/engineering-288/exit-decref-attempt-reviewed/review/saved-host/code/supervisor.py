"""Persistent record writer for ONE child. No retries and no terminal dependency."""
from pathlib import Path
import os,sys,time,json,datetime,hashlib,subprocess,selectors,signal,traceback
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def syncdir(p):
 fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def save(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.partial')
 with q.open('xb') as f:f.write(enc(value));f.flush();os.fsync(f.fileno())
 q.replace(p);syncdir(p.parent)
def append(p,b):
 with Path(p).open('ab') as f:f.write(b);f.flush();os.fsync(f.fileno())
def process_identity(pid):
 try:
  s=Path('/proc/'+str(pid)+'/stat').read_text();start=s[s.rfind(')')+2:].split()[19]
  return {'pid':pid,'proc_start_ticks':start,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
 except OSError:return {'pid':pid,'proc_start_ticks':None,'boot_id':None}
def run(out,limit,command,scope):
 out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False);signal.signal(signal.SIGHUP,signal.SIG_IGN)
 state={'termination_requested':None};signal.signal(signal.SIGTERM,lambda s,f:state.update(termination_requested='supervisor-SIGTERM'))
 start=time.monotonic();p=None;failure=None;timed=False;term_at=None;kill_sent=False;last_hb=start;chunks={'stdout':[],'stderr':[]};buffers={'stdout':b'','stderr':b''};phase_count=0
 for n in chunks:(out/(n+'-chunks')).mkdir();(out/(n+'.log')).touch(exist_ok=False)
 save(out/'launch.json',{'started_utc':now(),'command':command,'cwd':str(Path.cwd()),'scope':scope,'supervisor_identity':process_identity(os.getpid()),'hard_seconds':limit,'automatic_retries':0,'terminal_independent_stdio':True,'SIGHUP':'ignored','validation_pass_claim':False})
 sel=selectors.DefaultSelector()
 try:
  p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,close_fds=True)
  save(out/'process.json',{'utc':now(),'child':process_identity(p.pid),'supervisor':process_identity(os.getpid())})
  for n,f in [('stdout',p.stdout),('stderr',p.stderr)]:os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,n)
  exit_seen=None
  while sel.get_map() or p.poll() is None:
   clock=time.monotonic();elapsed=clock-start
   if elapsed>=limit:timed=True
   if (timed or state['termination_requested']) and term_at is None:
    term_at=clock;append(out/'supervisor-events.jsonl',(json.dumps({'utc':now(),'event':'owned-child-SIGTERM','reason':'deadline' if timed else state['termination_requested']})+'\n').encode())
    try:os.killpg(p.pid,signal.SIGTERM)
    except ProcessLookupError:pass
   if term_at is not None and clock-term_at>=15 and not kill_sent:
    kill_sent=True
    try:os.killpg(p.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   for key,_ in sel.select(timeout=.2):
    b=os.read(key.fileobj.fileno(),65536);n=key.data
    if not b:sel.unregister(key.fileobj);key.fileobj.close();continue
    q=out/(n+'-chunks')/(str(len(chunks[n])+1).zfill(6)+'.bin')
    with q.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    syncdir(q.parent);entry={'sequence':len(chunks[n])+1,'utc':now(),'path':q.relative_to(out).as_posix(),'identity':ident(b)};chunks[n].append(entry)
    append(out/(n+'.log'),b);append(out/'chunk-index.jsonl',(json.dumps({'stream':n,**entry})+'\n').encode())
    buffers[n]+=b
    while b'\n' in buffers[n]:
     line,buffers[n]=buffers[n].split(b'\n',1)
     if n=='stdout' and line.startswith(b'EVENT '):
      try:event=json.loads(line[6:])
      except (ValueError,UnicodeDecodeError):continue
      if event.get('event') in ('computation-progress','dummy-computation-phase','actual-authenticated-basis-returned','public-validator-entered','public-validator-departed','focused-case-start'):
       phase_count+=1;append(out/'computation-phases.jsonl',(json.dumps(event)+'\n').encode())
   if p.poll() is not None:
    if exit_seen is None:exit_seen=clock
    if sel.get_map() and clock-exit_seen>30:raise RuntimeError('PIPE-DRAIN-INCOMPLETE-AFTER-CHILD-EXIT')
   if clock-last_hb>=15:
    append(out/'heartbeat.jsonl',(json.dumps({'utc':now(),'seconds':elapsed,'child_poll':p.poll(),'stdout_bytes':sum(x['identity']['bytes'] for x in chunks['stdout']),'recorded_computation_events':phase_count,'heartbeat_is_not_computation':True})+'\n').encode());last_hb=clock
  p.wait(timeout=2)
 except BaseException as e:
  failure={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()}
  if p is not None and p.poll() is None:
   try:os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=15)
   except subprocess.TimeoutExpired:
    os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
 finally:
  streams={}
  for n,parts in chunks.items():
   h=hashlib.sha256();size=0
   with (out/(n+'-captured.bin')).open('xb') as f:
    for x in parts:
     b=(out/x['path']).read_bytes()
     if ident(b)!=x['identity']:raise RuntimeError('CAPTURE-CHUNK-ALTERED')
     f.write(b);h.update(b);size+=len(b)
    f.flush();os.fsync(f.fileno())
   streams[n]={'bytes':size,'sha256':h.hexdigest()}
  save(out/'capture.json',{'chunks':chunks,'streams':streams,'unparsed_tail_bytes':{n:len(b) for n,b in buffers.items()},'recorded_computation_events':phase_count})
  save(out/'exit.json',{'finished_utc':now(),'seconds':time.monotonic()-start,'child_exit':p.poll() if p is not None else None,'child_identity':process_identity(p.pid) if p is not None and p.poll() is None else None,'timed_out':timed,'termination_requested':state['termination_requested'],'kill_sent':kill_sent,'supervisor_failure':failure,'streams':streams,'automatic_retries':0,'scope':scope,'outcome_requires_result_reconciliation':True})
 return 1 if failure or timed or state['termination_requested'] or p is None else p.returncode
if __name__=='__main__':raise SystemExit(run(sys.argv[1],float(sys.argv[2]),sys.argv[4:],sys.argv[3]))
