# PRIVACY_THREAT_MODEL.md

Supporting document only.
If this document conflicts with `STATE.md`, **STATE.md wins**.

---

# Speak-up-appV3 Privacy Threat Model (v1)

This document describes the **privacy guarantees**, **remaining leak vectors**, and the **roadmap toward Tornado-grade anonymity** for the Speak-up petition system.

It focuses on **adversary analysis**, not implementation details.

Architecture details remain in `STATE.md`.

---

## Current Layer Status Note

This document is a supporting threat-analysis document.

Current implementation authority and active layer semantics remain governed by:

- `STATE.md`
- `docs/CONTINUITY_CUSTODY_MODEL_V1.md`
- `docs/PRIVACY_ENGINE_DEFINITION.md`

Current layer ownership:

- M2 owns identity / proof semantics
- Enrollment owns economic admission / eligibility semantics
- TEMPEST owns execution / submission semantics
- REFLECT owns path / publication semantics
- Custody owns local secret portability semantics

Some roadmap sections below are retained as historical/evolutionary privacy planning context and may not reflect the latest implementation status.

---

# 1. Privacy Goal

Speak-up aims to allow users to sign petitions anonymously while ensuring:

• only verified members may sign
• each member signs at most once per petition
• identity is never revealed

The system must prove **membership eligibility** without revealing **which member signed**.

Target privacy level:

> Comparable anonymity properties to Tornado Cash, adapted to a petition signing system.

This means breaking links between:

* identity
* wallet
* membership enrollment
* petition choice
* transaction submission

---

# 2. Core Privacy Mechanism

The system uses:

* Poseidon-based Merkle membership tree
* client-side ZK proof generation
* Groth16 verification on-chain
* nullifier-based uniqueness

Public inputs:

1. nullifier
2. petitionId
3. membershipRoot

The ZK proof demonstrates:

* knowledge of a valid membership leaf
* membership leaf inclusion in the Merkle tree
* correct nullifier generation

Without revealing:

* which leaf was used
* the member secret
* the membership path

The smart contract verifies the proof and rejects duplicate nullifiers.

---

# 3. Adversary Model

The threat model considers the following adversaries.

## 3.1 Public blockchain observers

Capabilities:

* observe all transactions
* inspect calldata
* inspect contract state
* inspect logs

Goal:

* determine who signed a petition.

---

## 3.2 Backend observer

Capabilities:

* observe incoming requests to the relay
* observe timing
* observe request metadata

Goal:

* correlate a user request with a blockchain transaction.

---

## 3.3 Network observer

Capabilities:

* observe IP traffic
* observe TLS metadata
* observe request timing

Goal:

* correlate network activity with petition signing events.

---

## 3.4 Malicious member

Capabilities:

* enroll multiple identities
* attempt replay attacks
* attempt deanonymization of other users.

---

# 4. Current Privacy Guarantees

The system currently provides the following protections.

## 4.1 Identity privacy inside the proof

The ZK proof hides:

* membership leaf
* membership path
* member secret

Observers cannot determine which member produced the proof.

---

## 4.2 Petition uniqueness

Nullifiers ensure:

* one signature per petition per member.

This prevents double-signing while preserving anonymity.

---

## 4.3 Wallet unlinkability during signing

Signing transactions are submitted by the **relayer**, not the user wallet.

Therefore:

* the on-chain sender address does not reveal the user wallet.

---

## 4.4 Wallet removal from membership path queries

The backend API distributes Merkle paths using:

```
GET /membership/path?leaf=<hash>
```

instead of wallet-based queries.

This removes a direct mapping between wallet address and membership tree position.

---

# 5. Remaining Privacy Limitations

The system does **not yet provide full Tornado-grade anonymity**.

The following information leaks remain possible.

---

## 5.1 Enrollment linkability

Membership enrollment currently occurs via a wallet transaction.

This reveals:

* wallet address
* enrollment timing
* membership leaf creation event

Observers could potentially correlate enrollment with later activity.

---

## 5.2 Relay observation

The relay can observe:

* submission timing
* petition target
* nullifier

Even though the relay does not know the member identity, it still sees submission events.

---

## 5.3 Network metadata

Without network-level privacy:

* IP addresses
* timing patterns
* TLS metadata

may allow correlation between users and petition activity.

---

## 5.4 Small anonymity sets

If only a small number of members exist, anonymity sets are limited.

Large anonymity sets are required for strong privacy guarantees.

---

# 6. Privacy Evolution Roadmap

The system evolves privacy in stages.

## Stage 1 — ZK proof verification

Achieved.

Membership is proven anonymously via ZK proof.

---

## Stage 2 — Wallet decoupling from membership lookup

Achieved.

Leaf-based membership path queries removed wallet identifiers.

---

## Stage 3 — Relayed signing

Achieved.

Transaction sender is the relayer, not the user wallet.

---

## Stage 4 — Unlinkable membership acquisition (future)

Goal:

Allow users to join the membership set without revealing a link between:

* their wallet
* their membership identity.

Possible mechanisms include:

* deposit-style membership commitments
* stealth enrollment flows
* relayed enrollment transactions.

This stage is the most important step toward Tornado-grade anonymity.

---

## Stage 5 — Multi-relayer infrastructure (future)

Note: Current TEMPEST implementation status and relay semantics are governed by `STATE.md`.  
This section is retained as roadmap/evolution history.

Single-relayer infrastructure introduces trust assumptions.

Future design may include:

* multiple relayers
* open relay markets
* fee markets for relaying.

---

## Stage 6 — Network privacy improvements (future)

Users may submit relay requests through privacy networks such as:

* Tor
* VPNs
* privacy relayer infrastructure.

This reduces IP-based correlation risk.

---

# 7. Anonymity Set Requirements

Strong anonymity requires:

* large membership sets
* uniform participation
* unpredictable signing timing.

If only a small number of members exist, anonymity guarantees weaken.

The system should encourage growth of the membership tree to increase anonymity sets.

---

# 8. Threats Outside Scope

The following threats are outside the current scope:

* malicious browsers leaking secrets
* compromised user devices
* wallet malware
* hardware-level surveillance.

The system assumes users control their local environment.

---

# 9. Relay Privacy + Logging Policy

The backend relayer is part of the privacy boundary.

It exists to decouple the user's wallet from the on-chain signing transaction, but it must not become a surveillance point.

---

## 9.1 Allowed relay logging

The relayer may log only minimal operational data:

* timestamp
* event type
* petitionId
* nullifier
* txHash
* high-level error message

Typical events include:

* `submit-ok`
* `already-signed`
* `submit-error`

These logs are intended solely for operational monitoring.

---

## 9.2 Data that must NOT be intentionally logged

The relayer should not intentionally store:

* proof arrays (`pA`, `pB`, `pC`)
* full `pubSignals`
* request bodies
* IP address histories
* user agent strings
* browser/device fingerprints
* wallet-linked identity metadata.

Minimizing log surface area reduces the risk of the relay becoming a deanonymization database.

---

## 9.3 Current relay hardening

Current relay protections include:

* strict payload validation
* canonical public input checks
* signed-state precheck
* request body size limits
* in-memory rate limiting
* structured minimal logging
* relay health monitoring endpoint.

---

## 9.4 Remaining relay privacy limitations

Even with relayed signing, the backend may still observe:

* request timing
* petitionId
* nullifier
* network metadata at the transport layer.

Therefore, relayed signing improves privacy but does not yet achieve Tornado-grade anonymity.

Further privacy improvements depend primarily on **unlinkable membership acquisition**.
