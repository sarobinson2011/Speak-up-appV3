"""ZIP identity/member verification and safe fresh extraction. No candidate execution."""
import hashlib,json,sys,zipfile
from pathlib import Path,PurePosixPath
p=Path(sys.argv[1]);dest=Path(sys.argv[2]);assert not dest.exists(),'fresh destination required'
raw=p.read_bytes();z=zipfile.ZipFile(p);names=z.namelist()
assert len(names)==len(set(names)) and z.testzip() is None
for n in names:
 q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and not n.endswith('/')
 assert (z.getinfo(n).external_attr>>16)&0o170000 != 0o120000
m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
for n,v in m.items():
 b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
z.extractall(dest)
assert {str(q.relative_to(dest)) for q in dest.rglob('*') if q.is_file()}==set(names)
for n,v in m.items():
 b=(dest/n).read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
print(json.dumps({'bytes':len(raw),'entries':len(names),'sha256':hashlib.sha256(raw).hexdigest(),'CRC':'PASS','exact_membership':'PASS','manifest_hashes':'PASS','fresh_extraction':'PASS'}))
