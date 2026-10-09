import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((R/'PACKAGE-MANIFEST.json').read_bytes())
actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE-MANIFEST.json'}
# The only top-level excluded manifest is this package's own.
actual={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=R/'PACKAGE-MANIFEST.json'}
assert actual=={x['path'] for x in m['files']}
for x in m['files']:
 p=R/x['path'];assert not p.is_symlink() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],x['path']
old=json.loads((R/'ORIGINAL-PACKAGE-MANIFEST.json').read_bytes());runtime=[x for x in old['files'] if x['path'].startswith('runtime/')]
for x in runtime:assert sha(R/x['path'])==x['sha256'],x['path']
print(json.dumps({'result':'PASS-DIAGNOSTIC-PACKAGE','members':len(m['files']),'unchanged_runtime_files':len(runtime),'full_stream_processed':False,'actual_admission':False}))
