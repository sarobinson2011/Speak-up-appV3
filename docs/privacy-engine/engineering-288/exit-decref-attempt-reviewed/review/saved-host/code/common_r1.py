"""Preparation/service utilities. No candidate or application imports."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile,importlib.util,datetime
HERE=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def identity(path):
 h=hashlib.sha256();size=0
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def load(name):
 s=importlib.util.spec_from_file_location('_r1_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def exact_tree(root,manifest):
 root=Path(root);need(stat.S_ISDIR(root.lstat().st_mode),'ROOT-TYPE')
 files=set(manifest);dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};seenf=set();seend=set()
 def walk(path):
  for e in os.scandir(path):
   p=Path(e.path);n=p.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):need(n in dirs,'UNDECLARED-DIRECTORY:'+n);seend.add(n);walk(p)
   else:need(stat.S_ISREG(mode) and n in files,'UNDECLARED-OR-SPECIAL:'+n);seenf.add(n)
 walk(root);need(seenf==files and seend==dirs,'EXACT-MEMBERSHIP')
 for n,pin in manifest.items():need(identity(root/n)==pin,'STALE-BYTES:'+n)
 return {'files':len(files),'directories':len(dirs),'exact_types_membership_hashes':'PASS'}
def unzip(archive,dest,expected=None):
 if expected:need(identity(archive)==expected,'ARCHIVE-PIN')
 dest=Path(dest);dest.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();need(len(names)==len(set(names)),'ZIP-DUPLICATES');m=json.loads(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'ZIP-MEMBERSHIP')
  for i in z.infolist():
   n=PurePosixPath(i.filename);need(str(n)==i.filename and not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG) and not i.flag_bits&1,'ZIP-ENTRY')
   b=z.read(i.filename)
   if i.filename in m:need({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==m[i.filename],'ZIP-BYTES')
   p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 return m
