"""Package already-completed independent evidence. No candidate execution."""
from review_bytes import HERE as B,read,save,fid,ident,safe
from pathlib import Path
import json,zipfile,stat
ids={
 'host':('I164-enter-call-attempt-public-1-host-evidence.tar.gz','libfile_fde3_f-8045c5eee1488191bcbcf2ac9d65183f_39c64cf85e608191bb9545db7327fd84',7692623,'fb367b2210875601b83c2629abae36ce7ee3fb8a54b34f40a89af0f58d5a6c51'),
 'byte_recovery_dependency':('I164-helper-open-persistent-host-launcher-review-2.zip','libfile_fde3_f-f9fd72efc654819194987af266042001_39c64cf85e608191bb9545db7327fd84',204417990,'b0a8a98f2485699ae484432daa4afcf3c5c442bc45241338973a90499242c07c'),
 'reused_lookup_review':('I164-context-special-lookup-1-independent-review.zip','libfile_fde3_f-dab1323a294c819180bea0f62fe25851_39c64cf85e608191bb9545db7327fd84',6633907,'aa52620a54fb0511abe00020d5f92c44445601e90010f198519db9dd93ae8f24')}
inputs={}
for role,(filename,library_id,size,sha) in ids.items():
 pin={'bytes':size,'sha256':sha};assert fid(B/'inputs'/filename)==pin
 inputs[role]={'filename':filename,'library_file_id':library_id,'link':'https://chatgpt.com/library?file_id='+library_id+'&account_id=personal',**pin,'retrieved_directly_and_verified':True,'included_in_review':role=='host'}
inputs['instructions']='Receiving chat retrieves omitted dependencies directly, verifies identity, reuses completed results. A handoff is not permission to replay checks; do not ask Steve to hunt for or upload already saved files.'
save(B/'INPUTS.json',inputs)
failures=[
 {'kind':'documentation finding and reviewer audit exit 1','record':'recovery-audit.exit.json','raw':['recover_candidate.py','recovery-audit.stdout','recovery-audit.stderr'],'qualification':'byte recovery succeeded; root checks completed before six-versus-five assertion; continuation did not replay recovery','resolution':'finish-byte-audit.exit.json; final-root-audit.json','candidate_control_count':0},
 {'kind':'reviewer file-layout audit exit 1','record':'record-audit.exit.json','raw':['reconcile_saved.py','record-audit.stdout','record-audit.stderr'],'qualification':'missing empty stderr-chunks directory; 489-row supplied audit already saved; no candidate invocation','resolution':'record-audit-continuation.exit.json','candidate_control_count':0},
 {'kind':'historical reported read-only EVENT-prefix parser failure','record':'reported-parser-failure-evidence.json','qualification':'reported; no raw failed-parser records recovered; not rerun or reconstructed','candidate_control_count':0},
 {'kind':'incidental read-only filename probe','qualification':'rg requested event_filter.c instead of _event_filter.c, exit 2; exact existing _event_filter.c subsequently inspected; no validation or source change','candidate_control_count':0}]
