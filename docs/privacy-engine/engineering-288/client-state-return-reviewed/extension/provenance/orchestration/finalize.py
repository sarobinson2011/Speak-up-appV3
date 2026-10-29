import datetime,hashlib,io,json,runpy,zipfile
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B/'client-state-return';T=B/'client-state-tools'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,v):(R/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
primary=json.loads((R/'results/primary/RESULT.json').read_bytes());recovered=json.loads((T/'recovered-output/RESULT.json').read_bytes());fresh=json.loads((T/'fresh.stdout').read_text().splitlines()[-1])
assert primary['result']==recovered['result']==fresh['result']=='PASS'
processes={}
for mode in ('fresh','recovered'):
 p=json.loads((T/(mode+'.process.json')).read_bytes());assert p['exit']==0 and not (T/(mode+'.stderr')).read_bytes();processes[mode]=p
 for suffix in ('stdout','stderr','process.json'):(R/'results'/(mode+'.'+suffix)).write_bytes((T/(mode+'.'+suffix)).read_bytes())
out=R/'results/recovered';out.mkdir()
for p in (T/'recovered-output').iterdir():assert p.is_file();(out/p.name).write_bytes(p.read_bytes())
(R/'results/recovery-gate.json').write_bytes((T/'recovery-gate.json').read_bytes())
write('results/fresh-result.json',fresh)
write('RESULTS.json',{'new_extension':{'primary':{'checks':primary['checks'],'result':primary['result'],'seconds':primary['seconds']},'recovered':{'checks':recovered['checks'],'result':recovered['result'],'seconds':recovered['seconds']},'fresh_process':{'checks':fresh['checks'],'result':fresh['result'],'exit':processes['fresh']['exit'],'seconds':fresh['seconds']},'source_preflight_separate':True,'failed_new_campaigns':[],'independent_review':'PENDING'},
 'reused_independent_classification':{'primary_checks':172,'recovered_root_checks':131,'CLI':1,'failed_attempt_counts':[0,15],'progress_reconciliation':{'combined_rows':31,'failed_prefix':15,'unique_completed_suffix':16,'duplication_mechanism':'UNKNOWN','repeated_validation':False},'prefix_termination_caveat':'CLOSED within terminal classification/modelled paths','rerun':False},
 'reused_independent_forwarding':{'primary_checks':217,'recovered_root_checks':149,'CLI':1,'extra_caveat_cases_separate':6,'rerun':False},
 'prior_supplied_classification':{'primary_checks':131,'recovered_checks':129,'process':1,'failed_attempts':[81,103],'rerun':False},'prior_supplied_forwarding':{'corrected_focused':17,'recovered':168,'process':1,'precorrection_separate':170,'rerun':False},
 'new_requests':0,'new_signatures':0,'database_connections':0,'session_operations':0,'runtime_changes':0,'acquisitions':0,'Git_saves':0,'completed_suite_review_pipeline_lifecycle_reruns':False,
 'all_eleven_obligations_preserved':True,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':'DISABLED'})
review_path=B/'upload/Formal-Lab6-I164-outside-catch-classification-correction-independent-review(1).zip';review=zipfile.ZipFile(review_path);prior_raw=review.read('input/I164-outside-catch-classification-correction-1.zip');prior=zipfile.ZipFile(io.BytesIO(prior_raw));preservation={}
for folder,z in [('retained/client',prior),('retained/review',review)]:
 names=[n for n in z.namelist() if not (folder=='retained/review' and n.startswith('input/'))];root=R/folder;actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()};assert actual==set(names)
 for n in names:assert (root/n).read_bytes()==z.read(n),folder+'/'+n
 preservation[folder]={'files':len(names),'exact_bytes_membership':'PASS'}
manifest=json.loads((B/'client-state-recovered/MANIFEST.json').read_bytes())
for n,pin in manifest.items():assert ident((R/n).read_bytes())==pin,n
fixture=json.loads((R/'fixtures/normal-cases.json').read_bytes());assert ident((R/fixture['source']).read_bytes())==fixture['identity']
preservation['recovered_core']={'files':len(manifest),'final_input_bytes_identical':True};preservation['fixture_lineage']='PASS';preservation['runtime_sources_changed']=0
write('results/final-core-preservation.json',preservation)
changes=json.loads((R/'CHANGED-IDENTITIES.json').read_bytes())
for n,pin in changes['current_code'].items():assert ident((R/'code'/n).read_bytes())==pin
for n,pin in changes['new_controls'].items():assert ident((R/n).read_bytes())==pin
assert ident((R/'results/client-state-correspondence.json').read_bytes())==changes['receipt']
write('CHECKPOINT.json',{'checkpoint':'I164-client-state-return-correspondence-1','author':'SU-Engineering[288D]','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_status':'READY_FOR_INDEPENDENT_REVIEW; no independent support claimed for new extension','scope':'Mandatory typed state forwarding and source-specific _data detachment in both contexts','format':'I164-CLIENT-STATE-RETURN-CORRESPONDENCE-1','code':changes['current_code'],'receipt':changes['receipt'],'prior_review':ident(review_path.read_bytes()),'prior_checkpoint':ident(prior_raw),'results':{'primary':primary['checks'],'recovered':recovered['checks'],'fresh_process':fresh['checks']},'source_additions':json.loads((R/'provenance/source-change-audit.json').read_bytes()),'preserved_all_obligations_and_boundaries':True,'actual_admission':False})
write('DEPENDENCIES.json',{'prior_checkpoint':{'filename':'I164-outside-catch-classification-correction-1.zip','identity':ident(prior_raw),'entries':1508,'decoded_root':'retained/client','complete':True},'independent_review':{'filename':review_path.name,'identity':ident(review_path.read_bytes()),'entries':134,'decoded_non_input_root':'retained/review','non_input_members':133,'omits_only_redundant_input_zip':True},'executable_predecessors':'retained/client/original/retained/handle and documented predecessors','historical_archival_qualifications':'Preserve exact prior RECOVERY.md and DEPENDENCIES.json statements; omitted historical archive bytes are not newly available or qualified.','recovery_input':json.loads((R/'results/recovery-input.json').read_bytes()),'no_original_archive_deletion_compaction_or_replacement':True})
(R/'provenance/orchestration/finalize.py').write_bytes((T/'finalize.py').read_bytes())
api=runpy.run_path(str(R/'tools/checkpoint.py'),run_name='_archive');files=api['inventory'](R);dirs={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_dir()};expected={p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'};assert dirs==expected
identity=api['pack'](files,B/'I164-client-state-return-correspondence-1.zip');(T/'final-archive-identity.json').write_bytes(api['enc'](identity));print(json.dumps(identity),flush=True)
