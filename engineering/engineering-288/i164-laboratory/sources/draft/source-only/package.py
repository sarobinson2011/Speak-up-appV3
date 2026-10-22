import json,pathlib,hashlib,zipfile
P=pathlib.Path(__file__).resolve().parent;W=P.parent
ident=lambda p:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for name in ['positive','recovered']:
 assert 'PASS SOURCE-ONLY' in (P/'results'/f'{name}.log').read_text()
a=json.loads((P/'results/positive.json').read_bytes());b=json.loads((P/'results/recovered.json').read_bytes());assert a==b
checks={n:len(json.loads((P/'results'/n).read_bytes())) for n in ['mutations.json','disk.json','result-mutations.json']}
new={str(p.relative_to(P)):{'old':None,'new':ident(p),'change':'new companion code only'} for p in (P/'code').glob('*.py')}
(P/'CHANGED-IDENTITIES.json').write_text(json.dumps({'candidate_changes':[],'candidate_members_unchanged':666,'new_code':new,'scope_universe_inputs':'byte-exact original manifest trees; old/new identities equal','candidate_pins_changed':False},indent=2)+'\n')
(P/'SUMMARY.json').write_text(json.dumps({'status':'IMPLEMENTED; pending independent review of manifest and executable integration together','fresh_checks':checks,'final_code_recovered_positive_commands':1,'development_positive_comparison_commands':1,'both_contexts':a['contexts'],'producer_execution':False,'historical_and_review_rerun':False,'candidate_changes':0,'historical_files_preserved':90,'relationships_preserved':43,'obligations_retained':len(a['obligations']),'native_counts':{k:a['consumption'][k] for k in ['family_count','directory_count','relation_duties']},'operational_assurance':False,'global_capacity':None,'readiness':'BLOCKED','final_binding':'BLOCKED','streams':'UNCOMPUTED','admission':False},indent=2)+'\n')
m={str(f.relative_to(P)):ident(f) for f in sorted(P.rglob('*')) if f.is_file() and f!=P/'MANIFEST.json'}
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n');dest=W/'Engineering-288C-I164-source-only-integration.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(P)))
fresh=W/'scope-integration-package-fresh';assert not fresh.exists()
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(m)|{'MANIFEST.json'};entries=len(z.namelist());z.extractall(fresh)
assert {str(f.relative_to(fresh)) for f in fresh.rglob('*') if f.is_file()}==set(m)|{'MANIFEST.json'}
for n,v in m.items():assert ident(fresh/n)==v
result={**ident(dest),'entries':entries,'CRC_membership_manifests_fresh_extraction':'PASS'};(W/'scope-integration-package-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
