# Exact recovery and command

Verify this checkpoint's archive identity, CRC, exact membership and MANIFEST.json. The scope/ and universe/ trees are unchanged exact extractions of:

- Engineering-288C-I164-protected-scope-source-only-v2.zip: 3,998,361 bytes, 32 entries, SHA-256 268763d4b51488a1c976314ee870fedb415cd347e762a5d24f43c5422c41a3a5.
- Engineering-288C-I164-protected-production-universe-verified.zip: 2,900,168 bytes, 46 entries, SHA-256 ee38c692edbbed742c5e90eb8f9b898111bddd410daba23427efdceaf55da3d4.

The current candidate is the exact unchanged 666-file root. Reuse a verified root. If unavailable, recover it using universe/code/recover.py with the two unchanged external review archives:

- discriminator closure: 9,280,888 bytes / 50 entries / a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218;
- unknown-method closure: 31,900,862 bytes / 56 entries / 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.

Use its exact existing recovery instructions and preserve unexpected partials outside strict roots; do not weaken membership. Other review and version-1 scope archives are provenance, not additional runtime inputs. Their verified identities are in results/dependencies.json. Historical original retry ZIP remains unavailable.

With CPython 3.12.14 and the retained dependencies, from this checkpoint root:

    python3 -B code/scope_integration.py --root /exact/current --output /new/source-only-result.json
    python3 -B code/scope_integration.py --root /exact/current --result /new/source-only-result.json

Output must not already exist and must be outside scope/, universe/ and the candidate. The first command is the one runnable path; the second validates the entire current result. Both invoke existing small saved-evidence validators and count-only/duty paths, not runtime producers. Full expansion is never invoked.

Focused test commands (only if separately needed for review):

    python3 -B code/checks.py /exact/current /new/mutations.json
    python3 -B code/disk_checks.py /new/disk-results.json /new/disk-input-fixture

Do not modify the exact scope/universe trees, including their preserved prior result and failure records. Future versions need explicit new authority/input identities and review; supplied replacement pins are not accepted. Existing historical validation outputs do not satisfy the new result format.

To exercise the result-envelope mutation controls against a saved result:

    python3 -B code/result_checks.py /exact/current /saved/result.json /new/result-mutations.json

An optional fourth file argument compares a separately generated recovered-root result and checks both contexts. The full CLI --result path regenerates and compares the complete current result; no acceptance cache is used.
