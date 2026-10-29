from pathlib import Path,PurePosixPath
import sys,json,zipfile,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integrity import check_tree,ident,PIN
w=Path(__file__).resolve().parents[2];base=w/'cs-review';archive=w/'upload/I164-client-state-return-correspondence-1(1).zip';raw=archive.read_bytes();assert ident(raw)==PIN
with zipfile.ZipFile(archive) as z:
 names=z.namelist();m=json.loads(z.read('MANIFEST.json'));parents={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'};mi=ident(z.read('MANIFEST.json'))
 for root in (w/'cs-input',w/'cs-recovered'):check_tree(root,names,parents,m,mi)
totals={};groups={}
for label in ('primary','recovered'):
 rows=[];group=[]
 for p in sorted((base/('independent-'+label)).glob('*/RESULT.json')):
  r=json.loads(p.read_bytes());progress=[json.loads(x) for x in p.with_name('progress.jsonl').read_text().splitlines()];assert r['result']=='PASS' and r['error'] is None and r['rows']==progress and r['checks']==len(progress)
  rows.extend(progress);group.append({'path':p.parent.relative_to(base).as_posix(),'checks':len(progress),'result':ident(p.read_bytes()),'seconds':r['seconds'],'environment':r['environment']})
 totals[label]=len(rows);groups[label]=group
assert totals=={'primary':273,'recovered':196}
f=base/'failures/reviewer-handler-shape-attempt-1';r=json.loads((f/'results/RESULT.json').read_bytes());assert r['result']=='FAIL' and r['checks']==17 and r['rows']==[json.loads(x) for x in (f/'results/progress.jsonl').read_text().splitlines()]
cli=json.loads((base/'cli-recovered/RESULT.json').read_bytes());assert cli['result']=='PASS' and cli['process']['exit_code']==0
r={'result':'PASS','input_archive_after_testing':ident(raw),'unchanged_roots':{'files_each':len(names),'directories_each':len(parents),'roots':['cs-input','cs-recovered'],'regular_exact_membership_and_bytes':'PASS'},'independent_completed_checks':totals,'independent_groups':groups,'separate_actual_public_CLI':cli,'reviewer_failed_attempts':[{'path':f.relative_to(base).as_posix(),'checks_before_failure':17,'included_in_completed_totals':False,'reason':'Incomplete reviewer expectation for nested handler annotation; source-derived corrected test passed. Implementation unchanged.'}],'supplied_counts_separate':{'primary':171,'recovered':173,'fresh_process_assertions':5},'new_implementation_defect_witness':None,'implementation_modified':False}
(base/'results/final-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'result':'PASS','checks':totals,'separate_CLI':1,'failed_attempt_checks_excluded':17,'input_members_unchanged':len(names)}))
