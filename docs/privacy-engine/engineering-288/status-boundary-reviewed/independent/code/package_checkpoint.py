"""Package independent review evidence; exclude only reproducible mutation tree."""
import hashlib, json, stat, sys, zipfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
output=Path(sys.argv[1]).resolve()
excluded=root/'independent-process-controls/mutated-source-copy'
files=[]
for p in sorted(root.rglob('*')):
    if p==excluded or excluded in p.parents:continue
    if p.is_dir():continue
    assert stat.S_ISREG(p.lstat().st_mode),p
    if p==root/'MANIFEST.json':continue
    files.append(p)
members={str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(root/'MANIFEST.json').write_text(json.dumps({'format':'Formal-Lab6-independent-review-manifest-1','members':members},indent=2)+'\n')
with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files+[root/'MANIFEST.json']):
        i=zipfile.ZipInfo(str(p.relative_to(root)),date_time=(2026,10,26,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(i,p.read_bytes())
print(json.dumps({'bytes':output.stat().st_size,'entries':len(files)+1,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
