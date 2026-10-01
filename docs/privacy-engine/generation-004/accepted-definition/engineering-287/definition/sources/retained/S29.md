# Privacy Engine Application Adapter Contract V1

STATE.md remains canonical.

This document is supporting documentation only.  
If this document conflicts with STATE.md, STATE.md wins.

## 1. Why an Application Adapter Exists

An Application Adapter exists because the Privacy Engine must be usable by many application types without becoming those applications.

The adapter is the narrow boundary where an external application supplies action intent and receives public action outcome.

It prevents two failures:

1. application logic becoming protocol authority
2. protocol machinery absorbing application semantics

The adapter answers:

> how does an application use the Privacy Engine without redefining it?

## 2. Privacy Engine Ownership

The Privacy Engine owns:

- anonymous membership identity
- enrollment/admission boundary
- member secret -> leaf semantics
- nullifier derivation semantics
- ZK proof validity
- root validity
- uniqueness enforcement
- path/witness-data acquisition semantics
- execution/submission semantics
- privacy-layer observability rules
- failure semantics inside protocol layers

The Privacy Engine does not own:

- application purpose
- application metadata
- application-specific display
- application-specific business rules
- application-specific read models
- application-specific interpretation of public outcomes

Core rule:

> The Privacy Engine proves and submits valid private participation.  
> It does not decide what the application means.

## 3. Application Ownership

The application owns:

- application object type
- application object creation
- application metadata
- application-specific read surface
- application-specific UI
- application-specific outcome interpretation
- application-level authorization unrelated to anonymous action validity
- product-specific lifecycle

For the current reference application, this means petitions own:

- petition creation
- petition title/description/metadata
- petition list presentation
- petition-specific display semantics
- signature-count presentation

But petitions do not own:

- anonymous identity
- proof validity
- nullifier semantics
- path selection
- relay selection
- execution fallback
- protocol observability policy

## 4. Stable Adapter Boundary

The stable adapter boundary is:

Application intent  
-> protocol action request  
-> Privacy Engine validation/submission  
-> public verifiable result  
-> application read interpretation

The application may request that a private actor perform a public action.

The Privacy Engine determines whether the anonymous participant can validly perform that action.

The application may consume the result.

The application must not inspect, reshape, or control the hidden protocol machinery used to produce the result.

## 5. Information Flow Across the Boundary

Allowed application -> protocol inputs:

- action identifier
- public application target
- application-defined public metadata reference, where applicable
- operator request to perform an action
- protocol-compatible proof payload produced by the client/prover path

Allowed protocol -> application outputs:

- accepted/rejected action result
- public transaction result
- public action event
- application-safe aggregate state
- coarse readiness where required

Forbidden boundary flow:

- memberSecret
- admissionSecret
- wallet-derived identity continuity
- relay slot
- relay permutation
- REFLECT mirror topology
- path request history
- execution fallback path
- private identity provenance
- admission-to-action linkage
- any reusable cross-action identity tag

## 6. Visible Protocol Interfaces

Applications may depend on only stable protocol-facing concepts:

- enrollment produces anonymous membership capability
- membership is represented by leaf inclusion
- private action validity is proven by ZK proof
- uniqueness is enforced by nullifier
- action validity is publicly verifiable
- accepted actions become public actions
- read models may expose application-safe public results

Current visible reference surfaces include:

- petition creation/read APIs
- membership readiness/leaf status at coarse level
- proof-compatible signing request
- public signature count
- transaction outcome

These are adapter-visible because the application needs them to operate.

## 7. Hidden Protocol Interfaces

Applications must not depend on:

- M2 secret custody internals
- enrollment secret material
- internal REFLECT envelopes
- REFLECT connector/chunk selection
- REFLECT fallback selection
- REFLECT publication-state internals
- TEMPEST seed derivation
- TEMPEST slot permutation
- TEMPEST relay-domain mapping
- TEMPEST fallback traversal
- relayer wallet selection
- backend/indexer internal state beyond stable read APIs
- ZK artifact implementation details beyond locked public input contract

Hidden means:

> replaceable without application redesign.

## 8. Adapter Compatibility Requirements

An adapter is compatible if it preserves the following:

