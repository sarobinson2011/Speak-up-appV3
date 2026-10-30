"""Read-only preservation and packaging. Never import or execute reviewed code."""
from pathlib import Path,PurePosixPath
import hashlib,json,re,stat,zipfile,datetime
BASE=Path('/workspace/scratch/ace5c9b2f18b');HERE=BASE/'cc-recovery-20261030';OLD=BASE/'cc-review'
INPUT=BASE/'upload/I164-control-callback-exception-correspondence-1(1).zip'
PIN={'bytes':124424355,'sha256':'ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20'}
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def read_stable(p):
 assert stat.S_ISREG(p.lstat().st_mode),p
 before=p.stat();b=p.read_bytes();after=p.stat()
 assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),p
 return b,after
inspection=json.loads((HERE/'PROCESS-INSPECTION.json').read_bytes());assert inspection['matching_validator_processes']==[] and inspection['exit_status'] is None
files={};inventory={}
for p in sorted(OLD.rglob('*')):
 if not p.is_file():continue
 b,s=read_stable(p);n=p.relative_to(OLD).as_posix();files['review-files/'+n]=b;inventory[n]={**ident(b),'mtime_ns':s.st_mtime_ns}
def obj(n):return json.loads(files['review-files/'+n])
def rows_stdout(name):
 stem='results/'+name+'/';rows=[json.loads(b) for b in files['review-files/'+stem+'progress.jsonl'].splitlines()];printed=[]
 for line in files['review-files/results/'+name+'.stdout'].decode().splitlines():
  m=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED)',line)
  if m:printed.append((int(m[1]),m[2],m[3]))
 assert printed==[(i,r['check'],r['result']) for i,r in enumerate(rows,1)],name
 return rows
groups={};total=0
for name,expected in [('primary',184),('recovered',158),('source',70),('coordinated',106),('fresh-semantic',2)]:
 stem='results/'+name+'/';v=obj(stem+'RESULT.json');rows=rows_stdout(name)
 assert v['result']=='PASS' and v['error'] is None and v['checks']==len(rows)==expected and rows==v['rows']
 groups[name]={'controls':expected,'outcomes':{k:sum(x['result']==k for x in rows) for k in ('PASS','REJECTED')},'result_identity':ident(files['review-files/'+stem+'RESULT.json']),'record_reconciliation':'PASS','environment':v['environment']};total+=expected
assert total==520
partial=rows_stdout('fresh-public');assert len(partial)==9
for n in ('RESULT.json','failure.txt','final-verification.json'):assert 'review-files/results/fresh-public/'+n not in files
cli=obj('results/fresh-public/CLI-result.json');assert cli['result']=='PASS' and cli['actual_admission'] is False
raw,_=read_stable(INPUT);assert ident(raw)==PIN;files['input/I164-control-callback-exception-correspondence-1.zip']=raw
with zipfile.ZipFile(INPUT) as z:
 manifest=json.loads(z.read('MANIFEST.json'))
 source_preservation={}
 for which in ('primary','recovered'):
  root=Path('/workspace/review-evidence/FL6-control-20261030')/which;source_preservation[which]={}
  for n in ('code/correspondence.py','code/managed_coverage.py','source-evidence/prospective_entry.py'):
   b,_=read_stable(root/n);assert ident(b)==manifest[n];source_preservation[which][n]=ident(b)
