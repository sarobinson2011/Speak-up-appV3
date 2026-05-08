# TEMPEST Observability Policy V1

## Core Principle

TEMPEST relayers are:

**operationally stateful, but privacy-stateless**

---

## Absolute Rule

Relayers must not retain identity or correlation state:

- intentionally
- accidentally
- via misconfiguration
- via emergent behavior

---

## Allowed State

- in-flight request handling
- nonce tracking
- gas balance awareness
- coarse success/failure counts
- short-lived request outcome class

---

## Forbidden State

- IP address logs (persistent)
- user-agent tracking
- proof payload storage
- nullifier history logs
- cross-request correlation
- cross-relay tracking
- path request metadata

---

## Retention Model

### Ephemeral
- in-memory only

### Short-lived
- minimal operational logs

### Long-lived
- aggregate metrics only

---

## Structural Safeguards

- logging schemas must exclude sensitive fields
- no debug mode that exposes identity data
- no optional verbose logging that breaks privacy
- request data must be discarded after use

---

## Health Visibility

Public relay observability must remain coarse only.

Allowed public visibility:

- coarse online/reachable state
- coarse mode classification
- chain reachability

Allowed internal-only operational awareness:

- signer balance awareness
- bounded execution readiness
- bounded startup validation

Not allowed:

- relay slot visibility
- execution-domain visibility
- fallback traversal visibility
- per-request telemetry
- per-user metrics
- nullifier-linked telemetry
- petition-linked telemetry
- relay reputation state
- correlation signals
- infrastructure-specific exposure
