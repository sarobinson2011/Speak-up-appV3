"""ZIP-based read-only host preflight; optional explicit install-and-run.
Invoked with globals ZIP_PATH and MODE; never reads .env or changes cwd.
"""
import hashlib,json,os,platform,resource,shutil,struct,subprocess,sys,zipfile
from pathlib import Path
PREFIX='Engineering-288-checkpoint-4R/'
TARGET=Path('/home/steve/dev/Engineering-288-execution')
GIB=1024**3

def hash_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def verify_zip(z):
 m=json.loads(z.read(PREFIX+'PACKAGE-MANIFEST.json'));expected={PREFIX+e['path'] for e in m['files']}|{PREFIX+'PACKAGE-MANIFEST.json'}
 if set(z.namelist())!=expected or len(z.namelist())!=len(expected):raise ValueError('archive membership/duplicates')
 for e in m['files']:
  p=Path(e['path'])
  if p.is_absolute() or '..' in p.parts or '.env' in p.parts:raise ValueError('unsafe package path')
  b=z.read(PREFIX+e['path'])
  if (len(b),hashlib.sha256(b).hexdigest())!=(e['bytes'],e['sha256']):raise ValueError('package bytes: '+e['path'])
 return m

def memory_available():
 d={l.split(':')[0]:int(l.split()[1])*1024 for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith(('MemTotal:','MemAvailable:'))};limits=[]
 # Account for cgroup-v2 ancestors, when this runtime is constrained.
 cg=Path('/proc/self/cgroup').read_text().splitlines()
 for line in cg:
  if line.startswith('0::'):
   suffix=line.split('::',1)[1].lstrip('/');p=Path('/sys/fs/cgroup')/suffix
   # Namespaced mounts can expose the current group directly at mount root.
   if not p.exists():p=Path('/sys/fs/cgroup')
   while p.is_relative_to(Path('/sys/fs/cgroup')):
    try:
     limit=(p/'memory.max').read_text().strip();cur=int((p/'memory.current').read_text())
     if limit!='max':limits.append(max(0,int(limit)-cur))
    except FileNotFoundError:pass
    if p==Path('/sys/fs/cgroup'):break
    p=p.parent
  elif ':memory:' in line:
   p=Path('/sys/fs/cgroup/memory')/line.split(':',2)[2].lstrip('/')
   try:limits.append(max(0,int((p/'memory.limit_in_bytes').read_text())-int((p/'memory.usage_in_bytes').read_text())))
   except FileNotFoundError:raise ValueError('cannot determine cgroup-v1 available memory')
 return {**d,'cgroup_headroom_bytes':limits,'effective_available_bytes':min([d['MemAvailable']]+limits)}

def native_probe(binary,descriptor):
 # Linux anonymous RAM files: no extraction, no disk writes, only 6 tiny candidates.
 fds=[]
 try:
  for name,b in [('cp4r-worker',binary),('cp4r-probe',descriptor)]:
   fd=os.memfd_create(name,0);os.write(fd,b);fds.append(fd)
  worker='/proc/self/fd/'+str(fds[0]);desc='/proc/self/fd/'+str(fds[1]);os.fchmod(fds[0],0o500)
  ldd=subprocess.run(['ldd',worker],pass_fds=tuple(fds),capture_output=True,text=True,timeout=10)
  if ldd.returncode or 'not found' in ldd.stdout:raise ValueError('native dynamic dependencies: '+ldd.stdout+ldd.stderr)
  libs={}
  for line in ldd.stdout.splitlines():
   for word in line.split():
    if word.startswith('/'):
     p=Path(word);libs[str(p.resolve())]=hash_file(p)
  if not libs:raise ValueError('native dependency identities unavailable')
  expected=b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n'+b''.join(struct.pack('>II',i,j) for i in range(4) for j in range(i+1,4) if (i,j)!=(0,1))
  rows=[]
  for engine in ('complement','predicate'):
   p=subprocess.run([worker,desc,'0','6','INIT',engine,'2'],pass_fds=tuple(fds),capture_output=True,text=True,timeout=3)
   if p.returncode:raise ValueError('native compatibility: '+p.stderr)
   r=json.loads(p.stdout)
   if r['prefix_sha256']!=hashlib.sha256(expected).hexdigest() or r['rows']!=5:raise ValueError('native exact-byte probe')
   rows.append({'engine':engine,'rows':5,'sha256':r['prefix_sha256']})
  return {'result':'PASS','library_sha256':libs,'bounded_probe':rows}
 finally:
  for fd in fds:os.close(fd)

