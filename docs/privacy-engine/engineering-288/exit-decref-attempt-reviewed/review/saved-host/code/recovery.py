"""Byte-only recovery from pinned nested archives. Never imports candidate code."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile, stat, os, shutil
PINS={
 'prerun':{'bytes':203902321,'sha256':'52568dfb3afd650b7addc03a9f98ec4632b680ca8303d75779e8ea81ca784165'},
 'progress':{'bytes':32674,'sha256':'664aaabe5990baf1abb985c13dc7a879a04bc56d8fa8d737df2c0e8836beca0d'}}
HARNESS_PINS={'_event_filter.c': {'bytes': 4936, 'sha256': '7544bb593f45412807e4b98c40b82417ae78d6f3976f66e1adfe0a975293d22a'}, '_event_filter.cpython-312-x86_64-linux-gnu.so': {'bytes': 17240, 'sha256': '36d7f88ac907b39dab2576d3122e6038afc2f7803b5fd6abe7f92e4b7ae29e3f'}, 'common.py': {'bytes': 3910, 'sha256': '86bb554d39e86cbfb8ad52b55a808d6bff08a1b7357b7a760e4ec00ee867543e'}, 'native_observer.py': {'bytes': 3205, 'sha256': '5f2b4b5e05cf513cd012b08e8d59e57cd2d8aa168a6a12020768796739e69151'}, 'observer.py': {'bytes': 5383, 'sha256': 'aef90431e2800350c2c74a3edc6821c8685e750ceef65b2605acdced72b0af4a'}, 'public_checks.py': {'bytes': 11740, 'sha256': 'd5e3df07f91abcd2e4538168969190acec136ae8f8479d9e885010f73f621add'}}
ROOT_PIN={'bytes':1694211,'sha256':'5852ec258fbf3543215754c5fdac3d01d475a0e2bd190da4493b07f1ac91071b'}
def identity(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def file_identity(p):
 h=hashlib.sha256();size=0
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def need(ok,message):
 if not ok:raise RuntimeError(message)
def safe_name(name):
 p=PurePosixPath(name);need(str(p)==name and not p.is_absolute() and '..' not in p.parts and '\\' not in name,'UNSAFE-ARCHIVE-NAME');return p
def unpack_manifest(archive,dest):
 dest=Path(dest);dest.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();need(len(names)==len(set(names)),'DUPLICATE-ARCHIVE-NAME');m=json.loads(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'ARCHIVE-MEMBERSHIP')
  for info in z.infolist():
   n=safe_name(info.filename);need(not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG) and not info.flag_bits&1,'ARCHIVE-TYPE')
   b=z.read(info.filename)
   if info.filename in m:need(identity(b)==m[info.filename],'ARCHIVE-BYTES:'+info.filename)
   p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('xb') as f:f.write(b)
 return m
def verify_harness(path):
 path=Path(path);need(stat.S_ISDIR(path.lstat().st_mode),'HARNESS-ROOT-TYPE');need({p.name for p in path.iterdir()}==set(HARNESS_PINS),'HARNESS-MEMBERSHIP')
 for n,pin in HARNESS_PINS.items():need(stat.S_ISREG((path/n).lstat().st_mode) and file_identity(path/n)==pin,'HARNESS-BYTES:'+n)
 return {'files':len(HARNESS_PINS),'identities':'PASS'}
def verify_root(root):
 root=Path(root);need(stat.S_ISDIR(root.lstat().st_mode),'ROOT-TYPE');need(file_identity(root/'MANIFEST.json')==ROOT_PIN,'ROOT-MANIFEST')
 m=json.loads((root/'MANIFEST.json').read_bytes());files=set(m)|{'MANIFEST.json'};dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};seenf=set();seend=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);name=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):need(name in dirs,'UNDECLARED-DIRECTORY');seend.add(name);walk(q)
   else:need(stat.S_ISREG(mode) and name in files,'UNDECLARED-OR-NONREGULAR');seenf.add(name)
 walk(root);need(seenf==files and seend==dirs,'ROOT-MEMBERSHIP')
 for name,pin in m.items():need(file_identity(root/name)==pin,'ROOT-BYTES:'+name)
 return {'files':len(files),'directories':len(dirs),'manifest':ROOT_PIN,'exact_membership_types_hashes':'PASS'}
def recover(prerun,progress,dest,emit=print):
 dest=Path(dest);dest.mkdir(parents=True,exist_ok=False)
 for name,p in [('prerun',prerun),('progress',progress)]:need(file_identity(p)==PINS[name],'INPUT-IDENTITY:'+name)
 unpack_manifest(prerun,dest/'retained-prerun');unpack_manifest(progress,dest/'retained-progress')
 root=dest/'candidate';root.mkdir();pool=dest/'byte-recovery-archives';pool.mkdir();outer=dest/'retained-prerun/unchanged-input/I164-helper-open-attempt-construction-1.zip'
 with zipfile.ZipFile(outer) as z:
  raw=z.read('construction/I164-helper-open-attempt-prerun-1.zip');pre=pool/'helper-open-prerun.zip';pre.write_bytes(raw)
 with zipfile.ZipFile(pre) as z:manifest=z.read('ROOT-MANIFEST.json')
 need(identity(manifest)==ROOT_PIN,'EXPECTED-ROOT-MANIFEST');expected=json.loads(manifest);wanted={}
 for name,pin in expected.items():safe_name(name);wanted.setdefault((pin['bytes'],pin['sha256']),[]).append(name)
 sizes={k[0] for k in wanted};origins={};visited=set();written=0
 def visit(archive,lineage):
  nonlocal written
  ap=file_identity(archive)
  if ap['sha256'] in visited:return
  visited.add(ap['sha256'])
  with zipfile.ZipFile(archive) as z:
   names=z.namelist();need(len(names)==len(set(names)),'NESTED-DUPLICATES')
   # Extract no unspecified file-system entries. Root paths come ONLY from the exact manifest.
   children=[]
   for info in z.infolist():
    if info.is_dir():continue
    safe_name(info.filename);need(stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG) and not info.flag_bits&1,'NESTED-UNSUPPORTED-ENTRY')
    if info.file_size in sizes:
     b=z.read(info.filename);pin=identity(b);key=(pin['bytes'],pin['sha256'])
     if key in wanted:
      for name in wanted.pop(key):
       p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
       with p.open('xb') as f:f.write(b)
       origins[name]={'archive':ap,'archive_lineage':lineage,'entry':info.filename,'identity':pin};written+=1
      if written%100<20:emit(json.dumps({'phase':'byte-recovery','files_written':written,'files_expected':len(expected)}),flush=True)
    if info.filename.endswith('.zip'):
     temp=pool/('member-'+str(len(list(pool.iterdir())))+'.partial');h=hashlib.sha256()
     with z.open(info) as src,temp.open('xb') as out:
      for b in iter(lambda:src.read(1024*1024),b''):h.update(b);out.write(b)
     child=pool/(h.hexdigest()+'.zip')
     if child.exists():temp.unlink() # duplicate transfer scratch; retained archive remains exact
     else:temp.rename(child)
     children.append((child,lineage+[info.filename]))
   for child,path in children:
    if wanted:visit(child,path)
 visit(pre,['unchanged-input/I164-helper-open-attempt-construction-1.zip','construction/I164-helper-open-attempt-prerun-1.zip'])
 need(not wanted,'MISSING-DECLARED-BYTES:'+str(sum(len(x) for x in wanted.values())))
 (root/'MANIFEST.json').write_bytes(manifest);result=verify_root(root)
 shutil.copytree(dest/'retained-prerun/harness',dest/'harness')
 for name,pin in json.loads((dest/'retained-prerun/CHECKPOINT.json').read_bytes())['changed_harness_identities'].items():need(file_identity(dest/name)==pin,'HARNESS-BYTES:'+name)
 (dest/'byte-origins.json').write_text(json.dumps(origins,sort_keys=True,indent=2)+'\n');(dest/'recovery-result.json').write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':
 import sys
 print(json.dumps(recover(*sys.argv[1:4])),flush=True)
