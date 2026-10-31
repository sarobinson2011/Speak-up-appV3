from pathlib import Path,PurePosixPath
import hashlib,json,io,os,stat,zipfile
BASE=Path('/workspace/scratch/ace5c9b2f18b')
INPUT=BASE/'upload/I164-control-construction-exception-correspondence-1(1).zip'
PIN={'bytes':127845952,'sha256':'ae720b26da6eb537209215e7545bd08e3e46c803650d02158631a935260aaf10'}
PRIOR=BASE/'ccn-dependencies/Formal-Lab6-I164-control-callback-exception-independent-review.zip'
PRIOR_PIN={'bytes':122719216,'sha256':'056f198bb178235e4b607eab22652cdeff5c105471880a4bacee74fd848b9229'}
INCOMPLETE_PIN={'bytes':122064627,'sha256':'1821bf45816c834bceada2e14f8899f947b7b238473da60d94346e4303083895'}
OLD_PIN={'bytes':124424355,'sha256':'ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20'}
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
 assert identity(INPUT.read_bytes())==PIN;assert identity(PRIOR.read_bytes())==PRIOR_PIN
 with zipfile.ZipFile(INPUT) as z,zipfile.ZipFile(PRIOR) as review:
  m=verified(z);pm=verified(review);assert len(m)==3259 and len(pm)==29
  ib=review.read('retained/INCOMPLETE-recovery.zip');assert identity(ib)==INCOMPLETE_PIN
  with zipfile.ZipFile(io.BytesIO(ib)) as inc:
   im=verified(inc);assert len(im)==70
   ob=inc.read('input/I164-control-callback-exception-correspondence-1.zip');assert identity(ob)==OLD_PIN
   with zipfile.ZipFile(io.BytesIO(ob)) as old:
    om=verified(old);assert len(om)==3068
    expected={}
    for n in old.namelist():expected['retained/control/'+n]=old.read(n)
    for n in inc.namelist():
     if n!='input/I164-control-callback-exception-correspondence-1.zip':expected['retained/incomplete/'+n]=inc.read(n)
    for n in review.namelist():
     if n!='retained/INCOMPLETE-recovery.zip':expected['retained/review/'+n]=review.read(n)
    assert {n for n in z.namelist() if n.startswith('retained/')}==set(expected)
    for n,b in expected.items():assert z.read(n)==b,n
  cut=json.loads(z.read('provenance/recovery-cut-manifest.json'));adds=json.loads(z.read('provenance/final-added-files.json'));frozen=json.loads(z.read('provenance/frozen-input-manifest.json'))
  assert not set(cut)&set(adds)
  assert set(z.namelist())==set(cut)|set(adds)|{'provenance/final-added-files.json','MANIFEST.json'}
  for plan in (cut,adds,frozen):
   for n,pin in plan.items():assert m[n]==pin,n
  roots={}
  for label in ('primary','recovered'):
   root=Path('/workspace/review-evidence/FL6-construction-20261031')/label;root.mkdir(parents=True,exist_ok=False)
   for n in z.namelist():
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(z.read(n))
   roots[label]={'path':str(root),**verify_root(root)}
  result={'input':PIN,'entries':3260,'manifested_hashes':3259,'manifest':identity(z.read('MANIFEST.json')),'CRC':'PASS','safe_exact_membership':'PASS','all_manifest_hashes':'PASS','preserved_control_members':3069,'preserved_incomplete_members':70,'preserved_completed_review_members':29,'new_members':92,'retained_byte_comparisons':'EXACT','prior_review':PRIOR_PIN,'prior_incomplete':INCOMPLETE_PIN,'prior_target':OLD_PIN,'frozen_members_preserved':len(frozen),'recovery_cut_members_preserved':len(cut),'final_additions':len(adds),'intermediate_cut_original_outer_bytes_freshly_verified':False,'roots':roots,'extracted_bytes':sum(i.file_size for i in z.infolist())}
 (BASE/'ccn-review/results/integrity.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
