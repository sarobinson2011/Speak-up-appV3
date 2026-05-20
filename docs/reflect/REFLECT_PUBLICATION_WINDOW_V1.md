# REFLECT_PUBLICATION_WINDOW_V1

## Policy

REFLECT uses a **bounded recent publication window**.

- not latest-only
- not unbounded history

---

## Rule

Client selects one state from a recent bounded set.

---

## Constraints

- window is protocol-defined
- publication-state acceptance is client-derived
- mirrors are replaceable publication surfaces, not state authorities
- older states are not considered live