#!/usr/bin/env python3
import argparse,threading
from superlib import *
def launch(t,key,c):
 lock=Lock(t/'CONTROL.LOCK')
 try:
  b=budget(t,key,c)
  if (t/'data/STATE.json').exists() and read(t/'data/STATE.json',key)['status']=='PASS-CONDITIONAL-BYTE-VALIDATION':return {'result':'ALREADY-COMPLETE','actual_admission':False}
  need(b['authorized_ns']>b['charged_ns'],'aggregate budget exhausted; add an explicit grant')
  # Corrupt checkpoints are checked before starting any work; absence is only initial state.
  if (t/'data').exists():read(t/'data/IDENTITY.json',key);read(t/'data/STATE.json',key)
  (t/'PAUSE.json').unlink(missing_ok=True)
  reserved=reserve(t,key,c) # Durable prepayment includes daemon bootstrap and all initialization.
  p=subprocess.Popen([sys.executable,'-B',str(ROOT/'supervisor.py'),'run',str(t),str(lock.fd),reserved['lease']['id']],pass_fds=(lock.fd,),stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
  threading.Thread(target=p.wait,daemon=True).start()
  return {'result':'DETACHED-SUPERVISOR-LAUNCHED','pid':p.pid,'task':str(t),'log':str(t/'progress.log'),'note':'Launch is not completion. Terminal closure does not stop the detached supervisor.','actual_admission':False}
 finally:lock.close()
def verify_completion(t,key,c):
 need(c['implementation']==binding(),'completion supervisor/code/runtime identity mismatch')
 with core.Job(t/'data',t/'execution.key') as j:
  s=j.state;r=s['result'];m=c['manifest'];need(j.identity['manifest']==m,'source binding');need(s['status']=='PASS-CONDITIONAL-BYTE-VALIDATION' and r['complete'] and r['eof_observed'],'not complete');need(s['offset']==m['expected']['bytes'] and r['whole_stream_sha256']==m['expected']['sha256'],'whole byte identity')
  # Rebuild the exact descriptor index only; never replay stream bytes.
  j.services('validate');idx=j.validator.ready;need(r['structural']==idx['structural'] and r['potential']==idx['potential'] and r['rows']==idx['structural']+idx['potential'],'separate semantic completeness')
  return {'result':'VERIFIED-CONDITIONAL-INDEPENDENT-ROW-VALIDATION','rows':r['rows'],'structural':r['structural'],'potential':r['potential'],'serialized_bytes':r['offset'],'whole_stream_sha256':r['whole_stream_sha256'],'model_sha256':m['model']['sha256'],'contract_sha256':m['contract']['sha256'],'descriptor_sha256':m['descriptor']['sha256'],'source_kind':m['source']['kind'],'trust':'MAC-protected trusted local execution state; not source authentication','actual_admission':False,'qualification_established':False,'four_file_authentication_complete':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['init','run','resume','status','pause','stop','grant','backup','restore','verify','settle']);p.add_argument('--task',required=True);p.add_argument('--manifest');p.add_argument('--spool-mib',type=int,default=64);p.add_argument('--authorize-review-hours',type=float);p.add_argument('--grant-id');p.add_argument('--archive');a=p.parse_args();t=Path(a.task).resolve()
 if a.command=='init':need(a.manifest,'manifest required');create(t,core.load_json(a.manifest),a.spool_mib*1048576);return {'result':'INITIALIZED-NOT-STARTED','actual_admission':False}
 t,key,c=config(t)
 if a.command=='status':return status(t,key,c)
 if a.command in ('pause','stop'):
  save(t/'PAUSE.json',{'nonce':c['nonce'],'requested':a.command},key);return {'result':'PAUSE-REQUESTED','note':'Check status until running=false. No progress or budget reset.','actual_admission':False}
 if a.command=='resume':return launch(t,key,c)
 if a.command=='run':
  with Lock(t/'CONTROL.LOCK'):
   b=budget(t,key,c);need(b['authorized_ns']==0,'initial authorization already exists; use resume');need(a.authorize_review_hours and a.authorize_review_hours>0,'explicit initial hours required');grant(t,key,c,a.authorize_review_hours*3600,'initial-review')
  return launch(t,key,c)
 with Lock(t/'CONTROL.LOCK'):
  if a.command=='settle':
   b=budget(t,key,c)
   if b['lease'] is not None:b['lease']=None;b['status']='UNCERTAIN-ATTEMPT-FULLY-CHARGED';bsave(t,key,b)
   finish_restore(t,key);return status(t,key,c)
  if a.command=='grant':need(a.authorize_review_hours and a.grant_id,'explicit hours and unique grant id required');grant(t,key,c,a.authorize_review_hours*3600,a.grant_id);return status(t,key,c)
  if a.command=='backup':return backup(t,key,c)
  if a.command=='restore':need(a.archive,'backup archive required');return restore(t,key,c,a.archive)
  if a.command=='verify':return verify_completion(t,key,c)
if __name__=='__main__':
 try:print(json.dumps(main(),indent=2))
 except BaseException as e:print(json.dumps({'result':'REJECTED-OR-BLOCKED','detail':str(e),'actual_admission':False}));sys.exit(2)
