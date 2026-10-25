"""Create or verify a compact exact-membership checkpoint; no validation code runs."""
import argparse,hashlib,json,os,stat,zipfile
from pathlib import Path,PurePosixPath

def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(p,dest=None):
 with zipfile.ZipFile(p) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
  m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
  for i in z.infolist():
   n=PurePosixPath(i.filename);assert not n.is_absolute() and '..' not in n.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
  for n,v in m.items():assert ident(z.read(n))==v,n
  if dest:
   dest=Path(dest);assert not dest.exists();dest.mkdir(parents=True);z.extractall(dest)
   assert {f.relative_to(dest).as_posix() for f in dest.rglob('*') if f.is_file()}==set(names)
   for n,v in m.items():assert ident((dest/n).read_bytes())==v,n
 return {**ident(Path(p).read_bytes()),'entries':len(names),'CRC':'PASS','membership':'PASS','manifest_hashes':'PASS'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['build','verify']);ap.add_argument('path');ap.add_argument('--output');ap.add_argument('--extract');a=ap.parse_args()
 if a.action=='build':
  root=Path(a.path);files={}
  for p in sorted(root.rglob('*')):
   assert not p.is_symlink() and (p.is_dir() or p.is_file()), str(p)
   if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json':files[p.relative_to(root).as_posix()]=ident(p.read_bytes())
  (root/'MANIFEST.json').write_text(json.dumps(files,indent=2)+'\n')
  out=Path(a.output);assert not out.exists();pending=out.with_suffix('.pending');assert not pending.exists()
  with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for p in sorted(root.rglob('*')):
    if p.is_file():z.write(p,p.relative_to(root).as_posix())
  with pending.open('rb') as f:os.fsync(f.fileno())
  pending.rename(out);print(json.dumps(verify(out,a.extract),indent=2))
 else:print(json.dumps(verify(a.path,a.extract),indent=2))
if __name__=='__main__':main()
