from pathlib import Path
import json,sys,collections,hashlib,stat,zipfile
sys.path.insert(0,str(Path(__file__).parent))
from integrity import root,ident
W=Path(__file__).resolve().parents[2];R=W/'sr-review';result={}
roots=[Path('/workspace/review-evidence/FL6-stored-20261030')/s for s in ('primary','recovered')]
for p in roots:result[str(p)]=root(p)
with zipfile.ZipFile(W/'upload/I164-stored-failure-revocation-correspondence-1(1).zip') as z:
 for p in roots:
  for n in ('code/correspondence.py','code/managed_coverage.py','source-evidence/prospective_entry.py','source-evidence/lab_bootstrap.py','source-evidence/live_connection.py'):
   assert (p/n).read_bytes()==z.read(n)
counts={}
for name in ('primary-complete','recovered-controls','source-controls','fresh-public','fresh-semantic'):
 calls=json.loads((R/'results'/name/'calls.json').read_bytes());counts[name]=dict(collections.Counter(v['function'] for v in calls))
 ops=[v for v in calls if Path(v['file']).name=='prospective_entry.py' and v['function'] not in ('_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>')]
 assert not ops,ops
 result[name]={'monitored_call_counts':counts[name],'forbidden_application_operations':0}
assert counts['primary-complete']['_basis']>=1 and counts['primary-complete']['_checked']>=4
result['result']='PASS';result['candidate_and_runtime_bytes_unchanged']=True
(R/'results/final-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict) or 'monitored_call_counts' not in v},indent=2))
