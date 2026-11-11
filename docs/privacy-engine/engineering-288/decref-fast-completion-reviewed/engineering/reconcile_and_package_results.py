"""Read saved records and package once. No candidate import or model replay."""
from pathlib import Path
import hashlib,json,datetime,zipfile,stat,shutil,collections
R=Path(__file__).resolve().parent;A=R/'attempt-1';D=R/'results-checkpoint';D.mkdir(exist_ok=False)
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(name,x):p=D/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
source=json.loads((R/'source-identity.json').read_bytes());save=json.loads((R/'source-save-confirmation.json').read_bytes());source.update({'library_file_id':save['library_file_id'],'link':'https://chatgpt.com/library?file_id='+save['library_file_id']+'&account_id=personal','version':save['current_version_number']})
assert ident((R/source['filename']).read_bytes())=={k:source[k] for k in ('bytes','sha256')}
launch=json.loads((A/'launch.json').read_bytes());exit_record=json.loads((A/'exit.json').read_bytes());assert launch['source_sha256']==source['sha256']
rows=[json.loads(p.read_bytes()) for p in sorted((A/'raw').glob('[0-9][0-9][0-9][0-9].json'))]
progress=[json.loads(s) for s in (A/'raw/progress.jsonl').read_text().splitlines()]
stdout=(A/'stdout.log').read_bytes();parsed=[json.loads(s) for s in stdout.decode().splitlines()];printed=[j for j in parsed if 'sequence' in j];finals=[j['result'] for j in parsed if j.get('event')=='RESULT']
assert rows==progress==printed
assert [j['sequence'] for j in rows]==list(range(1,len(rows)+1))
chunks={'stdout':bytearray(),'stderr':bytearray()};metadata=sorted((A/'chunks').glob('*.json'))
for p in metadata:
 j=json.loads(p.read_bytes());b=(A/j['path']).read_bytes();assert ident(b)=={k:j[k] for k in ('bytes','sha256')};chunks[j['stream']].extend(b)
for k,b in chunks.items():assert bytes(b)==(A/(k+'.log')).read_bytes()
assert len(metadata)==exit_record['captured_chunks']
counts=dict(collections.Counter(j['status'] for j in rows));result_path=A/'raw/RESULT.json';failure_path=A/'raw/FAILURE.json'
result=json.loads(result_path.read_bytes()) if result_path.exists() else None
failure=json.loads(failure_path.read_bytes()) if failure_path.exists() else None
if result:
 assert finals==[result] and result['rows']==len(rows)
 assert result['counts']=={k:counts.get(k,0) for k in ('PASS','REJECTED','FAIL')}
complete=bool(result and result['result']=='PASS' and counts.get('FAIL',0)==0 and exit_record['returncode']==0 and not exit_record['timed_out'])
# Check the fixed source tree remains exact without executing any of it.
manifest=json.loads((R/'candidate/MANIFEST.json').read_bytes())
assert {p.relative_to(R/'candidate').as_posix() for p in (R/'candidate').rglob('*') if p.is_file()}==set(manifest)|{'MANIFEST.json'}
assert all(ident((R/'candidate'/n).read_bytes())==v for n,v in manifest.items())
recon={'status':'COMPLETED_AND_RECONCILED' if complete else 'FAILED_OR_INCOMPLETE_PRESERVED','recorded_rows':len(rows),'corroborated_rows':len(rows),'qualified_rows':0,'counts':{k:counts.get(k,0) for k in ('PASS','REJECTED','FAIL')},'individual_progress_stdout_equal':True,'final_result_stdout_equal':result is not None and finals==[result],'child_exit':exit_record,'captured_stream_chunks':len(metadata),'stdout':ident(stdout),'stderr':ident((A/'stderr.log').read_bytes()),'chunks_concatenate_exactly':True,'source_checkpoint':source,'source_tree_unchanged':True,'layer_counts':dict(collections.Counter(j['layer'] for j in rows)),'public_authentication':'UNEXECUTED','authenticated_constructed_path':'UNEXECUTED','public_runs':0,'full_public_negative_derivations':0,'independent_acceptance':'PENDING','failure':failure}
shutil.copytree(A,D/'attempt-1');put('RECONCILIATION.json',recon);put('SOURCE.json',source)
for n in ('CHANGES.json','ACCOUNTING.json','DEPENDENCIES.json'):
 shutil.copyfile(R/'candidate'/n,D/n)
