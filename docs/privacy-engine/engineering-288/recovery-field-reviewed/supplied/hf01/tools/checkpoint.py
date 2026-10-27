"""Package/recover regular source and saved-evidence files; no app execution."""
import argparse,hashlib,json,os,stat,zipfile
from pathlib import Path,PurePosixPath

def identity(path):
 h=hashlib.sha256();size=0
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
 return {'bytes':size,'sha256':h.hexdigest()}
def pack(root,output):
 files={}
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):walk(q)
   else:
    assert stat.S_ISREG(mode),q
    name=q.relative_to(root).as_posix()
    if name!='MANIFEST.json':files[name]=identity(q)
 walk(root)
 manifest=root/'MANIFEST.json';manifest.write_text(json.dumps(files,sort_keys=True,indent=2)+'\n')
 temporary=Path(str(output)+'.building');assert not Path(output).exists()
 with zipfile.ZipFile(temporary,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in sorted(set(files)|{'MANIFEST.json'}):z.write(root/name,name)
 with temporary.open('rb') as f:os.fsync(f.fileno())
 verify(temporary)
 temporary.rename(output)
 return verify(output)
def verify(path,destination=None):
 with zipfile.ZipFile(path) as z:
  names=z.namelist();assert len(names)==len(set(names))
  for i in z.infolist():
   p=PurePosixPath(i.filename);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  assert z.testzip() is None
  manifest=json.loads(z.read('MANIFEST.json'));assert set(names)==set(manifest)|{'MANIFEST.json'}
  if destination is not None:destination.mkdir(parents=True,exist_ok=False)
  for name in names:
   b=z.read(name)
   if name in manifest:assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==manifest[name],name
   if destination is not None:
    q=destination/name;q.parent.mkdir(parents=True,exist_ok=True)
    with q.open('xb') as f:f.write(b)
  return {'filename':Path(path).name,**identity(path),'entries':len(names),'manifested_files':len(manifest),'CRC':'PASS','safe_unique_regular_membership':'PASS','all_member_hashes':'PASS','manifest_identity':{'bytes':len(z.read('MANIFEST.json')),'sha256':hashlib.sha256(z.read('MANIFEST.json')).hexdigest()}}
def main():
 p=argparse.ArgumentParser();p.add_argument('operation',choices=['pack','verify','recover']);p.add_argument('archive',type=Path);p.add_argument('--root',type=Path);a=p.parse_args()
 result=pack(a.root,a.archive) if a.operation=='pack' else verify(a.archive,a.root if a.operation=='recover' else None)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
