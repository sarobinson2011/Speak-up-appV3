"""Recover only byte identities; no candidate validation, tests or application execution."""
from bytes_only import B,fid,read,save,tree
import subprocess,sys,time,shutil,ast
from datetime import datetime,timezone
h=B/'host';source=B/'source';prior=B/'prior-review';plan=read(h/'PLAN.json')
wrapper=prior/'recover_for_inspection.py';cmd=[sys.executable,'-I','-B',str(wrapper),'--launcher',str(B/'inputs/I164-helper-open-persistent-host-launcher-review-2.zip'),'--destination',str(B/'parent-recovered')]
save(B/'byte-recovery-launch.json',{'command':cmd,'timeout_seconds':360,'code':fid(wrapper),'candidate_invocations':0,'utc':datetime.now(timezone.utc).isoformat()})
t=time.monotonic();timeout=False
with (B/'byte-recovery.stdout').open('xb') as out,(B/'byte-recovery.stderr').open('xb') as err:
 try:rc=subprocess.run(cmd,stdout=out,stderr=err,timeout=360).returncode
 except subprocess.TimeoutExpired:rc=None;timeout=True
save(B/'byte-recovery-exit.json',{'returncode':rc,'timed_out':timeout,'seconds':time.monotonic()-t})
assert rc==0 and not timeout
root=B/'candidate';shutil.copytree(source,root);(root/'retained').mkdir();(B/'parent-recovered/candidate').rename(root/'retained/enter')
old=root/'retained/enter';records={}
records['root']=tree(root,read(h/'expected/ASSEMBLED-ROOT-MANIFEST.json'))
assert records['root']=={'files':4222,'directories':1183,'exact_types_membership_hashes':'PASS'}
assert fid(h/'expected/ASSEMBLED-ROOT-MANIFEST.json')==plan['assembled_root_manifest']
assert read(root/'reference/enter/ASSEMBLED-ROOT-MANIFEST.json')==read(B/'parent-recovered/host/expected/ASSEMBLED-ROOT-MANIFEST.json')
assert (h/'code/recovery.py').read_bytes()==(B/'parent-recovered/host/code/recovery.py').read_bytes()
changes=read(root/'CHANGES.json');before=(old/'code/managed_coverage.py').read_bytes();after=(root/'code/managed_coverage.py').read_bytes()
assert len(before)==440168 and after.startswith(before)
funcs=[n.name for n in ast.parse(after[len(before):]).body if isinstance(n,ast.FunctionDef)]
assert funcs==changes['new_functions'] and len(funcs)==changes['new_function_count']==5
for n,v in changes['intentional_implementation_changes'].items():assert fid(root/n)==v['after'] and fid(old/n)==v['before']
for name in ('managed_coverage.py','correspondence.py'):
 assert (root/'reference/enter/code'/name).read_bytes()==(old/'code'/name).read_bytes()==(prior/'inspected/code'/name).read_bytes()
for name in ('bytecodes.c','typeobject.c','compound_stmts.rst','LICENSE'):assert (root/'reference/cpython-3.12.14'/name).read_bytes()==(old/'reference/cpython-3.12.14'/name).read_bytes()
assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(old/'source-evidence/lab_bootstrap.py').read_bytes()
for n,pin in read(root/'provenance/component-pins.json').items():assert fid(root/n)==pin,n
for p in (root/'reference/review').iterdir():assert p.read_bytes()==(prior/p.name).read_bytes(),p.name
for p in (h/'observer-reference').iterdir():assert p.read_bytes()==(B/'parent-recovered/recovered-helper/harness'/p.name).read_bytes(),p.name
for p in (root/'fixtures/retained-enter').glob('*.json'):assert p.read_bytes()==(prior/'independent/fixtures'/p.name).read_bytes(),p.name
records.update({'current_producer':fid(root/'code/managed_coverage.py'),'current_adapter':fid(root/'code/correspondence.py'),'producer_prefix':fid(old/'code/managed_coverage.py'),'new_functions':funcs,'appended_bytes':len(after)-len(before),'all_4169_parent_members_unchanged':True,'defining_runtime_and_cpython_sources_unchanged':True,'observer_files_unchanged':True,'review_excerpts_and_constructed_parent_fixtures':'exact verified prior review bytes','actual_parent_manifest':fid(root/'reference/enter/ASSEMBLED-ROOT-MANIFEST.json'),'current_manifest':fid(h/'expected/ASSEMBLED-ROOT-MANIFEST.json'),'candidate_execution':0,'recovery_records':'parent-recovered/recovery-verification.json, recovery-exit.json, recovered-helper/byte-origins.json'})
save(B/'source-recovery-audit.json',records);save(B/'source-recovery-audit.exit.json',{'exit':0,'failure':None});print(records,flush=True)
