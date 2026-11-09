"""Continue after the preserved declared-function-count mismatch; no recovery replay."""
from review_bytes import HERE,read,save,fid,ident
import ast
root=HERE/'candidate';lookup=root/'retained/lookup';host=HERE/'host';prior=HERE/'prior-review/context-lookup-review'
old=(lookup/'code/managed_coverage.py').read_bytes();new=(root/'code/managed_coverage.py').read_bytes()
assert new.startswith(old) and len(old)==429112
funcs=[n.name for n in ast.parse(new[len(old):]).body if isinstance(n,ast.FunctionDef)]
assert funcs==['compile_enter_call','validate_enter_call','enter_call_binding','enter_call_projection','validate_enter_call_projection']
save(HERE/'recovery-audit.exit.json',{'exit':1,'observed_by':'exec process session 20687 exit status plus saved traceback','stage':'read-only appended-function count assertion after all three root manifest comparisons','candidate_controls':0,'byte_recovery_child':read(HERE/'byte-recovery-exit.json'),'failure':'CHANGES.json declares six appended functions; source has five','raw_stderr':fid(HERE/'recovery-audit.stderr'),'script':fid(HERE/'recover_candidate.py'),'disposition':'Original failure retained. Continue remaining byte inspections only, no recovery replay.'})
for n in ('managed_coverage.py','correspondence.py'):assert (root/'reference/lookup/code'/n).read_bytes()==(lookup/'code'/n).read_bytes()
assert (root/'source-evidence/lab_bootstrap.py').read_bytes()==(lookup/'source-evidence/lab_bootstrap.py').read_bytes()
for n in ('bytecodes.c','typeobject.c','compound_stmts.rst','LICENSE'):assert (root/'reference/cpython-3.12.14'/n).read_bytes()==(lookup/'reference/cpython-3.12.14'/n).read_bytes()
for n,pin in read(root/'provenance/component-pins.json').items():assert fid(root/n)==pin,n
for v in read(root/'CHANGES.json')['intentional_candidate_changes']:
    assert fid(root/v['path'])==v['after'] and fid(lookup/v['path'])==v['before'],v['path']
for p in (host/'observer-reference').iterdir():assert p.read_bytes()==(HERE/'recovered-helper/harness'/p.name).read_bytes(),p.name
for p in (root/'reference/review').iterdir():assert p.read_bytes()==(prior/p.name).read_bytes(),p.name
save(HERE/'source-byte-audit.json',{'status':'PASS with documentation-count discrepancy','producer_prefix':ident(old),'new_producer':ident(new),'appended_bytes':len(new)-len(old),'appended_functions':funcs,'new_adapter':fid(root/'code/correspondence.py'),'prior_adapter':fid(lookup/'code/correspondence.py'),'runtime_interpreter_and_prior_sources':'exact unchanged bytes','prior_review_excerpts':'exact verified prior review members','six_observer_files':'exact unchanged','documentation_witness':{'file':'source/CHANGES.json','claim':'append six new pure-source functions; entire predecessor prefix retained','actual_functions':funcs,'count':5,'minimal_reproduction':'ast.parse(current_producer_bytes[429112:]) -> five top-level FunctionDef names','implementation_defect':False},'root_audit':'original recovery audit passed all three exact tree comparisons before stopping at documentation count; final post-control verification will be saved separately','candidate_execution':0})
save(HERE/'finish-byte-audit.exit.json',{'exit':0,'failure':None,'earlier_failure_preserved':True})
print({'source_bytes':'verified','functions':funcs,'previous_recovery_replayed':False},flush=True)
