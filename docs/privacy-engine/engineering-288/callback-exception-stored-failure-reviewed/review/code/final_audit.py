from pathlib import Path
import sys,json,collections,zipfile
sys.path.insert(0,str(Path(__file__).parent))
from integrity import root
W=Path(__file__).resolve().parents[2];R=W/'cb-review';result={}
for p in [Path('/workspace/review-evidence/FL6-callback-20261030')/s for s in ('primary','recovered')]:
 result[str(p)]=root(p)
 with zipfile.ZipFile(W/'upload/I164-callback-exception-stored-failure-correspondence-1(1).zip') as z:
  for n in ('code/managed_coverage.py','code/correspondence.py','source-evidence/prospective_entry.py','source-evidence/lab_bootstrap.py','source-evidence/live_connection.py'):assert (p/n).read_bytes()==z.read(n)
for name in ('primary','recovered','source-controls','completion','fresh-public','fresh-normal'):
 p=R/'results'/name;r=json.loads((p/'RESULT.json').read_bytes());assert r['result']=='PASS' and r['error'] is None;calls=json.loads((p/'calls.json').read_bytes());counts=dict(collections.Counter(c['function'] for c in calls))
 assert not [v for v in calls if Path(v['file']).name=='prospective_entry.py' and v['function'] not in ('_identity','_regular','verify_inputs','walk','<genexpr>','<setcomp>','<dictcomp>','<listcomp>')]
 if name in ('primary','recovered'):assert counts['_basis']>=1 and counts['_checked']>=5
 if name=='fresh-normal':assert counts['constructed_normal_callback']>=1 and counts['semantic']>=1
 result[name]={'monitored_calls':counts,'forbidden_application_operations':0}
result.update(result='PASS',implementation_and_runtime_source_bytes_unchanged=True)
(R/'results/final-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict) or 'monitored_calls' not in v},indent=2))
