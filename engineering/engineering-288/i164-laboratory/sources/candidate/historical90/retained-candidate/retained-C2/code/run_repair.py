import subprocess,sys,time,json,resource,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];start=time.monotonic()
p=subprocess.run([sys.executable,'-B',str(R/'code/test_retirement.py')],capture_output=True,timeout=30)
(R/'results/repair.stdout').write_bytes(p.stdout);(R/'results/repair.stderr').write_bytes(p.stderr)
r={'tests':16,'exit_code':p.returncode,'seconds':time.monotonic()-start,'timeout_seconds':30,'parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'python':sys.version,'bridge_sha256':hashlib.sha256((R/'code/bridge.py').read_bytes()).hexdigest(),'actual_admission':False}
(R/'results/repair.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));sys.exit(p.returncode)
