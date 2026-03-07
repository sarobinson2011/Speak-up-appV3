# Relayer Signing Specification
Speak-up-appV3 (M2-only baseline)
Status: LIVE (Engineering[5] design phase)
Last updated: 2026-02-27 (Europe/London)

---

## 1. Purpose

Allow petition signing without revealing the signer’s wallet address
as the transaction sender.

The cryptographic proof remains unchanged.

We improve metadata privacy by decoupling:
- proof generation
- transaction broadcasting

---

## 2. Baseline (Current State)

User signs directly:
wallet → contract.signWithProof(...)

This leaks:
- wallet address
- timing
- gas payment source

Even though proof hides membership identity.

---

## 3. Goals

- Preserve all ZK correctness guarantees
- Preserve nullifier uniqueness enforcement
- Avoid trusted eligibility gate
- Prevent replay
- Mitigate spam

---

## 4. Non-Goals

- No circuit change
- No modification to nullifier formula
- No change to membership model (yet)

---

## 5. Architecture

Add new contract entrypoint:

signWithProofRelayed(
    petitionId,
    nullifier,
    membershipRoot,
    proof,
    relayData,
    relaySig
)

Existing direct path remains unchanged.

---

## 6. Relay Authorization Model

Client generates ephemeral relay key:

relayPrivKey (local only)
relayPubKey

Client signs EIP-712 typed data:

{
  petitionId,
  nullifier,
  membershipRoot,
  proofHash,
  expiry,
  nonce
}

Relayer submits:
- proof
- relayData
- relaySig

Contract verifies:
- relaySig valid
- not expired
- nonce unused
- nullifier unused
- proof valid

---

## 7. Abuse Controls

Relayer must:
- verify proof locally before submission
- enforce rate limits
- enforce expiry window
- enforce max size

Contract must:
- store used (relayPubKey, nonce)
- enforce expiry
- enforce nullifier uniqueness

---

## 8. Privacy Properties

Improved:
- tx sender no longer signer wallet

Remaining leaks:
- timing
- relayer operator trust
- network-level metadata

This is strictly stronger than baseline.

---

## 9. Compatibility Plan

Phase 1:
- Keep direct path
- Add relayed path
- Feature flag in frontend

Phase 2:
- Optionally default to relayed path

---

## 10. Acceptance Criteria

- User can sign without wallet appearing as tx sender
- Proof validity unchanged
- Nullifier enforcement unchanged
- Replay prevented
- No trusted eligibility gate added

Document remains LIVE until relayer path is production-ready.