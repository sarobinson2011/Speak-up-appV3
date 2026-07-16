# Privacy Engine Protocol State Model V1

STATE.md remains canonical.
This document is supporting documentation only.

# 1. Purpose of Protocol State

Protocol state defines the minimal architectural state required to preserve the published semantics of the Privacy Engine.

It identifies what the protocol owns.

It does not define implementation.

# 2. Definition of Protocol State

Protocol state is the minimal set of protocol-defined state required to preserve anonymous participation semantics across valid protocol execution.

Protocol state exists independently of any particular implementation.

# 3. Protocol State Identity

Protocol state is defined only by published protocol semantics.

Its identity is determined by:

- protocol-defined state elements
- protocol-defined state transitions
- protocol-defined invariants

It is not determined by implementation structure.

# 4. Protocol-Owned State

Protocol-owned state consists only of state required by published protocol semantics.

Examples include:

- anonymous membership state
- protocol-defined participation state
- protocol-defined uniqueness state
- protocol-defined lifecycle state
- protocol-defined invariant state

Only state required to preserve protocol semantics belongs to the protocol.

# 5. State Outside the Protocol

The following do not constitute Privacy Engine protocol state:

- application state
- user interface state
- backend state
- database state
- cache state
- deployment state
- runtime configuration
- implementation-specific storage
- operational telemetry

Such state may support an implementation but never defines the protocol.

# 6. Relationship to Runtime

The Privacy Engine runtime executes protocol-defined state transitions.

The runtime preserves protocol state.

It does not redefine protocol state.

Execution changes protocol state only through published protocol semantics.

# 7. Relationship to Application State

Application state remains architecturally independent.

Applications may consume protocol outputs.

Applications may maintain their own state.

Application state neither defines nor extends protocol state.

The protocol remains application-agnostic.

# 8. Protocol State Preservation

Every valid implementation must preserve protocol state exactly as defined by the published protocol.

Implementations may differ internally.

They must not alter:

- protocol state identity
- protocol state transitions
- protocol state ownership
- protocol state invariants

Implementation freedom exists only where protocol semantics are preserved.

# 9. Protocol State Invariants

Protocol state must preserve:

- anonymous participation semantics
- protocol-defined ownership of state
- deterministic protocol state transitions
- separation from application state
- preservation of published protocol semantics

No implementation may weaken these invariants.

# 10. Conclusion

Privacy Engine protocol state is the minimal architectural state required to preserve the published anonymous participation semantics of the protocol.

It is owned by the protocol, preserved by the runtime, independent of application state, and defined solely by published protocol semantics.
