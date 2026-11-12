"""Record systemd's service outcome separately; never infer a child/public result."""
from pathlib import Path
import sys,os,json,datetime
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
v={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'SERVICE_RESULT':os.environ.get('SERVICE_RESULT'),'EXIT_CODE':os.environ.get('EXIT_CODE'),'EXIT_STATUS':os.environ.get('EXIT_STATUS'),'meaning':'Service-manager observation only; distinct from supervisor child exit and public result'}
with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
