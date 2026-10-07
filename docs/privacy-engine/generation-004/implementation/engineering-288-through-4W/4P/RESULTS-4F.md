# Actual checkpoint 4F results

Parent verification: saved CP4E ZIP, 51,930,254 bytes, SHA-256
02b231f4ef29f38f73dd862fcaf9771fca3827d3d251f87be95088f29b4a108e;
CRC and all 981 manifested files passed. The reuse receipt verifies 77 protected
files unchanged and the retained CP4C/4B/4A/3/2/1 archive identities; bootstrap
also checks the exact CP4D identity. No expansion was rerun.

Current executable results are results/4F-verified-regression/check-results.json,
results/4F-targeted-verified.log and results/4F-cli.json. The initial full run passed
211 tests; the final 212-test run passes with the explicit profile-digest
precedence regression. Its first fixture attempt accidentally changed a member
name, correctly yielding schema failure; the corrected fixture changes body
bytes only. Both attempts are retained. The final targeted 25-test run also
includes the two additional noncanonical-key differential probes.
The five new CLI cases cover key creation, pause, resume to exact-byte success,
integrated refusal with valid supplied links, and changed completed input.
All success outputs retain profile_admitted=false.

The test corpus includes an independent exact small-object oracle, 25 new
acquisition/crypto tests, arbitrary chunk boundaries, pauses in headers and
bodies, exact file boundaries, zero-length four-file members, repeated and
terminal resumes, same-size changed prefixes with restored timestamp, changed
suffixes, truncated/missing/extended inputs, wrong journal keys and corrupt
journals, atomic-write interruption, asynchronous mid-parser interruption,
cross-job link journal substitution, all three small scopes and ordered multiple
failures. In-flight signals preserve the prior committed checkpoint.

Two standard RFC8032 vectors pass both installed independent verifiers. Small
signed V2 fixtures and the original-message iterator pass. Adversarial bytes,
keys/signatures, lengths, selected point/scalar encodings, signatures over
digests and actual Ed25519ph are rejected in the recorded cases. The small-order
identity-key differential and two demonstrated noncanonical-key acceptances by
OpenSSL (rejected by libsodium) are recorded, not suppressed; no universal backend
acceptance-equivalence claim is made.

## Measured synthetic byte preflight

results/4F-benchmark.json and .log retain the actual execution. Payload:
100,663,296 bytes (96 MiB), original-message length 100,664,680 bytes, total
outer+four-file acquisition 100,691,096 bytes. Payload is opaque synthetic data,
not a conforming link table, not the retained stream and not signature evidence.

Uninterrupted acquisition: 0.123228 seconds. Pause at 40 MiB: 0.051046 seconds.
Resume: 0.152229 seconds, including 83,859,783 prefix bytes rechecked. Whole
benchmark including generation and independent oracle: 0.576148 seconds;
hard process limit 60 seconds. Total performance benchmark execution this turn
is this single 0.576148-second run, below 180 seconds. Peak child RSS 23,900 KiB
(~23.34 MiB); read chunks <=1 MiB. Temporary disk measured 100,700,104 bytes;
the synthetic payload was removed. No retained semantic-validator performance
is inferred from this warm-cache byte-hashing measurement.

Both uninterrupted and resumed exact V2 object SHA-256 matched the independently
constructed oracle:
e793c05e340224bf0ecb4ac0cd282bd5ef6c9ede307beaa9c9722c255703e440.
Per-file digests matched too. This is a hash of the synthetic object preimage,
not a full retained link/pair stream hash or a signature verification result.

## Capability verdict

Implemented/verified: bounded-memory exact four-file/outer acquisition and
hashing, original-message iteration, durable acquisition recovery and small
static integration with retained supplied-link recovery. Backend candidate
review is documented; incremental pure Ed25519 verification, large cryptographic
recovery and actual admission are NOT implemented. No >64 MiB signature was
verified. Qualification and source authority remain unestablished.

Historical CP4E and predecessor results remain clearly named and retained.
Earlier input-stream/cloud failure causes remain unknown. No reported result
from the original unresponsive cloud workspace has been promoted to verified
implementation evidence. Packaging/fresh-restore evidence is in the 4F-named
restore receipt and the adjacent final ZIP receipt.

The pre-seal ZIP passed fresh extraction, all delivered-file hashes, retained
bootstrap and all five new CLI cases. results/4F-fresh-restore.json records the
pre-seal ZIP identity. The final ZIP adds that receipt and final documentation;
make_package.py separately verifies final CRC and every member hash. A package
cannot include its own final archive hash; that is in the adjacent receipt.
