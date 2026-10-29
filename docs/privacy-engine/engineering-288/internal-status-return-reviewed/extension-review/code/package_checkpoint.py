from pathlib import Path
import hashlib,json,zipfile,shutil,stat
w=Path(__file__).resolve().parents[2];base=w/'sr-review';inp=base/'input';inp.mkdir(exist_ok=False);shutil.copyfile(w/'upload/I164-internal-status-return-correspondence-1(1).zip',inp/'I164-internal-status-return-correspondence-1.zip')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert ident((inp/'I164-internal-status-return-correspondence-1.zip').read_bytes())=={'bytes':62835317,'sha256':'06d3b32fdf83757b40d9963a45a21ca5a5a80d2ca5c4af813655b4ad465f3864'}
ps=sorted(p for p in base.rglob('*') if p.is_file() and p.relative_to(base).as_posix()!='MANIFEST.json');assert all(stat.S_ISREG(p.lstat().st_mode) for p in ps);m={p.relative_to(base).as_posix():ident(p.read_bytes()) for p in ps};(base/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
out=w/'Formal-Lab6-I164-internal-status-return-correspondence-independent-review.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(base.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(base).as_posix())
print(json.dumps({'path':str(out),**ident(out.read_bytes()),'entries':len(m)+1}))
