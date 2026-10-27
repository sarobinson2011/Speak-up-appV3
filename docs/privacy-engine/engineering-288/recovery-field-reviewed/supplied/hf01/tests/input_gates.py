"""New HF-01 recovered input-root controls, disposable extraction only."""
import json,os,runpy,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);ns=runpy.run_path(str(root/'tests/controls.py'),run_name='_audit_only');m=ns['module'](root/'code/correspondence.py');base=root/'original';rows=[]
def forbidden(*args):raise AssertionError('IMPORTED-BEFORE-INPUT-GATE')
m._module=forbidden
def reject(label):
 try:m.recovery_inputs(root)
 except ValueError as ex:rows.append({'check':label,'result':'PASS','reason':str(ex)})
 else:raise AssertionError('Unexpected acceptance')
q=base/'undeclared-empty';q.mkdir()
try:reject('undeclared empty directory')
finally:q.rmdir()
q=base/'undeclared-fifo';os.mkfifo(q)
try:reject('undeclared FIFO')
finally:q.unlink()
q=base/'undeclared-symlink';q.symlink_to('MANIFEST.json')
try:reject('undeclared symlink')
finally:q.unlink()
q=base/'results/recovery-field-correspondence.json';raw=q.read_bytes()
try:q.write_bytes(raw+b' ');reject('stale original receipt')
finally:q.write_bytes(raw)
try:q.unlink();reject('missing original receipt')
finally:q.write_bytes(raw)
manifest=json.loads((base/'MANIFEST.json').read_bytes());assert all(ns['identity']((base/n).read_bytes())==pin for n,pin in manifest.items())
out.write_text(json.dumps({'result':'PASS','passed':len(rows),'checks':rows,'all_rejected_before_predecessor_import':True,'restored_original_bytes':True,'unix_sockets_devices':'UNTESTED; prior limitation preserved','no_runtime':True},indent=2)+'\n')
print('PASS',len(rows),'HF-01 input gates')
