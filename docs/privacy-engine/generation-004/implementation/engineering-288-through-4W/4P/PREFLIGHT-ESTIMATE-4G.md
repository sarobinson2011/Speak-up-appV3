# Pre-computation estimate

Only a 96 MiB synthetic opaque links.tsv payload is constructed. The V2 signed
message includes exact evidence.tsv/tokens.tsv/links.tsv bytes and the original
domain. It is not a valid complete-model link table and will not enter link
semantics or admission. No retained full stream is read or generated.

Estimated disk: ~100–150 MiB temporary fixture, removed after results. Signing
and independent one-shot verification use cryptography/OpenSSL and libsodium,
not the candidate backend. Estimated signing/reference peak RSS 200–400 MiB;
streaming native verifier plus Python controller under 40 MiB. Expected total
fixture/sign/reference/stream/recovery time 2–20 seconds, uncertain by hardware.
Measure signer, established verifier, and streaming/recovery worker separately.
Each child has a hard 60-second wall-clock limit. Aggregate child execution
must stay below 180 seconds; record elapsed times and stop on timeout.

Planned passes: construct payload and exact expected file/object identities;
one-shot original-message signing (two internal message passes); independent
one-shot verifier; streaming uninterrupted verification; pause at 40 MiB;
resume by refeeding every consumed original message byte, then remaining bytes.
Recovery costs exactly P replay bytes plus N new message bytes, with a fresh
library SHA-512 verification state and SHA-256 prefix identity check. No digest
is imported as verifier state. A prefix replay that exceeds the configured
deadline makes no progress and preserves the last checkpoint. Repeated resumes
cost the sum of their prefix lengths. Optional full 4F byte/object acquisition
adds its documented separate passes; it is not folded into signature timing.

Toolchain preparation, estimated before execution: ~120 MiB downloads, under
1 GiB working space, a few minutes; retain verified tarballs/cache/target files
for recovery. These are build operations, not performance benchmarks. The
pinned Rust compiler and all registry dependencies are verified/preserved for
rebuilding; the delivered build uses offline locked vendored sources.
