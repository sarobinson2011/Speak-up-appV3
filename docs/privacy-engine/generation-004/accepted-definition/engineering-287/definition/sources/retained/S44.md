# Privacy Engine Integrator Obligations V1

STATE.md remains canonical.

This document is supporting documentation only. If this document conflicts with STATE.md, STATE.md wins.

## 1. Why Integrator Obligations Exist

The Privacy Engine exposes protocol guarantees through bounded interfaces.

Those guarantees can be weakened at the integration boundary if an application:

- reinterprets protocol outputs
- depends on internal machinery
- adds cross-layer identifiers
- claims privacy guarantees the protocol does not provide
- turns application semantics into protocol semantics

Integrator Obligations exist because systems most often break at interfaces.

The outer protocol boundary is the compound interface where all lower-layer interfaces become externally consumed.

Therefore:

The integrator does not merely call the protocol.

The integrator preserves the protocol.

## 2. Protocol Guarantees Integrators May Rely Upon

An integrator may rely on the stable protocol surface defined by the Privacy Engine.

Allowed reliance includes:

- valid anonymous membership can be proven without revealing the memberSecret
- membership identity is derived from the memberSecret through the leaf
- the nullifier enforces one valid action per action scope
- on-chain verification is authoritative for proof validity, root validity, and nullifier uniqueness
- protocol-owned layers preserve their stated responsibilities
- the application adapter boundary separates protocol ownership from application ownership
- internal machinery may be replaced if the stable protocol surface is preserved

Integrator reliance is limited to stable protocol outputs and documented adapter surfaces.

An integrator must not rely on internal implementation shape.

## 3. Guarantees Integrators Must Not Claim

An integrator must not claim guarantees that the Privacy Engine does not provide.

Forbidden claims include:

- one identity per human
- one identity per wallet
- guaranteed Sybil prevention
- network-level anonymity
- total timing-correlation resistance
- total relay or mirror non-observability
- recovery of identity without the original memberSecret
- application-level privacy from protocol validity alone
- stronger privacy than the deployed protocol layer actually provides

The protocol provides bounded privacy guarantees.

The application must not inflate them.

## 4. Integrator-Owned Responsibilities

The integrator owns application semantics.

Integrator-owned responsibilities include:

- application purpose
- user-facing workflows
- application authorization rules
- application metadata
- application persistence
- application UI
- application moderation
- application lifecycle
- application-specific read models
- application-specific indexing
- application-specific risk communication
- application-specific legal or policy obligations

The integrator must ensure that application-owned behaviour does not reinterpret protocol-owned guarantees.

Application logic may consume protocol outputs.

Application logic must not redefine protocol meaning.

## 5. Protocol-Owned Responsibilities

The Privacy Engine owns protocol semantics.

Protocol-owned responsibilities include:

- anonymous membership semantics
- memberSecret / leaf identity semantics
- ZK proof validity semantics
- public input order
- nullifier derivation and uniqueness semantics
- enrollment semantics
- REFLECT path / witness-data semantics
- TEMPEST execution / submission semantics
- protocol compatibility boundaries
- protocol-owned privacy guarantees
- adapter contract meaning

The integrator must treat these as reserved protocol authority.

## 6. Privacy-Preserving Integration Rules

A protocol-safe integration must:

- use only stable adapter surfaces
- preserve protocol-owned semantics
- keep application identifiers outside protocol identity semantics
- avoid creating cross-layer join keys
- avoid carrying enrollment identifiers into action surfaces
- avoid wallet-based reconstruction of anonymous identity
- avoid backend identity inference
- avoid persistent provenance bridges
- treat protocol internals as replaceable
- fail closed when compatibility cannot be preserved

Core rule:

Application state may reference application facts.

Protocol state may express protocol facts.

Neither may silently become the other.

## 7. Forbidden Integration Patterns

The following patterns violate protocol ownership:

- treating wallet address as anonymous identity
- treating enrollment funding source as participant identity
- treating admission consumption as participant readiness
- treating nullifier as reusable cross-application identity
- deriving application profiles from protocol artefacts
- persisting protocol-internal routing details as application state
- exposing relay, mirror, slot, path, or fallback internals as application semantics
- using implementation details as integration requirements
- adding application metadata to protocol validity semantics
- claiming protocol privacy from application-only behaviour
- silently adapting protocol truth when validation fails

Forbidden pattern summary:

Protocol output -> application identity is forbidden.

Application metadata -> protocol truth is forbidden.

Internal machinery -> external contract is forbidden.

## 8. Safe Application-Specific Extensions

Application extensions are protocol-safe when they remain outside protocol ownership.

Safe extensions may include:

