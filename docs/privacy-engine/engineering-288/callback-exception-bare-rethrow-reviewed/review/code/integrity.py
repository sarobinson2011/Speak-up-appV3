import argparse,hashlib,json,os,stat,zipfile
from pathlib import Path,PurePosixPath
PIN={'bytes':88596749,'sha256':'c24b08d598115b1118121aeb6c9d42bbdd780a58a98375a29b96224e8c825876'}
PRIOR_MANIFEST={'bytes':819714,'sha256':'dd9371b8c8520a3950f3fc26915884be9e0f2f6239a97ab7c6dbd00d6323223a'}
NEW_PLAN='''FINAL-RECOVERY-NOTES.txt MANIFEST.json PRIMARY-LOG-RECONCILIATION.txt README.md RECOVERY.md RESULTS.json SEMANTICS.md code/correspondence.py code/managed_coverage.py failures/packaging-reconciliation/RESULT.json failures/packaging-reconciliation/freeze-original.py failures/packaging-reconciliation/observation.json failures/packaging-reconciliation/packaging-failure.txt failures/packaging-reconciliation/primary.log failures/packaging-reconciliation/progress.jsonl failures/process-membership/EVIDENCE.json failures/process-membership/public/RESULT.json failures/process-membership/public/calls.json failures/process-membership/public/failure.txt failures/process-membership/public/stdout.log failures/process-membership/recovered/RESULT.json failures/process-membership/recovered/calls.json failures/process-membership/recovered/failure.txt failures/process-membership/recovered/stdout.log failures/process-membership/undeclared-partial.bin provenance/changed-files.json provenance/clean-recovery-identity.json provenance/intake.json provenance/intentional.diff provenance/primary-input-manifest.json provenance/primary-reconciliation.json provenance/prior-review.json provenance/recovery-cut-identity.json provenance/recovery-cut-manifest.json provenance/recovery-cut-note.txt results/primary/RESULT.json results/primary/callback-bare-rethrow.json results/primary/calls.json results/primary/final-verification.json results/primary/fixtures.json results/primary/input-verification.json results/primary/progress.jsonl results/primary/receipt-identity.json results/primary/stdout.log results/public/CLI-result.json results/public/CLI.stdout results/public/RESULT.json results/public/calls.json results/public/final-verification.json results/public/input-verification.json results/public/progress.jsonl results/public/stdout.log results/recovered/RESULT.json results/recovered/calls.json results/recovered/final-verification.json results/recovered/input-verification.json results/recovered/progress.jsonl results/recovered/stdout.log source-evidence/lab_bootstrap.py source-evidence/live_connection.py source-evidence/prospective_entry.py tests/cases.py tests/focused.py tests/offline.py tests/process_checks.py tools/checkpoint.py'''.split()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate-key:'+k)
  d[k]=v
 return d
def parse(b):return json.loads(b,object_pairs_hook=unique)
def safe(n):
 p=PurePosixPath(n)
 assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==n and '\\' not in n and ':' not in n and n not in ('','.')
def verify_root(root):
 root=Path(root);assert stat.S_ISDIR(root.lstat().st_mode)
 m=parse((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in PurePosixPath(n).parents if p.as_posix()!='.'};seen=set();files=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds:
   p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(root).as_posix())
  for n in fs:
   p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
 assert files==expected and seen==dirs,(sorted(files-expected),sorted(expected-files),sorted(seen-dirs))
 for n,v in m.items():assert identity((root/n).read_bytes())==v,n
 return {'files':len(files),'directories':len(dirs),'safe_exact_membership':'PASS','hashes':'PASS'}
def verify(archive,dest):
 p=Path(archive);assert identity(p.read_bytes())==PIN
 with zipfile.ZipFile(p) as z:
  entries=z.infolist();names=[x.filename for x in entries];assert len(names)==2938 and len(set(names))==len(names)
  for i in entries:safe(i.filename);assert stat.S_ISREG(i.external_attr>>16) and not i.is_dir() and not i.flag_bits&1
  assert z.testzip() is None
  raw=z.read('MANIFEST.json');m=parse(raw);assert len(m)==2937 and set(names)==set(m)|{'MANIFEST.json'}
  oldraw=z.read('retained/callback/MANIFEST.json');assert identity(oldraw)==PRIOR_MANIFEST;old=parse(oldraw)
  reviewraw=z.read('retained/review/MANIFEST.json');review=parse(reviewraw)
  oldplan={'retained/callback/'+n for n in set(old)|{'MANIFEST.json'}}
  reviewplan={'retained/review/'+n for n in set(review)|{'MANIFEST.json'} if not n.startswith('input/')}
  assert len(oldplan)==2807 and len(reviewplan)==65 and len(NEW_PLAN)==66
  assert set(names)==oldplan|reviewplan|set(NEW_PLAN)
  for n,v in old.items():assert m['retained/callback/'+n]==v
  for n,v in review.items():
   if not n.startswith('input/'):assert m['retained/review/'+n]==v
  for n in names:
   b=z.read(n)
   if n!='MANIFEST.json':assert identity(b)==m[n],n
  dest=Path(dest);dest.mkdir(parents=True,exist_ok=False)
  for n in names:
   q=dest/n;q.parent.mkdir(parents=True,exist_ok=True)
   with q.open('xb') as f:f.write(z.read(n))
  return {'archive':PIN,'entries':len(names),'manifested_hashes':len(m),'manifest':identity(raw),'CRC':'PASS','composition_plan':'2807 predecessor + 65 retained review + 66 current = 2938','safe_exact_membership':'PASS','predecessor_manifest':identity(oldraw),'prior_review_manifest':identity(reviewraw),'root':verify_root(dest)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--root',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=verify(a.archive,a.root);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
