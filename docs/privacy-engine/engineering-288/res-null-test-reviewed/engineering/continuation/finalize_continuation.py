"""Reconcile and package saved records only. Does not import or execute candidate code."""
import collections, hashlib, json, shutil, zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encoded(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def write(p,v):p.write_bytes(encoded(v))
plan=read(P/'harness/FULL-PLAN.json');bplan=read(P/'harness/BATCH-PLAN.json')
old=read(P/'prior-results/RECONCILIATION.json')
prior=[read(f) for f in sorted((P/'prior-results/attempt-1/raw').glob('[0-9][0-9][0-9][0-9].json'))]
prior_progress=[json.loads(x) for x in (P/'prior-results/attempt-1/raw/progress.jsonl').read_bytes().splitlines()]
prior_stdout=[json.loads(x) for x in (P/'prior-results/attempt-1/stdout.log').read_bytes().splitlines()]
assert prior==prior_progress==prior_stdout and len(prior)==145
for n,r in enumerate(prior,1):
 assert r['sequence']==n and r['name']==plan[n-1]['name'] and r['layer']==plan[n-1]['layer']
assert old['explicit_exit']==read(P/'prior-results/attempt-1/exit.json')
new=[];batch_records=[];unstarted=[]
for spec in bplan['batches']:
 b=P/'batches'/spec['id']
 if not b.exists():unstarted.append(spec['id']);continue
 assert (b/'exit.json').exists() and (b/'RECONCILIATION.json').exists(),'Cannot package an active or unreconciled batch'
 rec=read(b/'RECONCILIATION.json');batch_records.append(rec)
 rows=[read(f) for f in sorted((b/'raw').glob('[0-9][0-9][0-9][0-9].json'))]
 assert [r['original_sequence'] for r in rows]==rec['original_sequences']
 for r in rows:
  expected=plan[r['original_sequence']-1]
  for k in ('name','layer','case','callsite','assertion_AST_sha256'):assert r[k]==expected[k]
 new.extend(rows)
ids=[r['sequence'] for r in prior]+[r['original_sequence'] for r in new]
assert len(ids)==len(set(ids)) and ids==list(range(1,len(ids)+1))
remaining=[x for x in range(1,317) if x not in ids]
complete=not remaining and all(r['status']=='COMPLETE' for r in batch_records) and len(new)==171
for n,pin in read(P/'source/MANIFEST.json').items():assert identity((P/'source'/n).read_bytes())==pin
assert {f.relative_to(P/'source').as_posix() for f in (P/'source').rglob('*') if f.is_file()}==set(read(P/'source/MANIFEST.json'))|{'MANIFEST.json'}
def counts(rows):return dict(collections.Counter(r['status'] for r in rows))
layers={}
for r in new:
 layer=layers.setdefault(r['layer'],{});layer[r['status']]=layer.get(r['status'],0)+1
summary={'status':'COMPLETE_FOCUSED_PLAN_ACROSS_SEPARATE_ATTEMPTS' if complete else 'PARTIAL_CONTINUATION_NO_AUTOMATIC_RETRY',
 'planned':316,'attempt_1':{'rows':145,'counts':counts(prior),'campaign_status':'TIMED_OUT_INCOMPLETE','exit':old['explicit_exit'],'missing_final_RESULT':True,'missing_child_FAILURE':True},
 'continuation':{'rows':len(new),'counts':counts(new),'batches':len(batch_records),'unstarted_batches':unstarted,'layer_counts':layers},
 'combined_coverage':{'rows':len(ids),'counts':counts(prior+new),'unique_original_sequences':ids,'remaining_original_sequences':remaining,'missing_records_reconstructed':False},
 'candidate_bytes_unchanged':True,'original_assertion_ASTs_unchanged':True,'completed_assertions_replayed':0,'setup_reconstruction_assertion_credit':0,
 'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'independent_acceptance':'PENDING',
 'confirmed_commit_reused':'18f94ee24bf148c0570df7db650f310defbb056e','git_operations':0,'host_operations':0,'database_session_operations':0,
 'historical_groups':'151 independent (81 PASS/70 REJECTED); 399 Engineering (196 PASS/203 REJECTED); one saved Ubuntu public positive; older 184/eight/750/single-positive groups remain separate.',
 'boundaries':'After line2517 comparison only; no true-branch decrement or false-branch stack/dispatch. Both acquisitions and contexts preserved; eleven obligations, four inventory/fourteen lifetime UNKNOWN; Decision B, retention and allowances unchanged. Zero-count destructor, runtime and qualified-binary gaps persist. SOURCE-ONLY, cumulative envelope unadopted, backup kernel-only, streams UNCOMPUTED, readiness/final binding blocked, admission disabled.'}
out=P/'final-delivery';out.mkdir(exist_ok=False)
for src,dest in [(P/'harness',out/'harness'),(P/'batches',out/'batches')]:shutil.copytree(src,dest)
for n in ('intake-verification.json','prepare_harness.py','finalize_continuation.py','preparation-identity.json','preparation-save.json'):
 if (P/n).exists():shutil.copy2(P/n,out/n)
(out/'preserved-attempt-1').mkdir();shutil.copy2(P/'intake/I164-res-null-test-1-results.zip',out/'preserved-attempt-1/I164-res-null-test-1-results.zip')
(out/'saved-checkpoints').mkdir()
for p in sorted(P.glob('batch-*-identity.json')):shutil.copy2(p,out/'saved-checkpoints'/p.name)
for p in sorted(P.glob('batch-*-save.json')):shutil.copy2(p,out/'saved-checkpoints'/p.name)
write(out/'RECONCILIATION.json',summary);write(out/'BATCH-RECONCILIATIONS.json',batch_records)
write(out/'COMBINED-INDEX.json',[{'original_sequence':r['sequence'],'group':'attempt-1','name':r['name'],'layer':r['layer'],'status':r['status']} for r in prior]+[{'original_sequence':r['original_sequence'],'group':'continuation','name':r['name'],'layer':r['layer'],'status':r['status'],'case':r['case'],'callsite':r['callsite']} for r in new])
write(out/'DEPENDENCIES.json',{'source':{'filename':'I164-res-null-test-1-source.zip','library_file_id':'libfile_fde3_f-4be7af487cac819189678acd4dc81981_39c64cf85e608191bb9545db7327fd84','bytes':3779700,'sha256':'280bf68065066e3da79f86ef85d68ea7f03a98e93ec02b078077a63eb1507667'},'attempt_1':{'filename':'I164-res-null-test-1-results.zip','library_file_id':'libfile_fde3_f-82a7b2bafb60819196a41f0a33d9a633_39c64cf85e608191bb9545db7327fd84','bytes':197874,'sha256':'6e0f8fc9dafc4d638b419cda5e130f354cbbbba46d29ecd93dbf4c271d1a82ee','embedded':True}})
write(out/'CHANGES.json',{'candidate_changes':[],'harness_only':{p.relative_to(P).as_posix():identity(p.read_bytes()) for p in sorted((P/'harness').rglob('*')) if p.is_file()},'assertions':'Original assertion calls and lambdas are checked against pinned AST hashes. The record function adds sequence/case/timing metadata; batch wrappers skip completed assertions without evaluating them. Original execution guards remain active. Pure-model setup reconstructed only for outstanding aggregate/context work; serialized setup is not authenticated evidence or physical identity.'})
write(out/'FAILURES.json',{'attempt_1':read(P/'prior-results/FAILURES.json'),'new_batches':[{'batch':r['batch'],'status':r['status'],'exit':r['explicit_exit'],'parse_errors':r['parse_errors']} for r in batch_records],'historical':'Original archives, omissions, discrepancies and qualifications remain unchanged. No retry or reconstruction of missing historical records.'})
(out/'RECOVERY.txt').write_text('Read RECONCILIATION.json and BATCH-RECONCILIATIONS.json first. This is saved evidence, not a new validation authorization. Retrieve the exact fixed source using DEPENDENCIES.json; verify archive identity and manifest before byte-only extraction under source/. Do not rerun completed assertions. FULL-PLAN pins all 316 original assertions by sequence, case/stage, callsite and AST identity; REMAINING-PLAN pins the authorized 171. Each batch preserves launch, raw rows, progress, stdout/stderr chunks, explicit exit, actual pure-model setup state and its lineage. The original results ZIP is embedded byte-for-byte. Attempt 1 remains a timeout with no final RESULT/FAILURE, even if combined assertion coverage is complete. Public authentication and authenticated constructed paths remain UNEXECUTED. Independent acceptance is pending. For a partial continuation, remaining_original_sequences states the exact uncompleted set; no automatic retry is authorized. No application/runtime, database, session, host or Git operation occurred. Admission remains disabled.\n')
(out/'START-HERE.txt').write_text(summary['status']+'\nFixed I164-RES-NULL-TEST-1 candidate. Read RECONCILIATION.json, DEPENDENCIES.json, CHANGES.json and RECOVERY.txt. Counts distinguish the retained timed-out attempt from the new bounded batches. Negative claims apply only at each recorded layer; no full public negative derivation.\n')
members={f.relative_to(out).as_posix():identity(f.read_bytes()) for f in sorted(out.rglob('*')) if f.is_file()};write(out/'MANIFEST.json',members)
zpath=P/'I164-res-null-test-1-continuation-results.zip'
with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(out).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(members)+1
 for n,pin in members.items():assert identity(z.read(n))==pin
result={'filename':zpath.name,**identity(zpath.read_bytes()),'entries':len(members)+1,'status':summary['status'],'continuation':summary['continuation'],'combined_counts':summary['combined_coverage']['counts'],'remaining':remaining}
write(P/'final-identity.json',result);print(json.dumps(result,indent=2))
