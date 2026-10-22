"""Focused filesystem tests. No application import, session or database creation."""
import argparse, hashlib, importlib.util, json, os, shutil, socket, stat, subprocess, sys
from pathlib import Path
from unittest.mock import patch
ap=argparse.ArgumentParser()
ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--draft',type=Path,required=True)
ap.add_argument('--old',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True)
a=ap.parse_args();a.evidence.mkdir(parents=True,exist_ok=False)
P=Path(__file__).resolve().parents[1];new=P/'implementation/code/lab_bootstrap.py'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=load(new,'corrected');old=load(a.old,'old')
rows=[];gaps=[]
def record(n,f):
 try:f();rows.append({'name':n,'status':'PASS'})
 except BaseException as e:
  rows.append({'name':n,'status':'FAIL','error':repr(e)})
  (a.evidence/'results.json').write_text(json.dumps({'checks':rows,'gaps':gaps},indent=2));raise
def rejects(f):
 try:f()
 except b.Blocked:return
 raise AssertionError('accepted')
def cli(script,draft,dest,accept):
 p=subprocess.run([sys.executable,'-B',str(script),'recover-runtime','--candidate',str(a.candidate),'--draft',str(draft),'--destination',str(dest)],capture_output=True,text=True,timeout=60)
 (a.evidence/(dest.name+'.log')).write_text(p.stdout+p.stderr)
 assert (p.returncode==0)==accept
 if not accept:assert not dest.exists()
def ident(p):return b.identity(p)
record('exact candidate666 and draft163',lambda:b.inputs(a.candidate,a.draft))
d=a.evidence/'draft';shutil.copytree(a.draft,d)
fifo=d/'unexpected.pipe';os.mkfifo(fifo)
record('old direct FIFO accepted witness',lambda:old.tree(d,old.read(old.P/'provenance/draft-members.json')))
record('old fresh full recovery accepts FIFO witness',lambda:cli(a.old,d,a.evidence/'old-runtime',True))
record('new fresh full recovery rejects FIFO before destination',lambda:cli(new,d,a.evidence/'rejected-runtime',False))

def rejects_no_read(root):
 with patch.object(b,'identity',side_effect=AssertionError('payload read before rejection')):
  rejects(lambda:b.tree(root,b.read(b.P/'provenance/draft-members.json')))
record('FIFO rejected before any payload read',lambda:rejects_no_read(d))
def session_gate():
 with patch.object(b,'load_runtime',side_effect=AssertionError('runtime imported')):
  with b._session(a.candidate,d,a.evidence/'old-runtime',a.evidence/'never-session',create=True):pass
record('session input gate rejects before runtime import or database',lambda:rejects(session_gate))
assert not (a.evidence/'never-session').exists()
fifo.unlink()
pins=b.read(b.P/'provenance/draft-members.json')
record('legitimate clean draft after witness removal',lambda:b.tree(d,pins))
for kind in ['regular','directory','symlink','fifo']:
 p=d/'extra'
 if kind=='regular':p.write_text('undeclared')
 elif kind=='directory':p.mkdir()
 elif kind=='symlink':p.symlink_to(d/'REPORT.md')
 else:os.mkfifo(p)
 record('undeclared '+kind,lambda:rejects(lambda:b.tree(d,pins)))
 if kind=='directory':p.rmdir()
 else:p.unlink()
# Replace a required member: must reject without blocking or opening it.
p=d/'REPORT.md';raw=p.read_bytes();p.unlink();os.mkfifo(p)
record('required-file FIFO substitution',lambda:rejects_no_read(d))
p.unlink();p.write_bytes(raw)
p=d/'REPORT.md';p.write_bytes(raw+b'altered')
record('altered required bytes',lambda:rejects(lambda:b.tree(d,pins)))
p.write_bytes(raw);p.unlink()
record('missing required member',lambda:rejects(lambda:b.tree(d,pins)))
p.write_bytes(raw)
# Actual socket where supported; preserve a precise environment gap otherwise.
s=None
try:
 s=socket.socket(socket.AF_UNIX);s.bind(str(d/'socket'))
except OSError as e:gaps.append({'control':'actual AF_UNIX socket','status':'UNAVAILABLE','error':repr(e)})
else:record('actual socket rejection',lambda:rejects_no_read(d))
finally:
 if s:s.close()
 if os.path.lexists(d/'socket'):(d/'socket').unlink()
# Stat-mode unit controls exercise device/socket branches without provisioning devices.
class Entry:
 path=str(d/'synthetic')
 def __init__(self,mode):self.mode=mode
 def stat(self,*,follow_symlinks):
  assert follow_symlinks is False
  return type('Status',(),{'st_mode':self.mode})()
class Scan:
 def __init__(self,mode):self.mode=mode
 def __enter__(self):return iter([Entry(self.mode)])
 def __exit__(self,*_):pass
for label,mode in [('FIFO',stat.S_IFIFO),('socket',stat.S_IFSOCK),('character-device',stat.S_IFCHR),('block-device',stat.S_IFBLK),('symlink',stat.S_IFLNK),('unknown-type',0)]:
 def f(mode=mode):
  with patch.object(b.os,'scandir',return_value=Scan(mode)),patch.object(b,'identity',side_effect=AssertionError('opened special file')):
   rejects(lambda:b.tree(d,pins))
 record('synthetic lstat mode '+label,f)
positive=a.evidence/'clean-draft';shutil.copytree(a.draft,positive)
record('fresh legitimate runtime recovery',lambda:cli(new,positive,a.evidence/'new-runtime',True))
record('recovered runtime93 exact bytes and helper mode',lambda:b.validate_runtime(a.evidence/'new-runtime'))
r=a.evidence/'new-runtime';os.mkfifo(r/'extra.pipe')
record('runtime FIFO rejected',lambda:rejects(lambda:b.validate_runtime(r)))
(r/'extra.pipe').unlink()
record('recovered runtime remains valid',lambda:b.validate_runtime(r))
record('repeated pristine input validation',lambda:[b.inputs(a.candidate,positive) for _ in range(3)])
record('candidate preservation666',lambda:b.tree(a.candidate,b.read(b.P/'provenance/candidate-members.json')))
assert len(b.runtime_pins())==93
record('runtime93 unchanged',lambda:[(lambda p,v: (_ for _ in ()).throw(AssertionError(p)) if ident(r/p)!=v else None)(p,v) for p,v in b.runtime_pins().items()])
out={'checks':rows,'gaps':gaps,'python':sys.version,'scope':'filesystem/recovery only; no application import, sessions, keys, DB connections or host probe','synthetic_device_controls':'mode classification only, not actual device creation','candidate_members':666,'runtime_members':93}
(a.evidence/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
