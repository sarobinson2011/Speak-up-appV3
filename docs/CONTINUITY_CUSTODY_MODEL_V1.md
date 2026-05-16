# Continuity Custody Model V1

Status: Supporting documentation  
Canonical authority: `STATE.md`

If this document conflicts with `STATE.md`, `STATE.md` wins.

---

## 1. Purpose

This document defines the operator-facing custody model for M2 secret continuity.

It exists to prevent semantic drift in UI copy, code comments, documentation, and future product decisions.

The goal is clarity:

- what continuity means
- what export/import means
- what encrypted continuity bundles mean
- what the system does not provide

This document does not introduce new architecture.

---

## 2. Scope

This document covers:

- local `memberSecret` custody
- plaintext secret export/import
- encrypted continuity bundle export/import
- O0/O1/O2 operator expectations
- replacement warnings
- forbidden continuity language

This document does not modify:

- ZK circuits
- nullifier derivation
- membership tree semantics
- contract interfaces
- relay behavior
- TEMPEST
- REFLECT
- backend authority

---

## 3. Core Continuity Rule

M2 continuity is defined only as:

> possession of the same original `memberSecret`

Nothing else establishes continuity.

Not a wallet.

Not a backend record.

Not an account.

Not an encrypted bundle by itself.

Not a password by itself.

Not a browser profile.

Not a relay.

Not a REFLECT mirror.

The active anonymous membership is continued only when the same original `memberSecret` is present locally and its derived leaf is enrolled.

---

## 4. Identity Boundary

The M2 identity primitive is:

    memberSecret -> leaf -> nullifier

Canonical derivations:

    leaf = Poseidon1(memberSecret)
    nullifier = Poseidon3(memberSecret, petitionId, SIGN_DOMAIN)

A different `memberSecret` is a different anonymous membership candidate.

The system must not infer identity continuity from:

- wallet address
- connected account
- browser state
- backend memory
- admission records
- relay state
- encrypted bundle metadata

---

## 5. Operator State Model

### O0 — No local secret present

Meaning:

- no active local `memberSecret`
- no local M2 identity material available

Allowed:

- create new secret
- import saved secret
- import encrypted continuity bundle

Blocked:

- export
- enroll
- sign

---

### O1 — Local secret present, not enrolled

Meaning:

- active local `memberSecret` exists
- derived leaf is not currently enrolled

Allowed:

- export current secret
- export encrypted continuity bundle
- import saved secret
- import encrypted continuity bundle
- create new secret with explicit replacement
- enroll current secret

Blocked:

- sign

---

### O2 — Local secret present, enrolled and usable

Meaning:

- active local `memberSecret` exists
- derived leaf is enrolled
- signing is possible if the petition nullifier is unused

Allowed:

- export current secret
- export encrypted continuity bundle
- import saved secret with explicit replacement semantics
- import encrypted continuity bundle with explicit replacement semantics
- create new secret with explicit replacement semantics
- sign if nullifier unused

Blocked:

- enroll current secret again

---

## 6. Plaintext Export Semantics

Plaintext export copies the current `memberSecret` into operator custody.

It does not:

- create an account
- create a recovery service
- register anything with the backend
- notify the chain
- involve TEMPEST
- involve REFLECT
- prove continuity

Plaintext export is dangerous because anyone with the exact secret can continue the same anonymous membership.

UI copy should emphasize:

- exact secret custody
- offline storage
- local responsibility
- same-secret continuity only

---

## 7. Plaintext Import Semantics

Plaintext import sets the active local secret to supplied material.

Import may continue an existing anonymous membership only if the imported value is the same original `memberSecret`.

Import does not prove continuity.

Import does not recover identity through external authority.

Import does not derive identity from the connected wallet.

Import means:

    set active local secret = imported secret

The existing M2 logic then determines whether the derived leaf is enrolled.

---

## 8. Encrypted Continuity Bundle Semantics

An encrypted continuity bundle is portable encrypted custody of the current `memberSecret`.

It contains only encrypted secret material and required decrypt metadata.

It is not:

- an account
- a recovery phrase
- a wallet recovery mechanism
- a cloud backup
- a synced identity
- an identity provider
- backend custody
- protocol authority

Encrypted bundle import means:

    decrypt bundle locally
    -> extract memberSecret
    -> import memberSecret using existing import semantics

The bundle itself has no independent identity meaning.

Continuity exists only if the decrypted secret is the same original `memberSecret`.

---

## 9. Replacement Semantics

Creating or importing a secret while another secret is active replaces the active local secret on that device/browser.

Replacement must be explicit.

Replacement must never be silent.

Replacement must not be framed as recovery.

Correct framing:

- replace active local secret
- switch away from current anonymous membership
- re-import the same original secret to continue that membership

Incorrect framing:

- recover account
- restore identity
- restore account
- switch account
- sync identity

---

## 10. Forbidden Semantics

The following language must not be used for M2 continuity UX unless a future architecture explicitly introduces such semantics and `STATE.md` is updated first:

- account recovery
- restore account
- recover identity
- wallet recovery
- recovery phrase
- cloud backup
- synced identity
- identity restoration service
- profile restore
- backend recovery
- server-side recovery
- wallet-based continuity
- account restore

Avoid softer variants that imply the same thing:

- your account
- your profile
- automatic recovery
- recover access
- sync across devices
- retrieve your identity

Preferred language:

- active local secret
- same original secret
- saved copy of this secret
- encrypted continuity bundle
- encrypted local custody
- import saved secret
- import encrypted bundle
- replace active local secret
- continue the same anonymous membership

---

## 11. Non-Goals

The continuity custody model does not provide:

- account recovery
- human identity recovery
- wallet-based recovery
- backend-assisted recovery
- cloud synchronization
- automatic multi-device continuity
- key escrow
- password reset
- server-side identity restoration

If the operator loses the original `memberSecret` and has no saved copy or encrypted bundle containing it, the previous anonymous membership cannot be continued.

---

## 12. Relationship to M2, TEMPEST, and REFLECT

M2 owns identity and proof semantics.

Continuity custody is an operator custody surface around M2 secret material.

TEMPEST does not participate in continuity.

REFLECT does not participate in continuity.

The backend does not participate in continuity.

The chain does not recover continuity.

Layer separation:

    M2        -> identity / proof semantics
    Custody   -> local secret custody and portability
    TEMPEST   -> execution / submission semantics
    REFLECT   -> path / publication semantics

No layer may infer or recreate the responsibility of another.

---

## 13. Operational Guidance

Future UI, docs, comments, and tests should preserve these rules:

1. Say “same original secret,” not “account recovery”.
2. Say “replace active local secret,” not “restore identity”.
3. Say “encrypted continuity bundle,” not “recovery phrase”.
4. Say “local/browser custody,” not “cloud backup”.
5. Keep encrypted bundle semantics subordinate to ordinary import semantics.
6. Treat wording as part of the privacy boundary.
7. Do not imply the backend, wallet, relay, or mirror can restore continuity.

---

## 14. Locked Interpretation

Continuity is possession of the same original `memberSecret`.

Export copies it.

Import sets it.

Encrypted bundles encrypt and transport it.

Nothing else restores, recovers, syncs, or authorizes it.
