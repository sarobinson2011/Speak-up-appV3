"""Package only finalized independent results; never execute candidate code."""
from pathlib import Path
import hashlib,json,re,stat,zipfile,sys
BASE=Path('/workspace/scratch/ace5c9b2f18b');R=BASE/'cc-review';INPUT=BASE/'upload/I164-control-callback-exception-correspondence-1(1).zip'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
assert sys.argv[1:]==['--supported-after-review']
groups={};total=0
for name in ('primary','recovered','source','coordinated','fresh-public','fresh-semantic'):
 d=R/'results'/name;raw=(d/'RESULT.json').read_bytes();v=json.loads(raw);assert v['result']=='PASS' and v['error'] is None,name
 progress=[json.loads(b) for b in (d/'progress.jsonl').read_bytes().splitlines()];assert progress==v['rows'] and len(progress)==v['checks']
 printed=[]
 for line in (R/'results'/(name+'.stdout')).read_text().splitlines():
  m=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED)',line)
  if m:printed.append((int(m[1]),m[2],m[3]))
 assert printed==[(i,x['check'],x['result']) for i,x in enumerate(progress,1)],name
 assert all(v[k]==0 for k in ('runtime_calls','session_operations','database_connections'))
 groups[name]={'controls':len(progress),'outcomes':{k:sum(x['result']==k for x in progress) for k in ('PASS','REJECTED')},'identity':pin(raw),'seconds':v['seconds'],'environment':v['environment'],'stdout_progress_result_exact':True};total+=len(progress)
