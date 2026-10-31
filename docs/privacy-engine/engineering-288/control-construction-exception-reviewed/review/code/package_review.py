"""Read-only result reconciliation and review packaging. No candidate execution."""
from pathlib import Path
import sys,json,datetime,zipfile,stat
sys.path.insert(0,str(Path(__file__).parent))
from integrity import BASE,INPUT,PIN,PRIOR_PIN,identity,enc,safe,verify_root
REVIEW=BASE/'ccn-review'
def reconcile(label):
 p=REVIEW/'results'/label;proc=REVIEW/'processes'/label
 if not (proc/'exit-status.json').exists():return {'state':'NOT FINALIZED','completed_group':False}
 ex=json.loads((proc/'exit-status.json').read_bytes());result=json.loads((p/'RESULT.json').read_bytes()) if (p/'RESULT.json').exists() else None
 rows=[json.loads(x) for x in (p/'progress.jsonl').read_text().splitlines()] if (p/'progress.jsonl').exists() else []
 printed=[]
 for line in (proc/'stdout.log').read_text().splitlines():
  t=line.split(' ',1)
  if len(t)==2 and t[0].isdigit():n,status=t[1].rsplit(' ',1);printed.append((int(t[0]),n,status))
 assert [(i+1,x['check'],x['result']) for i,x in enumerate(rows)]==printed,label
 if result is not None:assert result['rows']==rows and result['checks']==len(rows),label
 return {'state':result['result'] if result else 'INCOMPLETE','completed_group':bool(result and result['result']=='PASS' and ex['returncode']==0 and ex['timed_out'] is False),'corroborated_rows':len(rows),'result':result,'exit':ex,'progress_stdout_reconciled':True}
