"""Exact delivered file identities; no expansion, benchmarks or full streams."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE-MANIFEST.json').read_bytes())
for e in manifest['files']:
 p=(root/e['path']).resolve()
 assert p.is_relative_to(root) and p.is_file(),e['path']
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1024*1024):h.update(b)
 assert p.stat().st_size==e['bytes'] and h.hexdigest()==e['sha256'],e['path']
print(json.dumps({'result':'PASS-DELIVERED-FILE-HASHES','files':len(manifest['files']),'full_stream_computed':False,'profile_admitted':False}))
