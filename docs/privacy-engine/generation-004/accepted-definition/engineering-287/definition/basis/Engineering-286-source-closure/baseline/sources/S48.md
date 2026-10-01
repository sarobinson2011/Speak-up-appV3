# Privacy Engine Compatibility / Conformance Model V1

STATE.md remains canonical.

This document is supporting documentation only. If this document conflicts with STATE.md, STATE.md wins.

## 1. Why Compatibility Exists

Compatibility exists so the Privacy Engine can evolve without becoming defined by one implementation, one application, one deployment, or one current cryptographic stack.

Compatibility means preserving protocol-owned semantics across implementation replacement.

## 2. Definition of Privacy Engine Compatibility

An implementation is Privacy Engine compatible if it preserves the protocol-owned guarantees, boundaries, and invariants defined by STATE.md while allowing implementation and application details to vary.

Minimum rule:

    compatibility = invariant preservation

## 3. Definition of Protocol Conformance

Protocol conformance means evidenced semantic preservation of the Privacy Engine protocol.

A conforming implementation must preserve what the protocol means, not merely resemble the current implementation.

Minimum rule:

    conformance = evidenced semantic preservation

## 4. Protocol Invariants Required for Compatibility

Every compatible implementation must preserve:

- private actors, public actions
- anonymous membership identity
- secret-derived membership continuity
- nullifier-based uniqueness
- ZK validity authority
- enrollment/application/action separation
- REFLECT path/witness-data preservation
- TEMPEST execution/submission preservation
- non-authoritative backend support
- protocol/application ownership separation
- explicit failure semantics
- observability discipline

## 5. Implementation Freedom

Compatible implementations may vary:

- language
- frontend
- backend
- database
- indexer
- deployment topology
- internal services
- infrastructure
- relayer machinery
- mirror machinery
- storage format
- application UI
- application metadata
- operational tooling

Implementation freedom ends where protocol meaning changes.

## 6. Compatibility-Preserving Changes

A change is compatibility-preserving when it changes machinery without changing protocol semantics.

Examples:

- refactoring internal services
- replacing databases
- changing UI components
- improving validation
- improving tests
- changing relayer internals without exposing route identity
- changing witness-data internals without changing REFLECT preservation semantics
- replacing cryptographic machinery only with explicit versioning and semantic preservation

Rule:

    same invariant meaning -> compatible

## 7. Protocol-Breaking Changes

A change is protocol-breaking if it alters ownership, authority, observability, or invariant meaning.

Examples:

- wallet-based uniqueness replacing nullifiers
- backend identity becoming authoritative
- admission identifiers becoming action correlation tags
- REFLECT providers selecting truth
- cross-state witness-data mixing
- TEMPEST route exposure
- application policy redefining protocol validity
- silent identity replacement
- reusable public action linkage identifiers

Rule:

    changed invariant meaning -> protocol-breaking

## 8. Compatibility Responsibilities

The protocol owns:

- identity semantics
- proof semantics
- nullifier semantics
- enrollment separation
- REFLECT preservation
- TEMPEST execution boundary
- protocol/application boundary
- observability restrictions

Implementers own:

- faithful implementation
- invariant evidence
- boundary preservation
- no hidden coupling
- no forbidden observability
- explicit versioning of semantic changes

Applications own:

- application action meaning
- metadata
- UI
- read models
- application policy outside protocol validity

## 9. Future Evolution Rules

Future evolution must:

- preserve invariant meaning where compatibility is claimed
- explicitly version semantic changes
- avoid fossilizing current machinery as protocol law
- prefer additive extension over mutation
- record architectural changes in STATE.md first

## 10. Compatibility Assessment Model

For each proposed change, ask:

1. Which surface changed?
2. Is the surface protocol-owned, implementation-owned, or application-owned?
3. Does the invariant meaning remain the same?
4. Does the change create cross-layer linkage?
5. Does the change expose new observability?
6. Is explicit versioning required?

Classify the change as:

- compatible
- compatible with evidence required
- compatible only under explicit versioning
- protocol-breaking
- out of protocol scope

## 11. Long-Term Conformance Model

A conforming implementation must evidence preservation across:

- identity
- membership
- proof validity
- nullifier uniqueness
- enrollment separation
- REFLECT preservation
- TEMPEST execution
- application adapter boundary
- observability discipline

The long-term model is invariant-based, not implementation-based.

## 12. Conclusion

Privacy Engine compatibility means semantic preservation of the protocol.

It is not defined by code identity, API similarity alone, deployment shape, backend design, UI, database schema, or the petition use case.

Minimum compatibility rule:

    preserve private actors, public actions

Minimum conformance rule:

    preserve protocol invariant meaning with evidence

Minimum evolution rule:

    replace machinery only when meaning is preserved; version meaning changes explicitly