shutil.copyfile(R/'source-save-confirmation.json',D/'source-save-confirmation.json')
put('CHECKPOINT.json',{'identity':'I164-DECREF-FAST-COMPLETION-1-RESULTS','scope':'one new focused pure source/model pass only','result':recon['status'],'rows':len(rows),'counts':recon['counts'],'source':source,'groups_separate':True,'historical_primary':184,'historical_supplement':8,'historical_Engineering':750,'historical_public_positive':1,'new_public_runs':0,'new_authenticated_constructed_path':'UNEXECUTED','new_authentication':'UNEXECUTED','independent_acceptance':'PENDING','runtime_arrival_and_physical_effects':'UNESTABLISHED','zero_count_destructor_completion':'UNRESOLVED','both_acquisitions':'PRESERVED','obligations':11,'inventory_UNKNOWN':4,'lifetime_UNKNOWN':14,'Decision_B':'UNCHANGED','retention':'UNCHANGED','allowances':'UNCHANGED','SOURCE_ONLY':True,'cumulative_envelope':'UNADOPTED','backup':'KERNEL-ONLY','streams':'UNCOMPUTED','readiness':'BLOCKED','final_binding':'BLOCKED','admission':False})
put('FAILURES.json',{'attempts':1,'automatic_retries':0,'new_failed_controls':counts.get('FAIL',0),'new_process_nonzero':exit_record['returncode']!=0,'new_timeout':exit_record['timed_out'],'failure_record':failure,'historical':'Preserved via fixed source and unchanged review/resolution dependencies; no missing record reconstructed or old campaign replayed.'})
(D/'REPORT.txt').write_text('I164-DECREF-FAST-COMPLETION-1 — focused results\n\n'+recon['status']+'\n'+f'{len(rows)} individual records = progress rows = stdout rows. Counts: {recon["counts"]}. Child exit {exit_record["returncode"]}; elapsed {exit_record["seconds"]:.3f}s; timeout {exit_record["timed_out"]}.\n'+f'All {len(metadata)} saved stream chunks concatenate exactly to captured stdout/stderr. Final result and stdout RESULT agree. Source archive/tree remain unchanged.\n\n'+
 'This is one pure source/model pass over the fixed saved candidate, not a public validation or authenticated constructed campaign. Rejections are labelled per raw row: defining-source/catalogue, pure-model binding/guard/order/type or output comparison, and pre-derivation receipt shape. No full public negative derivation is claimed. New mandatory authentication and authenticated constructed paths were inspected statically and remain UNEXECUTED.\n\n'+
 'The two conditional fast branches cover both contexts, both reviewed control prefixes, both protected failure origins and all three retained res classes. Branch state is never inferred from res. Actual returned binding, catalogue and projection mutations are checked separately from copied-output mutations. New model completion is confined to explicit conditional claims; physical effects, actual object state/arrival, zero-count destructor completion, qualified-binary mapping and line2517 remain outside scope.\n\n'+
 'Historical184 primary, eight supplement,750 Engineering and one public positive are separate. Preserve all original failures/UNKNOWN histories, DOC-ENTER-01, R1 discrepancy, recovery assertion/copied-output qualifications, monitoring limits and50.0.0/50.0.2 distinction. No runtime/host, application/helper, database/session, source-retrieval or Git operation was performed. Independent acceptance pending; admission disabled.\n')
(D/'RECOVERY.txt').write_text('Read SOURCE.json and retrieve its exact source checkpoint directly by the supplied Library ID/link. Do not substitute a later source version. Verify this results ZIP identity, CRC, safe exact membership and flat MANIFEST hashes. Read RECONCILIATION.json, REPORT.txt, FAILURES.json and original attempt records.\n\nThe completed pass must be reused; no retry/replay is authorized. The source checkpoint remains source-first historical evidence and was not rewritten after execution. The results include individual rows, progress, stdout/stderr, chunks, final RESULT and explicit child exit. A successful-looking stdout string alone is not the completion claim; reconciliation establishes agreement.\n\nNo public/authenticated constructed path ran. A future separately authorized public preparation must byte-recover the exact4271-file/1197-directory reviewed parent using the source DEPENDENCIES/RECOVERY. It must invoke the unchanged actual authentication path and use the returned basis, never these saved constructed model fixtures as an authenticated basis. No such execution is authorized by this checkpoint.\n\nAll authority boundaries persist; admission disabled.\n')
# Retain this byte-only reconciliation method as provenance; it is not a new model suite.
shutil.copyfile(Path(__file__),D/'reconcile_and_package_results.py')
mm={p.relative_to(D).as_posix():ident(p.read_bytes()) for p in sorted(D.rglob('*')) if p.is_file()};put('MANIFEST.json',mm)
out=R/'I164-decref-fast-completion-1-results.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():
   i=zipfile.ZipInfo(p.relative_to(D).as_posix(),(2026,11,11,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,p.read_bytes())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names)) and set(names)==set(mm)|{'MANIFEST.json'}
 for n,v in mm.items():assert ident(z.read(n))==v
final=dict(ident(out.read_bytes()),filename=out.name,entries=len(names),manifested_hashes=len(mm),reconciliation=recon['status'],rows=len(rows),counts=recon['counts'],exit=exit_record['returncode'])
(R/'results-identity.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps(final,indent=2))
