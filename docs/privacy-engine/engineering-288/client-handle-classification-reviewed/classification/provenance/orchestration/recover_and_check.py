"""One new recovered-root classification check; no old campaign is invoked."""
import json,os,runpy,stat,sys,time
from pathlib import Path
base=Path(__file__).resolve().parents[1]
root=base/'outside-catch-correction'
api=runpy.run_path(str(root/'tools/checkpoint.py'),run_name='_pack_api')
archive=base/'outside-catch-recovery-input.zip'
recovered=base/'outside-catch-recovered'
output=base/'outside-catch-tools/recovered-output'
gate=base/'outside-catch-tools/recovery-gate.json'
start=time.monotonic()
identity=api['verify'](archive,recovered)
manifest=json.loads((recovered/'MANIFEST.json').read_bytes())
expected=set(manifest)|{'MANIFEST.json'}
dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'}
files=set();seen_dirs=set()
for parent,ds,ns in os.walk(recovered,followlinks=False):
 for n in ds:
  p=Path(parent)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen_dirs.add(p.relative_to(recovered).as_posix())
 for n in ns:
  p=Path(parent)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(recovered).as_posix())
assert files==expected and seen_dirs==dirs
for n,pin in manifest.items():assert api['identity']((recovered/n).read_bytes())==pin,n
gate.write_text(json.dumps({'result':'PASS','identity':identity,'files':len(files),'directories':len(dirs),'exact_membership_before_candidate_loading':True},sort_keys=True,indent=2)+'\n')
sys.argv=[str(recovered/'tests/controls.py'),'--root',str(recovered),'--output',str(output),'--recovered']
runpy.run_path(str(recovered/'tests/controls.py'),run_name='__main__')
for n,pin in manifest.items():assert api['identity']((recovered/n).read_bytes())==pin,n
print(json.dumps({'root_bytes_unchanged_after_validation':True,'seconds_including_extraction':time.monotonic()-start}),flush=True)
