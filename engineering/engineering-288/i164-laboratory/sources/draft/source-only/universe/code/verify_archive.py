"""Verify exact review/input archive identities, CRC and safe manifest membership."""
import argparse,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--bytes',type=int);p.add_argument('--entries',type=int);p.add_argument('--sha256');p.add_argument('--extract',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
b=a.archive.read_bytes();identity={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
if a.bytes is not None:assert len(b)==a.bytes
if a.sha256 is not None:assert identity['sha256']==a.sha256
with zipfile.ZipFile(a.archive) as z:
 names=z.namelist();assert len(names)==len(set(names));assert z.testzip() is None
 if a.entries is not None:assert len(names)==a.entries
 for i in z.infolist():
  n=PurePosixPath(i.filename);assert not i.is_dir() and not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and str(n)==i.filename and not stat.S_ISLNK(i.external_attr>>16)
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n,v in m.items():
  raw=z.read(n);assert {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==v,n
 if a.extract:
  assert not a.extract.exists();z.extractall(a.extract)
identity.update(entries=len(names),CRC='PASS',safe_exact_membership='PASS',manifest_hashes='PASS')
if a.output:a.output.write_text(json.dumps(identity,indent=2)+'\n')
print(json.dumps(identity))
