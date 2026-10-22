"""Run only in disposable source copies: tests deliberately replace bound files."""
from pathlib import Path
import subprocess,sys,time,resource,json,hashlib,tempfile,shutil,os
R=Path(__file__).resolve().parents[1];start=time.monotonic()
with tempfile.TemporaryDirectory(prefix='i164-C2-') as d:
 kit=Path(d)/'kit';kit.mkdir()
 for n in ['code','retained']:shutil.copytree(R/n,kit/n)
 p=subprocess.run([sys.executable,'-B',str(kit/'code/test_identity.py')],capture_output=True,timeout=30)
(R/'results/C2.stdout').write_bytes(p.stdout);(R/'results/C2.stderr').write_bytes(p.stderr)
r={'tests':14,'exit_code':p.returncode,'seconds':time.monotonic()-start,'timeout_seconds':30,'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'bridge_sha256':hashlib.sha256((R/'code/bridge.py').read_bytes()).hexdigest(),'actual_admission':False}
(R/'results/C2.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));sys.exit(p.returncode)
