"""Reviewer byte integrity/recovery utilities; no candidate imports or execution."""
import gzip,hashlib,json,os,stat,tarfile,zipfile
from pathlib import Path,PurePosixPath
B=Path(__file__).resolve().parent

def ident(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def fid(path):
 h=hashlib.sha256();n=0
 with Path(path).open('rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):h.update(data);n+=len(data)
 return {'bytes':n,'sha256':h.hexdigest()}
def read(p):return json.loads(Path(p).read_bytes())
def save(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
def safe(n):
 assert type(n) is str and n and not n.startswith('/') and '\\' not in n and '\x00' not in n and ':' not in n.split('/')[0]
 assert all(x not in ('','.','..') for x in n.split('/')),n
 return n
def write_members(files,dest):
 dest.mkdir(parents=True,exist_ok=False)
 for n,b in files.items():
  p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('xb') as f:f.write(b)
def unzip(p,dest,pin=None):
 if pin is not None:assert fid(p)==pin
 files={}
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for item in z.infolist():
   n=safe(item.filename);assert n not in files and not item.is_dir() and not item.flag_bits&1 and stat.S_IFMT(item.external_attr>>16) in (0,stat.S_IFREG),n
   files[n]=z.read(item)
 manifest=json.loads(files['MANIFEST.json']);assert set(files)==set(manifest)|{'MANIFEST.json'}
 for n,pin in manifest.items():assert ident(files[n])==pin,n
 write_members(files,dest)
 return {'identity':fid(p),'entries':len(files),'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership':'PASS','members':{n:ident(v) for n,v in files.items()}}
def untar(p,dest,pin):
 assert fid(p)==pin
 total=0
 with gzip.open(p,'rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):total+=len(data)
 files={}
 with tarfile.open(p,'r:gz') as t:
  for item in t.getmembers():
   n=safe(item.name);assert n not in files and item.isfile(),(n,item.type)
   files[n]=t.extractfile(item).read()
 assert len(files)==637
 manifest=json.loads(files['EXPORT-MANIFEST.json']);assert len(manifest)==635 and set(files)==set(manifest)|{'EXPORT-MANIFEST.json','EXPORT-STATUS.json'}
 for n,pin in manifest.items():assert ident(files[n])==pin,n
 prep=json.loads(files['MANIFEST.json'])
 for n,pin in prep.items():assert n in files and ident(files[n])==pin,n
 write_members(files,dest)
 return {'identity':fid(p),'entries':len(files),'manifested_hashes':len(manifest),'preparation_pins':len(prep),'gzip_integrity':'PASS','uncompressed_bytes':total,'safe_exact_membership':'PASS','all_members_regular':True,'members':{n:ident(v) for n,v in files.items()}}
def tree(root,manifest):
 got={};dirs=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):dirs.add(n);walk(q)
   else:assert stat.S_ISREG(mode),n;got[n]=fid(q)
 walk(root);assert got==manifest,(set(got)^set(manifest))
 assert dirs=={str(p) for n in manifest for p in PurePosixPath(n).parents if str(p)!='.'}
 return {'files':len(got),'directories':len(dirs),'exact_types_membership_hashes':'PASS'}
if __name__=='__main__':
 try:
  host=untar(B/'inputs/I164-enter-return-res-public-1-host-evidence.tar.gz',B/'host',{'bytes':10112583,'sha256':'bcd694478e38d06777112a45b6d2ea1e20f251bddf35de30cd634c4c47ca7155'})
  save(B/'host-archive-audit.json',host)
  prior=unzip(B/'inputs/I164-enter-call-attempt-1-independent-review.zip',B/'prior-review',{'bytes':8272994,'sha256':'381bc024997b4c7c136dbb1c656a5dd3ababcb4fefa40dcc04d055334a261995'})
  save(B/'prior-review-archive-audit.json',prior)
  save(B/'initial-archive.exit.json',{'exit':0,'failure':None})
  print({k:host[k] for k in ('identity','entries','manifested_hashes','preparation_pins','gzip_integrity','safe_exact_membership')},flush=True)
 except BaseException as e:save(B/'initial-archive.exit.json',{'exit':1,'failure':repr(e)});raise
