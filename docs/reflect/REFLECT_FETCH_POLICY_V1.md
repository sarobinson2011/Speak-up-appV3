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

---

## Retrieval Provider Boundary

A retrieval provider is a future runtime acquisition surface only.

It may supply already-selected publication material to the acquisition layer.

It must not:

- select publication state
- rank publication state
- repair publication state
- prefer faster or newer state
- mutate traversal order
- mutate continuation semantics
- infer validity from availability
- expose topology-aware behavior

The acquisition layer validates retrieved material against the existing acquisition plan.

The previous local implementation passed publication material directly into traversal validation.

This means `acquireTraversalTarget(...)` validates already-supplied material; it does not perform retrieval.

The current local implementation introduces a local retrieval-provider abstraction before traversal validation.

The local retrieval provider returns an already-supplied publication group.

The retrieval unit is the publication group:

- descriptor
- connector
- chunks

Retrieval providers attach before traversal validation and remain subordinate to:

- selected publication-state identity
- acquisition plan
- traversal order
- object identity
- bounded continuation rules

Retrieval may obtain material.

Retrieval may not choose truth.

Validation accepts or rejects material.


Current retrieval identity surface:

- acquisition target

The local retrieval provider consumes acquisition targets directly.

No separate retrieval-request abstraction currently exists.

The acquisition plan remains the authority for:

- selected publication-state identity
- traversal ordering
- object identity

Retrieval providers remain subordinate to that authority.

Future retrieval-provider evolution must preserve this separation.

See also:

- `docs/reflect/REFLECT_RETRIEVAL_PROVIDER_EVOLUTION_V1.md`
