from pathlib import Path
import json,zipfile,importlib.util,shutil,ast,hashlib
from verify_inputs_corrected import ident,zip_verify
B=Path(__file__).resolve().parent;H=B/'host';plan=json.loads((H/'PLAN.json').read_text())
def load(n):
 p=H/'code'/f'{n}.py';s=importlib.util.spec_from_file_location('review_bytes_'+n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 common=load('common_r1');rec=load('recovery')
 assert ident(H/'code/recovery.py')=={'bytes':7152,'sha256':'e5b7d25fe9092732468b3954fa46a1bc8d818530d1ca2365a6e228c8a92c2428'}
 large=B/'inputs/I164-helper-open-persistent-host-launcher-review-2.zip';assert ident(large)==plan['launcher_archive']
 audits={'large':zip_verify(large)}
 with zipfile.ZipFile(large) as z:
  for n in ('prerun','progress'):
   p=B/'inputs'/f'{n}.zip';p.write_bytes(z.read('inputs/'+n+'.zip'));assert ident(p)==rec.PINS[n]
 audits['helper']=rec.recover(B/'inputs/prerun.zip',B/'inputs/progress.zip',B/'recovered-helper')
 root=B/'candidate';common.unzip(H/'inputs/I164-exit-decref-attempt-1-source.zip',root,plan['source_archive'])
 current=root;roots={};files=[('res-null','I164-res-null-test-1-source.zip','res_null'),('fast','I164-decref-fast-completion-1-source.zip','fast'),('decref','I164-enter-decref-attempt-1-source.zip','decref'),('return','I164-enter-return-res-1-source.zip','return'),('enter','I164-enter-call-attempt-1-source.zip','enter')]
 for name,filename,key in files:
  dest=current/'retained'/name;dest.parent.mkdir();common.unzip(H/'inputs'/filename,dest,plan[key+'_source_archive']);roots[key]=dest;current=dest
 for name,filename,key in [('lookup','reference/lookup/I164-context-special-lookup-1-source.zip','lookup'),('r1','reference/r1/I164-open-return-reconstruction-1-source.zip','r1')]:
  dest=current/'retained'/name;dest.parent.mkdir();common.unzip(current/filename,dest,plan[key+'_source_archive']);roots[key]=dest;current=dest
 (current/'retained').mkdir();(B/'recovered-helper/candidate').rename(current/'retained/helper-open')
 audits['roots']={}
 for key,r in reversed(list(roots.items())):
  stem='RES-NULL' if key=='res_null' else key.upper();mp=H/'expected'/f'{stem}-ROOT-MANIFEST.json'
  assert ident(mp)==plan[key+'_root_manifest'];audits['roots'][key]=common.exact_tree(r,json.loads(mp.read_text()))
  assert audits['roots'][key]['files']==plan[key+'_files'] and audits['roots'][key]['directories']==plan[key+'_directories']
 audits['roots']['current']=common.exact_tree(root,json.loads((H/'expected/ASSEMBLED-ROOT-MANIFEST.json').read_text()))
 assert audits['roots']['current']['files']==4963 and audits['roots']['current']['directories']==1264
 parent=roots['res_null'];ch=json.loads((root/'CHANGES.json').read_text())
 for n,row in ch['changed_implementation'].items():assert ident(root/n)==row['after'] and ident(parent/n)==row['before']
 raw=(root/'code/managed_coverage.py').read_bytes();old=(parent/'code/managed_coverage.py').read_bytes();assert len(old)==519785 and raw[:len(old)]==old
 a=ast.parse(raw);o=ast.parse(old);assert [ast.dump(x) for x in a.body[:len(o.body)]]==[ast.dump(x) for x in o.body]
 added=[x.name for x in a.body[len(o.body):]];assert added==ch['appended_functions'] and len(added)==7
 assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(parent/'source-evidence/lab_bootstrap.py').read_bytes()
 for p in (parent/'reference/resolution/source').rglob('*'):
  if p.is_file():assert p.read_bytes()==(root/p.relative_to(parent)).read_bytes()
 assert (root/'reference/res-null/correspondence.py').read_bytes()==(parent/'code/correspondence.py').read_bytes()
 audits['inheritance']={'prefix_bytes':len(old),'appended_functions':added,'declared_changes':ch,'runtime_and_resolution_sources_unchanged':True,'actual_parent_adapter_unchanged':True}
 (B/'recovery-audit.json').write_text(json.dumps(audits,indent=2)+'\n');print(json.dumps(audits,indent=2))
if __name__=='__main__':main()
