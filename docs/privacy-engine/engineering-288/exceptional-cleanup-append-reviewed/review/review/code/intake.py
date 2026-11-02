"""Independent byte-only recovery and preservation audit; no candidate execution."""
from pathlib import Path,PurePosixPath
import zipfile,io,os,stat,json,hashlib,ast,difflib
BASE=Path('/workspace/scratch/ace5c9b2f18b')
AREA=Path('/workspace/review-evidence/FL6-EC01-20261101')
INPUT=BASE/'upload/I164-EC01-terminal-exception-correction-1(1).zip'
PIN={'bytes':153799952,'sha256':'ae83c5eeb7bf4ab09943f66f239bea3c7802777899f4fe6417e10e39dc9b1f71'}
REVIEW={'bytes':156078207,'sha256':'212d2f0886cb09cddb119470ba908e2142bb141a6eb6bdca83a3e5f83b82cbcb'}
OLD={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d,k;d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 assert n and n==str(PurePosixPath(n)) and not PurePosixPath(n).is_absolute() and '\\' not in n and '\x00' not in n and all(x not in ('','.','..') for x in n.split('/'));return n
def unpack(raw,dest,pin,count):
 assert identity(raw)==pin;dest.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  info=z.infolist();names=[safe(i.filename) for i in info];assert len(names)==len(set(names))==count
  assert not (set(names)&{str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'})
  for i in info:assert i.filename==i.orig_filename and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1
  manifest=js(z.read('MANIFEST.json'));assert set(names)==set(manifest)|{'MANIFEST.json'}
  for n in names:
   b=z.read(n)
   if n in manifest:assert identity(b)==manifest[n],n
   p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 return manifest
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode);m=js((root/'MANIFEST.json').read_bytes());names=set(m)|{'MANIFEST.json'};dirs={str(p) for n in names for p in PurePosixPath(safe(n)).parents if str(p)!='.'};seen=set();found=set()
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(root).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in dirs;seen.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in names,n;found.add(n)
 walk(root);assert found==names and seen==dirs
 for n,pin in m.items():assert identity((root/n).read_bytes())==pin,n
 return {'root':str(root),'files':len(found),'directories':len(seen),'manifest':identity((root/'MANIFEST.json').read_bytes()),'exact_membership_types_hashes':'PASS'}
def main():
 AREA.mkdir(parents=True,exist_ok=False);pkg=AREA/'package';prior=AREA/'prior-review';root=AREA/'recovered'
 manifest=unpack(INPUT.read_bytes(),pkg,PIN,57);print('outer archive CRC, safe membership, 56 hashes PASS',flush=True)
 reviewraw=(pkg/'retained/Formal-Lab6-I164-exceptional-cleanup-append-independent-review.zip').read_bytes();rm=unpack(reviewraw,prior,REVIEW,85)
 oldraw=(prior/'input/I164-exceptional-cleanup-append-correspondence-1.zip').read_bytes();oldmanifest=unpack(oldraw,root,OLD,3982)
 changes=js((pkg/'overlay/ec01/provenance/changed-files.json').read_bytes())['intentional_existing_file_changes'];assert set(changes)=={'code/correspondence.py','code/managed_coverage.py','tests/cases.py'}
 om=js((pkg/'OVERLAY-MANIFEST.json').read_bytes());newmanifest=js((pkg/'ROOT-MANIFEST.json').read_bytes());assert len(om)==20
 assert {n.removeprefix('overlay/') for n in manifest if n.startswith('overlay/')}==set(om)
 assert set(newmanifest)==set(oldmanifest)|set(om)
 assert {n for n in oldmanifest if newmanifest[n]!=oldmanifest[n]}==set(changes)
 diffs=[]
 for n,pin in om.items():
  safe(n);raw=(pkg/'overlay'/n).read_bytes();assert identity(raw)==pin==newmanifest[n]
  if n in oldmanifest:
   assert identity((root/n).read_bytes())==changes[n]['before']==oldmanifest[n] and pin==changes[n]['after'];assert (pkg/'overlay/ec01/original'/n).read_bytes()==(root/n).read_bytes()
   diffs.append(''.join(difflib.unified_diff((root/n).read_text().splitlines(True),raw.decode().splitlines(True),fromfile='historical/'+n,tofile='corrected/'+n)))
  else:assert n.startswith('ec01/') and not (root/n).exists()
  p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 (root/'MANIFEST.json').write_bytes((pkg/'ROOT-MANIFEST.json').read_bytes())
 # Source byte changes are bounded exactly, independently of the declared diff.
 oldp=(root/'ec01/original/code/managed_coverage.py').read_bytes();newp=(root/'code/managed_coverage.py').read_bytes();before=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True if terminal=='raise' else False";after=b"'terminal_python_exception_in_model':None if terminal in ('process-termination','unobserved') else True"
 assert oldp.count(before)==1 and oldp.replace(before,after)==newp
 olda=(root/'ec01/original/code/correspondence.py').read_bytes();newa=(root/'code/correspondence.py').read_bytes();assert olda.replace(repr(identity(oldp)).encode(),repr(identity(newp)).encode())==newa
 oldt=(root/'ec01/original/tests/cases.py').read_bytes();newt=(root/'tests/cases.py').read_bytes();addition=b" # EC-01: lab_bootstrap.py:167-171 remains in the constructor-error handler.\n # A normal cleanup append does not establish normal overall return.\n if terminal is None:assert out['terminal_python_exception_in_model'] is True\n";assert newt.count(addition)==1 and newt.replace(addition,b'')==oldt
 declared=(pkg/'overlay/ec01/provenance/implementation.diff').read_text();names=['code/managed_coverage.py','code/correspondence.py','tests/cases.py'];assert declared==''.join(''.join(difflib.unified_diff((root/'ec01/original'/n).read_text().splitlines(True),(root/n).read_text().splitlines(True),fromfile='historical/'+n,tofile='corrected/'+n)) for n in names)
 oldreceipt=(root/'results/recovered/cleanup-append.json').read_bytes();newreceipt=(root/'ec01/receipts/prepared-cleanup-append.json').read_bytes();oldv=js(oldreceipt);newv=js(newreceipt);expected=js(oldreceipt)
 for name in ('managed_coverage.py','correspondence.py'):expected['extension_components'][name]=identity((root/'code'/name).read_bytes())
 canonical=lambda v:(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();assert canonical(expected)==newreceipt
 assert oldreceipt==(root/'results/primary/cleanup-append.json').read_bytes()
 for n in ('EC01-smallest-case.json','EC01-accepted-result.json','EC01-source-consistent-one-field-output.json','EC01-witness.json'):assert (root/'ec01/witnesses'/n).read_bytes()==(prior/'review/results/public-recovered'/n).read_bytes()
 assert (root/'ec01/original/MANIFEST.json').read_bytes()==(prior/'input/I164-exceptional-cleanup-append-correspondence-1.zip').read_bytes()[:0]+enc(oldmanifest) or js((root/'ec01/original/MANIFEST.json').read_bytes())==oldmanifest
 result={'input':PIN,'outer_entries':57,'manifested_hashes':56,'CRC':'PASS','safe_membership':'PASS','retained_review':REVIEW,'retained_review_entries':85,'original_candidate':OLD,'original_candidate_entries':3982,'declared_overlay_members':20,'new_ec01_files':17,'existing_changed_files':changes,'only_claimed_three_changes':True,'all_other_original_members_unchanged':len(oldmanifest)-3,'root':verify_root(root),'unchanged_LD01_predecessor':verify_root(root/'retained/details'),'historical_receipt':identity(oldreceipt),'corrected_receipt':identity(newreceipt),'receipt_change_paths':['extension_components.managed_coverage.py','extension_components.correspondence.py'],'preparation_is_validation':False,'retained_witnesses_unchanged':True,'candidate_or_validator_executions':0}
 (BASE/'ec01-review/results/intake.json').write_bytes(enc(result));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
