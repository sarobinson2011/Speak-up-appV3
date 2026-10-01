# Privacy Engine Certification Basis Model V1

STATE.md remains canonical.  
This document is supporting documentation only.

# 1. Purpose of Certification Bases

A certification basis identifies the published conformance requirements governing one bounded certification evaluation.

Its purpose is to establish exactly which requirements apply when evaluating one published conformance package.

A certification basis provides evaluation scope.

It does not:

- define protocol truth
- create protocol requirements
- evaluate an implementation
- evaluate a package
- record an evaluation outcome
- define certification procedures

# 2. Definition of a Certification Basis

A certification basis is an immutable identification of the published conformance requirements against which one published conformance package is evaluated.

It defines the governing evaluation reference.

It does not define the evaluation method or result.

# 3. Basis Scope

A certification basis identifies:

- one published Privacy Engine protocol generation
- the published conformance requirements applicable to the evaluation
- the bounded requirement set governing the evaluation

Its scope is limited to requirement identification.

A certification basis does not identify or redefine:

- implementation identity
- conformance claim identity
- evidence identity
- artifact identity
- package identity
- certification decision identity

# 4. Basis Contents

A certification basis may contain immutable references to:

- one published protocol generation
- one published conformance requirement set
- applicable compatibility requirements
- applicable conformance requirements

Every included requirement must derive from published protocol truth.

A certification basis contains no:

- implementation evidence
- conformance artifacts
- package contents
- evaluation findings
- scores
- weights
- maturity levels
- probabilistic judgements
- testing procedures

# 5. Basis Identity

A certification basis is identified by its complete immutable requirement composition.

Its identity therefore depends on:

- the identified protocol generation
- the identified published conformance requirements
- the bounded applicability of those requirements

Changing any governing requirement creates a different certification basis.

A certification basis cannot be silently amended while retaining the same identity.

# 6. Relationship to Protocol Generations

A certification basis is subordinate to one published protocol generation.

The protocol generation defines protocol truth.

Published conformance requirements derive from that truth.

The certification basis identifies which of those published requirements govern one bounded evaluation.

A certification basis cannot:

- modify the referenced protocol generation
- extend its semantics
- create new conformance obligations
- reinterpret compatibility
- redefine protocol identity

# 7. Relationship to Packages and Decisions

A conformance package publishes the implementation material supporting one conformance claim.

A certification basis identifies the published requirements governing the evaluation of that package.

A certification decision records whether the identified package satisfies the identified basis.

These responsibilities remain separate:

- packages supply published implementation material
- bases identify governing requirements
- decisions record evaluation outcomes

A certification basis does not modify package identity or package contents.

A certification basis does not determine or modify decision semantics.

# 8. Relationship to Protocol Truth

Protocol generations define truth.

Published conformance requirements derive from protocol truth.

Certification bases identify those requirements for bounded evaluations.

Certification bases never become protocol authority.

They cannot:

- replace protocol generations
- redefine protocol semantics
- redefine compatibility
- redefine conformance
- create implementation obligations not already derived from published requirements

If a certification basis conflicts with the protocol generation it references, the protocol generation governs.

# 9. Conclusion

A certification basis is the immutable identification of the published conformance requirements governing one bounded certification evaluation.

It establishes evaluation scope.

It creates no protocol truth.

It creates no new implementation obligations.

It contains no evidence and records no outcome.

A protocol generation defines truth.

A certification basis identifies the requirements derived from that truth.

A certification decision records only whether one published conformance package satisfies that basis.
