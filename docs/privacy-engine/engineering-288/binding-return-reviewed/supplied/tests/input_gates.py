"""New binding input-loader gates on a separate disposable copy only."""
import json,runpy,sys,shutil
from pathlib import Path
source=Path(sys.argv[1]).resolve();target=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=False)
assert not target.exists();shutil.copytree(source,target)
ns=runpy.run_path(str(source/'tests/controls.py'),run_name='_audit_only');m=ns['module'](source/'code/correspondence.py');rows=[];error=None
def reject(label,reason):
 try:m.inputs(target)
 except ValueError as e:assert str(e)==reason,(label,str(e));rows.append({'check':label,'result':'PASS','reason':str(e)});return
 raise AssertionError('Unexpected input acceptance: '+label)
try:
 d=target/'retained/hf01/undeclared-empty';d.mkdir();reject('new predecessor loader rejects undeclared directory','BINDING-UNDECLARED-DIRECTORY');d.rmdir()
 p=target/'retained/hf01/undeclared.txt';p.write_bytes(b'not declared');reject('new predecessor loader rejects undeclared regular entry','BINDING-UNDECLARED-OR-NONREGULAR');p.unlink()
 p=target/'code/managed_coverage.py';raw=p.read_bytes();p.write_bytes(raw+b'\n# stale source\n');reject('new loader rejects stale producer before import','BINDING-PRODUCER-SOURCE');p.write_bytes(raw)
 p=target/'retained/hf01/code/managed_coverage.py';raw=p.read_bytes();p.write_bytes(raw+b'\n');reject('new loader rejects changed predecessor source before import','BINDING-PREDECESSOR-BYTES:code/managed_coverage.py');p.write_bytes(raw)
except BaseException as e:error=repr(e);raise
finally:
 r={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'positive_validation_on_gate_root':False,'unix_socket_and_device_cases':'NOT TESTED','database_connections':0,'session_operations':0}
 (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
