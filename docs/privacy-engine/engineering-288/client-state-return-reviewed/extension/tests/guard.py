"""Offline source/evidence checks only; forbid application operations and input writes."""
import os,sys
from pathlib import Path
def install(root):
 root=Path(root).resolve();protected=[str(root/n)+'/' for n in ('retained','code','tests')]
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   p=os.fsdecode(args[0]);flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
   if p.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if any(str(Path(p).absolute()).startswith(n) for n in protected) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  if event!='call':return
  name=frame.f_code.co_filename.rsplit('/',1)[-1]
  if name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
  if name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','_data','_fail','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile)
