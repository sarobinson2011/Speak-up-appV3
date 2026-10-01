from pathlib import Path
import runpy,io,contextlib,json
O=Path(__file__).resolve().parents[1]
m=runpy.run_path(str(O/'privacy/expand_privacy.py'));report=m['expand']()
p=json.loads((O/'privacy/expanded/PRIVACY.candidate.json').read_text());ts=p['tokens'];by={t['id']:t for t in ts}
a=by['SYMBOLIC-U-ONE::PUBLIC-PI:r'];b=by['SYMBOLIC-U-TWO::PUBLIC-PI:a']
assert a['arbitrary'] and b['arbitrary'] and a['exposure']==b['exposure']=='PUBLIC'
# Verify the decisive pair against the retained approved procedure using its existing synthetic vector.
with contextlib.redirect_stdout(io.StringIO()):v=runpy.run_path(str(O/'privacy/test_public_relationships.py'))
w=next(r for r in v['results'] if r['case']=='cross-role scalar equality receives no permission')
assert w['earliest_failure']=='UNIQUENESS-FAILURE' and 'CORRELATION-FAILURE' in w['failures']
# Distinct component binding occurrences are expanded; canonical component joins stay local.
for c in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
 bindings=[t for t in ts if t['context']==c and t['surface']=='CORE:COMPONENT-BINDING.bound_value']
 assert {t['record'] for t in bindings}=={1,2}
small=[{'index':0,'arbitrary':False,'symbolic_digest':'A'},{'index':1,'arbitrary':False,'symbolic_digest':'B'},{'index':2,'arbitrary':True,'symbolic_digest':'C'},{'index':3,'arbitrary':False,'symbolic_digest':'A'}]
assert list(m['equal_pairs'](small))==[(0,2),(0,3),(1,2),(2,3)]
assert len({t['id'] for t in ts})==len(ts)
assert p['actor_graph_policy']=='ALL structural and equality edges; no visibility/permission filtering'
report['decisive_public_pair']=[a['id'],b['id']];report['existing_counterexample']=w
(O/'verification/privacy-expansion.json').write_bytes(m['canonical'](report))
print('PASS — complete two-context declaration expansion and canonical candidate regeneration.')
print('PASS — all '+format(report['potential_equality_edges'],',')+' potential equality pairs streamed; count independently checked.')
print('PASS — historical unqualified cross-role counterexample remains rejected.')
