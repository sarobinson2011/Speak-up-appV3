from pathlib import Path
import sys,runpy,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integrity import verify_archive
archive,root,out,script,*args=sys.argv[1:];r=verify_archive(Path(archive),Path(root));Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out+'-recovery.json').write_text(json.dumps(r,indent=2)+'\n')
sys.argv=[str(Path(__file__).with_name(script)),root,out,*args];runpy.run_path(sys.argv[0],run_name='__main__')
