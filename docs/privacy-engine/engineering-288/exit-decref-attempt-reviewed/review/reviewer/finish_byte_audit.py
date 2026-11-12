from recover_bytes import B,H,plan,load,ident
import ast,json
common=load('common_r1');root=B/'candidate';parent=root/'retained/res-null'
audit={'previous_recovery_exit':json.loads((B/'recovery.exit.json').read_text()),'qualification':'Byte recovery completed; original final audit used reference/res-null/correspondence.py instead of reference/res-null/code/correspondence.py. No candidate validation executed. Recovery not repeated.','roots':{}}
r=root
for key,part in [('assembled',None),('res_null','res-null'),('fast','fast'),('decref','decref'),('return','return'),('enter','enter'),('lookup','lookup'),('r1','r1')]:
 if part:r=r/'retained'/part
 stem='RES-NULL' if key=='res_null' else key.upper();mp=H/'expected'/f'{stem}-ROOT-MANIFEST.json';assert ident(mp)==plan[key+'_root_manifest']
 audit['roots'][key]=common.exact_tree(r,json.loads(mp.read_text()))
ch=json.loads((root/'CHANGES.json').read_text())
for n,row in ch['changed_implementation'].items():assert ident(root/n)==row['after'] and ident(parent/n)==row['before']
raw=(root/'code/managed_coverage.py').read_bytes();old=(parent/'code/managed_coverage.py').read_bytes();assert len(old)==519785 and raw[:len(old)]==old
a=ast.parse(raw);o=ast.parse(old);assert [ast.dump(x) for x in a.body[:len(o.body)]]==[ast.dump(x) for x in o.body]
added=[x.name for x in a.body[len(o.body):]];assert added==ch['appended_functions'] and len(added)==7
assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(parent/'source-evidence/lab_bootstrap.py').read_bytes()
source_count=0
for p in (parent/'reference/resolution/source').rglob('*'):
 if p.is_file():assert p.read_bytes()==(root/p.relative_to(parent)).read_bytes();source_count+=1
for n in ('correspondence.py','managed_coverage.py'):assert (root/'reference/res-null/code'/n).read_bytes()==(parent/'code'/n).read_bytes()
audit.update({'status':'PASS','prefix_bytes':len(old),'appended_functions':added,'declared_changes':ch,'source_resolution_files_unchanged':source_count,'runtime_and_actual_parent_unchanged':True})
(B/'recovery-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({'status':'PASS','roots':audit['roots'],'added':added}))
