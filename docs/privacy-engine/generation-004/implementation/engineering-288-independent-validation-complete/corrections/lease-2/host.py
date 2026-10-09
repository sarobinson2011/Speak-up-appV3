"""Standalone read-only ZIP/installed host preflight; explicit prepare is separate."""
import argparse,hashlib,json,os,platform,signal,subprocess,sys,zipfile,shutil
from pathlib import Path
MODEL='dd946419e4fd4c657a0a0d663b145e958ddf3c4957bf006b94b5c3f7ec96e74d';CONTRACT='2bbd9d52e1591bc12adc9cc0983c1686ade2cfc4cbcbeb95b6025259d5bf07fc';DESC='c79ea7fa8e27de3fb051c50f4f50d52cecb51c3d3e0025c9569b174d27882f5f';TEXT='dc5776088dfc860e25a42e260b245b607969f6c49346bd6912eecc0ef53d8a74'
S='Engineering-288-checkpoint-4S';T='Engineering-288-checkpoint-4T'
EXPECTED={'model':('model.json',382700006,MODEL,S+'/candidate/model.json'),'contract':('selected-contract.json',312547,CONTRACT,S+'/candidate/reused/selected-contract.json'),'descriptor':('links.txt',236894099,DESC,T+'/inputs/links.txt')}
ARCHIVES={'4S':('ae4f7fa4469c1b90345fb05858be3e661ae67265dfab4cdf933d7fb825aacbbf',512084676),'4T':('98a1027a7968da0f940e501a6b0a65eeb4a066a301645c4110a2e637a757fa5f',18540491)}
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def discover(roots):
 candidates=[];archives=[];seen=0
 for root in roots:
  root=Path(root).expanduser()
  if not root.exists():continue
  for d,dirs,files in os.walk(root,followlinks=False):
   dirs[:]=sorted(x for x in dirs if not x.startswith('.') and x!='Speak-up-appV3' and not Path(d,x).is_symlink())
   seen+=1
   if seen>10000:raise ValueError('bounded input discovery exceeded 10000 directories; supply narrower --search-root')
   for name in files:
    if name=='.env' or name.startswith('.'):continue
    p=Path(d,name)
    if p.is_symlink():continue
    if name in [x[0] for x in EXPECTED.values()]:candidates.append(p)
    for stage in ARCHIVES:
     if name.startswith('Engineering-288-checkpoint-'+stage) and name.endswith('.zip'):archives.append((stage,p))
 out={};archive_checked={}
 for kind,(name,size,h,member) in EXPECTED.items():
  for p in candidates:
   if p.name==name and p.stat().st_size==size and sha(p)==h:out[kind]={'kind':'file','path':str(p.resolve()),'bytes':size,'sha256':h};break
  if kind in out:continue
  stage='4T' if kind=='descriptor' else '4S'
  for st,p in archives:
   if st!=stage or p.stat().st_size!=ARCHIVES[st][1]:continue
   if p not in archive_checked:archive_checked[p]=sha(p)==ARCHIVES[st][0]
   if not archive_checked[p]:continue
   with zipfile.ZipFile(p) as z:
    if member not in z.namelist() or z.getinfo(member).file_size!=size:continue
    with z.open(member) as f:found=hashlib.file_digest(f,'sha256').hexdigest()
   if found==h:out[kind]={'kind':'zip-member','path':str(p.resolve()),'archive_sha256':ARCHIVES[st][0],'member':member,'bytes':size,'sha256':h};break
 return out

def package_files(archive=None):
 root=Path(__file__).resolve().parent
 if archive:
  z=zipfile.ZipFile(archive);prefix='Engineering-288-checkpoint-4W/';manifest=json.loads(z.read(prefix+'PACKAGE-MANIFEST.json'));expected={prefix+x['path'] for x in manifest['files']}|{prefix+'PACKAGE-MANIFEST.json'}
  if len(z.namelist())!=len(set(z.namelist())) or set(z.namelist())!=expected:raise ValueError('package ZIP membership')
  for x in manifest['files']:
   with z.open(prefix+x['path']) as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   if h!=x['sha256'] or z.getinfo(prefix+x['path']).file_size!=x['bytes']:raise ValueError('package bytes '+x['path'])
  bins={n:z.read(prefix+'runtime/native/'+n) for n in ['emitter_service','validator_service']};z.close();return manifest,bins
 manifest=json.loads((root/'PACKAGE-MANIFEST.json').read_text())
 for x in manifest['files']:
  p=root/x['path']
  if p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise ValueError('package bytes '+x['path'])
 return manifest,{n:(root/'runtime/native'/n).read_bytes() for n in ['emitter_service','validator_service']}

def native_check(bins):
 results=[];libs={}
 for name,data in bins.items():
  fd=os.memfd_create(name,0)
  try:
   os.write(fd,data);os.fchmod(fd,0o700);path='/proc/self/fd/'+str(fd)
   cp=subprocess.run([path,'--selftest'],pass_fds=(fd,),capture_output=True,text=True,timeout=10)
   if cp.returncode:raise ValueError(name+' compatibility: '+cp.stderr)
   results.append({'name':name,'sha256':hashlib.sha256(data).hexdigest(),'result':json.loads(cp.stdout)})
   dep=subprocess.run(['ldd',path],pass_fds=(fd,),capture_output=True,text=True,timeout=5)
   if dep.returncode or 'not found' in dep.stdout:raise ValueError('native library availability')
   for line in dep.stdout.splitlines():
    for word in line.split():
     if word.startswith('/'):
      p=Path(word).resolve()
      if p.is_file():libs[str(p)]=sha(p)
  finally:os.close(fd)
 return results,libs

