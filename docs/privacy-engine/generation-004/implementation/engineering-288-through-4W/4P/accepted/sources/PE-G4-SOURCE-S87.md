# PE-G4-SOURCE-S87 — authorized cross-role public uniqueness correction

Unpublished source candidate. Steve expressly authorized applying the same scheme to uniqueness on 2026-09-30 after verifying S86. This adopts the exact additional rule proposed in UNIQUENESS-DECISION.md. It appoints no source and grants no profile admission.

<a id="qualification"></a>
## qualification

Public uniqueness MUST apply exactly the authenticated S86 cross-role semantic-separation qualification to each candidate pair; no additional evidence shortcut or same-role permission is granted.

<a id="all-pairs"></a>
## all-pairs

Every other cross-context public equal-byte pair MUST still be assessed under the existing uniqueness rule; qualifying one pair MUST NOT suppress an unrelated uniqueness failure.

<a id="preservation"></a>
## preservation

The complete actor graph, same-role cross-action nullifier protection, source-established linkage, unknown-evidence failure and all remaining admission requirements MUST be preserved.

## Exact scope and evidence reuse

S86 remains the exclusive qualifier for a pair: different public roles, different contexts, exact equal canonical scalar bytes, exact source-domain/graph bindings, independently authenticated separation and absence of source-defined linkage, and complete known edge-origin evidence marking only raw scalar equality. Its existing evidence scope label CROSS-ROLE-RAW-SCALAR-CORRELATION-ONLY is preserved as the historical evidence-contract literal. S87 authorizes reuse of those same authenticated facts for uniqueness; the immutable S87 rule supplies this authority, not a renamed caller scope or evidence issuer permission. The source/evidence admission process must bind the active S87 policy. No older admitted policy is retroactively changed.

The procedure first executes S86, which assesses actor reconstruction on every original graph edge. It then reassesses every public cross-context equal-digest pair under the original constant/S84 permissions plus the exact S86-qualified unordered pairs. Only UNIQUENESS-FAILURE is recomputed. Every other failure stays. Same-role pairs cannot qualify; a separate bad pair remains a failure even if some other pair qualifies. Graph-level absence of failures is never a source qualification or profile admission result.

There are no new evidence fields: all S86 domain/provenance surfaces remain in the expanded equality and actor graph unchanged. Actual source authentication, complete observer/coalition/visibility evidence, applicable source coverage and canonical governing profile integration remain required. Static potential equality is still fully generated and never pruned by this assessment permission.

## Exact authored procedure

```python
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
```
