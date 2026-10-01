# Privacy Engine Protocol Action Model V1

STATE.md remains canonical.

# 1. Purpose

This document defines the architectural model of a Privacy Engine Protocol
Action.

A Protocol Action is the fundamental first-class subject of protocol-use
semantics.

It represents one bounded occurrence of protocol-defined behaviour presented
for evaluation under the rules of one published Privacy Engine protocol
generation.

This document establishes:

- why a Protocol Action is a first-class architectural subject;
- what identifies one Protocol Action occurrence;
- how an action is bounded;
- the distinction between an action type and an action occurrence;
- the relationship between an action attempt and an evaluated action;
- how public inputs and applicable protocol rules relate to an action;
- the distinction between protocol-action validity and proof verification;
- the distinction between action validity and an acceptance determination;
- the consequences of acceptance and rejection;
- the relationship between Protocol Actions and private actors;
- the relationship between Protocol Actions and public state transitions;
- the separation between protocol validity and application-defined meaning;
- the privacy and protocol-authority boundaries governing all actions.

This document does not define an application-specific action.

It defines the general architectural subject through which protocol-defined
behaviour occurs.

# 2. Scope

This document applies to bounded occurrences of behaviour governed by a
published Privacy Engine protocol generation.

It defines:

- Protocol Action identity;
- Protocol Action scope;
- Protocol Action type;
- Protocol Action occurrence;
- action attempts;
- declared public inputs;
- applicable protocol rules;
- protocol-action validity;
- action evaluation;
- action acceptance;
- action rejection;
- possible public consequences;
- relationships to adjacent architectural subjects.

This document does not define:

- petition signing;
- voting;
- credential presentation;
- application payload schemas;
- transport protocols;
- transaction formats;
- proof-system internals;
- public-input schemas;
- implementation-specific execution flows;
- application truth;
- legal truth;
- factual truth.

Application-specific behaviour may be realized through Protocol Actions only
when that behaviour is defined by the applicable protocol generation,
Protocol Specification, and implementation profile.

Application meaning remains outside the Protocol Action model.

# 3. Primary Definition

A Privacy Engine Protocol Action is one bounded occurrence of protocol-defined
behaviour, presented through an implementation for evaluation under the
applicable rules of one published Privacy Engine protocol generation, carrying
its declared public inputs and receiving one acceptance or rejection
determination.

Let:

- `P` be one published Privacy Engine protocol generation;
- `S` be one Privacy Engine Protocol Specification;
- `F` be one implementation profile;
- `I` be one implementation;
- `X` be one private actor;
- `A` be one Protocol Action;
- `T` be one Protocol Action type;
- `PI` be one declared public-input set;
- `R` be the applicable protocol-rule set;
- `Z` be one proof;
- `V` be one proof-verification determination;
- `D` be one action-acceptance determination;
- `C` be the applicable evaluation context;
- `U` be one public state transition;
- `M` be application-defined meaning.

The implementation-facing derivation remains:

> derives(S, P)

> derives(F, S)

> implements(I, F)

A Protocol Action occurrence is related to these subjects by:

> occurrenceOf(A, T)

> governedBy(A, P)

> performedThrough(A, I)

> carries(A, PI)

> applicableRules(A, R)

> evaluatedIn(A, C)

> evaluates(D, A)

A private actor may perform the action:

> performs(X, A)

A proof may support the action:

> supports(Z, A)

A verification determination evaluates the proof and the declared public
inputs required by the proof relation:

> verifies(V, Z, PI)

An action-acceptance determination evaluates the Protocol Action:

> evaluates(D, A)

The action receives exactly one authoritative protocol outcome:

> accepts(D, A) xor rejects(D, A)

An accepted action may produce a public state transition:

> accepts(D, A) -> mayProduce(A, U)

An application may assign meaning to an action:

> interpretsApplication(A, M)

Application interpretation does not become part of Protocol Action identity or
protocol validity.

