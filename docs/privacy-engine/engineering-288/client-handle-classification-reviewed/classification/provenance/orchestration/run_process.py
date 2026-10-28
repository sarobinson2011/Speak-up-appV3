"""Record one isolated saved-input validator invocation, without automatic retry."""
import json,subprocess,sys,time
from pathlib import Path
base=Path(__file__).resolve().parents[1];root=base/'outside-catch-correction'
mode=sys.argv[1];assert mode in ('fresh','recovered')
prefix=base/'outside-catch-tools'/mode
for suffix in ('.stdout','.stderr','.process.json'):assert not prefix.with_suffix(suffix).exists()
command=[sys.executable,'-I','-B']+([str(root/'tests/fresh_check.py'),str(root)] if mode=='fresh' else [str(base/'outside-catch-tools/recover_and_check.py')])
start=time.monotonic()
with prefix.with_suffix('.stdout').open('xb') as out,prefix.with_suffix('.stderr').open('xb') as err:
 p=subprocess.run(command,stdout=out,stderr=err,check=False)
report={'mode':mode,'command':command,'exit':p.returncode,'seconds':time.monotonic()-start,'retry':False,'new_focused_validation_only':True}
prefix.with_suffix('.process.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
raise SystemExit(p.returncode)
