# Recovery and validation

Verify this checkpoint's delivered byte count and SHA-256 before extraction.
`code/verify_checkpoint.py` verifies CRC, safe unique regular-file membership and
all manifest identities into a NEW persistent directory. Do not use `/tmp`.

Required unchanged inputs:

1. Engineering-288C-I164-evidence-count-receipts.zip: 3,789,194 bytes,
   SHA-256 d22b07f1d39bd45c4c306790ec83a40de1cf316e7ff57ad62ec2d9ee55a7ca32.
   The exact original is included under `inputs/`. Extract it separately with
   its own manifest checks; no source change or overlay is applied.
2. The exact current 666-member candidate and 163-member draft roots. Their
   manifests are included under `provenance/`. Reuse verified roots.
3. To recover unavailable roots, use the original draft recovery instructions:
   Engineering-288C-I164-source-only-model-ledger-inputs.zip, 13,820,246 bytes,
   SHA-256 f26d73237597ad2998735d6c71810f341b9bdbbf705497b0360f2ae59fbd6ec3;
   discriminator closure 9,280,888 bytes,
   SHA-256 a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218;
   unknown-method closure 31,900,862 bytes,
   SHA-256 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.
   Unexpected extraction partials are not admitted. Preserve them outside strict
   roots, authenticate all intended bytes and apply only the documented overlay.

The evidence-count independent review is retained separately:
Engineering-Anchor2-I164-evidence-count-independent-review.zip, 6,888,066 bytes,
59 entries, SHA-256 ed561b8a61672bd99f93ae6e35feab7a51d8fb7c9478d74332ea5d7f4638e2f5.
Its scoped report/summary are included as exact provenance, not rerun evidence.
The historical multi-gigabyte parent/base models are not needed for this finite
adapter: their builder interfaces are read from the pinned current source tree.
No historical model bytes are relabelled as current.

Run once with the compatible environment and exact roots (typically several
minutes per positive invocation; this is not a production runtime bound):

```sh
/home/steve/dev/Engineering-288-execution/I164-python31214-01qgue5t/venv/bin/python -I -B /ABS/checkpoint/code/finite_inputs.py validate --component /ABS/evidence-count-component --root /ABS/current-candidate --draft /ABS/draft-connection --bundle /ABS/checkpoint/outputs/bundle.json --output /ABS/NEW-PERSISTENT-VALIDATION
```

For an explicitly authorized fresh input-bundle construction use `build` and
omit `--bundle`. Inputs must remain unchanged; output must not exist. The command
records failure details in its new output directory. Preserve failures; do not
reset or reacquire the session. No request/database connection is needed.

`code/checks.py` supplies focused author mutation controls. Do not rerun them
merely to establish continuity. New independent review remains pending.

SOURCE-ONLY; readiness/final binding BLOCKED; backup KERNEL-ONLY; streams
UNCOMPUTED; admission DISABLED. Full native construction and ledger rebinding
remain separate, blocked steps.
