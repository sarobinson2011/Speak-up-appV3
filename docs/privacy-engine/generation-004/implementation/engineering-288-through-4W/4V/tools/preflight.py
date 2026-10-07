#!/usr/bin/env python3
"""Read-only host/package preflight. No job creation or full-stream computation."""
import argparse,json,os,platform,resource,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from adapter.core import sha,MODEL,CONTRACT,DESC,check_file,runtime

def host(target):
 errors=[];target=Path(target).expanduser().absolute();probe=target
 while not probe.exists():probe=probe.parent
 st=os.statvfs(probe);disk=st.f_bavail*st.f_frsize
 mem={}
 for line in Path('/proc/meminfo').read_text().splitlines():
  k,_,v=line.partition(':')
  if k in ('MemAvailable','MemTotal'):mem[k]=int(v.split()[0])*1024
 caps=[]
 # cgroup v2 ceilings of this process and ancestors (not file mode or timestamps).
 try:
  cg=next(x.split(':',2)[2] for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0::'))
  p=Path('/sys/fs/cgroup')/cg.lstrip('/')
  while p==Path('/sys/fs/cgroup') or Path('/sys/fs/cgroup') in p.parents:
   if (p/'memory.max').exists():
    mx=(p/'memory.max').read_text().strip()
    if mx!='max':caps.append(max(0,int(mx)-int((p/'memory.current').read_text())))
   if p==Path('/sys/fs/cgroup'):break
   p=p.parent
 except (OSError,StopIteration,ValueError):pass
 effective=min([mem.get('MemAvailable',0)]+caps)
 if sys.version_info<(3,11):errors.append('Python >=3.11 required')
 if platform.system()!='Linux' or platform.machine() not in ['x86_64','amd64']:errors.append('built native kit requires Linux x86_64; reviewed rebuild/new identity otherwise')
 if effective<4*1024**3:errors.append('effective available RAM below 4 GiB preflight reserve')
 # Includes fresh package+extraction, separate pinned inputs, job + backup+restore,
 # 256 MiB bounded rotating logs and >1 GiB working margin. No retained TSV.
 if disk<2*1024**3:errors.append('free task disk below 2 GiB conservative requirement')
 if st.f_favail<256:errors.append('fewer than 256 free inodes')
 native=[]
 for name in ['emitter_service','validator_service']:
  try:
   cp=subprocess.run([str(ROOT/'native'/name),'--selftest'],capture_output=True,text=True,timeout=10)
   if cp.returncode:errors.append(name+' native selftest failed')
   native.append({'name':name,'returncode':cp.returncode,'result':cp.stdout.strip(),'sha256':sha(ROOT/'native'/name)})
  except Exception as e:errors.append(name+': '+str(e))
 try:libs=runtime()
 except Exception as e:libs={};errors.append(str(e))
 return {'result':'PASS-HOST-PREFLIGHT' if not errors else 'BLOCKED','target':str(target),'python':platform.python_version(),'platform':platform.platform(),'available_memory':mem,'cgroup_headroom_bytes':caps,'effective_available_bytes':effective,'free_disk_bytes':disk,'free_inodes':st.f_favail,'required_available_memory_bytes':4*1024**3,'initial_RAM_planning_ceiling_bytes':8*1024**3,'required_free_disk_bytes':2*1024**3,'native':native,'library_sha256':libs,'compiler':shutil.which('g++'),'errors':errors,'writes_performed':False,'full_execution_started':False,'actual_admission':False,'limitations':'Read-only host check does not prove fsync durability or future capacity. Throughput must be measured separately on this host; cloud timings are not local timings.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--target',required=True);a=p.parse_args();r=host(a.target);print(json.dumps(r,indent=2));sys.exit(bool(r['errors']))
