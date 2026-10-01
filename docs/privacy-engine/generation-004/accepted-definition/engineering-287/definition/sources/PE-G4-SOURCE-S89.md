# PE-G4-SOURCE-S89 — authorized relation-aware static admission

Unpublished source construction; no appointment, adoption or publication. S03–S88 historical bytes remain unchanged. The precedence below is explicit and limited to the authorized G4 redesign.

<a id="precedence"></a>
## precedence

For this unpublished G4 candidate only, S89 MUST supersede S71 static potential-equality interpretation by rules R1–R7; established occurrence evidence and S83–S87 protections remain required.

<a id="graph"></a>
## graph

The full two-context node, structural-edge and potential-equality universe MUST remain bound without removal, scope restriction or automatic actor-path exemption.

<a id="branches"></a>
## branches

The static checker MUST distinguish equal-action, unequal-action unequal-output and unequal-action equal-output branches without treating symbolic placeholders as observed equality.

<a id="proof"></a>
## proof

The conditional collision derivation MUST be checked by the closed proof kernel below against independently regenerated bindings; its premises MUST NOT be represented as established facts.

<a id="security"></a>
## security

Collision resistance MUST NOT be represented as unlinkability, mathematical injectivity or proof soundness; exact algorithm, adversary, observer, security budget and whole-view evidence MUST remain separate obligations.

<a id="failures"></a>
## failures

Established cross-action linkage, source linkage and actor reconstruction risks MUST remain rejected; unknown visibility, unsupported arguments and incomplete evidence MUST fail closed.

<a id="serialization"></a>
## serialization

For the S89 rule set, the V3 declaration below MUST replace the S88 V2 declaration selection in CAP-088; the inherited three-member outer framing and V2 evidence signature preimages remain unchanged.

<a id="admission"></a>
## admission

Serialization and a valid conditional derivation MUST NOT grant admission; production acceptance requires independent validation of all governing evidence and complete integration, with no issuer completion flags.

## Rule details

# Authorized unpublished G4 relation-aware admission redesign

Status: authorized unpublished rule, integrated by PE-G4-SOURCE-S89 and the V3 candidate declaration. Not published, appointed or admitted. Retained S03–S88 bytes remain exact; S89 explicitly states the limited G4 precedence change.

## Exact replacement rule

R1. Enumerate the same complete two-context universe, structural edges and potential equality edges. Preserve endpoints, provenance, constants, public roles, all observer coalitions and actor nodes. No edge is deleted, no action scope narrowed, and no symbolic placeholder is evidence of actual equality. Occurrence evidence continues to use exact authenticated records and the S83–S87 policies.

R2. A potential equality is a candidate obligation, not an assertion that its endpoint values actually coincide. Partition its relation-valid assignments, including equal-action and unequal-action branches. A branch may be discharged only by a mechanically checked impossibility proof or a separately justified computational security argument bound to exact source, circuit, algorithm parameters, public input encoding, model, adversary, observer scope and security budget. Unknown, incomplete or unsupported branches remain unresolved. Signatures authenticate claims, not their truth.

R3. The initial supported relation is exactly n=Poseidon3(memberSecret, actionId, SIGN_DOMAIN) from retained S22 section 7. If two canonical action scalars differ, the corresponding ordered three-input tuples differ, irrespective of whether the secrets agree. Conditional on both accepted proofs enforcing that exact relation and binding their public inputs, equal n values imply a collision in that exact Poseidon3 function. This is a conditional reduction, not an impossibility proof, a probability bound, or evidence that this Poseidon instantiation has the required security.

R4. The unequal-action branch requires relation enforcement/proof soundness, canonical ordered-input binding, the exact hash instantiation and collision-resistance argument, plus independent cross-action unlinkability and complete observer/actor analysis. Collision resistance does not imply pseudorandomness, secret entropy, anonymity or resistance to dictionary attacks. No 1/p probability, random-oracle model, security bits or acceptable failure budget is assumed. These must be justified explicitly. Same-action duplicate permissions remain exactly S84; all other paths remain checked.

R5. For a whole-view claim, account for simultaneous conditions along paths and across all relevant occurrences. A path cannot be declared safe by checking isolated edges, nor can pairwise unlinkability be promoted to coalition unlinkability. Retain the full graph as an audit universe; evaluate realizable or computationally bounded paths only after checking the complete argument. No public-to-private actor path receives an automatic exemption. A full-graph actor failure remains unresolved unless a corresponding whole-view argument is validated under the redesigned rule.

