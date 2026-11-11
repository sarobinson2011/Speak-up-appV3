from bytes_only import *
import datetime
out=B/'I164-decref-fast-completion-1-independent-review.zip'
assert not out.exists()
ind=read(B/'independent-reconciliation.json');host=read(B/'host-record-audit.json');author=read(B/'focused-record-audit.json')
assert read(B/'final-audit.exit.json')['exit']==0
checkpoint={'identity':'I164-DECREF-FAST-COMPLETION-1-INDEPENDENT-REVIEW','reviewer':'Formal-Lab[6] / Codex, independent of Engineering construction','verdict':'SUPPORTED within bounded conditional SOURCE-ONLY fast-completion contract','candidate_defect_demonstrated':False,'smallest_defect_witness':None,'source_revision':'2abcf904b8dac8c999d2b3aac76681abb333798a','recovered_root':read(B/'final-root-audit.json'),'producer':read(B/'source-recovery-audit.json')['producer'],'adapter':read(B/'source-recovery-audit.json')['adapter'],'predecessor_prefix_bytes':464085,'appended_functions':8,'independent':{'completed':151,'PASS':81,'REJECTED':70,'exit':0,'prior_failed_attempt':'one failed source row, zero successful/candidate-model controls, exit1; preserved separately'},'Engineering':{'completed':399,'PASS':196,'REJECTED':203,'exit':0,'replayed':False},'saved_public':{'positives':1,'actual_basis_captures':1,'receipt':host['receipt'],'receipt_bytes_equal_both_contexts':True,'child_exit':0,'child_finished_utc':host['child_exit']['finished_utc'],'child_seconds':host['child_exit']['seconds'],'wrapper_exit':0,'manager':'success/exited/0','event_records':276,'stdout_chunks':275,'progress_snapshots':220,'selected_function_entries_returns':17836,'computation_events_are_controls':False},'fresh_public_runs':0,'full_public_negative_derivations':0,'authenticated_constructed_path':'UNTESTED','runtime_effects':'UNESTABLISHED','qualified_binary_correspondence':'UNESTABLISHED','zero_count_destructor_completion':'UNRESOLVED','stop':'before bytecodes.c:2517','historical_groups':'184 primary, eight direct-alias supplement, 750 Engineering and prior public positive stay separate; all historical qualifications retained','environment':ind['environment'],'prior_50_0_2_host':'distinct from current50.0.0; no equivalence/qualification claim','both_acquisitions':'PRESERVED','obligations':11,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':True,'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False,'confirmed_save_reused_without_Git_operation':'f6fc8753701f8f2b8e75c8be646228d36a5e178d'}
save(B/'CHECKPOINT.json',checkpoint)
files={}
def add(p,n=None):
 p=Path(p);n=n or p.relative_to(B).as_posix();safe(n);assert n not in files;files[n]=p.read_bytes()
for n in ('REVIEW.txt','RECOVERY.txt','INPUTS.json','FAILURES.json','CHECKPOINT.json'):add(B/n)
for p in sorted(B.glob('*.py')):add(p,'reviewer/'+p.name)
for p in sorted(B.glob('*.json')):
 if p.name not in files:add(p,'audits/'+p.name)
for directory in ('independent','independent-completion'):
 for p in sorted((B/directory).rglob('*')):
  if p.is_file():add(p)
for pat in ('independent*.stdout','independent*.stderr','byte-recovery.stdout','byte-recovery.stderr'):
 for p in sorted(B.glob(pat)):add(p,'streams/'+p.name)
for k in ('source','results'):
 n=read(B/'host/INPUTS.json')[k]['filename'];add(B/'host/inputs'/n,'inputs/'+n)
for p in sorted((B/'host/validation/results').glob('*.json')):
 # Preserve basis provenance, all progress snapshots and root/result records;
 # the large actual receipt is pinned and remains in the exact primary input.
 if p.name!='actual-derived-receipt.json':add(p,'saved-host/results/'+p.name)
for n in ('events.jsonl',):add(B/'host/validation/results'/n,'saved-host/results/'+n)
for n in ('exit.json','capture.json','process.json','launch.json','stdout.log','stderr.log','chunk-index.jsonl','computation-phases.jsonl'):add(B/'host/validation/process'/n,'saved-host/process/'+n)
for n in ('PLAN.json','INPUTS.json','FAILURES.json','PREPARED.json','ONE-ATTEMPT-RESERVATION.json','LAUNCH-RECEIPT.json','service-exit.json','manager-exit.json','service-runtime-profile.json','AUTHENTICATION-PATH.txt','RECOVERY.txt','MANIFEST.json'):
 add(B/'host'/n,'saved-host/'+n)
for n in ('public_positive.py','host_prepare_launch.py'):add(B/'host/code'/n,'saved-host/code/'+n)
add(B/'host/observer-reference/native_observer.py','saved-host/observer-reference/native_observer.py')
for p in sorted((B/'host/expected').glob('*ROOT-MANIFEST.json')):add(p,'recovery-pins/'+p.name)
for p in sorted((B/'prior-review').glob('*')):
 if p.name in ('REVIEW.txt','CHECKPOINT.json','FAILURES.json','RECOVERY.txt','independent-reconciliation.json','INPUTS.json'):add(p,'prior-review/'+p.name)
manifest={n:ident(v) for n,v in files.items()};files['MANIFEST.json']=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,v in sorted(files.items()):
  i=zipfile.ZipInfo(n,(2026,11,11,10,30,0));i.compress_type=zipfile.ZIP_DEFLATED;i.create_system=3;i.external_attr=(stat.S_IFREG|0o600)<<16;z.writestr(i,v)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(files) and len(z.namelist())==len(files)
 for n,pin in manifest.items():assert ident(z.read(n))==pin
info={'filename':out.name,**fid(out),'entries':len(files),'manifested_hashes':len(manifest),'CRC_safe_exact_membership_hashes':'PASS'}
save(B/'delivery-identity.json',info);print(json.dumps(info),flush=True)
