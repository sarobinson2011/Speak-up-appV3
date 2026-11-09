"""Optional future byte-only recovery into a NEW directory. No validation/host launch.
Run only to recover lost bytes, not as a reason to replay completed checks.
"""
from pathlib import Path
import argparse,sys,shutil,subprocess,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from review_bytes import fid,read,save,untar_host,unzip,verify_tree
p=argparse.ArgumentParser();p.add_argument('--launcher',type=Path,required=True);p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;dest=a.destination.resolve();dest.mkdir(exist_ok=False)
main=base/'inputs/I164-enter-call-attempt-public-1-host-evidence.tar.gz'
records={'host':untar_host(main,dest/'host')};h=dest/'host';deps=read(h/'DEPENDENCIES.json');plan=read(h/'PLAN.json')
for key,target in [('source','source'),('results','focused')]:
 d=deps[key];records[key]=unzip(h/d['included'],dest/target,{k:d[k] for k in ('bytes','sha256')})
d=deps['external_recovery_archive'];records['launcher']=unzip(a.launcher.resolve(),dest/'launcher',{k:d[k] for k in ('bytes','sha256')})
recovery=h/'code/recovery.py';assert fid(recovery)=={'bytes':7152,'sha256':'e5b7d25fe9092732468b3954fa46a1bc8d818530d1ca2365a6e228c8a92c2428'}
assert recovery.read_bytes()==(dest/'launcher/code/recovery.py').read_bytes()
cmd=[sys.executable,'-I','-B',str(recovery),str(dest/'launcher/inputs/prerun.zip'),str(dest/'launcher/inputs/progress.zip'),str(dest/'recovered-helper')]
save(dest/'recovery-launch.json',{'command':cmd,'timeout_seconds':300,'no_candidate_imports':True})
t=time.monotonic();timeout=False
with (dest/'recovery.stdout').open('xb') as out,(dest/'recovery.stderr').open('xb') as err:
 try:rc=subprocess.run(cmd,stdout=out,stderr=err,timeout=300).returncode
 except subprocess.TimeoutExpired:rc=None;timeout=True
save(dest/'recovery-exit.json',{'returncode':rc,'timed_out':timeout,'seconds':time.monotonic()-t})
assert rc==0 and not timeout
root=dest/'candidate';shutil.copytree(dest/'source',root);lookup=root/'retained/lookup'
unzip(root/'reference/lookup/I164-context-special-lookup-1-source.zip',lookup,plan['lookup_source_archive'])
r1=lookup/'retained/r1';unzip(lookup/'reference/r1/I164-open-return-reconstruction-1-source.zip',r1,plan['r1_source_archive'])
(r1/'retained').mkdir();(dest/'recovered-helper/candidate').rename(r1/'retained/helper-open')
records['root']=verify_tree(root,read(h/'expected/ASSEMBLED-ROOT-MANIFEST.json'))
save(dest/'recovery-verification.json',records)
print('Byte-only recovery verified; no public validation, application or control replay.')
