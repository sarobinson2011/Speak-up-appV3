# Focused checkpoint 4F review

## Source continuity and preimages

The saved CP4E ZIP's CRC and all 981 manifested members verified before edits.
Its exact archive SHA is 02b231f4ef29f38f73dd862fcaf9771fca3827d3d251f87be95088f29b4a108e.
results/4F-source-input-manifest.json pins the retained ancestor archives and
77 unchanged protected files, including accepted sources, V4 ingestion,
ledger/admission/scope logic and supplied-link validators. The retained 4D
archive is additionally verified by prepare_retained.py before its child is
materialized. No completed expansion result was recomputed.

The focused governing clauses are the retained CLAUSE-MAP-4E.json: S70 immutable
outer/V2 framing, external appointment and ordered failures; S90 lines 739–790
exact model/scope identities, four-file joins, final outer binding, result-cell
qualification and unchanged V2 preimages. BACKEND-REVIEW-4F.md addresses the
referenced RFC semantics only; this is not another broad definition review.

Object bytes are the literal OBJECT-V2 domain followed, in order, by each of
evidence.tsv, tokens.tsv, links.tsv and signature.txt, each prefixed by its
unsigned eight-byte big-endian length. The SHA is built from bytes actually
read. Completed individual-file hashes must match expected identities; a
complete object hash is withheld until all files, EOF and expected identity
checks pass. Incomplete files have explicit file_complete=false and prefix
hashes only. Prefix digests never become complete-file digests.

The outer parser incrementally consumes the literal immutable-profile domain,
three exact ordered member names, L64 lengths, nonempty member bytes and EOF.
It hashes the complete outer container and each member's exact bytes. The
metadata join checks the signed evidence row's profile_sha256 against this
final outer identity, not a privacy-member or descriptor hash. It does not claim
semantic validation of arbitrarily large member JSON. Existing bounded 4E
record/source/ledger semantics remain independent prerequisites.

The independent fixture producer manually serializes domains and lengths.
The large synthetic oracle also constructs framing separately. Neither uses
the production object hasher to derive expected object identities. The exact
signed-message iterator has no lengths, signature file or digest substitution.

## Durable acquisition and composition

The job identifies the exact five input files plus descriptor/contract. Durable
state records all byte positions, individual prefix hashes, ordered object
prefix hash, outer parser/header/member state and progress sequence. Live SHA
states are reconstructed from all consumed original bytes on resume. This
avoids relying on an undocumented serializable hashlib/OpenSSL layout. The
journal binds manifest, paths, model/contract, phase, scope and code version.
It uses retained CP4C HMAC/atomic-fsync persistence. Corruption and wrong keys
are rejected; no trusted execution record confers source authentication.

There is no read-ahead beyond the reported consumed boundary. An asynchronous
interrupt may happen between hash/parser updates, so the handler preserves the
last committed state instead of saving a potentially inconsistent in-flight
state. Timed/new-byte pauses occur between completed updates and commit current
state. Every prior byte is checked again on resume, including completed inputs.
Local metadata only guards concurrent changes; it does not establish identity.

The preflight adapter checks external appointment structure/fingerprint,
evidence identity/scope/algorithm, final profile join, table hashes and signature
line/issuer. It then invokes unchanged CP4C recovery for exact legal link
membership, framing, order, uniqueness and separate structural/potential counts.
It binds an existing link journal to this exact input/descriptor/contract, so a
journal from another job cannot be substituted. Required set equality still
needs the retained legal membership + uniqueness + exact separate cardinalities;
a count alone is not completeness. Descriptor/model and scoped-set derivation
must remain source-grounded; arbitrary job metadata does not qualify them.

Available independent failures are collected using unchanged inherited ORDER.
Missing authority, bad bytes and legal-link checks are exercised together.
Pause results are progress only; failures are reevaluated on continuation.
Unavailable crypto and semantic qualification always prevent a successful
integrated verdict. The existing 4E conditional collector is untouched.

## Deliberate limits

This closes large acquisition/object-hash/outer-byte binding and its recovery,
not large signature authentication. The new adapter supports static supplied
link jobs; it does not introduce occurrence semantics or replace the complete
three-scope source/ledger collector. Large token-table semantic parsing, full
outer-member/source acquisition and a scalable bridge into all qualified 4E
scope/ledger mechanisms remain production integration work. Small metadata
caps are explicit capabilities; they do not modify accepted byte grammar.
The canonical model hash in a job is bound, not magically proven to correspond
to an arbitrary descriptor supplied by a caller.

No full retained pair or link stream was touched. Their full hashes remain
unknown/null. Full semantic coverage, serialized stream identity, cryptographic
verification and source qualification remain separate obligations.
