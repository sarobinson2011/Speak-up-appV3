# REFLECT_OBJECT_MODEL_V1

## Object Classes

Each REFLECT mirror publishes:

1. Root Metadata
2. Manifest
3. Subtree Chunks
4. Connector Object

---

## Core Rule

A client must build a witness from **one coherent publication state only**.

No cross-state mixing is allowed.

---

## Publication State Identity

All objects must share:

- publication state ID
- root
- protocol interpretation

---

## Integrity Model

Each object must be:

- independently verifiable
- compatible with manifest
- consistent with root metadata