# 4. First-Class Subject Test

A proposed first-class architectural subject must possess an identity, scope,
validity relation, evaluation relationship, lifecycle position, or consequence
that cannot be reduced to another existing architectural subject.

The Protocol Action satisfies this test.

It possesses:

- an independently bounded occurrence;
- an action type;
- declared public inputs;
- applicable protocol rules;
- an evaluation context;
- protocol-action validity;
- one acceptance or rejection determination;
- possible public consequences.

A Protocol Action cannot be reduced to its actor because the performer and the
performed occurrence are distinct.

It cannot be reduced to its type because one type may classify many action
occurrences.

It cannot be reduced to its public inputs because data values do not constitute
the occurrence that carries them.

It cannot be reduced to its proof because the proof supplies bounded evidence
supporting the action.

It cannot be reduced to proof verification because proof verification is one
determination contributing to action evaluation.

It cannot be reduced to action acceptance because an acceptance determination
evaluates the action.

It cannot be reduced to a public state transition because a transition is a
possible consequence of an accepted action.

It cannot be reduced to an implementation because an implementation realizes
the behaviour through which many actions may occur.

It cannot be reduced to application meaning because application interpretation
is external to protocol validity.

Therefore:

> independentIdentity(A)

> independentScope(A)

> independentValidityRelation(A)

> independentEvaluation(A)

> independentOutcome(A)

> independentPublicConsequence(A)

> irreducible(A)

> firstClass(A)

A Privacy Engine Protocol Action is a distinct first-class architectural
subject.

Its recognition does not reintroduce the rejected Protocol Claim model.

# 5. Protocol Action Identity

Every Protocol Action occurrence possesses its own bounded architectural
identity.

Protocol Action identity identifies exactly one occurrence of protocol-defined
behaviour presented for protocol evaluation.

It does not identify:

- the private actor;
- a wallet;
- a membership secret;
- an enrollment event;
- an admission event;
- an action type by itself;
- a proof by itself;
- a public-input set by itself;
- a transaction by itself;
- an acceptance determination;
- a resulting state transition;
- application-defined meaning.

Formally:

> identity(A) != identity(X)

> identity(A) != identity(T)

> identity(A) != identity(Z)

> identity(A) != identity(PI)

> identity(A) != identity(V)

> identity(A) != identity(D)

> identity(A) != identity(U)

> identity(A) != identity(M)

Action identity is occurrence identity.

This model does not require one universal technical action identifier.

An applicable Protocol Specification or implementation profile may define the
coordinates by which an occurrence is represented, distinguished, or
referenced.

Those coordinates must preserve the architectural distinction between the
action occurrence and the private actor.

Therefore:

> identifiesAction(id(A), A)

> identifiesAction(id(A), A) =/=> identifiesActor(id(A), X)

No action identifier may become a reusable participant identifier or a
cross-action identity mechanism.

# 6. Protocol Action Scope and Boundedness

A Protocol Action is bounded by the protocol behaviour presented for one
evaluation.

Its scope includes:

- one action occurrence;
- one action type;
- one declared public-input set;
- one applicable protocol-rule set;
- one applicable evaluation context;
- one action-acceptance determination;
- one acceptance or rejection outcome.

Formally:

> bounded(A)

> oneOccurrence(A)

> oneType(A, T)

> onePublicInputSet(A, PI)

> oneApplicableRuleSet(A, R)

> oneEvaluationContext(A, C)

> oneDetermination(A, D)

The action does not absorb:

- the identity or history of the actor;
- unrelated actions;
- the implementation as a whole;
- the protocol generation as a whole;
- transport attempts;
- application workflows;
- application interpretation;
- every downstream consequence.

A logical action occurrence must not be silently widened merely because an
implementation retries transport, submission, or internal processing.

An applicable specification must determine whether repeated authoritative
presentations represent:

- repeated attempts concerning one occurrence; or
- distinct action occurrences.