R6. Established cross-action nullifier equality, established source linkage, reconstruction paths, malformed evidence and unknown visibility remain rejection conditions. A computational argument cannot override a known counterexample. Neither sample success nor issuer completion flags discharge an obligation. Observed output equality without authenticated relation witnesses is already a protected linkage failure; it need not be called a demonstrated hash collision.

R7. A production acceptance procedure must independently regenerate the obligation universe, validate exact proof/argument artifacts and their trust basis, account for the overall security budget, then apply all inherited admission gates and precedence. The implementation constructs obligations and checks the conditional symbolic reduction. It provides no implementation of general cryptographic security argument validation and grants no profile admission. Existing rejection-only admission.py remains explicitly incomplete.

## Concrete evidence obligations for this candidate

1. Exact circuit/relation and artifact binding: show that every accepted proof constrains public n,a,r and the ordered Poseidon inputs as required; cover verifier inability and soundness, not Boolean success alone.
2. Exact Poseidon3 instantiation: parameters, field, encoding, domain constant, applicable security analysis and any collision counterevidence. The S22 formula alone does not supply these facts.
3. Unlinkability: adversary capabilities, secret generation/entropy, domain/action selection, repeated queries, auxiliary data, coalition observations and a justified reduction or security analysis. No witness or member secret is requested for publication.
4. Full producer/observer model: resolve visibility, custody, timing, retries, errors and source-established links; bind every relevant graph path and all 118 field joins.
5. Explicit computational claim and budget: state the assumption, adversary resources, number of compared occurrences/queries, bound and acceptance threshold; justify composition. None is invented by this proposal.
6. Independently competent appraisal/appointment and exact authenticated evidence bundles, separate from the mathematical/cryptographic evidence above.

The redesign removes the logical demand to equate every potential equality with an established leak. It does not establish that this candidate satisfies the new obligations. Source-determined construction delivered here is a branch semantics, reduction checker and exact candidate obligation manifest. Production acceptance remains unfinished; missing cryptographic evidence and missing validator construction are separately recorded.

## Exact closed derivation checker

```python
"""Closed symbolic derivation checker. No hash evaluation or security assumption discharge."""
import hashlib,json

def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def application(secret,action):return ['POSEIDON3',[secret,action,'SIGN_DOMAIN']]
PREMISES={
 'action-distinct':['NE','a1','a2'],
 'left-relation':['EQ','n1',application('s1','a1')],
 'right-relation':['EQ','n2',application('s2','a2')],
 'output-equal':['EQ','n1','n2']}

def derive(proof,binding):
 if type(proof) is not dict or set(proof)!={'binding','steps'} or proof['binding']!=binding:raise ValueError('proof binding')
 if type(binding) is not dict or not binding or any(type(k) is not str or type(v) is not str or len(v)!=64 or any(c not in '0123456789abcdef' for c in v) for k,v in binding.items()):raise ValueError('digest binding')
 steps=proof['steps']
 if type(steps) is not list or len(steps)!=6:raise ValueError('closed proof length')
 out=[]
 for i,step in enumerate(steps):
  if type(step) is not dict:raise ValueError('proof step')
  rule=step.get('rule')
  if rule=='PREMISE':
   if set(step)!={'rule','name'} or step['name'] not in PREMISES:raise ValueError('unrecognized premise')
   out.append(PREMISES[step['name']])
  elif rule=='ORDERED-TUPLE-DISTINCT':
   if set(step)!={'rule','refs'} or type(step['refs']) is not list or len(step['refs'])!=1:raise ValueError('tuple rule schema')
   r=step['refs'][0]
   if type(r) is not int or not 0<=r<i or out[r]!=PREMISES['action-distinct']:raise ValueError('tuple rule premise')
   out.append(['NE',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']])
  elif rule=='COLLISION-DEFINITION':
   if set(step)!={'rule','refs'} or type(step['refs']) is not list or len(step['refs'])!=4 or any(type(r) is not int or not 0<=r<i for r in step['refs']):raise ValueError('collision references')
   got=[out[r] for r in step['refs']]
   want=[['NE',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']],PREMISES['left-relation'],PREMISES['right-relation'],PREMISES['output-equal']]
   if got!=want:raise ValueError('collision premises')
   out.append(['COLLISION','POSEIDON3',['s1','a1','SIGN_DOMAIN'],['s2','a2','SIGN_DOMAIN']])
  else:raise ValueError('unsupported rule')
 if out[-1][0]!='COLLISION':raise ValueError('wrong conclusion')
 return {'result':'VALID-CONDITIONAL-DERIVATION','assumptions':PREMISES,'conclusion':out[-1],'binding':binding,'security_established':False,'profile_admitted':False}

def certificate(binding):
 return {'binding':binding,'steps':[{'rule':'PREMISE','name':x} for x in PREMISES]+[{'rule':'ORDERED-TUPLE-DISTINCT','refs':[0]},{'rule':'COLLISION-DEFINITION','refs':[4,1,2,3]}]}
```

