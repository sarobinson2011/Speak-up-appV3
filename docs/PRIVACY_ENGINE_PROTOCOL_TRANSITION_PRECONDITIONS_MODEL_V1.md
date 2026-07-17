# Privacy Engine Protocol Transition Preconditions Model V1

STATE.md remains canonical.  
This document is supporting documentation only.

# 1. Purpose of Transition Preconditions

Protocol transition preconditions determine whether one identified published transition is eligible to derive a successor protocol state.

They do not:

- define valid protocol state
- define transition effects
- request a transition
- mutate protocol state
- define implementation-local restrictions

# 2. Definition of a Protocol Transition Precondition

A protocol transition precondition is a published transition-specific semantic condition that must be satisfied before one identified published transition may derive a successor state.

A precondition governs transition eligibility.

It does not itself derive or modify protocol state.

# 3. Precondition Identity

A precondition is identified by its published semantic definition and the identified transition it governs.

The protocol specification determines:

- which preconditions exist
- which transition each precondition governs
- what constitutes satisfaction

A condition associated only with implementation behaviour is not a protocol transition precondition.

# 4. Precondition Scope

Preconditions are transition-specific.

For an identified transition \(T\), let:

\[
P(T)
\]

denote the complete published set of preconditions governing \(T\).

A condition belongs to \(P(T)\) only when published protocol semantics assign it to \(T\).

An implementation cannot alter \(P(T)\).

# 5. Relationship to Source State

Preconditions are evaluated in relation to the valid source state from which the transition is requested.

Given:

\[
S = \text{valid source state}
\]

\[
T = \text{identified published transition}
\]

transition eligibility requires:

\[
\forall p \in P(T),\ \mathrm{satisfied}(p,S,T)
\]

Source-state validity is not itself a transition precondition.

It is established by protocol invariants before transition eligibility is considered.

Where \(P(T)\) is empty, the universal satisfaction condition is true. The transition therefore has no additional transition-specific eligibility conditions beyond the already-required valid source state and identified published transition.

# 6. Relationship to Protocol Operations

A protocol operation requests execution of one identified published transition.

The operation does not:

- define the transition's preconditions
- determine what constitutes satisfaction
- imply that the preconditions are satisfied
- authorize successor-state derivation by itself

Operation invocation initiates transition enforcement.

Transition eligibility remains determined exclusively by the published preconditions governing the identified transition.

# 7. Precondition Satisfaction

All required preconditions must be satisfied exactly as published.

Eligibility is:

\[
\mathrm{Eligible}(S,T)
\iff
S\ \text{is valid}
\land
T\ \text{is identified}
\land
\forall p \in P(T),\ \mathrm{satisfied}(p,S,T)
\]

Precondition satisfaction permits successor-state derivation to proceed.

It does not guarantee a successor state unless the published transition can derive exactly one valid successor state.

# 8. Unsatisfied Preconditions

If any required precondition is unsatisfied:

\[
S \rightarrow S
\]

No protocol state transition occurs.

Transition enforcement must not:

- infer satisfaction
- weaken the failed precondition
- substitute another condition
- repair the source state
- perform a partial transition
- derive an alternate successor state

Failure preserves the original protocol state.

# 9. Distinction from Protocol Invariants

A protocol invariant defines a property that must hold across every valid protocol state.

A protocol transition precondition defines a condition that must hold before one identified transition may derive a successor state.

Therefore:

\[
\text{Invariant}
\rightarrow
\text{validity of protocol state}
\]

\[
\text{Precondition}
\rightarrow
\text{eligibility of one transition}
\]

Preconditions do not replace invariants.

Invariants do not define the complete transition-specific eligibility conditions of every transition.

# 10. Transition Enforcement

Transition enforcement evaluates the published preconditions governing the identified transition.

It does not define them.

Success path:

\[
S
\rightarrow
\mathrm{preconditions\ satisfied}
\rightarrow
\mathrm{derive}(S')
\]

Failure path:

\[
S
\rightarrow
\mathrm{precondition\ unsatisfied}
\rightarrow
S
\]

Precondition evaluation and successor-state derivation remain distinct semantic stages.

# 11. Implementation-Local Restrictions

An implementation may impose external restrictions on whether it:

- exposes an operation
- accepts an operation request
- submits an operation for transition enforcement

Such restrictions are implementation-local.

They do not:

- become protocol preconditions
- alter \(P(T)\)
- redefine transition eligibility
- alter protocol semantics
- establish protocol authority

An implementation restriction may prevent an operation from being offered or requested. It cannot change whether the published protocol transition itself is eligible.

# 12. Protocol Authority

Published protocol semantics exclusively determine:

- precondition existence
- precondition identity
- transition assignment
- satisfaction semantics
- transition eligibility

Implementations evaluate published preconditions.

They must not:

- weaken them
- strengthen them
- add protocol preconditions
- remove protocol preconditions
- infer missing preconditions
- replace published preconditions
- silently supplement them

Any change to a protocol transition precondition is a change to published protocol semantics.

# 13. Conclusion

A Privacy Engine protocol transition precondition is a published transition-specific semantic condition that must be satisfied before successor-state derivation may occur.

All required preconditions must be satisfied exactly as published.

If any required precondition is unsatisfied, no protocol state transition occurs and the source state remains unchanged.

Published protocol semantics define preconditions.

Implementations only evaluate them.
