# Recovery

This is a new compact correction checkpoint. Verify the delivered ZIP identity, CRC, exact membership and MANIFEST.json after fresh extraction. `python -B code/verify_package.py` performs read-only local membership/hash checks. Begin with REPORT.md and review/findings.json. The unchanged predecessor report/results are under prior/ and are historical, not current correction receipts.

Inspect code diffs under results/, corrected code, field coverage, original minimal witness and current results. Source/runtime reference bytes are pinned by reference/hashes.json. No entire predecessor archive is nested.

Optional focused reproduction (Python 3 with cryptography, no network):

    python -B code/check_response_envelope.py
    python -B code/check_integration.py

These write local test results; preserve the packaged saved receipts first if reproducing in place. Prefer a disposable extracted copy. The first script uses public laboratory authentication seeds solely for two synthetic parser fixtures and negative response-association controls; it never invokes transaction signing or the candidate scheduler. Its old-code subprocess deliberately reproduces IA-01 using review/old-code plus unchanged helper modules. The witness remains byte-exact. The original review scripts are provenance and need their original review layout; do not run them in this reduced tree.

For normal CLI entry:

    python -B code/pipeline.py ingest --input review/independent/F1-minimal.json --output /tmp/i164-corrected-response-new.json

Output must not exist. Immutable SQLite acquisition still requires quiescent files and an independently authoritative expected HEAD; bundled fixture HEADs remain laboratory evidence, not protected operational anchors. Final canonical binding always refuses while its obligations remain unresolved.

Preserve these separately:

| Predecessor | Bytes | Entries | SHA-256 |
|---|---:|---:|---|
| Formal-Lab-Engineering-288C-I164-option-a-integration-review.zip | 16408060 | 148 | 523a5818cceeace3e46382015110766004e006a285a131ee7b2c49e323bb0e2c |
| Engineering-288C-I164-option-a-integration.zip | 2363307 | 102 | 27dcf10c9b7548ff0e8cda4fd1ca5fdcc606f6cec0052f5837cdf7234c22b86f |
| Engineering-288C-I164-option-a-correspondence.zip | 6781314 | 54 | 8b6cc960a73c20271242529a607e6dd31a45ed7cf2e6592609e1364b46e742a0 |

Prior recovery identities and adoption records remain in provenance/, reference/ and prior/RECOVERY.md. The original retry ZIP remains unavailable: 54,899,989 bytes / 1f06a4034fab8ab7e0c17ea409ea15d113c9106f63bbfad96291fcb1368e5f09. The incomplete copy remains 50,045,652 bytes / 859cbc5f79a032ed07c24e8d64b707ef15da0d13f060fe50c5f37b7305631e74. Neither is relabeled as recovered.

Return to Engineering-Anchor[2] before independent closure review. No review has been commissioned. Actual admission remains disabled.
