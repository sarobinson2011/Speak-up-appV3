import json,os,runpy,stat,sys,time
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'client-state-return';T=B/'client-state-tools';api=runpy.run_path(str(R/'tools/checkpoint.py'),run_name='_archive')
start=time.monotonic();root=B/'client-state-recovered';identity=api['verify'](B/'client-state-recovery-input.zip',root)
m=json.loads((root/'MANIFEST.json').read_bytes());expected=set(m)|{'MANIFEST.json'};expected_dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();dirs=set()
for parent,ds,ns in os.walk(root,followlinks=False):
 for n in ds:
  p=Path(parent)/n;assert stat.S_ISDIR(p.lstat().st_mode);dirs.add(p.relative_to(root).as_posix())
 for n in ns:
  p=Path(parent)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
assert files==expected and dirs==expected_dirs
for n,pin in m.items():assert api['identity']((root/n).read_bytes())==pin,n
(T/'recovery-gate.json').write_text(json.dumps({'result':'PASS','archive':identity,'files':len(files),'directories':len(dirs),'exact_membership_before_loading':True},indent=2)+'\n')
sys.argv=[str(root/'tests/controls.py'),'--root',str(root),'--output',str(T/'recovered-output'),'--recovered'];runpy.run_path(str(root/'tests/controls.py'),run_name='__main__')
for n,pin in m.items():assert api['identity']((root/n).read_bytes())==pin,n
print(json.dumps({'all_recovered_input_bytes_unchanged':True,'seconds_with_extraction':time.monotonic()-start}),flush=True)
