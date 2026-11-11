from bytes_only import *
import subprocess,sys,time,datetime
cmd=[sys.executable,'-I','-B','-u',str(B/'independent_controls_completion.py')]
save(B/'independent-completion-launch.json',{'command':cmd,'timeout_seconds':240,'automatic_retry':False,'scope':'new independent pure-source/model only; no public or application execution','script':fid(B/'independent_controls_completion.py'),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
t=time.monotonic();timeout=False
with (B/'independent-completion.stdout').open('xb') as so,(B/'independent-completion.stderr').open('xb') as se:
 try:rc=subprocess.run(cmd,stdout=so,stderr=se,timeout=240).returncode
 except subprocess.TimeoutExpired:rc=None;timeout=True
save(B/'independent-completion-exit.json',{'exit':rc,'timeout':timeout,'seconds':time.monotonic()-t,'automatic_retry':False,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps(read(B/'independent-completion-exit.json')),flush=True)
