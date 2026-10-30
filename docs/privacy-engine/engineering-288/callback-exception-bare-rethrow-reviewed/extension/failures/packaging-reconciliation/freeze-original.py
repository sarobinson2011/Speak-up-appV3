from pathlib import Path
import json,types,shutil
r=Path('callback-bare');p=r/'tools/checkpoint.py';m=types.ModuleType('pack');exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
out=Path('callback-bare-runs/primary');v=json.loads((out/'RESULT.json').read_bytes());assert v['result']=='PASS' and v['error'] is None
rows=[json.loads(x) for x in (out/'progress.jsonl').read_text().splitlines()];assert rows==v['rows'] and len(rows)==v['checks']
manifest=json.loads((r/'MANIFEST.json').read_bytes());files=m.inventory(r);assert set(files)==set(manifest)|{'MANIFEST.json'}
for n,pin in manifest.items():assert m.identity(files[n])==pin,n
shutil.copyfile(r/'MANIFEST.json',r/'provenance/primary-input-manifest.json');(r/'MANIFEST.json').unlink();shutil.copytree(out,r/'results/primary');shutil.copyfile('callback-bare-tools/primary.log',r/'results/primary/stdout.log')
info=m.pack(m.inventory(r),Path('callback-bare-recovery-cut.zip'));m.verify(Path('callback-bare-recovery-cut.zip'),Path('callback-bare-recovered'));shutil.copyfile('callback-bare-recovered/MANIFEST.json',r/'MANIFEST.json');Path('callback-bare-tools/recovery-cut-identity.json').write_bytes(m.enc(info));print(json.dumps({'cut':info,'primary_controls':v['checks']},sort_keys=True))
