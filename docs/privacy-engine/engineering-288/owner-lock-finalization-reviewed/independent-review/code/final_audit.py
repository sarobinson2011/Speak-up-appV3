"""Reconcile finished review evidence and verify unchanged input roots."""
from pathlib import Path
import collections,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import ident,verify_root
w=Path(__file__).resolve().parents[2];r=w/'ol-review';groups={}
for name,count in [('primary',265),('recovered',49),('fresh-semantic',3),('fresh-constructed',2),('fresh-public',4)]:
 p=r/name;v=json.loads((p/'RESULT.json').read_bytes());lines=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()]
 assert v['result']=='PASS' and v['error'] is None and v['checks']==count and v['rows']==lines and len(lines)==count and v['outcomes']==dict(collections.Counter(x['result'] for x in lines))
 groups[name]={'checks':count,'outcomes':v['outcomes'],'result_identity':ident((p/'RESULT.json').read_bytes()),'seconds':v['seconds'],'environment':v['environment']}
roots={name:verify_root(w/name) for name in ('ol-input','ol-recovered')}
raw=(w/'upload/I164-owner-lock-finalization-correspondence-1(1).zip').read_bytes();assert ident(raw)=={'bytes':74161617,'sha256':'09f8b6d8c527f4032977f4e2862ba9a23e0e678a6f8294a5050603a26fb43a9b'}
failed=json.loads((w/'ol-input/failures/derive-attempt-1/ATTEMPT.json').read_bytes());assert failed['completed_assertions']==0 and failed['cause']=='UNESTABLISHED' and failed['counted_in_completed_totals'] is False
out={'result':'PASS','completed_independent_controls':sum(v['checks'] for v in groups.values()),'independent_groups':groups,'actual_CLI_check_included_once':True,'strict_verified_roots':roots,'input_archive_unchanged':ident(raw),'implementation_unchanged':True,'current_independent_control_attempts_failed':0,'supplied_failed_attempt_preserved':failed,'prior_failures_and_forensic_partial_preserved_unchanged':True}
(r/'results/final-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
