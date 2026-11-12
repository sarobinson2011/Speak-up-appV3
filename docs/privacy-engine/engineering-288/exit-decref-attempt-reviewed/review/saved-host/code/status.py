"""Read-only status of the one selected attempt. No start, stop, retry or file writes."""
from pathlib import Path
import json,subprocess,sys,datetime
WORK=Path('/srv/Engineering-288-execution/steve/I164-exit-decref-attempt-public-1-20261112')
UNIT='i164-exit-decref-attempt-public-1-20261112.service'
def read(name):
 p=WORK/name
 if not p.exists():return None
 try:return json.loads(p.read_bytes())
 except (OSError,ValueError):return {'unreadable_or_partial':str(p)}
def service():
 try:
  r=subprocess.run(['systemctl','--user','show',UNIT,'--property=LoadState,ActiveState,SubState,MainPID,Result,ExecMainCode,ExecMainStatus'],capture_output=True,text=True,timeout=10)
  return {'query_exit':r.returncode,**dict(x.split('=',1) for x in r.stdout.splitlines() if '=' in x)}
 except (OSError,subprocess.TimeoutExpired) as e:return {'query_error':str(e)}
def alive(identity):
 if not identity or not all(identity.get(k) is not None for k in ('pid','proc_start_ticks','boot_id')):return None
 try:
  s=Path('/proc/'+str(identity['pid'])+'/stat').read_text();ticks=s[s.rfind(')')+2:].split()[19]
  boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
  return ticks==identity['proc_start_ticks'] and boot==identity['boot_id']
 except FileNotFoundError:return False
 except OSError:return None
def inspect():
 state=service();plan=read('PLAN.json');result=read('validation/results/RESULT.json');ex=read('validation/process/exit.json');recon=read('validation/RECONCILIATION.json');wrapper=read('service-exit.json');manager=read('manager-exit.json');proc=read('validation/process/process.json')
 child_alive=alive(proc.get('child')) if proc else None
 events=[];partial=False;p=WORK/'validation/results/events.jsonl'
 if p.is_file():
  for line in p.read_bytes().splitlines():
   try:events.append(json.loads(line))
   except ValueError:partial=True
 progress=[e for e in events if e.get('event')=='computation-progress'];latest=progress[-1] if progress else None
 advancing=False
 if len(progress)>1:
  prev=progress[-2];age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(latest['utc'])).total_seconds()
  advancing=0<=age<=60 and any(latest.get(k,0)>prev.get(k,0) for k in ('entered','returned','abrupt_or_None_qualified'))
 running=state.get('ActiveState') in ('active','activating','deactivating') or child_alive is True
 agree=bool(plan and result and ex and recon and wrapper and manager and result.get('result')=='PASS' and result.get('attempt')==recon.get('attempt')==plan.get('attempt') and result.get('public_result',{}).get('receipt')==recon.get('expected_receipt')==plan.get('expected_receipt') and result.get('exit_decref_public_call_count')==1 and result.get('actual_returned_basis_captured') is True and result.get('new_authenticated_constructed_call_count')==0 and result.get('receipt_agreements')=={'exit_decref':True,'res_null':True,'fast':True,'decref':True,'return':True,'enter':True,'lookup':True,'r1':True,'helper':True} and result.get('thin_wrapper_calls')=={'res_null':0,'fast':0,'decref':0,'return':0,'enter':0,'lookup':0,'R1':0,'helper':0} and ex.get('child_exit')==0 and ex.get('timed_out') is False and ex.get('supervisor_failure') is None and recon.get('status')=='PASS' and wrapper.get('exit')==0 and manager.get('SERVICE_RESULT')=='success' and manager.get('EXIT_CODE')=='exited' and manager.get('EXIT_STATUS')=='0')
 failed=bool((ex and (ex.get('child_exit') not in (None,0) or ex.get('timed_out') is True or ex.get('supervisor_failure'))) or (result and result.get('result')=='FAILED-ATTEMPT') or (wrapper and wrapper.get('exit') not in (None,0)))
 if running:status='RUNNING AND PROGRESSING' if advancing else 'RUNNING WITH NO VERIFIED RECENT PROGRESS'
 elif agree and state.get('ActiveState') in ('inactive','failed') and child_alive is False:status='COMPLETED — saved records agree'
 elif failed:status='FAILED — preserve this attempt; no retry'
 elif not WORK.exists():status='NOT STARTED — workspace absent'
 else:status='UNKNOWN — final records or process evidence do not establish completion'
 return {'status':status,'service':state,'original_child_alive':child_alive,'latest_verified_computation':latest,'latest_event':events[-1] if events else None,'partial_event_record':partial,'public_result':result.get('result') if result else None,'child_exit':ex,'service_exit':wrapper,'manager_observation':manager,'records':str(WORK/'validation')}
if __name__=='__main__':print(json.dumps(inspect(),sort_keys=True,indent=2))
