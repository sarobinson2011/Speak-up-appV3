"""Package completed independent evidence; no control or candidate execution."""
from bytes_only import B,read,save,fid,ident,safe
from pathlib import Path
import zipfile,json,stat
items={
 'host_evidence':('I164-enter-return-res-public-1-host-evidence.tar.gz','libfile_fde3_f-03a0d02143108191878e4941143297bd_39c64cf85e608191bb9545db7327fd84',10112583,'bcd694478e38d06777112a45b6d2ea1e20f251bddf35de30cd634c4c47ca7155'),
 'retained_enter_review':('I164-enter-call-attempt-1-independent-review.zip','libfile_fde3_f-eeeeeda6c1c48191bede2f043aa4cb96_39c64cf85e608191bb9545db7327fd84',8272994,'381bc024997b4c7c136dbb1c656a5dd3ababcb4fefa40dcc04d055334a261995'),
 'byte_recovery_dependency':('I164-helper-open-persistent-host-launcher-review-2.zip','libfile_fde3_f-f9fd72efc654819194987af266042001_39c64cf85e608191bb9545db7327fd84',204417990,'b0a8a98f2485699ae484432daa4afcf3c5c442bc45241338973a90499242c07c')}
inputs={}
for role,(name,library_id,size,sha) in items.items():
 pin={'bytes':size,'sha256':sha};assert fid(B/'inputs'/name)==pin
 inputs[role]={'filename':name,'library_file_id':library_id,'link':'https://chatgpt.com/library?file_id='+library_id+'&account_id=personal',**pin,'retrieved_directly_and_verified':True,'included_in_this_review':role=='host_evidence'}
inputs['receiving_chat_instruction']='Retrieve omitted saved artifacts directly. Verify exact bytes/hashes, reuse verified copies and completed results. Do not ask Steve to re-upload or hunt through Downloads. A handoff authorizes no validation replay.'
save(B/'INPUTS.json',inputs)
save(B/'FAILURES.json',{'new_candidate_defects_demonstrated':[],'fresh_control_failures':0,'fresh_control_timeouts':0,'fresh_control_retry':False,'byte_or_record_audit_failures':0,'incidental_read_only_probe':{'file':'host/ACCOUNTING.json','observation':'cat reported missing file; not a required current input and not manifested. Required documents were read. No candidate invocation or control count.'},'retained_failures':'Exact prior review reference/review/FAILURES.json and its Library archive retain DOC-ENTER-01 audit failure, empty stderr-directory audit failure, reported EVENT-prefix parser failure and all earlier qualifications. No missing records reconstructed.'})
host=read(B/'host-record-audit.json');fresh=read(B/'independent-reconciliation.json');source=read(B/'source-recovery-audit.json');archives=read(B/'nested-archive-audit.json');ha=read(B/'host-archive-audit.json')
checkpoint={
 'review':'I164-ENTER-RETURN-RES-1','reviewer':'Formal-Lab[6], author-independent reviewer of fixed Engineering source; reviewer code/report only',
 'verdict':'SUPPORTED within the bounded conditional SOURCE-ONLY completed-C-return and res-assignment correspondence contract; no candidate defect demonstrated',
 'input':inputs['host_evidence'],'integrity':{k:ha[k] for k in ('identity','entries','manifested_hashes','preparation_pins','gzip_integrity','safe_exact_membership')},
 'nested_archives':{k:{x:v[x] for x in ('identity','entries','manifested_hashes','CRC','safe_exact_membership')} for k,v in archives.items()},
 'implementation':source,'final_root':read(B/'final-root-audit.json'),
 'independent':{'rows':253,'PASS':159,'REJECTED':94,'FAIL':0,'one_fresh_process':True,'exit':0,'timed_out':False,'reconciliation':'independent-reconciliation.json','public_runs':0,'authenticated_constructed_runs':0},
 'supplied_focused':{'rows':723,'PASS':197,'REJECTED':526,'exit':0,'chunks':766,'replayed':False,'reconciliation':'focused-record-audit.json'},
 'saved_host':{'public_positive':1,'actual_basis_capture':1,'receipt':host['receipt'],'receipt_bytes_equal':True,'event_records':276,'snapshots':220,'stdout_chunks':275,'new_root_public_validate_calls':1,'thin_enter_lookup_R1_helper_validate_calls':0,'total_validate_entries_in_deeper_chain':sum(host['public_calls'].values()),'last_computation':host['last_computation'],'computation_events_are_controls':False,'child_exit':host['child_exit'],'reconciliation':'host-record-audit.json','fresh_replays':0},
 'full_public_negative_derivations':0,'authenticated_constructed_path':'mandatory static wiring; execution remains UNTESTED',
 'precise_model_limits':['C NULL is a completed C return and can be assigned to res; it is not absent return','Python None is a non-NULL object-case premise','concrete_value None means unobserved; not a C pointer or observed Python value','terminal True on normal model progression concerns original pending outer error, not helper C error indicator','termination/unobserved terminal None; prior established return retained when assignment unestablished','helper error indicator and deeper guarantees UNKNOWN','stop before Py_DECREF(enter):2516'],
 'execution_environment':fresh['environment'],'historical_qualifications':['DOC-ENTER-01 preserved; current five-function declaration agrees','R1 five-versus-six discrepancy remains separate','False/None fixture qualification','prior audit failures, reported parser failure, incomplete/missing records and UNKNOWN attempts','cooperative monitoring, cleanup interruption, termination and hostile replacement limits','50.0.0 versus retained historical host 50.0.2; no equivalence'],
 'authority':{'both_acquisitions':'PRESERVED','obligations':11,'inventory_unknown_totals':4,'lifetime_unknown_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False},
 'implementation_changes':0,'runtime_helper_acquisition_database_session_git_operations':0,'recovery':'RECOVERY.txt and recorded recover_and_audit.py; byte-only','failures':'FAILURES.json'
}
save(B/'CHECKPOINT.json',checkpoint)
files={p.name:p for p in B.iterdir() if p.is_file() and p.name!='package-identity.json'}
for p in (B/'independent').rglob('*'):
 if p.is_file():files[p.relative_to(B).as_posix()]=p
name=items['host_evidence'][0];files['inputs/'+name]=B/'inputs'/name
for n in ('code/managed_coverage.py','code/correspondence.py','CHANGES.json','SEMANTICS.txt','source-evidence/lab_bootstrap.py','reference/cpython-3.12.14/bytecodes.c','reference/cpython-3.12.14/typeobject.c'):
 files['inspected/'+n]=B/'source'/n
for p in (B/'source/reference/review').iterdir():files['reused-enter-review/'+p.name]=p
for n in ('recovery-launch.json','recovery-exit.json','recovery.stdout','recovery.stderr','recovery-verification.json','recovered-helper/byte-origins.json','recovered-helper/recovery-result.json'):
 files['byte-recovery/'+n]=B/'parent-recovered'/n
manifest={safe(n):fid(p) for n,p in sorted(files.items())};dest=B.parent/'I164-enter-return-res-1-independent-review.zip'
with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.writestr('MANIFEST.json',json.dumps(manifest,indent=2,sort_keys=True)+'\n')
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(manifest)|{'MANIFEST.json'}
 for i in z.infolist():assert safe(i.filename) and not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG)
 for n,pin in manifest.items():assert ident(z.read(n))==pin
identity={'filename':dest.name,'path':str(dest),'entries':len(manifest)+1,'manifested_hashes':len(manifest),**fid(dest),'CRC':'PASS','safe_exact_membership':'PASS','all_manifested_hashes':'PASS'}
save(B/'package-identity.json',identity);print(json.dumps(identity,indent=2))
