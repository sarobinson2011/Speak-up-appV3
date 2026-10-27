"""New outer predecessor-root gates; mutate only a disposable recovered root."""
import argparse,json,os,runpy
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 ns=runpy.run_path(str(a.root/'tests/controls.py'),run_name='_audit_only');m=ns['module'](a.root/'code/correspondence.py');base=a.root/'retained/references';rows=[]
 def forbidden(*args):raise AssertionError('PREDECESSOR-IMPORTED-BEFORE-GATE')
 m._module=forbidden
 def reject(label):
  try:m.recovery_inputs(a.root)
  except ValueError as e:rows.append({'check':label,'result':'PASS','rejection':str(e)})
  else:raise AssertionError('Unexpected acceptance')
 q=base/'undeclared-empty';q.mkdir()
 try:reject('undeclared empty directory before import')
 finally:q.rmdir()
 q=base/'undeclared-fifo';os.mkfifo(q)
 try:reject('undeclared FIFO before import')
 finally:q.unlink()
 q=base/'undeclared-link';q.symlink_to('MANIFEST.json')
 try:reject('symlink before import')
 finally:q.unlink()
 q=base/'results/reference-correspondence.json';raw=q.read_bytes()
 try:q.write_bytes(raw+b' ');reject('stale receipt before import')
 finally:q.write_bytes(raw)
 try:q.unlink();reject('missing receipt before import')
 finally:q.write_bytes(raw)
 # Verify exact restoration without invoking the imported validators a second
 # time here; the separate recovered controls and fresh process do that.
 manifest=json.loads((base/'MANIFEST.json').read_bytes())
 assert all(ns['identity']((base/n).read_bytes())==pin for n,pin in manifest.items())
 a.output.write_text(json.dumps({'result':'PASS','checks':rows,'passed':len(rows),'root':str(a.root),'restored_exact_manifest':True,'unix_socket_and_device_entries':'UNTESTED; preexisting limitation preserved','no_runtime':True},indent=2)+'\n')
 print('PASS',len(rows),'new input gates')
if __name__=='__main__':main()
