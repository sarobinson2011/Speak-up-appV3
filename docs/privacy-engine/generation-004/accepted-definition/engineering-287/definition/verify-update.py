"""Fresh documentary checks; writes only this candidate's verification reports."""
from pathlib import Path
import csv,json,hashlib,runpy,io,contextlib
O=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(O/'verify-candidate.py'),run_name='__main__')
with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(O/'privacy/regenerate_declared_model.py'),run_name='__main__')
module=runpy.run_path(str(O/'privacy/observation_correlation.py'));vectors=module['test_vectors']()
def rr(p):return list(csv.DictReader((O/p).open(),delimiter='\t'))
fields=rr('profile/fragments/fields.tsv');ops=rr('profile/fragments/operations.tsv');defs=rr('profile/fragments/definitions.tsv');nodes=rr('privacy/model/nodes.tsv');edges=rr('privacy/model/structural-edges.tsv');coverage=rr('privacy/model/field-coverage.tsv');syntax=rr('privacy/model/expression-syntax.tsv');entry=json.loads((O/'profile/fragments/entry.json').read_text())
ns={r['node_id']:r for r in nodes};assert len(ns)==len(nodes)==3040
assert len(edges)==9516 and len({tuple(r.values()) for r in edges})==len(edges)
assert all(r['from_node'] in ns and r['to_node'] in ns for r in edges)
assert len(fields)==len(coverage)==118 and len(entry['root_fields'])==94
assert {r['field_id'] for r in coverage}=={r['field_id'] for r in fields}
for f in fields:
 assert 'FIELD:'+f['field_id'] in ns
 assert sum(n.startswith('READ-META:'+f['field_id']+':') for n in ns)==9
for op in ops:assert 'OP:'+op['operation_id'] in ns
for d in defs:assert 'DEF:'+d['definition_id'] in ns
assert len(ops)==93 and len(defs)==60 and len(syntax)==978
assert len([x for x in nodes if x['kind']=='PUBLIC-RELATIONSHIP-EVIDENCE'])==21
assert len([x for x in nodes if x['kind']=='PROGRAM-FIELD'])==118
assert len([x for x in nodes if x['kind']=='READ-OBJECT-METADATA'])==1062
assert len([x for x in nodes if x['kind']=='PROPOSED-PRODUCER-WORK'])==32
assert len([x for x in nodes if x['kind']=='PROPOSED-EVIDENCE-FIELD'])==174
for name in ('n','a','r'):
 assert ns['PUBLIC-PI:'+name]['declared_exposure']=='PUBLIC' and ns['PUBLIC-PI:'+name]['reuse']=='NONE'
