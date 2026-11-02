from pathlib import Path,PurePosixPath
import os,stat,json,hashlib,zipfile,ast
BASE=Path('/workspace/scratch/ace5c9b2f18b');INPUT=BASE/'upload/I164-exceptional-cleanup-append-correspondence-1(2).zip';AREA=Path('/workspace/review-evidence/FL6-cleanup-append-20261101')
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def unique(ps):
 d={}
 for k,v in ps:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 p=PurePosixPath(n);assert n and not p.is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/')) and str(p)==n,n
 return n
def verify_root(root):
 root=Path(root);m=js((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'};found=set();seen=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs,n;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected,n;found.add(n)
 walk(root);assert found==expected and seen==dirs
 for n,pin in m.items():assert identity((root/n).read_bytes())==pin,n
 return {'root':str(root),'files':len(found),'directories':len(seen),'safe_exact_membership_hashes':'PASS'}
def main():
 pin=identity(INPUT.read_bytes());assert pin=={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
 AREA.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(INPUT) as z:
  ii=z.infolist();names=[safe(i.filename) for i in ii];assert len(names)==len(set(names))==3982
  for i in ii:assert i.orig_filename==i.filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,i.filename
  m=js(z.read('MANIFEST.json'));assert len(m)==3981 and set(names)==set(m)|{'MANIFEST.json'}
  for n,p in m.items():assert identity(z.read(n))==p,n
  for label in ('primary','recovered'):
   root=AREA/label;root.mkdir()
   for n in names:p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 root=AREA/'primary';prior=root/'retained/details';pr=verify_root(prior);assert pr['files']==3771 and identity((prior/'MANIFEST.json').read_bytes())=={'bytes':1313785,'sha256':'a0a0f40e02254798c0e5b8e3e35d8b46850fa9ac0721e32f3043ab211c28a679'}
 review=root/'retained/closure-review';rm=js((review/'MANIFEST.json').read_bytes());kept=0
 for n,p in rm.items():
  if n=='input/I164-LD01-monitoring-lease-correction-1.zip':assert p=={'bytes':139583348,'sha256':'e4accc10b74390d08266853a0da649c8e4c235ce839bbf2b9bb9548926f7c97c'}
  else:assert identity((review/n).read_bytes())==p,n;kept+=1
 changes=js((root/'provenance/changed-files.json').read_bytes())
 for n,p in changes['intentional_changes'].items():assert identity((root/n).read_bytes())==p['after'] and identity((prior/n).read_bytes())==p['before']
 old=(prior/'code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes();assert len(old)==322999 and new.startswith(old);a=ast.parse(old);b=ast.parse(new);assert len(b.body)==len(a.body)+6 and all(ast.dump(x,include_attributes=True)==ast.dump(y,include_attributes=True) for x,y in zip(a.body,b.body))
 for n in ('lab_bootstrap.py','prospective_entry.py'):assert (root/'source-evidence'/n).read_bytes()==(prior/'source-evidence'/n).read_bytes()
 frozen=js((root/'provenance/frozen-input-manifest.json').read_bytes())
 for n,p in frozen.items():assert identity((root/n).read_bytes())==p,n
 receipt=(root/'results/recovered/cleanup-append.json').read_bytes();assert receipt==(root/'results/primary/cleanup-append.json').read_bytes()==(root/'receipts/prepared-cleanup-append.json').read_bytes()
 r={'input':pin,'entries':3982,'manifested_hashes':3981,'CRC':'PASS','manifest':identity((root/'MANIFEST.json').read_bytes()),'roots':{k:verify_root(AREA/k) for k in ('primary','recovered')},'predecessor':pr,'prior_closure_noninput_members':kept,'prior_compressed_archives_freshly_verified':False,'frozen_members':len(frozen),'changes':changes,'producer_prefix_bytes':len(old),'inherited_producer_functions':sum(isinstance(n,ast.FunctionDef) for n in a.body),'new_producer_functions':6,'receipt':identity(receipt),'receipt_identity_not_itself_validation':True}
 (BASE/'eca-review/results/integrity.json').write_bytes(enc(r));print(json.dumps(r),flush=True)
if __name__=='__main__':main()
