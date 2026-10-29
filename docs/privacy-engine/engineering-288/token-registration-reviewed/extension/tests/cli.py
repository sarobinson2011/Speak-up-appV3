"""Guarded independent-process invocation of current public CLI, not a session."""
from pathlib import Path
import sys,runpy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
try:
 rec.save('input-verification.json',verify_root(root));guard(root,rec.path)
 sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/token-registration-correspondence.json')]
 runpy.run_path(sys.argv[0],run_name='__main__');rec.row('recovered guarded public CLI PASS','PASS')
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering recovered CLI process; not host smoke or runtime execution')
