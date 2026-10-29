"""Build the review archive from immutable reviewed input and completed evidence."""
from pathlib import Path
import hashlib,json,stat,zipfile
w=Path(__file__).resolve().parents[2];r=w/'ol-review';target=w/'Formal-Lab6-I164-owner-lock-finalization-independent-review.zip'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert not target.exists()
files={p.relative_to(r).as_posix():p.read_bytes() for p in sorted(r.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
raw=(w/'upload/I164-owner-lock-finalization-correspondence-1(1).zip').read_bytes();assert ident(raw)=={'bytes':74161617,'sha256':'09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b'}
files['input/I164-owner-lock-finalization-correspondence-1.zip']=raw
manifest=(json.dumps({n:ident(b) for n,b in sorted(files.items())},indent=2)+'\n').encode();(r/'MANIFEST.json').write_bytes(manifest);files['MANIFEST.json']=manifest
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,b in sorted(files.items()):
  i=zipfile.ZipInfo(n,date_time=(2026,10,29,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b,compresslevel=9)
print(json.dumps({'file':str(target),'entries':len(files),'manifested_hashes':len(files)-1,**ident(target.read_bytes())},indent=2))
