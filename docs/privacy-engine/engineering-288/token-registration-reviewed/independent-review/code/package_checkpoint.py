from pathlib import Path
import hashlib,json,zipfile,shutil,stat
w=Path(__file__).resolve().parents[2];base=w/'tr-review';inp=base/'input';inp.mkdir(exist_ok=False)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
source=w/'upload/I164-token-registration-correspondence-1(1).zip';assert ident(source.read_bytes())=={'bytes':69308990,'sha256':'84c714c62aa6aa3956e5b137d03e584b055c06b26200b6768090ad33a5e4dbeb'};shutil.copyfile(source,inp/'I164-token-registration-correspondence-1.zip')
ps=sorted(p for p in base.rglob('*') if p.is_file() and p.relative_to(base).as_posix()!='MANIFEST.json');assert all(stat.S_ISREG(p.lstat().st_mode) for p in ps)
m={p.relative_to(base).as_posix():ident(p.read_bytes()) for p in ps};(base/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
out=w/'Formal-Lab6-I164-token-registration-independent-review.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(base.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(base).as_posix())
print(json.dumps({'path':str(out),**ident(out.read_bytes()),'entries':len(m)+1}))
