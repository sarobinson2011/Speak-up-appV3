from pathlib import Path
import sys,runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import guard
root=Path(sys.argv[1]).resolve();guard(root)
sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/client-state-correspondence.json')]
runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
