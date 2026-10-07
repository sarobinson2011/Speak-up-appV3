# Focused accepted-clause implementation review

## Governing clauses

The focused source extracts and exact source/excerpt SHA-256 identities are in CLAUSE-MAP-4E.json. S70's retained scope constructor and validator (lines 969–1047) derive a nonempty component seed, close it over all undirected graph links, retain exact scoped token order and lexical unique link order, and keep composition distinct. S70 lines 713–715 require canonical model use, external appointment and ordered collection. S90 lines 739–790 preserve edge identifiers, full model/potential equality, exact scoped row identities, three distinct bundles, whole experiment/target/view qualifications, final outer-profile binding and the unchanged V2 preimages. S90's primitive/source-reference clauses preserve independent source semantics and qualification.

Accepted sources, selected contract, retained model and V4 primitive grammar are unchanged. The source/carrier formats added here are concrete laboratory mechanism metadata, not new protocol serializers or authority appointments.

## Executable changes

`scope_auth/acquisition.py` acquires source/material and four-file bytes from local relative-path manifests. It rejects changed, missing, truncated, oversized and duplicate objects. It does not infer identity from size or timestamps. Partial acquisition reports failures while retaining available inputs for the ordered collector.

`scope_auth/auth.py` integrates exact external appointment equality, four-file identities and signature checks. In the accepted order:

* Signed message: literal `PE-TSE-PRIVACY-EVIDENCE-V2\n` followed by exact evidence.tsv, tokens.tsv and links.tsv bytes, with no added lengths or digest substitution.
* Object SHA-256: literal `PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n` followed by each of evidence.tsv, tokens.tsv, links.tsv, signature.txt prefixed by its unsigned 64-bit big-endian byte length.
* signature.txt: exact appointed authority, ASCII space, lowercase 128-hex signature, LF.

Verification uses the existing cryptography pure Ed25519 API against the original message. A signature over SHA-256(message) fails. This is not Ed25519ph or Ed25519ctx. A valid key/signature does not appoint its holder: the exact appointment is separately supplied and the evidence-authority qualification dependency is required. Actual authority establishment is always false in this laboratory provider.

`scope_auth/closure.py` computes exact static or actual-value connected components. An arbitrary static token connects to every token. In its absence, symbolic-digest groups are cliques; exact actual byte groups govern occurrence equality. A spanning star per clique preserves exact reachability without enumerating its edges. All structural edges participate without visibility or permission filtering. Scope projection preserves original model indexes and relation identities; only TSV row ordinals restart. The unchanged CP4B validator checks exact scoped legal membership, uniqueness, order and separate structural/potential cardinalities. This proves equality of supplied scoped link sets only when all those independent conditions pass; it does not replace serialized-stream hashes.

`scope_auth/scopes.py` and `material.py` acquire a code-bound source seed/view contract and three separate source binding objects. Each object joins the exact scope, phase, model, final outer profile, all four file identities, object digest, complete external security-record bytes, ledger source reference, exact closure and required experiment/target/coalition/rule/qualification coverage. Static construction precedes the final profile; external bundle assertions follow completed profile, records and signatures. No assertion is embedded in the immutable profile or its own signed/object preimage, so these joins create no digest cycle. Declared material dependencies must be completely available, digest-correct, supported and acyclic.

The concrete finite source mechanism requires each required experiment and its entire target/view in every bundle. It does not derive a weaker scope by intersection or accept a caller's omitted experiment. A different actual mechanism needs independently qualified applicability and coverage semantics; it cannot silently inherit these laboratory assumptions. Seed ownership/completeness likewise comes from the independently supplied source contract under explicit classifier/producer/observer hypotheses; signature possession alone does not establish those facts.

The ordered collector still collects available authority, signature, digest, local grammar, model, scope and later semantic failures before selecting inherited ORDER. Source assertion disagreement must not hide independently detectable malformed links. Positive ledger dispositions/budgets are withheld when scope/authentication/qualification prerequisites are missing or inconsistent. A genuinely computed over-budget value remains available with its failure; a dishonest signed PASS does not erase that negative result. `scope_validation.ready` means its prerequisites were bound conditionally; `conditional_checks_pass` additionally requires consistent signed result cells and no collected failures. Neither is actual qualification or admission.

## Full retained model: exact compact result and limits

The verified CP4D domain inventory contains 426,984 tokens, 50 fixed tokens and 91,157,453,467 required potential pairs. Token index 1 is arbitrary. Therefore every nonempty valid static seed reaches every token, and composition covers all tokens. `retained_scope_receipt.py` records that exact reachability deduction and source-owned component-value incidence witnesses. It neither claims an independently qualified complete seed directory nor computes a serialized link/pair hash. Structural and potential sets, exact framing and full byte digests remain separate verification obligations.

## Narrow identifier reconciliation

CP4D correctly reproduced rejection of a literal `SYMBOLIC-U-ONE::SECURITY:ALGORITHM.$record::CP2-ALGORITHM-000001` in OBLIGATION.node_ids. That rejection is not a general impossibility of referencing that part of the model: accepted S90 structural and potential edge IDs are ordinary primitive-compatible IDs, and a template can use an incident edge with an empty node_ids list. `reconcile_identifiers.py` verifies both accepted grammar and the implementation, resolves a real incident structural edge and a legal potential edge from pinned saved model segments, and records all cases.

Edge-only syntax is not, by itself, proof of complete node/edge duty coverage or a qualified ledger. It merely preserves a legal reference path without renaming the token. It does not repair FIELD-LABEL.surface_id: the selected contract directly requires `SECURITY:ALGORITHM.$record`, and this field has primitive ID type with no edge-reference alternative. That specific selected-directory/accepted-grammar incompatibility remains unresolved. No wider definition defect is claimed; no identifier was renamed, escaped, dropped or accepted by a relaxed grammar. CP4B's printable exact model-derived TSV cell treatment remains valid and unchanged; record primitive ID is a separate case.

## Unimplemented large-input authentication

The existing CP4B/4C supplied-link semantic validator is bounded-memory and recoverable, but 4E's file acquisition and pure Ed25519 verifier remain bounded small-message implementations. Streaming exact four-file object hashing, large source/model/outer-container acquisition, and a scalable exact-message pure Ed25519 backend integrated with durable recovery are not implemented. No segmented SHA-256 concatenation, descriptor digest, Ed25519ph or signing a digest is an acceptable replacement. Source authentication, appointment and qualification would remain separate even after that implementation is supplied.
