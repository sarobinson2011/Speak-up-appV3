“When in doubt, STATE.md wins.”
“Changes must be recorded here before implementation.”

STATE.md — Speak-up-appV3

Last updated: 2026-02-27 (Europe/London)

This file is the canonical “source of truth” for architecture decisions, invariants, deployed addresses, and the current MVP baseline. Any design change must be reflected here before implementation.

---

## 1) Project goal (M2-only MVP)

Build a privacy-preserving petition platform where users can:

- Create petitions (wallet-authenticated; not private in MVP)
- Sign petitions with **Strong Privacy (M2)**:
  - proof is generated client-side
  - on-chain verification is authoritative
  - uniqueness is enforced via a nullifier (not via wallet address)
- (Comments are explicitly **disabled** in MVP baseline)

---

## 2) Core product rules (invariants)

Locked for MVP:

1. **Uniqueness:** max 1 signature per (petitionId, member) enforced via **nullifier**, not wallet.
2. **Privacy:** signer proves membership without revealing which member they are.
3. **On-chain authority:** chain verifies proof + root validity + nullifier uniqueness.
4. **No trusted gatekeeper (baseline):** membership is permissionless on-chain; backend is non-authoritative convenience only.
5. **M2-only mode:** no email verification, no JWT, no attestations, no M1 routes/UI.

---

## 3) ZK stack (current)

- Circuit framework: **Circom**
- Prover/verifier: **Groth16 (BN254)**
- Proof tooling: **snarkjs**
- Hashing: **Poseidon**
  - leaf: Poseidon1
  - merkle node: Poseidon2(left, right)
  - nullifier: Poseidon3

---

## 4) Membership model (baseline)

### 4.1 Identity material (client-side)

- Client stores one secret per wallet in localStorage:

  - key: `su_memberSecret_v1:wallet:<walletLowercase>`
  - value: decimal string representing a BigInt field element

- **MVP rule:** if a wallet is enrolled and you lose its secret on that device, that wallet is dead for signing on that device.

### 4.2 Leaf definition (locked)

- `leaf = Poseidon1(memberSecret)`

### 4.3 Tree parameters (locked)

- DEPTH = 16 (≈ 65,536 leaves)
- Root history window N = 16 (contract retains last 16 roots as valid)

### 4.4 Registration (permissionless; on-chain)

- Wallet registers its leaf on-chain once (baseline: **one leaf per wallet**).

Sybil friction (baseline iteration 1):
- registration requires a **refundable bond** (exact amount read from chain)
- bond is locked for a time window

### 4.5 Deployed membership contract (Aurora testnet)

- Chain: Aurora testnet (chainId 1313161555)
- MembershipRegistry: `0x7C329B70Da1Dc94d5655a0DB907637bc4530991f`
- `registerBondWei()` = `1e15` (0.001 ETH)
- `bondLockSeconds()` = `3600` (1 hour)

(Values above are from on-chain reads during MVP test session.)

---

## 5) Nullifier model (anti double-signing)

Locked:

- `SIGN_DOMAIN = 0x5349474e` (ASCII "SIGN" as a field element)
- `nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)`

On-chain:
- store nullifier per petition and reject duplicates.

---

## 6) Backend role (non-authoritative, MVP)

Backend is a **convenience indexer**:

- mirrors on-chain membership events
- rebuilds the Merkle tree
- serves Merkle paths to clients

Backend MUST NOT:
- gate membership
- gate signing
- store member secrets

### 6.1 Required endpoint (MVP)

- `GET /api/membership/path?wallet=<address>`

Returns:
- `wallet`, `leaf`, `index`, `root`
- `siblings[]` (length = DEPTH)
- `pathBits[]` (length = DEPTH)

If wallet not enrolled, returns 404 with `wallet not found in membership index`.

---

## 7) Frontend UX (MVP baseline)

### 7.1 Wallet connect

- User connects MetaMask.
- App ensures secret exists via `ensureMemberSecret(account)` on wallet connect and on `accountsChanged`.

### 7.2 Petition details: M2 signing preflight

A petition can be signed if ALL are true:

- `memberSecret` present locally
- `membershipPath` loaded from backend
- `leafMatches`:
  - computed leaf from local secret equals backend leaf for wallet
- not already signed (checked via on-chain `hasSignedPetition(petitionId, nullifier)`)

### 7.3 Enrollment UX (Option B: “proper”)

If secret is present but membership path is missing:

- show **Enroll (one-time)** button
- clicking enroll:
  - computes leaf from local secret
  - reads `registerBondWei()` from MembershipRegistry
  - calls `registerLeaf(leaf)` with `{ value: bond }`
  - after tx confirms, UI refreshes and backend path should become available

This is the deterministic “plumbing” baseline that makes new wallets work.

---

## 8) Known limitations (explicitly accepted for MVP)

- Losing localStorage secret breaks signing for that wallet on that device.
- No comment flow (UI placeholder only).
- No metadata fetching from IPFS beyond showing URI.
- Backend is required for path distribution in MVP (can be decentralized later).

---

## 9) MVP acceptance checklist (must all pass)

- New wallet:
  - connect → secret created → enroll (one-time) → membership path loads → sign succeeds
- Returning wallet:
  - connect → secret persists → membership path loads → sign button enabled (if not signed)
- Already-signed wallet:
  - connect → sign is blocked via on-chain nullifier check
- Leaf mismatch:
  - UI blocks signing and explains “secret mismatch”
- Backend down:
  - UI shows “membership not loaded” and blocks signing

---

## 10) Next steps (after baseline)

1. Update docs (this file + ZK_CIRCUIT_SPEC.md) and commit MVP baseline.
2. Cleanup / delete M1 artifacts and dead code paths.
3. Add explicit export/import secret flow (NOT MVP).
4. Add comments + moderation pipeline (post-MVP).