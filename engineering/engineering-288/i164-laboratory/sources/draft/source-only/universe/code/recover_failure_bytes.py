"""Reconstruct exact saved workspace-partial failure bytes; never writes candidate."""
import json,sys,hashlib
from pathlib import Path
import cardinality
P=Path(__file__).resolve().parents[1];root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();cardinality.verify_root(root);assert not out.exists() and not out.is_relative_to(root)
for r in json.loads((P/'provenance/failure-prefixes.json').read_bytes()):
 b=(root/r['source_member']).read_bytes();assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==r['source_identity'];b=b[:r['prefix_bytes']];assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==r['identity'];p=out/r['reconstructed_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('PASS exact failure bytes reconstructed outside candidate')
