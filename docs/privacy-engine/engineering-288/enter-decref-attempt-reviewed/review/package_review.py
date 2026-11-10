"""Package completed evidence only. No validation or control execution."""
from bytes_only import *
import shutil,zipfile,datetime,collections
review=B/'REVIEW.txt';review.write_text(review.read_text().replace('55.856seconds supervisor time','55.777711seconds supervisor time'))
inputs={
 'primary_host':('I164-enter-decref-attempt-public-1-host-evidence.tar.gz','libfile_fde3_f-0af3218ebfec8191a9f05d9435017df6_39c64cf85e608191bb9545db7327fd84',B/'inputs/I164-enter-decref-attempt-public-1-host-evidence.tar.gz',648,646,True),
 'fixed_source':('I164-enter-decref-attempt-1-source.zip','libfile_fde3_f-9689a6522478819194aca21a5e97b90b_39c64cf85e608191bb9545db7327fd84',B/'host/inputs/I164-enter-decref-attempt-1-source.zip',49,48,False),
 'supplied_results':('I164-enter-decref-attempt-1-results.zip','libfile_fde3_f-f8f8b8f2fd74819199e87cb156b17c81_39c64cf85e608191bb9545db7327fd84',B/'host/inputs/I164-enter-decref-attempt-1-results.zip',2341,2340,False),
 'byte_recovery_dependency':('I164-helper-open-persistent-host-launcher-review-2.zip','libfile_fde3_f-f9fd72efc654819194987af266042001_39c64cf85e608191bb9545db7327fd84',B/'inputs/I164-helper-open-persistent-host-launcher-review-2.zip',60,59,False),
 'reused_prior_review':('I164-enter-return-res-1-independent-review.zip','libfile_fde3_f-d53a35fcea408191a502c425650114a1_39c64cf85e608191bb9545db7327fd84',B/'inputs/I164-enter-return-res-1-independent-review.zip',326,325,False)
}
meta={}
for role,(name,lid,p,entries,hashes,included) in inputs.items():
 meta[role]={'filename':name,'library_file_id':lid,'link':'https://chatgpt.com/library?file_id='+lid+'&account_id=personal',**fid(p),'entries':entries,'manifested_hashes':hashes,'retrieved_and_verified':role not in ('fixed_source','supplied_results'),'embedded_bytes_verified_and_used':role in ('fixed_source','supplied_results'),'included_in_checkpoint':included,'inside_primary_host':role in ('fixed_source','supplied_results')}
