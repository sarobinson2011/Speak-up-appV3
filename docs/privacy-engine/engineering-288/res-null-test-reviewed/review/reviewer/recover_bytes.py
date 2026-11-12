"""New root assembly from already verified saved predecessor, bytes only."""
from bytes_only import *
import shutil,ast
H=B/'host';old=B.parent/'fast-review';R=B/'candidate';plan=read(H/'PLAN.json')
try:
 dep=read(B/'source/DEPENDENCIES.json')['inputs']['independent_review']
 assert fid(old/dep['filename'])=={k:dep[k] for k in ('bytes','sha256')}
 assert read(old/'final-audit.exit.json')['exit']==0
 assert fid(old/'host/expected/ASSEMBLED-ROOT-MANIFEST.json')==plan['fast_root_manifest']
 assert fid(old/'host/inputs/I164-decref-fast-completion-1-source.zip')==plan['fast_source_archive']
 assert (H/'inputs/I164-decref-fast-completion-1-source.zip').read_bytes()==(old/'host/inputs/I164-decref-fast-completion-1-source.zip').read_bytes()
 # Recheck identities of the reused bytes, not completed semantic checks.
 oldtree=tree(old/'candidate',read(H/'expected/FAST-ROOT-MANIFEST.json'))
 shutil.copytree(B/'source',R);shutil.copytree(old/'candidate',R/'retained/fast')
 out={'reused_parent':oldtree,'assembled':tree(R,read(H/'expected/ASSEMBLED-ROOT-MANIFEST.json'))}
 assert out['assembled']['files']==4729 and out['assembled']['directories']==1238
 assert fid(H/'expected/ASSEMBLED-ROOT-MANIFEST.json')==plan['assembled_root_manifest']
 p=R/'retained/fast';ch=read(R/'CHANGES.json');before=(p/'code/managed_coverage.py').read_bytes();after=(R/'code/managed_coverage.py').read_bytes()
 assert len(before)==505497 and after.startswith(before)
 funcs=[x.name for x in ast.parse(after[len(before):]).body if isinstance(x,ast.FunctionDef)]
 assert funcs==ch['appended_functions'] and len(funcs)==7
 for n,pins in ch['changed_implementation'].items():assert fid(R/n)==pins['after'] and fid(p/n)==pins['before']
 for name in ('managed_coverage.py','correspondence.py'):assert (R/'reference/fast/code'/name).read_bytes()==(p/'code'/name).read_bytes()
 for folder in ('source-evidence','reference/cpython-3.12.14','reference/resolution/source'):
  for x in (R/folder).rglob('*'):
   if x.is_file():assert x.read_bytes()==(p/x.relative_to(R)).read_bytes(),str(x)
 for n,pin in read(R/'provenance/component-pins.json').items():assert fid(R/n)==pin,n
 assert (R/'reference/fast/actual-receipt.json').read_bytes()==(old/'host/validation/results/actual-derived-receipt.json').read_bytes()
 assert fid(R/'reference/fast/actual-receipt.json')==plan['fast_receipt']
 for x in (H/'observer-reference').iterdir():assert x.read_bytes()==(old/'host/observer-reference'/x.name).read_bytes()
 for tag in ('FAST','DECREF','RETURN','ENTER','LOOKUP','R1'):
  assert fid(H/'expected'/(tag+'-ROOT-MANIFEST.json'))==plan[tag.lower()+'_root_manifest']
 out.update({'producer':fid(R/'code/managed_coverage.py'),'adapter':fid(R/'code/correspondence.py'),'unchanged_prefix':fid(p/'code/managed_coverage.py'),'appended_functions':funcs,'parent_files_preserved':4500,'runtime_source_bytes_unchanged':True,'observer_files_unchanged':True,'actual_parent_receipt_bytes_reused':True,'reused_review':{k:dep[k] for k in ('filename','library_file_id','bytes','sha256')},'candidate_imports':0,'old_campaigns_replayed':0})
 save(B/'source-recovery-audit.json',out);save(B/'source-recovery-audit.exit.json',{'exit':0});print(json.dumps(out),flush=True)
except BaseException as e:save(B/'source-recovery-audit.exit.json',{'exit':1,'failure':repr(e)});raise
