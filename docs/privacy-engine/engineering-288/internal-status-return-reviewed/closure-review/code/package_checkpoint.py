from pathlib import Path
import os,stat,json,hashlib,zipfile,shutil
w=Path(__file__).resolve().parents[2];base=w/'is01-review'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
source=w/'upload/I164-IS01-correction(1).zip';assert ident(source.read_bytes())=={'bytes':68317556,'sha256':'5915d8d409d043e9dd95535e91880263e26c776220b8c6d48bf75690e3fc60a9'}
inp=base/'input';inp.mkdir(exist_ok=False);shutil.copyfile(source,inp/'I164-IS01-correction.zip')
files={};omitted=[]
def walk(path):
 for e in os.scandir(path):
  p=Path(e.path);n=p.relative_to(base).as_posix();mode=e.stat(follow_symlinks=False).st_mode
  if stat.S_ISDIR(mode):walk(p)
  elif stat.S_ISREG(mode):files[n]=p
  elif stat.S_ISLNK(mode) and n=='adjacent/root-link':omitted.append({'path':n,'target':os.readlink(p),'reason':'Actual refusal-control symlink retained locally; exact record and rejection included, not an archive member.'})
  else:raise AssertionError(('unexpected artifact type',n))
walk(base);assert len(omitted)==1
(base/'results/package-selection.json').write_text(json.dumps({'omitted_filesystem_entries':omitted,'candidate_or_historical_files_omitted':0},indent=2)+'\n');files['results/package-selection.json']=base/'results/package-selection.json';files.pop('MANIFEST.json',None)
m={n:ident(p.read_bytes()) for n,p in sorted(files.items())};(base/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');files['MANIFEST.json']=base/'MANIFEST.json'
out=w/'Formal-Lab6-I164-IS01-independent-closure-review.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
print(json.dumps({'path':str(out),**ident(out.read_bytes()),'entries':len(files)}))
