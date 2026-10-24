# Recovery

Verify delivered ZIP bytes/SHA, CRC, exact MANIFEST.json membership and all member
identities; extract into a NEW persistent directory, never /tmp. outputs/ledger.json
is the actual constructed artifact. No session/database/builder executes on recovery.

Required unchanged dependencies:
- Engineering-288C-I164-finite-native-inputs.zip: 45,747,644 bytes, 60 entries,
  SHA-256 94791c65c3502d85fc452c0e9c100391f5d0199f7690462e92b91c1a600caa8b.
- Engineering-288C-I164-finite-native-consumer-verified.zip: 6,636,286 bytes, 40 entries,
  SHA-256 cb88382f2e16ee9fbd44a30f05033ef12c6e467b838784fa25fa16b88bc5e5f5.
  Recover its exact outputs/native.json; do not rerun construction to replace it.
  Native bytes: 35,955,155; SHA-256
  1401d5797186b99790ffc6d868cadab62f358bdc1aea0a3946469eab636337ed.
- Review provenance: I164-finite-output-verifier-independent-review.zip,
  14,095,640 bytes, 56 entries, SHA-256
  99bc661eb6de2c9af36253c5b39344e7a2a21d4b1aa4d3d0c59891479080df51.
  Exact relevant texts included; unchanged reviewed verifier checkpoint included
  at provenance/reviewed-verifier-checkpoint.zip (96,006 bytes, SHA-256
  34f425f044337d14ca0abf6eb5469e69826f9ba4332035a5ec05603e67b52310).

Validate this saved ledger, from the recovered checkpoint directory:
python3 -I -B code/ledger.py --component /ABS/finite-native-inputs.zip --consumer /ABS/finite-native-consumer-verified.zip --model /ABS/native.json --submitted outputs/ledger.json --output /ABS/NEW-PERSISTENT-VALIDATION

For fresh construction of this same finite scope, omit --submitted. Both modes
revalidate the actual representation and preserve failure.txt on rejection.
Standard library only, tested CPython 3.12.14. No prepared-host compatibility
result is claimed for this new ledger component. Allow roughly 10–30 seconds
per public run depending on I/O; no automatic retry.

Focused new tests: code/checks.py with --component, --consumer, --model,
--ledger outputs/ledger.json, --output /ABS/NEW-PERSISTENT-CONTROLS.
Do not rerun predecessor reviews/lifecycles. Original failure and partial-delivery
evidence remains in exact predecessor archives. Preserve this output and any
failed-run directories; never overwrite a failed or completed output directory.
