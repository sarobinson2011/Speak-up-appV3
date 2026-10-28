"""Bounded offline child-process recorder; no application/session execution."""
from pathlib import Path
import json,subprocess,sys,time
root=Path(sys.argv[1]).resolve();mode=sys.argv[2];case=sys.argv[3];base=Path(__file__).resolve().parents[1]
assert mode in ('primary','recovered')
out=base/('independent-'+mode)/case;record=base/'processes'/(mode+'-'+case);record.mkdir(parents=True,exist_ok=False)
command=[sys.executable,'-I','-B',str(Path(__file__).with_name('entry_controls.py')),str(root),str(out),'--case',case]
if mode=='recovered':command.append('--recovered')
start=time.monotonic()
with (record/'stdout').open('xb') as stdout,(record/'stderr').open('xb') as stderr:
 p=subprocess.run(command,stdout=stdout,stderr=stderr)
r={'exit_code':p.returncode,'seconds':time.monotonic()-start,'case':case,'mode':mode,'command':command,'result':'PASS' if p.returncode==0 else 'FAIL'}
(record/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));assert p.returncode==0
