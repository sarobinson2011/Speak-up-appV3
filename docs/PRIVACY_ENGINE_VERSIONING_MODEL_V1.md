# Privacy Engine Versioning Model V1

STATE.md remains canonical.  
This document is supporting documentation only.

If this document conflicts with STATE.md, STATE.md wins.

## 1. Purpose of Versioning

Versioning exists to preserve protocol identity across time.

The Privacy Engine may evolve, but external integrators need to know whether a later form preserves the same protocol contract or creates a new protocol generation.

Versioning answers one question:

> Does this evolution preserve the same protocol identity?

Version numbers communicate protocol evolution.

They do not prove compatibility.

Compatibility remains determined by invariant preservation.

## 2. Protocol Identity

A Privacy Engine protocol version is a published semantic contract.

It is not defined by:

- one implementation
- one deployment
- one repository
- one operator
- one application
- one cryptographic library
- one backend shape

It is defined by the externally relied-upon protocol semantics.

Same protocol identity means:

> all externally relied-upon protocol semantics remain preserved.

Different protocol identity means:

> the version changes those semantics such that an application, integrator, proof system, or layer implementation can no longer rely on the same contract.

## 3. Version-Stable Invariants

The following invariants are version-stable unless a new protocol generation is explicitly declared.

### Core rule

Private actors, public actions.

### Layer separation

Each layer preserves its own responsibility:

- identity / membership
- witness-data / path material
- execution / submission
- application action
- read / indexing support

No layer may silently become another layer's authority.

### Actor privacy

The protocol must preserve ambiguity about which private actor produced a public valid action.

### Public action validity

Public actions must remain externally verifiable.

### Uniqueness

Action uniqueness must be enforced by the protocol's declared uniqueness primitive, not by wallet identity, backend memory, or implementation heuristics.

### No hidden coupling

Protocol layers must not introduce silent join keys, reusable correlation tags, provenance bridges, or implicit identity reconstruction.

### Implementation independence

Internal machinery remains replaceable if protocol semantics are preserved.

### Compatibility by invariant preservation

Compatibility is judged against the protocol contract, not against a reference implementation.

## 4. Compatible Evolution

A change is version-compatible when it preserves protocol identity.

Compatible evolution may include:

- replacing internal implementations
- changing deployment addresses
- improving runtime robustness
- replacing backend internals
- optimizing proof generation
- changing data structures that do not affect external semantics
- adding non-authoritative tooling
- improving documentation without changing meaning
- adding implementation options that preserve existing protocol obligations
- introducing stricter validation that enforces already-required invariants

Compatible change rule:

> If every externally relied-upon invariant remains true, the change may remain within the same protocol generation.

Compatible does not mean risk-free.

It means semantically preserving.

## 5. Breaking Evolution

A change is version-breaking when it changes protocol identity.

Breaking changes include:

- changing identity semantics
- changing uniqueness semantics
- changing public action validity semantics
- changing layer authority
- allowing a layer to infer or reconstruct another layer's state
- introducing reusable public actor correlation
- changing required application obligations
- changing what compatibility means
- changing proof/public-signal semantics relied upon by applications
- changing privacy guarantees
- changing protocol-level trust assumptions
- removing an invariant external integrators rely on

Breaking change rule:

> If an existing conforming application cannot rely on the same protocol contract after the change, a new protocol generation is required.

## 6. Multi-Version Coexistence

Multiple Privacy Engine protocol generations may coexist.

Coexistence is valid only when version identity is explicit.

Each generation must publish its own semantic contract.

A system must not imply that two generations are compatible merely because they share:

- implementation code
- infrastructure
- application UI
- deployment operator
- brand
- repository history
- proof tooling

Coexistence rule:

> Different protocol generations may interoperate only through explicitly defined adapters or migration rules.

No silent equivalence.

No implicit upgrade path.

No compatibility by naming.

## 7. Responsibilities of Protocol Authors

Future protocol authors must preserve version clarity.

They must:

- state the protocol version being defined
- identify whether changes are compatible or breaking
- preserve version-stable invariants unless declaring a new generation
- publish the semantic contract external integrators rely upon
- distinguish protocol semantics from implementation details
- avoid treating version numbers as conformance evidence
- document migration or coexistence rules when generations differ
- update STATE.md before architectural changes

They must not:

- hide semantic changes inside implementation changes
- redefine compatibility after the fact
- make version identity depend on a deployment
- use a reference implementation as the protocol definition
- introduce new authority surfaces without explicit version treatment

## 8. Published Version Contract

Every Privacy Engine protocol version must publish the minimum contract required for external reliance.

Required published information:

- protocol name
- protocol generation
- version identifier
- canonical protocol invariant set
- layer boundary definitions
- external application obligations
- compatibility criteria
- conformance evidence requirements
- known breaking changes from prior generation, if any
- coexistence or migration notes, if applicable
- deprecation status, if applicable

The published contract should exclude:

- private implementation details
- deployment-specific addresses unless the version is deployment-bound by design
- operational runbooks
- UI behavior
- database structure
- non-authoritative helper tooling
- reference implementation internals

Published version contract rule:

> Publish what external parties may rely on. Do not publish machinery as protocol identity.

## 9. Conclusion

A Privacy Engine protocol version is a semantic contract.

The same protocol may evolve when its externally relied-upon invariants remain preserved.

A new protocol generation is required when protocol identity changes.

Versioning does not replace compatibility analysis.

Versioning identifies protocol identity across time.

Compatibility remains invariant preservation.

Minimum model:

> Version = published protocol contract.  
> Compatible evolution = same contract preserved.  
> Breaking evolution = new contract required.  
> Coexistence = explicit generation identity.  
> Conformance = evidenced semantic preservation.
