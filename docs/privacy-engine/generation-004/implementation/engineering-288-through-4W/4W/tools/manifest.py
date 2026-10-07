import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
files=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p!=R/'PACKAGE-MANIFEST.json':
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  files.append({'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':h})
(R/'PACKAGE-MANIFEST.json').write_text(json.dumps({'format':'ENGINEERING-288-4W-PACKAGE-MANIFEST-1','files':files,'member_bytes':sum(x['bytes'] for x in files),'actual_admission':False},indent=2)+'\n')
