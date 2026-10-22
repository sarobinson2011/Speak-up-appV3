# Recovery and inspection

Verify delivered ZIP size/SHA-256, CRC, exact membership and MANIFEST.json after fresh extraction. Read REPORT.md and UNRESOLVED.md, then code/static_declarations.py, static_ingest.py and reconcile_baseline.py. No candidate execution is needed to inspect declarations/static.json, checklist-links.json or results.

The original adapters and runtime references are unchanged. New modules are listed in changed-identities.json. Reference source hashes are pinned by reference/hashes.json; the added historical catalog has separately recorded archive provenance. Declarations are supporting templates with provisional selectors, never allocated canonical class identities.

For optional focused reproduction, use a disposable extracted copy and preserve its saved results first:

    mv results results-saved
    mkdir results
    python -B code/check_static.py
    python -B code/check_reconciliation_semantics.py
    python -B code/check_checklist.py

Python 3 and cryptography are required for the retained authenticated parser path. No package installation, network access, candidate scheduler/signing or lifecycle is needed. The tests recreate a fixture-only baseline and two-delta chain. They never update canonical inputs. Old legacy check scripts are retained source, not instructions to rerun prior suites.

Normal supporting entry point:

    python -B code/static_ingest.py fixtures/minimal-response.json declarations/static.json /tmp/i164-static-new.json

Output must not already exist. Reconciliation entry point:

    python -B code/reconcile_baseline.py INPUT_DIRECTORY PIN_FILE EXACT_EXTERNALLY_VERIFIED_PIN_SHA256

Do not use fixture-pin.json as real authority. Native canonical inputs require exact source-preserving mapping and externally established completeness. The result is correspondence, never a grant of canonical registration or actual admission.

Preserve unchanged predecessors separately; none are nested:

- Engineering-288C-I164-response-envelope-correction.zip: 3,213,216 bytes, 139 entries; 8217415cbe9b296485f7abc1af00badc49bf960d346c725c7d1a2bc9f54545f1.
- Formal-Lab-Engineering-288C-I164-response-envelope-review.zip: 15,408,085 bytes, 167 entries; 5645172da4137408d05d103ecbcf1070f5b81854e949d0bbfb78347d9766b629.
- Engineering-288C-I164-option-a-correspondence.zip: 6,781,314 bytes, 54 entries; 8b6cc960a73c20271242529a607e6dd31a45ed7cf2e6592609e1364b46e742a0.

The original retry ZIP remains unavailable: 54,899,989 bytes / 1f06a4034fab8ab7e0c17ea409ea15d113c9106f63bbfad96291fcb1368e5f09. Recovery-package provenance and prior adoption records remain preserved; no archive is relabeled as that original.

Return to Engineering-Anchor[2] before focused independent review. Actual admission remains disabled; changed stream identities UNCOMPUTED.
