"""Normal service release -> exact offline sink -> pinned isolated Engine.
No network sender. Synthetic NEAR wrapper/finality are labelled, not Engine observations.
"""
from pathlib import Path
import json,sys,subprocess,time,resource,os,copy,fcntl
from anchor import *
from carrier_fixture import Fixture
import runtime,connected,outcome,stages
P=Path(__file__).resolve().parents[1];OLD=P.parent/'Engineering-288B-I164-signing-cleanup-execution'
BIN=P/'bin/i164-aurora-stages'
def save(p,x):
 t=p.with_suffix('.tmp');t.write_bytes(enc(x))
 with t.open('rb') as f:os.fsync(f.fileno())
 os.replace(t,p)
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(256*1024**3,)*2);resource.setrlimit(resource.RLIMIT_CPU,(45,)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(512*1024**2,)*2)
def run(idx):
 q=P/'runs'/str(idx);full=parse((q/'records/full.json').read_bytes(),2**24);rows=full['cases'][0]['transactions'];state=q/'results/state-0.json';ledger=q/'results/connected.json'
 r=parse(ledger.read_bytes(),2**24) if ledger.exists() else {'format':'CONNECTED-ENGINE-1','full_sha256':sha((q/'records/full.json').read_bytes()),'rows':[],'complete':False,'actual_admission':False}
 need(r['full_sha256']==sha((q/'records/full.json').read_bytes()),'INPUT-MUTATION')
 f=Fixture(q/'stores',parse((q/'records/prerequisites.json').read_bytes(),MAX_INTENT),False)
 started=time.monotonic()
 def engine(end,release=None):
  need(time.monotonic()-started<600,'HARNESS-TIME')
  key=str(idx)+':'+str(end);budget_path=P/'results/execution-budget.json';budget=parse(budget_path.read_bytes(),2**24) if budget_path.exists() else {'charged_seconds':0,'attempts':[]}
  need(not any(a['key']==key for a in budget['attempts']),'UNCERTAIN-ENGINE-ATTEMPT-NO-AUTOMATIC-REEXECUTION')
  need(budget['charged_seconds']+50<=180,'ENGINE-BUDGET')
  if state.exists():need(sha(state.read_bytes())==r['rows'][-1]['state_sha256'],'STATE-SUBSTITUTION')
  selected=copy.deepcopy(full);selected['cases'][0]['transactions']=rows[:end];(q/'records/probes.json').write_bytes(enc(selected))
  attempt={'key':key,'reserved_seconds':50,'release':release,'selected_sha256':sha(enc(selected))};budget['charged_seconds']+=50;budget['attempts'].append(attempt);save(budget_path,budget)
  t=time.monotonic();cp=subprocess.run([str(BIN),str(q),'0',str(10**15),'45'],capture_output=True,timeout=50,preexec_fn=limits)
  elapsed=time.monotonic()-t;(q/'results'/f'execution-{end}.jsonl').write_bytes(cp.stdout);(q/'results'/f'execution-{end}.stderr').write_bytes(cp.stderr)
  attempt.update(seconds=elapsed,exit_code=cp.returncode,child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);budget['charged_seconds']+=elapsed-50;save(budget_path,budget)
  need(cp.returncode==0,'ENGINE-FAILURE-PRESERVED');lines=[json.loads(l) for l in cp.stdout.splitlines()];last=lines[-1];need(json.loads(state.read_bytes())['next']==end,'ENGINE-NEXT')
  # Raw Engine submit result, not fabricated EVM status.
  raw=bytes.fromhex(last['return_bytes']);d=outcome.engine_result(raw);need(d['evm_outcome']=='SUCCESS','ACTUAL-EVM-FAILURE-PRESERVED')
  if rows[end-1]['stage'] in ['registry-signing','cleanup']:(q/'results'/('state-after-'+rows[end-1]['stage']+'.json')).write_bytes(state.read_bytes())
  entry={'end':end,'stage':rows[end-1]['stage'],'execution':last,'decoded':d,'state_sha256':sha(state.read_bytes()),'release':release};r['rows'].append(entry);save(ledger,r)
  return raw
 try:
  if r['complete']:
   f.x.recover();print(json.dumps({'case':idx,'result':'REUSED-COMPLETED-EXACT-JOB','actual_admission':False}));return
  start=int(f.pre['ethereum_carrier']['stage_start_nonce'])
  if not r['rows']:engine(start)
  # A completed Engine transaction may precede interruption before laboratory observation.
  # Reuse exact saved execution; never transmit or run it again.
  last=r['rows'][-1]
  if last.get('release') and 'accounted_head_after_result' not in last:
   need(sha(state.read_bytes())==last['state_sha256'],'RECOVERY-STATE-BINDING')
   raw=bytes.fromhex(last['execution']['return_bytes']);s=f.s.fresh();v=s['u'][f.u]
   if last['stage']=='registry-signing':
    need(v['record']['tx_ref']==last['release']['evm_sha256'],'RECOVERY-SIGNING-BINDING')
    if v['saved'] is None:f.x.save_outcome_evidence(f.u,'observe',f.packet(raw))
    f.x.internal_terminal_repair()
   else:
    pending=v['stage']['pending'];need(pending is not None and pending['evm']==last['release']['evm_sha256'] and pending['near']==last['release']['near_sha256'],'RECOVERY-STAGE-BINDING')
    f.stage_result(raw)
   last['accounted_head_after_result']=f.s.fresh()['head'];last['recovered_saved_execution_without_send']=True;save(ledger,r)
  end=r['rows'][-1]['end']
  for j in range(end,len(rows)):
   row=rows[j];evm=bytes.fromhex(row['signed_transaction']);spec,near=f.near(evm,j+1)
   if row['stage']=='registry-signing':
    f.x.seal_conditional(f.u,'seal');f.x.bind_near_conditional(f.u,'bind-near',spec,near);f.x.submit_conditional(f.u,'signing-attempt',f.sink)
   else:
    if row['stage']=='cleanup':f.sch.advance(f.u,'STAGE_CLEANUP_READY')
    f.sch.prepare(f.u,spec,near,evm);f.sch.send(f.u,f.sink)
   need(f.sink.sent[-1]==near,'SINK-BYTES');need(runtime.retained.t.exact_near(spec,evm,near)==sha(near[:-65]),'SUBMITTED-EXACT-BYTES')
   s=f.s.fresh();v=s['u'][f.u];release={'head':s['head'],'attempt_count':s['counts']['attempt'],'near_sha256':sha(near),'evm_sha256':sha(evm),'intent':v['intent'],'stage':row['stage']}
   (q/'results'/f'submission-{j}.near').write_bytes(near);save(q/'results'/f'submission-{j}.json',{'spec':spec,'release':release,'signed_evm_hex':evm.hex()})
   raw=engine(j+1,release)
   if row['stage']=='registry-signing':
    # Close both clients after actual signing but before result recording. No new send on recovery.
    before=connected.copy_counts(f.s.fresh());f.close();f=Fixture(q/'stores',parse((q/'records/prerequisites.json').read_bytes(),MAX_INTENT),False);f.x.recover();need(connected.copy_counts(f.s.fresh())==before,'RECOVERY-COUNTERS')
    try:f.x.submit_conditional(f.u,'forbidden-second-release',f.sink)
    except ValueError:pass
    else:raise AssertionError('SECOND-RELEASE')
    packet=f.packet(raw);save(q/'results/signing-local-lab-packet.json',packet);f.x.save_outcome_evidence(f.u,'observe',packet);before=connected.copy_counts(f.s.fresh());f.x.internal_terminal_repair();f.x.internal_terminal_repair();need(before==connected.copy_counts(f.s.fresh()),'C1-CONSERVATION')
   else:f.stage_result(raw)
   r['rows'][-1]['accounted_head_after_result']=f.s.fresh()['head'];save(ledger,r)
  s=f.s.fresh();need(s['u'][f.u]['stage']['status']=='COMPLETE' and s['u'][f.u]['record']['status']=='SUCCESS','TERMINAL-CORRESPONDENCE')
  before=connected.copy_counts(s)
  for action in [lambda:f.sch.send(f.u,f.sink),lambda:f.sch.advance(f.u,'STAGE_CLEANUP_READY'),lambda:f.x.submit_conditional(f.u,'replay',f.sink),lambda:f.x.operational_submit()]:
   try:action()
   except ValueError:pass
   else:raise AssertionError('REPLAY')
  f.x.recover();f.x.internal_terminal_repair();need(before==connected.copy_counts(f.s.fresh()),'REPLAY-ALLOWANCES')
  r.update(complete=True,counts=s['counts'],partitions=s['partitions'],recovery_no_second_release=True,normal_authenticated_ingress=True,genuine_C4=False,operational_admission=False,final_head=s['head']);save(ledger,r);print(json.dumps({'case':idx,'result':'PASS-CONDITIONAL-CONNECTED-SIGNED-CARRIER','counts':s['counts'],'actual_admission':False}),flush=True)
 finally:f.close()
if __name__=='__main__':
 lock=(P/'results/execution.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 for i in map(int,sys.argv[1:] or ['0','1']):run(i)
