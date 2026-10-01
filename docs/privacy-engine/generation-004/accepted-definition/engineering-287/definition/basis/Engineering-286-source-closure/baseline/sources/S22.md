# Privacy Engine Protocol Surface V1

STATE.md remains canonical.  
This document is supporting documentation only.

## 1. Why Protocol Surface Matters

The Privacy Engine must be distinguishable from one implementation of it.

A protocol surface defines what another implementation must preserve to remain compatible with the same Privacy Engine.

Implementation machinery may change.  
Protocol commitments must not silently change.

## 2. Protocol Surface vs Implementation

Protocol surface means:

- externally stable compatibility boundary
- invariant-preserving interface
- layer-owned semantic contract
- versioned if changed incompatibly

Implementation means:

- code structure
- storage layout choices
- local orchestration
- deployment topology
- internal helper names
- optimization strategy

Rule:

A surface is protocol-defining only if changing it changes what applications, operators, proofs, or public verifiers may rely on.

## 3. Public Privacy Primitive

The core primitive is:

Private actor proves valid public action.

Stable public commitments:

- anonymous membership validity
- one action per member per action context
- public verification of validity
- no reusable public actor identifier
- application does not learn identity

Not protocol commitments:

- petition-specific UI
- current backend route layout
- current database schema
- current localStorage implementation
- current relayer implementation count

## 4. Enrollment Protocol Surface

Protocol-defining:

- public economic admission exists
- funded rights are economic objects, not identities
- funder is not reliably participant
- activation consumes a right into anonymous membership
- consumption is accounting-only
- no public participant-readiness signal
- no admission identifier may become an action-layer correlation tag

Implementation-defined:

- exact contract module split
- current bond amount
- current signer model for incentive settlement
- current refund-band implementation
- frontend enrollment UX

Versioning required if changed:

- admission becomes wallet-bound
- funder becomes participant by protocol assumption
- consumed rights become public participant labels
- admissionCommitment becomes action correlation material

## 5. M2 Protocol Surface

Protocol-defining:

- identity is memberSecret-derived
- leaf = Poseidon1(memberSecret)
- continuity = possession of same memberSecret
- no wallet-based identity recovery
- O-state semantics are observable-state only
- enrollment attaches to present secret only

Implementation-defined:

- browser storage key
- import/export UI
- encrypted bundle UX
- component structure
- local status wording

Versioning required if changed:

- identity becomes wallet-derived
- backend can recover identity
- secret continuity semantics change
- leaf derivation changes

## 6. ZK Protocol Surface

Protocol-defining:

- proof proves membership without revealing identity
- on-chain verification is authoritative
- public input order:
  1. nullifier
  2. petitionId/actionId
  3. membershipRoot
- root validity is enforced
- proof artifact provenance is mandatory

Implementation-defined:

- proving UI placement
- frontend proof-generation wrapper
- build scripts
- local artifact paths

Versioning required if changed:

- circuit semantics
- verifier encoding
- public input order
- proving system
- root validity model
- artifact manifest rules

## 7. Nullifier Protocol Surface

Protocol-defining:

- nullifier = Poseidon3(memberSecret, actionId, SIGN_DOMAIN)
- uniqueness is per `(actionId, member)`
- uniqueness is not wallet-based
- nullifier is the sole action-layer duplicate-prevention primitive
- nullifiers must not create cross-action linkage

Implementation-defined:

- naming of petitionId vs actionId in adapters
- frontend duplicate-state display
- backend preflight checks

Versioning required if changed:

- nullifier derivation
- domain separation
- uniqueness scope
- duplicate enforcement authority

## 8. REFLECT Protocol Surface

Protocol-defining:

- REFLECT owns path / witness-data acquisition
- selected state must be preserved
- deterministic state targeting
- integrity and coherence verification
- no cross-state mixing
- fallback must not reselect truth
- mirrors are replaceable acquisition surfaces, not authorities

Implementation-defined:

- local service layout
- chunk storage mechanics
- mirror deployment details
- backend orchestration
- internal object serialization, unless externally committed

Versioning required if changed:

