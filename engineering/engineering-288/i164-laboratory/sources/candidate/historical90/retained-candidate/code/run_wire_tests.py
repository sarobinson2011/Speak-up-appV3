import sys,subprocess,time,resource,json
from pathlib import Path
start=time.monotonic()
def limits():
 resource.setrlimit(resource.RLIMIT_AS,(1073741824,1073741824));resource.setrlimit(resource.RLIMIT_CPU,(50,50))
p=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(Path(__file__).resolve().parent),'-p','test_wire.py','-v'],capture_output=True,text=True,timeout=60,preexec_fn=limits)
print(p.stdout,end='');print(p.stderr,end='');print(json.dumps({'result':'PASS' if p.returncode==0 else 'FAIL','seconds':time.monotonic()-start,'parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'wall_limit':60,'address_space_limit':1073741824,'network_used':False,'actual_admission':False}));sys.exit(p.returncode)
