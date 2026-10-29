"""Exact new-root recovery followed only by this extension's focused checks."""
import hashlib,json,os,runpy,stat,sys,zipfile
from pathlib import Path,PurePosixPath
B=Path(__file__).resolve().parents[1];R=B/'status-forward-recovered';T=B/'status-forward-tools';archive=B/'status-forward-recovery-input.zip';expected=json.loads((B/'status-forwarding/results/recovery-input.json').read_bytes())
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert ident(archive.read_bytes())=={k:expected[k] for k in ('bytes','sha256')}
with zipfile.ZipFile(archive) as z:
 names=z.namelist();assert len(names)==len(set(names))==expected['entries'] and z.testzip() is None
 manifest=json.loads(z.read('MANIFEST.json'));assert set(names)==set(manifest)|{'MANIFEST.json'}
 for i in z.infolist():
  p=PurePosixPath(i.filename);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==i.filename and not i.is_dir() and stat.S_ISREG(i.external_attr>>16)
 for n,p in manifest.items():assert ident(z.read(n))==p
 R.mkdir()
 for n in names:p=R/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
expected_dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'};actual_files=set();actual_dirs=set()
for base,dirs,files in os.walk(R,followlinks=False):
 for n in dirs:p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);actual_dirs.add(p.relative_to(R).as_posix())
 for n in files:p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);actual_files.add(p.relative_to(R).as_posix())
assert actual_files==set(names) and actual_dirs==expected_dirs
before={n:ident((R/n).read_bytes()) for n in names};report={'archive':expected,'files':len(names),'directories':len(expected_dirs),'preconsume_exact_membership_types_hashes':'PASS'}
(T/'recovery-gate.json').write_text(json.dumps(report,indent=2)+'\n')
sys.argv=['controls.py','--root',str(R),'--output',str(T/'recovered-output'),'--recovered'];runpy.run_path(str(R/'tests/controls.py'),run_name='__main__')
sys.argv=['type_controls.py','--root',str(R),'--output',str(T/'recovered-types')];runpy.run_path(str(R/'tests/type_controls.py'),run_name='__main__')
assert all(ident((R/n).read_bytes())==pin for n,pin in before.items());report['all_recovered_bytes_unchanged']='PASS';(T/'recovery-gate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
