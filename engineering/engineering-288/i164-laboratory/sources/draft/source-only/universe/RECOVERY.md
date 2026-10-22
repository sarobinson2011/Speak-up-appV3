# Exact recovery

Use CPython 3.12.14 without optimization and the existing cryptography dependency. Verify this ZIP against the delivered bytes/SHA-256, CRC, exact membership and MANIFEST.json with code/verify_archive.py. Two unchanged archives are required, with exact identities in provenance/recovery-archives.json:

- Engineering-Anchor2-I164-discriminator-type-closure-review.zip — 9,280,888 bytes, 50 entries, a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218.
- Engineering-Anchor2-I164-unknown-method-closure-review.zip — 31,900,862 bytes, 56 entries, 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.

Names may contain the download suffix (1); pass the actual paths. No other predecessor archive is required. The first embeds the exact discriminator correction, the second its preceding correction and baseline transport. They are referenced rather than nested again. Historical retry ZIP unavailability remains unchanged; no reconstruction of that original ZIP container is claimed.

From a clean extraction of this checkpoint:

    python3 -B code/recover.py --closure /path/to/discriminator-review.zip --unknown /path/to/unknown-review.zip --destination /new/current --dependencies /new/dependencies

Choose nonexistent destinations outside the checkpoint. Recovery verifies all archive manifests and every one of the 666 current candidate files; it runs no tests or producers. Extra files must reject. All historical candidate files and evidence stay byte-exact. The new code is a separate supporting companion, not a candidate overlay or canonical registration.

Reproduce this new bounded construction when needed:

    python3 -B code/universe.py /new/current /new/construction
    python3 -B code/checks.py /new/current /new/focused-results
    python3 -B code/recovered_checks.py /new/current /new/recovered-results.json

The first command invokes the existing cardinality/count-only/procedure machinery. The second uses the exact supplied outputs as expected current inputs; it does not regenerate the saved review projections or replay any lifecycle. The third is a separate-process current-input/result/readiness check. Generated directories must be outside both checkpoint and candidate roots. Do not substitute fixture counts into production unknowns or relabel old source coverage as current.

Read REPORT.md, DECISION-BRIEF.md, DEPENDENCIES.json, outputs/universe.json and outputs/consumption.json. Failures and superseded development outputs are separate from the completed focused and recovered controls. The output universe contains identities and source locations for every covered family/directory; retained projection provenance is in provenance/retained-projections.json. No large expansion or streams are needed to inspect or reproduce this slice.

Readiness/final binding blocked; backup kernel-only; streams UNCOMPUTED; actual admission disabled.

The unexpected partial workspace copies are losslessly represented by exact prefix references in provenance/failure-prefixes.json. Every prefix was byte-compared to its pinned predecessor member and hashed; original partial files remain separately preserved. To reconstruct the exact failure bytes outside the candidate:

    python3 -B code/recover_failure_bytes.py /new/current /new/failure-bytes

This is transport encoding of duplicate workspace artifacts, not a runtime retention/deletion amendment. The failed first delivery ZIP identity is recorded separately and is not claimed verified.