The general Protocol Action model does not infer or merge identity across such
presentations.

# 7. Action Type and Action Occurrence

A Protocol Action type is a protocol-defined classification of behaviour.

A Protocol Action occurrence is one bounded instance of that behaviour
presented for evaluation.

Formally:

> defines(P, T)

> occurrenceOf(A, T)

The type determines which protocol rules and public-input requirements are
applicable to the occurrence.

> occurrenceOf(A, T) -> selectsApplicableRules(T, R)

> occurrenceOf(A, T) -> selectsPublicInputRequirements(T)

An action type may classify multiple action occurrences:

> occurrenceOf(A1, T)

> occurrenceOf(A2, T)

> A1 != A2

Therefore:

> T != A

An action type is not performed as an individual occurrence.

An occurrence is not itself the general type.

This document defines the action occurrence as the first-class Protocol Action.

It does not introduce a separate first-class action-type ontology beyond the
classification required to determine applicable protocol behaviour.

# 8. Action Attempt

An action attempt is an effort to construct, present, submit, or obtain
evaluation of a candidate Protocol Action occurrence.

An attempt is not automatically an evaluated Protocol Action.

Local construction, abandoned preparation, transport failure, unavailable
infrastructure, or failure before the authoritative evaluation boundary does
not constitute protocol rejection.

Formally:

> attempts(X, candidateA)

does not by itself imply:

> evaluates(D, A)

or:

> rejects(D, A)

A Protocol Action occurrence enters the protocol-action model when a bounded
candidate is admitted to the applicable authoritative evaluation boundary.

> admittedForEvaluation(candidateA) -> instantiates(candidateA, A)

> instantiates(candidateA, A) -> evaluates(D, A)

An action that reaches authoritative evaluation may be accepted or rejected.

> evaluates(D, A) -> accepts(D, A) xor rejects(D, A)

Transport failure is not protocol invalidity.

Pre-evaluation refusal is not action rejection unless the applicable protocol
rules explicitly place that refusal within the authoritative evaluation
boundary.

The distinction is:

> attempt -> possible evaluation

> evaluation -> acceptance xor rejection

The attempt supplies no independent protocol authority.

# 9. Declared Public Inputs

Every Protocol Action carries the public-input set declared for its action type
by the applicable protocol rules.

Formally:

> carries(A, PI)

> declaredFor(PI, T)

> occurrenceOf(A, T)

Declared public inputs are the public values required to evaluate the action.

They may participate in:

- proof verification;
- action-type validation;
- state-dependent validation;
- uniqueness enforcement;
- permitted-context validation;
- public consequence determination.

The public inputs do not constitute the action occurrence.

> PI != A

The same value may appear in more than one permitted public-input set without
making the corresponding actions identical.

Public inputs must be limited to values required by the applicable protocol
rules.

They must not introduce:

- actor identity;
- wallet identity;
- membership-secret material;
- enrollment provenance;
- admission provenance;
- unnecessary participant identifiers;
- reusable cross-action identifiers;
- application-only correlation fields.

The declared public-input set must preserve the privacy semantics of the
published protocol generation.

# 10. Applicable Protocol Rules

Every Protocol Action is evaluated under one bounded set of applicable protocol
rules.

Formally:

> governedBy(A, P)

> occurrenceOf(A, T)

> applicableRules(A, R)

The applicable rules derive from the published protocol generation through the
implementation-facing specification structure:

> derives(S, P)

> derives(F, S)

> implements(I, F)

The action type, implementation profile, protocol state, and permitted
evaluation context may determine which requirements apply.

> determinesApplicability(T, F, C, R)

Applicable rules may constrain:

- action shape;
- required public inputs;
- proof requirements;
- permitted protocol state;
- root validity;
- nullifier or uniqueness conditions;
- domain separation;
- action authorization without actor identification;
- acceptance consequences.

