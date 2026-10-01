"""S87: extend exactly S86's authenticated pair qualification to uniqueness.
This graph procedure neither authenticates evidence nor admits a profile.
"""
from pathlib import Path
from itertools import combinations
import runpy
C=runpy.run_path(str(Path(__file__).with_name('cross_role_correlation.py')))
def graph_checks(nodes,edges,required_views,visibility,public_bindings=None,domain_separations=None,authenticated_separation_ids=None,edge_origins=None):
 result=C['graph_checks'](nodes,edges,required_views,visibility,public_bindings,domain_separations,authenticated_separation_ids,edge_origins)
 permitted_indices=result.get('correlation_only_exempted_edge_indices',[])
 if not permitted_indices:return result
 # Qualification is exactly S86's, including graph/source/domain/provenance checks.
 # Do not merely clear UNIQUENESS-FAILURE after seeing any qualified pair.
 pairs={frozenset(edges[i][:2]) for i in permitted_indices}
 failures=set(result['failures']);bindings,bad=C['BASE']['validate_public_bindings'](nodes,public_bindings);failures.update(bad)
 unique=True
 for a,b in combinations(sorted(k for k,v in nodes.items() if v['exposure']=='PUBLIC'),2):
  x,y=nodes[a],nodes[b]
  if x['context']==y['context'] or x['digest']!=y['digest']:continue
  if x['reuse']==y['reuse']!='NONE' or C['BASE']['public_pair_permitted'](a,b,bindings):continue
  if frozenset((a,b)) in pairs:continue
  unique=False
 if unique:failures.discard('UNIQUENESS-FAILURE')
 else:failures.add('UNIQUENESS-FAILURE')
 order=C['BASE']['ORDER']
 return {**result,'failures':[x for x in order if x in failures],'earliest_failure':next((x for x in order if x in failures),'NONE'),'uniqueness_rule_unchanged':False,'uniqueness_exempted_pairs':[sorted(p) for p in sorted(pairs,key=lambda p:tuple(sorted(p)))],'profile_admitted':False}
