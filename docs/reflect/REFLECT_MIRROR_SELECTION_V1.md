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

## Interpretation Boundary

Mirror assignment is deterministic publication-surface assignment.

It exists to preserve bounded separation and fragmented observability.

Mirror assignment does not define:

- publication-state validity
- publication-state priority
- mirror trust
- mirror preference
- mirror capability ranking
- routing authority
- topology authority
- adaptive retrieval authority

A primary mirror is not a semantic authority.

A fallback mirror is not a lower-priority publication state.

Mirror roles are runtime retrieval surfaces only.

Mirror roles must not be used to:

- alter publication-state selection
- infer object validity
- infer state freshness
- optimize toward fastest response
- introduce adaptive routing
- introduce probabilistic mirror choice
- expose topology-aware client behavior

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