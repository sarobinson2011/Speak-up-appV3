from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
from integrity import verify_root,identity
ROOT=Path('/workspace/review-evidence/FL6-control-20261030');OUT=Path('/workspace/scratch/ace5c9b2f18b/cc-review/results')
result={n:verify_root(ROOT/n) for n in ('primary','recovered')}
p=ROOT/'primary';m=json.loads((p/'MANIFEST.json').read_bytes())
for plan in ('provenance/new-files.json','provenance/recovery-cut-manifest.json','provenance/final-added-files.json'):
 v=json.loads((p/plan).read_bytes());assert all(m[n]==pin for n,pin in v.items());result[plan]={'unchanged_members':len(v)}
(OUT/'final-verification.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