## Exact V3 representation

```python
"""S89 V3 candidate declaration; exact construction, never privacy admission."""
from pathlib import Path
import runpy,hashlib,json
O=Path(__file__).resolve().parents[2]
P=runpy.run_path(str(Path(__file__).with_name('privacy_member.py')))
K=runpy.run_path(str(O/'privacy/relation-aware/proof_kernel.py'))
FILES=['sources/PE-G4-SOURCE-S89.md','privacy/relation-aware/rule.md','privacy/relation-aware/construct.py','privacy/relation-aware/proof_kernel.py','profile/integration/relation_member.py','profile/integration/relation_admission.py']
def declaration():
 # Refresh all graph declarations and full streamed equality binding locally.
 X=runpy.run_path(str(O/'privacy/expand_privacy.py'));X['expand']()
 base=P['declaration']()
 binding={p:hashlib.sha256((O/p).read_bytes()).hexdigest() for p in FILES+['sources/retained/S22.md','privacy/expanded/PRIVACY.candidate.json']}
 proof=K['certificate'](binding);checked=K['derive'](proof,binding)
 obligations=runpy.run_path(str(O/'privacy/relation-aware/construct.py'))['construct']()
 # Diagnostic implementation status is not an immutable governing fact.
 policy_obligations={k:obligations[k] for k in ('full_graph','pair','branches','all_other_pairs','established_cross_action_equality','unknown_visibility','actor_graph')}
 return {**base,'format':'PE-G4-PRIVACY-PROFILE-V3','format_source':'PE-G4-SOURCE-S89','format_source_sha256':binding['sources/PE-G4-SOURCE-S89.md'],'policy_sources':base['policy_sources']+['PE-G4-SOURCE-S89'],'procedures_sha256':{**base['procedures_sha256'],**binding},'relation_policy':{'bindings':binding,'conditional_proof':proof,'conclusion':checked['conclusion'],'premises':checked['assumptions'],'obligations':policy_obligations,'security_claim':'NONE-ESTABLISHED-BY-SERIALIZATION'}}
def member(appointment,trusted):
 P['appointment_shape'](appointment);P['appointment_shape'](trusted)
 if appointment!=trusted:raise ValueError('INVALID-EVIDENCE-AUTHORITY')
 return P['A']['canonical']({**declaration(),'appointment':appointment})
def construct_outer(appointment,trusted):
 privacy=member(appointment,trusted);body,program=P['A']['member_bytes']()
 return P['A']['encode_container']({'SOURCE-OWNED-BODY':body,'EXPRESSION-PROGRAM':program,'PRIVACY':privacy})
def validate_serialization(raw,appointment,trusted):
 decoded=P['A']['decode_container'](raw)
 if raw!=construct_outer(appointment,trusted):raise ValueError('PROFILE-DIGEST-MISMATCH')
 return {'serialization':'EXACT-V3','profile_admitted':False,'security_established':False}
```

## V3 rejection integration boundary

The exact rejection entrypoint below MUST independently regenerate V3 and MUST NOT accept V2 as this rule set. It remains rejection-only; the explicit unfinished acceptance path is not an evidence appointment gap alone.

```python
"""V3 rejection integration. Cryptographic argument validation is not implemented."""
from pathlib import Path
import runpy,contextlib,io
O=Path(__file__).resolve().parents[2]
M=runpy.run_path(str(Path(__file__).with_name('relation_member.py')))
A=runpy.run_path(str(Path(__file__).with_name('admission.py')))
def evaluate(request):
 try:
  with contextlib.redirect_stdout(io.StringIO()):
   runpy.run_path(str(O/'verify-candidate.py'))
   model=M['declaration']()
  result=A['collect'](request,model)
  result['candidate_format']='PE-G4-PRIVACY-PROFILE-V3'
  result['unfinished_integration']=['CRYPTOGRAPHIC-ARGUMENT-VALIDATOR','COMPLETE-SOURCE-OBSERVER-EVIDENCE-UNIVERSE','PRODUCTION-ACCEPTANCE-PATH']
  result['conditional_derivation']='CHECKED-NOT-SECURITY-EVIDENCE'
  return result
 except Exception as error:
  return {**A['decision']({'INVALID-PROFILE-SCHEMA'},{},['REGENERATION-FAILED']),'regeneration_error_type':type(error).__name__}
```
