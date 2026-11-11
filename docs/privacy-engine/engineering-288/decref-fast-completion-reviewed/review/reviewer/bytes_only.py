"""Reviewer byte-only archive tools; never import candidate code."""
from pathlib import Path,PurePosixPath
import json,hashlib,gzip,tarfile,zipfile,stat,os
B=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_bytes())
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def fid(p):return ident(Path(p).read_bytes())
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def safe(n):
 assert n and not n.startswith('/') and '\\' not in n and '\x00' not in n and ':' not in n.split('/')[0]
 assert all(s not in ('','.','..') for s in n.split('/'));return n
def write(files,dest):
 dest.mkdir(parents=True,exist_ok=False)
 for n,b in files.items():
  p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def unzip(p,dest,pin=None):
 if pin:assert fid(p)==pin
 files={}
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for i in z.infolist():
   n=safe(i.filename);assert n not in files and not i.is_dir() and not i.flag_bits&1 and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG);files[n]=z.read(i)
 m=json.loads(files['MANIFEST.json']);assert set(files)==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert ident(files[n])==pin,n
 write(files,dest);return {'identity':fid(p),'entries':len(files),'manifested_hashes':len(m),'CRC_safe_exact_membership_all_hashes':'PASS'}
def untar(p,dest,pin,entries,hashes):
 assert fid(p)==pin
 with gzip.open(p,'rb') as f:
  while f.read(1048576):pass
 files={}
 with tarfile.open(p,'r:gz') as t:
  for i in t.getmembers():
   n=safe(i.name);assert n not in files and i.isfile();files[n]=t.extractfile(i).read()
 m=json.loads(files['EXPORT-MANIFEST.json']);assert len(files)==entries and len(m)==hashes and set(files)==set(m)|{'EXPORT-MANIFEST.json','EXPORT-STATUS.json'}
 for n,pin in m.items():assert ident(files[n])==pin,n
 prep=json.loads(files['MANIFEST.json'])
 for n,pin in prep.items():assert n in files and ident(files[n])==pin,n
 write(files,dest);return {'identity':fid(p),'entries':len(files),'manifested_hashes':len(m),'preparation_pins':len(prep),'gzip_safe_exact_membership_all_hashes':'PASS','members':{n:ident(v) for n,v in files.items()}}
def tree(root,m):
 found={};dirs=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):dirs.add(n);walk(q)
   else:assert stat.S_ISREG(mode);found[n]=fid(q)
 walk(root);assert found==m;assert dirs=={str(p) for n in m for p in PurePosixPath(n).parents if str(p)!='.'}
 return {'files':len(found),'directories':len(dirs),'exact_types_membership_hashes':'PASS'}
