"""Release utility: creates an exact inventory. Never updates historical artifacts."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or '__pycache__' in p.parts or p==ROOT/'PACKAGE-MANIFEST.json':continue
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':h})
(ROOT/'PACKAGE-MANIFEST.json').write_text(json.dumps({'format':'ENGINEERING-288-4V-PACKAGE-MANIFEST-1','files':files,'member_bytes':sum(x['bytes'] for x in files),'actual_admission':False},indent=2)+'\n')
