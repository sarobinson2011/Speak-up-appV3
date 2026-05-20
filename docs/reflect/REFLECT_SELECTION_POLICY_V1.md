# REFLECT_SELECTION_POLICY_V1

## State Selection

Client deterministically selects the highest recent valid publication state.

Selection is derived entirely from client-verifiable publication-state semantics.

Mirrors do not determine state validity, state priority, or state acceptance.

---

## Selection Inputs

Selection is derived from:

- bounded publication-window ordering
- publication-state validity
- coherent publication-state identity
- deterministic client interpretation
- connector/chunk compatibility
- integrity verification

Selection is not derived from:

- mirror preference
- mirror freshness claims
- adaptive routing behavior
- topology awareness
- availability optimization
- federation consensus
- runtime popularity
- probabilistic retrieval behavior

---

## Highest Recent Valid State

“Highest recent valid publication state” means:

- highest according to deterministic publication-window ordering
- recent according to bounded publication-window policy
- valid according to client-derived verification
- coherent as one publication-state lifecycle boundary

This does not mean:

- latest mirror response
- most available object set
- dynamically preferred state
- adaptive state choice
- cross-state reconstruction candidate

---

## Coherence Constraint

A selected publication state is atomic for witness construction purposes.

Selection must preserve:

- publication state ID
- root
- protocol interpretation
- connector/chunk relationship
- deterministic state target

A client must not combine objects from different publication states.

---

## Fallback Constraint

Fallback may replace the mirror used to retrieve an object.

Fallback must not:

- alter publication-state selection
- trigger adaptive reselection
- mutate the deterministic state target
- introduce cross-state recovery
- weaken connector separation constraints

Fallback is bounded object retrieval substitution only.

---

## No External Influence

- mirrors do not suggest state
- mirrors do not authorize state
- no randomness is required
- no adaptive routing is required
- selection is fully client-derived
- selection must remain topology-neutral