- application-specific content
- application-specific metadata
- application-specific display logic
- application-specific moderation
- application-specific permissions
- application-specific read models
- application-specific analytics that do not touch protocol identifiers
- application-specific reputation that does not derive from hidden protocol identity
- application-specific workflows that consume protocol validity without redefining it

Safe extension rule:

The extension may use the fact that a valid protocol action occurred.

It must not infer who performed it.

## 9. Unsafe Application-Specific Extensions

Application extensions become protocol-breaking when they create new interpretation bridges.

Unsafe extensions include:

- action history grouped by nullifier-like artefacts
- application accounts linked to protocol identity primitives
- wallet recovery framed as anonymous identity recovery
- admission right history used as participant provenance
- enrollment timestamps used as usability signals
- relay path history stored per action
- mirror fetch history stored per participant
- application scoring based on hidden protocol-layer behaviour
- UI or docs that imply stronger privacy than the protocol provides
- compatibility shims that mutate protocol meaning instead of failing

Unsafe extension rule:

If the extension narrows anonymity, reassigns protocol authority, or depends on replaceable internals, it is not protocol-safe.

## 10. Upgrade / Replacement Obligations

Integrator compatibility must survive protocol-internal replacement.

Integrators must:

- depend only on stable protocol and adapter surfaces
- avoid dependencies on internal storage layouts
- avoid dependencies on concrete relay or mirror topology
- avoid dependencies on specific implementation files
- avoid dependencies on current backend convenience structure
- avoid dependencies on current ZK implementation beyond documented stable inputs and guarantees
- treat protocol upgrades as compatible only if protocol-owned semantics are preserved

Protocol replacement is allowed when stable meaning is preserved.

Integrator dependence on internals makes replacement unsafe.

Therefore:

Internal machinery is not an integration contract.

## 11. Documentation & Naming Obligations

Integrator documentation, code comments, variable names, logs, tests, UI copy, and API names must preserve privacy boundaries.

Forbidden language includes wording that implies:

- wallet identity equals anonymous identity
- funder equals participant
- admission right equals signer
- consumed right equals participant birth
- nullifier equals user identity
- relay path equals user route
- protocol validity equals human uniqueness
- application account equals protocol member

Naming is part of the security boundary.

An innocuous name can recreate a forbidden linkage model.

Integrator documentation must distinguish:

- protocol guarantees
- application guarantees
- known limitations
- non-goals

## 12. Integrator Contract Assessment

A compliant integrator accepts the following minimum obligation set:

1. Use only stable adapter surfaces.
2. Preserve protocol-owned semantics.
3. Do not depend on internal protocol machinery.
4. Do not introduce cross-layer identifiers.
5. Do not reinterpret protocol outputs as application identity.
6. Do not overclaim privacy guarantees.
7. Keep application semantics outside the protocol boundary.
8. Preserve naming and documentation discipline.
9. Preserve upgrade and replacement compatibility.
10. Fail compatibility rather than silently adapting protocol truth.

Assessment:

If an integration preserves these obligations, it may consume the Privacy Engine without acquiring protocol authority.

If it violates these obligations, it becomes protocol-breaking even if the API calls still succeed.

## 13. Protocol, Implementation, and Operations Boundary

Protocol, implementation, and operations are separate concerns.

The protocol specifies externally relied-upon semantics.

The implementation realizes those semantics.

Operations sustain an implementation that continues to realize them.

A conforming integrator must preserve:

- published protocol semantics
- published protocol invariants
- published interfaces
- published observable behaviour
- published failure semantics

Preserving those properties is mandatory.

Preserving any particular internal implementation structure is not.

Implementation substitution is permitted provided the published protocol semantics, interfaces, observable behaviour, and failure semantics remain invariant.

Operational mechanisms may vary provided the implementation continues to preserve the published protocol requirements.

The protocol intentionally does not prescribe:

- treasury architecture
- relay funding model
- signer custody
- RPC provider selection
- execution topology
- deployment architecture
- operational monitoring
- infrastructure platform

These remain implementation and operational concerns.

They must not become protocol requirements merely because one implementation uses them.

Protocol authority ends at the externally relied-upon semantics.

## 14. Conclusion

Integrator compatibility is not merely API compatibility.

Integrator compatibility is preservation of protocol ownership.

The application may consume protocol guarantees.

It must not manufacture them, weaken them, rename them, or claim ownership of them.

The Privacy Engine owns privacy semantics.

The application owns application semantics.

A conforming Privacy Engine integrator must preserve the published protocol semantics and observable behaviour.

Implementation architecture and operational provisioning remain intentionally outside protocol authority.

The protocol specifies what must be preserved.

The implementation determines how it is realized.

Operations sustain a conforming implementation over time.

The boundary between protocol authority and implementation freedom is the integration contract.

That boundary must remain explicit, preserved, and non-negotiable.
