"""One fresh-process public validation, with no application/session execution."""
import json,os,sys,types
from pathlib import Path
def audit(event,args):
 if event in ('sqlite3.connect','socket.connect','socket.bind'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
root=Path(sys.argv[1]);p=root/'code/correspondence.py'
m=types.ModuleType('_fresh_reference');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
print(json.dumps(m.validate(root,(root/'results/reference-correspondence.json').read_bytes()),sort_keys=True))
