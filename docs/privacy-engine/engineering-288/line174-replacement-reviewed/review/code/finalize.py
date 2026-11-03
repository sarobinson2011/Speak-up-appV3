"""Package observed review conclusions only after completed-record reconciliation."""
from pathlib import Path
import sys,json,zipfile,datetime,hashlib
sys.path.insert(0,str(Path(__file__).parent))
from integrity import BASE,AREA,INPUT,PIN,enc,file_ident,ident
assert sys.argv[1:] == ['--supported']
def read(p):return json.loads(Path(p).read_bytes())
reconciled=read(BASE/'results/independent-reconciliation.json');main=reconciled['public-recovered'];monitor=reconciled['slot1-monitor'];intake=read(BASE/'results/intake.json')
assert main['rows']==255 and main['kinds']=={'PASS':77,'REJECTED':178} and main['exit']['returncode']==0 and main['input_final_root_equal']
assert monitor['rows']==13 and monitor['kinds']=={'PASS':12,'QUALIFIED':1} and monitor['exit']['returncode']==0
assert file_ident(INPUT)==PIN
prerun=BASE.parent/'I164-line174-FL6-independent-prerun.zip';frozen={}
with zipfile.ZipFile(prerun) as z:
 for p in [BASE/'code'/n for n in ('common.py','public_review.py','independent_model.py','monitor.py','supervise.py','prepare.py','integrity.py')]+sorted((BASE/'fixtures').glob('*.json')):
  name='review/'+p.relative_to(BASE).as_posix();assert p.read_bytes()==z.read(name);frozen[name]=file_ident(p)
(BASE/'results/frozen-review-code-fixtures.json').write_bytes(enc({'prerun':file_ident(prerun),'all_executed_harness_files_and_eight_fixtures_unchanged':True,'files':frozen}))
normal=[]
for p in sorted((BASE/'results/public-recovered').glob('normal-*.json')):
 value=read(p);idx,control,origin=p.stem.removeprefix('normal-').split('-');assert value['scope']['context']==('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO')[int(idx)]
 assert value['earlier_control_completed_in_model'] is (True if control=='True' else None)
 assert value['failure_origin_region']=='protected-'+origin and value['terminal_python_exception_in_model'] is True and value['call_attempt_established'] is True
 normal.append({'file':p.name,'identity':file_ident(p),'context':value['scope']['context'],'control_prefix':'completed normally' if control=='True' else 'absent; no completion asserted','failure_origin':value['failure_origin_region'],'invocation':value['scope']['invocation'],'normal_overall_return':value['normal_overall_return_established'],'helper_body_entry':value['write_new_body_entry_established']})
assert len(normal)==8
supplied=read(BASE/'results/supplied-audit.json');public=read(BASE/'results/public-recovered/actual-public-result.json');limits=read(AREA/'recovered/receipts/prepared-write-call-replacement.json')['new_write_call_limits']
assert limits['all_eleven_obligations_preserved'] is True and limits['inventory_unknown_totals']==4 and limits['lifetime_unknown_totals']==14 and limits['actual_admission'] is False
partials=[]
for p in sorted((BASE/'saves').glob('partial*.json')):
 meta=read(p);local=BASE.parent/meta['file_name'];partials.append({'library_file_id':meta['library_file_id'],'name':meta['file_name'],**file_ident(local)})