Applicable rules must not be invented by an implementation during evaluation.

> applicableRules(A, R) -> derivesRules(R, P)

Implementation policy may control whether an implementation offers or
transports an action, but implementation policy does not silently become
protocol validity.

# 11. Protocol-Action Validity

Protocol-action validity is the property that one Protocol Action satisfies all
applicable protocol rules in its applicable evaluation context.

Formally:

> protocolValid(A, C) iff satisfiesAll(A, R, C)

where:

> applicableRules(A, R)

Protocol-action validity is:

- action-specific;
- rule-relative;
- context-bounded;
- determined by protocol semantics;
- independent of application truth.

It is not reducible to successful proof verification.

A verified proof may establish one or more required validity conditions:

> verifiesValid(V, Z, PI) -> establishesEvidence(V, A)

But:

> verifiesValid(V, Z, PI) =/=> protocolValid(A, C)

unless proof verification is the complete applicable rule set for that action.

Other applicable conditions may include public-input validity, state validity,
uniqueness, permitted-root status, or action-type constraints.

Conversely, protocol validity does not imply any external factual or legal
claim.

> protocolValid(A, C) =/=> externallyTrue(M)

The published protocol generation determines the semantics from which
protocol-action validity derives.

# 12. Action Acceptance

Action acceptance is the positive outcome of the authoritative evaluation of
one Protocol Action.

Formally:

> evaluates(D, A)

> accepts(D, A)

Acceptance recognizes that the evaluated action satisfies the applicable
protocol requirements at the applicable evaluation context.

For a correct protocol realization:

> correctEvaluation(D, A, C) ->
> (accepts(D, A) iff protocolValid(A, C))

Acceptance does not create protocol validity by discretion.

It recognizes validity under the applicable rules.

An implementation error may produce an incorrect determination, but that error
does not redefine the protocol semantics:

> incorrect(D) =/=> changesSemantics(P)

An accepted Protocol Action may produce one or more protocol-defined public
consequences:

> accepts(D, A) -> mayProduce(A, U)

Acceptance does not establish:

- the identity of the private actor;
- application truth;
- legal truth;
- factual truth;
- ownership of the action by a disclosed person;
- a Protocol Claim.

Acceptance establishes only the protocol outcome defined by the applicable
rules.

# 13. Action Rejection

Action rejection is the negative outcome of the authoritative evaluation of
one Protocol Action.

Formally:

> evaluates(D, A)

> rejects(D, A)

For a correct protocol realization:

> correctEvaluation(D, A, C) ->
> (rejects(D, A) iff not protocolValid(A, C))

Rejection means that the action did not satisfy one or more applicable protocol
requirements in the applicable evaluation context.

Rejection does not mean:

- that the private actor has been identified;
- that the actor is permanently ineligible;
- that an application proposition is false;
- that a legal or factual claim is false;
- that every future action attempt must fail;
- that transport or infrastructure merely failed before evaluation.

A rejected Protocol Action produces no accepted-action state transition:

> rejects(D, A) -> not producesAcceptedTransition(A, U)

Rejection may produce only such bounded public rejection consequence as the
applicable protocol expressly defines.

The general model does not require public persistence of rejected actions.

# 14. Relationship to Private Actors

A private actor may perform a Protocol Action:

> performs(X, A)

The actor and action remain distinct:

> X != A

The action is public to the extent required by the applicable protocol.

The actor remains private to the extent guaranteed by the protocol privacy
model.

The governing principle is:

> Private actors, public actions.

Action validity must depend on satisfaction of the applicable protocol rules,
not disclosure of the actor’s civil, wallet, enrollment, admission, or
application identity.

A Protocol Action must not require or imply disclosure of:

- actor identity;
- wallet identity;
- membership secret;
- enrollment provenance;
- admission provenance;
- reusable participant identity;
- cross-action identity.

Formally:

> performs(X, A)

> public(A)

> private(X)

