"""Read-only audit of source changes and supplied records. No control replay."""
from pathlib import Path
import sys,ast,zipfile,json,re,collections,traceback
sys.path.insert(0,str(Path(__file__).parent))
from intake import AREA,identity,enc,js,verify_root
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
pkg=AREA/'package';root=AREA/'recovered';prior=AREA/'prior-review'
def record(p):return js(p.read_bytes())
def stream_rows(p):return [js(s) for s in p.read_bytes().splitlines() if s]
def numbered(p):
 rows=[]
 for s in p.read_text().splitlines():
  m=re.fullmatch(r'(\d+) (.*) (PASS|REJECTED|DEFECT-OBSERVED)',s)
  if m:rows.append((int(m[1]),{'check':m[2],'result':m[3]}))
 assert [n for n,_ in rows]==list(range(1,len(rows)+1));return [x for _,x in rows]
try:
 result=record(pkg/'new/results/focused-recovered/RESULT.json');progress=stream_rows(pkg/'new/results/focused-recovered/progress.jsonl');stdout=numbered(pkg/'new/processes/focused-recovered/stdout.log');exit=record(pkg/'new/processes/focused-recovered/exit-status.json')
 assert result['rows']==progress and len(progress)==105 and stdout==[{k:r[k] for k in ('check','result')} for r in progress]
 assert dict(collections.Counter(r['result'] for r in progress))=={'PASS':55,'REJECTED':50} and exit['returncode']==0 and exit['timed_out'] is False and result['error'] is None
 supplied={'controls':105,'PASS':55,'REJECTED':50,'exit':exit,'result_identity':identity((pkg/'new/results/focused-recovered/RESULT.json').read_bytes()),'layer_counts':dict(collections.Counter(r['layer'] for r in progress)),'rows_stdout_result_reconciled':True,'new_execution_calls':0}
 # Verify original review's groups and status, not just the correction's summary.
 oldreview=record(prior/'CHECKPOINT.json');assert oldreview['verdict'].startswith('NOT ACCEPTED AS COMPLETE')
 oldgroups={}
 for label in ('source-slot3','source-completion','public-recovered'):
  p=prior/'review/results'/label;res=record(p/'RESULT.json');rows=stream_rows(p/'progress.jsonl');text=numbered(prior/'review/processes'/label/'stdout.log');assert rows==res['rows'] and len(rows)==res['checks'] and text==[{k:r[k] for k in ('check','result')} for r in rows]
  oldgroups[label]={'result':res['result'],'rows':len(rows),'kinds':dict(collections.Counter(r['result'] for r in rows))),'exit':record(prior/'review/processes'/label/'exit-status.json')}
 assert oldgroups['source-slot3']['rows']==50 and oldgroups['source-slot3']['exit']['returncode']==1 and oldgroups['source-completion']['rows']==21 and oldgroups['public-recovered']['rows']==170 and oldgroups['public-recovered']['kinds']['DEFECT-OBSERVED']==4
 oldengineering={}
 for label,total in (('source-1',46),('recovered',341),('primary',1300)):
  p=root/'results'/label;rows=stream_rows(p/'progress.jsonl');text=numbered(root/'processes'/label/'stdout.log');assert len(rows)==total and text==[{k:r[k] for k in ('check','result')} for r in rows[:len(text)]]
  if label=='primary':
   assert len(text)==165 and all(not (p/n).exists() for n in ('RESULT.json','calls.json','final-verification.json'));ex=record(root/'processes'/label/'exit-status.json');assert ex['returncode']==-15 and ex['timed_out'] is True
  else:assert record(p/'RESULT.json')['rows']==rows and len(text)==total
  oldengineering[label]={'progress':len(rows),'stdout':len(text),'completed':label!='primary','discrepancy_cause':'UNKNOWN' if label=='primary' else None}
 # Exact original manifest bytes and three carried independent factory identities.
 with zipfile.ZipFile(prior/'input/I164-exceptional-cleanup-append-correspondence-1.zip') as z:assert z.read('MANIFEST.json')==(root/'ec01/original/MANIFEST.json').read_bytes()
 for n in ('cases.py','parent_cases.py','parent_details.py'):assert (Path(__file__).parent/n).read_bytes()==(prior/'review/code'/n).read_bytes()
 olda=ast.parse((root/'ec01/original/code/correspondence.py').read_bytes());newa=ast.parse((root/'code/correspondence.py').read_bytes());oldfun={n.name:ast.dump(n,include_attributes=True) for n in olda.body if isinstance(n,ast.FunctionDef)};newfun={n.name:ast.dump(n,include_attributes=True) for n in newa.body if isinstance(n,ast.FunctionDef)};assert oldfun==newfun
 producer=ast.parse((root/'code/managed_coverage.py').read_bytes());fun=next(n for n in producer.body if isinstance(n,ast.FunctionDef) and n.name=='cleanup_append_projection');ret=fun.body[-1];flag=next(v for k,v in zip(ret.value.keys,ret.value.values) if isinstance(k,ast.Constant) and k.value=='terminal_python_exception_in_model')
 assert ast.unparse(flag)=="None if terminal in ('process-termination', 'unobserved') else True"
 launcher=(root/'source-evidence/lab_bootstrap.py').read_text().splitlines();source='\n'.join(launcher[166:171]);assert 'except BaseException as e:' in source and "details['cleanup'].append([name,'close returned'])" in source
 oldpin=record(root/'ec01/provenance/prepared-receipt.json');assert identity((root/oldpin['new_receipt_path']).read_bytes())==oldpin['new_receipt'] and identity((root/oldpin['historical_receipt_path']).read_bytes())==oldpin['historical_receipt']
 assert record(pkg/'RESULTS.json')['confirmed_save_reused']=='c43954ff5ee384c6fb6e7a85d83eb36bfea342d1'
 audit={'kind':'Read-only source, preservation and supplied-record audit','validator_projector_calls':0,'supplied':supplied,'historical_independent_separate':oldgroups,'historical_Engineering_separate':oldengineering,'zero_control_audit_failure_and_correction':oldreview['fresh_independent_groups_separate']['audit']|{'correction':oldreview['fresh_independent_groups_separate']['audit-completion']},'historical_verdict':oldreview['verdict'],'original_manifest_bytes_exact':True,'all_adapter_function_bodies_and_locations_unchanged':True,'independent_factory_reuse_byte_exact':True,'corrected_expression':ast.unparse(flag),'source_167_171':source,'author_oracle_executed':False,'historical_missing_records_reconstructed':False,'root':verify_root(root),'prior_LD01_closure_reused':True,'new_controls':0,'new_Git_save':False}
 (out/'AUDIT.json').write_bytes(enc(audit));print(json.dumps({'result':'PASS','supplied':'105 = 55 PASS + 50 REJECTED','old_primary':'1300 progress / 165 stdout, incomplete','new_validator_calls':0}),flush=True)
except BaseException:
 (out/'failure.txt').write_text(traceback.format_exc());raise
