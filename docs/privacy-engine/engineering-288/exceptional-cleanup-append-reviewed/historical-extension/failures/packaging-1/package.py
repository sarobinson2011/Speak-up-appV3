"""Preserve completed new controls and exact dependency bytes; no validator execution."""
from pathlib import Path
import hashlib,json,stat,zipfile,datetime,os
T=Path(__file__).resolve().parents[1];root=T/'input';dest=T/'checkpoint';dest.mkdir(exist_ok=False)
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def cp(src,out):out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(src.read_bytes())
frozen=json.loads((root/'MANIFEST.json').read_bytes())
print('1/4 Preserve frozen inputs and finish read-only post-process membership/identity audit; no control replay',flush=True)
expected=set(frozen)|{'MANIFEST.json'};dirs={p.as_posix() for n in expected for p in Path(n).parents if p.as_posix()!='.'};files=set();seen=set()
for base,ds,fs in os.walk(root,followlinks=False):
 for n in ds:
  p=Path(base)/n;assert stat.S_ISDIR(p.lstat().st_mode);seen.add(p.relative_to(root).as_posix())
 for n in fs:
  p=Path(base)/n;assert stat.S_ISREG(p.lstat().st_mode);files.add(p.relative_to(root).as_posix())
assert files==expected and seen==dirs
for n,pin in frozen.items():
 b=(root/n).read_bytes();assert ident(b)==pin,n;out=dest/n;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
cp(root/'MANIFEST.json',dest/'provenance/frozen-input-manifest.json');cp(T/'RECOVERY-INPUT-IDENTITY.json',dest/'provenance/recovery-input-identity.json')
print('2/4 Reconcile completed groups and the interrupted primary attempt separately',flush=True)
groups={}
for name in ('source-1','recovered'):
 result=json.loads((T/'results'/name/'RESULT.json').read_bytes());exit_=json.loads((T/'processes'/name/'exit-status.json').read_bytes());assert result['result']=='PASS' and exit_['returncode']==0 and not exit_['timed_out'],name
 rows=[json.loads(x) for x in (T/'results'/name/'progress.jsonl').read_text().splitlines()];assert rows==result['rows'] and len(rows)==result['checks'],name
 stdout=(T/'processes'/name/'stdout.log').read_text().splitlines();recorded=[x for x in stdout if x.split(' ',1)[0].isdigit()];assert recorded==[str(i)+' '+row['check']+' '+row['result'] for i,row in enumerate(rows,1)],name
 groups[name]={'checks':result['checks'],'scope':result['scope'],'result_identity':ident((T/'results'/name/'RESULT.json').read_bytes()),'exit':exit_,'environment':result['environment'],'rows_progress_stdout_reconciled':True}
