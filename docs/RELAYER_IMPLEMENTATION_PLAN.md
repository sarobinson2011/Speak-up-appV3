# RELAYER_IMPLEMENTATION_PLAN_V0.md

Last updated: 2026-03-10 (Europe/London)

Status: design locked for implementation planning

---

Supporting historical implementation-planning document only.  
If this document conflicts with `STATE.md`, **STATE.md wins**.

This document reflects the original minimal-relayer implementation phase that later evolved into TEMPEST execution/submission semantics.

Current relay, execution, submission, fallback, observability, and topology semantics are governed by:

- `STATE.md`
- `docs/tempest/*`

This document remains useful as historical implementation-evolution context, but should not be interpreted as redefining current TEMPEST architecture authority.

---

# 1) Purpose

This document defines the first implementation path for relayed petition signing in Speak-up-appV3.

Goal:

- preserve the current ZK circuit and verifier flow
- remove the user wallet as the on-chain transaction sender
- keep the implementation minimal and operationally simple
- avoid introducing protocol drift before the privacy transport layer is proven

This is **Phase A: Minimal Centralized Relayer**.

It is intentionally smaller than a full trust-minimized relayer architecture.

---

# 2) Problem being solved

Current M2 signing flow:

1. user generates proof client-side
2. user wallet submits `signPetitionWithZKProof(...)`
3. contract verifies proof and records nullifier

This preserves identity privacy inside the proof, but still leaks metadata because:

- the user wallet is the tx sender
- chain observers can correlate the signing event with that wallet
- this weakens the privacy profile relative to Tornado-style systems

Relayer mode changes only the submission path:

- proof generation remains client-side
- contract verification remains unchanged
- relayer wallet becomes the tx sender

---

# 3) Scope (Phase A only)

Included:

- backend relayer route
- backend relayer wallet
- frontend optional relayed submission mode
- payload validation
- basic anti-abuse checks
- no circuit change
- no contract change

Not included yet:

- account abstraction
- ERC-2771 trusted forwarder
- permissionless relayers
- relay authorization signatures
- anti-replay nonce scheme
- privacy-preserving transport
- unlinkable enrollment
- treasury-funded gas subsidies

---

# 4) Architectural principle

The relayer is a **transport/privacy layer**, not a cryptographic redesign.

Therefore:

- use the current contract function unchanged
- use the current proof format unchanged
- use the current nullifier logic unchanged
- do not modify Groth16 public inputs
- do not modify the verifier contract

Current on-chain function remains:

`signPetitionWithZKProof(uint256 petitionId, bytes32 nullifier, uint256[2] pA, uint256[2][2] pB, uint256[2] pC, uint256[3] pubSignals)`

---

# 5) Phase A flow

## Current direct mode

1. frontend computes proof
2. frontend calls contract directly through wallet
3. wallet address is public tx sender

## New relayed mode

1. frontend computes proof
2. frontend sends proof payload to backend relayer endpoint
3. backend validates payload shape
4. backend checks current signed state (`hasSignedPetition`)
5. backend submits `signPetitionWithZKProof(...)` using relayer wallet
6. contract verifies proof exactly as before
7. frontend receives tx hash and refreshes state

Result:

- user wallet is not tx sender on-chain
- relayer wallet is tx sender on-chain

---

# 6) Backend route

Add route:

`POST /api/relay/sign`

Suggested request body:

```json
{
  "petitionId": "10",
  "nullifier": "0x...",
  "pA": ["0x...", "0x..."],
  "pB": [["0x...", "0x..."], ["0x...", "0x..."]],
  "pC": ["0x...", "0x..."],
  "pubSignals": ["0x...", "0x...", "0x..."]
}
