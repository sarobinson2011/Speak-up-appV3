"""Package only saved EC01 results after explicit process completion. No validator replay."""
from pathlib import Path
import json,hashlib,zipfile,stat,shutil,datetime,collections
T=Path(__file__).resolve().parents[1];B=T/'bundle';name='focused-recovered';R=T/'results'/name;P=T/'processes'/name
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def copy_file(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
print('1/4 Reconcile new results, both saved streams and explicit exit; no control replay',flush=True)
result=json.loads((R/'RESULT.json').read_bytes());ex=json.loads((P/'exit-status.json').read_bytes())
assert result['result']=='PASS' and ex['returncode']==0 and ex['timed_out'] is False
rows=[json.loads(x) for x in (R/'progress.jsonl').read_text().splitlines()]
assert rows==result['rows'] and len(rows)==result['checks']
stdout=(P/'stdout.log').read_text().splitlines();numbered=[x for x in stdout if x.split(' ',1)[0].isdigit()]
assert numbered==[str(i)+' '+row['check']+' '+row['result'] for i,row in enumerate(rows,1)]
assert (P/'stderr.log').read_bytes()==b''
assert {k:(P/k).stat().st_size for k in ('stdout.log','stderr.log')}==ex['streams_bytes_observed']
assert all(row['result'] in ('PASS','REJECTED') and row['layer'] for row in rows)
calls=json.loads((R/'calls.json').read_bytes());root=(T/'recovered').resolve()
counts={}
for label,path in [('current',root/'code/correspondence.py'),('unchanged_predecessor',root/'retained/details/code/correspondence.py')]:
 counts[label]=dict(collections.Counter(x['function'] for x in calls if x['file']==str(path)))
 assert counts[label].get('validate')==1 and counts[label].get('_basis')==1
pin=ident((B/'ROOT-MANIFEST.json').read_bytes())
assert json.loads((R/'input-verification.json').read_bytes())['manifest']==pin
assert json.loads((R/'final-verification.json').read_bytes())['manifest']==pin
receipt=(B/'overlay/ec01/receipts/prepared-cleanup-append.json').read_bytes();public=json.loads((R/'actual-public-result.json').read_bytes())
assert public['result']=='PASS' and public['receipt']==ident(receipt) and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
assert json.loads((R/'validated-receipt-identity.json').read_bytes())==ident(receipt)
review=json.loads((T/'review/CHECKPOINT.json').read_bytes())
assert review['target_identity']=={'bytes':155659416,'sha256':'14bfe3fcc3da3f5f8e2ab6cfb3c820229f1520b439b9ebaf5f6bad83daf25c50'}
changes=json.loads((B/'overlay/ec01/provenance/changed-files.json').read_bytes())
for n,c in changes['intentional_existing_file_changes'].items():
 assert ident((B/'overlay'/n).read_bytes())==c['after']
 assert ident((B/'overlay/ec01/original'/n).read_bytes())==c['before']
om=json.loads((B/'OVERLAY-MANIFEST.json').read_bytes())
assert set(om)=={p.relative_to(B/'overlay').as_posix() for p in (B/'overlay').rglob('*') if p.is_file()}
for n,pin in om.items():assert ident((B/'overlay'/n).read_bytes())==pin,n
for tree in ('results','processes','failures'):
 source=T/tree
 if source.exists():
  for p in sorted(source.rglob('*')):
   if p.is_file():copy_file(p,B/'new'/tree/p.relative_to(source))
for n in ('recovery.stdout','recovery.stderr'):
 copy_file(T/n,B/'new/recovery'/n)
copy_file(Path(__file__),B/'tools/package.py')
new={'status':'AUTHOR FOCUSED CORRECTION CHECKS COMPLETED; INDEPENDENT CLOSURE PENDING','group':name,'controls':result['checks'],'row_types':dict(collections.Counter(x['result'] for x in rows)),'layers':dict(collections.Counter(x['layer'] for x in rows)),'stdout_progress_RESULT_reconciled':True,'supervisor_observed_stream_sizes_match':True,'exit':ex,'environment':result['environment'],'result_identity':ident((R/'RESULT.json').read_bytes()),'actual_monitored_call_counts':counts,'full_public_negative_derivations':0}
results={'checkpoint':'I164-EC01-terminal-exception-correction-1','author':'SU-Engineering[288D]','independent_closure':'PENDING','scope':'EC-01 only: pending exception remains True after normal selected close/append; None frontiers and replacement semantics retained','new_focused_group':new,'new_receipt':{'path':'overlay/ec01/receipts/prepared-cleanup-append.json','identity':ident(receipt),'prepared_separately':True,'actual_public_validation':public,'preparation_record_remains_historical':True},'intentional_changes':changes,'historical_review_verdict_unchanged':review['verdict'],'historical_review_finding_unchanged':review['finding'],'historical_independent_groups_separate':review['fresh_independent_groups_separate'],'historical_Engineering_groups_separate':review['engineering_separate'],'unqualified_combined_total':None,'source_consistent_historical_rejections':'EC-01 defect evidence, not protective rejection support','historical_missing_records_reconstructed':False,'confirmed_save_reused':review['confirmed_save_reused'],'limits':review['limits'],'preservation':{**review['preservation'],'candidate_implementation':'Only EC-01 declared changes; runtime and predecessor unchanged'},'operations':{'requests':0,'acquisitions':0,'database_connections':0,'session_operations':0,'Git_saves':0,'completed_campaign_replays':0,'runtime_changes':0,'new_full_public_positive_processes':1}}
results['previous_bounded_source_support_carried_forward_unchanged']=review['previous_bounded_source_support_carried_forward_unchanged']
results['prior_LD01_closure_reused']=review['prior_LD01_closure_reused']
(B/'RESULTS.json').write_bytes(enc(results))
(B/'START-HERE.txt').write_text('Active EC-01 correction. Read README.txt, RESULTS.json and RECOVERY.txt. Retained review verdict NOT ACCEPTED AS COMPLETE — EC-01 stays historical. Independent closure is pending. Use tools/recover.py only for byte reconstruction; it does not validate. New active receipt is ec01/receipts/prepared-cleanup-append.json in the recovered root, validated by the saved new focused group. Original receipts, missing records and failures stay unchanged. No completed work replay authorized.\n')
print('2/4 Declare every checkpoint file, including exact retained review and correction overlay',flush=True)
files=sorted(p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file());assert 'MANIFEST.json' not in files
for n in files:assert not n.startswith('/') and '..' not in Path(n).parts and stat.S_ISREG((B/n).lstat().st_mode)
manifest={n:ident((B/n).read_bytes()) for n in files};(B/'MANIFEST.json').write_bytes(enc(manifest));files=['MANIFEST.json',*files]
out=T.parent/'I164-EC01-terminal-exception-correction-1.zip'
print('3/4 Create the checkpoint archive',flush=True)
with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in files:
  zi=zipfile.ZipInfo(n);zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,(B/n).read_bytes())
print('4/4 Verify exact safe membership, CRC and all manifested bytes',flush=True)
with zipfile.ZipFile(out) as z:
 assert z.namelist()==files and len(set(files))==len(files) and z.testzip() is None
 for n,p in manifest.items():assert ident(z.read(n))==p,n
identity={'filename':out.name,**ident(out.read_bytes()),'entries':len(files),'manifested_files':len(manifest),'CRC':'PASS','membership':'PASS','all_manifested_hashes':'PASS','new_completed_controls':result['checks'],'historical_totals_not_combined':True,'independent_closure':'PENDING'}
(T/'CHECKPOINT-IDENTITY.json').write_bytes(enc(identity));(T/'TASK-STATE.json').write_bytes(enc({'status':'VERIFIED_CHECKPOINT_READY_TO_SAVE','identity':identity}));print(json.dumps(identity,indent=2),flush=True)
