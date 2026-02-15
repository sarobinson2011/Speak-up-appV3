“When in doubt, STATE.md wins.”
“Changes must be recorded here before implementation.”

STATE.md — Speak-up-appV3

Last updated: 2026-02-15 (Europe/London)

This file is the canonical “source of truth” for current architecture decisions, invariants, versions, and the next concrete steps. When something changes in design or build/toolchain, update this file and commit it.

1) Project goal

Build a privacy-preserving petition signing system (with optional commenting) that supports:

Client-side ZK proof generation

On-chain verification (EVM)

Minimal trust assumptions and strong privacy defaults

2) Core product rules (invariants)

Uniqueness rule: One sign (+ optional comment) per petition per user, enforced via nullifier, not via wallet address.

Privacy rule: Users prove eligibility/membership without revealing identity.

Verification rule: On-chain verification is the authority; the chain verifies proofs and checks nullifiers.

No trusted gatekeeper (baseline): membership does not require email/SSO or any trusted issuer. Membership is permissionless via an on-chain registration transaction. Backend is non-authoritative.

3) ZK stack (current)

Circuit framework: Circom

Proof system: Groth16

Tooling: snarkjs

Hashing (in-circuit): Poseidon (SNARK-friendly)

Notes:

Groth16 proof size is constant w.r.t. circuit size; proving time increases with circuit constraints.

Merkle inclusion proof length scales as log2(n) (tree depth).

4) Membership + Merkle tree model (Baseline: Model A + 1A + 2B + DEPTH=16)
4.1 Membership identity material

Client generates: memberSecret locally (random 31-byte value; interpreted as a BN254 field element). Never leaves device.

Leaf definition (locked): leaf = Poseidon1(memberSecret).

4.2 Registration (permissionless; on-chain; no gatekeeper)

User becomes a member by calling the membership contract:

Function (locked): registerLeaf(leaf) (exact type bytes32 or uint256, but consistent across stack)

Sybil friction (locked, iteration 1): registration requires a refundable bond (see §6)

Wallet anchoring (locked for iteration 1): one active leaf per wallet (prevents one wallet registering many leaves cheaply)

Contract must:

record the wallet→leaf association for the active membership

incorporate the leaf into membership set / root update

emit registration + root update events

4.3 Tree depth (locked)

Merkle depth: DEPTH = 16 (≈ 65,536 leaves)

4.4 Root validity model (locked: 1A, last N roots)

Merkle root changes as new leaves register/unregister. Proofs must not be flaky due to root churn.

Baseline rule: proofs are valid if the public input membershipRoot is in the contract’s valid root set.

Implementation (locked): contract stores the last N roots in a ring-buffer/set.

N = 16 (baseline; adjustable later)

On root update: add new root; evict oldest if ring-buffer full

Contract exposes either:

isValidRoot(root) -> bool, or

validRoots(root) -> bool mapping getter

4.5 Merkle path distribution model (locked: 2B, backend convenience)

Client needs membership path (siblings + indices) to generate proof.

Baseline: backend provides convenience endpoints returning Merkle path data for a given wallet/leaf.

Backend is dumb / non-authoritative: it mirrors on-chain events, rebuilds the tree, and serves:

current root + recent roots

membershipPath[], membershipIndices[], and leafIndex for the wallet’s leaf

Safety: client must only prove against a root accepted by the contract (membershipRoot ∈ validRoots).

5) Nullifier model (anti double-signing)

Concept: a per-(user, petition) unique value revealed publicly, without revealing identity.

Baseline form (locked, domain-separated):

nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)

SIGN_DOMAIN = 0x5349474e (ASCII "SIGN") as a constant field element

On-chain: store nullifier in a mapping/set; reject if already seen for that petition.

Example: usedSignNullifier[petitionId][nullifier] = true

Planned decision points (TBD but must be made before circuit/contract freeze):

petitionId encoding (u32/u64) and field packing rules (must match circuit + Solidity types exactly).

6) Sybil / spam / DDOS posture (minimal baseline, iteration 1 locked)

