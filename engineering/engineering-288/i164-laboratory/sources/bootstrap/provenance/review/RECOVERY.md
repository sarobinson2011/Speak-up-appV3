# Review checkpoint recovery

Verify the external review ZIP identity, CRC, safe exact membership and every MANIFEST.json entry before extracting. `code/verify_checkpoint.py` performs the independent ZIP checks. The review contains the unchanged submitted bootstrap archive and the exact reviewed draft dependency under inputs/.

| Input | Bytes | Entries | SHA-256 |
| --- | ---: | ---: | --- |
| inputs/bootstrap.zip | 12,197,057 | 416 | 8081d716e9bf20cc527092e383e534285c84358a686118a9843bc047b88cf3b8 |
| inputs/draft.zip | 13,820,246 | 56 | f26d73237597ad2998735d6c71810f341b9bdbbf705497b0360f2ae59fbd6ec3 |

Extract the draft ZIP to a fresh directory and run only its `recover.py` to materialize its exact embedded SOURCE-ONLY integration. The declared recovered composition has 163 files. The supplied bootstrap's 164-file draft pin is the BR-01 defect; do not fabricate its extra partial as a recovery step.

Reuse an exact previously verified 666-member candidate. If unavailable, the draft's documented candidate recovery requires these unchanged external archives:

- Discriminator closure review: 9,280,888 bytes / 50 entries / a5a928a1d45e792059c70bc727a58fd4186865518fe158b9055fe4cdf861b218.
- Unknown-method closure review: 31,900,862 bytes / 56 entries / 5c4f1f9960493de9c3c0ec8c80fda2da0b75b5fb70c079149f422f3d737c3aff.

This review ZIP is not a self-contained recovery of the entire candidate. The unavailable original retry ZIP remains unavailable. No historical review or lifecycle needs to be rerun. Check the 666-member manifest and exact directories; preserve undeclared material outside strict roots.

The review's `code/prepare.py` is a test-isolation record, not an operational installer: it constructs the explicitly synthetic as-pinned fixture to distinguish BR-01 from the mechanics being tested. Scripts retain workspace-relative names (`br-input`, `br-current`, `br-draft`, `br-as-pinned-draft`, `br-runtime`). The raw first-attempt failure is preserved; its later clean-root witness is in results/BR-01.json. Do not run completed controls merely for continuity.

Raw supplied failure evidence is inside inputs/bootstrap.zip. Fresh temporary test databases and failure markers are under temporary-state/. Recorded symlink metadata permits lossless fixture reconstruction without unsafe ZIP symlink entries. The raw prefix files under failures/ are preserved evidence only, not declared candidate dependencies.

The Ubuntu diagnostic command and exact bounds are in REPORT.md and UBUNTU-VERIFY.sh. It uses temporary state only, enforces the public environment, preserves failure evidence, and does not fix either finding or authorize a persistent session. The required prepared host records remain unreconciled.

Return BR-01 and BR-02 to Engineering-Anchor[2]. Readiness/final binding remain blocked; SOURCE-ONLY unchanged; streams UNCOMPUTED; admission disabled.
