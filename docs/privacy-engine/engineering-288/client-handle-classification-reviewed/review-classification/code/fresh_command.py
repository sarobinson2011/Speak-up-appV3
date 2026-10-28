"""Actual current public CLI in a separate guarded interpreter."""
from pathlib import Path
import json,runpy,subprocess,sys,types
if len(sys.argv)>1 and sys.argv[1]=='--child':
 root=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]).resolve();C=runpy.run_path(str(Path(__file__).with_name('common.py')));C['guards'](root)
 def watch(code):
  if code.co_name in ('_basis','derive_client','validate','derive_handle'):sys.monitoring.set_local_events(4,code,sys.monitoring.events.PY_START)
  for x in code.co_consts:
   if isinstance(x,types.CodeType):watch(x)
 def audit(event,args):
  if event=='exec' and args[0].co_filename in (str(root/'code/correspondence.py'),str(root/'original/retained/handle/code/correspondence.py')):watch(args[0])
 sys.addaudithook(audit);sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/client-handle-correspondence.json')]
 try:runpy.run_path(sys.argv[0],run_name='__main__')
 finally:
  sys.monitoring.free_tool_id(4);(out/'calls.json').write_text(json.dumps(C['MONITOR_CALLS'],indent=2)+'\n')
else:
 root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
 p=subprocess.run([sys.executable,'-I','-B',str(Path(__file__).resolve()),'--child',str(root),str(out)],capture_output=True)
 (out/'stdout').write_bytes(p.stdout);(out/'stderr').write_bytes(p.stderr);r={'exit_code':p.returncode,'stderr_bytes':len(p.stderr),'stdout_bytes':len(p.stdout),'saved_inputs_only':True};(out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
 assert p.returncode==0 and p.stderr==b'';r['answer']=json.loads(p.stdout);assert r['answer']['result']=='PASS' and r['answer']['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and r['answer']['actual_admission'] is False and r['answer']['runtime_client_handle_chain']=='UNAVAILABLE'
 calls=json.loads((out/'calls.json').read_bytes());assert any(x['function']=='derive_handle' for x in calls);r['predecessor_derive_handle_observed']=True;(out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
