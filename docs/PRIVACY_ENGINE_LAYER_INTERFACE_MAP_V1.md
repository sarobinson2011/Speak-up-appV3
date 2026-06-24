# Privacy Engine Layer Interface Map V1

STATE.md remains canonical.  
This document is supporting documentation only.

## 1. Why Layer Interfaces Matter

The privacy engine is only modular if each layer owns a narrow responsibility and exposes only the information required by the next layer.

A layer interface defines:

- what information may cross a boundary
- what information must remain local
- what public artifacts are allowed
- what must remain replaceable behind the boundary

The rule is:

    A layer may consume the minimum preserved output of the previous layer.
    It must not inherit the previous layer’s provenance, operator context, wallet context, timing context, or internal machinery.

## 2. Interface Map Overview

Privacy engine layers:

    Enrollment
      -> Anonymous Membership / M2
      -> ZK validity layer
      -> Nullifier layer
      -> REFLECT
      -> TEMPEST
      -> Chain verification
      -> Application adapter

Reference adapter:

    Petitions

Petitions consume the privacy engine.  
Petitions do not define the privacy engine.

## 3. Enrollment → M2 Boundary

Enrollment owns:

- public economic admission
- bonded admission rights
- admission-right lifecycle
- refund / consumption accounting

Allowed crossing:

- valid activation of a funded right
- creation of one membership leaf
- accounting-only consumed state

Forbidden crossing:

- funding wallet
- sponsor identity
- admission provenance
- public participant-readiness signal
- right-to-participant mapping
- cohort or batch marker
- admissionCommitment as action-layer correlation tag

Stable interface:

    funded right + private activation material -> membership leaf admission

Replaceable implementation:

- bond amount
- lock period
- refund mechanics
- incentive settlement authority
- admission contract implementation

## 4. M2 → ZK Boundary

M2 owns:

- memberSecret possession
- leaf derivation
- membership inclusion identity
- O0 / O1 / O2 operator state

Allowed crossing:

- private witness material into local proof generation:
  - memberSecret
  - Merkle path
  - leaf-related witness data
- public proof target material:
  - petition/action id
  - current membership root

Forbidden crossing:

- wallet identity as anonymous identity
- backend identity inference
- admission provenance
- secret recovery semantics
- sponsor or funding context

Stable interface:

    memberSecret + valid path + action context -> proof witness

Replaceable implementation:

- frontend storage mechanism
- custody/export UI
- local proof-generation implementation
- membership path delivery substrate

## 5. ZK → Verification Boundary

ZK owns:

- proof construction
- circuit validity
- public/private input separation
- artifact integrity

Allowed crossing to verification:

- Groth16 proof
- public inputs in locked order:
  1. nullifier
  2. petitionId / actionId
  3. membershipRoot

Forbidden crossing:

- memberSecret
- leaf
- Merkle path
- wallet address
- admissionCommitment
- relay choice
- REFLECT mirror choice
- TEMPEST slot/domain choice

Stable interface:

    proof + [nullifier, actionId, membershipRoot]

Replaceable implementation:

- proving implementation
- verifier implementation after controlled artifact regeneration
- future proof system, if it preserves the same interface semantics

## 6. Nullifier Boundary

Nullifier owns:

- uniqueness per anonymous member per action
- duplicate prevention
- public one-use marker

Canonical derivation:

    nullifier = Poseidon3(memberSecret, actionId, SIGN_DOMAIN)

Allowed crossing:

- nullifier as public uniqueness key
- action id
- domain separator

Forbidden crossing:

- reusable cross-action identity
- leaf as action identity
- admissionCommitment as action identity
- wallet-derived uniqueness
- backend-enforced identity uniqueness

Stable interface:

    anonymous member + action id -> one public nullifier

Replaceable implementation:

- hash implementation only through explicit cryptographic redesign
- storage/indexing implementation of used nullifiers

## 7. REFLECT → Proof Generation Boundary

REFLECT owns:

- path / witness-data acquisition
- publication-state selection
- integrity verification
- coherence verification
- no cross-state mixing
- no global reshuffle during fallback

Allowed crossing:

- proof-compatible Merkle path material
- selected membership root
- required witness data for local proving

Forbidden crossing:

- mirror topology
- mirror identity as authority
- provider trust as validity
- request history
- path telemetry
- identity tracking
- petition-linked path tracking
- mixed publication states
- repaired or inferred witness state

Stable interface:

    selected valid publication state -> coherent path material

Replaceable implementation:

- mirror implementation
- chunk layout
- connector format
- local publication representation
- fetch policy, if selected-state preservation is unchanged

## 8. Client → TEMPEST Boundary

Client owns:

- proof generation
- construction of the canonical action submission
- submission request to the execution layer

Allowed crossing:

- petition/action id
- nullifier
- proof pA / pB / pC
- ordered public signals
- fixed zero admissionCommitment where required by current payload shape

