from pathlib import Path
import sys,runpy,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integrity import verify_archive
from common import guard
archive=Path(sys.argv[1]);root=Path(sys.argv[2]);record=Path(sys.argv[3]);info=verify_archive(archive,root);record.write_text(json.dumps(info,indent=2)+'\n');guard(root.resolve());sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/token-registration-correspondence.json')];runpy.run_path(sys.argv[0],run_name='__main__')
