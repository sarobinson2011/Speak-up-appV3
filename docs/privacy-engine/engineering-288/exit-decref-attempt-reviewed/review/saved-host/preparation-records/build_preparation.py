"""Build prospective recording/launch files only; never runs a host entry."""
from pathlib import Path
import ast,copy,hashlib,json,shutil,traceback,datetime
B=Path(__file__).resolve().parent;H=B/'parent-host';O=B/'package';C=B/'candidate'
AUTH='I164-EXIT-DECREF-ATTEMPT-FULL-PUBLIC-POSITIVE-1-20261112'
WORK='/srv/Engineering-288-execution/steve/I164-exit-decref-attempt-public-1-20261112'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def wr(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def rep(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def rename(s):return s.replace('res-null-test','exit-decref-attempt').replace('res-null','exit-decref').replace('res_null','exit_decref').replace('RES-NULL-TEST','EXIT-DECREF-ATTEMPT').replace('RES-NULL','EXIT-DECREF').replace('20261111','20261112')
try:
 shutil.copytree(H/'code',O/'code');shutil.copytree(H/'observer-reference',O/'observer-reference')
 shutil.copytree(H/'inputs',O/'inputs')
 for n in ('I164-exit-decref-attempt-1-source.zip','I164-exit-decref-attempt-1-results.zip'):shutil.copyfile(B.parent/n,O/'inputs'/n)
 for p in (H/'expected').iterdir():
  if p.name=='ASSEMBLED-ROOT-MANIFEST.json':shutil.copyfile(p,O/'expected/RES-NULL-ROOT-MANIFEST.json')
  else:shutil.copyfile(p,O/'expected'/p.name)
 shutil.copyfile(B/'ASSEMBLED-ROOT-MANIFEST.json',O/'expected/ASSEMBLED-ROOT-MANIFEST.json')
 for n in ['validation/results/RESULT.json','validation/results/actual-parent-provenance.json','validation/results/actual-receipt-comparison.json','validation/process/exit.json','validation/RECONCILIATION.json','service-exit.json','manager-exit.json','host-profile.stdout','service-runtime-profile.json','PLAN.json','EXPORT-MANIFEST.json','EXPORT-STATUS.json','FAILURES.json']:
  p=O/'reference/parent-host'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(H/n,p)
 # Preserve prior historical preparation/review chronology; no re-interpretation.
 shutil.copytree(H/'reference',O/'reference/parent-retained')
 plan=json.loads((H/'PLAN.json').read_bytes());old=copy.deepcopy(plan);assembled=json.loads((B/'byte-recovery-result.json').read_bytes());expected=json.loads((B/'offline-assembly.json').read_bytes())
 plan.update({'identity':'I164-EXIT-DECREF-ATTEMPT-1-PUBLIC-POSITIVE-PREPARATION-1','attempt':AUTH,'workspace':WORK,'unit':'i164-exit-decref-attempt-public-1-20261112.service','confirmed_save_reused':'dc0851dae241ffaaf7ed84e75830f672981c020e',
  'source_archive':ident((B.parent/'I164-exit-decref-attempt-1-source.zip').read_bytes()),'focused_results_archive':ident((B.parent/'I164-exit-decref-attempt-1-results.zip').read_bytes()),
  'res_null_source_archive':old['source_archive'],'res_null_root_manifest':old['assembled_root_manifest'],'res_null_receipt':old['expected_receipt'],'res_null_files':4729,'res_null_directories':1238,
  'expected_receipt':expected['expected_receipt'],'assembled_root_manifest':ident((B/'ASSEMBLED-ROOT-MANIFEST.json').read_bytes()),'new_candidate_files':assembled['roots']['NEW']['files'],'new_candidate_directories':assembled['roots']['NEW']['directories'],
  'qualification':'Conditional SOURCE-ONLY completed true comparison plus explicit continuation and selected exit-role continuity to Py_DECREF(exit) attempt at bytecodes.c:2518/generated_cases.c.h:3532. Stop before decrement completion/effects, error routing or false-branch operations. C NULL differs from Python None. Runtime arrival, object state, physical effects, zero-count destructor completion and qualified-binary correspondence remain unestablished.'})
 ex=json.loads((H/'validation/process/exit.json').read_bytes());assert ex['child_exit']==0 and not ex['timed_out']
 plan['deadline_basis'].update({'retained_res_null_child_seconds':ex['seconds'],'retained_res_null_child_exit':0,'retained_res_null_timeout':False,'explanation':'Saved reviewed res-null parent public positive took '+str(ex['seconds'])+' seconds (~59.4 minutes). One finite declaration layer is added. Retain 60–90 minute estimate,110-minute soft,115-minute child-supervisor and120-minute service limits, with final-record margin. No benchmark, dummy or completed campaign replay.'})
 plan['actual_wrapper_expectations']['res_null_validate']=0
 plan['reused_groups']['res_null_focused']=plan['reused_groups'].pop('new_slice_focused')
 plan['reused_groups'].update({'res_null_independent':{'total':159,'PASS':79,'REJECTED':80,'read_only_reconciliation_failure':'corrected; historical original preserved'},'res_null_Ubuntu_public_positive':1,'new_slice_focused':{'total':289,'PASS':79,'REJECTED':210,'batches':[{'name':'source-rows','rows':55,'PASS':15,'REJECTED':40},{'name':'matrix-one','rows':43,'PASS':19,'REJECTED':24},{'name':'matrix-two','rows':43,'PASS':19,'REJECTED':24},{'name':'mutations-one','rows':74,'PASS':13,'REJECTED':61},{'name':'mutations-two','rows':74,'PASS':13,'REJECTED':61}],'exits':[0,0,0,0,0],'replayed':0,'layers':'Pure source/model, static integration and pre-derivation gates only; no authenticated basis/constructed-path credit'}})
 wr(O/'PLAN.json',plan)
 # Add one actual returned-parent level to the reused recording harness.
 s=rename((H/'code/public_positive.py').read_text())
 s=rep(s,"'fast':False}","'fast':False,'res_null':False}")
 s=rep(s,"fast_path=root/'retained/fast';", "res_null_path=root/'retained/res-null';fast_path=res_null_path/'retained/fast';")
 s=rep(s," fastmod=basis['parent_module'];fb=basis['parent_basis']", " resmod=basis['parent_module'];nb=basis['parent_basis']\n need(Path(resmod.__file__).resolve()==res_null_path/'code/correspondence.py','ACTUAL-RES-NULL-MODULE-ORIGIN')\n res_null_bytes=resmod.enc(resmod._assemble(nb))\n need(res_null_bytes==basis['fresh']['saved'] and byte_identity(res_null_bytes)==plan['res_null_receipt'],'ACTUAL-RES-NULL-BASIS-RECEIPT');agreements['res_null']=True\n fastmod=nb['parent_module'];fb=nb['parent_basis']")
 s=rep(s,"fast_bytes==basis['fresh']['saved']","fast_bytes==nb['fresh']['saved']")
 s=rep(s,"'fast_basis_source':'actual unchanged fast-completion _basis return inside new exit-decref _basis'", "'res_null_basis_source':'actual unchanged res-null _basis return inside new exit-decref _basis','res_null_receipt':byte_identity(res_null_bytes),'res_null_validation':basis['parent_public'],'fast_basis_source':'actual unchanged fast-completion _basis return inside res-null _basis'")
 s=rep(s,"'fast_validation':basis['parent_public']","'fast_validation':nb['parent_public']")
 s=s.replace('thin_fast_decref_return_enter_lookup_R1_helper_validate_wrappers_called','thin_res_null_fast_decref_return_enter_lookup_R1_helper_validate_wrappers_called')
 s=rep(s,"[('fast',fast_path),","[('res_null',res_null_path),('fast',fast_path),")
 s=rep(s,"'thin_wrapper_calls':{'fast':","'thin_wrapper_calls':{'res_null':count(res_null_path/'code/correspondence.py'),'fast':")
 (O/'code/public_positive.py').write_text(s)
 for n in ('service_entry.py','status.py','export_evidence.py'):
  s=rename((H/'code'/n).read_text())
  if n=='status.py':
   s=rep(s,"{'exit_decref':True,'fast':True", "{'exit_decref':True,'res_null':True,'fast':True")
   s=rep(s,"{'fast':0,'decref':0", "{'res_null':0,'fast':0,'decref':0")
  (O/'code'/n).write_text(s)
 s=rename((H/'code/host_prepare_launch.py').read_text())
 s=rep(s,"  root=WORK/'candidate';(root/'retained').mkdir();fast=root/'retained/fast'", "  root=WORK/'candidate';(root/'retained').mkdir();res_null=root/'retained/res-null'\n  common.unzip(WORK/'inputs/I164-res-null-test-1-source.zip',res_null,plan['res_null_source_archive'])\n  (res_null/'retained').mkdir();fast=res_null/'retained/fast'")
 s=rep(s,"  need(identity(root/'reference/fast/actual-receipt.json')", "  rescheck=common.exact_tree(res_null,json.loads((WORK/'expected/RES-NULL-ROOT-MANIFEST.json').read_bytes()))\n  need(rescheck['files']==4729 and rescheck['directories']==1238,'RES-NULL-ASSEMBLED-MEMBERSHIP');save(WORK/'res-null-root.json',rescheck)\n  need(identity(root/'reference/res-null/actual-receipt.json')==plan['res_null_receipt'],'RES-NULL-RECEIPT-PIN')\n  need(identity(res_null/'reference/fast/actual-receipt.json')")
 s=s.replace('exact fast/decref/return/enter-call/lookup parents','exact res-null/fast/decref/return/enter-call/lookup parents')
 s=rep(s,"'source_archive':plan['source_archive'],'fast_receipt':", "'source_archive':plan['source_archive'],'res_null_receipt':plan['res_null_receipt'],'fast_receipt':")
 (O/'code/host_prepare_launch.py').write_text(s)
 unchanged=['common_r1.py','recovery.py','runtime_profile.py','expected-runtime.json','supervisor.py','manager_exit.py'];changed={};syntax=[]
 for n in unchanged:assert (O/'code'/n).read_bytes()==(H/'code'/n).read_bytes()
 for p in (O/'observer-reference').iterdir():assert p.read_bytes()==(H/'observer-reference'/p.name).read_bytes()
 for p in sorted((O/'code').glob('*.py')):
  ast.parse(p.read_bytes(),filename=str(p));compile(p.read_bytes(),str(p),'exec');syntax.append(p.name)
  if p.read_bytes()!=(H/'code'/p.name).read_bytes():changed[p.name]={'before':ident((H/'code'/p.name).read_bytes()),'after':ident(p.read_bytes())}
 tree=ast.parse((O/'code/public_positive.py').read_bytes());pub=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='m' and n.func.attr=='validate'];assert len(pub)==1
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('_basis','inputs','derive','_construct_checked','constructed_projection') for n in ast.walk(tree))
 wr(O/'preparation-records/static-launcher-audit.json',{'syntax_parsed_not_executed':syntax,'sole_public_validate_call_AST':1,'harness_direct_authentication_calls':0,'substantive_authentication':'inside unchanged candidate validate/derive/_basis path','candidate_or_harness_validation_executed':False,'unchanged_recording_and_preflight':{n:ident((O/'code'/n).read_bytes()) for n in unchanged},'observer_unchanged':{p.name:ident(p.read_bytes()) for p in (O/'observer-reference').iterdir()},'changed_preparation_code':changed})
 wr(O/'CHANGES.json',{'candidate_changes':[],'parent_changes':[],'preparation_changes':changed,'unchanged_recording_and_preflight':unchanged,'new_expected_output_only':plan['expected_receipt'],'source_version':'Exact I164-EXIT-DECREF-ATTEMPT-1 source archive'})
 wr(O/'INPUTS.json',{'source':{'filename':'I164-exit-decref-attempt-1-source.zip','library_file_id':'libfile_fde3_f-d61c757824a881918ebff2155bc690a2_39c64cf85e608191bb9545db7327fd84',**plan['source_archive']},'focused_results':{'filename':'I164-exit-decref-attempt-1-results.zip','library_file_id':'libfile_fde3_f-824dbe68880481919e317ac9c01bc91e_39c64cf85e608191bb9545db7327fd84',**plan['focused_results_archive']},'reviewed_parent_host':{'filename':'I164-res-null-test-public-1-host-evidence.tar.gz','library_file_id':'libfile_fde3_f-9fd2f48060608191982d6a4292de1ad5_39c64cf85e608191bb9545db7327fd84','bytes':23682326,'sha256':'e20093f20368ff130a6c64d6a634fc993b43a05b1e65b01ec6a4e54a58902101'},'large_recovery_dependency':{'filename':'I164-helper-open-persistent-host-launcher-review-2.zip','library_file_id':'libfile_fde3_f-f9fd72efc654819194987af266042001_39c64cf85e608191bb9545db7327fd84',**plan['launcher_archive'],'existing_host_path':plan['launcher_host_path']}})
 wr(O/'FAILURES.json',{'new_preparation_execution_failures':[],'read_only_inspection_misses':['Initial guessed validate_once.py path absent; actual public_positive.py identified via file listing.','Compact saved selection omitted recovery.py; full pinned host archive retrieved, original bytes used.','No saved catalogue/setup artifact in new focused results; offline expected catalogue derived from fixed producer, retained parent declaration and source bytes.'], 'campaigns_replayed':0,'source_construction_qualifications':json.loads((C/'FAILURES.json').read_bytes()),'historical':'All failures,missing/UNKNOWN records,145 timeout/171 continuation and159 independent controls remain distinct; no reconstruction or replay. DOC-ENTER-01,R1 discrepancy,monitoring cleanup qualifications and50.0.0/50.0.2 distinction retained.','new_authenticated_constructed_path':'UNEXECUTED','new_public_validation':'UNEXECUTED','independent_acceptance':'PENDING'})
 for n in ('assemble_parent.py','offline_expected.py','build_preparation.py','INTAKE-VERIFICATION.json','byte-recovery-result.json','byte-recovery-exit.json','byte-recovery.stdout','byte-recovery.stderr','offline-assembly.json','offline-assembly-exit.json','offline-assembly.stdout','offline-assembly.stderr'):shutil.copyfile(B/n,O/'preparation-records'/n)
 print(json.dumps({'attempt':AUTH,'expected_receipt':plan['expected_receipt'],'assembled_files':plan['new_candidate_files'],'assembled_directories':plan['new_candidate_directories'],'candidate_changes':0,'status':'PREPARED ONLY'},indent=2))
except BaseException as e:
 wr(B/'preparation-build-failure.json',{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});raise