groups={n:reconcile(n) for n in ('primary','recovered','source','audit-completion')}
assert groups['primary']['state']!='NOT FINALIZED','Primary still active/unfinalized; no packaging yet'
if groups['primary']['completed_group']:assert groups['recovered']['state']!='NOT FINALIZED','Recovered process still required/active'
assert groups['source']['corroborated_rows']==61 and not groups['source']['completed_group']
assert groups['audit-completion']['completed_group'] and groups['audit-completion']['corroborated_rows']==0
supported=groups['primary']['completed_group'] and groups['recovered']['completed_group']
verdict='SCOPED SUPPORT WITH RETAINED ACCOUNTING AND OBSERVATION QUALIFICATIONS' if supported else 'INCOMPLETE INDEPENDENT REVIEW'
if supported:
 for label in ('primary','recovered'):
  result=groups[label]['result'];assert result['public_basis_calls_observed']==1
  events=[json.loads(x) for x in (REVIEW/'results'/label/'events.jsonl').read_text().splitlines()]
  assert sum(x['event']=='actual_basis_return_observed' for x in events)==1
  calls=json.loads((REVIEW/'results'/label/'calls.json').read_bytes());current='/workspace/review-evidence/FL6-construction-20261031/'+label+'/code/correspondence.py'
  assert sum(x['file']==current and x['function']=='_basis' for x in calls)==1
  assert sum(x['file']==current and x['function']=='derive_construction' for x in calls)==1
  assert sum(x['file']==current and x['function']=='validate' for x in calls)==13
 rejected=json.loads((REVIEW/'results/recovered/public-rejection.json').read_bytes());assert rejected['error']=='CONSTRUCTION-STALE-OR-ALTERED-RECEIPT' and rejected['layer']=='public post-derivation receipt comparison'
 raw=Path('/workspace/review-evidence/FL6-construction-20261031/recovered/results/primary/control-construction.json').read_bytes();q=json.loads(raw)
 for row in q['contexts']:
  x=row['control_construction_revocation_correspondence'];assert x['construction_completed'] is False and x['control_callback_execution'] is False and x['exception_chain_observation'] is None and x['declaration']['source']['completed_control_object_established'] is False
  x['construction_completed']=True;x['control_callback_execution']=True;x['exception_chain_observation']={'existing_cause':None};x['declaration']['source']['completed_control_object_established']=True
 assert (json.dumps(q,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()==(REVIEW/'results/recovered/coordinated-receipt.json').read_bytes()
final={n:verify_root(Path('/workspace/review-evidence/FL6-construction-20261031')/n) for n in ('primary','recovered')}
(REVIEW/'results/final-preservation.json').write_bytes(enc(final))
integrity=json.loads((REVIEW/'results/integrity.json').read_bytes());audit=json.loads((REVIEW/'results/audit-completion/preservation-and-supplied.json').read_bytes())
root=Path('/workspace/review-evidence/FL6-construction-20261031/primary');old=json.loads((root/'retained/control/results/primary/control-exception.json').read_bytes());new=json.loads((root/'results/primary/control-construction.json').read_bytes())
assert all(new[k]==v for k,v in old.items() if k not in ('format','extension_components','contexts'))
assert len(new['contexts'])==len(old['contexts'])==2
for before,after in zip(old['contexts'],new['contexts']):
 assert set(after)==set(before)|{'control_construction_revocation_correspondence'}
 assert all(after[k]==v for k,v in before.items())
assert new['prior_control_components']==old['extension_components']
outcomes={n:{k:sum(x['result']==k for x in g.get('result',{}).get('rows',[])) for k in ('PASS','REJECTED')} for n,g in groups.items() if g.get('result')}
summary=('Fresh primary and recovered-root processes completed with exit 0 and no timeout. Primary recorded '+str(groups['primary']['corroborated_rows'])+' controls; recovered recorded '+str(groups['recovered']['corroborated_rows'])+'. Each result row reconciles with saved progress and stdout. The primary process executed actual pristine public validation in both contexts. The recovered process executed one fresh coordinated two-context public rejection and independently confirmed its exact post-derivation receipt-comparison layer, then representative internal-core checks. Its private derived receipt equals the saved pristine bytes. These are separate process groups, not a rerun of Engineering\'s campaign. No residual implementation defect was demonstrated within this bounded slice.' if supported else 'Fresh execution did not complete the necessary review. Exact available results, timeouts/failures, partial rows and missing work are retained in CHECKPOINT.json. No passing source or supplied record substitutes for unfinished validation. No support verdict is inferred.')
summary+='\n\nThe independent source attempt recorded 61 corroborated successful/intentionally rejected rows before a separate reviewer audit-order failure; it remains a failed attempt outside completed-group totals. The subsequent read-only audit completed with zero controls replayed. The preparation-only import error has zero controls. A first packaging assertion also incorrectly compared whole context arrays despite the declared added relation; its code/log are preserved, and the corrected audit verifies exact preservation of every old field plus exactly that one addition in each context. This packaging failure executed zero controls. No unqualified total combines these records.\n\nPublic mutable results, privately returned projections and semantic row copies were tested separately from authenticated predecessor reconstruction. Source-derived and constructed tests establish no runtime observation. Private-core negatives reuse the actually returned authenticated basis; they are not claimed as separate public/full-basis executions.'
report=(REVIEW/'REPORT.draft.txt').read_text().replace('VERDICT_PENDING_PROCESS_RESULTS','Verdict: '+verdict).replace('INDEPENDENT_RESULTS_PENDING',summary)
(REVIEW/'REPORT.txt').write_text(report)
checkpoint={'reviewer':'Formal-Lab[6]','construction_author':'SU-Engineering[288D]','author_independent':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_name':'I164-control-construction-exception-correspondence-1.zip','target':PIN,'verdict':verdict,'scoped_support':supported,'integrity':integrity,'independent_groups':groups,'outcomes':outcomes,'completed_group_control_counts':{n:g['corroborated_rows'] for n,g in groups.items() if g['completed_group']},'independent_failed_attempt_source_rows':61,'combined_unqualified_total':None,'supplied_records':audit['supplied'],'prior_qualified_accounting':audit['prior_qualified_accounting'],'preservation':audit['scope_limits'],'final_roots':final,'all_predecessor_receipt_fields_preserved':True,'all_117_inherited_definitions_preserved':True,'implementation_unchanged_by_reviewer':True,'process_environment':groups['primary'].get('result',{}).get('environment'),'runtime_observations':'UNAVAILABLE','outer_cleanup':'UNEXPANDED','selected_owner_continuity':'CONDITIONAL','existing_cause_context_suppression':'UNKNOWN','observer':'UNJOINED','all_eleven_obligations':'PRESERVED','inventory_unknown_totals':4,'lifetime_unknown_totals':14,'SOURCE_ONLY':'UNCHANGED','cumulative_envelope':'UNADOPTED','readiness':'BLOCKED','final_binding':'BLOCKED','actual_admission':False,'completed_suite_reruns':0,'database_connections':0,'session_operations':0,'acquisitions':0,'runtime_changes':0}
checkpoint.pop('all_predecessor_receipt_fields_preserved')
checkpoint['all_old_context_fields_preserved']=True
checkpoint['predecessor_receipt_preserved_except_declared_extension_envelope']=True
checkpoint['declared_envelope_changes']=['format identifier','extension_components moved intact to prior_control_components','one construction relation added in each context','new extension identity and limit fields']
(REVIEW/'CHECKPOINT.json').write_bytes(enc(checkpoint))
(REVIEW/'RECOVERY.txt').write_text('Verify the delivered outer archive identity, safe unique regular-file membership, CRC and all MANIFEST.json hashes. The exact construction input is included under input/. Its safe manifest recovery produces 3,260 files and 898 implied directories, including all required predecessor roots. Do not put review output or forensic extras into strict predecessor roots. No validator is executed automatically. Completed groups and source controls must not be replayed merely to inspect this checkpoint.\n\nThe independent comparison used the exact external prior review archive: '+json.dumps(PRIOR_PIN)+'; Library libfile_2fbb2a5dde04819196cee9fcc6faa325, Formal-Lab6-I164-control-callback-exception-independent-review.zip. Its exact nested incomplete/target identities are recorded in results/integrity.json. These original outer archives are not reconstructed from flattened members. Current candidate recovery is self-contained; repeating the historical original-archive comparison requires that exact external predecessor review. The original intermediate engineering recovery-cut outer ZIP remains continuity evidence only.\n\nKeep all failed/interrupted campaigns and partial files as evidence. Never convert 285/71 plus two separate supplied checks, prior 520/517/106-103-103/9+1, or this review\'s 61-row failed source-audit attempt into an unqualified completed total. No runtime/session/database operations, policy changes or admission are authorized.\n')
(REVIEW/'START-HERE.txt').write_text('Read REPORT.txt, CHECKPOINT.json and RECOVERY.txt. Target: I164-control-construction-exception-correspondence-1.zip. Verdict: '+verdict+'. Original candidate code and all evidence remain unchanged. The draft is retained as history.\n')
members={'input/I164-control-construction-exception-correspondence-1.zip':INPUT}
for p in sorted(REVIEW.rglob('*')):
 if p.is_dir():continue
 assert stat.S_ISREG(p.lstat().st_mode),p
 n=p.relative_to(REVIEW).as_posix();safe(n);members[n]=p
manifest={n:identity(p.read_bytes()) for n,p in members.items()};assert 'MANIFEST.json' not in manifest
archive=BASE/('Formal-Lab6-I164-control-construction-exception-'+('independent-review' if supported else 'INCOMPLETE-review')+'.zip')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in members.items():
  info=zipfile.ZipInfo(n);info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
 info=zipfile.ZipInfo('MANIFEST.json');info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,enc(manifest))
with zipfile.ZipFile(archive) as z:
 assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(manifest)|{'MANIFEST.json'}
 for info in z.infolist():safe(info.filename);assert stat.S_ISREG(info.external_attr>>16)
 for n,pin in manifest.items():assert identity(z.read(n))==pin,n
 assert identity(z.read('input/I164-control-construction-exception-correspondence-1.zip'))==PIN
out={'path':str(archive),'identity':identity(archive.read_bytes()),'entries':len(manifest)+1,'manifested_hashes':len(manifest),'CRC':'PASS','safe_exact_membership':'PASS','all_manifest_hashes':'PASS','verdict':verdict}
(BASE/'ccn-package.json').write_bytes(enc(out));print(json.dumps(out),flush=True)
