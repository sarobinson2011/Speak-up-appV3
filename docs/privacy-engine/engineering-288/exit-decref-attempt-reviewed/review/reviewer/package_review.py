from pathlib import Path
import json,zipfile,hashlib,stat
from verify_inputs_corrected import zip_verify
B=Path(__file__).resolve().parent;H=B/'host';out=B/'I164-exit-decref-attempt-1-independent-review.zip';files={}
def add(p,n):
 assert p.is_file() and not p.is_symlink() and n not in files,(p,n);files[n]=p
for n in ('REVIEW.txt','RECOVERY.txt','CHECKPOINT.json','INPUTS.json','FAILURES.json'):add(B/n,n)
for p in B.glob('*.py'):add(p,'reviewer/'+p.name)
for p in B.iterdir():
 if p.is_file() and p.name not in ('CHECKPOINT.json','INPUTS.json','FAILURES.json','delivery-identity.json') and p.suffix in ('.json','.stdout','.stderr'):
  add(p,'audits/'+p.name)
for p in (B/'independent').rglob('*'):
 if p.is_file():add(p,'independent/'+p.relative_to(B/'independent').as_posix())
for n in ('I164-exit-decref-attempt-1-source.zip','I164-exit-decref-attempt-1-results.zip'):add(H/'inputs'/n,'inputs/'+n)
for n in ('CHECKPOINT.json','REVIEW.txt','RECOVERY.txt','FAILURES.json','INPUTS.json','MANIFEST.json'):add(B/'parent-review'/n,'prior-review/'+n)
for n in ('AUTHENTICATION-PATH.txt','CHANGES.json','CHECKPOINT.json','FAILURES.json','INPUTS.json','PLAN.json','PREPARED.json','RECOVERY.txt','START-HERE.txt','MANIFEST.json','EXPORT-MANIFEST.json','EXPORT-STATUS.json','ONE-ATTEMPT-RESERVATION.json','LAUNCH-RECEIPT.json','service-exit.json','manager-exit.json','service-runtime-profile.json','service-root-verification.json','host-profile.stdout','host-profile.stderr','host-profile.exit.json','byte-recovery.stdout','byte-recovery.stderr','byte-recovery.exit.json','assembled-root.json','preparation-launch.json','service-launch.stdout','service-launch.stderr','service-launch.exit.json','service.stdout','service.stderr'):
 add(H/n,'saved-host/'+n)
for folder in ('validation','code','observer-reference','expected','preparation-records'):
 for p in (H/folder).rglob('*'):
  if p.is_file():add(p,'saved-host/'+p.relative_to(H).as_posix())
for n in ('byte-origins.json','recovery-result.json'):add(B/'recovered-helper'/n,'byte-recovery/'+n)
manifest={n:{'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for n,p in sorted(files.items())}
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.writestr('MANIFEST.json',json.dumps(manifest,indent=2,sort_keys=True)+'\n')
result=zip_verify(out);result['filename']=out.name
(B/'delivery-identity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
