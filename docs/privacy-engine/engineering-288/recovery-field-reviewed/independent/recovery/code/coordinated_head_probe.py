"""Saved-input-only probe of coordinated head substitution, no DB operations."""
from pathlib import Path
import copy,hashlib,json,os,sys,types
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
sys.addaudithook(audit)
def profile(frame,event,arg):
 if event=='call' and frame.f_code.co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
p=root/'code/correspondence.py';m=types.ModuleType('probe');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
d=m.recovery_inputs(root);cat=m.recovery_catalogue(d);original=d['ctx']['e'];e=dict(original)
x=json.loads(e['evidence/recovery-export-0.json']);h=json.loads(bytes.fromhex(x['head']));before=h['head'];after=('1' if before[0]!='1' else '2')+before[1:];assert before!=after
h['head']=after;x['head']=m.enc(h).hex();x['expected_head']=after;e['evidence/recovery-export-0.json']=m.enc(x)
t=json.loads(e['evidence/execution-trace.json']);r=next(v for v in t['events'] if v['event']=='return' and v['function']=='ManagedAuthority.recover');r['value']['head']=after;e['evidence/execution-trace.json']=m.enc(t)
hand=json.loads(e['evidence/client-handoff.json']);hand[0]['state']['head']=after;e['evidence/client-handoff.json']=m.enc(hand)
complete=json.loads(e['evidence/session-records/BOOTSTRAP-COMPLETE.json']);complete['state']['head']=after
for n in ['evidence/session-records/BOOTSTRAP-COMPLETE.json','new-session-records/BOOTSTRAP-COMPLETE.json']:e[n]=m.enc(complete)
result=json.loads(e['evidence/smoke-result.json']);result['state']['head']=after;result['head']=x['head'];e['evidence/smoke-result.json']=m.enc(result)
close=json.loads(e['evidence/confirmed-close.json'])
for k in ['before','after']:close[k]['BOOTSTRAP-COMPLETE.json']=m.identity(e['evidence/session-records/BOOTSTRAP-COMPLETE.json'])
e['evidence/confirmed-close.json']=m.enc(close)
changed={k:{'before':m.identity(original[k]),'after':m.identity(v)} for k,v in e.items() if v!=original[k]}
assert len(changed)==7
answers={}
for name,fn in [('semantic',lambda:m.connected_recovery(d,cat,e)),('derivation',lambda:m.derive_recovery(d,cat,e))]:
 try:
  value=fn();answers[name]={'result':'ACCEPTED'}
  if name=='derivation':(out/'altered-derived-receipt.json').write_bytes(m.enc(value))
 except (ValueError,TypeError,KeyError) as ex:answers[name]={'result':'REJECTED','type':type(ex).__name__,'message':str(ex)}
for name in changed:
 p=out/'mutated'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(e[name])
(out/'RESULT.json').write_text(json.dumps({'substitution':{'old':before,'new':after},'changed':changed,'checks':answers,'retained_database_payloads_unchanged':all(v==original[k] for k,v in e.items() if k.endswith('.sqlite')),'not_admitted_as_public_input':True,'no_runtime_database_or_session_operations':True},indent=2)+'\n')
print(json.dumps(answers))