integrity=json.loads((R/'results/integrity.json').read_bytes());recovered=json.loads((R/'results/recovered-integrity.json').read_bytes());audit=json.loads((R/'results/composition-and-supplied.json').read_bytes());final=json.loads((R/'results/final-verification.json').read_bytes())
assert pin(INPUT.read_bytes())==integrity['archive']
verdict='SUPPORTED within the bounded mandatory SOURCE-ONLY control-callback exception correspondence contract'
checkpoint={'checkpoint':'Formal-Lab6-I164-control-callback-exception-independent-review','date':'2026-10-30','review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'target':'I164-control-callback-exception-correspondence-1.zip','input':integrity['archive'],'entries':3069,'manifested_hashes':3068,'verdict':verdict,'smallest_residual_witness':None,'integrity':integrity,'recovered_integrity':recovered,'final_roots':final,'preservation_and_supplied_records':audit,'independent_controls':total,'independent_groups':groups,'actual_CLI_counted_once':True,
 'supplied_results_inspected_not_rerun':{'primary':276,'recovered_root':64,'public_process':7,'logs_reconciled':True,'two_zero_control_failures':True,'four_partials_preserved':True,'prior_independent':459,'historical_Engineering_primary':[308,307,303],'historical_missing_progress_ordinal':304,'historical_missing_stdout_ordinals':[304,305,306,307,308],'historical_gap_cause':'UNESTABLISHED','historical_separate_recovered_public':[78,5]},
 'independent_failed_attempts':[{'kind':'Audit incorrectly conflated failed outer and strict predecessor manifest membership','path':'failures/audit-membership-level','controls_completed':0,'included_in_completed_totals':False,'candidate_changed':False,'only_review_audit_corrected':True}],
 'limits':{'static_constructed_only':True,'control_constructor_must_complete_before_selected_frontier':True,'control_callable_body_execution_observed':False,'source_guard':'control is not None','selected_owner_failure_guard':False,'subsequent_client_handler_selected':False,'control_exception_exact_type_value_history_frame':'UNAVAILABLE','new_explicit_cause_assignment_established':False,'existing_cause_context_suppression_cleanup_link':'UNKNOWN','selected_owner_registry_continuity':'Explicit conditional premise; UNKNOWN remains supported','cleanup_may_supersede_control_propagation':True,'termination_establishes_new_exception_unwind_or_removal':False,'earlier_prefix_facts_erased':False,'runtime_control_finally_removal_chain':'UNAVAILABLE','control_constructor_exception_expansion':'OUTSIDE SLICE','full_outer_cleanup':'UNEXPANDED','exceptional_owner_lock_finalization':'UNEXPANDED','physical_reference_equality_or_inequality':'UNESTABLISHED','physical_lock_release_exclusivity_durability':'UNESTABLISHED','saved_traced_invocations':18,'observer':'Separate frameless Client.state call; UNJOINED','lifetime_repetition_coverage':False},
 'boundaries':{'obligations':11,'obligations_identity':{'bytes':56813,'sha256':'2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45'},'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False},
 'operations':dict.fromkeys(('implementation_changes','runtime_changes','acquisitions','requests','database_connections','session_operations','host_smokes','Git_saves','completed_suite_reruns','completed_review_reruns','lifecycle_reruns','policy_changes'),0)}
(R/'CHECKPOINT.json').write_bytes(enc(checkpoint))
draft=(R/'REPORT.draft.txt').read_text().replace('VERDICT_PENDING_COMPLETED_CHECKS',verdict+'. No residual defect witness was found within this retained contract.')
table='\nCompleted independent validation\n\n'+str(total)+' completed independent controls, separate from supplied and inherited results. Integrity/composition audits are not inflated into this total.\n\n| Group | Controls | PASS | Expected rejection |\n| --- | ---: | ---: | ---: |\n'
for n,v in groups.items():table+=f"| {n} | {v['controls']} | {v['outcomes']['PASS']} | {v['outcomes']['REJECTED']} |\n"
table+='''\nAll successful independent result rows reconcile exactly with progress and captured stdout. Cases are independently assembled and checked against a separate source-based outcome oracle. Primary and recovered groups each validate the real mandatory predecessor chain and derive the exact current receipt. Direct paired-substitution controls use the newly independently authenticated fixtures; these pure producer controls do not themselves authenticate a root. Source controls independently traverse AST ancestry and reject coordinated source/pin changes. The fresh public process executes the actual CLI, requires both contexts and all five relations, checks returned-result isolation and rejects a coordinated invented cause/client-handler receipt. The separate fresh semantic process rejects altered authenticated evidence. Narrow checks of retained reviewed branches exercise only their connection through the new adapter; no old campaign is rerun.\n'''
(R/'REPORT.txt').write_text(draft+table)
(R/'START-HERE.txt').write_text('Read REPORT.txt and CHECKPOINT.json. Exact target ZIP is under input/. This is an author-independent bounded review; supplied results, historical qualifications and failed attempts remain separate. No operational or admission authorization is added.\n')
(R/'RECOVERY.txt').write_text('Verify this review ZIP identity, CRC, safe unique regular membership and MANIFEST.json hashes. The unchanged target ZIP under input/ has the identity in CHECKPOINT.json. Its self-contained source/dependency contents recover the mandatory static validator. Original outer predecessor/recovery-cut ZIP identities remain continuity records where duplicate outer bytes were omitted; do not recompress and claim original identities. Forensic partials remain in their declared failure locations outside strict predecessor roots. Reuse completed controls; recovery does not authorize campaign or session operations.\n')
files={}
for p in sorted(R.rglob('*')):
 if not p.is_file():continue
 n=p.relative_to(R).as_posix()
 if n in ('REPORT.draft.txt','MANIFEST.json'):continue
 assert stat.S_ISREG(p.lstat().st_mode);files[n]=p.read_bytes()
files['input/I164-control-callback-exception-correspondence-1.zip']=INPUT.read_bytes();files['MANIFEST.json']=enc({n:pin(b) for n,b in sorted(files.items())})
target=BASE/'Formal-Lab6-I164-control-callback-exception-independent-review.zip';assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(files.items()):
  i=zipfile.ZipInfo(n,(2026,10,30,0,0,0));i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
record={'archive':str(target),'identity':pin(target.read_bytes()),'entries':len(files),'manifested_hashes':len(files)-1,'independent_controls':total,'verdict':verdict}
(BASE/'cc-package.json').write_bytes(enc(record));print(json.dumps(record,indent=2))