audit=obj('results/composition-and-supplied.json')
checkpoint={'checkpoint':'Formal-Lab6-I164-control-callback-exception-INCOMPLETE-recovery','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_author':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,
 'target':'I164-control-callback-exception-correspondence-1.zip','input':PIN,'input_entries':3069,'input_manifested_hashes':3068,'review_verdict':'INCOMPLETE — final public rejection unconfirmed; no closure verdict issued','closure_established':False,
 'process_inspection':inspection,'completed_independent_controls_preserved':total,'completed_groups':groups,'partial_public_logged_rows':9,'partial_public_rows_in_completed_total':False,'partial_public_log_reconciliation':'Nine progress rows match captured stdout exactly; no group RESULT exists','public_pristine_CLI_result':cli,
 'pending_check':{'ordinal_in_public_driver':10,'label':'public coordinated client-handler and cause invention','entry_point':'correspondence.validate(root, enc(q))','expected_result':'ValueError containing CONTROL-STALE-OR-ALTERED-RECEIPT','actual_result':'UNRECOVERED / UNCONFIRMED','mutation':'For both contexts, set control_exception_revocation_correspondence.exception_chain_observation to {existing_cause: null}, client_handler_applicable to true, and declaration.source.new_explicit_cause_assignment to true. Validate the changed serialized receipt.','mutation_source_identity':inventory['code/process_controls.py'],'mutated_receipt_saved':False,'mutated_receipt_origin':'In-memory value described by the preserved driver; no saved mutated input bytes recovered','also_unfinished':'End-of-public-group recovered-root verification and final RESULT/call-record write'},
 'exit_status':None,'termination_cause':'UNESTABLISHED; interrupted wait is not evidence of a particular process exit or signal','candidate_source_preservation_at_recovery':source_preservation,
 'supplied_results':{'primary':276,'recovered_root':64,'public_process':7,'log_reconciliation':'Previously inspected and preserved; not rerun','two_zero_control_failures':'PRESERVED','four_forensic_partials':'PRESERVED','historical_primary_discrepancy':[308,307,303],'historical_missing_progress_ordinal':304,'historical_missing_stdout_ordinals':[304,305,306,307,308],'historical_gap_cause':'UNESTABLISHED','historical_separate_recovered_public':[78,5]},
 'preserved_review_harness_failure':{'path':'review-files/failures/audit-membership-level','controls':0,'included_in_completed_total':False},
 'limitations':{'no_final_public_rejection_inferred_from_other_passes':True,'runtime_control_finally_removal_observations':'UNAVAILABLE','control_constructor_exception_continuation':'OUTSIDE SLICE','full_outer_cleanup':'UNEXPANDED','selected_owner_continuity':'CONDITIONAL','existing_cause_context_suppression':'UNKNOWN','physical_reference_identity':'UNESTABLISHED','observer':'Separate Client.state call remains UNJOINED','saved_traced_invocations':18},
 'boundaries':{'obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False,'backup':'KERNEL-ONLY','streams':'UNCOMPUTED'},
 'this_continuation':{'new_validator_processes':0,'duplicate_validator_launches':0,'completed_control_reruns':0,'Engineering_campaign_reruns':0,'candidate_code_changes':0,'runtime_or_session_operations':0,'database_connections':0,'acquisitions':0,'scope':'Bounded process/log inspection, record reconciliation and integrity-verified recovery packaging only'},
 'previous_integrity_records':{'primary':obj('results/integrity.json'),'recovered':obj('results/recovered-integrity.json')},'previous_composition_audit':audit}
(HERE/'CHECKPOINT.json').write_bytes(enc(checkpoint));(HERE/'SOURCE-INVENTORY.json').write_bytes(enc(inventory))
report='''INCOMPLETE INDEPENDENT REVIEW — RECOVERY CHECKPOINT

Target: I164-control-callback-exception-correspondence-1.zip
124,424,355 bytes; 3,069 entries; SHA-256 ed07f4ceb638f1c967cb3936b0051f5c0c8d781c95d26838b7bdc7baba7f4c20.
Construction: SU-Engineering[288D]. Independent review: Formal-Lab[6].

Verdict: INCOMPLETE. The final public rejection is unconfirmed. This is an integrity-verified recovery archive, not a completed acceptance or closure review.

Bounded recovery found no matching validator process in the available process table. Last known PID: 11584; tool session: 83132. The tool session lookup returned "Unknown process id 83132". No recoverable exit status, final public RESULT.json, failure.txt or end-of-group verification record exists. The underlying exit/signal/cause is UNESTABLISHED; no success or failure of the pending validation is inferred from absence of the process or from the interrupted wait.

The five finalized independent groups retain 520 passed controls: primary 184, recovered-root 158, source 70, paired substitutions 106 and fresh semantic validation two. Their saved RESULT, progress and stdout records reconcile exactly. This continuation inspected those records; it did not rerun their checks.

The unfinished public group has nine matching progress/stdout rows. They include acceptance of the exact pristine receipt, returned-result isolation checks and rejection of missing mandatory relations, a missing context and the legacy receipt. They remain partial evidence outside the 520 completed-group total. The actual pristine CLI result is preserved. No tenth row or final group result has been fabricated.

Exact outstanding check: "public coordinated client-handler and cause invention". In both contexts it changes control_exception_revocation_correspondence.exception_chain_observation to {"existing_cause": null}, client_handler_applicable to true, and declaration.source.new_explicit_cause_assignment to true, then invokes public validate(root, enc(q)). Expected rejection is CONTROL-STALE-OR-ALTERED-RECEIPT. Actual outcome is UNRECOVERED. The altered receipt existed in memory; no saved copy was recovered. Its exact generating driver is preserved. Final public recovered-root verification and RESULT/call-record writing were also unfinished or unrecorded.

No duplicate validator was launched and no further waiting was attempted after the process/session proved unavailable. The existing implementation and evidence were left unchanged. Both recovered roots' current producer, adapter and defining prospective_entry.py bytes were checked against the target manifest during packaging; no new claim about a complete current recovered-root revalidation is made.

Engineering's supplied 276/64/7 controls remain separate. Their previously inspected log reconciliation, both zero-control membership failures, four partial files and historical 308/307/303 discrepancy are retained. The missing historical progress row 304, stdout rows 304–308, separate 78/5 results and UNESTABLISHED cause remain qualified. The review's own zero-control membership-level audit failure also remains preserved and excluded from totals.

The original review draft, code, fixtures, completed results and partial public logs are preserved byte-for-byte under review-files/. The draft remains a draft. In particular, the prewritten supported-verdict packager was not executed and is not a verdict. CHECKPOINT.json and this report govern the recovery archive's INCOMPLETE status.

The earlier source analysis and completed controls remain available, but they cannot replace the unfinished public check. No new implementation defect was demonstrated by this bounded process recovery; closure is still unestablished. To finish later, first use any recoverable original result with exact provenance. If none exists, the missing evidence is one separately authorized execution of only the unfinished public rejection and its concluding verification, not a rerun of completed campaigns. This checkpoint itself does not launch or authorize that execution.

Runtime control/finally/removal observations remain unavailable; control-constructor exceptional continuation and full outer cleanup remain outside this slice. Selected-owner continuity is conditional; existing cause/context/suppression and physical reference identity remain qualified. The 18 saved traced invocations and separate frameless Client.state observer remain unjoined.

All eleven obligations, four inventory and fourteen lifetime UNKNOWN totals, Decision B, retention and allowances remain unchanged. SOURCE-ONLY; cumulative-envelope unadopted; backup kernel-only; streams UNCOMPUTED; readiness/final binding blocked; admission disabled. Saved test environment remains CPython 3.12.14 / Cryptography 50.0.2. No application, database, session, acquisition, policy or admission operation was performed.
'''
(HERE/'REPORT.txt').write_text(report)
(HERE/'START-HERE.txt').write_text('INCOMPLETE REVIEW. Read REPORT.txt and CHECKPOINT.json. The original target ZIP and unchanged review evidence are included. No final closure verdict exists. Do not run the preserved completed campaigns or the draft supported-verdict packager.\n')
(HERE/'RECOVERY.txt').write_text('Verify the outer recovery ZIP identity, CRC, safe exact membership and all MANIFEST.json hashes. The exact input under input/ retains the original implementation, dependencies, supplied failures and partials. review-files/ preserves the interrupted independent review. SOURCE-INVENTORY.json records its unchanged bytes. PROCESS-INSPECTION.json records the bounded process lookup and missing final result. No process is resumed or duplicated by this checkpoint. Preserve the nine partial public rows outside completed totals. Any later result must be tied to the exact input, driver and pending mutation; absence of a process is not a successful exit.\n')
for p in sorted(HERE.iterdir()):
 if p.is_file():files[p.name]=p.read_bytes()
for n,b in files.items():
 q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and '\\' not in n and ':' not in n and q.as_posix()==n
files['MANIFEST.json']=enc({n:ident(b) for n,b in sorted(files.items())})
target=BASE/'Formal-Lab6-I164-control-callback-exception-INCOMPLETE-recovery.zip';assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(files.items()):
  i=zipfile.ZipInfo(n,(2026,10,30,0,0,0));i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,b)
