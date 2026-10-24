"""Read-only checkpoint integrity; optional safe NEW-directory extraction."""
import argparse,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--sha256',required=True);p.add_argument('--bytes',required=True,type=int);p.add_argument('--extract',type=Path);a=p.parse_args()
def need(v,m):
 if not v:raise ValueError(m)
b=a.archive.read_bytes();need(len(b)==a.bytes and hashlib.sha256(b).hexdigest()==a.sha256,'ARCHIVE-IDENTITY')
with zipfile.ZipFile(a.archive) as z:
 names=z.namelist();need(len(names)==len(set(names)) and z.testzip() is None,'ZIP-INTEGRITY');m=json.loads(z.read('MANIFEST.json'));need(set(names)==set(m)|{'MANIFEST.json'},'MEMBERSHIP')
 for i in z.infolist():
  n=PurePosixPath(i.filename);need(not n.is_absolute() and '..' not in n.parts and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'REGULAR-SAFE-PATH')
 for n,v in m.items():
  raw=z.read(n);need(v=={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'HASH:'+n)
 if a.extract:
  need(not a.extract.exists() and not str(a.extract.resolve()).startswith('/tmp/'),'NEW-PERSISTENT-DESTINATION');a.extract.mkdir(parents=True)
  for n in names:
   dest=a.extract/n;dest.parent.mkdir(parents=True,exist_ok=True)
   with dest.open('xb') as f:f.write(z.read(n))
  need({p.relative_to(a.extract).as_posix() for p in a.extract.rglob('*') if p.is_file()}==set(names),'EXTRACTED-MEMBERSHIP')
  for n in names:need((a.extract/n).read_bytes()==z.read(n),'EXTRACTED-BYTES:'+n)
print('PASS CRC, exact membership, manifests'+(' and fresh extraction' if a.extract else ''))
