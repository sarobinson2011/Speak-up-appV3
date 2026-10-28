import ast,hashlib,io,json,os,runpy,stat,zipfile
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'outside-catch-correction';T=B/'outside-catch-tools'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):(R/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
primary=json.loads((R/'results/primary/RESULT.json').read_bytes());recovered=json.loads((T/'recovered-output/RESULT.json').read_bytes())
assert primary['result']==recovered['result']=='PASS' and primary['checks']==131 and recovered['checks']==129
for mode in ['fresh','recovered']:
 p=json.loads((T/(mode+'.process.json')).read_bytes());assert p['exit']==0 and not (T/(mode+'.stderr')).read_bytes()
 for suffix in ['stdout','stderr','process.json']:(R/'results'/(mode+'.'+suffix)).write_bytes((T/(mode+'.'+suffix)).read_bytes())
out=R/'results/recovered';out.mkdir()
for p in (T/'recovered-output').iterdir():assert p.is_file();(out/p.name).write_bytes(p.read_bytes())
(R/'results/recovery-gate.json').write_bytes((T/'recovery-gate.json').read_bytes())
fresh=json.loads((T/'fresh.stdout').read_bytes());assert fresh['result']=='PASS' and fresh['actual_admission'] is False
write('RESULTS.json',{
 'new_correction':{'primary':{'assertions':131,'result':'PASS','seconds':primary['seconds']},'recovered':{'assertions':129,'result':'PASS','seconds':recovered['seconds']},'fresh_process':{'checks':1,'result':'PASS','exit':0},'new_independent_review':False},
 'new_failed_attempts_excluded_from_completed_totals':[{'path':'failures/primary-fixture-selector','completed_before_failure':81,'error':'StopIteration in fixture selection'},{'path':'failures/primary-normal-comparison','completed_before_failure':103,'error':'Compared deliberate historical output mutation as if pristine'}],
 'reused_Formal_Lab6_forwarding_review':{'primary_assertions':217,'recovered_root_assertions':149,'separate_CLI_checks':1,'additional_caveat_cases_excluded':6,'failed_recovery_assertions':0,'scoped_support':True,'classification_caveat_preserved':True,'rerun':False},
 'prior_supplied_forwarding_results':{'corrected_focused_controls':17,'recovered_controls':168,'process_checks':1,'precorrection_controls_separate':170,'rerun':False},
 'new_control_environment':'CPython 3.12.14; Cryptography 50.0.2; -I -B; no optimization',
 'constructed_not_runtime':True,'requests':0,'new_signatures':0,'database_connections':0,'session_operations':0,'acquisitions':0,'runtime_changes':0,'Git_saves':0,'completed_campaigns_rerun':False,
 'all_eleven_obligations_preserved':True,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':'DISABLED'})
reviewpath=B/'upload/Formal-Lab6-I164-client-handle-return-correspondence-independent-review(1).zip'
review=zipfile.ZipFile(reviewpath);original=zipfile.ZipFile(io.BytesIO(review.read('input/I164-client-handle-return-correspondence-1.zip')))
report={}
for folder,z in [('original',original),('review',review)]:
 names=[n for n in z.namelist() if not (folder=='review' and n.startswith('input/'))]
 actual={p.relative_to(R/folder).as_posix() for p in (R/folder).rglob('*') if p.is_file()}
 assert actual==set(names)
 for n in names:assert (R/folder/n).read_bytes()==z.read(n),folder+'/'+n
 report[folder]={'files':len(names),'exact_bytes_membership':'PASS'}
recovery=json.loads((B/'outside-catch-recovered/MANIFEST.json').read_bytes())
for n,p in recovery.items():assert ident((R/n).read_bytes())==p,n
report['recovered_core']={'files':len(recovery),'all_final_input_bytes_match':'PASS'}
report['runtime_source_changes']=0
write('results/final-core-preservation.json',report)
changes=json.loads((R/'CHANGED-IDENTITIES.json').read_bytes())
for n,v in changes.items():
 if n.startswith('code/'):assert ident((R/n).read_bytes())==v['current']
for n,v in changes['new_support_files'].items():assert ident((R/n).read_bytes())==v
write('CHECKPOINT.json',{'name':'I164-outside-catch-classification-correction-1','author':'SU-Engineering[288D]','scope':'Terminal conditional outcome/catch-location clarification; no runtime behavior change','current_receipt':ident((R/'results/client-handle-correspondence.json').read_bytes()),'current_code':{n:v['current'] for n,v in changes.items() if n.startswith('code/')},'semantic_contract':'I164-CLIENT-TERMINAL-CLASSIFICATION-1','review_status':'READY_FOR_INDEPENDENT_REVIEW; no closure claimed','preserved_inputs':json.loads((R/'provenance/input-verification.json').read_bytes()),'retained_runtime_observation_gap':True,'all_obligations_and_blockers_preserved':True})
write('DEPENDENCIES.json',{'reviewed_forwarding_checkpoint':{'name':'I164-client-handle-return-correspondence-1.zip','identity':ident((B/'I164-client-handle-return-correspondence-1.zip').read_bytes()),'decoded_root':'original/','all_1282_members_retained':True,'archive_retained_separately':True},'independent_review':{'name':reviewpath.name,'identity':ident(reviewpath.read_bytes()),'decoded_non_input_members':'review/','all_171_non_input_members_retained':True,'only_redundant_embedded_input_zip_omitted':True,'archive_retained_separately':True},'executable_predecessor':'original/retained/handle','earlier_archival_availability':'Preserve original/RECOVERY.md and original/retained/handle/DEPENDENCIES.json qualifications; omitted historical forensic archives are not claimed newly present.','recovery_input':json.loads((R/'results/recovery-input.json').read_bytes()),'no_deletion_or_compaction_permission':True})
for n in ['finalize.py']:(R/'provenance/orchestration'/n).write_bytes((T/n).read_bytes())
api=runpy.run_path(str(R/'tools/checkpoint.py'),run_name='_archive')
files=api['inventory'](R)
dirs={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_dir()}
expected={p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'}
assert dirs==expected
target=B/'I164-outside-catch-classification-correction-1.zip'
identity=api['pack'](files,target)
(T/'final-archive-identity.json').write_bytes(api['enc'](identity));print(json.dumps(identity),flush=True)
