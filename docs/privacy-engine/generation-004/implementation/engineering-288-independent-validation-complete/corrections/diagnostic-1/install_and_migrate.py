"""Isolated installer; invoked only from a separately SHA-256 checked archive."""
import hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path
NAME='Engineering-288-checkpoint-4W-diagnostic-1'
def install(archive,base):
 archive=Path(archive);base=Path(base).resolve();dest=base/NAME;tmp=base/(NAME+'.installing')
 if 'Speak-up-appV3' in base.parts or '.env' in base.parts:raise ValueError('isolated task directory required')
 with zipfile.ZipFile(archive) as z:
  prefix=NAME+'/';m=json.loads(z.read(prefix+'PACKAGE-MANIFEST.json'));names={prefix+x['path'] for x in m['files']}|{prefix+'PACKAGE-MANIFEST.json'}
  if set(z.namelist())!=names or len(z.namelist())!=len(names):raise ValueError('ZIP membership')
  for n in names:
   p=Path(n)
   if p.is_absolute() or '..' in p.parts or '.env' in p.parts or stat.S_ISLNK(z.getinfo(n).external_attr>>16):raise ValueError('unsafe member')
  if not dest.exists():
   if tmp.exists():raise ValueError('unpublished installation exists; preserve and inspect')
   tmp.mkdir(parents=True,mode=0o700)
   for x in m['files']:
    data=z.read(prefix+x['path'])
    if len(data)!=x['bytes'] or hashlib.sha256(data).hexdigest()!=x['sha256']:raise ValueError('member hash')
    p=tmp/x['path'];p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
   with (tmp/'PACKAGE-MANIFEST.json').open('xb') as f:f.write(z.read(prefix+'PACKAGE-MANIFEST.json'));f.flush();os.fsync(f.fileno())
   for d in sorted([p for p in tmp.rglob('*') if p.is_dir()]+[tmp],key=lambda p:len(p.parts),reverse=True):
    fd=os.open(d,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
   os.replace(tmp,dest);fd=os.open(base,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
  for x in m['files']:
   p=dest/x['path']
   if p.is_symlink() or not p.is_file() or p.stat().st_size!=x['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:raise ValueError('installed bytes differ: '+x['path'])
  for n in ['emitter_service','validator_service']:(dest/'runtime/native'/n).chmod(0o755)
 return dest
