# Privacy Engine Protocol Operation Model V1

STATE.md remains canonical.  
This document is supporting documentation only.

# 1. Purpose of Protocol Operations

Protocol operations identify the published semantic invocations through which protocol state transitions may be requested.

They do not:

- define protocol state
- define transition semantics
- bypass transition enforcement
- directly mutate protocol state
- create implementation authority

# 2. Definition of a Protocol Operation

A protocol operation is a published semantic invocation that requests one published protocol state transition.

An operation identifies the transition being requested and the published semantics governing that request.

It is not an implementation function, interface, transaction, or execution mechanism.

# 3. Operation Boundary

A protocol operation begins at the published semantic request boundary.

It ends with exactly one of two outcomes:

- one valid protocol state transition
- no protocol state transition

No partial protocol outcome exists.

# 4. Relationship to Transition Enforcement

A protocol operation does not mutate protocol state.

It invokes one published transition-enforcement boundary.

Transition enforcement determines whether the requested transition can derive exactly one valid successor state.

The semantic sequence is:

    Operation
        ->
    Transition Enforcement
        ->
    Successor-State Derivation
        ->
    State Transition or No Transition

Direct mutation is forbidden:

    Operation -> Direct State Mutation

# 5. Operation Identity

A protocol operation is identified by its published semantic definition.

Its identity includes:

- the transition requested
- the required source-state conditions
- the published preconditions
- the permitted semantic outcome

Implementation details do not define operation identity.

# 6. Operation Outcome

An operation succeeds only when transition enforcement derives exactly one valid successor state.

Success:

    Operation(S) -> S'

Failure:

    Operation(S) -> S

Failure does not produce:

    partial(S')
    repaired(S')
    inferred(S')
    substituted(S')

# 7. Operation Determinism

For the same valid source state and the same published operation semantics, the protocol outcome is deterministic.

The operation does not choose among multiple successor states.

If exactly one valid successor state cannot be derived, no transition occurs.

# 8. Operation Composition

Multiple protocol operations remain distinct semantic invocations.

One operation must not silently introduce, merge, substitute, or complete another operation.

Any composed protocol behavior must preserve:

- each operation's published identity
- each transition boundary
- deterministic successor-state derivation
- all published protocol invariants

Composition does not create a direct state-mutation path.

# 9. Relationship to Protocol Authority

Published protocol semantics determine:

- which operations exist
- what transition each operation requests
- the operation's preconditions
- the permitted outcome

Implementations realize published operations.

Applications and operators may request them.

Neither implementations, applications, nor operators define their semantics.

# 10. Relationship to Protocol Invariants

Every successful protocol operation preserves all published protocol invariants.

An operation cannot complete by weakening, bypassing, repairing, or redefining an invariant.

If invariant preservation is impossible, the operation produces no protocol state transition.

# 11. Conclusion

A Privacy Engine protocol operation is a published semantic invocation that requests one published protocol transition.

Operations never mutate protocol state directly.

They invoke transition enforcement, which derives exactly one valid successor state while preserving all published protocol invariants.

If no valid successor state can be derived, the operation produces no protocol state transition.
