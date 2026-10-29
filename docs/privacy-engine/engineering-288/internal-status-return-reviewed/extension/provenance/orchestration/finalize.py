"""Package completed current results. Never runs validators or application code."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,runpy,shutil,zipfile
B=Path(__file__).resolve().parents[1];R=B/'status-forwarding';T=B/'status-forward-tools'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def copy_new(src,dst):
 assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
pre=read(R/'results/pre-type-hardening-primary/RESULT.json');types=read(R/'results/exact-types/RESULT.json');rec=read(T/'recovered-output/RESULT.json');rectypes=read(T/'recovered-types/RESULT.json')
freshprocess=read(T/'fresh.process.json');recprocess=read(T/'recovered.process.json')
assert pre['result']==types['result']==rec['result']==rectypes['result']=='PASS'
assert pre['checks']==204 and types['checks']==36 and rec['checks']==205 and rectypes['checks']==34
assert freshprocess['exit']==recprocess['exit']==0 and not (T/'fresh.stderr').read_bytes() and not (T/'recovered.stderr').read_bytes()
fresh=json.loads((T/'fresh.stdout').read_text().splitlines()[-1]);assert fresh['result']=='PASS' and fresh['checks']==5
for folder,result in [(R/'results/pre-type-hardening-primary',pre),(R/'results/exact-types',types),(T/'recovered-output',rec),(T/'recovered-types',rectypes)]:
 progress=[json.loads(x) for x in (folder/'progress.jsonl').read_text().splitlines()];assert len(progress)==result['checks'] and progress==result['rows']
for group in ('recovered-output','recovered-types'):
 for p in (T/group).iterdir():copy_new(p,R/'results'/group/p.name)
for mode in ('fresh','recovered'):
 for ext in ('stdout','stderr','process.json'):copy_new(T/(mode+'.'+ext),R/'results'/(mode+'.'+ext))
(R/'results/fresh-result.json').write_bytes(enc(fresh));copy_new(T/'recovery-gate.json',R/'results/recovery-gate.json')
gate=read(T/'recovery-gate.json');assert gate['all_recovered_bytes_unchanged']=='PASS'
core=read(T/'recovery-core-identities.json');assert all(ident((R/n).read_bytes())==p for n,p in core.items())
(R/'results/final-core-preservation.json').write_bytes(enc({'recovered_input':read(R/'results/recovery-input.json'),'same_final_input_members':len(core),'all_bytes_unchanged':True,'final_added_records':'current recovered/fresh process results, final metadata and provenance; no code/input substitution'}))
prior=R/'retained/state';manifest=read(prior/'MANIFEST.json')
assert all(ident((prior/n).read_bytes())==pin for n,pin in manifest.items())
review=R/'retained/review';rm=read(review/'MANIFEST.json');selected=[n for n in rm if not n.startswith('input/')];assert all(ident((review/n).read_bytes())==rm[n] for n in selected)
(R/'provenance/final-retained-preservation.json').write_bytes(enc({'prior_target_members':len(manifest)+1,'exact_hashes':'PASS','review_non_input_members':len(selected)+1,'exact_review_hashes':'PASS','omission':'redundant review input ZIP only, retained in original external archive','historical_qualifications_unchanged':True}))
old=(prior/'code/managed_coverage.py').read_text();new=(R/'code/managed_coverage.py').read_text()
(R/'provenance/change-managed_coverage.py.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='reviewed-client-state/code/managed_coverage.py',tofile='internal-status/code/managed_coverage.py')))
for name in ('setup.py','preflight.py','run_process.py','recover_and_check.py','finalize.py'):copy_new(T/name,R/'provenance/orchestration'/name)
results={'result':'PASS within bounded static/conditional correspondence scope','current_exact_type_primary':{'checks':36,'original_acceptance_witness_reproductions':12,'result':'PASS'},'current_recovered_root':{'correspondence_checks':205,'exact_type_checks':34,'original_witness_reproductions_in_type_count':12,'result':'PASS'},'current_fresh_process':{'checks':5,'exit':0,'result':'PASS'},'pre_type_hardening_primary':{'checks':204,'scope':'original new extension before exact-type correction; separate, not counted as current primary'},'failed_new_control_attempt':{'checks_before_failure':17,'excluded_from_completed_totals':True,'kind':'ineffective guard mutation'},'original_type_acceptance_witnesses':'preserved source and twelve reproductions across both contexts; corrected rejection controls separate','prior_independent':{'primary':273,'recovered':196,'CLI':1,'failed_reviewer_attempt':17,'packaging_failure_separate':True,'rerun':False},'prior_Engineering':{'primary':171,'recovered':173,'fresh_assertions':5,'rerun':False},'fresh_process_seconds':freshprocess['seconds'],'recovered_process_seconds':recprocess['seconds'],'application_operations':0,'database_connections':0,'session_operations':0,'requests':0,'acquisitions':0,'Git_operations':0,'runtime_source_changes':0,'completed_prior_suites_rerun':False}
(R/'RESULTS.json').write_bytes(enc(results))
(R/'CHECKPOINT.json').write_bytes(enc({'checkpoint':'I164-internal-status-return-correspondence-1','construction_author':'SU-Engineering[288D]','independent_review':'REQUESTED; not claimed','result':results['result'],'current_components':{n:ident((R/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'receipt':ident((R/'results/status-forward-correspondence.json').read_bytes()),'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'hops':['manager-return','session-return','control-return'],'prior_producer_functions_preserved':70,'new_producer_functions':6,'runtime_forwarding_evidence':'UNAVAILABLE','physical_reference_observations':None,'observer_join':None,'source_phase_cases_not_complete_history':True,'all_eleven_obligations_preserved':True,'inventory_UNKNOWN_totals':4,'lifetime_UNKNOWN_totals':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False}))
(R/'DEPENDENCIES.json').write_bytes(enc({'reviewed_predecessor':read(R/'provenance/input-verification.json'),'current_executable_predecessor':'retained/state','recovery_input':read(R/'results/recovery-input.json'),'current_profile':read(R/'results/offline-environment.json'),'historical_archive_omissions':'preserved exactly as qualified in retained/review/results/composition.json; no new outer archive claim','no_database_connection_required':True}))
(R/'failures/README.md').write_text('The failed 17-check ineffective-guard control attempt is exact under control-attempt-1 and excluded. The original type-acceptance producer/adapter and control source are exact under type-acceptance-precorrection; deterministic acceptance/rejection witnesses are in tests/type_controls.py and results/exact-types/original-witnesses.json. The successful 204-check pre-type campaign is retained separately, not counted as current-code primary support. All earlier independent/supplied failures remain unchanged inside retained roots. No failure was deleted, silently repaired or promoted into completed totals.\n')
pack=runpy.run_path(str(R/'tools/checkpoint.py'));files=pack['inventory'](R);assert 'MANIFEST.json' not in files
target=B/'I164-internal-status-return-correspondence-1.zip';identity=pack['pack'](files,target)
# Preserve the final manifest alongside the exact packaged root; no executable check.
with zipfile.ZipFile(target) as z:(R/'MANIFEST.json').write_bytes(z.read('MANIFEST.json'))
(T/'final-archive-identity.json').write_bytes(enc(identity));print(json.dumps(identity,indent=2))
