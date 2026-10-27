"""Guarded fresh-process exercise of the new offline check command only."""
from pathlib import Path
import os,runpy,sys
root=Path(sys.argv[1]).resolve()
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)):
  name=os.fsdecode(args[0])
  if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
  if name.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
sys.addaudithook(audit)
def profile(f,event,arg):
 n=f.f_code.co_filename.rsplit('/',1)[-1]
 if event=='call' and (n in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or n=='prospective_entry.py' and f.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
p=root/'code/correspondence.py';sys.argv=[str(p),'check',str(root/'results/status-field-correspondence.json')]
runpy.run_path(str(p),run_name='__main__')
