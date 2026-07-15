# Privacy Engine Application Runtime Boundary V1

STATE.md remains canonical.
This document is supporting documentation only.

# 1. Purpose

This document defines the implementation responsibility boundary between:

- the application
- the application adapter
- the Privacy Engine runtime

It does not redesign the protocol.

It does not define implementation structure, migration, deployment, or contract extraction.

# 2. Boundary Principle

The application chooses the action context.

The Privacy Engine verifies anonymous participation within that context.

The Privacy Engine does not understand application meaning.

# 3. Application Responsibility

The application owns:

- application objects
- application metadata
- application lifecycle
- application policy
- application-specific eligibility
- the meaning of an accepted action
- the consequence of an accepted action
- application-specific records and events

For the petition application, this includes:

- petition creation
- petition existence
- petition metadata
- petition lifecycle
- the meaning of a petition signature
- petition-specific signature records
- petition-specific read models

These responsibilities remain outside the Privacy Engine runtime.

# 4. Privacy Engine Runtime Responsibility

The Privacy Engine runtime owns authoritative anonymous-action verification for an application-supplied action context.

It owns:

- proof verification
- public-signal validation
- membership-root validation
- nullifier enforcement
- anonymous-action acceptance or rejection
- protocol-level duplicate prevention
- preservation of protocol invariants
- publication of the protocol-valid action result

The runtime determines only:

> whether a valid anonymous member performed one valid action within the supplied action context.

It does not determine what that action means.

# 5. Application Adapter Responsibility

The application adapter is the boundary between application meaning and protocol verification.

It owns:

- receiving the application-selected action context
- preserving that context
- presenting the context to the Privacy Engine runtime
- receiving the runtime result
- returning that result to the application
- applying no independent interpretation of protocol validity

The adapter must not:

- choose a different action context
- redefine protocol acceptance
- duplicate proof verification
- duplicate membership-root validation
- duplicate nullifier enforcement
- modify protocol outputs
- expose application meaning to the runtime

# 6. Action Context

The action context is selected by the application.

It identifies the application action for which anonymous participation is being verified.

For the current petition implementation:

`petitionId` is the action context.

At the protocol boundary:

`petitionId` functions as `actionId`.

The runtime requires only the stable action context value.

It does not require knowledge that the value represents a petition.

# 7. Anonymous-Action Acceptance

Anonymous-action acceptance requires:

- a valid proof
- the locked public signal structure
- a valid membership root
- a nullifier derived for the supplied action context
- an unused nullifier within that context

Acceptance means only:

> anonymous participation is protocol-valid for the supplied action context.

Acceptance does not mean:

- the application object exists
- the application permits the action
- the action has application meaning
- application state has been updated
- application policy has been satisfied

Those remain application responsibilities.

# 8. Responsibility Sequence

The responsibility sequence is:

Application chooses action context.

Application Adapter preserves action context.

Privacy Engine Runtime verifies anonymous participation.

Application Adapter returns the verification result.

Application applies the application-specific consequence.

Formally:

A = application-selected action context

Application:
    choose A

Adapter:
    preserve A

Runtime:
    verify anonymous participation within A

Adapter:
    return accepted(A) or rejected(A)

Application:
    apply application consequence only after accepted(A)

Forbidden paths:

Runtime chooses A

Runtime interprets A

Runtime changes A -> A'

Adapter repairs or replaces A

Application redefines runtime acceptance

# 9. PetitionRegistry Responsibility Split

The current PetitionRegistry contains both petition-application and Privacy Engine runtime responsibilities.

Protocol responsibilities currently present within it include:

- proof verification
- membership-root validation
- public-signal validation
- nullifier uniqueness enforcement
- anonymous-action acceptance

Petition-application responsibilities currently present within it include:

- petition creation
- petition existence
- petition metadata association
- petition-specific action records
- petition-specific events
- petition signature consequences

The current co-location does not change responsibility ownership.

Protocol enforcement remains Privacy Engine responsibility.

Petition meaning remains application responsibility.

# 10. Invariant Preservation

This boundary preserves:

- the existing ZK circuit
- public signal ordering
- leaf = Poseidon1(memberSecret)
- nullifier derivation
- membership-root semantics
- one action per anonymous member per action context
- TEMPEST execution semantics
- REFLECT path semantics
- frontend secret-custody semantics
- frontend privacy semantics
- externally visible petition behaviour

No cryptographic or protocol semantic change is required.

# 11. Application Independence

The Privacy Engine runtime is application-independent when:

- the application supplies an action context
- the runtime verifies anonymous participation against that context
- the runtime does not know the application object type
- the runtime does not know the application policy
- the runtime does not determine the application consequence
- application semantics can change without changing protocol verification

Application independence does not require hypothetical application support.

It requires only the absence of petition meaning from runtime responsibility.

# 12. Minimum Runtime Boundary

The minimum application-independent runtime is the authority that:

1. accepts an application-supplied action context
2. verifies the anonymous-action proof
3. validates the membership root
4. enforces nullifier uniqueness
5. returns authoritative acceptance or rejection

Nothing else is required by this boundary.

# 13. Conclusion

The application owns action meaning.

The application chooses the action context.

The application adapter preserves and conveys that context.

The Privacy Engine runtime authoritatively verifies anonymous participation within that context.

The runtime does not understand, select, modify, or apply application meaning.

The current implementation already contains this runtime responsibility.

The remaining alignment requirement is to preserve this responsibility boundary explicitly at the implementation level.
