import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'PACKAGE-MANIFEST.json').read_text());actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=R/'PACKAGE-MANIFEST.json'}
assert actual=={x['path'] for x in m['files']} and len(m['files'])==len(actual),'package membership'
for x in m['files']:
 p=R/x['path'];assert not p.is_symlink() and p.stat().st_size==x['bytes']
 with p.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==x['sha256'],x['path']
old=json.loads((R/'evidence/4V-PACKAGE-MANIFEST.json').read_text());by={x['path']:x for x in old['files']};retained=json.loads((R/'evidence/RUNTIME-REUSE.json').read_text())
for x in retained:
 assert by[x['4V_path']]['sha256']==x['sha256'] and by[x['4V_path']]['bytes']==x['bytes']
 with (R/x['path']).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==x['sha256']
measured=json.loads((R/'results/MEASURED-IMPLEMENTATION.json').read_text())
for name,h in measured['code'].items():
 p=R/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=h:p=R/'results/measured-wrapper-sources'/name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==h,'measurement source unavailable '+name
print(json.dumps({'result':'PASS-4W-PACKAGE','files':len(m['files']),'runtime_files_exactly_reused_from_4V':len(retained),'measured_source_identities_verified':True,'actual_admission':False}))
