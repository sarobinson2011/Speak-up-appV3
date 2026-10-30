"""Independent archive, declared-composition and recovered-filesystem verification."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,zipfile,sys
BASE=Path('/workspace/scratch/ace5c9b2f18b')
INPUT=BASE/'upload/I164-control-callback-exception-correspondence-1(1).zip'
PIN={'bytes':124424355,'sha256':'ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20'}
PRIOR=BASE/'Formal-Lab6-I164-callback-exception-bare-rethrow-independent-review.zip'
PRIOR_PIN={'bytes':86457161,'sha256':'cd33f568c226319866e2c03aec678bc623e364369b962f261176ec54743fb6ba'}
PREDECESSOR_PIN={'bytes':88596749,'sha256':'c24b08d598115b1118121aeb6c9d42bbdd780a58a98375a29b96224e8c825876'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def safe(n):
 p=PurePosixPath(n)
 assert n and not p.is_absolute() and p.as_posix()==n and '..' not in p.parts and '\\' not in n and ':' not in n and not n.endswith('/'),n
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode)
 mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode);m=json.loads(mp.read_bytes())
 expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'};seen=set();files=set()
 for n in expected:safe(n)
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;files.add(n)
 walk(root);assert files==expected and seen==dirs,(files-expected,expected-files,seen-dirs,dirs-seen)
 for n,pin in m.items():assert identity((root/n).read_bytes())==pin,n
 return {'files':len(files),'directories':len(dirs),'safe_exact_membership':'PASS','hashes':'PASS'}
def recover(root,output):
 assert identity(INPUT.read_bytes())==PIN
 assert identity(PRIOR.read_bytes())==PRIOR_PIN
 with zipfile.ZipFile(PRIOR) as prior,zipfile.ZipFile(INPUT) as z:
  names=z.namelist();assert len(names)==3069==len(set(names))
  for i in z.infolist():safe(i.filename);assert stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,i.filename
  m=json.loads(z.read('MANIFEST.json'));assert len(m)==3068 and set(names)==set(m)|{'MANIFEST.json'}
  cut=json.loads(z.read('provenance/recovery-cut-manifest.json'));adds=json.loads(z.read('provenance/final-added-files.json'))
  assert not set(cut)&set(adds)
  assert set(names)==set(cut)|set(adds)|{'provenance/final-added-files.json','MANIFEST.json'}
  for n,pin in (cut|adds).items():assert m[n]==pin,n
  pm=json.loads(prior.read('MANIFEST.json'));assert len(pm)==64
  prior_input='input/I164-callback-exception-bare-rethrow-correspondence-1.zip'
  original=prior.read(prior_input);assert identity(original)==PREDECESSOR_PIN
  import io
  with zipfile.ZipFile(io.BytesIO(original)) as old:
   assert len(old.namelist())==2938
   inherited={'retained/bare/'+n for n in old.namelist()}
   retained={'retained/review/'+n for n in prior.namelist() if n!=prior_input}
   assert len(inherited)==2938 and len(retained)==64
   assert {n for n in names if n.startswith('retained/')}==inherited|retained
   root=Path(root);root.mkdir(parents=True,exist_ok=False)
   for n in names:
    b=z.read(n) # zipfile checks member CRC before returning bytes.
    if n!='MANIFEST.json':assert identity(b)==m[n],n
    if n.startswith('retained/bare/'):assert b==old.read(n.removeprefix('retained/bare/')),n
    elif n.startswith('retained/review/'):assert b==prior.read(n.removeprefix('retained/review/')),n
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
   result={'archive':PIN,'entries':len(names),'manifested_hashes':len(m),'manifest':identity(z.read('MANIFEST.json')),'CRC':'PASS','safe_exact_membership':'PASS','declared_composition':'2938 predecessor + 64 prior-review non-input + 67 current = 3069','cut_members_unchanged':len(cut),'final_added_members':len(adds),'predecessor':PREDECESSOR_PIN,'prior_review':PRIOR_PIN,'preserved_predecessor_members':2938,'preserved_prior_review_members':64,'all_member_comparisons':'EXACT','root':verify_root(root),'root_path':str(root),'extracted_bytes':sum(i.file_size for i in z.infolist())}
 Path(output).parent.mkdir(parents=True,exist_ok=True);Path(output).write_bytes(enc(result));print(json.dumps(result,sort_keys=True))
if __name__=='__main__':recover(sys.argv[1],sys.argv[2])
