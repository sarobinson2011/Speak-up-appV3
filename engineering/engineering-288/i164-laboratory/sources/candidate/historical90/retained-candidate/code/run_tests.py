"""Focused offline checks only. No network or operational state."""
import subprocess,sys,resource,time,json
from pathlib import Path
root=Path(__file__).resolve().parent
start=time.monotonic()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(1073741824,1073741824))
 resource.setrlimit(resource.RLIMIT_CPU,(25,25))
p=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(root),'-p','test_connected.py','-v'],capture_output=True,text=True,timeout=30,preexec_fn=limits)
print(p.stdout,end='');print(p.stderr,end='')
print(json.dumps({'result':'PASS' if p.returncode==0 else 'FAIL','wall_seconds':time.monotonic()-start,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'wall_budget_seconds':30,'child_address_space_bytes':1073741824,'backend':'OFFLINE-SIMULATION','actual_admission':False}))
sys.exit(p.returncode)
