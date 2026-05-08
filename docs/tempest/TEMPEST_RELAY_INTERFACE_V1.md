# TEMPEST Relay Interface V1

## Purpose

Define the bounded relay execution interface for TEMPEST Phase A.

TEMPEST is the execution/submission layer. It must not expose identity, topology, or correlation surfaces.

---

## Current MVP Backend Endpoints

### POST /api/relay/sign

Submit a canonical proof payload for relayed petition signing.

### GET /api/relay/status

Returns coarse relay status only.

Current public fields:

- ok
- mode
- chainId

### GET /api/relay/health

Returns coarse relay health only.

Current public fields:

- ok
- mode
- chainId
- chainReachable

---

## Sign Request Fields

- petitionId
- nullifier
- pA
- pB
- pC
- pubSignals

The relay route internally fixes admissionCommitment to zero for the active M2 signing path.

---

## Success Response

The sign response may return:

- txHash

No relay slot, execution path, execution-domain detail, fallback traversal, signer identity, or topology metadata may be returned.

---

## Constraints

Relay interfaces must not expose:

- identity fields
- client metadata
- wallet data
- relay slot selection
- permutation order
- execution path
- execution-domain details
- fallback traversal
- relayer identity
- infrastructure-specific details

---

## Invariant

All execution paths must behave identically at protocol level.

The frontend must not become aware of TEMPEST topology.