> public(A) =/=> identified(X)

> identity(A) =/=> identity(X)

Where protocol rules prove possession, membership, authorization, eligibility,
or uniqueness, they do so only according to the privacy-preserving semantics of
the published protocol generation.

# 15. Relationship to Proofs

A proof may support the validity of one Protocol Action:

> supports(Z, A)

The proof and action are distinct:

> Z != A

A proof supplies evidence concerning the statement and public inputs defined by
the applicable proof relation.

It does not by itself constitute:

- the action occurrence;
- the action type;
- the complete applicable rule set;
- the action-acceptance determination;
- the resulting public state transition;
- application meaning.

The same proof system may support multiple action types or occurrences without
making those actions identical.

A Protocol Action may require one proof, multiple proofs, or no proof only where
the applicable published protocol semantics permit that structure.

This document does not redefine proof identity, proof construction, proof
verification, or cryptographic soundness.

It preserves the existing proof architecture.

# 16. Relationship to Public Inputs

A Protocol Action carries its declared public inputs:

> carries(A, PI)

The action and its public inputs are distinct:

> A != PI

Public inputs expose only the values required for public protocol evaluation.

They describe protocol-relevant coordinates of the action but do not disclose
the private witness or private actor.

A public-input set does not independently possess:

- action occurrence identity;
- action acceptance;
- action rejection;
- public consequence authority;
- application meaning.

The interpretation of public inputs remains bounded by the applicable protocol
rules.

An application must not treat the mere presence of a public value as proof of
meaning not established by the protocol.

# 17. Relationship to Verification

Proof verification is a bounded determination concerning a proof and its
declared public inputs.

Formally:

> verifies(V, Z, PI)

Verification and Protocol Action evaluation are distinct:

> V != D

> V != A

A successful proof-verification determination may contribute evidence to the
action-acceptance determination:

> verifiesValid(V, Z, PI) -> contributesTo(V, D)

A failed required proof-verification determination prevents protocol validity:

> requiredFor(V, A)

> verifiesInvalid(V, Z, PI) -> not protocolValid(A, C)

Successful verification does not necessarily establish complete
protocol-action validity:

> verifiesValid(V, Z, PI) =/=> protocolValid(A, C)

Action evaluation must also enforce every other applicable protocol rule.

Verification proves only what the applicable proof relation establishes.

It does not establish actor identity, application truth, legal truth, or factual
truth.

# 18. Relationship to Implementations

A Protocol Action is performed through an implementation:

> performedThrough(A, I)

The implementation realizes one implementation profile:

> implements(I, F)

The implementation profile derives from one Protocol Specification:

> derives(F, S)

The Protocol Specification derives from one published protocol generation:

> derives(S, P)

An implementation may provide:

- action construction;
- input validation;
- proof generation or receipt;
- proof verification;
- protocol-state evaluation;
- action submission;
- action-acceptance determination;
- public consequence realization.

The implementation does not own protocol semantics.

> realizes(I, P)

> realizes(I, P) =/=> authorizesSemantics(I, P)

Implementation-specific transport, storage, execution, or transaction choices
do not redefine Protocol Action identity unless the applicable specification
expressly makes those coordinates semantically relevant.

A defective implementation may incorrectly process an action.

That defect is an implementation failure, not a new protocol rule.

# 19. Relationship to Public State Transitions

An accepted Protocol Action may produce a protocol-defined public state
transition:

> accepts(D, A) -> mayProduce(A, U)

The action and transition are distinct:

> A != U

The transition is downstream of action acceptance:

> A -> D -> U

where the transition exists only when permitted by the applicable protocol
rules.

A Protocol Action cannot be reduced to a public state transition because:

- rejected actions do not produce accepted-action transitions;
- accepted actions may produce only a public record or other non-mutating
  consequence;
- one accepted action may authorize multiple bounded state effects;
- the transition is a consequence rather than the evaluated occurrence.

