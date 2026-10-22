"""Derive strict dependency membership only from verified declared archive bytes."""
import io,json,hashlib,zipfile
from pathlib import Path
DRAFT=(13820246,'f26d73237597ad2998735d6c71810f341b9bdbbf705497b0360f2ae59fbd6ec3',56)
INTEGRATION=(9569533,'7f58a377120157b379058f3aa4642de14625eda243792b8a5b681da9f969596d',107)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def archive(raw,pin):
 assert (len(raw),hashlib.sha256(raw).hexdigest())==pin[:2],'ARCHIVE-IDENTITY'
 z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist();assert len(names)==pin[2] and len(names)==len(set(names)) and z.testzip() is None,'ARCHIVE-INTEGRITY'
 assert all(not n.startswith('/') and '..' not in Path(n).parts and not n.endswith('/') for n in names),'MEMBER-PATH'
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'},'MEMBERSHIP'
 for n,v in m.items():assert ident(z.read(n))==v,'MEMBER-IDENTITY'
 return z

def derive(raw):
 z=archive(raw,DRAFT);nested=archive(z.read('inputs/source-only-integration.zip'),INTEGRATION)
 m={n:ident(z.read(n)) for n in z.namelist()}
 for n in nested.namelist():
  key='source-only/'+n;assert key not in m,'RECOVERY-COLLISION';m[key]=ident(nested.read(n))
 assert len(m)==163
 return m
if __name__=='__main__':
 import sys
 out=Path(sys.argv[2]);assert not out.exists(),'DESTINATION-EXISTS'
 out.write_text(json.dumps(derive(Path(sys.argv[1]).read_bytes()),indent=2,sort_keys=True)+'\n')
