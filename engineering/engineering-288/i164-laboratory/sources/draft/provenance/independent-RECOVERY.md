# Verified review checkpoint recovery

Use CPython 3.12.14 without optimization and the retained cryptography dependency. Verify the checkpoint's delivered byte count/SHA-256, CRC, exact safe membership and MANIFEST.json. `verify_checkpoint.py ARCHIVE.zip` verifies ZIP structure and member identities independently of supplied implementation code.

Extract into a fresh workspace directory named `so-review`. The checkpoint embeds both exact supplied archives. Full candidate recovery additionally requires these unchanged external review ZIPs:

- discriminator closure: 9,280,888 bytes; 50 entries; SHA-256 a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218.
- unknown-method closure: 31,900,862 bytes; 56 entries; SHA-256 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.

    python3 -B so-review/recover_checkpoint.py --closure /path/to/discriminator-review.zip --unknown /path/to/unknown-review.zip

It verifies/extracts sibling so-integration and so-supporting-review and invokes the original recovery into so-current/so-deps. It runs no tests, reviews, producers or lifecycle. The original scope-v2 ZIP container and earlier version-1 scope ZIP are not required: the exact scope member tree and manifest are embedded.

Unexpected files must reject. This review's original recovery stopped after the unknown-method predecessor was extracted, before the 17 discriminator overlays. `resume_recovery.py` records the exact continuation used: prove each extra is a unique exact pinned-member prefix; preserve it outside the root; verify all predecessor members; apply only the declared before/after overlay bytes; verify all current members. Use it only in a separately preserved recovery workspace at that precise stage, not blindly on another failure. Do not overwrite original logs. No validator or candidate implementation was edited.

Recover the three exact new partial files outside strict roots:

    python3 -B so-review/reconstruct_partials.py so-current /new/outside-partials

An additional partial found in the supporting-review extraction is stored directly as failures/preserved-author-review-partial.bin; results/final-input-extra.json identifies its original path and exact archive-member prefix. Keep it outside strict supplied-input roots.

The three candidate-root raw files were preserved during review; these pinned prefix records are lossless transport. Earlier partial and failure records remain preserved in unchanged predecessor artifacts. The protected-universe independent review remains 5,748,755 bytes / 34 entries / SHA-256 9637bc2081a0f1ce77238269290ab7b668a5ee1cb3029e951855d513f64ae959; it is a continuity/failure-history reference, not an additional runtime recovery dependency.

The actual mandatory command, if a new authorized run is needed, is:

    python3 -B so-integration/code/scope_integration.py --root so-current --output /new/source-only-result.json
    python3 -B so-integration/code/scope_integration.py --root so-current --result /new/source-only-result.json

Read REPORT.md and the separate results before considering any rerun. The independent scripts are audit evidence, not an instruction to repeat completed work. They expect sibling so-integration, so-current and, for cross-root alias checks, a separately verified unchanged root named pu-current. audit.py also compares the reused protected-universe artifacts in pu-input/pu-review; those comparisons can be satisfied from the unchanged preceding checkpoint without rerunning its review. Keep all newly generated results outside strict recovered roots and preserve this checkpoint's original logs.

No operational assurance, finite global capacity or admission is established. All eleven obligations remain open; no policy changed.
