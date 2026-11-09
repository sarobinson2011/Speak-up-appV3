"""Byte-only recovery: no candidate imports, validators, tests or host launch."""
import subprocess,sys,time,datetime,shutil,ast
from review_bytes import HERE,fid,ident,read,save,unzip,verify_tree
host=HERE/'host';launcher=HERE/'launcher';source=HERE/'source';plan=read(host/'PLAN.json')
recovery=host/'code/recovery.py'
assert fid(recovery)=={'bytes':7152,'sha256':'e5b7d25fe9092732468b3954fa46a1bc8d818530d1ca2365a6e228c8a92c2428'}
assert recovery.read_bytes()==(launcher/'code/recovery.py').read_bytes()
cmd=[sys.executable,'-I','-B',str(recovery),str(launcher/'inputs/prerun.zip'),str(launcher/'inputs/progress.zip'),str(HERE/'recovered-helper')]
save(HERE/'byte-recovery-launch.json',{'command':cmd,'seconds_limit':300,'source':fid(recovery),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_imports':0})
start=time.monotonic()
with (HERE/'byte-recovery.stdout').open('xb') as out,(HERE/'byte-recovery.stderr').open('xb') as err:
    try:
        p=subprocess.run(cmd,stdout=out,stderr=err,timeout=300);ex={'exit':p.returncode,'timed_out':False}
    except subprocess.TimeoutExpired:ex={'exit':None,'timed_out':True}
ex['seconds']=time.monotonic()-start;save(HERE/'byte-recovery-exit.json',ex)
assert ex['exit']==0 and ex['timed_out'] is False,ex
root=HERE/'candidate';shutil.copytree(source,root)
lookup=root/'retained/lookup'
lookupzip=source/'reference/lookup/I164-context-special-lookup-1-source.zip'
lookupinfo=unzip(lookupzip,lookup,plan['lookup_source_archive'])
r1=lookup/'retained/r1'
r1info=unzip(lookup/'reference/r1/I164-open-return-reconstruction-1-source.zip',r1,plan['r1_source_archive'])
(r1/'retained').mkdir();(HERE/'recovered-helper/candidate').rename(r1/'retained/helper-open')
records={}
for n,base,m in [('r1',r1,'R1-ROOT-MANIFEST.json'),('lookup',lookup,'LOOKUP-ROOT-MANIFEST.json'),('candidate',root,'ASSEMBLED-ROOT-MANIFEST.json')]:
    records[n]=verify_tree(base,read(host/'expected'/m));records[n]['manifest']=fid(host/'expected'/m)
assert [(records[k]['files'],records[k]['directories']) for k in ('r1','lookup','candidate')]==[(4090,1142),(4124,1155),(4169,1169)]
old=(lookup/'code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
assert len(old)==429112 and new.startswith(old)
funcs=[n.name for n in ast.parse(new[len(old):]).body if isinstance(n,ast.FunctionDef)];assert len(funcs)==6
for name in ('managed_coverage.py','correspondence.py'):
    assert (root/'reference/lookup/code'/name).read_bytes()==(lookup/'code'/name).read_bytes()
assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(lookup/'source-evidence/lab_bootstrap.py').read_bytes()
for n in ('bytecodes.c','typeobject.c','compound_stmts.rst','LICENSE'):
    assert (root/'reference/cpython-3.12.14'/n).read_bytes()==(lookup/'reference/cpython-3.12.14'/n).read_bytes()
for n,pin in read(root/'provenance/component-pins.json').items():assert fid(root/n)==pin,n
for v in read(root/'CHANGES.json')['intentional_candidate_changes']:
    assert fid(root/v['path'])==v['after'] and fid(lookup/v['path'])==v['before'],v['path']
for p in (host/'observer-reference').iterdir():assert p.read_bytes()==(HERE/'recovered-helper/harness'/p.name).read_bytes(),p.name
review=HERE/'prior-review/context-lookup-review'
for p in (root/'reference/review').iterdir():assert p.read_bytes()==(review/p.name).read_bytes(),p.name
records.update({'byte_recovery_exit':ex,'lookup_source_zip':lookupinfo,'r1_source_zip':r1info,'producer_prefix':ident(old),'new_producer':ident(new),'appended_bytes':len(new)-len(old),'new_functions':funcs,'new_adapter':fid(root/'code/correspondence.py'),'all_4124_predecessor_members':'unchanged','runtime_and_C_sources':'unchanged','review_excerpts':'exact copies from verified prior review','retained_observer':'six files unchanged','candidate_imports':0})
save(HERE/'recovery-audit.json',records);save(HERE/'recovery-audit.exit.json',{'exit':0,'failure':None})
print({k:records[k] for k in ('r1','lookup','candidate','byte_recovery_exit','new_functions')},flush=True)
