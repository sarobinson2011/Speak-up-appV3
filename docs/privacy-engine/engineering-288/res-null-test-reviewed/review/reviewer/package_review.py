from bytes_only import *
out=B/'I164-res-null-test-1-independent-review.zip';assert not out.exists()
ind=read(B/'independent-reconciliation.json');h=read(B/'host-record-audit.json');a=read(B/'focused-record-audit.json');s=read(B/'source-recovery-audit.json')
assert read(B/'final-audit.exit.json')['exit']==0 and read(B/'focused-record-audit-corrected.exit.json')['exit']==0 and read(B/'host-record-audit.exit.json')['exit']==0
cp={'identity':'I164-RES-NULL-TEST-1-INDEPENDENT-REVIEW','reviewer':'Formal-Lab[6] / Codex, independent of Engineering construction','verdict':'SUPPORTED within bounded conditional SOURCE-ONLY pointer-comparison contract','candidate_defect_demonstrated':False,'smallest_defect_witness':None,'implementation_unchanged':True,'root':read(B/'final-root-audit.json'),'producer':s['producer'],'adapter':s['adapter'],'unchanged_prefix':s['unchanged_prefix'],'appended_functions':s['appended_functions'],'source_boundary':{'comparison':'bytecodes.c:2517 / generated_cases.c.h:3531','true_stop_before':'Py_DECREF(exit), bytecodes.c:2518 / generated_cases.c.h:3532','false_stop_before':'STACK_GROW, generated_cases.c.h:3536; no stack stores or dispatch'},'fresh_independent':{'completed':159,'PASS':79,'REJECTED':80,'exit':0,'timed_out':False,'layers':'independent-reconciliation.json / individual rows','pure_parent_setup_credit':0},'Engineering_timeout':a['timeout_attempt'],'Engineering_continuation':{'rows':171,'PASS':54,'REJECTED':117,'batches':5,'all_exits':0},'unique_Engineering_plan_coverage':{'rows':316,'PASS':135,'REJECTED':181,'not_one_successful_campaign':True},'saved_public':{'positives':1,'actual_basis_captures':1,'receipt':h['receipt'],'exact_receipt_bytes_both_contexts':True,'child_exit':0,'child_finished_utc':h['child_exit']['finished_utc'],'child_seconds':h['child_exit']['seconds'],'wrapper_exit':0,'manager':'success/exited/0','EVENT_rows':286,'stdout_chunks':285,'progress_snapshots':230,'selected_computation_entries_returns':17846,'computation_events_add_controls':False},'fresh_public_runs':0,'authenticated_constructed_path':'UNEXECUTED','full_public_negative_derivations':0,'runtime_arrival_effects':'UNESTABLISHED','qualified_binary_correspondence':'UNESTABLISHED','zero_count_destructor_completion':'UNRESOLVED','environment':ind['environment'],'prior_50_0_2_evidence':'distinct; no equivalence or fresh qualification','reviewer_read_only_audit_failure':'Preserved wrong-index-schema assertion, exit1; corrected exact reconciliation passes; zero candidate controls in either audit','historical_qualifications':'Preserved separately in exact source/results/parent inputs; preparation-only chronology retained','both_acquisitions':'PRESERVED','obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':True,'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False,'Git_operations':0}
save(B/'CHECKPOINT.json',cp)
files={}
def add(p,n=None):
 p=Path(p);n=n or p.relative_to(B).as_posix();safe(n);assert n not in files;files[n]=p.read_bytes()
for n in ('REVIEW.txt','RECOVERY.txt','INPUTS.json','FAILURES.json','CHECKPOINT.json'):add(B/n)
for p in sorted(B.glob('*.py')):add(p,'reviewer/'+p.name)
for p in sorted(B.glob('*.json')):
 if p.name not in files:add(p,'audits/'+p.name)
for p in sorted((B/'independent').rglob('*')):
 if p.is_file():add(p)
for n in ('independent.stdout','independent.stderr'):add(B/n,'streams/'+n)
for key in ('source','focused_results'):
 n=read(B/'host/INPUTS.json')[key]['filename'];add(B/'host/inputs'/n,'inputs/'+n)
for p in sorted((B/'host/validation/results').glob('*.json')):
 if p.name!='actual-derived-receipt.json':add(p,'saved-host/results/'+p.name)
add(B/'host/validation/results/events.jsonl','saved-host/results/events.jsonl')
for n in ('exit.json','capture.json','process.json','launch.json','stdout.log','stderr.log','chunk-index.jsonl','computation-phases.jsonl'):add(B/'host/validation/process'/n,'saved-host/process/'+n)
for n in ('PLAN.json','INPUTS.json','FAILURES.json','PREPARED.json','ONE-ATTEMPT-RESERVATION.json','LAUNCH-RECEIPT.json','service-exit.json','manager-exit.json','service-runtime-profile.json','AUTHENTICATION-PATH.txt','RECOVERY.txt','MANIFEST.json'):
 add(B/'host'/n,'saved-host/'+n)
for n in ('public_positive.py','host_prepare_launch.py'):add(B/'host/code'/n,'saved-host/code/'+n)
add(B/'host/observer-reference/native_observer.py','saved-host/observer-reference/native_observer.py')
for p in sorted((B/'host/expected').glob('*ROOT-MANIFEST.json')):add(p,'recovery-pins/'+p.name)
old=B.parent/'fast-review'
for n in ('REVIEW.txt','CHECKPOINT.json','FAILURES.json','RECOVERY.txt','independent-reconciliation.json','INPUTS.json'):add(old/n,'reused-fast-review/'+n)
manifest={n:ident(v) for n,v in files.items()};files['MANIFEST.json']=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,v in sorted(files.items()):
  i=zipfile.ZipInfo(n,(2026,11,11,16,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.create_system=3;i.external_attr=(stat.S_IFREG|0o600)<<16;z.writestr(i,v)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==len(files) and set(z.namelist())==set(files)
 for n,pin in manifest.items():assert ident(z.read(n))==pin
delivery={'filename':out.name,**fid(out),'entries':len(files),'manifested_hashes':len(manifest),'CRC_safe_exact_membership_hashes':'PASS'}
save(B/'delivery-identity.json',delivery);print(json.dumps(delivery),flush=True)
