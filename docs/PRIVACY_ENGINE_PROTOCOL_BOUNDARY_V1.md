# PRIVACY_ENGINE_PROTOCOL_BOUNDARY_V1

## 1. Why a Privacy Engine Exists

The privacy engine exists to provide one reusable protocol capability:

> private actors, public actions.

Applications need public verifiability without public actor attribution.

The engine therefore owns the machinery that allows an action to be accepted as valid, unique, and authorized while preserving ambiguity about which private participant performed it.

Petitions are the first reference application. They are not the protocol.

## 2. Privacy Engine Boundary

The privacy engine is the bounded protocol substrate that turns:

    private membership + valid proof + public action intent

into:

    publicly verifiable action acceptance without actor disclosure

The privacy engine owns:

- anonymous identity primitives
- enrollment/admission semantics
- membership validity
- nullifier uniqueness
- proof verification semantics
- witness/path acquisition semantics
- submission/execution semantics
- privacy-preserving boundary rules between those layers

The privacy engine does not own:

- petition meaning
- application-specific metadata
- application UI
- application business logic
- application moderation
- application-specific ranking, display, or interpretation
- social meaning of the public action

## 3. Layers Inside the Privacy Engine

Inside the privacy engine:

1. Enrollment / admission layer
2. Anonymous membership layer
3. ZK proof layer
4. Nullifier layer
5. REFLECT
6. TEMPEST
7. Non-authoritative backend support

## 4. Layers Outside the Privacy Engine

Outside the privacy engine:

- petition creation semantics
- petition titles/descriptions/metadata
- application routing
- frontend presentation
- public read models
- application-specific counters
- application-specific eligibility language
- social policy
- moderation
- ranking
- discovery
- governance of application content

## 5. Layer Ownership Model

Enrollment owns admission friction.
It must not own anonymous identity.

M2 owns anonymous identity.
It must not own funding provenance.

The ZK layer owns private validity proof.
It must not own application meaning.

The nullifier layer owns uniqueness.
It must not own identity recovery or human uniqueness.

REFLECT owns witness-data acquisition.
It must not own truth selection beyond its locked preservation semantics.

TEMPEST owns execution/submission.
It must not own action validity.

The application owns meaning.
It must not own privacy semantics.

## 6. Forbidden Layer Knowledge

Forbidden knowledge bridges:

- wallet → anonymous identity
- funder → participant
- admission right → public action actor
- backend request → identity
- relay path → participant
- mirror access → participant
- application metadata → protocol identity
- petition action → reusable public participant tag

## 7. Stable Protocol Surfaces

Stable protocol surfaces:

- memberSecret → leaf
- leaf membership inclusion
- nullifier derivation
- proof public input meaning
- on-chain proof verification
- nullifier uniqueness
- admission-right accounting separation
- REFLECT selected-state preservation
- TEMPEST deterministic execution/fallback boundary
- backend non-authority
- application adapter boundary

## 8. Replaceable Components

Replaceable components include:

- proving system implementation
- verifier implementation
- hash implementation (through explicit protocol migration)
- relay infrastructure
- mirror infrastructure
- backend implementation
- indexer implementation
- frontend framework
- application use case
- petition-specific contract surfaces
- policy modules that do not redefine core privacy semantics

## 9. Application Adapter Boundary

The application adapter is the boundary between:

    privacy engine action validity

and:

    application-specific action meaning

For petitions:

    valid anonymous action
        →
    petition signature

The adapter may define what an action means.

It must not define who the private actor is.

## 10. Future Cryptographic Replaceability

Stable semantics:

- prove valid private membership
- prove correct nullifier
- expose only required public signals
- preserve one-action uniqueness
- reveal no actor identity

Replaceable internals:

- Groth16
- Circom
- BN254
- verifier contract shape
- proving artifacts
- future proof systems

A replacement is valid only if application semantics do not change.

## 11. Protocol Boundary Assessment

The privacy engine boundary is:

Enrollment
    admits economic participation

M2
    defines private membership identity

ZK
    proves private validity

Nullifier
    enforces scoped uniqueness

REFLECT
    preserves witness-data acquisition semantics

TEMPEST
    preserves submission/execution semantics

Application Adapter
    maps valid anonymous action into application meaning

Petitions sit above the adapter.

They are not the engine.

## 12. Conclusion

The privacy engine is the modular protocol layer that lets applications accept public actions from private actors.

Its stable core is:

- private membership
- public validity
- scoped uniqueness
- non-attribution
- replaceable infrastructure
- application-independent semantics

The protocol boundary is clean if:

- applications can change without changing M2/TEMPEST/REFLECT/nullifiers
- infrastructure can evolve without changing action semantics
- cryptography can be upgraded without changing application meaning
- no layer gains forbidden knowledge from another layer

Speak-up is not merely a petitions app.

Petitions are the first adapter.

The architectural center is the privacy engine.