1. It treats anonymous identity as protocol-owned.
2. It treats nullifier uniqueness as protocol-owned.
3. It never introduces wallet-based continuity.
4. It never introduces action-to-admission linkage.
5. It never observes or requires execution topology.
6. It never observes or requires path topology.
7. It consumes only public action results.
8. It separates application metadata from protocol identity.
9. It does not convert protocol failure into application-side inference.
10. It can be replaced without changing M2, ZK, REFLECT, TEMPEST, or enrollment semantics.

## 9. Forbidden Adapter Responsibilities

An adapter must not:

- derive identity
- restore identity
- infer continuity
- bind anonymous action to wallet
- bind anonymous action to admission funding
- store member secrets
- store admission secrets
- choose REFLECT mirrors
- choose TEMPEST relayers
- inspect relay fallback
- inspect witness/path internals
- reinterpret nullifiers
- override proof validity
- create protocol-side reputation
- create provenance records
- add correlation keys
- require implementation-specific internal data

Forbidden path:

Application asks:

> who is this actor?

Valid path:

Application asks:

> did a valid private actor perform this public action?

## 10. Adapter Replaceability

The adapter must be replaceable.

A petition adapter, voting adapter, coordination adapter, funding adapter, or login adapter should all be able to use the same Privacy Engine boundary.

Replaceability requires:

- same protocol validity model
- same anonymous membership model
- same nullifier discipline
- same hidden execution/path machinery
- application-specific object semantics outside the protocol

Adapter replacement must not require:

- ZK redesign
- nullifier redesign
- enrollment redesign
- REFLECT redesign
- TEMPEST redesign
- identity model redesign

## 11. Compatibility-Preserving Changes

The following are compatibility-preserving:

- replacing application UI
- changing application metadata shape
- adding new application object types
- changing application read presentation
- replacing internal REFLECT implementation while preserving path semantics
- replacing internal TEMPEST implementation while preserving execution semantics
- upgrading ZK implementation while preserving public validity contract
- changing backend implementation while preserving stable adapter-visible APIs
- adding application-specific indexing that consumes only public events

## 12. Compatibility-Breaking Changes

The following are compatibility-breaking:

- changing memberSecret -> leaf semantics
- changing nullifier semantics
- changing public input order without protocol migration
- exposing relay topology to applications
- exposing mirror topology to applications
- making application metadata part of identity semantics
- making wallet identity part of anonymous identity
- making admission funding part of action identity
- requiring applications to understand REFLECT internals
- requiring applications to understand TEMPEST internals
- allowing applications to decide proof validity
- allowing applications to reinterpret uniqueness

## 13. Adapter Contract Assessment

The minimum stable adapter contract is:

Application owns public purpose.  
Privacy Engine owns private validity.

Application supplies:

- public action target
- application-specific public metadata
- request to perform action

Privacy Engine supplies:

- anonymous membership validity
- proof validity
- uniqueness enforcement
- path acquisition
- execution/submission
- public verifiable result

Application observes:

- public action result
- public aggregate state
- protocol-safe readiness

Application must not observe:

- private identity material
- protocol routing internals
- path internals
- relay internals
- provenance bridges
- cross-action identity tags

In symbolic form:

Application chooses A.  
Privacy Engine validates private right to perform A.  
Public chain records performed(A).

Valid:

A -> private-valid(A) -> public-action(A)

Forbidden:

A -> infer(actor)  
A -> infer(wallet)  
A -> infer(admission source)  
A -> choose protocol route  
A -> redefine nullifier  
A -> redefine membership

## 14. Conclusion

The Application Adapter is the contract between external use cases and the Privacy Engine.

It preserves the distinction:

- application = public meaning
- protocol = private validity

The Privacy Engine must remain application-agnostic.

The application must remain protocol-non-authoritative.

The stable boundary is therefore:

> Applications define what public action exists.  
> The Privacy Engine defines whether a private actor may validly perform it.

This preserves:

- protocol ownership
- application replaceability
- layer independence
- privacy boundary discipline
- future application portability

Engineering[70] conclusion:

The minimum stable Application Adapter Contract is now identified.

The next application built on top of the Privacy Engine should integrate through this adapter boundary, not through M2, enrollment, REFLECT, TEMPEST, or ZK internals.
