# Actual checkpoint 4G evidence

Backend verdict: compatible through the canonical library decode/re-encode
adapter; executable built, reproduced and tested. Incremental pure exact-message
verification and full-prefix reconstruction recovery are implemented. This is
not competent external qualification. Actual admission remains disabled.

## Parent, source and build verification

CP4F ZIP: 65,377,122 bytes, SHA-256
905e2e55a0826adbcd339b1c8f2cf0150256c47060cd3d241a5fa3a57756cbb4.
CRC and all 1,091 manifested files passed before construction. The 4G reuse
manifest verifies 85 protected source/implementation/input files unchanged,
including all large_auth files. Accepted sources, complete model identity and
selected finite contract are preserved. Exact predecessor archives remain nested
and recoverable. No expansion was rerun.

Pinned backend: ed25519-dalek 2.2.0, curve25519-dalek 4.1.3, sha2 0.10.9;
Rust/cargo 1.85.1; offline locked vendored builds. Executable: 440,816 bytes,
SHA-256 3d8b65ea87eb5b5a680c9c51c6897a8c32641f1580947046d1cc6c7f765c152b.
A clean rebuild under a different source root and target directory produced
identical bytes. Both build logs and the comparison receipt are included.
Compiler components total 112,687,308 downloaded bytes; the retained scratch
setup, extracted installers, caches and two builds occupied about 1.1 GiB,
slightly above the initial under-1-GiB estimate. These scratch toolchain binaries
are not bundled; exact download hashes and installer commands are included.
The delivered native verifier and all 36 locked registry dependency sources are
bundled. Build/OS/linker identities and upstream licences are preserved.

## Tests actually run

results/4G-final-regression/check-results.json: **228 tests passed**, zero
failures/errors, and all four retained admission CLI cases passed. Protected
accepted/retained inputs stayed unchanged. The expected negative-validator
messages at the beginning of the summary log are adversarial checks, not
unreported suite failures.

results/4G-targeted-final.log: **16 focused tests passed**, including RFC pure
vectors, all retained 4F discrepancies, canonical small-order acceptance,
noncanonical A/R encodings, both signs of zero, non-points, scalar boundaries,
Ed25519ctx/Ed25519ph and digest-signature rejection, exact EOF/truncation/trailing
bytes, native process interruption, independent small V2 signing/verification,
chunk/file/domain boundaries, repeated and terminal recovery, altered prefixes
with restored mtime, changed suffixes, wrong journal keys, corrupt journals,
backend/key/signature/model-manifest substitution, interrupted atomic writes
before and after replacement, mid-stream interruption, and outer-byte tampering.
The first 15-test attempt contained a no-op signature mutation (the replacement
hex digit already matched); its failed log is retained. Correcting the fixture
to always alter the byte resolved it; no acceptance rule was weakened.

results/4G-cli.json: **eight new CLI cases passed**: key creation, two durable
pauses, completion, terminal re-verification, byte+crypto preflight pause/resume,
and rejection of mutated completed input. Every result retains admission=false.

## Independently signed large exact-message test

results/4G-large-message.json records 100,663,296 synthetic payload bytes and
100,664,676 exact original V2 message bytes. OpenSSL/cryptography independently
signed it; OpenSSL and libsodium independently verified it. The new backend then
verified it uninterrupted and after a 41,943,040-byte pause/replay. All complete
message identities matched SHA-256:
8b22dde86d0f09913959bc5e0a074d411ebe89065b3e731ea5a89ddd61234079.
That SHA is an observed exact-message identity, never the Ed25519 message input.

| Separate process | Wall time including launch | Peak RSS |
| --- | ---: | ---: |
| Fixture generation/signing | 0.646000 s | 218,804 KiB |
| Independent one-shot verifiers | 0.580718 s | 216,600 KiB |
| Streaming controller + recovery | 1.011699 s | controller 22,468 KiB; native children 22,444 KiB |

The native-child figure is process high-water accounting and can include fork/
launch overhead. It is separate from signing memory and is a conservative bound,
not exact cryptographic workspace. Native reads are 64 KiB; controller chunks
<=1 MiB. Individual verification timings: uninterrupted 0.418933 s; pause
0.145821 s; resumed 0.377393 s, including complete 40 MiB prefix reconstruction.
Aggregate benchmark execution was **2.238418 seconds**. Every child was capped
at 60 seconds, with a 180-second aggregate cap. No additional performance
benchmarks were run. Temporary fixture disk: 100,699,968 bytes, then removed.
The estimate was recorded before execution in PREFLIGHT-ESTIMATE-4G.md.

The payload is deliberately opaque synthetic data, not a conforming full-model
link table. This establishes large exact-message crypto and recovery capability,
not semantic link completeness, full-universe conformance or authoritative
qualification. No full retained pair/link stream was generated, replayed,
validated or hashed; those complete-stream digests remain null/uncomputed.

## Packaging and restoration

The initial ZIP attempt rejected upstream pre-1980 timestamps. The archive
writer now clamps ZIP metadata timestamps while preserving all member bytes;
the affected operation and successful correction are recorded. Fresh extraction
then passed delivered-file hashes, retained bootstrap and all eight CLI cases.
results/4G-fresh-restore.json pins that pre-seal archive. The final archive adds
this receipt/documentation and separately passes CRC and every member hash.
Its final archive SHA is in the adjacent receipt rather than a circular
self-hash inside the ZIP.
