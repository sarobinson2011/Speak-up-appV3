"""Fixture-only commands; no RPC, keys or project accounting access."""
from fixtures import *
import argparse
p=argparse.ArgumentParser();p.add_argument('action',choices=['init','prepare','submit-simulated','reconcile-success-simulated','status','repair','backup']);p.add_argument('--directory',required=True);p.add_argument('--request');p.add_argument('--output');a=p.parse_args()
with Bridge(a.directory,config(),a.action=='init') as b:
 if a.action=='init':r={'result':'LAB-INITIALIZED','actual_admission':False}
 elif a.action=='prepare':
  b.retire('LAB-U-1',intent(config()));b.seal_conditional('LAB-U-1');b.prepare('LAB-U-1',*envelope(b));r={'result':'LAB-PREPARED','actual_admission':False}
 elif a.action=='submit-simulated':r=b.submit('LAB-U-1',a.request,t.OfflineTransport())
 elif a.action=='reconcile-success-simulated':
  sim=t.OfflineTransport();sim.outcome=outcome(b);r=b.reconcile('LAB-U-1',a.request,sim)
 elif a.action=='status':r=b.status(a.request)
 elif a.action=='backup':r=b.backup(a.output,a.request)
 else:
  b.internal_terminal_repair()
  raise SystemExit(0) # internal repair emits no observation or status payload
 print(json.dumps(r,sort_keys=True))
