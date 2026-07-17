# Privacy Engine Protocol Operation Model V1

STATE.md remains canonical.
This document is supporting documentation only.

# 1. Purpose of Protocol Operations

A protocol operation defines the published request by which a protocol transition is evaluated.

Its purpose is to identify exactly one published transition for evaluation.

It does not:

- define protocol states
- define protocol invariants
- define transition semantics
- determine eligibility
- perform enforcement
- perform execution

# 2. Definition of a Protocol Operation

A protocol operation is an immutable published protocol request identifying one published transition for evaluation.

It defines the request.

It does not define the outcome.

# 3. Operation Identity

Operation identity is defined by the published operation itself.

It is independent of:

- implementations
- execution mechanisms
- transport
- invocation method

Changing implementation does not change operation identity.

# 4. Operation Scope

A protocol operation identifies:

- one published transition
- the request for evaluation

It does not determine whether the transition may execute.

# 5. Relationship to Protocol Transitions

A protocol operation requests evaluation of exactly one published transition.

Given:

    O = published protocol operation

    T = published protocol transition

the protocol defines:

    O ⇒ request(T)

Operations request transitions.

They do not redefine them.

# 6. Relationship to Transition Preconditions

Transition preconditions determine whether the requested transition is eligible.

Operations neither satisfy nor modify those preconditions.

# 7. Relationship to Enforcement

Enforcement evaluates whether the requested transition satisfies its published preconditions.

Enforcement is not part of the operation.

# 8. Relationship to Execution

Execution realizes a published transition after successful evaluation.

Execution is not part of the operation.

# 9. Implementation Independence

Operations remain identical across all implementations.

Implementations may realize operations through different mechanisms without altering their published semantic identity.

# 10. Protocol Authority

Operations are defined only by the published protocol generation.

Implementations may realize published operations.

They never redefine them.

# 11. Conclusion

A protocol operation is the immutable published request for evaluation of one published protocol transition.

It identifies what is requested.

Eligibility, enforcement, execution, and resulting state remain distinct protocol concepts.