A public transition must not disclose private-actor information beyond what the
published protocol generation permits.

The transition must preserve the action’s privacy boundary:

> produces(A, U) -> preservesPrivacy(U, A)

Public observability of the transition does not authorize reconstruction of the
private actor.

# 20. Relationship to Application Semantics

An application may interpret a Protocol Action:

> interpretsApplication(A, M)

Application-defined meaning and Protocol Action identity remain distinct:

> M != A

Applications may describe accepted actions using domain-specific concepts.

Those concepts may include application-specific assertions, choices, signals,
requests, or records.

Such interpretation remains outside the Protocol Action’s protocol validity.

Formally:

> protocolValid(A, C) =/=> applicationTrue(M)

> applicationTrue(M) =/=> protocolValid(A, C)

> interpretsApplication(A, M) =/=> incorporatesMeaning(A, M)

The protocol determines whether the action satisfies protocol rules.

The application determines what application-level meaning it assigns to the
action.

No intermediate Protocol Claim object exists.

Application meaning must not be promoted into protocol authority merely because
it is attached to an accepted action.

# 21. Protocol Validity and External Truth

Protocol validity and external truth are separate semantic domains.

Protocol validity asks:

> Did the Protocol Action satisfy all applicable protocol rules in the
> applicable evaluation context?

External truth asks questions defined outside the protocol, including whether
an application proposition is factually, legally, socially, or institutionally
true.

The Privacy Engine establishes only protocol validity.

It does not establish external truth.

Formally:

> protocolValid(A, C) iff satisfiesAll(A, R, C)

But:

> protocolValid(A, C) =/=> factuallyTrue(M)

> protocolValid(A, C) =/=> legallyTrue(M)

> protocolValid(A, C) =/=> sociallyAccepted(M)

> protocolValid(A, C) =/=> institutionallyRecognized(M)

Likewise:

> externallyTrue(M) =/=> protocolValid(A, C)

An application may treat an accepted action as evidence that protocol-defined
conditions were satisfied.

It must not describe that result as proof of an external proposition unless an
independent external system supplies that authority.

This boundary preserves the Engineering[138] determination that no Protocol
Claim object exists.

# 22. Preservation of Privacy Semantics

Every Protocol Action must preserve the privacy semantics of the published
protocol generation.

The core invariant is:

> Private actors, public actions.

Public action identity identifies the occurrence, not the actor.

> identifiesAction(id(A), A)

> identifiesAction(id(A), A) =/=> identifiesActor(id(A), X)

A Protocol Action must not introduce or require:

- actor identity;
- wallet-bound identity;
- secret disclosure;
- enrollment provenance;
- admission provenance;
- reusable participant identifiers;
- cross-action identity;
- unnecessary public correlation fields;
- implementation-specific identity reconstruction.

Where action uniqueness is required, uniqueness must be established according
to the applicable privacy-preserving protocol semantics.

Action uniqueness must not silently become participant identity.

> uniqueForScope(A) =/=> reusableIdentity(X)

Where authorization is required, authorization must not silently become actor
identification.

> authorized(A) =/=> identified(X)

Where multiple public actions are observed, their public occurrence must not
create cross-action linkage beyond what the published protocol expressly
defines.

No implementation, profile, application, or action type may weaken these
privacy semantics while continuing to represent itself as preserving the same
protocol generation.

# 23. Preservation of Protocol Semantics

The Protocol Action model organizes protocol-use semantics.

It does not redefine them.

Every applicable action rule derives from the published protocol generation:

> applicableRules(A, R) -> derivesRules(R, P)

The implementation-facing chain remains:

> derives(S, P)

> derives(F, S)

> implements(I, F)

The protocol-use chain is:

> performs(X, A)

> performedThrough(A, I)

> carries(A, PI)

> supports(Z, A)

> verifies(V, Z, PI)

> evaluates(D, A)

> accepts(D, A) xor rejects(D, A)

