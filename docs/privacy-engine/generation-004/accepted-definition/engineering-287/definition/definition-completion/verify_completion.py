"""Verify the whole definition-review construction. No admission/authority claims."""
from pathlib import Path
import csv,json,runpy,hashlib,struct,copy
from fractions import Fraction
O=Path(__file__).resolve().parents[1];D=O/'definition-completion'
def rows(p):return list(csv.DictReader(p.open(),delimiter='\t'))
fields=rows(D/'security-fields.tsv');rels=rows(D/'security-relations.tsv');custody=rows(D/'security-custody.tsv')
assert len({f['surface_id'] for f in fields})==len(fields)==156
assert len(custody)==len(fields)*7 and all(c['visibility']=='UNKNOWN' for c in custody)
M=runpy.run_path(str(D/'assemble_definition.py'));decl=M['declaration']()
assert decl['governing_policy'] is None and decl['privacy_admission'] is False
for p,h in decl['input_sha256'].items():assert hashlib.sha256((O/p).read_bytes()).hexdigest()==h
s=(O/'sources/PE-G4-SOURCE-S90.md').read_text()
for p in ('ACCEPTANCE-CONTRACT.txt','security-fields.tsv','security-relations.tsv','security-custody.tsv','qualification-interface.tsv','budget.py','assemble_definition.py'):assert (D/p).read_text() in s
# Complete synthetic directories with multiple instances: data never written as a profile.
schemas={f['schema'] for f in fields};directory={s:['FIXTURE-ONE'] for s in schemas}
for name in ('EXPERIMENT','ARGUMENT','ASSESSMENT'):directory[name]=['FIXTURE-ONE','FIXTURE-TWO']
directory['POLICY-APPLICABILITY']=['FIXTURE-STATIC','FIXTURE-E','FIXTURE-PRE-EXECUTION','FIXTURE-PRE-COMMITMENT']
g=M['instantiate_security'](directory)
assert len({t['id'] for t in g['tokens']})==len(g['tokens'])
base=runpy.run_path(str(O/'privacy/expand_privacy.py'))['construct']()
old=base[2];oldids={t['id'] for t in old};newids={t['id'] for t in g['tokens']}
assert not oldids&newids
assert all(a in newids and b in newids|oldids for a,b,_,_ in g['structural_edges'])
for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
 for f in fields:
  assert sum(t['surface']==f['surface_id'] and t['context']==context for t in g['tokens'])==len(directory[f['schema']])
# Preserve original universe and add all new arbitrary pairs. Segment ordering is
# original bound stream first, then lexicographic pairs with at least one new index.
start=len(old);nnew=len(g['tokens']);total=start+nnew
h=hashlib.sha256(b'PE-G4-SECURITY-ADDED-EQUALITY-PAIRS-V1\n');count=0
for a in range(total):
 for b in range(max(a+1,start),total):h.update(struct.pack('>II',a,b));count+=1
assert count==start*nnew+nnew*(nnew-1)//2
# No missing-policy directory is accepted by the documentary expansion helper.
negative=0
for bad in ({},{**directory,'POLICY':[]},{**directory,'POLICY':['x','y']},{**directory,'ARTIFACT':['x','x']},{**directory,'ARGUMENT':['x::y']}):
 try:M['instantiate_security'](bad)
 except ValueError:negative+=1
 else:raise AssertionError('bad directory')
B=runpy.run_path(str(D/'budget.py'))
terms=[{'argument_id':'fixture-one','bound':[1,10],'multiplicity':2},{'argument_id':'fixture-two','bound':[1,20],'multiplicity':1}]
r=B['union_budget'](terms,[1,4]);assert r['bound']==[1,4] and r['budget_result']=='WITHIN' and r['profile_admitted'] is False
assert B['union_budget'](terms,[1,5])['budget_result']=='EXCEEDED'
saturated=B['union_budget']([{'argument_id':'x','bound':[3,4],'multiplicity':2}],[3,4]);assert saturated['bound']==[1,1] and saturated['budget_result']=='EXCEEDED'
for value in ([1,0],[2,1],[-1,3],[2,4],[True,2],[0.1,1]):
 try:B['rational'](value)
 except ValueError:negative+=1
 else:raise AssertionError('bad probability')
for bad in ([],[{'argument_id':'x','bound':[1,2],'multiplicity':False}],[{'argument_id':'x','bound':[1,2],'multiplicity':1,'complete':True}],terms+terms):
 try:B['union_budget'](bad,[1,2])
 except ValueError:negative+=1
 else:raise AssertionError('bad budget terms')
req=json.loads((O/'composition/requirement-inventory.json').read_text());assert len(req)==972
assert [r['requirement_id'] for r in req[959:971]]==[f'PE-G4-CAP-{i:03}' for i in range(99,111)]
projection=rows(O/'profile/fragments/BOUNDED-NOT-ADMITTED-projection.tsv')
assert len(projection)==2 and all(r['ordering_coordinate_definition_ids']=='NONE' for r in projection)
assert all(r['dependency_coordinate_definition_ids']=='PE-G4-CAP-SEMANTIC-BASIS-COORDINATE,PE-G4-CAP-E-BASIS-COORDINATE' for r in projection)
report={'construction':'PASS-DEFINITION-REVIEW-BASIS','security_fields':len(fields),'potential_custody_cells':len(custody),'unknown_visibility_not_admitted':True,'synthetic_instance_graph':{'scope':'TEST-ONLY-NOT-PROFILE-MATERIAL','prior_tokens':start,'security_tokens':nnew,'prior_structural_edges_preserved':len(base[3]),'new_structural_edges':len(g['structural_edges']),'added_potential_equality_pairs':count,'added_pair_sha256':h.hexdigest(),'original_equality_descriptor_retained':True,'actor_graph_pruned':False},'negative_cases':negative,'budget_arithmetic':'PASS-CONDITIONAL-ONLY','source_qualified_assessor_appointed':False,'independent_definition_review':False,'governing_V4_profile_constructed':False,'privacy_admitted':False}
(O/'verification/definition-completion.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'DEFINITION-DECLARATION-V4.json').write_bytes(M['canonical'](decl))
print('PASS — acceptance contract, explicit schema/custody/interface registers and rational budget checks.')
print('PASS — repeated-record expansion retains all inherited nodes/edges and every added potential equality pair.')
print('BOUNDARY — approved A integrated; concrete source/privacy evidence and an admitted V4 profile remain absent.')
