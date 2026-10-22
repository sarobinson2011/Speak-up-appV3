"""Minimal D1 reproduction with real process death and preserved state cuts."""
import sys,os,json,subprocess,hashlib,time,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'code'))
from fixtures import *
out=R/'results/D1-final-repaired';out.mkdir(exist_ok=False);job=out/'job'
c=config()
def capture(label):
 d=out/label;d.mkdir()
 for n in ['executor.db','transport.db','independent-anchor.db']:shutil.copyfile(job/n,d/n)
with Bridge(job,c,True) as b:
 b.backup(out/'legitimate-old-backup.zip','backup-before-retirement')
capture('before-retirement')
script="from fixtures import *;import os,sys;b=Bridge(sys.argv[1],config());\ntry:b.retire('LAB-U-1',intent(config()),'after_executor')\nexcept RuntimeError:os._exit(77)"
env=dict(os.environ,PYTHONPATH=str(R/'code'),PYTHONDONTWRITEBYTECODE='1')
p=subprocess.run([sys.executable,'-B','-c',script,str(job)],env=env,capture_output=True,timeout=10)
(out/'child.stdout').write_bytes(p.stdout);(out/'child.stderr').write_bytes(p.stderr);assert p.returncode==77,p.stderr
capture('committed-with-pending-anchor')
with zipfile.ZipFile(out/'legitimate-old-backup.zip') as z:(job/'executor.db').write_bytes(z.read('executor.db'))
capture('only-executor-restored')
for n in ['transport.db','independent-anchor.db']:
 assert (out/'committed-with-pending-anchor'/n).read_bytes()==(out/'only-executor-restored'/n).read_bytes()
start=time.monotonic()
with Bridge(job,c) as b:
 recover_seconds=time.monotonic()-start;assert b.executor.states['LAB-U-1']['intent_sha256']==e.sha(e.enc(intent(c)))
 changed=intent(c);changed['registry']='3'*40
 try:b.retire('LAB-U-1',changed)
 except ValueError:pass
 else:raise AssertionError('changed U reused')
 b.seal_conditional('LAB-U-1');b.prepare('LAB-U-1',*envelope(b));sim=t.OfflineTransport();b.submit('LAB-U-1','a',sim)
 try:b.submit('LAB-U-1','retry',sim)
 except ValueError:pass
 else:raise AssertionError('second submission')
 assert sim.calls==1 and b.transport.counts['attempt']==1
 result={'verdict':'REPAIR-VERIFIED','child_exit':77,'only_executor_restored':True,'anchor_and_transport_not_restored':True,'same_U_changed_intent_accepted':False,'exact_same_intent_resumed_once':True,'reopen_seconds':recover_seconds,'backup_charge_retained':b.transport.counts['snapshot'],'actual_admission':False}
capture('after-U-reuse')
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
