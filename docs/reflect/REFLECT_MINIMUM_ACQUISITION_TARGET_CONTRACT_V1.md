# REFLECT_MINIMUM_ACQUISITION_TARGET_CONTRACT_V1

## Purpose

This document defines the minimum stable contract of the
REFLECT acquisition target.

The objective is to preserve acquisition truth while allowing
acquisition surfaces, providers, routing mechanisms, and
retrieval infrastructure to evolve independently.

If any conflict exists, STATE.md remains authoritative.

---

## Core Principle

The acquisition target is an acquisition identity object.

It is not:

- a retrieval instruction
- an acquisition plan
- a routing request
- a transport request

The target describes what must be acquired.

The target does not describe how acquisition occurs.

---

## Authority Boundary

Truth selection occurs before target construction.

Target construction occurs before retrieval.

Retrieval consumes targets.

Retrieval does not construct, mutate, reinterpret,
or extend target authority.

---

## Target Authority Surface

The target may contain only authority required to preserve acquisition truth.

### Acquisition Authority

Example:

- acquisitionKey

Purpose:

- identifies the selected acquisition coordinate

### Validation Authority

Example:

- contentDigest

Purpose:

- preserves object identity independent of acquisition surface

### Traversal Authority

Example:

- sequence

Purpose:

- preserves traversal identity and ordering semantics

### State-Coherence Authority

Example:

- selectedStateDigest

Purpose:

- preserves selected publication-state identity

---

## Truth-Preservation Rule

Target owns truth-preservation authority.

Acquisition machinery owns truth-acquisition behavior.

Truth-preservation authority answers:

- What object is being acquired?

Truth-acquisition behavior answers:

- How is that object obtained?

Only the former belongs inside target.

---

## Forbidden Authority Migration

The following authority classes must never migrate into target.

### Provider Authority

Examples:

- providerId
- providerClass
- providerPreference

Provider replacement does not alter acquisition truth.

### Surface Authority

Examples:

- surfaceId
- surfaceClass

Acquisition-surface replacement does not alter acquisition truth.

### Routing Authority

Examples:

- route
- priority
- preference

Routing is acquisition strategy.

### Fallback Authority

Examples:

- fallbackProvider
- fallbackChain
- retryOrder

Fallback is execution behavior.

### Topology Authority

Examples:

- mirrorSet
- providerGraph
- sourceList

Topology is environmental knowledge, not acquisition identity.

### Transport Authority

Examples:

- url
- endpoint
- protocol
- headers
- timeouts

Transport belongs to retrieval implementation.

---

## Contamination Test

Future target additions must satisfy the following test:

If acquisition surfaces changed completely,
would this field still be required to identify
the same acquisition objective?

If yes:

- the field may be target authority

If no:

- the field is acquisition-mechanism information
- it must remain outside target

---

## Evolution Constraints

Acquisition implementation may evolve.

Target identity must not.

Changes to:

- providers
- surfaces
- routing
- fallback
- topology
- transport
- orchestration

must not require target mutation.

---

## Minimum Stable Acquisition Target Contract

Required authority classes:

- acquisition authority
- validation authority
- traversal authority
- state-coherence authority

Forbidden authority classes:

- provider authority
- surface authority
- routing authority
- fallback authority
- topology authority
- transport authority

---

## Conclusion

The acquisition target is the minimum authority bundle
required to preserve acquisition truth across acquisition
surface evolution.

Target may acquire additional truth-preservation coordinates.

Target must not acquire truth-acquisition coordinates.
