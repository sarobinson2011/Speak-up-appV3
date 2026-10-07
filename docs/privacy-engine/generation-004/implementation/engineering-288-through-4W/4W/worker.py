import json,os,resource,signal,subprocess,sys,time,shutil,hashlib
from pathlib import Path
from superlib import *
class GuardedService(core.Service):
 def __init__(self,args):
  self.buf=b'';parent=os.getpid()
  self.p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=lambda:death(parent,True))
  try:self.ready=self.read(55);need(self.ready.get('ready') is True,'worker readiness')
  except BaseException:self.close();raise
core.Service=GuardedService

def initialized(t,key,c):
 final=t/'data';tmp=t/'initializing.tmp'
 if final.exists():need(not tmp.exists(),'unexpected unpublished initialization alongside data');return
 if tmp.exists():
  # No validator ever runs in the unpublished directory. No committed progress exists.
  shutil.rmtree(tmp)
 core.initialize(tmp,t/'execution.key',c['manifest'],c['spool_cap'])
 i=read(tmp/'IDENTITY.json',key);s=read(tmp/'STATE.json',key);need(s['offset']==0 and s['validator_state']=='-','initialization is not zero-state')
 i['job_path']=str(final);s['identity_sha256']=hashlib.sha256(core.wire(i)).hexdigest();save(tmp/'IDENTITY.json',i,key);save(tmp/'STATE.json',s,key);core.fsyncdir(tmp);os.replace(tmp,final);core.fsyncdir(t)
def emit(x):print(json.dumps(x,separators=(',',':')),flush=True)
def main():
 t,key,c=config(sys.argv[1]);need(c['implementation']==binding(),'supervisor/code/runtime incompatibility');finish_restore(t,key)
 emit({'stage':'BOUND-INPUT-INITIALIZATION'});initialized(t,key,c)
 with core.Job(t/'data',t/'execution.key') as j:
  emit({'ready':True,'offset':j.state['offset']})
  for line in sys.stdin:
   need(line=='STEP\n','worker command')
   if c['test_delay']:time.sleep(c['test_delay'])
   r=j.step();emit({'result':r,'sequence':j.state['sequence'],'offset':j.state['offset'],'ready_indexes':j.ready,'metrics':j.state['metrics'],'native_pids':[x.p.pid for x in [j.emitter,j.validator] if x]})
   if r['result']!='PAUSED':return
if __name__=='__main__':
 def pause(*_):raise core.Interrupted('graceful pause requested')
 signal.signal(signal.SIGTERM,pause);signal.signal(signal.SIGINT,pause)
 try:main()
 except core.Interrupted:emit({'paused':True})
 except BaseException as e:emit({'error':type(e).__name__+': '+str(e)});sys.exit(2)
