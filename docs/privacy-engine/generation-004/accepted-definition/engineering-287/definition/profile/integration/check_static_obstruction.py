"""Concrete authored-static obstruction, not a claim about actual proof occurrences."""
from pathlib import Path
import runpy,contextlib,io,json
O=Path(__file__).resolve().parents[2]
with contextlib.redirect_stdout(io.StringIO()):
 v=runpy.run_path(str(O/'verify-candidate.py'))
 T=runpy.run_path(str(O/'privacy/test_public_relationships.py'))
app=v['asts']['PE-G4-CAP-APPLICABILITY']
rows=[]
for a in ('11','12'):
 av=('PE-TSE-UINT',a);nv=('PE-TSE-UINT','13');state=('PE-G4-CAP-SCOPED-STATE',[av,nv,('PE-TSE-BOOL3',0)])
 result=v['evaluate'](app,[v['type_ref'],v['rules_ref'],av,nv,state]);assert result==('PE-TSE-BOOL3',1)
 rows.append({'a':a,'n':'13','source_used':False,'mapping_applicability':True,'actual_E_or_D_asserted':False})
X=runpy.run_path(str(O/'privacy/expand_privacy.py'));_,_,tokens,_=X['construct']();by={t['id']:t for t in tokens}
a=by['SYMBOLIC-U-ONE::PUBLIC-PI:n'];b=by['SYMBOLIC-U-TWO::PUBLIC-PI:n'];assert a['arbitrary'] and b['arbitrary'] and a['exposure']==b['exposure']=='PUBLIC'
# S87 explicitly cannot exempt same-role n pairs; existing authorized fixture confirms.
n,e,bindings=T['fixture'](('a','n'),{'a':(11,12),'n':(13,13)})
M=runpy.run_path(str(O/'privacy/cross_role_uniqueness.py'))
views=[('public',)];visibility={views[0]:{'nodes':{k:'VISIBLE' for k in n},'edges':{i:'VISIBLE' for i in range(len(e))}}}
r=M['graph_checks'](n,e,views,visibility,bindings)
assert 'UNIQUENESS-FAILURE' in r['failures'] and 'CORRELATION-FAILURE' in r['failures']
report={'finding':'GENERIC-STATIC-CROSS-ACTION-NULLIFIER-OBSTRUCTION','current_applicability_accepts_both_source_classes':rows,'static_pair':[a['id'],b['id']],'retained_static_generator_includes_pair':True,'same_role_pair_not_covered_by_S86_S87':True,'bounded_policy_counterexample':r,'actual_proof_relation_realizability_established':False,'actual_privacy_breach_claimed':False,'scope':'Current conservative abstract admission model only; no claim about completed real E/D/U','consequence':'Appointments or signatures alone cannot turn this declared generic static abstraction into an admission PASS. An explicit source-grounded resolution of this remaining static case is required; sampled success or ignoring the pair is insufficient.'}
(O/'verification/static-nullifier-obstruction.json').write_text(json.dumps(report,indent=2)+'\n')
print('BOUNDARY — current generic applicability and static expansion retain a protected cross-action nullifier case.')
print('No actual proof occurrence or privacy breach is asserted; no same-role exception added.')
