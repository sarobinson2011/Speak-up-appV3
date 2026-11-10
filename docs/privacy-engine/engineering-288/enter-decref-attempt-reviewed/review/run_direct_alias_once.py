from pathlib import Path
import sys,subprocess,time
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));from bytes_only import save,fid
assert not (B/'direct-alias').exists()
cmd=[sys.executable,'-I','-B',str(B/'direct_alias_controls.py')];save(B/'direct-alias-launch.json',{'command':cmd,'timeout_seconds':60,'reviewer_code':fid(B/'direct_alias_controls.py'),'reason':'actual returned object alias isolation not established by mutation of a deepcopy','no_replay':True})
t=time.monotonic();timeout=False
with (B/'direct-alias.stdout').open('xb') as so,(B/'direct-alias.stderr').open('xb') as se:
 try:rc=subprocess.run(cmd,stdout=so,stderr=se,timeout=60).returncode
 except subprocess.TimeoutExpired:rc=None;timeout=True
save(B/'direct-alias-exit.json',{'returncode':rc,'timed_out':timeout,'no_retry':True,'seconds':time.monotonic()-t,'streams':{s:fid(B/('direct-alias.'+s)) for s in ('stdout','stderr')}})
raise SystemExit(0 if rc==0 and not timeout else 1)
