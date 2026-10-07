"""Detached parent + separate prepaid-deadline watchdog, with no stream semantics."""
import select
from superlib import *

def watchdog(task,pidfd):
 t,key,c=config(task)
 while True:
  if select.select([pidfd],[],[],0)[0]:return
  try:
   b=budget(t,key,c);lease=b['lease'];valid=lease and lease['boot_id']==boot() and now()<lease['deadline_ns']
  except BaseException:valid=False
  if not valid:
   killfd(pidfd);return
  time.sleep(.1)

def run(task,lockfd,lease_id):
 # lockfd inherited from launcher: there is no launch race window.
 t,key,c=config(task);need(lockfd>=0,'inherited lock required');worker=None;guard=None;pidfd=None;b=None;terminal='FAILED';detail=None;stop=False;stop_at=None;last_progress=0;pending=b'';busy=False
 def requested(*_):
  nonlocal stop;stop=True
 signal.signal(signal.SIGTERM,requested);signal.signal(signal.SIGINT,requested)
 try:
  b=budget(t,key,c);need(b['lease'] and b['lease']['id']==lease_id and b['lease']['boot_id']==boot(),'launch reservation mismatch');(t/'WORKERS.json').unlink(missing_ok=True)
  need(c['implementation']==binding(),'code/backend/runtime changed');need(now()<b['lease']['deadline_ns'],'initialization reservation expired before worker launch')
  worker=spawn([sys.executable,'-B',str(ROOT/'worker.py'),str(t)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,start_new_session=True)
  pidfd=os.pidfd_open(worker.pid)
  guard=spawn([sys.executable,'-B',str(ROOT/'supervisor.py'),'watch',str(t),str(pidfd)],pass_fds=(pidfd,),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
  save(t/'RUNNING.json',{'supervisor_pid':os.getpid(),'worker_pid':worker.pid,'watchdog_pid':guard.pid,'attempt_id':b['lease']['id'],'boot_id':boot()},key)
  log(t,{'event':'START','attempt':b['attempts'],'charged_or_reserved_seconds':b['charged_ns']/NS})
  while True:
   ts=now()
   if (t/'PAUSE.json').exists():
    pause=read(t/'PAUSE.json',key);need(pause['nonce']==c['nonce'],'pause substitution');stop=True
   if guard.poll() is not None and worker.poll() is None:
    killfd(pidfd);terminal='BUDGET-EXHAUSTED' if ts>=b['lease']['deadline_ns'] else 'WATCHDOG-STOP';detail='watchdog terminated or prepaid deadline expired';break
   if ts>=b['lease']['deadline_ns']:
    killfd(pidfd);terminal='BUDGET-EXHAUSTED';break
   if not stop and b['lease']['deadline_ns']-ts<min(3*NS,max(1,c['quantum_ns']//3)):
    renew(t,key,c,b)
   if stop and stop_at is None:
    
    if terminal not in ('COMPLETE','SEMANTIC-REJECTED','WORKER-FAILED'):killfd(pidfd,signal.SIGTERM);terminal='PAUSED'
    stop_at=ts
   if stop_at is not None and ts-stop_at>5*NS:
    killfd(pidfd)
    if terminal=='PAUSED':terminal='PAUSED-FORCED-AFTER-GRACE'
   if ts-last_progress>=15*NS:
    progress=status(t,key,c);save(t/'PROGRESS.json',progress,key);log(t,{'event':'PROGRESS',**progress});last_progress=ts
   ready=select.select([worker.stdout],[],[],.1)[0]
   if ready:
    data=os.read(worker.stdout.fileno(),8192)
    if data:
     pending+=data;need(len(pending)<=core.PIPE_LIMIT,'worker response cap')
     while b'\n' in pending:
      line,pending=pending.split(b'\n',1);v=json.loads(line)
      if 'error' in v:terminal='WORKER-FAILED';detail=v['error'];stop=True
      elif v.get('paused'):terminal='PAUSED';stop=True
      elif v.get('ready') or 'result' in v:
       busy=False
       if 'native_pids' in v and v['native_pids'] and not (t/'WORKERS.json').exists():save(t/'WORKERS.json',{'lease_id':b['lease']['id'],'native_pids':v['native_pids']},key)
       if 'result' in v:
        if v['result']['complete']:terminal='COMPLETE';stop=True
        elif v['result']['result']=='REJECTED':terminal='SEMANTIC-REJECTED';detail=v['result']['failure'];stop=True
       if not stop:
        worker.stdin.write(b'STEP\n');worker.stdin.flush();busy=True
    elif worker.poll() is not None:break
   if worker.poll() is not None:break
  if terminal=='FAILED':terminal='WORKER-FAILED';detail='worker ended without a completion/paused result'
 except BaseException as e:
  terminal=('BUDGET-EXHAUSTED' if b and b.get('lease') and now()>=b['lease']['deadline_ns'] else 'WORKER-FAILED') if isinstance(e,BrokenPipeError) else 'SUPERVISOR-FAILED';detail=type(e).__name__+': '+str(e)
 finally:
  if pidfd is not None:killfd(pidfd)
  if worker:
   try:worker.wait(timeout=5)
   except subprocess.TimeoutExpired:terminal='CLEANUP-BLOCKED';detail='kernel did not complete worker termination within 5 seconds'
   for pipe in [worker.stdin,worker.stdout]:
    try:pipe.close()
    except OSError:pass
  if guard:
   guard.terminate()
   try:guard.wait(timeout=2)
   except subprocess.TimeoutExpired:guard.kill();guard.wait()
  if pidfd is not None:os.close(pidfd)
  if b is not None:
   # Same attempt only; invalid on-disk budget is never overwritten or repaired silently.
   try:
    disk=budget(t,key,c);need(disk['sequence']==b['sequence'] and disk['lease']==b['lease'],'budget changed during supervision')
    settle(t,key,b,terminal,detail);save(t/'PROGRESS.json',status(t,key,c),key);log(t,{'event':'STOP','status':terminal,'detail':detail,'charged_seconds':b['charged_ns']/NS,'observed_stop_overrun_seconds':b['observed_stop_overrun_ns']/NS})
   except BaseException as e:log(t,{'event':'BUDGET-INTEGRITY-FAILURE','detail':str(e)})
  os.close(lockfd)
if __name__=='__main__':
 if sys.argv[1]=='watch':watchdog(sys.argv[2],int(sys.argv[3]))
 else:run(sys.argv[2],int(sys.argv[3]),sys.argv[4])
