# REFLECT_OVERVIEW_V1

## Purpose

REFLECT defines the distributed path/publication model responsible for publishing and serving structured, client-verifiable data required for witness construction.

It enables:

- leaf-based membership path derivation
- decoupling from centralized path servers
- fragmentation of observable request patterns
- compatibility with deterministic privacy-preserving client behavior

---

## Current Implementation Status

Current REFLECT implementation authority is governed by `STATE.md`.

REFLECT currently defines the path/publication layer semantics for witness construction and publication-state coherence.

Current implementation primarily covers:

- prepared-path semantics
- local publication semantics
- publication-state coherence validation
- deterministic reconstruction semantics

Current architecture does NOT yet imply:

- deployed distributed mirror federation
- public mirror topology exposure
- remote mirror governance
- fully distributed publication infrastructure
- externally visible mirror traversal semantics

unless explicitly defined in `STATE.md`.

Clients/frontends must not infer, expose, or depend upon infrastructure topology assumptions.

---

## Core Principles

- Mirrors publish **shared structural objects**, not identity-addressed responses
- Clients derive all behavior **deterministically per action**
- No mirror has a **stable role across actions**
- No mirror sees the **full action context**
- **Connector separation is enforced**
- Failure must be **bounded and predictable**
- System must degrade **gracefully or fail cleanly**

---

## System Shape

- REFLECT = **7 mirrors**

Per action:

- 3 chunk interests
  - 1 required
  - 2 deterministic covers
- 1 connector object

All roles assigned via deterministic permutation.