"""Materialize only the exact unchanged companion dependency. No tests or runtime."""
import pathlib,zipfile,json,hashlib
P=pathlib.Path(__file__).resolve().parent;p=P/'inputs/source-only-integration.zip';b=p.read_bytes()
assert len(b)==9569533 and hashlib.sha256(b).hexdigest()=='7f58a377120157b379058f3aa4642de14625eda243792b8a5b681da9f969596d'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
with zipfile.ZipFile(p) as z:
 names=z.namelist();assert len(names)==107 and len(names)==len(set(names)) and z.testzip() is None
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n in names:assert not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts
 for n,v in m.items():assert ident(z.read(n))==v
 dest=P/'source-only'
 if dest.exists():
  assert {str(q.relative_to(dest)) for q in dest.rglob('*') if q.is_file()}==set(names)
  for n in names:assert (dest/n).read_bytes()==z.read(n)
 else:z.extractall(dest)
print('PASS exact SOURCE-ONLY dependency; use verified 666-member root; no tests or expansion run')