assert entry['groups']==[]
for r in json.loads((O/'privacy/model/manifest.json').read_text()):assert hashlib.sha256((O/r['path']).read_bytes()).hexdigest()==r['sha256']
inv=rr('composition/source-inventory.tsv');s83=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S83')
assert hashlib.sha256((O/s83['path']).read_bytes()).hexdigest()==s83['sha256']
s84=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S84')
assert hashlib.sha256((O/s84['path']).read_bytes()).hexdigest()==s84['sha256']
assert (O/'privacy/observation_correlation.py').read_text() in (O/s84['path']).read_text()
assert (O/'privacy/regenerate_declared_model.py').read_text() in (O/s84['path']).read_text()
req=json.loads((O/'composition/requirement-inventory.json').read_text());assert len(req)==972 and [r['requirement_id'] for r in req[931:936]]==[f'PE-G4-CAP-{i:03}' for i in range(71,76)]
assert [r['requirement_id'] for r in req[936:941]]==[f'PE-G4-CAP-{i:03}' for i in range(76,81)]
root=next(v for v in vectors if v['case']=='same public root across distinct contexts')
assert root['earliest_failure']=='UNIQUENESS-FAILURE' and 'CORRELATION-FAILURE' in root['failures']
assert next(v for v in vectors if v['case']=='hidden actor bridge still fails')['earliest_failure']=='ACTOR-RECONSTRUCTION-RISK'
assert next(v for v in vectors if v['case']=='constant exception never filters actor graph')['earliest_failure']=='ACTOR-RECONSTRUCTION-RISK'
with contextlib.redirect_stdout(io.StringIO()):relationship_results=runpy.run_path(str(O/'privacy/test_public_relationships.py'))['results']
assert len(relationship_results)==21
report={'author_checks':'PASS','scope':'Approved correlation integration and declared static model only','fields_covered':118,'root_inputs_covered':94,'read_metadata_cells':1062,'operation_nodes':93,'definition_nodes':60,'expression_nodes':978,'node_templates':3040,'structural_edge_templates':9516,'unresolved_producer_clauses':len(rr('privacy/model/unresolved-producer-conditions.tsv')),'graph_vectors':vectors,'source_appointed':False,'privacy_admitted':False,'full_equality_graph_instantiated':False,'source_complete_producer_observer_model':False,'public_relationship_permissions':['SAME-SCOPED-ROOT','SAME-SCOPED-A','SAME-SCOPED-A-N'], 'relationship_vectors':relationship_results,'publication_performed':False,'historical_constructor_executed':False}
(O/'verification/correlation-integration.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — approved G4 correlation source and all 118 field surfaces verified.')
print('PASS — 12 bounded graph vectors; complete actor-edge protection retained.')
print('PASS — 21 scoped relationship vectors; approved root, action and duplicate cases pass.')
print('PASS — cross-action nullifier links and actor-reconstruction paths remain rejected.')
runpy.run_path(str(O/'coordinates/verify_coordinates.py'),run_name='__main__')
runpy.run_path(str(O/'producer/verify_producer.py'),run_name='__main__')
runpy.run_path(str(O/'producer/test_evidence_carrier.py'),run_name='__main__')
runpy.run_path(str(O/'privacy/verify_expansion.py'),run_name='__main__')
with contextlib.redirect_stdout(io.StringIO()):runpy.run_path(str(O/'privacy/test_cross_role_correction.py'),run_name='__main__')
print('PASS — 14 retained correlation correction vectors.')
runpy.run_path(str(O/'privacy/test_cross_role_uniqueness.py'),run_name='__main__')
print('No profile admission, publication, repository edit or historical constructor execution.')

assert [r['requirement_id'] for r in req[941:945]]==[f'PE-G4-CAP-{i:03}' for i in range(81,85)]
s86=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S86')
assert (O/'privacy/cross_role_correlation.py').read_text() in (O/s86['path']).read_text()

assert [r['requirement_id'] for r in req[945:948]]==[f'PE-G4-CAP-{i:03}' for i in range(85,88)]
s87=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S87')
assert (O/'privacy/cross_role_uniqueness.py').read_text() in (O/s87['path']).read_text()

assert [r['requirement_id'] for r in req[948:951]]==[f'PE-G4-CAP-{i:03}' for i in range(88,91)]
s88=next(r for r in inv if r['source_id']=='PE-G4-SOURCE-S88')
for name in ['assemble_members.py','privacy_member.py','evidence_auth.py']:assert (O/'profile/integration'/name).read_text() in (O/s88['path']).read_text()
runpy.run_path(str(O/'profile/integration/test_members.py'),run_name='__main__')
runpy.run_path(str(O/'profile/integration/test_evidence_auth.py'),run_name='__main__')
runpy.run_path(str(O/'profile/integration/test_admission.py'),run_name='__main__')
runpy.run_path(str(O/'profile/integration/check_static_obstruction.py'),run_name='__main__')

runpy.run_path(str(O/'privacy/relation-aware/test_rule.py'),run_name='__main__')

runpy.run_path(str(O/'privacy/relation-aware/test_integration.py'),run_name='__main__')

runpy.run_path(str(O/'definition-completion/verify_completion.py'),run_name='__main__')