Problem:

Permissionless membership is Sybil-prone (cheap wallet creation).

Baseline mechanism (locked, iteration 1):

Refundable membership bond (Option 1):

User must post a bond when registering a leaf: registerLeaf(leaf) is payable and requires exact bond amount.

Refund is only possible via unregister: user calls unregisterAndRefund() which removes/deactivates membership and returns the bond.

This preserves friction while avoiding a permanent paywall.

Contract requirements:

store bond balance per wallet (or fixed-bond flag)

enforce one active leaf per wallet

unregisterAndRefund() updates membership state + root, then refunds bond

Future iterations (explicitly allowed; do not bake in now):

adjust bond amount dynamically

add client-side PoW to registration

add rate limiting / per-epoch membership

optional issuer/SSO mode as a separate product mode (not baseline)

7) Client performance assumptions

Main cost drivers for client-side proving:

total circuit constraints

Merkle depth × Poseidon hash cost

Merkle scaling is favorable: each doubling of members adds ~1 hash level.

Target UX: “smooth enough” for typical laptops; mobile later.

8) Implementation skeleton (high level)
Client

Generate and store memberSecret locally

Compute leaf = Poseidon(memberSecret)

Register leaf on-chain with bond

Fetch current valid root(s) (contract and/or backend convenience)

Fetch Merkle path from backend (convenience)

Build witness: (memberSecret, petitionId, membershipRoot, membershipPath, membershipIndices, …)

Generate Groth16 proof in browser

Submit: proof + public inputs (petitionId, membershipRoot, nullifier, …)

On-chain

Membership contract:

accept registerLeaf(leaf) with bond

accept unregisterAndRefund()

maintain Merkle root + last N roots

emit events for indexing

Petition/registry contract (or combined contract):

verify Groth16 proof

check membershipRoot is valid

check nullifier unused; mark used

emit PetitionSigned event

Backend (dumb / non-authoritative)

Mirror on-chain events (LeafRegistered, LeafUnregistered, RootAdded, PetitionSigned)

Rebuild Merkle tree and serve membership paths + convenience metadata

Must not gate membership or signing

9) Build / toolchain thread (placeholders)

Fill these in as you lock them down:

Repo path(s): ________________________________

Node version: ________________________________

Circom version: ________________________________

snarkjs version: ________________________________

Powers of Tau ceremony file: ________________________________

zkey / verification key locations: ________________________________

Solidity verifier generation steps: ________________________________

Deployment network + addresses: ________________________________

10) Current focus + next steps

Current focus:

Implement the baseline membership model cleanly: on-chain leaf registration w/ refundable bond, last-N root validity, backend-served Merkle paths.

Next concrete steps:

 Finalize minimal membership contract interface:

registerLeaf(leaf) payable

unregisterAndRefund()

isValidRoot(root) (or validRoots[root])

events: LeafRegistered, LeafUnregistered, RootAdded, BondRefunded

 Finalize minimal petition signing interface:

verifyAndSign(petitionId, membershipRoot, nullifier, proof, publicSignals)

event: PetitionSigned(petitionId, nullifier, ...)

 Define exact petitionId encoding rules and match across circuit/Solidity/frontend.

 Backend: index leaf/root events → serve {root(s), path, indices, leafIndex}.

 Client: generate/store secret, register, fetch path, prove, submit.

11) Notes (personal / operating constraints)

Sleep quality matters for productivity; avoid late stimulants.

Bedtime black tea swapped to milk; alcohol timing reduction improved sleep and reduced “full wake” on night bathroom trips.

12) Changelog

2026-02-14: Initial STATE.md created. Captures core ZK stack (Circom/snarkjs/Groth16/Poseidon), Merkle membership concept, nullifier uniqueness model, and anti-sybil options.

2026-02-15: Baseline locked: permissionless on-chain membership (leaf = Poseidon(memberSecret)), DEPTH=16, root validity = last N roots (N=16), backend as dumb convenience for paths/metadata, and Sybil friction iteration 1 = refundable membership bond with refund only via unregister.