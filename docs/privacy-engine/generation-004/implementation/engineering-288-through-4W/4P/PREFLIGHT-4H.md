# Bounded computation plan (written before benchmark execution)

No retained pair/link stream is opened. Regression tests reuse descriptors and small fixtures only.

One synthetic conforming transport: 512 arbitrary tokens, two existing symbolic contexts, two surface classes, 130,816 exact potential pairs and two structural rows. Token IDs are 270 ASCII characters. Expected supplied links: approximately 74 MiB; tokens under 200 KiB; model under 300 KiB. The independent fixture loops over this small synthetic universe only. This is not a sample of the retained universe.

Separate processes, each killed at 60 seconds: fixture construction/signing (expected 1–10 seconds; 200–400 MiB peak RSS), exact four-file/object/outer acquisition + pure crypto + streaming token/link checks (expected 5–45 seconds, under 100 MiB validation RSS plus model). At most 120 seconds of benchmark execution; aggregate hard stop remains 180 seconds. Storage estimate under 100 MiB synthetic input plus journals. No stream output is retained in the delivery: reproducible constructor, hashes and results are retained.

The large test establishes transport, cryptographic and supplied-set conformance. It is NOT a complete large three-scope ledger fixture. The retained finite assessor serializes its complete invocation and source dependency objects; an exhaustive 130,816-edge fixture repeated through those records is expected to exceed the 16 MiB record adapter limit and may exceed 1 GiB construction memory. Do not attempt that expansion under this bounded preflight. Small GAMMA/DELTA provide complete conditional collector coverage; production-scale semantic-record/assessor acquisition remains a specific implementation gap. These local caps are not accepted wire limits.

Recovery costs: all completed acquisition/crypto stages are rechecked; token and link parser state is reconstructed by replaying the exact consumed prefix. Repeated small increments have quadratic aggregate I/O. No benchmark extrapolation is conformance evidence or a full-run runtime commitment.