def preflight(target,roots,archive=None):
 errors=[];native=[];libs={};inputs={};mem={};caps=[];target=Path(target).expanduser().absolute();p=target
 while not p.exists():p=p.parent
 st=os.statvfs(p)
 if sys.version_info<(3,11) or platform.system()!='Linux' or platform.machine()!='x86_64':errors.append('Python >=3.11, Linux x86_64 required')
 for line in Path('/proc/meminfo').read_text().splitlines():
  k,_,v=line.partition(':')
  if k in ('MemAvailable','MemTotal'):mem[k]=int(v.split()[0])*1024
 try:
  cg=next(x.split(':',2)[2] for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0::'));p=Path('/sys/fs/cgroup')/cg.lstrip('/')
  while p==Path('/sys/fs/cgroup') or Path('/sys/fs/cgroup') in p.parents:
   if (p/'memory.max').exists():
    maximum=(p/'memory.max').read_text().strip()
    if maximum!='max':caps.append(max(0,int(maximum)-int((p/'memory.current').read_text())))
   if p==Path('/sys/fs/cgroup'):break
   p=p.parent
 except (OSError,StopIteration,ValueError):pass
 available=min([mem.get('MemAvailable',0)]+caps)
 if available<4*1024**3:errors.append('effective available memory <4 GiB reserve')
 if st.f_bavail*st.f_frsize<2*1024**3:errors.append('available disk <2 GiB reserve')
 if st.f_favail<256:errors.append('free inodes <256')
 try:fd=os.pidfd_open(os.getpid());signal.pidfd_send_signal(fd,0);os.close(fd);time_clock=__import__('time').CLOCK_BOOTTIME
 except Exception as e:errors.append('pidfd/CLOCK_BOOTTIME unavailable: '+str(e))
 try:m,bins=package_files(archive);native,libs=native_check(bins)
 except Exception as e:errors.append(str(e))
 try:inputs=discover(roots)
 except Exception as e:errors.append(str(e))
 for name in EXPECTED:
  if name not in inputs:errors.append('missing exact '+name+' (retain/retrieve 4S candidate or 4T descriptor; no stream rerun)')
 return {'result':'PASS-HOST-PREFLIGHT' if not errors else 'BLOCKED','target':str(target),'python':platform.python_version(),'platform':platform.platform(),'available_memory':mem,'cgroup_headroom_bytes':caps,'effective_available_bytes':available,'available_disk_bytes':st.f_bavail*st.f_frsize,'required_available_memory_bytes':4*1024**3,'planning_memory_ceiling_bytes':8*1024**3,'required_free_disk_bytes':2*1024**3,'inputs':inputs,'native':native,'library_sha256':libs,'errors':errors,'writes_performed':False,'full_validation_started':False,'actual_admission':False,'limitation':'Read-only checks do not prove power-loss durability, future capacity or external source authenticity.'}

def prepare(out,roots):
 inputs=discover(roots)
 if set(inputs)!=set(EXPECTED):raise ValueError('exact required inputs missing; run preflight')
 out=Path(out).resolve()
 if 'Speak-up-appV3' in out.parts or '.env' in out.parts:raise ValueError('isolated input preparation required')
 out.mkdir(parents=True,exist_ok=True);parentfd=os.open(out.parent,os.O_DIRECTORY);os.fsync(parentfd);os.close(parentfd);entries={}
 for name,x in inputs.items():
  p=out/EXPECTED[name][0]
  if not p.exists():
   tmp=p.with_suffix(p.suffix+'.part')
   if x['kind']=='file':
    with open(x['path'],'rb') as src,tmp.open('wb') as dst:shutil.copyfileobj(src,dst,1048576);dst.flush();os.fsync(dst.fileno())
   else:
    if sha(x['path'])!=x['archive_sha256']:raise ValueError('archive mutation')
    with zipfile.ZipFile(x['path']) as z,z.open(x['member']) as src,tmp.open('wb') as dst:shutil.copyfileobj(src,dst,1048576);dst.flush();os.fsync(dst.fileno())
   if tmp.stat().st_size!=x['bytes'] or sha(tmp)!=x['sha256']:raise ValueError('acquired input byte mismatch')
   os.replace(tmp,p)
  if p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise ValueError('existing prepared input mismatch')
  entries[name]={'path':str(p),'bytes':x['bytes'],'sha256':x['sha256']}
 m={'format':'CP4V-BYTE-SOURCE-1',**entries,'source':{'kind':'deterministic-laboratory-emitter'},'expected':{'bytes':19909380154846,'sha256':TEXT},'serialization':'S90-FCR-S70-STATIC-LINKS-TSV','laboratory_only':True};data=(json.dumps(m,sort_keys=True,separators=(',',':'))+'\n').encode();p=out/'source.json'
 if p.exists() and p.read_bytes()!=data:raise ValueError('existing source manifest differs')
 with p.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 fd=os.open(out,os.O_DIRECTORY);os.fsync(fd);os.close(fd);return {'result':'INPUTS-PREPARED-NOT-STARTED','manifest':str(p),'actual_admission':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['preflight','prepare']);p.add_argument('--target',default='/home/steve/dev/Engineering-288-execution/independent-4W');p.add_argument('--archive');p.add_argument('--out');p.add_argument('--search-root',action='append');a=p.parse_args();roots=a.search_root or ['/home/steve/Downloads','/home/steve/dev/Engineering-288-execution'];r=preflight(a.target,roots,a.archive) if a.command=='preflight' else prepare(a.out,roots);print(json.dumps(r,indent=2));return int(r['result']=='BLOCKED')
if __name__=='__main__':sys.exit(main())
