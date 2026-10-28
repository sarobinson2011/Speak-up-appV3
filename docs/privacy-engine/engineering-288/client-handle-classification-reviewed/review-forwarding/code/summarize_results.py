"""Aggregate completed new controls, with no validation execution."""
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parents[1]
groups={'primary':['core','legitimate','wrong-instance-0','wrong-instance-1','catalogue','journal-semantic','journal-derivation','mutable-input','missing-export','stale-output','public-omission','public-status','public-contexts','public-stale','semantic-alias','public-alias'], 'recovered':['core','wrong-instance-1','journal-derivation','missing-export','public-omission','public-alias']}
for mode,names in groups.items():
 root=base/('independent-'+mode);rows=[];records=[];calls=[];source=None;environment=None
 for name in names:
  p=root/name/'RESULT.json';raw=p.read_bytes();r=json.loads(raw);progress=[json.loads(x) for x in (p.parent/'progress.jsonl').read_text().splitlines()]
  assert r['result']=='PASS' and r['error'] is None and r['checks']==progress and len(progress)==r['assertions'] and r['recovered']==(mode=='recovered')
  assert all(x['result'] in ('PASS','REJECTED') for x in progress)
  if source is None:source=r['source'];environment=r['environment']
  assert source==r['source'] and environment==r['environment']
  if name!='core':
   process=json.loads((base/'processes'/(mode+'-'+name)/'RESULT.json').read_bytes());assert process['exit_code']==0 and process['result']=='PASS'
  rows.extend(dict(x,group=name) for x in progress);records.append({'group':name,'assertions':r['assertions'],'result_identity':{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}})
  calls.extend(dict(x,group=name) for x in json.loads((p.parent/'call-observations.json').read_bytes()))
 for kind in (('semantic','derivation') if mode=='primary' else ('derivation',)):
  assert any(x['check']=='coordinated journal and claims journal-'+kind and x['error']['message']=='HANDLE-VALIDATED-JOURNAL' for x in rows)
 assert any(x['check']=='pristine public after nested mutations' for x in rows)
 result={'result':'PASS','assertions':len(rows),'categories':{c:sum(x['category']==c for x in rows) for c in sorted({x['category'] for x in rows})},'checks':rows,'groups':records,'source':source,'environment':environment,'recovered':mode=='recovered','error':None,'partial_failed_or_interrupted_groups_included':False,'requests_issued':0,'new_signatures':0,'database_connections':0,'session_operations':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
 (root/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(root/'progress.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows));(root/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n')
 print(mode,len(rows),'assertions in',len(records),'completed groups')
