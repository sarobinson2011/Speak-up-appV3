"""Finalize exact metadata joins; no stream computation."""
from pathlib import Path
import json,hashlib,copy
from bind_ledger import check_binding
R=Path(__file__).resolve().parents[1]
def L(n):return json.loads((R/n).read_bytes())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def S(n,x):(R/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
i=L('candidate/identity.json');b=L('candidate/ledger/binding.json');v=L('results/expanded-verification.json');profile=L('candidate/profile-binding.json');checks=[]
assert check_binding(b,i,H(R/'records/expanded-contract.json'));checks.append('actual candidate ledger joins')
for key,value in [('model_sha256','0'*64),('contract_sha256','0'*64),('qualification_established',True),('textual_stream_sha256','0'*64)]:
 bad=copy.deepcopy(b);bad[key]=value
 try:check_binding(bad,i,H(R/'records/expanded-contract.json'))
 except ValueError:checks.append('reject '+key)
 else:raise AssertionError(key)
assert v['saved_model']['all_inherited_array_prefixes_exact'] and v['saved_model']['appended_saved_bytes_exact'];checks.append('historical arrays preserved')
assert profile['relationships_43_sha256']==H(R/'retained/mapping/records/relationships-43.json');checks.append('43 relationships identity preserved')
fields=L('records/added-fields.json');schemas={}
for f in fields:
 if f['record'] in schemas:assert schemas[f['record']]['slots']==f['slots']
 else:schemas[f['record']]={'slots':f['slots'],'field_classes':0}
 schemas[f['record']]['field_classes']+=1
for name in ['LOG','PAYLOAD','RECORD','BLOB']:assert schemas['EXECUTOR-'+name]['slots']==256
checks.append('all lifecycle repetition bounds retained')
S('records/complete-repetition-table.json',schemas)
S('results/final-bindings.json',{'result':'PASS-EXACT-FINAL-BINDINGS','checks':checks,'count':len(checks),'actual_admission':False})
pre=L('results/expansion-preflight.json')
delta={'parent_model_sha256':profile['parent_model_sha256'],'candidate_model_sha256':i['model_sha256'],'candidate_canonical_bytes':i['model_bytes'],'candidate_transport':{'file':'candidate/model.json.gz','bytes':i['compressed_bytes'],'sha256':i['compressed_sha256']},'arrays':{'surfaces':{'old':44167,'new':pre['surface_count']},'relations':{'old':61415,'new':pre['relation_count']},'tokens':{'old':4510432,'new':i['tokens']},'structural_edges':{'old':8439026,'new':i['structural_edges']}},'exact_unchanged_array_prefixes':True,'changed_model_fields':['surfaces appended','relations appended','tokens appended','structural_edges appended','equality_stream.rows','equality_stream.bytes'],'unchanged_model_fields':['actor_graph_policy','equality_stream.format','equality_stream.predicate','equality_stream.ordering','equality_stream.row_encoding','equality_stream.sha256 remains null'],'new_contract_sha256':b['contract_sha256'],'equality_stream':i['equality_stream'],'textual_stream_sha256':None,'dependent_updates':['expanded finite contract','field/occurrence directories','relation rules','token index','mechanical ledger','profile procedure and authority bindings'],'historical_signatures_and_receipts':'not rebound or relabelled','actual_admission':False}
S('records/candidate-delta.json',delta)
results=['accounting.json','metadata-tests.json','segment-recovery.json','facade.json','producer-accounting.json','final-bindings.json']
counts={n:(L('results/'+n).get('count') or L('results/'+n).get('checks')) for n in results}
S('results/COMPLETION.json',{'result':'COMPLETE-DECLARED-CONDITIONAL-MECHANICAL-MAPPING','four_tasks':{'repetition_coverage':'COMPLETE','expanded_arrays':'COMPLETE','exact_saved_model_identity':'VERIFIED','inherited_mechanical_ledger_rebinding':'COMPLETE'},'model_sha256':i['model_sha256'],'new_focused_checks':counts,'tests_total':sum(counts.values()),'reused_checks':{'directory':35,'repetition_witness':12,'observer_and_kernel':'retained results; not rerun'},'complete_token_directory':i['tokens'],'complete_structural_array':i['structural_edges'],'independent_added_structural_validation':v['structural'],'owning_profile_mapping_verdict':'Complete for the declared bounded conditional profile and adopted shared-accounting interpretation; no claim of qualified scope completeness or operational readiness.','remaining_code_defects_demonstrated':[],'remaining_evidence':['genuine authenticated occurrence inputs and required phases','independent source/model/assessor qualification and appointments','qualified obligation classifications/dispositions/budgets/non-vacuity','rollback-resistant authority and key/finality/custody operational assurances','changed candidate equality and textual stream identities','final full-model witness and required authentication'], 'full_stream_processed':False,'prospective_occurrence':False,'qualification_established':False,'actual_admission':False})
print(json.dumps({'result':'PASS-FINAL-BINDINGS','checks':len(checks),'model_sha256':i['model_sha256']}))
