from pathlib import Path,PurePosixPath
import hashlib,json,io,os,stat,zipfile
BASE=Path('/workspace/scratch/ace5c9b2f18b')
INPUT=BASE/'cln-input/I164-client-construction-none-correspondence-1.zip'
PIN={'bytes':134972464,'sha256':'550a9f0bf5e0643d79bbf7ac48a098015a06f05dc79ccde7f3eeb34a8cfbd1fe'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def safe(n):
 p=PurePosixPath(n);assert n and not p.is_absolute() and p.as_posix()==n and '..' not in p.parts and '\\' not in n and ':' not in n and not n.endswith('/'),n
def verified(z):
 names=z.namelist();assert len(names)==len(set(names))
 for i in z.infolist():safe(i.filename);assert stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,i.filename
 m=json.loads(z.read('MANIFEST.json'));assert set(names)==set(m)|{'MANIFEST.json'}
 for n,pin in m.items():assert identity(z.read(n))==pin,n
 return m
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode)
 mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode);m=json.loads(mp.read_bytes())
 files=set();seen=set();expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs
 for n,pin in m.items():safe(n);assert identity((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'safe_exact_membership':'PASS','all_hashes':'PASS'}
def main():
 assert identity(INPUT.read_bytes())==PIN
 oldpath=BASE/'upload/I164-control-construction-exception-correspondence-1(1).zip'
 reviewpath=BASE/'Formal-Lab6-I164-control-construction-exception-independent-review.zip'
 assert identity(oldpath.read_bytes())=={'bytes':127845952,'sha256':'ae720b26da6eb537209215e7545bd08e3e46c803650d02158631a935260aaf10'}
 assert identity(reviewpath.read_bytes())=={'bytes':125975482,'sha256':'9e8b9d4664cc4abe55d93ca84a5db51e0991b30299d974903ec5beefa369843b'}
 with zipfile.ZipFile(INPUT) as z,zipfile.ZipFile(oldpath) as old,zipfile.ZipFile(reviewpath) as review:
  m=verified(z);assert len(m)==3413
  expected={'retained/control-construction/'+n:old.read(n) for n in old.namelist()}
  # Prior review includes its exact candidate; flattened copy excludes that nested archive.
  review_names=[n for n in review.namelist() if not n.startswith('input/')]
  expected.update({'retained/independent-review/'+n:review.read(n) for n in review_names})
  actual_retained={n for n in z.namelist() if n.startswith('retained/')}
  if actual_retained!=set(expected):
   print('COMPOSITION-DIFFERENCES',sorted(actual_retained-set(expected))[:10],sorted(set(expected)-actual_retained)[:10]);raise AssertionError('COMPOSITION')
  for n,b in expected.items():assert z.read(n)==b,n
  frozen=json.loads(z.read('provenance/frozen-input-manifest.json'));cut=json.loads(z.read('provenance/recovery-cut-manifest.json'))
  for plan in (frozen,cut):
   for n,pin in plan.items():assert m[n]==pin,n
  roots={}
  for label in ('primary','recovered'):
   root=Path('/workspace/review-evidence/FL6-client-none-20261031')/label;root.mkdir(parents=True,exist_ok=False)
   for n in z.namelist():
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(z.read(n))
   roots[label]={'path':str(root),**verify_root(root)}
  result={'input':PIN,'entries':len(z.namelist()),'manifested_hashes':len(m),'CRC':'PASS','safe_exact_membership':'PASS','manifest':identity(z.read('MANIFEST.json')),'retained_target_members':len(old.namelist()),'retained_review_noninput_members':len(review_names),'new_members':len(m)+1-len(expected),'retained_bytes':'EXACT','frozen_members':len(frozen),'recovery_cut_members':len(cut),'intermediate_cut_outer_bytes_freshly_verified':False,'roots':roots,'extracted_bytes':sum(i.file_size for i in z.infolist())}
 (BASE/'cln-review/results/integrity.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
