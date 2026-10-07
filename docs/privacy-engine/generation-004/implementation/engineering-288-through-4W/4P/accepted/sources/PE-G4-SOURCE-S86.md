# PE-G4-SOURCE-S86 — authorized cross-role correlation correction

Unpublished source candidate. Steve authorized the narrowly scoped proposal on 2026-09-30. Separate semantic domains alone do not erase source-established dataflow. Existing S84 permissions remain intact. This module specializes correlation assessment only; public uniqueness is unchanged.

<a id="separation"></a>
## separation

Cross-role raw public scalar equality MUST be excluded from correlation only when independently authenticated separation evidence binds the exact public roles, source domains, complete graph and absence of source-defined linkage.

<a id="provenance"></a>
## provenance

The complete edge-origin classification MUST be independently established; missing or unknown provenance or separation evidence MUST NOT grant the correction.

<a id="preservation"></a>
## preservation

Actor reconstruction MUST retain every graph edge; unknown visibility, same-role cross-action nullifier links, source-established relations and alternate observable paths MUST retain their existing failure obligations.

<a id="scope"></a>
## scope

This correction MUST NOT change public uniqueness, appoint an evidence authority, assert source completeness or grant profile admission.

## Authority boundary

The authenticated_separation_ids input is the output of a competent external evidence validator, not a caller certification switch. It must bind the exact source/anchor/digest, domain records and graph digest, and the complete edge-origin map. This graph subroutine does not perform signatures, appointments or source completeness validation. No production caller may manufacture the authenticated set or classify a source-established equality as RAW-SCALAR-EQUALITY. The canonical profile/evidence validator remains an unclosed integration gate.

The pair-specific evidence schema is exact in the module below. Evidence identities are unique; no extra authenticated IDs or omitted edge origins are accepted. Distinct labels or numeric inequality of scope names is not proof of semantic separation. Source-established paths remain in the observable graph; raw scalar equalities cannot be used to erase them. Alternate paths independently retain correlation failure. Unknown visibility failures remain even when a correlation-only exception applies.

The complete actor assessment executes on the original graph. Only CORRELATION-FAILURE may be recomputed using the permitted raw-edge removal; all original other failures are retained. The new evidence fields and edge-origin/validation metadata are additional conservative surfaces in the expanded candidate graph. Their presence is not disclosure permission.

## Exact authored procedure

```python
"""S86 authorized correlation-only correction; never an evidence authenticator.
Caller must authenticate exact domain-separation and complete edge-origin evidence.
No caller boolean substitutes for independent source/visibility/authority validation.
"""
from pathlib import Path
import runpy,hashlib,json
BASE=runpy.run_path(str(Path(__file__).with_name('observation_correlation.py')))
def graph_digest(nodes,edges):
 return hashlib.sha256((json.dumps({'nodes':nodes,'edges':edges},sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def graph_checks(nodes,edges,required_views,visibility,public_bindings=None,domain_separations=None,authenticated_separation_ids=None,edge_origins=None):
 baseline=BASE['graph_checks'](nodes,edges,required_views,visibility,public_bindings)
 if not domain_separations:return baseline
 failures=set(baseline['failures']);permitted=set();ids=set()
 bindings,binding_failures=BASE['validate_public_bindings'](nodes,public_bindings)
 failures.update(binding_failures)
 auth=set(authenticated_separation_ids or ())
 origins={} if edge_origins is None else edge_origins
 origins_ok=set(origins)==set(range(len(edges))) and all(v in ('RAW-SCALAR-EQUALITY','SOURCE-ESTABLISHED','STRUCTURAL') for v in origins.values())
 if not origins_ok:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
 for proof in domain_separations:
  try:
   keys={'evidence_id','left_node','right_node','left_domain','right_domain','owner_source_id','source_sha256','source_anchor','graph_sha256','scope','separate_semantic_domains','no_source_defined_linkage'}
   if not isinstance(proof,dict) or set(proof)!=keys:raise ValueError('schema')
   eid=proof['evidence_id']
   if not isinstance(eid,str) or not eid or eid in ids:raise ValueError('evidence identity')
   ids.add(eid)
   if eid not in auth:failures.add('INVALID-EVIDENCE-AUTHENTICATION');continue
   if proof['graph_sha256']!=graph_digest(nodes,edges):failures.add('INVALID-EVIDENCE-DIGEST');continue
   if proof['scope']!='CROSS-ROLE-RAW-SCALAR-CORRELATION-ONLY':raise ValueError('scope')
   if proof['separate_semantic_domains'] is not True or proof['no_source_defined_linkage'] is not True:raise ValueError('unknown or false separation')
   for key in ('owner_source_id','source_anchor'):
    if not isinstance(proof[key],str) or not proof[key] or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:#-' for c in proof[key]):raise ValueError('source identity')
   d=proof['source_sha256']
   if not isinstance(d,str) or len(d)!=64 or any(c not in '0123456789abcdef' for c in d):raise ValueError('source hash')
   a,b=proof['left_node'],proof['right_node'];x,y=bindings[a],bindings[b]
   if nodes[a]['context']==nodes[b]['context'] or x['role']==y['role']:raise ValueError('must be cross-context and cross-role')
   domain=lambda q:{k:q[k] for k in ('role','owner_source_id','source_sha256','source_anchor','scope_id')}
   if proof['left_domain']!=domain(x) or proof['right_domain']!=domain(y):raise ValueError('domain join')
   if x['value_hex']!=y['value_hex']:raise ValueError('not equal scalar bytes')
   # A source-established direct relation can never be waived by separation evidence.
   related=[i for i,e in enumerate(edges) if {e[0],e[1]}=={a,b}]
   if not origins_ok:continue
   if not related or any(edges[i][2]!='EQUALS' or origins[i]!='RAW-SCALAR-EQUALITY' for i in related):raise ValueError('source/structural linkage retained')
   permitted.update(related)
  except (KeyError,TypeError,ValueError):failures.add('INVALID-ACTION-CONTEXT')
 if auth-ids:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
 # Recompute ONLY correlation on a view excluding approved raw-equality edges.
 # All original structural/visibility checks, uniqueness and full actor results stay.
 if permitted:
  keep=[i for i in range(len(edges)) if i not in permitted]
  projected={view:{'nodes':v.get('nodes',{}),'edges':{j:v.get('edges',{}).get(i,'UNKNOWN') for j,i in enumerate(keep)}} for view,v in visibility.items()}
  filtered=BASE['graph_checks'](nodes,[edges[i] for i in keep],required_views,projected,public_bindings)
  failures.discard('CORRELATION-FAILURE')
  if 'CORRELATION-FAILURE' in filtered['failures']:failures.add('CORRELATION-FAILURE')
 return {'scope':'GRAPH-CHECKS-ONLY-NOT-PROFILE-ADMISSION','failures':[x for x in BASE['ORDER'] if x in failures],'earliest_failure':next((x for x in BASE['ORDER'] if x in failures),'NONE'),'correlation_only_exempted_edge_indices':sorted(permitted),'full_actor_graph_preserved':True,'uniqueness_rule_unchanged':True}
```
