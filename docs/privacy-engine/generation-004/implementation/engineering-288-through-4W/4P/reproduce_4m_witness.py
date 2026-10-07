"""Run original failure witness from exact retained parent; never imports 4N store."""
import tempfile,zipfile,subprocess,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'retained/Engineering-288-checkpoint-4M.zip'
with p.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()=='119413ad8fe330afa823576f3c46efb528b90729162ae46d6f3a7a8a5612cecf'
with tempfile.TemporaryDirectory(prefix='4n-witness-') as td:
 with zipfile.ZipFile(p) as z:z.extractall(td)
 root=Path(td)/'Engineering-288-checkpoint-4M'
 r=subprocess.run([sys.executable,'run_4m_capability.py'],cwd=root,capture_output=True,text=True,timeout=30)
 assert r.returncode==0,r.stderr
 result=json.loads(r.stdout);print(json.dumps(result,indent=2))
 assert result['completed_small_documents']<result['attempted_documents'] and 'Too many open files' in result['failure']['detail']
