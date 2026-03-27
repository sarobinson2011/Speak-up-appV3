# TEMPEST Relay Interface V1

## Purpose

Standardize relay communication.

---

## Endpoints

### POST /relay/submit
Submit proof payload

### GET /relay/health
Coarse health state

### GET /relay/info
Relay metadata

---

## Request Fields

- petitionId
- nullifier
- pA, pB, pC
- pubSignals

---

## Response Classes

- success
- temporary_failure
- terminal_invalid
- unknown

---

## Constraints

- no identity fields
- no client metadata
- no wallet data
- no tracking IDs

---

## Invariant

All 7 relays must behave identically at protocol level.