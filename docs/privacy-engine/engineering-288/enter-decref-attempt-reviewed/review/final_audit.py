"""Read-only final reconciliation and byte preservation; no validation replays."""
from bytes_only import *
import collections,tarfile,ast
records={}
for name,folder in [('independent','independent'),('direct-alias','direct-alias')]:
 d=B/folder;rows=[json.loads(x) for x in (d/'progress.jsonl').read_text().splitlines()];out=[json.loads(x) for x in (B/(name+'.stdout')).read_text().splitlines()];res=read(d/'RESULT.json');ex=read(B/(name+'-exit.json'))
 assert rows==out[:-1]==[read(p) for p in sorted(d.glob('[0-9][0-9][0-9][0-9].json'))]
 assert [x['sequence'] for x in rows]==list(range(1,len(rows)+1)) and out[-1]=={'event':'RESULT','result':res}
 assert res['counts']==dict(collections.Counter(x['status'] for x in rows)) and res['rows']==len(rows) and res['result']=='PASS' and not res['failures']
 assert ex['returncode']==0 and ex['timed_out'] is False and ex['no_retry'] is True
 assert all(ex['streams'][s]==fid(B/(name+'.'+s)) for s in ('stdout','stderr')) and ex['streams']['stderr']['bytes']==0
 layers={}
 for x in rows:layers.setdefault(x['layer'],collections.Counter())[x['status']]+=1
 records[name]={'counts':res['counts'],'rows':len(rows),'layers':layers,'exact_individual_progress_stdout_RESULT_agreement':True,'exit':ex}
assert records['independent']['counts']=={'PASS':90,'REJECTED':94}
assert records['direct-alias']['counts']=={'PASS':6,'REJECTED':2}
records.update({'combined_fresh_only':{'rows':192,'PASS':96,'REJECTED':96},'public_authentication_runs':0,'authenticated_constructed_runs':0,'full_public_negative_derivations':0,'supplied_campaign_replays':0,'environment':read(B/'independent/environment.json'),'primary_alias_qualification':'Primary nested-output negatives mutate deepcopy; genuine actual-return isolation is established by separate eight-row supplement, not retroactively attributed.'})
save(B/'independent-reconciliation.json',records)
root=B/'candidate';post=tree(root,read(B/'host/expected/ASSEMBLED-ROOT-MANIFEST.json'));assert post['files']==4271 and post['directories']==1197
save(B/'post-review-root-audit.json',post)
f=root/'fixtures/retained-return-cases.json';assert f.read_bytes()==(B/'prior-review/independent/constructed-normal-cases.json').read_bytes()
tar=B/'prior-review/inputs/I164-enter-return-res-public-1-host-evidence.tar.gz'
assert fid(tar)=={'bytes':10112583,'sha256':'bcd694478e38d06777112a45b6d2ea1e20f251bddf35de30cd634c4c47ca7155'}
with tarfile.open(tar,'r:gz') as t:raw=t.extractfile('validation/results/actual-derived-receipt.json').read()
assert raw==(root/'reference/return/actual-receipt.json').read_bytes()
save(B/'predecessor-exact-byte-reuse.json',{'status':'PASS','receipt_byte_equality_to_prior_actual_saved_output':True,'prior_host_archive':fid(tar),'receipt':ident(raw),'retained_24_fixtures_exact_bytes':fid(f),'runtime_reexecution':False,'source_recovery_noop_line':'recover_bytes.py contains a non-contributing conditional-True assertion; no verification credit assigned to it. Actual prior receipt byte equality is independently checked here and by prior manifest pins.'})
save(B/'final-audit.exit.json',{'exit':0,'validation_replays':0});print(json.dumps({'fresh':records['combined_fresh_only'],'root':post}),flush=True)
