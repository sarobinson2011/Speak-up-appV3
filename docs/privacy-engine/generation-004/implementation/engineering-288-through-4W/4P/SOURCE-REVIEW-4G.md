# Focused source-level backend compatibility analysis

## Verdict and authority boundary

COMPATIBLE THROUGH A THIN CANONICAL-ENCODING ADAPTER; BUILT AND TESTED.
The adapter calls established library decompression and canonical compression
for A and R, compares their bytes with the originals, and delegates pure
streaming verification to pinned ed25519-dalek 2.2.0. It adds no curve or scalar
arithmetic. This is an implementation analysis, not competent external security
qualification, source appointment or an amendment to the accepted definition.

## Exact source paths

The complete unmodified upstream sources and their licences are vendored under
crypto_backend/vendor. Cargo.lock pins registry checksums; BUILD-MANIFEST.json
hashes every vendored file, adapter inputs and executable. The separately
retrieved ed25519-dalek 2.2.0 crate has the same checksum as the locked vendor
package. SOURCE-MAP-4G.json pins the focused files and line ranges below.

* curve25519-dalek 4.1.3, src/edwards.rs: CompressedEdwardsY::decompress and its
  step_1/step_2 check whether a curve point exists and select x's sign. This
  decoder alone accepts some noncanonical representations.
* EdwardsPoint::compress obtains affine coordinates, canonically serializes y,
  and adds x's parity bit. src/backend/serial/u64/field.rs::as_bytes reduces to
  the canonical field representative; src/field.rs::is_negative reads parity
  from canonical bytes. The pinned build explicitly selects the serial backend
  on x86_64, using this reviewed u64 field implementation.
* ed25519-dalek src/signature.rs::check_scalar uses Scalar::from_canonical_bytes
  when legacy_compatibility is absent. src/scalar.rs enforces the scalar's
  canonical range. The locked feature graph contains no legacy_compatibility.
* VerifyingKey::verify_stream parses InternalSignature before creating
  StreamVerifier. StreamVerifier uses RCompute<Sha512> with no prehash context.
  RCompute seeds SHA-512 with the original R and A encodings, then receives each
  original message chunk. Its finish delegates scalar reduction and group work
  to the library and canonically encodes the result of -[k]A + [S]B. The final
  comparison is against the original, adapter-validated R encoding.

VerifyingKey::to_bytes is NOT a canonicality test: that type retains the
original compressed public-key bytes. The adapter instead decompresses to an
EdwardsPoint and calls point.compress().to_bytes(). This distinction resolves
4F's precise obstacle; no input is silently normalized and then accepted.

## Compatibility argument

For each exactly 32-byte A/R input, successful library decompression establishes
that the encoded y admits a curve point. Re-encoding emits canonical y and the
parity of the recovered x. Byte equality therefore rejects y >= p and the
x=0/sign-bit-one encodings, while preserving both legitimate sign choices for
nonzero x. It also rejects nonsquare/unrecoverable encodings through the decoder.
These are the RFC8032 section 5.1.3 decoding conditions. No small-order or
prime-subgroup policy is added: canonical torsion points remain decodable, and
the canonical identity A/R with S=0 passes its valid verification equation.

S is checked without reducing an out-of-range supplied scalar. Hash reduction
and group operations occur only inside the pinned library. The resulting
uncofactored equation [S]B = R + [k]A is explicitly permitted by RFC8032 section
5.1.7. It can reject some signatures accepted by the cofactored equation; this
is the RFC-permitted choice, not an implicit strict or ZIP-215 policy. The
adapter never calls verify_strict, verify_prehashed, or a low-level bespoke
verification implementation.

The exact V2 signed message remains literal SIGN_DOMAIN followed by evidence.tsv,
tokens.tsv and links.tsv, without length prefixes. large_auth.message supplies
those original bytes. Object L64 framing remains a separate unchanged 4F hash.
Neither the object's SHA-256, a message SHA-256, nor concatenated segment hashes
is passed as the message to Ed25519. The SHA-256 maintained during verification
only checks consumed identity and journal replay. Pure Ed25519's own incremental
SHA-512 is maintained by the library.

## Primary references

RFC8032 sections 5.1.3, 5.1.7 and 7:
https://www.rfc-editor.org/rfc/rfc8032.html

Pinned API/source documentation:
https://docs.rs/ed25519-dalek/2.2.0/src/ed25519_dalek/verifying.rs.html
https://docs.rs/ed25519-dalek/2.2.0/ed25519_dalek/struct.VerifyingKey.html
https://docs.rs/curve25519-dalek/4.1.3/curve25519_dalek/edwards/struct.CompressedEdwardsY.html

The local downloaded/vendor source files, not a web snippet or mutable latest
release, are the executable review basis. Accepted S70/S90 V2 clauses and their
hashes remain in retained CLAUSE-MAP-4E.json. Model/contract/source identities
remain unchanged; no broader definition review was performed.

## What the tests establish and do not establish

Tests directly exercise canonical/noncanonical boundaries, both x sign bits,
non-points, S=0/L-1/L/above-L encodings, the exact 4F OpenSSL discrepancies,
canonical small-order acceptance, RFC known-answer vectors, wrong variants,
byte changes, lengths and recovery. The >64 MiB fixture is independently signed
by OpenSSL and verified by both OpenSSL and libsodium before streaming checks.
Those reference libraries are independent ordinary-signature checks, not the
canonicality oracle: their recorded encoding disagreements remain explicit.
The source argument supplies the general rule; finite tests are not exhaustive
proofs over all points/scalars, and neither is external competent qualification.
