# Privacy Engine Protocol Execution Model V1

STATE.md remains canonical.
This document is supporting documentation only.

# 1. Purpose of Protocol Execution

Protocol execution realizes an eligible published protocol transition.

Its purpose is to preserve the transition selected by the published protocol operation after enforcement has determined eligibility.

Execution does not determine eligibility.

Execution does not define successor state.

Execution introduces no independent protocol semantics.

# 2. Definition of Protocol Execution

Protocol execution is the realization of an eligible published protocol transition according to its published semantics.

Execution realizes exactly the transition requested by the published protocol operation.

Execution has no authority to reinterpret, substitute, repair, merge, or infer another transition.

# 3. Execution Inputs

Execution receives:

- the current protocol state
- one eligible published protocol operation
- the published transition requested by that operation

Eligibility has already been determined before execution begins.

# 4. Execution Preconditions

Execution is permitted only when the published operation has been determined eligible by protocol enforcement.

If enforcement does not determine eligibility, execution is not permitted.

# 5. Determinism

Execution preserves the published transition selected by the operation.

It introduces no independent selection.

It introduces no alternative interpretation.

Execution therefore preserves protocol determinism.

# 6. Execution Result

Execution produces exactly one of:

- realization of the published transition
- failure

Execution does not produce alternative transitions.

Execution does not redefine protocol semantics.

# 7. Relationship to Protocol Operations

Protocol operations request transitions.

Execution realizes the transition requested by the operation.

Operations define what is requested.

Execution realizes what has already been selected.

# 8. Relationship to Enforcement

Enforcement and execution are separate protocol concepts.

Enforcement determines whether execution is permitted.

Execution realizes the already-eligible transition.

Execution never performs enforcement.

Enforcement never performs execution.

# 9. Relationship to Protocol Transitions

Execution realizes the published transition exactly as defined.

Execution has no authority to:

- redefine transitions
- repair transitions
- substitute transitions
- merge transitions
- infer transitions

The published transition remains authoritative throughout execution.

# 10. Relationship to Successor State

Execution realizes a published transition.

It does not define successor-state identity.

It does not determine successor-state validity.

Successor state is a separate semantic object.

# 11. Failure Semantics

Execution either:

- realizes the published transition

or

- fails.

Failure never authorizes realization of another transition.

Failure never substitutes a different transition.

Failure does not redefine enforcement.

Failure does not redefine successor-state validity.

# 12. Implementation Independence

Execution is a protocol concept.

Its meaning does not depend upon:

- smart contracts
- RPC
- APIs
- wallets
- relayers
- databases
- storage engines
- transport protocols
- certification machinery

Implementations realize execution.

They do not define it.

# 13. Protocol Authority

Execution derives its authority solely from the published protocol generation.

Implementations realize published execution semantics.

They do not modify, reinterpret, or extend those semantics.

Protocol authority remains with the published protocol generation.

# 14. Conclusion

Protocol execution is the realization of an eligible published protocol transition according to its published semantics.

Execution preserves the transition selected by the published protocol operation, introduces no independent discretion, and produces either realization or failure.

Enforcement and successor state remain separate protocol concepts.
