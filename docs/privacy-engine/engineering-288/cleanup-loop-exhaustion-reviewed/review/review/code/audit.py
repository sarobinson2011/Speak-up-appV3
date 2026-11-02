"""Read-only evidence and preservation audit. Zero candidate/control executions."""
from pathlib import Path
import ast,json,collections,sys
sys.path.insert(0,str(Path(__file__).parent))
from intake import AREA,identity,enc,js
def main():
 p=AREA/'package';root=AREA/'recovered';decl=js((p/'CHECKPOINT.json').read_bytes())
 result=js((p/'new/results/focused-recovered/RESULT.json').read_bytes());rows=result['rows']
 progress=[js(line) for line in (p/'new/results/focused-recovered/progress.jsonl').read_bytes().splitlines()]
 stdout=[js(line[6:]) for line in (p/'new/processes/focused-recovered/stdout.log').read_bytes().splitlines() if line.startswith(b'CHECK ')]
 assert len(rows)==722 and len(progress)==len(stdout)==721
 assert [x['ordinal'] for x in rows]==list(range(1,723))
 assert progress==stdout==[x for x in rows if x['ordinal']!=134]
 assert rows[133]=={'ordinal':134,'check':'frontier 0-False-append inner-handler-departure-attempt unobserved','result':'PASS','layer':'authenticated-basis producer output-comparison core with validated parent + independent oracle'}
 kinds=lambda xs:dict(collections.Counter(x['result'] for x in xs))
 assert kinds(rows)=={'PASS':232,'REJECTED':490} and kinds(progress)=={'PASS':231,'REJECTED':490}
 ex=js((p/'new/processes/focused-recovered/exit-status.json').read_bytes());assert ex['returncode']==0 and ex['timed_out'] is False
 reconciled=js((p/'new/provenance/new-record-reconciliation.json').read_bytes());assert decl['new_records']==reconciled
 frozen={n:identity((p/'new/processes/focused-recovered'/n).read_bytes()) for n in ('stdout.log','stderr.log')}
 old=(root/'retained/report/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes();added=(p/'new/code/producer-addition.py').read_bytes()
 assert len(old)==359095 and new==old+added
 oldtree=ast.parse(old);addition=ast.parse(added);names={n.name for n in oldtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 assert all(isinstance(n,ast.FunctionDef) and n.name not in names for n in addition.body)
 class Normalize(ast.NodeTransformer):
  def visit_Constant(self,node):
   if type(node.value) is int and node.value in (4,5):node.value='SLOT'
   elif type(node.value) is str:
    if node.value.startswith(('LOOP-','REPORT-')):node.value=node.value.split('-',1)[1]
    elif node.value.endswith('authenticated-predecessor:'):node.value='LEASE'
   return node
 helpers=[]
 for name in ('code/correspondence.py','retained/report/code/correspondence.py'):
  f=next(n for n in ast.parse((root/name).read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');helpers.append(ast.dump(Normalize().visit(f),include_attributes=False))
 assert helpers[0]==helpers[1]
 fresh=js((root/'receipts/prepared-cleanup-loop.json').read_bytes());previous=js((root/'retained/report/receipts/prepared-error-report.json').read_bytes())
 restored=json.loads(json.dumps(fresh));restored['format']=previous['format'];restored['extension_components']=restored.pop('prior_error_report_components');restored.pop('prior_error_report_receipt');restored.pop('new_cleanup_loop_limits')
 for row in restored['contexts']:row.pop('cleanup_loop_exhaustion_correspondence')
 assert restored==previous
 assert fresh['prior_error_report_receipt']==identity((root/'retained/report/receipts/prepared-error-report.json').read_bytes())
 for n,pin in fresh['extension_components'].items():assert identity((root/'code'/n).read_bytes())==pin
 preparation=js((p/'new/provenance/receipt-preparation.json').read_bytes())
 assert preparation['receipt']==identity((root/'receipts/prepared-cleanup-loop.json').read_bytes())
 host=(p/'new/intake/confirmed-line172-git-receipt.json').read_bytes();h=js(host)
 assert h['commit']==h['remote_main']=='5ffd368df1012296a128c2dde134149d341780bc' and h['status']=='PASS'
 prior=js((p/'new/intake/line172-review-CHECKPOINT.json').read_bytes())
 # Preserved bytes and existing record status are evidence continuity, not reruns.
 audit={'kind':'Read-only preservation/record audit; zero candidate execution and zero completed-campaign replays','supplied':{'RESULT_rows':722,'progress_rows':721,'stdout_rows':721,'RESULT_kinds':kinds(rows),'corroborated_kinds':kinds(progress),'missing_progress_stdout_row':rows[133],'cause':'UNKNOWN','exit':ex,'frozen_stream_identities':frozen,'supervisor_stream_byte_observations':ex.get('streams_bytes_observed'),'different_byte_observations_preserved':True,'no_reconstruction':True,'layers':dict(collections.Counter(x['layer'] for x in rows))},'prior_qualified_records':{k:decl[k] for k in ('prior_independent_accounting','prior_slot4_failed_attempt','prior_Engineering_accounting','older_qualifications')},'prior_review_checkpoint_identity':identity((p/'new/intake/line172-review-CHECKPOINT.json').read_bytes()),'producer_prefix_unchanged_bytes':359095,'old_named_definitions_preserved':len(names),'new_function_names':[n.name for n in addition.body],'slot5_helper_AST_equivalent_to_reviewed_slot4_except_slot_labels_marker':True,'new_receipt_restores_exact_inherited_JSON':True,'preparation_is_validation':False,'new_receipt':preparation['receipt'],'preserved_host_receipt':identity(host),'confirmed_save_reused_only':'5ffd368df1012296a128c2dde134149d341780bc','Git_operations':0,'document_wording_qualification':{'field':'CHECKPOINT.json /monitoring','exact_text':decl['monitoring'],'reading':'This sentence does not establish qualification of cleanup failure, repeated interruption, termination, hostile replacement or alternate interpreters. README/RECOVERY and retained qualified observations govern the scoped review.'}}
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'AUDIT.json').write_bytes(enc(audit))
 print(json.dumps({'status':'PASS','controls':0,'candidate_executions':0,'supplied_RESULT':722,'supplied_corroborated':721,'missing_row':134,'frozen_stdout_bytes':frozen['stdout.log']['bytes'],'supervisor_stdout_bytes':ex.get('streams_bytes_observed',{}).get('stdout.log'),'cause':'UNKNOWN','output':str(out/'AUDIT.json')}),flush=True)
if __name__=='__main__':main()
