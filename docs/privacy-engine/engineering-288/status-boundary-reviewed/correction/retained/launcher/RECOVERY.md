# Recovery — new prospective component only

Verify the delivered archive's size and SHA-256 from the handoff, then CRC,
exact MANIFEST.json membership and every member's size/SHA-256. Extract to a NEW
persistent directory, never /tmp. Do not overlay an old launcher or session.
No script executes automatically. Original failures and inputs must be retained.

This package is self-contained for source inspection and focused test reproduction:
`python3 -I -B tests/checks.py --output /absolute/new/persistent/test-evidence`
The test command expects an assessment environment different from the pinned host;
it explicitly verifies refusal there and separately validates the captured host
observation. It creates isolated metadata/signature fixtures only, not sessions.
Do not use it as the exact-host compatibility command or rerun completed reviews.

For the exact host, after independent review, the bounded new-gate preflight is:

```
/home/steve/dev/Engineering-288-execution/I164-crypto5002-saved-compatibility-f8pegowh-environment/venv/bin/python -I -B code/lab_bootstrap.py check-environment
```

Run from this package's recovered directory. Preserve output in a new persistent
evidence directory. This command verifies the actual installed profile/records;
it does not initialize, reopen or access a session. A mismatch must stop; do not
edit the profile to match or rerun the environment setup to conceal it.

For future runtime recovery/use (NOT needed for this review and NOT authorized
as a session operation), exact unchanged inputs are required:
- current-candidate: 666 members, exact provenance/candidate-members.json.
- draft-connection: 163 members, exact provenance/draft-members.json.
- recovered runtime: 93 members, exact source-owned runtime-layout.json.
- prepared host environment and original interpreter: exact environment-profile.json.
The launcher retains the original `recover-runtime` interface and validates the
profile before copying. It does not substitute modules by filename.

Exact predecessor recovery artifact:
Engineering-288C-I164-BR01-filesystem-membership-correction(1).zip
15,341,542 bytes; SHA-256
1ca0a131a5b0e43799577388ad23752b53306f8067d92fe5b61ce366db777c3e.
Its inputs/predecessor.zip and RECOVERY.md retain bootstrap/runtime recovery and
failed-test provenance. This package includes unchanged old launcher/config and
manifests for comparison, but does not nest its entire evidence archive.

Candidate source retrieval artifact used here:
Engineering-Anchor2-I164-unknown-method-closure-review(1).zip
31,900,862 bytes; SHA-256
5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.
Chain: inputs/Engineering-Anchor2-I164-unknown-method-correction.zip ->
inputs/baseline-root.tar.xz. Only unchanged source bytes authenticated against
current manifests were selected; the old transport is not a substitute for the
complete corrected candidate composition.

Saved host compatibility report is included unchanged; its exact identities and
commands retain current adapter/consumer provenance. Preserve 55 independent
consumer controls separately from 28 supplied controls. No review rerun needed.

No initialization command is authorized by this package. In particular do not
point this launcher at I164-lab-session-001, rewrite its binding, or copy its
state into the new session label. Independent review precedes the narrow host
preflight and any separately authorized new-session work.