save(B/'FAILURES.json',failures)
source=read(B/'source-byte-audit.json');host=read(B/'host-record-audit.json');fresh=read(B/'independent-reconciliation.json');archives=read(B/'archive-audit.json')
checkpoint={
 'review':'I164-ENTER-CALL-ATTEMPT-1','reviewer':'Formal-Lab[6] author-independent; reviewer code/report only','verdict':'SUPPORTED within the bounded conditional SOURCE-ONLY enter-call-attempt correspondence contract; no candidate semantic defect demonstrated',
 'documentation_finding':'DOC-ENTER-01: CHANGES says six appended producer functions; exact appended bytes define five. Nonblocking; distinct from inherited R1 discrepancy.',
 'input':inputs['host'],'archive_checks':{k:{x:v[x] for x in ('identity','entries','manifested_hashes')} for k,v in archives.items()},
 'recovered_root':read(B/'final-root-audit.json'),'implementation':source,
 'independent_controls':{'rows':147,'PASS':64,'REJECTED':83,'FAIL':0,'exit':0,'timed_out':False,'reconciliation':'independent-reconciliation.json','fresh_process':True,'public_calls':0,'authenticated_basis_core_calls':0},
 'supplied_controls':{'rows':489,'PASS':101,'REJECTED':388,'exit':0,'replayed':False,'reconciliation':'focused-record-audit.json'},
 'saved_host':{'public_positives':1,'actual_basis_captures':1,'new_root_public_calls':1,'thin_lookup_R1_helper_validate_calls':0,'total_deeper_chain_validate_entries':26,'event_records':272,'progress_snapshots':216,'computation_entries':17812,'computation_returns':17812,'events_add_control_counts':False,'receipt':host['receipt'],'child_exit':host['child_exit'],'reconciliation':'host-record-audit.json','reviewer_reruns':0},
 'full_public_negative_derivations':0,'mandatory_constructed_path':'wired; authenticated execution UNEXECUTED','fresh_execution_environment':fresh['environment'],
 'retained_qualifications':['cooperative monitoring; free slot/hook removal not complete cleanup','historical UNKNOWN/missing records remain','R1 five-versus-six documentation and False/None fixture distinction','50.0.0 versus historical host 50.0.2; no equivalence','runtime arrival and physical effects unavailable','constructed fixtures not runtime observations','separate observer unjoined'],
 'limits':{'acquisitions':'both preserved; distinct identities','obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False},
 'stop':'selected _PyObject_CallNoArgs(enter) attempt; before helper dispatch/body, call outcome, res assignment, completed context entry or f binding',
 'recovery':'RECOVERY.txt and recover_for_inspection.py; byte-only, new destination, no replay','failure_records':'FAILURES.json','candidate_changes':0,'application_database_session_acquisition_git_actions':0
}
save(B/'CHECKPOINT.json',checkpoint)
# Include original main input for exact raw recovery; omit 204MB byte-recovery dependency.
# Reviewer scripts/failures are preserved as executed, including their original assumptions.
files={p.name:p for p in B.iterdir() if p.is_file() and p.suffix!='.zip' and p.name!='package-identity.json'}
for p in (B/'independent').rglob('*'):
 if p.is_file():files[p.relative_to(B).as_posix()]=p
files['inputs/'+ids['host'][0]]=B/'inputs'/ids['host'][0]
# Convenient source copies: byte-identical, never used as substitute authentication.
for p in [B/'source/code/managed_coverage.py',B/'source/code/correspondence.py',B/'source/CHANGES.json',B/'source/source-evidence/lab_bootstrap.py',B/'source/reference/cpython-3.12.14/bytecodes.c',B/'source/reference/cpython-3.12.14/typeobject.c',B/'source/reference/cpython-3.12.14/compound_stmts.rst']:
 files['inspected/'+p.relative_to(B/'source').as_posix()]=p
for p in (B/'source/reference/review').iterdir():files['reused-lookup-review/'+p.name]=p
manifest={safe(n):fid(p) for n,p in sorted(files.items())}
name='I164-enter-call-attempt-1-independent-review.zip';dest=B.parent/name
with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.writestr('MANIFEST.json',json.dumps(manifest,sort_keys=True,indent=2)+'\n')
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(manifest)|{'MANIFEST.json'}
 for x in z.infolist():assert safe(x.filename) and not x.is_dir() and stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG)
 for n,pin in manifest.items():assert ident(z.read(n))==pin
result={'filename':name,'path':str(dest),'entries':len(manifest)+1,'manifested_hashes':len(manifest),**fid(dest),'CRC':'PASS','safe_exact_membership':'PASS','all_manifested_hashes':'PASS'}
save(B/'package-identity.json',result);print(json.dumps(result,indent=2))
