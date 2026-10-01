from pathlib import Path
import runpy,itertools,json,contextlib,io
O=Path(__file__).resolve().parents[2]
M=runpy.run_path(str(Path(__file__).with_name('construct.py')))
f=M['collision_reduction'];count=0
# Exhaustive small-domain conditional logical cases, not Poseidon security tests.
for s1,s2,a1,a2,n1,n2 in itertools.product(range(3),repeat=6):
 r=f((s1,a1,2),(s2,a2,2),n1,n2)
 want='SAME-ACTION-NO-CROSS-ACTION-REDUCTION' if a1==a2 else 'OUTPUTS-DIFFER' if n1!=n2 else 'IF-BOTH-OUTPUTS-ARE-VALID-THEN-HASH-COLLISION'
 assert r==want;count+=1
for bad in (-1,M['P'],True,'1',None):
 try:f((1,bad,2),(1,2,2),1,1)
 except ValueError:pass
 else:raise AssertionError('malformed accepted')
try:f((1,1,2),(1,2,3),1,1)
except ValueError:pass
else:raise AssertionError('domain mismatch accepted')
with contextlib.redirect_stdout(io.StringIO()):
 T=runpy.run_path(str(O/'privacy/test_cross_role_uniqueness.py'))
for name,failure in [('same-role cross-action nullifier stays rejected','CORRELATION-FAILURE'),('hidden actor bridge retained','ACTOR-RECONSTRUCTION-RISK'),('unknown visibility remains a failure','INCOMPLETE-EVIDENCE-UNIVERSE'),('alternate observable source path retained','CORRELATION-FAILURE')]:
 assert failure in next(r for r in T['results'] if r['case']==name)['failures']
r=M['construct']();assert r['profile_admitted'] is False and r['discharged_obligations']==[]
assert r['full_graph']['removed_edges']==r['full_graph']['removed_nodes']==0
(O/'verification/relation-obligations.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print(f'PASS — {count} conditional reduction cases; malformed/domain mismatch cases rejected; no cryptographic security claim.')
print('PASS — observed cross-action equality, actor paths, source paths and unknown visibility remain rejected.')
print('BOUNDARY — exact cryptographic evidence, argument validator and production acceptance integration remain open.')
