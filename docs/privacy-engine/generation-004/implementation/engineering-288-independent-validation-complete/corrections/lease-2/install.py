"""Explicit isolated installation; not called by the read-only host preflight."""
import hashlib,json,os,stat,zipfile
from pathlib import Path
NAME='Engineering-288-checkpoint-4W'
def install(archive,base,expected_sha256):
 archive=Path(archive);base=Path(base).resolve();dest=base/NAME;tmp=base/(NAME+'.installing')
 if 'Speak-up-appV3' in base.parts or '.env' in base.parts:raise ValueError('isolated execution directory required')
 with archive.open('rb') as f:
  if hashlib.file_digest(f,'sha256').hexdigest()!=expected_sha256:raise ValueError('download ZIP SHA mismatch')
 with zipfile.ZipFile(archive) as z:
  prefix=NAME+'/';m=json.loads(z.read(prefix+'PACKAGE-MANIFEST.json'));names={prefix+x['path'] for x in m['files']}|{prefix+'PACKAGE-MANIFEST.json'}
  if set(z.namelist())!=names or len(z.namelist())!=len(names):raise ValueError('ZIP membership')
  for n in names:
   p=Path(n)
   if p.is_absolute() or '..' in p.parts or stat.S_ISLNK(z.getinfo(n).external_attr>>16):raise ValueError('unsafe ZIP member')
  if not dest.exists():
   if tmp.exists():raise ValueError('unpublished install exists; inspect it, do not overwrite')
   tmp.mkdir(parents=True,mode=0o700)
   for n in names:
    p=tmp/n[len(prefix):];p.parent.mkdir(parents=True,exist_ok=True)
    with z.open(n) as src,p.open('xb') as out:
     while True:
      b=src.read(1048576)
      if not b:break
      out.write(b)
     out.flush();os.fsync(out.fileno())
   for directory in sorted([x for x in tmp.rglob('*') if x.is_dir()]+[tmp],key=lambda x:len(x.parts),reverse=True):
    fd=os.open(directory,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
   os.replace(tmp,dest);fd=os.open(base,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
  for x in m['files']:
   p=dest/x['path']
   if p.is_symlink() or p.stat().st_size!=x['bytes']:raise ValueError('installed file size/type')
   with p.open('rb') as f:
    if hashlib.file_digest(f,'sha256').hexdigest()!=x['sha256']:raise ValueError('installed bytes differ: '+x['path'])
  for name in ['emitter_service','validator_service']:(dest/'runtime/native'/name).chmod(0o755)
 return str(dest)
