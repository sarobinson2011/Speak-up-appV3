from bytes_only import *
from collections import Counter
O=B/'independent'
rows=[read(p) for p in sorted(O.glob('[0-9][0-9][0-9][0-9].json'))]
progress=[json.loads(x) for x in (O/'progress.jsonl').read_text().splitlines()]
stdout=[json.loads(x) for x in (B/'independent.stdout').read_text().splitlines()]
result=read(O/'RESULT.json');ex=read(B/'independent-exit.json')
assert rows==progress==stdout[:-1] and stdout[-1]=={'event':'RESULT','result':result}
assert len(rows)==159 and [x['sequence'] for x in rows]==list(range(1,160))
assert Counter(x['status'] for x in rows)=={'PASS':79,'REJECTED':80}
assert result['counts']=={'PASS':79,'REJECTED':80,'FAIL':0} and ex['exit']==0 and ex['timed_out'] is False
assert (B/'independent.stderr').read_bytes()==b''
assert fid(B/'independent_controls.py')==read(B/'independent-launch.json')['script']
layers={}
for r in rows:layers.setdefault(r['layer'],Counter())[r['status']]+=1
save(B/'independent-reconciliation.json',{'status':'PASS','completed_controls':159,'counts':result['counts'],'layers':layers,'individual_progress_stdout_RESULT_exact_agreement':True,'exit':ex,'stderr':fid(B/'independent.stderr'),'fresh_public_runs':0,'authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'parent_setup_credit':0,'environment':read(O/'environment.json')})
root=tree(B/'candidate',read(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'))
assert root['files']==4729 and root['directories']==1238
save(B/'final-root-audit.json',dict(root,after_independent_controls=True,implementation_unchanged=True))
save(B/'final-audit.exit.json',{'exit':0,'control_reconciliation':'PASS','candidate_after_review':'UNCHANGED'})
print(json.dumps({'rows':159,'PASS':79,'REJECTED':80,'exit':0,'root':root}),flush=True)
