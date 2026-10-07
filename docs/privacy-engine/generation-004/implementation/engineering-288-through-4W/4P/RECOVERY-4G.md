# Exact-message recovery strategy

## Durable binding and state

The signature journal binds the backend executable, build manifest, Rust source,
lockfile, controller/parser code, Python version, exact public key and signature,
signature issuer, absolute job path, exact job bytes, file identities, model,
contract, canonical model hash, scope and phase. The original V2 message length
is derived from the domain and the exact three file lengths. It stores consumed
message offset, SHA-256 of that exact prefix, sequence and progress verdict.
No serialized private library state or hash digest is imported into SHA-512.

Every start/resume constructs a fresh library StreamVerifier. A resume reads
from the beginning through the previous offset, refeeding exactly those original
bytes into the verifier and a separate SHA-256 prefix check. The saved prefix
must match before any new bytes are accepted. It then advances at most the
configured new-byte budget. The eventual SHA-512 state is the same state obtained
by an uninterrupted update sequence, because the original ordered byte sequence
is identical. The SHA-256 check is an identity guard, not an Ed25519 prehash.
A completed journal is also reverified from byte zero; it is not trusted as a
cached authentication result.

The unchanged large_auth.message iterator checks regular-file sizes, shared
locks, per-file exact digests, EOF and mutation markers. The controller continues
to exhaust it after the last message byte so its terminal checks cannot be
skipped. It separately checks exact signature and job bytes before committing.
An expected size or timestamp never establishes an unchanged prefix: the entire
prefix is consumed and hashed again, with exact signature verification at EOF.
These are cryptographic byte identities under the retained hash assumptions,
not a mathematical claim that SHA-256 is injective.

## Read-ahead and interruption

The iterator may have read up to one chunk beyond a pause inside a chunk. Only
bytes actually sent to the native verifier enter the persisted consumed offset
and prefix digest. The unread tail is discarded. The next invocation starts at
byte zero and reconstructs the exact state, so no tail or partially consumed
row is skipped. Cryptographic verification treats table rows as raw bytes;
retained supplied-link parsing/recovery remains a separate semantic stage.

The native process requires exactly LIMIT transport bytes and EOF. When LIMIT
is smaller than TOTAL it returns PAUSED/verified=false and never finalizes a
positive signature result. Premature EOF, extra transport bytes and invalid
encoding/scalar/equation fail. The controller additionally requires full iterator
exhaustion, exact byte counts/digests and a successful process result before it
can commit a verified verdict.

Journal persistence reuses CP4C's HMAC, temporary file, file fsync, atomic replace
and directory fsync. The owner-only key authenticates local journal integrity
only. Before atomic replacement, interruption leaves the old commit usable.
After replacement, the new complete commit is usable. Tests cover both cases.
Signals/errors mid-verification discard in-flight native state and leave the
last durable journal; no attempt is made to save a possibly interrupted state.
A first invocation interrupted before any journal exists must be started again.
A corrupted/incompatible journal is rejected, not repaired by editing. A
known-good previous commit can be restored or a fresh validation started.

## Costs and limitations

For consumed prefix P and newly processed bytes N, a signature resume reads
P+N original message bytes; P are recovery overhead. It needs O(chunk) memory,
not O(P), and a small local journal. Repeated resumes cost sum(P_i) additional
bytes; late resumes of a multi-terabyte message are expensive. No sublinear
unchanged-prefix proof, portable serialized SHA-512 state or segment-hash
substitute is claimed. A deadline too short to replay P makes no progress;
increase the explicitly chosen budget after estimating the recovery cost.

The optional byte+crypto preflight also reruns 4F's exact-byte recovery, including
its separate object-prefix replay cost. Supplied-link semantics require their
own CP4C validation pass and recovery state. These costs must not be hidden by
reporting only signature throughput. No full-stream runtime or identity was
computed in this checkpoint.

Assumptions remain Linux/POSIX regular quiescent inputs, trusted local code/key
and filesystem behavior. Advisory locks do not exclude hostile writers; exact
byte checks detect changed consumed inputs, and mutation markers add guards.
Receipts refer to bytes consumed during that execution, not perpetual immutability
of a pathname. A trusted journal, known key or cryptographic signature grants
neither source appointment, semantic qualification nor actual admission.