- selection authority
- state validity rules
- cross-state mixing rule
- fallback semantics
- acquisition target contract

## 9. TEMPEST Protocol Surface

Protocol-defining:

- TEMPEST owns execution / submission
- canonical submission payload is frozen at execution boundary
- execution path must not expose identity material
- deterministic selection / fallback
- public response must not expose slot, domain, relayer, permutation, or fallback path
- success means protocol-level accepted submission, not topology disclosure

Implementation-defined:

- number of live wallets in current deployment
- local orchestration process
- RPC provider layout
- environment variable names
- readiness helper internals

Versioning required if changed:

- canonical submission payload
- execution-boundary visibility
- deterministic fallback semantics
- public relay response semantics
- topology exposure policy

## 10. Application Adapter Protocol Surface

Protocol-defining:

- application supplies action context
- application receives public action result
- application must not redefine identity, membership, nullifier, proof, REFLECT, or TEMPEST semantics
- application may define product meaning of the public action

For petitions:

- petitionId is the action context
- signature is the public action

For another adapter:

- actionId may represent another public action type
- privacy primitive remains unchanged

Implementation-defined:

- UI
- metadata schema
- product read model
- action labels
- adapter-specific routing

Versioning required if changed:

- application can weaken privacy semantics
- application can reinterpret member identity
- application can introduce cross-action join keys
- application can bypass protocol duplicate-prevention rules

## 11. Compatibility-Preserving Changes

Compatible changes include:

- replacing internal backend services
- changing database schema
- changing frontend components
- adding new application adapters that preserve protocol boundaries
- changing mirror or relay implementation machinery
- improving proof-generation ergonomics without changing proof semantics
- changing deployment topology without exposing new protocol surfaces
- replacing internal REFLECT acquisition machinery while preserving target/state rules
- replacing internal TEMPEST execution machinery while preserving canonical submission and response rules

## 12. Compatibility-Breaking Changes

Breaking changes include:

- changing leaf derivation
- changing nullifier derivation
- changing public proof inputs
- changing root validity semantics
- allowing wallet-based identity continuity
- carrying admission identifiers into action events
- allowing REFLECT fallback to choose a different truth state
- exposing TEMPEST topology or per-action execution path
- allowing application adapters to redefine privacy semantics
- making backend authoritative over membership, signing, or identity

## 13. Internal Replaceable Machinery

The following must remain internal unless explicitly promoted:

- current React component structure
- localStorage key shape
- current Express routes
- SQLite tables
- indexer implementation
- relayer wallet count
- RPC provider split
- REFLECT service file names
- TEMPEST helper names
- deployment scripts
- current petition metadata decoding

These may be important implementation details.

They are not automatically protocol commitments.

## 14. Protocol Surface Assessment

Minimum stable Privacy Engine compatibility boundary:

1. Enrollment creates anonymous membership without reliable public participant attribution.
2. M2 identity is secret-derived, not wallet-derived.
3. ZK validity proves membership and action validity without revealing identity.
4. Nullifier enforces one action per member per action context.
5. REFLECT preserves selected witness-data truth without provider authority.
6. TEMPEST submits canonical actions without exposing execution topology.
7. Application adapters consume the primitive but do not redefine it.

Protocol surface:

Enrollment -> M2 -> ZK validity -> Nullifier -> REFLECT -> TEMPEST -> Application Adapter

Implementation surface:

Everything that can change while preserving the above sequence and invariants.

## 15. Conclusion

The Privacy Engine protocol surface is the minimum set of interfaces required to preserve:

Private actors, public actions.

The stable protocol is not the current petition app.

The stable protocol is:

- anonymous admission into membership
- secret-derived identity
- proof-based validity
- nullifier-based uniqueness
- verified path acquisition
- topology-hidden execution
- application-bounded public action semantics

Current implementation details should not be promoted into protocol commitments unless they are necessary for compatibility, privacy, or verification.

Engineering[69] conclusion:

The Privacy Engine now has a bounded protocol surface.

Future work may replace machinery inside layers.

Future work must version changes that alter layer-owned protocol semantics.