checkpoint={'reviewer':'Formal-Lab[6], author-independent reviewer; not Engineering construction author','target':{'name':'I164-line174-NEW-replacement-construction-1.zip',**PIN,'entries':8,'manifested_hashes':7},'verdict':'SUPPORTED within the bounded conditional SOURCE-ONLY line174 correspondence contract, with explicit execution and monitoring qualifications; no candidate defect demonstrated','scope':'Validated selected loop exhaustion through line174 callable/argument evaluation and acknowledged write_new call attempt; stop before helper body','candidate_implementation_changed':False,'smallest_candidate_defect_witness':None,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_accounting':reconciled,'supplied_accounting':supplied,'actual_public_result':public,'same_process_actual_public_after_candidate_C_return_cleanup_without_reviewer_release':True,'authentic_basis_captures':1,'full_public_negative_derivations':0,'negative_layers':'results/rejection-layers.json: every independent negative identified by ordinal and actual error code/layer','normal_context_prefix_origin_matrix':normal,'input_and_recovery':intake,'actual_returned_evidence_audit':read(BASE/'results/returned-evidence-audit.json'),'source_audit':read(BASE/'results/source-audit.json'),'preparation_correction_audit':read(BASE/'results/preparation-correction-audit.json'),'runtime_environment':read(BASE/'results/public-recovered/environment.json'),'retained_host_environment':'Cryptography50.0.2; not equivalent to or qualified by current50.0.0 tests','reviewer_failures':[{'path':'failures/intake-fixture-origin','exit':1,'candidate_control_rows':0,'qualification':'Intake recovery succeeded before mistaken fixture-origin assertion; no recovery replay. Completion artifact/streams retained, but PTY completion exit unrecoverable.'},{'path':'failures/supplied-audit-path','exit':1,'candidate_control_rows':0,'qualification':'Read-only wrong process-directory selection; corrected audit does not replay controls.'}],'qualified_monitoring_observation':{'path':'results/slot1-monitor/qualified-cleanup-interruption.json','result':'QUALIFIED, not PASS','meaning':'Candidate released reservation and removed callback, but interruption prevented local-event reset. No complete-cleanup or reuse claim for that separate process.','reviewer_reset_or_release':False},'durable_prerun':{'library_file_id':'libfile_7f126a5fce6c81919621b2633e5497c8',**file_ident(prerun),'entries':48},'durable_partial_snapshots':partials,'historical_support':'Unchanged reviewed predecessors and LD01/EC01 support carried forward by exact byte preservation; all prior qualified groups/failures retained separately in embedded dependencies; no aggregate or replay','prohibitions_observed':{'application_write_new':0,'runtime_requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'implementation_changes':0,'Git_operations':0,'policy_adoption':0,'completed_campaign_replays':0},'confirmed_save_carried_forward_without_repetition':'88c9fba36bdb243212439acd3027ea934ceda115','limits':limits,'other_limits':['Both acquisitions remain separate','No concrete PID,directory contents/count,filename,resolved path or physical identity observed','Constructed normal/abrupt cases are not runtime execution observations','No helper body/return,encoding,open,write,flush,fsync,175suppression,176rethrow or owner finalization established','Non-None constructor and remaining outer-cleanup gaps remain','Repeated cleanup interruption,termination,alternate interpreters and hostile concurrent replacement remain unqualified','Free monitoring slot alone does not establish all state cleanup','Decision B,retention and allowances unchanged']}
(BASE/'CHECKPOINT.json').write_bytes(enc(checkpoint))
draft=(BASE/'REVIEW-DRAFT.txt').read_text();start=draft.index('Target and identity')
body=draft[start:].replace('The planned public positive uses','The completed public positive used').replace('only its observed returned basis can authorize core checks','only its observed returned basis authorized core checks')
heading='Formal-Lab[6] — AUTHOR-INDEPENDENT REVIEW\n\nVERDICT: SUPPORTED within the bounded conditional SOURCE-ONLY line174\ncorrespondence contract, with explicit execution and monitoring qualifications.\nNo candidate defect demonstrated. Candidate implementation unchanged.\n\n'
observed='''Independent completed evidence
The fresh recovered public process exited0 without timeout after2572.128 seconds.
255 rows reconcile across RESULT,progress,individual records and stdout:
77PASS/178REJECTED. These include one actual public positive through the unchanged
predecessor and one synthetic lease-interruption check before it. The actual
public run completed in the same process after candidate cleanup; no reviewer
release or restart. Exactly one actual authenticated basis was captured.
The receipt is17227133 bytes,SHA256
6d27fa6e1bc6acb56b492f959efea87f15b3febb3d9e299e7f42275178bc1579.
All eight context/prefix/failure-origin normal cases revalidated their parent.
The absent-control prefix retains None,not invented callback completion.
Thirty-two focused nonnormal frontiers and accompanying negatives preserve
source-specific stopping and exception/uncertainty semantics. Candidate inputs
and outputs never replace the actual authenticated basis. The authenticated
parent cases are conditional source models,not authenticated runtime executions.

The separate slot1 process exited0:12PASS and one QUALIFIED cleanup-interruption
observation. Do not call all13 PASS or merge these with Engineering's groups.
Raw stdout,immutable capture chunks,individual records,progress and explicit
exits reconcile exactly. No independent completed-row discrepancy remains.
Preparation exited0 and produced eight fixtures;it has zero recorded candidate
control rows and no authentication credit. Read-only byte/source/evidence audits
are separately recorded and are not silently added to numbered control totals.
See results/rejection-layers.json for every negative's precise layer. No full
public negative derivation was run or claimed. The independently read exact
saved start/binding members corroborate both returned session bindings without
host path resolution or physical-storage inference.

'''
(BASE/'REVIEW.txt').write_text(heading+observed+body)
(BASE/'START-HERE.txt').write_text('Formal-Lab[6] independent review: NEW line174 replacement construction.\n\nSUPPORTED within the bounded conditional SOURCE-ONLY contract; no candidate\ndefect demonstrated. Read REVIEW.txt,CHECKPOINT.json and RECOVERY.txt.\n255 corroborated process rows(77PASS/178REJECTED),exit0;separate slot1\n12PASS/1QUALIFIED,exit0. Engineering29source and314public/core remain separate.\n\nThe input ZIP is included unchanged and supplies all byte-recovery dependencies.\nReviewer code,fixtures,raw logs,chunks,exits,qualified observations and failures\nare retained. PRERUN.txt and REVIEW-DRAFT.txt are historical pre-final records.\nCurrent conclusions are REVIEW.txt and CHECKPOINT.json.\n\nNo application/helper-body execution,session/database operations,acquisition,\nimplementation change,Git save or policy adoption. All11 obligations,4/14UNKNOWN,\nDecision B,retention and allowances remain. SOURCE-ONLY;admission disabled.\n')
old=(BASE/'RECOVERY.txt').read_text();(BASE/'RECOVERY.txt').write_text('FINAL STATE: review completed. Commands below are documentary recovery instructions,\nnot authorization to replay completed checks. Recover bytes and read saved evidence.\nThe actual public and focused processes completed with explicit exits; no process\nis pending. Historical prerun wording remains identifiable below.\n\n'+old)
print(json.dumps({'verdict':checkpoint['verdict'],'main_rows':main['rows'],'main_kinds':main['kinds'],'separate_monitoring':monitor['kinds'],'review_code_and_fixtures_match_durable_prerun':True,'completed':True}),flush=True)
