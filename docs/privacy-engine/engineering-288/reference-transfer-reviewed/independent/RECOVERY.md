Formal-Lab[6] reference-transfer independent-review checkpoint

Verify the communicated review ZIP identity, CRC, safe unique regular membership and every MANIFEST.json member hash before extraction into a new persistent directory. The exact review target is included as input/I164-reference-transfer-correspondence-1.zip.

Target: 38,786,604 bytes, 552 entries, SHA-256 36e4dfd8199df3a9168e47416d1e2508a8868876170c3586734c5a714adadac9.

code/verify_input.py verifies the target identity, exact membership, manifest hashes and nested archives. Its --extract option creates a new root and refuses an existing destination. Preserve the complete directory structure. Do not overlay previous milestones or open embedded database files.

The target includes all 489 decoded predecessor field members and its full offline dependencies. The original field input ZIP and original independent field-review ZIP were separately verified and reused during this review. Their copied manifest scopes remain unchanged: the non-input review copy is partial, and no reconstructed original ZIP identity is claimed. The current executable consumer does not need those external outer ZIPs. code/composition.py takes the new root, result path, exact prior field-input ZIP and exact prior independent-review ZIP, in that order, for reproducing the byte-continuity audit only.

The bounded new offline command is:

```bash
python3 -I -B /absolute/new-root/code/correspondence.py \
  check /absolute/new-root/results/reference-correspondence.json
```

Use CPython 3.12.14 with optimization disabled. The command consumes source and saved evidence. It is not a session launcher, acquisition, host smoke or completed pipeline. Do not run historical suites, the old managed_coverage CLI, runtime/application entries, a lifecycle or any write mode as a recovery step.

code/source_oracle.py and code/case_matrix.py are reviewer-owned source/constructed expectations. code/independent_controls.py contains fresh bounded controls. Its primary and recovered results are separate from the supplied 182/182 controls. code/input_controls.py operates only on a new persistent fixture; code/fresh_command.py records the actual new command in a separate guarded process. Failed reviewer development attempts are preserved under failures/ and are not passing test counts.

The review does not establish actual reference transfer or connection identities. Both symbolic contexts remain distinct views, not extra executions. All UNKNOWN totals, obligations, retention, allowances and qualification/admission boundaries remain in force. Read REPORT.md and CHECKPOINT.json for the scoped verdict and precise limits.
