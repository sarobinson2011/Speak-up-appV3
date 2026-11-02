"""Read-only supplied-record reconciliation. Zero validator/projector replays."""
from pathlib import Path
import sys,json,re,difflib
sys.path.insert(0,str(Path(__file__).parent))
from integrity import identity,enc,js,verify_root
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False)
def rows(path):return [json.loads(s) for s in path.read_text().splitlines() if s]
def corroborate(group,complete):
 p=root/'results'/group;logs=root/'processes'/group;progress=rows(p/'progress.jsonl');numbered=[]
 for s in (logs/'stdout.log').read_text().splitlines():
  match=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED)',s)
  if match:numbered.append((int(match[1]),{'check':match[2],'result':match[3]}))
 assert [i for i,_ in numbered]==list(range(1,len(numbered)+1))
 assert [v for _,v in numbered]==[{k:x[k] for k in ('check','result')} for x in progress[:len(numbered)]]
 exit=js((logs/'exit-status.json').read_bytes());data={'progress_rows':len(progress),'stdout_corroborated':len(numbered),'exit':exit,'stream_hashes':{x:identity((logs/x).read_bytes()) for x in ('stdout.log','stderr.log','exit-status.json')},'progress_identity':identity((p/'progress.jsonl').read_bytes()),'completed':complete}
 if complete:
  result=js((p/'RESULT.json').read_bytes());assert result['rows']==progress and result['checks']==len(progress)==len(numbered) and result['error'] is None and result['result']=='PASS' and exit['returncode']==0 and exit['timed_out'] is False
  data['RESULT_identity']=identity((p/'RESULT.json').read_bytes());data['environment']=result['environment']
 else:
  assert len(progress)==1300 and len(numbered)==165 and exit['returncode']==-15 and exit['timed_out'] is True
  missing=['RESULT.json','calls.json','final-verification.json'];assert all(not (p/n).exists() for n in missing)
  data.update(missing_final_records=missing,missing_stdout_rows_inclusive=[166,1300],discrepancy_cause='UNKNOWN',result='INTERRUPTED; NOT COMPLETED',lost_records_reconstructed=False)
 return data
r={g:corroborate(g,g!='primary') for g in ('source-1','recovered','primary')};assert r['source-1']['progress_rows']==46 and r['recovered']['progress_rows']==341
for label in ('primary','recovered'):
 p=root/'results'/label;pub=js((p/'actual-public-result.json').read_bytes());prior=js((p/'predecessor-public-result.json').read_bytes());assert pub['result']==prior['result']=='PASS';r[label]['saved_public_positives']={'current':pub,'predecessor':prior};r[label]['layers']=js((p/'validation-layers.json').read_bytes())
receipt=(root/'results/recovered/cleanup-append.json').read_bytes();assert receipt==(root/'results/primary/cleanup-append.json').read_bytes()==(root/'receipts/prepared-cleanup-append.json').read_bytes()
prior=js((root/'retained/details/ld01/receipts/corrected-launcher-details.json').read_bytes());current=js(receipt)
for i in range(2):
 old=prior['contexts'][i];new=current['contexts'][i];assert {k:new[k] for k in old}==old and set(new)==set(old)|{'exceptional_cleanup_append_correspondence'}
assert current['prior_launcher_details_components']==prior['extension_components']
limits=current['new_cleanup_append_limits'];assert limits['all_eleven_obligations_preserved'] is True and limits['inventory_unknown_totals']==4 and limits['lifetime_unknown_totals']==14 and limits['actual_admission'] is False and limits['streams']=='UNCOMPUTED'
old=root/'retained/details';names=['code/managed_coverage.py','code/correspondence.py'];diffs={n:''.join(difflib.unified_diff((old/n).read_text().splitlines(True),(root/n).read_text().splitlines(True),fromfile='prior/'+n,tofile='current/'+n)) for n in names};saved_diff=(root/'provenance/implementation.diff').read_text()
assert saved_diff in (''.join(diffs[n] for n in names),''.join(diffs[n] for n in names[::-1]))
supplied=js((root/'RESULTS.json').read_bytes());failures={n:js(p.read_bytes()) for n in ('primary-timeout','preparation-membership','document-patch','packaging-1') for p in [root/'failures'/n/'RECORD.json']}
for item in failures['preparation-membership']['undeclared_entries']:
 p=root/'failures/preparation-membership'/item['preserved_file'];assert identity(p.read_bytes())=={k:item[k] for k in ('bytes','sha256')}
assert supplied['prior_save_reused']=='c43954ff5ee384c6fb6e7a85d83eb36bfea342d1'
r.update({'kind':'Read-only supplied record and preservation audit','new_controls':0,'validator_calls':0,'producer_calls':0,'candidate_changes':0,'new_replays':0,'receipt_identity':identity(receipt),'preparation_not_validation':True,'prior_relations_exactly_preserved':True,'declared_diff_exact':True,'input_recovery':verify_root(root),'historical_prior_review_counts':{'LD01':'52 focused + 15 recovered/public; separate qualified/failure records retained, not replayed','launcher_details':'523 completed checks, 80 qualified rows, zero-replay audit and original independent defect observations retained, not replayed'},'failed_attempts':failures,'withdrawn_claim_files':{n:identity((root/'failures/packaging-1'/n).read_bytes()) for n in ('README.before-accounting-correction.txt','RECOVERY.before-accounting-correction.txt')},'save_receipt':js((root/'provenance/prior-git-save-receipt.json').read_bytes()),'new_save_executed':False,'all_historical_qualifications_retained':True})
(out/'AUDIT.json').write_bytes(enc(r));print(json.dumps({'result':'PASS','source':46,'recovered':341,'interrupted_primary_progress':1300,'interrupted_primary_stdout':165,'new_validator_calls':0}),flush=True)
