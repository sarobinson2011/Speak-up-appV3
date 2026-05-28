# REFLECT_FETCH_POLICY_V1

## Fetch Stages

1. Root metadata (sequential)
2. Manifest (sequential)
3. Chunks + connector (parallel)

---

## Parallel Model

- 3 chunk fetches in parallel
- 1 connector fetch in parallel from separate mirror

## Runtime Interpretation Boundary

Fetch execution is runtime retrieval structure only.

Fetch behavior must remain subordinate to the selected publication state and acquisition plan.

Parallel retrieval does not define:

- publication-state validity
- publication-state priority
- state freshness
- mirror preference
- routing authority
- topology authority
- adaptive selection authority

A faster response does not make a publication state more valid.

A more responsive mirror does not become preferred semantic authority.

Fetch completion may only satisfy retrieval of already-selected objects.

Fetch failure may only trigger bounded deterministic retrieval substitution for the same selected object.

Fetch behavior must not:

- alter publication-state selection
- trigger adaptive reselection
- combine objects across publication states
- weaken connector separation
- introduce probabilistic routing
- expose topology-aware client behavior

---

## Constraints

- no cross-object dependency
- fallback is per-object
- no global reshuffle