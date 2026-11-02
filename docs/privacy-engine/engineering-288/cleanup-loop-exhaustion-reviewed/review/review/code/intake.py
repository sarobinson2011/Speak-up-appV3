"""Independent byte-only verification/recovery; no candidate code execution."""
from pathlib import Path,PurePosixPath
import json,zipfile,io,hashlib,stat,os
BASE=Path('/workspace/scratch/ace5c9b2f18b/loop-review')
AREA=Path('/workspace/review-evidence/FL6-loop-20261102')
INPUT=BASE.parent/'upload/I164-cleanup-loop-exhaustion-correspondence-1(1).zip'
PIN={'bytes':169181718,'sha256':'a48cb3be9002e8dbdcf3ac8c6e2d0ed45ea1eced14126af3d9d1862ec1963dd5'}
LINE_REVIEW={'bytes':160663290,'sha256':'156f5a7cca4b3966ac348d3bf6a0636a69ebd1c66375bb0c1277d929e4e37251'}
LINE={'bytes':159370715,'sha256':'2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1'}
CLOSURE={'bytes':154107404,'sha256':'7971a5cd95ef8775ff05e2db0ef5c3521903586c0d530b9e590b4bb54029fcef'}
EC01={'bytes':153799952,'sha256':'ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71'}
REVIEW={'bytes':156078207,'sha256':'212d2f0886cb09cddb119470ba908e2142bb141a6eb6bdca83a3e5f83b82cbcb'}
ORIGINAL={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 assert n and str(PurePosixPath(n))==n and not PurePosixPath(n).is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/'));return n
def archive(raw,pin,count):
 assert identity(raw)==pin;z=zipfile.ZipFile(io.BytesIO(raw));ns=[safe(i.filename) for i in z.infolist()]
 assert len(ns)==len(set(ns))==count
 assert not set(ns)&{str(p) for n in ns for p in PurePosixPath(n).parents if str(p)!='.'}
 for i in z.infolist():assert i.filename==i.orig_filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
 m=js(z.read('MANIFEST.json'));assert set(ns)==set(m)|{'MANIFEST.json'}
 for n,p in m.items():assert identity(z.read(n))==p,n
 assert z.testzip() is None
 return z,m
def put(root,n,b):
 p=root/safe(n);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode);mp=root/'MANIFEST.json';assert stat.S_ISREG(mp.lstat().st_mode);m=js(mp.read_bytes());ns=set(m)|{'MANIFEST.json'};dirs={str(p) for n in ns for p in PurePosixPath(safe(n)).parents if str(p)!='.'};files=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in ns,n;files.add(n)
 walk(root);assert files==ns and seen==dirs
 for n,p in m.items():assert identity((root/n).read_bytes())==p,n
 return {'files':len(files),'directories':len(dirs),'manifest':identity(mp.read_bytes()),'membership_types_hashes':'PASS'}
def additions(root,z):
 m=js(z.read('ADDITIONS-MANIFEST.json'))
 assert {n.removeprefix('root-additions/') for n in z.namelist() if n.startswith('root-additions/')}==set(m)
 for n,p in m.items():
  assert not n.startswith('retained/');raw=z.read('root-additions/'+safe(n));assert identity(raw)==p;put(root,n,raw)
 put(root,'MANIFEST.json',z.read('ROOT-MANIFEST.json'));return verify_root(root)
def main():
 AREA.mkdir(parents=True,exist_ok=False)
 z,outer=archive(INPUT.read_bytes(),PIN,81)
 for n in z.namelist():put(AREA/'package',n,z.read(n))
 print('Outer identity, CRC, safe exact membership and 80 hashes PASS',flush=True)
 lr,_=archive(z.read('retained/Formal-Lab6-I164-cleanup-error-report-independent-review.zip'),LINE_REVIEW,83)
 line,_=archive(lr.read('input/I164-cleanup-error-report-correspondence-1.zip'),LINE,83)
 closure,_=archive(line.read('retained/Formal-Lab6-I164-EC01-independent-closure.zip'),CLOSURE,52)
 ec,_=archive(closure.read('input/I164-EC01-terminal-exception-correction-1.zip'),EC01,57)
 old,_=archive(ec.read('retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip'),REVIEW,85)
 original,_=archive(old.read('input/I164-exceptional-cleanup-append-correspondence-1.zip'),ORIGINAL,3982)
 print('Exact nested archive identities, CRC, memberships and hashes PASS',flush=True)
 root=AREA/'recovered';prior=root/'retained/report';ecroot=prior/'retained/cleanup'
 for n in original.namelist():put(ecroot,n,original.read(n))
 overlay=js(ec.read('OVERLAY-MANIFEST.json'))
 for n,p in overlay.items():
  b=ec.read('overlay/'+safe(n));assert identity(b)==p;q=ecroot/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 (ecroot/'MANIFEST.json').write_bytes(ec.read('ROOT-MANIFEST.json'));ecverified=verify_root(ecroot)
 prior_verified=additions(prior,line);root_verified=additions(root,z)
 m=js(z.read('ROOT-MANIFEST.json'));pm=js(line.read('ROOT-MANIFEST.json'));ad=js(z.read('ADDITIONS-MANIFEST.json'))
 assert m=={**{'retained/report/'+n:identity((prior/n).read_bytes()) for n in set(pm)|{'MANIFEST.json'}},**ad}
 changed=js(z.read('new/provenance/changed-files.json'))
 for row in changed['intentional_replacements']:
  n=row['path'];assert identity((root/n).read_bytes())==row['new'] and identity((prior/n).read_bytes())==row['old']
 a=(root/'code/managed_coverage.py').read_bytes();b=(prior/'code/managed_coverage.py').read_bytes()
 assert len(b)==359095 and a==b+z.read('new/code/producer-addition.py')
 for n in ('lab_bootstrap.py','prospective_entry.py','live_connection.py'):assert (root/'source-evidence'/n).read_bytes()==(prior/'source-evidence'/n).read_bytes()
 result={'input':PIN,'entries':81,'manifested_hashes':80,'CRC':'PASS','safe_exact_membership':'PASS','dependencies':[LINE_REVIEW,LINE,CLOSURE,EC01,REVIEW,ORIGINAL],'recovered_root':root_verified,'unchanged_predecessor':prior_verified,'EC01':ecverified,'declared_additions':len(ad),'predecessor_members_preserved':len(pm)+1,'reviewed_producer_prefix_bytes':359095,'reviewed_producer_prefix_unchanged':True,'runtime_source_bytes_unchanged':True,'declared_changes':changed,'candidate_executions':0}
 (BASE/'results/intake.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
