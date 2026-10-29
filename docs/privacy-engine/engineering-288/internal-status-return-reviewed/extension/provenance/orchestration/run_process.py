import json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'status-forwarding';T=B/'status-forward-tools';mode=sys.argv[1];assert mode in ('fresh','recovered');prefix=T/mode
for ext in ('.stdout','.stderr','.process.json'):assert not prefix.with_suffix(ext).exists()
cmd=[sys.executable,'-I','-B']+([str(R/'tests/fresh_check.py'),str(R)] if mode=='fresh' else [str(T/'recover_and_check.py')]);start=time.monotonic()
with prefix.with_suffix('.stdout').open('xb') as out,prefix.with_suffix('.stderr').open('xb') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
result={'mode':mode,'command':cmd,'exit':p.returncode,'seconds':time.monotonic()-start,'automatic_retry':False,'new_extension_checks_only':True};prefix.with_suffix('.process.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);raise SystemExit(p.returncode)
