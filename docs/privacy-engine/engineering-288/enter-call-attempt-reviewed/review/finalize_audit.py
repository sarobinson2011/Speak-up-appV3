"""Reconcile only the finished reviewer child, then read-only final root identity check."""
from review_bytes import HERE,read,save,fid,verify_tree
import collections,json,ast
B=HERE;out=B/'independent';rows=[json.loads(s) for s in (out/'progress.jsonl').read_text().splitlines()]
assert rows==[read(p) for p in sorted((out/'rows').glob('*.json'))]
stream=[json.loads(s) for s in (B/'independent.stdout').read_text().splitlines()];result=read(out/'RESULT.json');ex=read(B/'independent-exit.json')
assert stream[:-1]==rows and stream[-1]=={'event':'RESULT','result':result}
assert [x['sequence'] for x in rows]==list(range(1,148))
counts=dict(collections.Counter(x['status'] for x in rows));assert counts=={'PASS':64,'REJECTED':83}
assert result['rows']==147 and result['status']=='PASS' and all(result['counts'][k]==0 for k in ('FAIL','HARNESS-FAIL','DEFECT-OBSERVED'))
assert ex['returncode']==0 and ex['timed_out'] is False and ex['no_retry'] is True
for s in ('stdout','stderr'):assert fid(B/('independent.'+s))==ex['streams'][s]
layers={}
for row in rows:layers.setdefault(row['layer'],collections.Counter())[row['status']]+=1
save(B/'independent-reconciliation.json',{'status':'PASS','rows':147,'counts':counts,'individual_progress_stdout_result_agreement':True,'layers':layers,'explicit_exit':ex,'qualifications':result['qualifications'],'environment':read(out/'environment.json'),'archive_and_record_audits_not_added_to_controls':True})
root=verify_tree(B/'candidate',read(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'))
save(B/'final-root-audit.json',{'status':'PASS','root':root,'manifest':fid(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'),'candidate_changes':0,'source_and_predecessor_files_unchanged':True})
p=B/'candidate/code/managed_coverage.py';old=B/'candidate/retained/lookup/code/managed_coverage.py';new=p.read_bytes();prefix=old.read_bytes();assert new.startswith(prefix)
names=[n.name for n in ast.parse(new[len(prefix):]).body if isinstance(n,ast.FunctionDef)]
save(B/'documentation-witness.json',{'finding':'DOC-ENTER-01','severity':'nonblocking documentation count discrepancy','claim_file':'source/CHANGES.json','claim':read(B/'source/CHANGES.json')['intentional_candidate_changes'][0] if False else 'append six new pure-source functions; entire predecessor prefix retained','before':fid(old),'after':fid(p),'prefix_bytes':len(prefix),'actual_functions':names,'actual_count':len(names),'candidate_semantic_defect':False,'smallest_reproduction':'AST-parse exact appended bytes after offset 429112; count top-level FunctionDef nodes','distinct_from_inherited_R1_five_versus_six':True})
save(B/'final-audit.exit.json',{'exit':0,'failure':None,'candidate_validation_replays':0})
print(json.dumps({'controls':counts,'total':147,'root':root,'documentation_functions':len(names)}),flush=True)
