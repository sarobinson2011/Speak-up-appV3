# REFLECT_MIRROR_SELECTION_V1

## Mirror Pool

REFLECT consists of 7 mirrors.

---

## Role Assignment (per action)

- required chunk → mirror A
- cover chunk 1 → mirror B
- cover chunk 2 → mirror C
- connector → mirror D

All must be distinct.

---

## Derivation

Roles are derived via deterministic permutation of the REFLECT pool using the action seed.

---

## Connector Rule

Connector mirror must be distinct from all chunk-serving mirrors.

This is enforced, not optional.

---

## Fallback

Each object has:

- 1 primary mirror
- 2 fallback mirrors

Fallback mirrors are derived from the same permutation and must respect separation constraints.