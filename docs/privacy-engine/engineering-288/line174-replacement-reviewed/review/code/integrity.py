"""Independent byte-only archive/root verification. No candidate imports."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat,os
BASE=Path('/workspace/scratch/ace5c9b2f18b/l174-review')
AREA=Path('/workspace/review-evidence/FL6-line174-20261103')
INPUT=BASE.parent/'upload/I164-line174-NEW-replacement-construction-1(1).zip'
PIN={'bytes':182650504,'sha256':'da1b070d16deadcb9e4ff741f76b370bcf62a2353787bde7ae1a44badd9bc173'}
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def file_ident(p):
 p=Path(p)
 with p.open('rb') as f:return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 assert n and str(PurePosixPath(n))==n and not PurePosixPath(n).is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/'));return n
def archive(path,pin,count):
 assert file_ident(path)==pin,(str(path),file_ident(path),pin)
 z=zipfile.ZipFile(path);names=[safe(i.filename) for i in z.infolist()]
 assert len(names)==len(set(names))==count
 assert not set(names)&{str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
 for i in z.infolist():assert i.orig_filename==i.filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
 m=js(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n,p in m.items():assert ident(z.read(n))==p,n
 assert z.testzip() is None
 return z
def put(root,n,b):
 p=Path(root)/safe(n);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def extract(z,root):
 assert not Path(root).exists()
 for n in z.namelist():put(root,n,z.read(n))
def verify(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode);mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode)
 m=js(mp.read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={str(p) for n in expected for p in PurePosixPath(safe(n)).parents if str(p)!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs
 for n,p in m.items():assert file_ident(root/n)==p,n
 return {'files':len(files),'directories':len(dirs),'manifest':file_ident(mp),'membership_types_hashes':'PASS'}
def additions(z,root,prefix):
 m=js(z.read('ADDITIONS-MANIFEST.json'));assert {n.removeprefix('root-additions/') for n in z.namelist() if n.startswith('root-additions/')}==set(m)
 for n,p in m.items():
  assert not n.startswith('retained/');b=z.read('root-additions/'+safe(n));assert ident(b)==p;put(root,n,b)
 put(root,'MANIFEST.json',z.read('ROOT-MANIFEST.json'))
 expected=js(z.read('ROOT-MANIFEST.json'));prior=Path(root)/prefix;pm=js((prior/'MANIFEST.json').read_bytes())
 assert expected=={**{prefix+'/'+n:file_ident(prior/n) for n in set(pm)|{'MANIFEST.json'}},**m}
 return verify(root)
