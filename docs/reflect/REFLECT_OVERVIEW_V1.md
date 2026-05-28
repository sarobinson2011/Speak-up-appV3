# REFLECT_OVERVIEW_V1

## Purpose

REFLECT defines the path/publication semantics responsible for publishing and serving structured, client-verifiable data required for witness construction.

REFLECT is centered on deterministic publication-state coherence semantics.

REFLECT does not treat mirrors as authorities.

REFLECT mirrors are replaceable publication surfaces.

Clients determine validity through deterministic verification of coherent publication-state object sets.

It enables:

- leaf-based membership path derivation
- deterministic publication-state selection
- coherent publication-state reconstruction
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
- bounded publication-window semantics
- coherent publication-state selection semantics
- connector/chunk verification semantics

Current architecture does NOT yet imply:

- deployed distributed mirror federation
- public mirror topology exposure
- remote mirror governance
- fully distributed publication infrastructure
- externally visible mirror traversal semantics
- adaptive routing infrastructure
- distributed consensus semantics
- topology-aware clients

unless explicitly defined in `STATE.md`.

Clients/frontends must not infer, expose, or depend upon infrastructure topology assumptions.

---

## Core Principles

- Mirrors publish shared structural objects, not identity-addressed responses
- Publication-state validity is client-derived
- Publication-state selection is deterministic
- Publication-state coherence is mandatory
- A publication state is a lifecycle boundary
- No mirror has a stable role across actions
- No mirror sees the full action context
- Connector separation is enforced
- Fallback replaces mirror, not publication state
- Failure must remain bounded and predictable
- System must degrade gracefully or fail cleanly

---

## Publication-State Model

A publication state is a coherent object set consisting of compatible:

- root metadata
- manifest
- connector object
- subtree chunks

Objects are usable only when accepted together as one coherent publication-state lifecycle boundary.

Cross-state reconstruction is forbidden.

Fallback may perform bounded deterministic retrieval substitution for selected objects through deterministic fallback mirrors, but fallback must not alter publication-state selection.

---

## System Shape

- REFLECT = 7 mirrors

Per action:

- 3 chunk interests
  - 1 required
  - 2 deterministic covers
- 1 connector object

Roles are derived deterministically per action.

Selection remains topology-neutral and client-derived.

Mirrors do not provide routing authority, state authority, or adaptive selection authority.

---

## Mirror Interpretation Boundary

REFLECT mirrors are publication surfaces.

They are not:

- trust authorities
- routing coordinators
- adaptive selection engines
- publication-state arbiters
- consensus participants
- identity-aware services

Mirror exposure alone does not make a publication state valid.

Only deterministic client verification determines whether publication material is acceptable for witness construction.
