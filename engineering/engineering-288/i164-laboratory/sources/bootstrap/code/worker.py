import sys,os,json
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'implementation/code'));import lab_bootstrap as b
case=sys.argv[1];c,d,r,dest=map(Path,sys.argv[2:6])
if case=='copy-interrupt':
 original=Path.write_bytes
 def fault(p,data):
  ret=original(p,data)
  if p.is_relative_to(dest):os._exit(77)
  return ret
 Path.write_bytes=fault
 b.recover_runtime(c,d,dest);raise AssertionError('NO-INJECTION')
if case=='recover':print(b.recover_runtime(c,d,dest));sys.exit()
if case=='inputs':b.inputs(c,d);print('PASS inputs');sys.exit()
# Local mechanics only: same explicit mismatch boundary as previous author/reviewer.
with b._session(c,d,r,dest,create=case in ['create','exit']) as g:
 assert g.status()['actual_admission'] is False
 if case=='exit':os._exit(78)
 print(json.dumps({'state':g.state(),'status':g.status()}))
print('PASS managed close')
