"""Independent byte-only verification/recovery; no candidate code execution."""
from pathlib import Path,PurePosixPath
import json,zipfile,io,hashlib,stat,os
BASE=Path('/workspace/scratch/ace5c9b2f18b/l172-review')
AREA=Path('/workspace/review-evidence/FL6-line172-20261102')
INPUT=BASE.parent/'upload/I164-cleanup-error-report-correspondence-1(1).zip'
PIN={'bytes':159370715,'sha256':'2b6d61b3f9dc756740a0c66f4bdf70a729cfb77d43beb495424965331aa72bd1'}
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
def main():
 BASE.joinpath('results').mkdir(parents=True,exist_ok=True);AREA.mkdir(parents=True,exist_ok=False)
 z,outer=archive(INPUT.read_bytes(),PIN,83)
 for n in z.namelist():put(AREA/'package',n,z.read(n))
 print('Outer identity, CRC, safe exact membership and 82 hashes PASS',flush=True)
 closure,cm=archive(z.read('retained/Formal-Lab6-I164-EC01-independent-closure.zip'),CLOSURE,52)
 ec,em=archive(closure.read('input/I164-EC01-terminal-exception-correction-1.zip'),EC01,57)
 old,om=archive(ec.read('retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip'),REVIEW,85)
 original,origm=archive(old.read('input/I164-exceptional-cleanup-append-correspondence-1.zip'),ORIGINAL,3982)
 print('All exact retained dependency archives and manifests PASS',flush=True)
 root=AREA/'recovered';prior=root/'retained/cleanup'
 for n in original.namelist():put(prior,n,original.read(n))
 overlay=js(ec.read('OVERLAY-MANIFEST.json'));expected_prior=js(ec.read('ROOT-MANIFEST.json'))
 for n,p in overlay.items():
  raw=ec.read('overlay/'+safe(n));assert identity(raw)==p==expected_prior[n];q=prior/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
 (prior/'MANIFEST.json').write_bytes(ec.read('ROOT-MANIFEST.json'));prior_verified=verify_root(prior)
 additions=js(z.read('ADDITIONS-MANIFEST.json'));assert {n.removeprefix('root-additions/') for n in outer if n.startswith('root-additions/')}==set(additions)
 for n,p in additions.items():
  assert not n.startswith('retained/');raw=z.read('root-additions/'+safe(n));assert identity(raw)==p;put(root,n,raw)
 put(root,'MANIFEST.json',z.read('ROOT-MANIFEST.json'));root_verified=verify_root(root)
 expected=js(z.read('ROOT-MANIFEST.json'));assert expected=={**{'retained/cleanup/'+n:identity((prior/n).read_bytes()) for n in set(expected_prior)|{'MANIFEST.json'}},**additions}
 changed=js(z.read('root-additions/provenance/changed-files.json'))
 for n,p in changed['changed_active_counterparts'].items():assert identity((root/n).read_bytes())==p['after'] and identity((prior/n).read_bytes())==p['before']
 prod=(root/'code/managed_coverage.py').read_bytes();prefix=(prior/'code/managed_coverage.py').read_bytes();assert prod==prefix+z.read('new/code/producer-addition.py')
 for n in ('lab_bootstrap.py','live_connection.py','prospective_entry.py'):assert (root/'source-evidence'/n).read_bytes()==(prior/'source-evidence'/n).read_bytes()
 for n in ('CHECKPOINT.json','REVIEW.txt','RECOVERY.txt'):put(AREA/'prior-closure',n,closure.read(n))
 reused={}
 for n in ('common.py','cases.py','parent_cases.py','parent_details.py','supervise.py'):
  b=closure.read('review/code/'+n);put(BASE/'retained-review-code',n,b);reused[n]=identity(b)
 for n in ('CHECKPOINT.json','REVIEW.txt'):put(AREA/'prior-append-review',n,old.read(n))
 result={'input':PIN,'entries':83,'manifested_hashes':82,'CRC':'PASS','safe_exact_membership':'PASS','dependencies':[CLOSURE,EC01,REVIEW,ORIGINAL],'recovered_root':root_verified,'unchanged_predecessor':prior_verified,'LD01':verify_root(prior/'retained/details'),'declared_additions':len(additions),'predecessor_members_preserved':len(expected_prior)+1,'reviewed_producer_prefix_unchanged':True,'runtime_source_bytes_unchanged':True,'changed_active_counterparts':changed,'reused_independent_helpers':reused,'candidate_executions':0}
 (BASE/'results/intake.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
