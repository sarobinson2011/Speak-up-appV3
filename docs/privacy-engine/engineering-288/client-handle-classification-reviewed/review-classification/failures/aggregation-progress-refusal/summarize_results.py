"""Aggregate only completed independent groups; no validator execution."""
from pathlib import Path
import json,hashlib
b=Path(__file__).resolve().parents[1]
groups={'primary':['core','additional','legitimate','semantic-contract','derive-contract','claims','public-old','public-coordinated','public-missing','semantic-alias','public-alias'],'recovered':['core','additional','legitimate','semantic-contract','public-old','public-alias']}
for mode,names in groups.items():
 rows=[];records=[];environment=None;root=b/('independent-'+mode)
 for name in names:
  p=root/name/'RESULT.json';raw=p.read_bytes();d=json.loads(raw);progress=[json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]
  assert d['result']=='PASS' and d['error'] is None and len(progress)==d['checks'] and progress==d['rows'] and all(x['result'] in ('PASS','REJECTED') for x in progress)
  if environment is None:environment=d['environment']
  assert environment==d['environment'];rows.extend(dict(x,group=name) for x in progress);records.append({'name':name,'checks':d['checks'],'identity':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}})
  if name not in ('core','additional'):
   calls=json.loads((p.parent/'calls.json').read_bytes());assert any(x['function']=='derive_handle' for x in calls)
   record=b/'processes'/(mode+'-'+name)/'RESULT.json'
   if record.exists():assert json.loads(record.read_bytes())['exit_code']==0
 result={'result':'PASS','checks':len(rows),'rows':rows,'groups':records,'categories':{k:sum(x['kind']==k for x in rows) for k in sorted({x['kind'] for x in rows})},'environment':environment,'failures_included':False,'old_suites_rerun':False,'constructed_is_runtime_evidence':False}
 (root/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(mode,len(rows),'checks',len(names),'groups')