primary=T/'results/primary';pe=json.loads((T/'processes/primary/exit-status.json').read_bytes());assert pe['returncode']==-15 and pe['timed_out'] is True
assert not (primary/'RESULT.json').exists() and not (primary/'final-verification.json').exists() and not (primary/'calls.json').exists()
pr=[json.loads(x) for x in (primary/'progress.jsonl').read_text().splitlines()]
po=[x for x in (T/'processes/primary/stdout.log').read_text().splitlines() if x.split(' ',1)[0].isdigit()]
assert len(pr)==1300 and po==[str(i)+' '+row['check']+' '+row['result'] for i,row in enumerate(pr,1)]
assert all(row['result'] in ('PASS','REJECTED') for row in pr)
assert pr[-1]=={'check':'all inherited context relations preserved','result':'PASS'}
parsed={p.name:ident(p.read_bytes()) for p in primary.glob('*.json') if json.loads(p.read_bytes()) is not None}
assert (primary/'cleanup-append.json').read_bytes()==(T/'results/recovered/cleanup-append.json').read_bytes()==(root/'receipts/prepared-cleanup-append.json').read_bytes()
assert (primary/'actual-public-result.json').read_bytes()==(T/'results/recovered/actual-public-result.json').read_bytes()
qualified={'status':'INTERRUPTED_AT_PROCESS_DEADLINE; NOT A COMPLETED PRIMARY CAMPAIGN','recorded_rows':len(pr),'stdout_corroborated_rows':len(po),'rows_outside_completed_group_totals':True,'exit':pe,
 'last_recorded_control':pr[-1],'actual_public_positive':'Saved PASS through unchanged predecessor; identical receipt to completed recovered run. Does not establish successful primary campaign completion.',
 'last_saved_phase':'validation-layers.json and fixtures.json are complete JSON; final-verification.json, calls.json and RESULT.json are absent.',
 'exact_interrupted_instruction':'UNOBSERVED; interruption occurred after the saved validation-layer record and before final input-verification/result records were saved.',
 'partial_files':'All original primary files and process logs preserved unchanged; no synthetic RESULT.json or resumed campaign.',
 'new_failure':'Supervisor-enforced 3600-second deadline, exit -15; stderr empty; no assertion failure recorded. This does not turn the interrupted attempt into a PASS.',
 'read_only_completion_audit':{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_files':len(files),'input_directories':len(seen),'exact_membership_types_and_frozen_hashes':'PASS','primary_saved_json_files':parsed,'progress_stdout_reconciled':True,'validator_or_projector_calls':0,'control_replays':0,'qualification':'Post-process observation only; no intervening-history or monitoring-cleanup guarantee; lost process call log is not reconstructed.'}}
f=T/'failures/primary-timeout';f.mkdir(exist_ok=False);(f/'RECORD.json').write_bytes(enc(qualified))
for tree in ('results','processes','failures'):
 for p in sorted((T/tree).rglob('*')):
  if p.is_file():cp(p,dest/tree/p.relative_to(T/tree))
for n in ('README','RECOVERY'):cp(T/(n+'.final.txt'),dest/(n+'.txt'))
cp(Path(__file__),dest/'tools/package.py')
prior=json.loads((root/'retained/closure-review/review/CHECKPOINT.json').read_bytes())
results={'checkpoint':'I164-exceptional-cleanup-append-correspondence-1','author':'SU-Engineering[288D]','independent_review':'PENDING','completed_groups_separate':groups,'interrupted_primary_separate':qualified,'unqualified_combined_total':None,
 'failed_attempts_separate':{'preparation-membership':json.loads((T/'failures/preparation-membership/RECORD.json').read_bytes()),'primary-timeout':qualified},
 'validation_layers':{'primary':json.loads((T/'results/primary/validation-layers.json').read_bytes()),'recovered':json.loads((T/'results/recovered/validation-layers.json').read_bytes()),'new_source_controls':'46 source/producer checks; no predecessor authentication in that group'},
 'predecessor_LD01_closure_scope':prior['verdict'],'independent_LD01_groups_separate':prior['independent_groups'],'Engineering_LD01_groups_separate':prior['supplied_results_separate'],'prior_independent_groups_separate':prior['retained_independent_results_separate'],'prior_Engineering_groups_separate':prior['prior_Engineering'],'prior_failures_and_qualifications':prior['historical_qualifications'],
 'prior_LD01_audit_failure':prior['independent_read_only_audit_failure'],'prior_LD01_zero_replay_completion':prior['read_only_audit_completion'],'historical_NOT_ACCEPTED_verdict':prior['prior_verdict_preserved'],
 'runtime_changes':0,'requests':0,'database_connections':0,'session_operations':0,'acquisitions':0,'Git_saves':0,'prior_completed_campaigns_replayed':False,'prior_save_reused':'c43954ff5ee384c6fb6e7a85d83eb36bfea342d1',
 'limits':{'both_contexts_and_prefixes':True,'runtime_observations':'UNAVAILABLE','observer_join':None,'continuity':'EXPLICIT CONDITIONAL PREMISE','non_None_constructor_branch':'UNEXPANDED','line172_error_report_append':'UNEXPANDED','later_iterations_and_outer_cleanup':'UNEXPANDED','physical_closure_durability_released_ownership':False,'same_try':'Append failure does not erase established close return; close_error eligibility alone does not establish a close failure'},
 'preservation':{'both_acquisitions':'SEPARATE','obligations':11,'inventory_UNKNOWN':4,'lifetime_UNKNOWN':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}}
(dest/'RESULTS.json').write_bytes(enc(results));(dest/'START-HERE.txt').write_text('Read README.txt, RESULTS.json and RECOVERY.txt. New active public adapter: code/correspondence.py; current validated receipt from completed campaign: results/recovered/cleanup-append.json. Primary recorded 1300 corroborated rows but was interrupted at its deadline; it is not a completed campaign. Retained LD01/old documents remain historical with their original statuses. No completed-check replay authorized.\n')
names=sorted(p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file());assert 'MANIFEST.json' not in names
m={n:ident((dest/n).read_bytes()) for n in names};(dest/'MANIFEST.json').write_bytes(enc(m));names=['MANIFEST.json',*names]
for n in names:assert not n.startswith('/') and '..' not in Path(n).parts and stat.S_ISREG((dest/n).lstat().st_mode)
out=T.parent/'I164-exceptional-cleanup-append-correspondence-1.zip'
print('3/4 Write the exact checkpoint, preserving failures and prior qualifications',flush=True)
with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in names:
  zi=zipfile.ZipInfo(n);zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,(dest/n).read_bytes())
print('4/4 Verify archive membership, CRC and every manifested file hash',flush=True)
with zipfile.ZipFile(out) as z:
 assert z.namelist()==names and len(set(names))==len(names) and z.testzip() is None
 for n,pin in m.items():assert ident(z.read(n))==pin,n
identity={**ident(out.read_bytes()),'entries':len(names),'manifested_files':len(m),'filename':out.name,'CRC':'PASS','membership':'PASS','all_manifested_hashes':'PASS','completed_groups':{n:g['checks'] for n,g in groups.items()},'interrupted_primary_recorded_and_corroborated_rows':1300,'interrupted_primary_completed':False}
(T/'CHECKPOINT-IDENTITY.json').write_bytes(enc(identity));(T/'TASK-STATE.json').write_bytes(enc({'status':'CHECKPOINT_VERIFIED_READY_TO_SAVE','identity':identity}));print(json.dumps(identity,indent=2))
