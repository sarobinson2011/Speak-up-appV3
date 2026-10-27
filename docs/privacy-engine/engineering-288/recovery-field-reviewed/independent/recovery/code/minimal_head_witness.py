"""Coordinated one-digit head witness. No implementation or DB changes."""
from pathlib import Path
import hashlib,json,os,re,sys,types
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=False)
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo'):raise AssertionError('PROHIBITED:'+event)
sys.addaudithook(audit)
def profile(frame,event,arg):
 name=frame.f_code.co_filename.rsplit('/',1)[-1]
 if event=='call' and (name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') or name=='prospective_entry.py' and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status')):raise AssertionError('APPLICATION-EXECUTION')
sys.setprofile(profile)
p=root/'code/correspondence.py';m=types.ModuleType('minimal_probe');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
d=m.recovery_inputs(root);cat=m.recovery_catalogue(d);original=d['ctx']['e'];e=dict(original)
x=json.loads(e['evidence/recovery-export-0.json']);oldraw=bytes.fromhex(x['head']);head=json.loads(oldraw);before=head['head'];after='1'+before[1:];assert before=='0'*64
def change_named(raw,name):
 pattern=rb'("'+name.encode()+rb'"\s*:\s*")'+before.encode()+rb'(")'
 changed,n=re.subn(pattern,lambda match:match[1]+after.encode()+match[2],raw);assert n==1,(name,n);assert len(changed)==len(raw);return changed
newraw=change_named(oldraw,'head')
for name in ['evidence/execution-trace.json','evidence/client-handoff.json','evidence/session-records/BOOTSTRAP-COMPLETE.json','new-session-records/BOOTSTRAP-COMPLETE.json']:
 e[name]=change_named(e[name],'head')
e['evidence/recovery-export-0.json']=change_named(e['evidence/recovery-export-0.json'],'expected_head').replace(oldraw.hex().encode(),newraw.hex().encode())
e['evidence/smoke-result.json']=change_named(e['evidence/smoke-result.json'],'head').replace(oldraw.hex().encode(),newraw.hex().encode())
# Preserve lengths and formatting. Only the two already retained byte digests
# of the one changed bootstrap record must follow that byte change.
oldpin=m.identity(original['evidence/session-records/BOOTSTRAP-COMPLETE.json']);newpin=m.identity(e['evidence/session-records/BOOTSTRAP-COMPLETE.json']);assert oldpin['bytes']==newpin['bytes']
name='evidence/confirmed-close.json';assert e[name].count(oldpin['sha256'].encode())==2;e[name]=e[name].replace(oldpin['sha256'].encode(),newpin['sha256'].encode())
changes={k:{'before':m.identity(original[k]),'after':m.identity(v),'different_byte_offsets':[i for i,(a,b) in enumerate(zip(original[k],v)) if a!=b]} for k,v in e.items() if v!=original[k]}
assert len(changes)==7 and all(v['before']['bytes']==v['after']['bytes'] for v in changes.values())
answers={}
derived=None
for name,fn in [('semantic',lambda:m.connected_recovery(d,cat,e)),('derivation',lambda:m.derive_recovery(d,cat,e))]:
 try:
  v=fn();answers[name]={'result':'ACCEPTED'}
  if name=='derivation':derived=m.enc(v);(out/'altered-derived-receipt.json').write_bytes(derived)
 except (ValueError,TypeError,KeyError) as ex:answers[name]={'result':'REJECTED','type':type(ex).__name__,'message':str(ex)}
if derived is not None:
 try:m.validate(root,derived);answers['public_receipt']={'result':'ACCEPTED'}
 except (ValueError,TypeError,KeyError) as ex:answers['public_receipt']={'result':'REJECTED','type':type(ex).__name__,'message':str(ex)}
answers['pristine_public']=m.validate(root,(root/'results/recovery-field-correspondence.json').read_bytes())
dbfacts={}
for k,b in original.items():
 if k.endswith('.sqlite'):
  assert e[k]==b
  dbfacts[k]={'identity':m.identity(b),'original_export_head_raw_occurrences':b.count(oldraw),'substituted_head_raw_occurrences':b.count(newraw),'first_original_raw_offset':b.find(oldraw),'no_SQLite_connection_used':True}
for name in changes:
 p=out/'mutated'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(e[name])
result={'finding':'HF-01 candidate witness, subject to scoped review','substitution':{'old':before,'new':after},'changed_members':changes,'checks':answers,'retained_database_byte_facts':dbfacts,'source_and_all_unlisted_evidence_members_unchanged':True,'public_root_evidence_not_modified':True,'no_runtime_database_or_session_operations':True}
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':answers,'changed_members':len(changes),'changed_bytes':sum(len(c['different_byte_offsets']) for c in changes.values())}))
