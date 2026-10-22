"""Read-only directory manifest verification; no experiments."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];m=json.loads((root/'MANIFEST.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
assert actual==set(m),(actual-set(m),set(m)-actual)
for n,v in m.items():
 b=(root/n).read_bytes();assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
print('Exact membership and all manifest hashes PASS:',len(m),'files plus manifest')