> accepts(D, A) -> mayProduce(A, U)

Application interpretation remains external:

> interpretsApplication(A, M)

> M != A

The preservation rule is:

> semantics(A) subsetOf semantics(P)

A Protocol Action cannot add, remove, or reinterpret protocol semantics.

An implementation cannot convert implementation behaviour into protocol
authority.

An application cannot convert application meaning into protocol validity.

A proof cannot establish more than its defined proof relation.

An acceptance determination cannot establish more than the applicable protocol
rules authorize.

# 24. Protocol Authority

Protocol authority always remains with the published Privacy Engine protocol generation.

The Protocol Specification derives from that generation.

Implementation profiles derive from the Protocol Specification.

Implementations realize implementation profiles.

Protocol Actions occur through implementations and are evaluated under rules
derived from the published protocol generation.

No Protocol Action possesses authority to redefine:

- the protocol generation;
- protocol semantics;
- privacy semantics;
- proof semantics;
- public-input semantics;
- validity requirements;
- implementation requirements;
- conformance;
- certification.

No implementation, application, actor, proof, verification determination,
acceptance determination, or public state transition becomes protocol authority
merely by participating in a Protocol Action.

Formally:

> authority(P)

> derives(S, P)

> derives(F, S)

> implements(I, F)

> governedBy(A, P)

> authority(A) = false

Protocol authority always remains with the published Privacy Engine protocol generation.

# 25. Explicit Exclusions

This document does not:

- define petition signing;
- define voting actions;
- define credential actions;
- define application payload schemas;
- define transport protocols;
- define transaction formats;
- define proof construction;
- define proof-system internals;
- redefine proofs;
- redefine public inputs;
- redefine proof verification;
- define implementation-specific action identifiers;
- require transaction hashes as action identities;
- redefine implementations;
- redefine implementation profiles;
- redefine conformance;
- redefine certification;
- introduce action ownership;
- introduce actor identity;
- introduce wallet identity;
- introduce reusable participant identifiers;
- introduce cross-action linkage;
- introduce enrollment provenance;
- introduce admission provenance;
- introduce legal truth;
- introduce factual truth;
- introduce institutional truth;
- introduce application truth as protocol truth;
- reintroduce a Protocol Claim;
- authorize implementations to redefine protocol rules;
- authorize applications to redefine protocol validity;
- redefine protocol semantics;
- redefine protocol authority.

The model defines only the architectural identity, boundaries, relationships,
evaluation, and possible consequences of a Privacy Engine Protocol Action.

# 26. Conclusion

A Privacy Engine Protocol Action is one bounded occurrence of protocol-defined
behaviour, presented through an implementation for evaluation under the
applicable rules of one published Privacy Engine protocol generation, carrying
its declared public inputs and receiving one acceptance or rejection
determination.

The Protocol Action possesses:

- independent occurrence identity;
- independent scope and boundedness;
- an applicable action type;
- declared public inputs;
- applicable protocol rules;
- protocol-action validity;
- an authoritative evaluation relationship;
- an acceptance or rejection outcome;
- possible public consequences.

It cannot be reduced to:

- the private actor;
- the action type;
- the proof;
- the public inputs;
- proof verification;
- action acceptance;
- an implementation;
- a public state transition;
- application meaning.

Therefore:

> firstClass(A)

The Protocol Action is a distinct first-class architectural subject.

Its identity identifies the public action occurrence, not the private actor.

Proof verification contributes evidence to action evaluation but does not
necessarily constitute complete protocol-action validity.

Acceptance recognizes protocol validity under the applicable rules.

Rejection records failure to satisfy those rules within the authoritative
evaluation boundary.

Application meaning remains outside the Protocol Action.

Protocol validity remains distinct from external truth.

No Protocol Claim model is introduced.

The governing privacy principle remains:

> Private actors, public actions.

Protocol authority always remains with the published Privacy Engine protocol generation.
