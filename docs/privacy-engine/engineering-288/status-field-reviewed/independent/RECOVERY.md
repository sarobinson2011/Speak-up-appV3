Formal-Lab[6] status-field independent-review checkpoint

Verify this review ZIP's communicated identity, CRC, safe unique regular membership and MANIFEST.json before extracting into a new persistent directory. The manifest binds every other review member. The exact target archive is included as input/I164-status-field-correspondence-1.zip, together with its complete embedded recovery chain.

Target identity: 38,539,130 bytes, 489 entries, SHA-256 b51b313de9d03d3bc5eb8436d18e219b05f173144be46d51f090d5119b244504.

code/verify_input.py verifies the exact target, member identities and nested archive/manifests; --extract creates a new root and refuses an existing destination. code/source_oracle.py is the reviewer-owned AST traversal and does not use either supplied guard extractor. code/composition.py records recovery equivalence and intentional changes; its provenance audit in this review read only two guard members from the already verified historical candidate archive, supplied as its third argument. That historical full candidate is not needed to run the delivered offline consumer, because both exact guard modules are included in the target. code/resolve_manifest_copies.py records where the exact bytes referenced by three partial historical review-manifest omissions remain available in the embedded archive chain.

On CPython 3.12.14 with optimization disabled, the bounded read-only command at a newly recovered target root is:

```bash
python3 -I -B /absolute/target/code/correspondence.py \
  check /absolute/target/results/status-field-correspondence.json
```

This is the new offline correspondence command. Do not run the historical managed_coverage CLI, worker, runtime/session entries, host smoke, old supplied/independent suites, completed pipeline or lifecycle as a recovery step. No dependency installation, existing session access or database connection is needed. SQLite content in embedded evidence stays closed file bytes.

independent-primary/ holds 147 new assertions; independent-recovered/ holds 24 focused assertions in a separate process against a second complete extraction. cli-recovered/ holds the actual offline command output, empty stderr and exit status. Constructed expression checks and altered-evidence controls are labelled separately and are not producer executions. The author's 156 controls and repetition remain supplied evidence within the target; they were not rerun.

The original SOC-closed 467-file tree, adapter, receipt, sources and evidence are unchanged. Do not reinterpret static origins as observed assignments, full runtime/repetition coverage or qualification. All obligations, UNKNOWN totals and admission/readiness boundaries remain in force.
