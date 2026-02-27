# ZK Circuit Specification — Speak-up-appV3 (M2-only MVP)

Last updated: 2026-02-27 (Europe/London)

This document is the *implementation-facing* spec for the **current** ZK circuit + proving + on-chain verification loop used by the M2-only MVP.

It is intentionally tight and excludes all deprecated designs (Noir, UltraHonk, attestations/M1, server-side proving).

---

## 1) Purpose

Prove, in zero knowledge:

1. The signer knows a private `memberSecret` corresponding to a registered membership leaf.
2. The signer is a member of the Merkle set under a *currently-valid* membership root.
3. The signer’s revealed `nullifier` is correctly derived for `(memberSecret, petitionId, SIGN_DOMAIN)`.

On-chain verifies the proof, checks `membershipRoot` validity, and enforces `nullifier` uniqueness per `petitionId`.

---

## 2) Cryptographic primitives (locked for MVP)

- Field: BN254 scalar field (as used by Groth16 verifier)
- Hashes:
  - `Poseidon1(x)` for leaves
  - `Poseidon2(left, right)` for Merkle parent hashing
  - `Poseidon3(a, b, c)` for nullifier

Domain separator (locked):
- `SIGN_DOMAIN = 0x5349474e`  // ASCII "SIGN" interpreted as field element

---

## 3) Definitions (locked)

### 3.1 Membership leaf

- `leaf = Poseidon1(memberSecret)`

### 3.2 Nullifier

- `nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)`

### 3.3 Merkle membership

- Tree depth: `DEPTH = 16`
- Root validity: membership contract accepts last `N = 16` roots

Merkle recomputation in-circuit:

- start = `leaf`
- for i in [0..DEPTH-1]:
  - if `pathBits[i] == 0`:  cur = Poseidon2(cur, siblings[i])
  - else:                  cur = Poseidon2(siblings[i], cur)
- assert `cur == membershipRoot`

---

## 4) Circuit interface

### 4.1 Private inputs

- `memberSecret` : Field
- `siblings[DEPTH]` : Field[]
- `pathBits[DEPTH]` : (0/1) bits

### 4.2 Public inputs

Locked semantics (order MUST match the generated Solidity verifier and frontend encoder):

1. `petitionId` : Field
2. `nullifier` : Field
3. `membershipRoot` : Field

If your generated verifier expects a different order, **do not “fix” it ad hoc** — regenerate the verifier and update the frontend encoder so all three layers agree.

---

## 5) Frontend witness formation (MVP)

Inputs available in frontend:

- `petitionId` (from UI / contract ID)
- `memberSecret` (from localStorage; decimal string → BigInt)
- `membershipPath` from backend:

  - `root` (hex string)
  - `siblings[]` (hex strings length DEPTH)
  - `pathBits[]` (0/1 array length DEPTH)
  - `leaf` (hex string) + `index` (u32) for debugging

Required preflight checks (must pass before attempting proof):

- `memberSecret` exists for connected wallet
- `membershipPath` loaded
- `Poseidon1(memberSecret) == BigInt(membershipPath.leaf)`  (leafMatches)

Then:

- compute `nullifier` in JS with Poseidon3 exactly as circuit does
- generate Groth16 proof in-browser with snarkjs
- submit tx to petition registry with `(petitionId, nullifier, membershipRoot, proof...)` per ABI

---

## 6) On-chain verification expectations (MVP)

Petition registry must enforce:

1. Groth16 proof verification succeeds for the public inputs.
2. `membershipRoot` is valid per MembershipRegistry (root ∈ last-N valid roots).
3. `nullifier` unused for this petition; store it to prevent re-sign.

Eventing:
- `PetitionSigned(petitionId, nullifier, ...)` emitted for indexing + UI counts.

---

## 7) Artifacts and locations (fill in as you lock repo paths)

You should be able to point to these in-repo:

- Circom circuit source:
  - `circuits/<...>/sign_petition.circom` (path: TODO)
- Proving key + verification key:
  - `.zkey` (path: TODO)
  - `verification_key.json` (path: TODO)
- Solidity verifier:
  - `contracts/<...>/Groth16Verifier.sol` (path: TODO)
- Frontend proof generator:
  - `frontend/src/components/M2SignButton.jsx` (or .tsx) (path: TODO)

---

## 8) Golden test (must stay green)

A “golden proof” test should exist and pass before any chain interaction:

- Given a fixed `memberSecret`, a toy tree, and a petitionId:
  - witness builds
  - proof verifies locally (snarkjs verify)
  - public signals match expected `petitionId/nullifier/root`

---

## 9) Non-goals for MVP (explicit)

- Noir / UltraHonk / Barretenberg references (deprecated)
- Server-side proving (not used; secrets never leave device)
- Comments circuit (future feature)
- Secret rotation/export/import (future feature)