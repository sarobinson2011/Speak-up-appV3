# STATE.md — Speak-up-appV3

Last updated: 2026-02-27 (Europe/London)

This file is the canonical source of truth for:

- Architecture decisions
- Invariants
- Deployed addresses
- ZK stack configuration
- Development governance model

When in doubt, STATE.md wins.
Changes must be recorded here before implementation.

---

# 0) Development Governance Model (Locked)

Baseline anchor (ground truth):

- Tag: baseline-v0
- Commit: e02aacdc0f10e6919d8a759d8829758b58e0367e

Current main includes baseline via merge commit:

- 0ecd367 on origin/main

Two-track development model:

## Human Track (main)

- Only Steve (human) develops on main
- Assisted by GPT in Engineering[5]
- Slow, deterministic, minimal diffs
- No speculative expansion
- Cryptographic correctness is paramount
- STATE.md must be updated before architectural changes

## Agent Track (separate machine)

- Agent NEVER checks out or commits to main
- One branch per iteration
- Branches created fresh from baseline-v0 (preferred)
- Naming convention:
  - agent/iter-0001-<desc>
  - agent/iter-0002-<desc>
- Human reviews before merge
- No automatic merges
- No silent merges

This separation is non-negotiable.

---

# 1) Project Goal (M2-only MVP)

Build a privacy-preserving petition platform where users can:

- Create petitions (wallet-authenticated; not private in MVP)
- Sign petitions with Strong Privacy (M2):
  - proof generated client-side
  - on-chain verification authoritative
  - uniqueness enforced via nullifier (not wallet address)

Comments are disabled in MVP.

---

# 2) Core Product Invariants (Locked)

1) Uniqueness:
- Max 1 signature per (petitionId, member)
- Enforced via nullifier
- Not wallet-based

2) Privacy:
- Signer proves membership without revealing identity

3) On-chain authority:
- Chain verifies proof validity
- Chain validates root validity
- Chain enforces nullifier uniqueness

4) No trusted gatekeeper:
- Membership is permissionless on-chain
- Backend is non-authoritative convenience only

5) M2-only mode:
- No email verification
- No JWT
- No attestations
- No M1 routes/UI

---

# 3) ZK Stack (Current, Locked)

Circuit framework: Circom
Prover/verifier: Groth16 (BN254)
Tooling: snarkjs

Hashing: Poseidon
- leaf: Poseidon1
- merkle node: Poseidon2
- nullifier: Poseidon3

SIGN_DOMAIN:
0x5349474e  // ASCII "SIGN"

Tree depth:
DEPTH = 16

Root history window:
N = 16

Full implementation spec:
See ZK_CIRCUIT_SPEC.md

---

# 4) ZK Artifact Integrity (Engineering[5])

Artifact reproducibility and tamper detection are mandatory.

Specification:
docs/ZK_ARTIFACT_PROVENANCE.md

This document defines:

- ZK_ARTIFACTS_MANIFEST.json
- Required pinned artifacts
- SHA-256 hashing rules
- Golden proof requirement
- CI enforcement rules
- Public input order lock

Public input order (locked):
1. petitionId
2. nullifier
3. membershipRoot

No circuit, key, verifier, or encoding change is allowed without:
- Regeneration
- Manifest update
- Explicit commit
- Golden proof passing

---

# 4.6) Network Endpoints + Deployed Contracts

Chain: Aurora Testnet
chainId: 1313161555
RPC_URL: https://testnet.aurora.dev

Deployed contracts:

- MembershipRegistry (membership tree / LeafRegistered): 0x7C329B70Da1Dc94d5655a0DB907637bc4530991f
- PetitionRegistry (proof verification entrypoint): 0x3fAfFFfA917b48Eff74EAAD48C3DF9DA44560eeD
- Groth16Verifier (ZK verifier): 0x25C9A59DC47Ba0869229f02f8d80CC22860bFFBa
- Poseidon2 (hash contract/library): 0xEFbb2780fA51c9D2f0375B226BEB03a897b0D9CF

---

# 5) Membership Model (Baseline)

Client stores one secret per wallet in localStorage.

Storage key:
su_memberSecret_v1:wallet:<walletLowercase>

Leaf definition:
leaf = Poseidon1(memberSecret)

Enrollment:
- One leaf per wallet
- Refundable bond required

Bond parameters:
registerBondWei() = 1e15 (0.001 ETH)
bondLockSeconds() = 3600

---

# 6) Nullifier Model (Locked)

nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)

On-chain:
- nullifier stored per petition
- duplicates rejected

This enforces one signature per petition per member.

---

# 7) Backend Role (MVP)

Backend is non-authoritative.

Responsibilities:
- Mirror membership events
- Rebuild Merkle tree
- Serve membership paths

Must NOT:
- Gate membership
- Gate signing
- Store secrets

---

# 8) Path Privacy Hardening (Agent Track)

Goal:
Remove wallet address from membership path requests.

Replace:
GET /api/membership/path?wallet=<address>

With:
GET /api/membership/path?leaf=<hex>

This reduces direct deanonymization risk.

Work package:
AGENT_WORK_PACKAGE_PATH_PRIVACY_V1.md

No circuit or contract changes required.

---

# 9) Relayer Signing (Design Phase — Not Implemented)

Goal:
Decouple proof submission from wallet tx sender.

Spec:
docs/RELAYER_SIGNING_SPEC.md

This is additive.
Direct path remains baseline.
No circuit changes required.

---

# 10) Known MVP Limitations

- Enrollment publicly tied to wallet
- No unlinkable membership acquisition
- No relayer path yet
- Backend required for path distribution
- Secret loss breaks signing on that device

---

# 11) Next Strategic Layer (Post-MVP)

Long-term Tornado-grade privacy requires:

- Unlinkable enrollment model
- Relayed/meta-tx signing path
- Strong artifact provenance enforcement
- Larger anonymity sets (with performance gating)

Design must precede implementation.
All changes must be reflected here first.

---

STATE.md remains canonical.

If any conflict arises between code and documentation:
STATE.md governs.