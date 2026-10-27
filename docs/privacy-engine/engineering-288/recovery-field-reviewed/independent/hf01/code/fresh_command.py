"""Fresh process for the actual new offline CLI, saved evidence only."""
from pathlib import Path
import json,os,runpy,subprocess,sys
if len(sys.argv)>1 and sys.argv[1]=='--child':
 root=Path(sys.argv[2]).resolve()
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
  if event=='open' and isinstance(args[0],(str,bytes)):
   name=os.fsdecode(args[0])
   if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if name.startswith(str(root)+'/') and len(args)>2 and type(args[2]) is int and args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def profile(frame,event,arg):
  name=frame.f_code.co_filename.rsplit('/',1)[-1]
  if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
 sys.setprofile(profile)
 sys.argv=[str(root/'code/correspondence.py'),'check',str(root/'results/hf01-correspondence.json')]
 runpy.run_path(sys.argv[0],run_name='__main__')
else:
 root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
 p=subprocess.run([sys.executable,'-I','-B',str(Path(__file__).resolve()),'--child',str(root)],capture_output=True)
 (out/'stdout').write_bytes(p.stdout);(out/'stderr').write_bytes(p.stderr)
 result={'returncode':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'new_offline_CLI_only':True}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 assert p.returncode==0 and p.stderr==b'',result
 result['answer']=json.loads(p.stdout)
 assert result['answer']['result']=='PASS' and result['answer']['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
 assert result['answer']['actual_admission'] is False and result['answer']['complete_repetition_coverage'] is False
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
