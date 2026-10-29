# Review checkpoint recovery

Verify the externally reported review ZIP identity, CRC, safe exact membership and all MANIFEST.json entries before consuming its contents. `code/verify_checkpoint.py` verifies the review archive and its exact embedded target without executing candidate or test code.

The exact reviewed construction is embedded as `input/I164-token-registration-correspondence-1.zip`. `code/integrity.py INPUT_ZIP NEW_EMPTY_ROOT` verifies its pinned identity, 2,178 safe entries and all 2,177 hashes, extracts a new root and checks exact files/directories. Use new persistent evidence directories outside any session. Preserve failed roots; do not overlay, repair or remove unexplained entries.

All bytes consumed by current offline validation are present. `retained/status` is the unchanged decoded IS-01 predecessor. `retained/closure-review` preserves its independent review except the redundant embedded predecessor ZIP. Historical compact manifests and omitted outer-archive qualifications remain as documented. The supplied intermediate recovery outer archive is not newly verified; its retained manifest selection and serialization were checked against the final target. Independent tests recovered the final archive itself.

The current receipt is `results/primary/token-registration-correspondence.json` inside the target. Actual current CLI validation was exercised once in a new process and recovered root, recorded under `fresh-cli`. Fresh controls, supplied Engineering controls, previous independent results and failures remain separately attributed. Completed campaigns are evidence to inspect, not instructions to rerun.

`code/oracle.py` is a reviewer AST/prefix oracle. It does not execute `_run` or any application method. `code/recover_script.py` is infrastructure for explicitly authorized new focused checks; it verifies a new root before loading a selected reviewer script. No new test or host command is required to receive this checkpoint.

The initial 11-check source-fragment parser failure and later zero-control diff-audit failure are preserved under `failures/` and excluded from completed totals. Prior IS-01 and older failures remain unchanged inside the target. All seven recovered layouts were verified unchanged after testing.

Environment: CPython 3.12.14, isolated mode, no bytecode writes, optimization disabled; Cryptography 50.0.2. No request, acquisition, database connection, session initialization/reopening, runtime change or policy adoption is needed or authorized by recovery. Runtime registration/revocation observations remain unavailable; observer unjoined; all obligations, UNKNOWN totals and authority boundaries persist; admission disabled.
