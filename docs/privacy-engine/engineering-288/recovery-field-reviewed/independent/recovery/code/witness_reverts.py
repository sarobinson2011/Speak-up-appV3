"""Check each member's necessity for the saved coordinated witness."""
from pathlib import Path
import json,os,sys,types
root=Path(sys.argv[1]).resolve();witness=Path(sys.argv[2]).resolve();out=Path(sys.argv[3]).resolve()
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
p=root/'code/correspondence.py';m=types.ModuleType('reverts');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);d=m.recovery_inputs(root);cat=m.recovery_catalogue(d);original=d['ctx']['e'];changed=json.loads((witness/'RESULT.json').read_bytes())['changed_members'];all_changed=dict(original)
for name in changed:all_changed[name]=(witness/'mutated'/name).read_bytes()
rows=[]
for name in changed:
 e=dict(all_changed);e[name]=original[name]
 try:m.connected_recovery(d,cat,e)
 except (ValueError,TypeError,KeyError) as ex:rows.append({'restored_member':name,'result':'REJECTED','reason':str(ex)});continue
 raise AssertionError('One-member restoration unexpectedly still accepted: '+name)
result={'result':'PASS','assertions':len(rows),'checks':rows,'scope':'Member-removal minimality for this fixed substitution; not a proof of global byte-minimality','no_database_or_runtime_operations':True}
out.write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(rows),'one-member restoration controls')
