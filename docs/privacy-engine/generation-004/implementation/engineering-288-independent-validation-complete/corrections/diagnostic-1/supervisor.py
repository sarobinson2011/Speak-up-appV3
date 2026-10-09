"""Detached parent + separate prepaid-deadline watchdog, with no stream semantics."""
import select,threading
from superlib import *

def watchdog(task,pidfd):
 t,key,c=config(task)
 while True:
  if select.select([pidfd],[],[],0)[0]:return
  observed=now();reason=None;extra={}
  try:
   b=budget(t,key,c);lease=b['lease']
   extra={'budget_sequence':b['sequence'],'authorized_ns':b['authorized_ns'],'charged_ns':b['charged_ns']}
   if not lease:reason='NO-ACTIVE-LEASE'
   elif lease['boot_id']!=boot():reason='BOOT-MISMATCH'
   else:
    observed=now();extra['deadline_ns']=lease['deadline_ns'];extra['observed_ns']=observed
    if observed>=lease['deadline_ns']:reason='PREPAID-LEASE-EXPIRED'
  except BaseException as e:reason='BUDGET-READ-OR-INTEGRITY-ERROR';extra={'error_type':type(e).__name__,'detail':str(e)[:500]}
  if reason:
   print(json.dumps({'event':'WATCHDOG-KILL','reason':reason,**extra}),flush=True)
   killfd(pidfd);return
  time.sleep(.1)

class StderrTail:
 def __init__(self,pipe):
  self.pipe=pipe;self.tail=b'';self.total=0
  self.thread=threading.Thread(target=self.drain,daemon=True);self.thread.start()
 def drain(self):
  try:
   while True:
    data=os.read(self.pipe.fileno(),4096)
    if not data:return
    self.total+=len(data);self.tail=(self.tail+data)[-1024:]
  except (OSError,ValueError):pass
 def result(self):return {'stderr_bytes_observed':self.total,'stderr_tail':self.tail.decode(errors='replace')}

def exit_info(code):
 return {'returncode':code,'signal':signal.Signals(-code).name if code is not None and code<0 else None}

def run(task,lockfd,lease_id):
 # lockfd inherited from launcher: there is no launch race window.
 t,key,c=config(task);need(lockfd>=0,'inherited lock required');worker=None;guard=None;pidfd=None;b=None;terminal='FAILED';detail=None;stop=False;stop_at=None;last_progress=0;pending=b'';busy=False;stderr_tail=None;exit_before_cleanup=None;guard_before_cleanup=None;termination_requested=None
 def requested(*_):
  nonlocal stop;stop=True
 signal.signal(signal.SIGTERM,requested);signal.signal(signal.SIGINT,requested)
 try:
  b=budget(t,key,c);need(b['lease'] and b['lease']['id']==lease_id and b['lease']['boot_id']==boot(),'launch reservation mismatch');(t/'WORKERS.json').unlink(missing_ok=True)
  need(c['implementation']==binding(),'code/backend/runtime changed');need(now()<b['lease']['deadline_ns'],'initialization reservation expired before worker launch')
  worker=spawn([sys.executable,'-B',str(ROOT/'worker.py'),str(t)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
  stderr_tail=StderrTail(worker.stderr)
  pidfd=os.pidfd_open(worker.pid)
  guard=spawn([sys.executable,'-B',str(ROOT/'supervisor.py'),'watch',str(t),str(pidfd)],pass_fds=(pidfd,),stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,start_new_session=True)
  save(t/'RUNNING.json',{'supervisor_pid':os.getpid(),'worker_pid':worker.pid,'watchdog_pid':guard.pid,'attempt_id':b['lease']['id'],'boot_id':boot()},key)
  log(t,{'event':'START','attempt':b['attempts'],'charged_or_reserved_seconds':b['charged_ns']/NS})
  while True:
   ts=now()
   if (t/'PAUSE.json').exists():
    pause=read(t/'PAUSE.json',key);need(pause['nonce']==c['nonce'],'pause substitution');stop=True
   if guard.poll() is not None and worker.poll() is None:
    termination_requested='WATCHDOG-EXIT';killfd(pidfd);terminal='BUDGET-EXHAUSTED' if ts>=b['lease']['deadline_ns'] else 'WATCHDOG-STOP';detail='watchdog terminated or prepaid deadline expired';break
   if ts>=b['lease']['deadline_ns']:
    termination_requested='SUPERVISOR-DEADLINE';killfd(pidfd);terminal='BUDGET-EXHAUSTED';break
   if not stop and b['lease']['deadline_ns']-ts<min(3*NS,max(1,c['quantum_ns']//3)):
    renew(t,key,c,b)
   if stop and stop_at is None:
    
    if terminal not in ('COMPLETE','SEMANTIC-REJECTED','WORKER-FAILED'):termination_requested='REQUESTED-PAUSE';killfd(pidfd,signal.SIGTERM);terminal='PAUSED'
    stop_at=ts
   if stop_at is not None and ts-stop_at>5*NS:
    termination_requested='PAUSE-GRACE-EXPIRED';killfd(pidfd)
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
  exit_before_cleanup=worker.poll() if worker else None
  guard_before_cleanup=guard.poll() if guard else None
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
  if stderr_tail:stderr_tail.thread.join(timeout=.5)
  diagnostics={'event':'EXIT-DIAGNOSTICS','worker_before_cleanup':exit_info(exit_before_cleanup),'worker_after_cleanup':exit_info(worker.returncode if worker else None),'watchdog_before_cleanup':exit_info(guard_before_cleanup),'watchdog_after_cleanup':exit_info(guard.returncode if guard else None),'supervisor_termination_request':termination_requested,**(stderr_tail.result() if stderr_tail else {})}
  if guard and guard.stdout:
   raw=guard.stdout.read(8192);guard.stdout.close()
   diagnostics['watchdog_report_raw']=raw.decode(errors='replace')
   try:
    v=json.loads(raw) if raw else None
    if v and v.get('reason')=='PREPAID-LEASE-EXPIRED' and terminal=='WORKER-FAILED':
     terminal='BUDGET-EXHAUSTED' if b['charged_ns']>=b['authorized_ns'] else 'LEASE-EXPIRED-WITH-BUDGET-REMAINING'
   except (ValueError,KeyError):pass
  if worker and worker.stderr:worker.stderr.close()
  try:log(t,diagnostics)
  except BaseException:pass
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
