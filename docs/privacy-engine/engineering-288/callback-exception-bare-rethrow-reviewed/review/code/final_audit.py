from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
from integrity import verify_root,identity
ROOT=Path('/workspace/review-evidence/FL6-bare-20261030');OUT=Path('/workspace/scratch/ace5c9b2f18b/br-review/results')
r={}
for name in ('primary','recovered'):r[name]=verify_root(ROOT/name)
p=ROOT/'primary';manifest=json.loads((p/'MANIFEST.json').read_bytes());plan=json.loads((p/'provenance/primary-input-manifest.json').read_bytes())
assert all(manifest[n]==v for n,v in plan.items())
changes=json.loads((p/'provenance/changed-files.json').read_bytes())
for n,pin in changes['tests'].items():assert identity((p/n).read_bytes())==pin
r['primary_input_plan_members_unchanged']=len(plan);r['declared_test_identities']='All four exact'
(OUT/'final-verification.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
