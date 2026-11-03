"""Save corrected replacement and exact available results before public validation."""
from pathlib import Path
import json,hashlib,zipfile,stat,datetime,os
W=Path(__file__).resolve().parents[1];R=W/'corrected/root';D=W/'active-checkpoint-records'
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 D.mkdir();m=json.loads((R/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};files=set();dirs=set();edirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'}
 def walk(p):
  for e in os.scandir(p):
   q=Path(e.path);n=q.relative_to(R).as_posix();mode=e.stat(follow_symlinks=False).st_mode
   if stat.S_ISDIR(mode):assert n in edirs;dirs.add(n);walk(q)
   else:assert stat.S_ISREG(mode) and n in expected;files.add(n)
 walk(R);assert files==expected and dirs==edirs
 for n,pin in m.items():assert ident((R/n).read_bytes())==pin,n
 result=json.loads((W/'results/replacement-source-corrected/RESULT.json').read_bytes());ex=json.loads((W/'processes/replacement-source-corrected/exit.json').read_bytes());assert result['result']=='PASS' and ex['exit']==0 and not ex['timed_out']
 progress=[json.loads(x) for x in (W/'results/replacement-source-corrected/progress.jsonl').read_text().splitlines()];stdout=[json.loads(x[6:]) for x in (W/'processes/replacement-source-corrected/stdout.log').read_text().splitlines() if x.startswith('CHECK ')];individual=[json.loads(p.read_bytes()) for p in sorted((W/'results/replacement-source-corrected/rows').glob('*.json'))];assert result['rows']==progress==stdout==individual
 source={'result':'PASS','RESULT_rows':len(result['rows']),'progress_rows':len(progress),'stdout_rows':len(stdout),'individual_rows':len(individual),'all_four_agree':True,'exit':ex,'kinds':{k:sum(x['result']==k for x in result['rows']) for k in ('PASS','REJECTED')},'layer':'source/saved-parent constructed checks; no predecessor authentication','prior_36_checks_reused':False}
 additions={n:pin for n,pin in m.items() if not n.startswith('retained/')};(D/'ADDITIONS-MANIFEST.json').write_bytes(enc(additions));(D/'ROOT-MANIFEST.json').write_bytes((R/'MANIFEST.json').read_bytes())
 cp={'format':'I164-LINE174-NEW-REPLACEMENT-PRERUN-2','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'SOURCE CHECKS COMPLETED; PUBLIC VALIDATION NOT STARTED','independent_review':'PENDING','baseline_review':json.loads((W/'CHECKPOINT.json').read_bytes())['baseline_review'],'confirmed_git_save':'88c9fba36bdb243212439acd3027ea934ceda115','Git_operations':0,'root_manifest':ident((R/'MANIFEST.json').read_bytes()),'files':len(files),'directories':len(dirs),'active_files':additions,'source_controls':source,'new_public_attempts':0,'preserved_zero_control_failure':json.loads((W/'results/replacement-source/RESULT.json').read_bytes()),'receipt_format_correction':json.loads((W/'provenance/receipt-format-correction.json').read_bytes()),'initial_checkpoint':json.loads((W/'provenance/prerun-library-save.json').read_bytes()),'environment':json.loads((W/'provenance/execution-environment-qualification.json').read_bytes()),'old_attempt_outcomes':'UNKNOWN; missing bytes not recreated','scope':'line174 evaluation and call attempt; body excluded','authority':'Both acquisitions;11 obligations;4/14 UNKNOWN;DecisionB/retention/allowances unchanged;SOURCE-ONLY;cumulative-envelope unadopted;backup kernel-only;streams UNCOMPUTED;readiness/final binding blocked;admission disabled'}
 (D/'CHECKPOINT.json').write_bytes(enc(cp));package={n:D/n for n in ('CHECKPOINT.json','ADDITIONS-MANIFEST.json','ROOT-MANIFEST.json')}
 for n in ('README.txt','RECOVERY.txt','HISTORY.txt'):package[n]=W/n
 for n in additions:package['root-additions/'+n]=R/n
 package['retained/cleanup-loop-review.zip']=W.parent/'upload/Formal-Lab6-I164-cleanup-loop-exhaustion-independent-review(2).zip'
 for folder in ('provenance','failures','results','processes'):
  for p in sorted((W/folder).rglob('*')):
   if p.is_file():package['new/'+p.relative_to(W).as_posix()]=p
 for p in (W/'tools').glob('*.py'):package['tools/'+p.name]=p
 package['INITIAL-PRERUN-IDENTITY.json']=W/'PRERUN-IDENTITY.json'
 manifest={n:ident(p.read_bytes()) for n,p in package.items()};target=W/'I164-line174-NEW-replacement-prerun-2.zip';assert not target.exists()
 with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,p in sorted(package.items()):
   b=p.read_bytes();assert ident(b)==manifest[n];zi=zipfile.ZipInfo(n,(2026,11,3,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,b)
  zi=zipfile.ZipInfo('MANIFEST.json',(2026,11,3,0,0,0));zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,enc(manifest))
 with zipfile.ZipFile(target) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(manifest)+1 and z.testzip() is None
  for n,pin in manifest.items():assert ident(z.read(n))==pin
 out={'name':target.name,**ident(target.read_bytes()),'entries':len(manifest)+1,'CRC_membership_hashes':'PASS','status':cp['status'],'source_controls':source};(W/'PRERUN2-IDENTITY.json').write_bytes(enc(out));print(json.dumps({k:v for k,v in out.items() if k!='source_controls'},indent=2),flush=True)
if __name__=='__main__':main()
