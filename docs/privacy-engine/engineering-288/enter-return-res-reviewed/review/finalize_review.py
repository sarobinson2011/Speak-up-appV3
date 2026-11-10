"""Read-only post-run reconciliation and final candidate byte check."""
from bytes_only import B,read,save,fid,tree
import json,collections
r=B/'independent';rows=[json.loads(x) for x in (r/'progress.jsonl').read_text().splitlines()]
assert rows==[read(p) for p in sorted((r/'rows').glob('*.json'))]
stdout=[json.loads(x) for x in (B/'independent.stdout').read_text().splitlines()];res=read(r/'RESULT.json');ex=read(B/'independent-exit.json')
assert stdout[:-1]==rows and stdout[-1]=={'event':'RESULT','result':res}
assert [x['sequence'] for x in rows]==list(range(1,254)) and res['rows']==253 and res['status']=='PASS'
counts=dict(collections.Counter(x['status'] for x in rows));assert counts=={'PASS':159,'REJECTED':94} and all(res['counts'][k]==0 for k in ('FAIL','HARNESS-FAIL','DEFECT-OBSERVED'))
assert ex['returncode']==0 and ex['timed_out'] is False and ex['no_retry'] is True
for s in ('stdout','stderr'):assert fid(B/('independent.'+s))==ex['streams'][s]
layers={}
for row in rows:layers.setdefault(row['layer'],collections.Counter())[row['status']]+=1
save(B/'independent-reconciliation.json',{'status':'PASS','rows':253,'counts':counts,'individual_progress_stdout_RESULT_agreement':True,'layers':layers,'exit':ex,'qualifications':res['qualifications'],'environment':read(r/'environment.json'),'record_and_byte_audits_add_no_controls':True})
verification=tree(B/'candidate',read(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'))
save(B/'final-root-audit.json',{'status':'PASS','root':verification,'manifest':fid(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'),'implementation_changes':0,'fresh_public_or_host_run':False})
save(B/'final-audit.exit.json',{'exit':0,'failure':None})
print(json.dumps({'independent_rows':253,'counts':counts,'final_root':verification}))