save(B/'INPUTS.json',{'artifacts':meta,'handoff_instruction':'Retrieve these saved artifacts directly using Library IDs/links. Steve should not download/re-upload. Reuse exact embedded source/results bytes. No completed run is authorized by recovery or transfer.'})
save(B/'FAILURES.json',{'new_candidate_defect':None,'smallest_witness':None,'fresh_failed_controls':0,'fresh_failed_processes':0,'fresh_timeouts':0,'byte_recovery_failed':False,'raw_record_audit_failed':False,'primary_alias_limit':'Copied output mutants did not prove actual returned-object isolation; separate eight-row direct alias supplement supplies that evidence without relabelling primary rows.','noncontributing_recovery_assertion':'Executed recover_bytes.py contains one conditional-True assertion; no verification credit. final_audit.py independently checks actual prior receipt bytes, recorded in predecessor-exact-byte-reuse.json.','historical_failures':'All retained source/history and prior-review findings preserved; missing/UNKNOWN remains missing/UNKNOWN. No repair/reconstruction/replay.','original_evidence_unchanged':True})
ind=read(B/'independent-reconciliation.json');host=read(B/'host-record-audit.json');src=read(B/'source-recovery-audit.json')
save(B/'CHECKPOINT.json',{'target':'I164-ENTER-DECREF-ATTEMPT-1','reviewer':'Formal-Lab[6] separate independent reviewer','review_date':'2026-11-10','verdict':'SUPPORTED within the bounded conditional SOURCE-ONLY correspondence contract','candidate_defect_demonstrated':False,'smallest_witness':None,'evidence':{'inputs':meta,'recovered_root':src['ASSEMBLED'],'producer':src['producer'],'adapter':src['adapter'],'prefix':src['unchanged_prefix'],'new_functions':src['new_functions'],'saved_receipt':host['receipt']},'accounting':{'Engineering':{'rows':750,'PASS':213,'REJECTED':537,'exit':0,'replayed':False},'saved_public':{'positives':1,'actual_basis_captures':1,'events':276,'stdout_rows':276,'stdout_chunks':275,'progress_snapshots':220,'final_computation_entries':17827,'final_computation_returns':17827,'child_exit':0,'wrapper_exit':0,'manager_exit':0,'timeout':False,'retry':False,'computation_credit':0},'fresh_primary':{'rows':184,'PASS':90,'REJECTED':94,'exit':0},'fresh_direct_alias_supplement':{'rows':8,'PASS':6,'REJECTED':2,'exit':0},'fresh_only_total':ind['combined_fresh_only'],'historical_groups':'separate and unchanged; no unqualified cross-group aggregate'},'reused_prior_support':meta['reused_prior_review'],'precise_layers':'See REVIEW.txt, individual records and independent-reconciliation.json; pure source/model, pre-derivation shape, static wiring and offline assembly are not authentication','constructed_authenticated_path':'UNTESTED','full_public_negative_derivations':0,'fresh_public_runs':0,'candidate_changes':0,'runtime_application_helper_executions':0,'session_database_operations':0,'acquisitions':0,'Git_operations':0,'confirmed_save_reused':'14e75952ce19cf518e8b6c7d3f5e6307c09db2bd','environment':ind['environment'],'retained_historical_host_cryptography':'50.0.2; no equivalence to current50.0.0','failure_and_qualification_record':'FAILURES.json; REVIEW.txt; unchanged original histories','both_acquisitions_preserved':True,'obligations':11,'UNKNOWN_totals':{'inventory':4,'lifetime':14},'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':True,'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False})
# Selected byte copies are for immediate read-only inspection; exact full root is recoverable.
inspect=B/'inspected'
for rel in ['code/managed_coverage.py','code/correspondence.py','source-evidence/lab_bootstrap.py','reference/cpython-3.12.14/bytecodes.c','reference/cpython-3.12.14/typeobject.c','reference/cpython-3.12.14/compound_stmts.rst','CHANGES.json','SEMANTICS.txt','DEPENDENCIES.json','provenance/component-pins.json']:
 p=inspect/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(B/'candidate'/rel,p)
prior=B/'retained-prior-findings';prior.mkdir()
for n in ['REVIEW.txt','CHECKPOINT.json','FAILURES.json','RECOVERY.txt','INPUTS.json','host-record-audit.json','focused-record-audit.json','independent-reconciliation.json']:
 shutil.copyfile(B/'prior-review'/n,prior/n)
# Package only compact evidence, never the large recovered candidate or launcher.
files={}
for p in B.iterdir():
 if p.is_file() and p.suffix in ('.py','.json','.txt','.stdout','.stderr') and p.name!='package-identity.json':files[p.name]=p
for directory in ['independent','direct-alias','inspected','retained-prior-findings']:
 for p in (B/directory).rglob('*'):
  if p.is_file():files[p.relative_to(B).as_posix()]=p
files['inputs/I164-enter-decref-attempt-public-1-host-evidence.tar.gz']=B/'inputs/I164-enter-decref-attempt-public-1-host-evidence.tar.gz'
for n in ('byte-origins.json','recovery-result.json'):files['byte-recovery/'+n]=B/'recovered-helper'/n
manifest={n:fid(p) for n,p in files.items()};mb=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();dest=B/'I164-enter-decref-attempt-1-independent-review.zip'
with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):safe(n);z.write(p,n)
 z.writestr('MANIFEST.json',mb)
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(files)|{'MANIFEST.json'}
 for n,pin in manifest.items():assert ident(z.read(n))==pin,n
save(B/'package-identity.json',{'filename':dest.name,**fid(dest),'entries':len(files)+1,'manifested_hashes':len(files),'CRC':'PASS','safe_exact_membership':'PASS','all_hashes':'PASS'});print(read(B/'package-identity.json'),flush=True)