# Verify the new recovery artifact, without re-executing any review checks.
with zipfile.ZipFile(target) as z:
 assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names))==len(files) and set(names)==set(files)
 mf=json.loads(z.read('MANIFEST.json'));assert set(names)==set(mf)|{'MANIFEST.json'}
 for i in z.infolist():
  n=i.filename;q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and '\\' not in n and ':' not in n and q.as_posix()==n and stat.S_ISREG(i.external_attr>>16)
  if n!='MANIFEST.json':assert ident(z.read(n))==mf[n],n
 assert ident(z.read('input/I164-control-callback-exception-correspondence-1.zip'))==PIN
for n,record in inventory.items():
 b,_=read_stable(OLD/n);assert ident(b)=={k:record[k] for k in ('bytes','sha256')},n
record={'archive':str(target),'identity':ident(target.read_bytes()),'entries':len(files),'manifested_hashes':len(files)-1,'CRC':'PASS','safe_exact_membership':'PASS','all_manifested_hashes':'PASS','embedded_input_identity':'PASS','original_review_files_unchanged':len(inventory),'review_status':'INCOMPLETE','completed_controls_preserved':520,'partial_public_rows':9,'pending_result':'UNRECOVERED','exit_status':None}
(BASE/'cc-recovery-package.json').write_bytes(enc(record));print(json.dumps(record,indent=2))
