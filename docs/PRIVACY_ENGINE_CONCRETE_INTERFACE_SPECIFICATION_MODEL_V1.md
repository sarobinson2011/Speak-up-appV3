# Privacy Engine Concrete Interface Specification Model V1

STATE.md remains canonical.
This document is supporting documentation only.

# 1. Purpose of Concrete Interface Specifications

A concrete interface specification defines the published representation through which one identified Privacy Engine interface contract is realized for one bounded integration surface.

Its purpose is to specify syntax, not protocol meaning.

It does not:

- define protocol semantics
- define protocol truth
- define protocol invariants
- define protocol transitions
- define internal implementation behavior

# 2. Definition of a Concrete Interface Specification

A concrete interface specification is a published syntactic realization of one identified Privacy Engine interface contract for one bounded integration surface.

It defines representation.

It does not define meaning.

# 3. Specification Scope

A concrete interface specification may define:

- operation names
- invocation form
- input representation
- output representation
- field ordering
- type constraints
- encoding rules
- transport binding
- externally observable error representation
- specification version
- mapping to one identified interface contract

It does not define protocol semantics.

# 4. Relationship to Interface Contracts

The governing interface contract defines published meaning.

The concrete interface specification defines how that meaning is represented.

Every concrete interface specification realizes exactly one identified interface contract.

Protocol authority remains with the interface contract.

# 5. Syntactic Realization

A concrete interface specification defines representation only.

It may choose any syntactic representation that preserves the governing interface contract.

Representation choices do not create protocol semantics.

# 6. Semantic Preservation

Representation may vary.

Published meaning must not vary.

Let:

- C be a published interface contract
- S be a concrete interface specification

S realizes C only when:

> semantics(S) = C

Any ambiguity in S is resolved in favour of C.

# 7. Multiple Realizations

Multiple concrete interface specifications may realize the same interface contract.

Different representations do not imply different protocol semantics.

Equivalent meaning may be realized through different representations.

# 8. Compatibility and Change

A representation-only change is not a protocol change when the governing interface-contract semantics remain preserved.

Representation may change.

Published meaning must remain invariant.

If representation no longer preserves the governing interface contract, the change is no longer representation-only.

# 9. Relationship to Implementations

Implementations realize both:

- the governing interface contract
- the concrete interface specification

Implementations remain replaceable while published interface-contract semantics are preserved.

# 10. Specification Authority

A concrete interface specification defines representation.

It does not acquire protocol authority.

It cannot redefine protocol meaning.

# 11. Protocol Authority

Protocol authority always remains with the published interface contract.

If conflict exists between a concrete interface specification and its governing interface contract, the interface contract governs.

# 12. Conclusion

A concrete interface specification defines the published representation through which one interface contract is realized for one bounded integration surface.

It defines representation, not meaning.

Representations may differ.

Implementations may differ.

Published interface-contract semantics must remain invariant.

Protocol authority remains with the interface contract.
