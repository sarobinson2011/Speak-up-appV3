"""Verify packaged or extracted checkpoint, without application imports."""
import hashlib,json,sys,zipfile,tempfile
from pathlib import Path

def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(path):
 if path.is_file():
  with zipfile.ZipFile(path) as z:
   names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
   m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
   for n,v in m.items():
    assert not n.startswith('/') and '..' not in Path(n).parts
    assert ident(z.read(n))==v,n
   with tempfile.TemporaryDirectory(prefix='i164-bootstrap-verify-') as tmp:
    z.extractall(tmp);verify(Path(tmp))
  print(json.dumps({'bytes':path.stat().st_size,'entries':len(names),'sha256':ident(path.read_bytes())['sha256'],'CRC_membership_manifests_fresh_extraction':'PASS'}))
 else:
  m=json.loads((path/'MANIFEST.json').read_bytes());assert {str(p.relative_to(path)) for p in path.rglob('*') if p.is_file()}==set(m)|{'MANIFEST.json'}
  for n,v in m.items():assert ident((path/n).read_bytes())==v,n
if __name__=='__main__':verify(Path(sys.argv[1]))
