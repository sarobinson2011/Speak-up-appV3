# REFLECT_OBJECT_MODEL_V1

## Purpose

This document defines REFLECT publication object classes and their coherence requirements.

REFLECT objects are client-verifiable publication material for witness construction.

Objects are not authoritative because a mirror publishes them.

Objects become usable only when they are accepted as part of one coherent, client-verified publication state.

---

## Object Classes

Each REFLECT publication surface may expose:

1. Root Metadata
2. Manifest
3. Subtree Chunks
4. Connector Object

Publication surfaces are replaceable.

They do not own object truth, state validity, or witness authority.

---

## Core Rule

A client must build a witness from **one coherent publication state only**.

No cross-state mixing is allowed.

A publication state is the lifecycle boundary for object acceptance.

---

## Publication State Identity

All objects used together must share:

- publication state ID
- root
- protocol interpretation

They must also preserve:

- connector/chunk relationship
- manifest compatibility
- root metadata consistency
- digest-layer separation

---

## Connector / Chunk Relationship

The connector object describes the chunk set that may be used for reconstruction.

Chunks must satisfy the connector.

The connector must satisfy the manifest and root metadata.

A connector from one publication state must never be combined with chunks from another publication state.

A chunk from one publication state must never be used to repair or complete another publication state.

---

## Integrity Model

Each object must be:

- independently verifiable
- compatible with manifest
- consistent with root metadata
- compatible with the selected publication state
- compatible with connector/chunk coherence rules

Digest layers must remain distinct.

Descriptor or group digests must not be treated as publication-state digests.

Publication-state digests must not be treated as connector or chunk digests.

---

## Mirror Non-Authority

Mirrors may expose object material.

Mirrors do not authorize:

- object validity
- publication-state validity
- connector/chunk compatibility
- root compatibility
- witness readiness
- state priority

Only client verification determines whether exposed objects are usable.

---

## Hard Rule

If object material cannot be verified as one coherent publication state, it must be rejected.

No partial object acceptance.

No cross-state repair.

No mirror-authorized reconstruction.

No adaptive object substitution.
