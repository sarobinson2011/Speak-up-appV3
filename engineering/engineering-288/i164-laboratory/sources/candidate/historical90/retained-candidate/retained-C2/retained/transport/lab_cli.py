"""Local laboratory recovery commands. No networking, production keys or accounts."""
import argparse,json,sys,os
from pathlib import Path
from transport import *
from fixtures import config,make,outcome
p=argparse.ArgumentParser();p.add_argument('action',choices=['init','prepare','send','reconcile','status','repair','backup']);p.add_argument('--job',required=True);p.add_argument('--request');p.add_argument('--mode',choices=['ack','ack_loss','reject','timeout_before','wrong_hash'],default='ack');p.add_argument('--outcome',choices=['pending','success','reverted','failure'],default='pending');p.add_argument('--crash',choices=['before_charge','after_charge','after_send','after_lookup']);a=p.parse_args()
j=Path(a.job).resolve();s=None
try:
 need(j.name.startswith('LAB-TRANSPORT-'),'LAB-JOB-PATH-REQUIRED')
 if a.action=='init':
  j.mkdir(exist_ok=False);c=config();(j/'config.json').write_bytes(enc(c));fsyncdir(j)
 else:need(j.is_dir(),'MISSING-JOB');c=parse((j/'config.json').read_bytes())
 s=Session(j/'job.db',j/'anchor.db',c,a.action=='init');t=OfflineTransport();t.mode=a.mode;u='LAB-U-1'
 result={'action':a.action,'actual_admission':False,'source':'LABORATORY-ONLY'}
 if a.action=='prepare':result['txid']=s.prepare(*make(c))
 if a.action=='send':result.update(s.submit(u,a.request,t,a.crash))
 if a.action=='reconcile':
  if a.outcome!='pending':t.outcome=outcome(s,near='FAILURE' if a.outcome=='failure' else 'SUCCESS',evm={'success':'SUCCESS','reverted':'REVERTED','failure':'NOT-EXECUTED'}[a.outcome])
  result.update(s.reconcile(u,a.request,t,a.crash))
 if a.action=='status':
  result['receipt']=s.charge('query',u,a.request);result.update(status=s.states[u]['status'],counts=s.counts,staging=s.staging,head=s.head)
 if a.action=='backup':result.update(s.backup(j/('backup-'+str(a.request)+'.db'),a.request))
 if a.action=='repair':s.internal_repair();result={'result':'INTERNAL-INTEGRITY-CHECK-ONLY','observation_returned':False,'actual_admission':False}
 print(json.dumps(result,sort_keys=True))
except Exception as e:print(json.dumps({'result':'BLOCKED-OR-FROZEN','error':str(e),'actual_admission':False}));sys.exit(2)
finally:
 if s:s.close()