Forbidden crossing:

- memberSecret
- leaf
- Merkle path
- wallet identity as signer identity
- local storage state
- REFLECT mirror choices
- request provenance beyond unavoidable transport metadata
- operator identity lifecycle state

Stable interface:

    canonical proof submission payload

Replaceable implementation:

- client framework
- local proof-generation library
- transport wrapper
- adapter UI

## 9. TEMPEST → Chain Boundary

TEMPEST owns:

- execution / submission
- deterministic relay selection
- fallback traversal
- topology hiding
- relay-domain abstraction

Allowed crossing to chain:

- contract call:
  - action id
  - nullifier
  - proof
  - public signals
- relayer wallet as transaction sender

Forbidden crossing:

- user wallet as action sender
- selected slot
- execution domain
- relay permutation
- fallback path
- seed
- relay topology
- relay reputation
- relay-linked action history

Stable interface:

    validated canonical submission -> on-chain verification transaction

Replaceable implementation:

- relay wallets
- RPC providers
- execution domains
- relay orchestration
- future distributed relayer substrate

## 10. Privacy Engine → Application Adapter Boundary

The privacy engine owns:

- anonymous membership
- proof validity
- nullifier uniqueness
- path acquisition
- execution submission
- privacy-preserving public action primitive

The application adapter owns:

- application-specific action meaning
- petition metadata
- petition creation
- petition display
- adapter-specific read model
- user-facing product flow

Allowed crossing:

- verified action result
- action id
- nullifier-used state
- signature/action count
- application metadata outside the privacy proof

Forbidden crossing:

- application semantics redefining identity
- petition logic redefining nullifier semantics
- adapter-specific identifiers entering M2 identity
- adapter-specific metadata entering proof identity
- application-level provenance becoming protocol authority

Stable interface:

    private actor proves valid public action

Replaceable implementation:

- petitions adapter
- future coordination adapter
- future voting/signaling/funding adapter
- frontend product surface
- read-model presentation

## 11. Forbidden Crossings

The following must never cross layer boundaries as protocol authority or reusable correlation material:

- memberSecret
- wallet address as anonymous identity
- funding wallet as participant identity
- admissionCommitment as action-layer tag
- leaf as public action identity
- Merkle path outside proof-generation need
- backend-inferred identity
- sponsor provenance
- relay slot
- relay domain
- relay permutation
- REFLECT mirror identity as authority
- publication-state mixing
- request history
- telemetry that links path acquisition to action submission
- application metadata that redefines privacy-engine identity

## 12. Stable Interfaces

Stable protocol interfaces:

1. Admission creates eligibility for membership without exposing participant identity.
2. M2 identity is memberSecret -> leaf.
3. Proof generation consumes secret, path, action id, and root locally.
4. Verification consumes proof plus public inputs.
5. Nullifier enforces one action per anonymous member per action id.
6. REFLECT supplies coherent path material for a selected state.
7. TEMPEST submits canonical proof payloads without exposing user wallet identity.
8. Application adapters consume verified public actions.

## 13. Replaceable Implementations

Replaceable behind stable interfaces:

- admission contract implementation
- bond economics
- incentive authority
- frontend custody UI
- proving library
- future proof system
- REFLECT mirror implementation
- REFLECT object/chunk implementation
- TEMPEST relay implementation
- RPC providers
- relayer wallets
- backend indexing implementation
- petition adapter

Not replaceable without protocol review:

- memberSecret identity model
- leaf derivation semantics
- nullifier semantics
- public input meaning/order
- no wallet-based anonymous identity
- no admission-to-action correlation tag
- REFLECT selected-state preservation
- TEMPEST topology hiding
- adapter boundary

## 14. Interface Boundary Assessment

The privacy engine boundary is coherent.

Each layer has a narrow output:

- Enrollment outputs eligibility converted into membership.
- M2 outputs anonymous membership witness capability.
- ZK outputs proof validity.
- Nullifier outputs uniqueness.
- REFLECT outputs coherent witness data.
- TEMPEST outputs execution without user-wallet submission.
- Chain outputs authoritative verification and uniqueness enforcement.
- Adapter outputs application-specific meaning.

The strongest boundary rule is:

    No layer may carry provenance from a previous layer unless that provenance is itself the explicit stable interface.

For this engine, provenance is almost always forbidden.

## 15. Conclusion

Engineering[68] defines the privacy engine’s stable information-flow boundaries.

The privacy engine is not the petition app.

The privacy engine is the layered protocol that allows:

    private actors -> public valid actions

The application adapter may decide what an action means.

It must not decide what identity means.

It must not redefine membership, proof validity, nullifier uniqueness, REFLECT preservation, or TEMPEST execution semantics.

Result:

    The privacy engine boundary is identifiable.
    The layer interfaces are now mappable.
    The implementations behind those interfaces remain replaceable.
