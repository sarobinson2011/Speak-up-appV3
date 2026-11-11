from bytes_only import *
import collections
r=B/'independent-completion'
rows=[read(p) for p in sorted(r.glob('[0-9][0-9][0-9][0-9].json'))]
progress=[json.loads(x) for x in (r/'progress.jsonl').read_text().splitlines()]
stdout=[json.loads(x) for x in (B/'independent-completion.stdout').read_text().splitlines()]
result=read(r/'RESULT.json');ex=read(B/'independent-completion-exit.json')
assert rows==progress==stdout[:-1] and stdout[-1]=={'event':'RESULT','result':result}
assert len(rows)==151 and [x['sequence'] for x in rows]==list(range(1,152))
assert collections.Counter(x['status'] for x in rows)=={'PASS':81,'REJECTED':70}
assert result['counts']=={'PASS':81,'REJECTED':70,'FAIL':0} and ex['exit']==0 and ex['timeout'] is False
assert (B/'independent-completion.stderr').read_bytes()==b''
assert fid(B/'independent_controls_completion.py')==read(B/'independent-completion-launch.json')['script']
failed=read(B/'independent/0001.json');assert failed['status']=='FAIL' and failed['detail']['type']=='StopIteration' and read(B/'independent-exit.json')['exit']==1
layers={}
for x in rows:layers.setdefault(x['layer'],collections.Counter())[x['status']]+=1
save(B/'independent-reconciliation.json',{'status':'PASS','completed_controls':151,'counts':result['counts'],'layers':layers,'individual_progress_stdout_RESULT_exact_agreement':True,'exit':ex,'stderr':fid(B/'independent-completion.stderr'),'prior_failed_attempt':{'rows':1,'successful_controls':0,'candidate_model_controls':0,'exit':1,'cause':'reviewer nonexistent configuration path; retained original script and traceback'},'completed_controls_replayed':0,'public_runs':0,'authenticated_constructed_path':'UNTESTED','full_public_negative_derivations':0,'environment':read(r/'environment.json')})
root=tree(B/'candidate',read(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'))
assert root['files']==4500 and root['directories']==1216
save(B/'final-root-audit.json',dict(root,after_independent_controls=True,implementation_unchanged=True))
save(B/'final-audit.exit.json',{'exit':0,'control_reconciliation':'PASS','candidate_after_review':'UNCHANGED'})
print(json.dumps({'completed':151,'PASS':81,'REJECTED':70,'exit':0,'root':root}),flush=True)
