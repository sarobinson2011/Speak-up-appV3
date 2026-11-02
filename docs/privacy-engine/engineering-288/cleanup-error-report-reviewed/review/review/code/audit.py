"""Read-only record/source reconciliation. Zero candidate/control replays."""
from pathlib import Path
import sys,json,re,ast,collections
sys.path.insert(0,str(Path(__file__).parent))
from intake import AREA,BASE,identity,enc,js
def main():
 p=AREA/'package';root=AREA/'recovered';decl=js((p/'RESULTS.json').read_bytes());res=js((p/'new/results/focused-recovered/RESULT.json').read_bytes());rows=res['rows'];progress=[js(x) for x in (p/'new/results/focused-recovered/progress.jsonl').read_bytes().splitlines()]
 stdout=[s for s in (p/'new/processes/focused-recovered/stdout.log').read_text().splitlines() if re.match(r'^\d+ ',s)]
 assert len(rows)==len(stdout)==392 and len(progress)==391 and rows[:391]==progress
 for i,(row,line) in enumerate(zip(rows,stdout),1):assert line==f"{i} {row['check']} {row['result']}"
 kinds=dict(collections.Counter(x['result'] for x in rows));pkinds=dict(collections.Counter(x['result'] for x in progress));assert kinds=={'PASS':130,'REJECTED':262} and pkinds=={'PASS':129,'REJECTED':262}
 assert rows[-1]['check']=='returned context mutations leave both expected contexts intact' and rows[-1]['result']=='PASS'
 ex=js((p/'new/processes/focused-recovered/exit-status.json').read_bytes());assert ex['returncode']==0 and not ex['timed_out']
 reconciliation=js((p/'new/provenance/final-accounting-reconciliation.json').read_bytes())
 for n,pin in reconciliation['recorded_identities'].items():assert identity((p/'new'/n).read_bytes())==pin
 retention=js((p/'new/failures/byte-recovery/retention.json').read_bytes())
 for item in retention:assert identity((p/'new'/item['retained_copy']).read_bytes())==item['identity'] and {k:item['original'][k] for k in ('bytes','sha256')}==item['identity']
 assert js((p/'new/failures/packaging-reconciliation/exit-status.json').read_bytes())['returncode']==1
 historic=js((AREA/'prior-closure/CHECKPOINT.json').read_bytes());inc=js((p/'new/provenance/review-and-save-incorporation.json').read_bytes())
 assert historic['fresh_independent']==inc['independent_EC01_controls']
 assert historic['historical_Engineering_separate']==inc['historical_Engineering'] and historic['historical_independent_separate']==inc['historical_independent']
 host=(p/'new/intake/SEND-TO-ANCHOR-git-exceptional-cleanup-EC01.json').read_bytes();assert identity(host)==inc['host_save_receipt'] and b'c2fb30a1a427db2a1066df4d40e17574fa51bcbf' in host
 old=(root/'retained/cleanup/code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes();addition=(p/'new/code/producer-addition.py').read_bytes();assert new==old+addition
 oldtree=ast.parse(old);added=ast.parse(addition);oldnames={n.name for n in oldtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};assert all(isinstance(n,ast.FunctionDef) and n.name not in oldnames for n in added.body)
 class Normalize(ast.NodeTransformer):
  def visit_Constant(self,node):
   if type(node.value) is int and node.value in (3,4):node.value='MONITORING-SLOT'
   elif type(node.value) is str:
    if node.value.startswith(('REPORT-','CLEANUP-')):node.value=node.value.split('-',1)[1]
    elif node.value.endswith('authenticated-predecessor:'):node.value='LEASE-MARKER'
   return node
 helpers=[]
 for n in ('code/correspondence.py','retained/cleanup/code/correspondence.py'):
  t=ast.parse((root/n).read_bytes());f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');helpers.append(ast.dump(Normalize().visit(f),include_attributes=False))
 assert helpers[0]==helpers[1]
 receipt=(root/'receipts/prepared-error-report.json').read_bytes();assert identity(receipt)==decl['current_receipt'];prep=js((root/'provenance/receipt-preparation.json').read_bytes());assert prep['receipt']==identity(receipt) and prep['public_validator_calls']==prep['predecessor_validator_calls']==0
 evidence={'kind':'Read-only record/source audit; no controls or candidate execution','supplied':{'RESULT_stdout_rows':392,'progress_rows':391,'RESULT_stdout_kinds':kinds,'progress_kinds':pkinds,'row392':rows[-1],'row392_progress':'UNAVAILABLE','cause':'UNKNOWN','no_reconstruction':True,'exit':ex,'layers':dict(collections.Counter(x['layer'] for x in rows))},'new_supplied_failures':{'byte_recovery':decl['new_preparation_failure'],'packaging':reconciliation,'undeclared_copies_verified':retention},'historical':inc,'prior_closure':historic['verdict'],'producer_append_only':True,'new_functions':[n.name for n in added.body],'slot4_helper_same_AST_as_retained_slot3_except_slot_error_labels_lease_marker':True,'prepared_receipt':identity(receipt),'preparation_is_validation':False,'host_save_receipt':identity(host),'Git_operations':0}
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);(out/'AUDIT.json').write_bytes(enc(evidence));print(json.dumps({'status':'PASS','controls':0,'candidate_executions':0,'supplied_rows':392,'missing_progress_row':392,'cause':'UNKNOWN','output':str(out/'AUDIT.json')}),flush=True)
if __name__=='__main__':main()
