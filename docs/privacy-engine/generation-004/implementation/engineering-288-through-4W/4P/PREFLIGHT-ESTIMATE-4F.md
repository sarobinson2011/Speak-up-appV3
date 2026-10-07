# Estimate recorded before the synthetic benchmark

Only synthetic opaque data is used. No retained pair/link stream is opened.
One 96 MiB `links.tsv` payload tests byte acquisition; it deliberately is not a
conforming link table and is never sent to the semantic link validator.
Its exact original V2 message is larger than 64 MiB. No large signature is
created or verified; the pure incremental verifier remains unavailable.

Plan: generate in <=1 MiB blocks, derive an independent streaming object oracle,
run uninterrupted acquisition, then pause at 40 MiB and resume. One benchmark
child has a hard 60-second timeout; aggregate benchmark cap is 180 seconds.
Estimated local time 2–20 seconds, strongly dependent on CPU and page cache;
timeout records incomplete results rather than extending the budget.
Temporary disk approximately 100–150 MiB; remove the reproducible synthetic
payload afterwards. Output receipts/journals are kilobytes. Process RSS expected
30–80 MiB including Python/crypto fixture imports; acquisition buffers <=1 MiB
and independent of input size. Journal and job metadata each capped at 1 MiB.
The retained semantic validator separately needs model-sized memory; inherited
4B/4C measurements remain applicable and are not new authentication benchmarks.

Let O be outer bytes, F total four-file bytes, D model descriptor+contract bytes,
and P consumed four-file prefix, Q consumed outer prefix. Start reads O+F+D.
Each resume reads D+Q+2P before new bytes: one full consumed-prefix recheck and
one ordered-object hash reconstruction. Hash objects are reconstructed, not
imported from their digests. Supplied-link semantics add a separate link pass,
with the retained CP4C exact-prefix replay on continuation. Cryptographic
verification would add a separate exact signed-message pass, but is unavailable.
No cryptographic recovery cost is claimed. Exact input prefix validation can
be expensive: replay deadlines must cover the complete prefix; a too-small
deadline leaves the previous checkpoint intact and makes no progress. Execution
deadlines are configurable; the 60-second rule caps benchmarks, not protocol
file sizes. At full retained link size (~19.91 TB) even one pass takes many
hours, and repeated near-end resumes multiply reads. Use measured storage
throughput and an approved recovery schedule before authorizing such a run.
