# Pure Ed25519 backend review and explicit implementation boundary

Decision: **no incremental verifier is enabled**. This checkpoint uses the
user-authorized fallback: independent exact-byte acquisition/hashing/recovery
is complete and executable, while exact-message cryptographic verification and
its recovery remain unavailable. No homemade point/scalar arithmetic was added.

## Accepted target

S70 and S90 retain ED25519-RFC8032 over the exact original message, with no
prehash variant or message-digest substitution. The signature message is
`PE-TSE-PRIVACY-EVIDENCE-V2\n || evidence.tsv || tokens.tsv || links.tsv`.
It has no L64 prefixes. signature.txt is outside that message. See the retained
CLAUSE-MAP-4E.json for exact accepted-source hashes and excerpts.

RFC 8032 sections 5.1.3/5.1.7 require 32-byte point encodings, decoded y below
2^255-19, a recoverable x coordinate, and rejection of x=0 with sign bit one.
Signatures contain R and S; S must be below the group order. Both public-key
and R decoding must succeed. Verification uses SHA-512 on R, A and the original
message for pure Ed25519. The cofactored equation is specified; the uncofactored
equation is also expressly permitted. A blanket small-order rejection must not
be silently conflated with these exact decoding/equation rules. Standard vectors
alone cannot establish equivalence over all encodings.

Primary reference (reviewed 2026-10-04):
https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1.7

## Reviewed candidate, pinned but NOT built or selected for execution

`ed25519-dalek = 2.2.0`, `hazmat` feature, `VerifyingKey::verify_stream` provides
incremental message processing. Its public-key constructor documents ZIP-215
point validation and explicitly says RFC8032/NIST point criteria are unsupported.
Its strict verifier is documented as differing from RFC8032; scalar range checks
are present in its verification functions. Simply changing to strict verification
therefore does not establish the required acceptance language.

Dependency: a competent cryptographic review of exact A/R encoding and equation
acceptance, followed by a reproducible, vendored, locked build and an adapter
that feeds the original bytes. No Rust toolchain/dependency build was available
in this runtime. This is not a claim that pure incremental verification is
impossible, or that the accepted definition needs modification. If this candidate
cannot match the retained semantics using reviewed library APIs, select another
established implementation. Do not write replacement group/scalar arithmetic.

Primary reference:
https://docs.rs/ed25519-dalek/2.2.0/ed25519_dalek/struct.VerifyingKey.html

## Installed established reference paths

cryptography 46.0.0 uses bundled OpenSSL 3.5.3 for one-shot pure Ed25519 tests.
OpenSSL's documented Ed25519 API does not provide DigestUpdate streaming.
This is not a bounded-memory exact-message solution at retained sizes.
https://docs.openssl.org/3.0/man7/EVP_SIGNATURE-ED25519/

libsodium 1.0.18 supplies an independent one-shot verifier for small fixtures.
Its multipart signature API implements Ed25519ph, which changes the variant;
it is deliberately used only to construct a rejected adversarial fixture.
https://doc.libsodium.org/public-key_cryptography/public-key_signatures

Exact installed binary SHA-256 identities, reference version pins, known-answer
vectors and all probe outcomes are in results/4F-backend-observations.json.
`python3 -m large_auth.audit` reproduces the observations and reports pin matches.
These installed binaries are not vendored in the ZIP. No backend equivalence or
full cryptographic audit is claimed.

## Actual bounded observations

Both independent verifiers accepted RFC8032 section 7.1 tests 1 and 2 and the
independent small V2 signed fixture. They rejected changed messages, wrong keys
and signatures, malformed lengths, S=L, selected noncanonical R/key encodings,
a negative-zero R fixture, true Ed25519ph, and signatures over SHA-256/SHA-512
of the message. The canonical identity-key/R, S=0 probe was accepted by OpenSSL
and rejected by libsodium. Two additional identity-key probes with noncanonical
y=p+1 and x=0/sign-bit-one encodings were also accepted by OpenSSL and rejected
by libsodium. These latter encodings violate the RFC decoding rules; this is a
demonstrated limitation of the retained one-shot reference path, not merely a
difference over valid small-order encodings. 4E conditional results do not prove
full RFC encoding acceptance. The new preflight never grants authentication
through that path; resolving this decoder compatibility is part of the open
backend dependency, without a local custom curve decoder. This differential is intentionally retained; a
small-order encoding is not automatically an invalid RFC decoding.

Selected invalid-signature fixtures do not isolate every decoder rule, and these
probes are not an exhaustive acceptance proof. No incremental verifier, large
signature check, durable crypto state, or cryptographic recovery test passed
because none is implemented. The 96 MiB test establishes byte hashing only.

`large_auth.message.signed_message` streams the exact original preimage to a
future verifier and validates consumed-file identities at exhaustion. A consumer
that stops early cannot obtain a verification result. The iterator is not a
cryptographic verifier and its digest checks cannot be used in place of one.
