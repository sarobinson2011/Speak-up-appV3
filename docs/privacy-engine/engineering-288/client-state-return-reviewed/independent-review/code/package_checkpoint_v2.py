from pathlib import Path
import hashlib,json,zipfile,stat
w=Path(__file__).resolve().parents[2];base=w/'cs-review'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert ident((base/'input/I164-client-state-return-correspondence-1.zip').read_bytes())=={'bytes':61624841,'sha256':'0ae24141a77f42eb96ed0f8d144f612d7a8045e04f7aa47dcaa8d1750f886907'}
files=sorted(p for p in base.rglob('*') if p.is_file() and p.relative_to(base).as_posix()!='MANIFEST.json');assert all(stat.S_ISREG(p.lstat().st_mode) for p in files)
m={p.relative_to(base).as_posix():ident(p.read_bytes()) for p in files};(base/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
out=w/'Formal-Lab6-I164-client-state-return-correspondence-independent-review.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(base.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(base).as_posix())
print(json.dumps({'path':str(out),**ident(out.read_bytes()),'entries':len(m)+1}))
