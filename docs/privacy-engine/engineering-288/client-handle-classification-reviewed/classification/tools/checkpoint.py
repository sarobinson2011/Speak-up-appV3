"""Pack/verify exact regular files without executing candidate/application code."""
import argparse,hashlib,json,os,stat,zipfile
from pathlib import Path,PurePosixPath
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def inventory(root):
 files={}
 for base,dirs,names in os.walk(root,followlinks=False):
  for n in dirs:assert stat.S_ISDIR((Path(base)/n).lstat().st_mode)
  for n in names:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);files[p.relative_to(root).as_posix()]=p.read_bytes()
 return files
def pack(files,target):
 assert 'MANIFEST.json' not in files;files=dict(files);files['MANIFEST.json']=enc({n:identity(b) for n,b in sorted(files.items())})
 assert not target.exists();temp=target.with_name(target.name+'.building');assert not temp.exists()
 with zipfile.ZipFile(temp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(files.items()):
   i=zipfile.ZipInfo(n,(2026,10,27,0,0,0));i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
 os.replace(temp,target);return verify(target)
def verify(path,extract=None):
 with zipfile.ZipFile(path) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None;m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
  if extract is not None:extract.mkdir(parents=True,exist_ok=False)
  for n in names:
   p=PurePosixPath(n);i=z.getinfo(n);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and not i.is_dir() and stat.S_ISREG(i.external_attr>>16)
   raw=z.read(n)
   if n!='MANIFEST.json':assert identity(raw)==m[n],n
   if extract is not None:
    q=extract/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
  return dict(identity(path.read_bytes()),entries=len(names),manifested_files=len(m),CRC='PASS',safe_unique_regular_membership='PASS',all_hashes='PASS',manifest_identity=identity(z.read('MANIFEST.json')))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path);p.add_argument('--zip',type=Path,required=True);p.add_argument('--extract',type=Path);a=p.parse_args()
 print(json.dumps(pack(inventory(a.root),a.zip) if a.root else verify(a.zip,a.extract),sort_keys=True))
