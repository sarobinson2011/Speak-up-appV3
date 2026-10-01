# Draft uniqueness-effect source — exact selected semantics

Draft owner label: E283-DRAFT-EFFECT-SOURCE. Documentary semantic author text only; not an authenticated successor source or an admitted mapping. User authorization selects the root-policy and protocol-effect basis, not a current G3 registry entry. All local identifiers are unallocated draft coordinates.

<a id="state-constructors"></a>
## State values and constructors

Let a and n be the fixed action context and its correctly derived nullifier, represented canonically in the retained scalar domain. E283-DRAFT-SCOPED-STATE is a declared ordered tuple (a,n,used), with fields UINT, UINT, BOOL3. Its valid authoritative `used` values are FALSE and TRUE; UNRESOLVED is an evidence/evaluation status, not a third valid participation state. The typedef does not itself validate scalar range, scope or authority.

SOURCE-STATE(a,n) constructs (a,n,FALSE). SUCCESSOR-STATE(a,n) constructs (a,n,TRUE). The exact constructors are in definitions.tsv and use the existing canonical BOOL3 encodings. Neither constructor creates authenticated state or grants authorization. A missing status record is not evidence of FALSE.

<a id="source-successor-classes"></a>
## Source and successor classes

For the fixed key (a,n), the valid source class is exactly its authenticated unused state. The bounded successor class is exactly its used state. IS-SOURCE(a,n,q) tests equality to SOURCE-STATE(a,n); IS-SUCCESSOR(a,n,q) tests equality to SUCCESSOR-STATE(a,n). Canonical typed equality is justified here by the explicitly declared complete three-field bounded state meaning. Digest/commitment equality does not replace that meaning or authenticate its facts.

This transition writes only the scoped participation fact. It leaves other keys, membership-root/history state and all product records unchanged. Root history is an eligibility/read dependency, not a second owned state-changing effect. A realization cannot overwrite unrelated current state from an old whole-system snapshot. No new storage layout, table or protocol object is required.

<a id="successor-relation"></a>
## Successor relation and exact signature

SUCCESSOR-RELATION has ordered inputs (a,n,q0,q1) of types (UINT,UINT,E283-DRAFT-SCOPED-STATE,E283-DRAFT-SCOPED-STATE), returning BOOL3. It is TRUE exactly when q0 equals (a,n,FALSE) and q1 equals (a,n,TRUE), on valid complete authenticated domain inputs.

The prior draft described the conceptual two-state relation Successor(q0,q1). This four-input realization passes the already fixed action/nullifier coordinates explicitly so existing tuple construction and equality suffice; the language has no field-extraction operator. It preserves the same relation and effect, and does not introduce new public proof inputs, change PI order or select a universal relation arity. Final mapping/program/header signatures must agree exactly if this draft is later admitted.

Existence and uniqueness: for eligible (a,n,FALSE), constructing (a,n,TRUE) supplies a successor, and the equality condition fixes every bounded output field. No second bounded semantic successor satisfies the relation. This proves only the selected local effect's determinism. Full source validity, frame conditions, exact scope, external state authentication and all admission obligations remain necessary.

<a id="cardinality"></a>
## Required effect and recovery

One accepting D requires one scoped atomic uniqueness effect through a valid authorized U. Acceptance alone does not create U or authorize execution. This is required successful effect cardinality, not the number of failed attempts over time. Existing recovery may require new authorization/new U, and new E/new D only on successful new E, as specified by the exact 21-row table. Failed U never resumes; a committed effect marks the scoped key used and cannot be committed again for that same scoped key under the unused precondition. No second independent product effect is inserted.

<a id="gate-materiality"></a>
## Source-owned comparison core

After validation of the complete identity/context/profile/authorization/opening/state-authentication material, the predicate inputs are:

- v: authenticated acceptedness of the same declared root under the fixed policy at the current gate;
- b: authenticated used status of the exact scoped key at that gate.

Authorized eligibility requires v=TRUE and b=FALSE. For a correctly bound authorized context, the candidate comparison core is EQ(v,b)=v AND NOT b. Ordered sufficient conflicts are ROOT-CONFLICT(v,b)=NOT v, then USED-CONFLICT(v,b)=b. Their aggregate is OR(NOT v,b). definitions.tsv gives the exact expressions and signatures.

A wrong action/nullifier/root/policy binding is not fed to these predicates as an ordinary Boolean difference: existing identity/context validation fails first. Other complete required material conditions must be included in the actual projection/predicate composition if source closure shows them relevant. This core does not claim completeness of the final profile or license their omission.

On all four complete Boolean input pairs, EQ and aggregate MC are mutually exclusive and exhaustive. With unresolved input, retain the existing ordered procedure. An authenticated used=TRUE is independently sufficient conflict even if root acceptedness is unresolved; authenticated v=FALSE is independently sufficient conflict even if used status is unresolved. A validation/authentication failure still takes precedence and yields indeterminate. The existing both-true guard remains; proving it unreachable within this small well-formed core does not remove the guard from the protocol.

Changes in whole root history are not automatically conflicts if the declared root stays accepted, but every actual read, call, status, argument and control dependency remains in Dep(D). No claim of unchanged-D sufficiency may be based solely on stable v. Static profile graph is not actual occurrence evidence.

<a id="privacy-preservation"></a>
## Privacy and implementation independence

The scoped key is semantic input, not authority to expose participant links. Preserve action-local nullifier meaning, no secret/leaf/wallet/provenance joins, minimality, complete privacy composition and the full actor graph. Public proof inputs remain exactly nullifier/actionId/root. Candidate field inputs do not create new public outputs.

If two U compete for one unused key, only a commitment with authoritative unused status at its final indivisible gate may set it used. A later competitor must see the authoritative used fact and cannot commit. This argument depends on faithful current-state/commitment realization; the draft chooses no lock, database, chain, consensus or ordering implementation. If that correspondence is absent, readiness is unestablished.

Preserved source basis: S19 §4.3; S22 §7; S26 §§2/4/8–9; S35–39; S43 §§3–9; TRANSAUTH-001–015; S70 TYPES/COMPARISON/DEPENDENCY/RECOVERY/PRIVACY; S71; S72. Selected new effect scope/cardinality is recorded separately. No G3 mapping/profile is created; M remains zero.