def preflight(z,target):
 m=verify_zip(z);errors=[]
 def need(test,msg):
  if not test:errors.append(msg)
 need(sys.version_info>=(3,11),'Python 3.11+ required')
 need(platform.system()=='Linux' and platform.machine()=='x86_64','shipped native worker requires Linux x86_64')
 release=Path('/etc/os-release').read_text();need('ID=ubuntu' in release or 'ID="ubuntu"' in release,'intended supported execution target is Ubuntu; other distribution requires review')
 need(hasattr(os,'memfd_create'),'Linux anonymous-executable compatibility probe unavailable')
 need(shutil.which('ldd') is not None,'ldd required for native dependency identity')
 need('Speak-up-appV3' not in target.parts and target.is_absolute(),'isolated absolute task path required')
 # Refuse symlink components: no implicit redirection into a project or another mount.
 for p in [target,*target.parents]:need(not p.is_symlink(),'symlink task path component: '+str(p))
 nearest=target
 while not nearest.exists():nearest=nearest.parent
 need(nearest.is_dir() and os.access(nearest,os.W_OK|os.X_OK),'task parent is not accessible/writable')
 st=os.statvfs(nearest);free=st.f_bavail*st.f_frsize
 need(not(st.f_flag & getattr(os,'ST_NOEXEC',8)),'target mount is noexec')
 need(not(st.f_flag & getattr(os,'ST_RDONLY',1)),'target mount is read-only')
 mem=memory_available();need(mem['effective_available_bytes']>=8*GIB,'less than initial 8 GiB available RAM/headroom')
 soft,_=resource.getrlimit(resource.RLIMIT_AS);need(soft==resource.RLIM_INFINITY or soft>=2*GIB,'address-space limit below 2 GiB supervisor/worker limit')
 storage=m['storage'];need(free>=storage['required_free_bytes'],'insufficient disk: requires '+str(storage['required_free_bytes'])+' free bytes')
 need(st.f_frsize<=storage['filesystem_allocation_unit_max_bytes'],'filesystem allocation unit exceeds costed 4 KiB; storage estimate requires review')
 need(st.f_favail>=storage['required_free_inodes'],'insufficient free inodes')
 native=None
 if platform.system()=='Linux' and platform.machine()=='x86_64' and hasattr(os,'memfd_create') and shutil.which('ldd'):
  try:native=native_probe(z.read(PREFIX+'runner/pairs'),z.read(PREFIX+'inputs/probe.txt'))
  except Exception as e:errors.append(str(e))
 r={'result':'REJECTED' if errors else 'PASS-HOST-PREFLIGHT','target':str(target),'python':sys.version.split()[0],'platform':platform.platform(),'available_memory':mem,'available_disk_bytes':free,'storage_requirements':storage,'native':native,'errors':errors,'writes_performed':False,'full_enumeration_started':False,'actual_admission':False,'limitation':'Read-only checks cannot prove power-loss durability/fsync support or future capacity; user-controlled durable filesystem required.'}
 return r

def main(zip_path,mode,target=TARGET):
 if mode not in ('preflight','install-and-run'):raise ValueError('explicit operation required')
 target=Path(target)
 with zipfile.ZipFile(zip_path) as z:
  r=preflight(z,target);print(json.dumps(r,indent=2),flush=True)
  if r['errors']:return 2
  if mode=='preflight':return 0
  # Writes begin only here, in the explicitly isolated task root.
  target.mkdir(parents=True,exist_ok=True);dest=target/PREFIX.rstrip('/');m=json.loads(z.read(PREFIX+'PACKAGE-MANIFEST.json'))
  for e in m['files']+[{'path':'PACKAGE-MANIFEST.json'}]:
   p=dest/e['path'];b=z.read(PREFIX+e['path'])
   for ancestor in [p,*p.parents]:
    if ancestor==target:break
    if ancestor.is_symlink():raise ValueError('symlink inside installation: '+str(ancestor))
   if p.exists():
    if p.is_symlink() or p.read_bytes()!=b:raise ValueError('refusing substituted existing installation: '+str(p))
   else:
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
  (dest/'runner/pairs').chmod(0o500)
  archive=target/'Engineering-288-checkpoint-4R.zip'
  if archive.exists():
   if hash_file(archive)!=hash_file(zip_path):raise ValueError('existing archive mismatch')
  else:shutil.copyfile(zip_path,archive)
 # Stored hardware receipt is provenance only. Every run rechecks exact native/code identity.
 receipt=target/'host-preflight.json';tmp=receipt.with_suffix('.part');tmp.write_text(json.dumps(r,indent=2)+'\n');os.replace(tmp,receipt)
 return subprocess.call([sys.executable,'-B',str(dest/'run_task.py'),'run','--task',str(target)])

if __name__=='__main__':
 try:raise SystemExit(main(ZIP_PATH,MODE))
 except Exception as e:print('REJECTED:',e,file=sys.stderr);raise SystemExit(2)
