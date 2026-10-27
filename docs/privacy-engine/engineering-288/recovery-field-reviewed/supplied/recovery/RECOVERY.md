# Offline recovery instructions

This checkpoint is self-contained for its new offline validation. Verify the outer ZIP identity supplied with it, safe unique regular member names, CRC and the flat MANIFEST.json hashes before extraction. Extract into a new persistent directory. Do not extract over an existing session or evidence root. Every predecessor member is included at retained/references/; exact original outer ZIPs named in DEPENDENCIES.json remain separate and are not reconstructed byte-for-byte by extraction.

On a trusted Python 3.12.14 process with optimization disabled and no bytecode writes, the bounded saved-evidence check is:

```
python3 -I -B tests/fresh_check.py "$PWD"
```

For independent review of the new controls only, use a fresh output directory outside the checkpoint:

```
python3 -I -B tests/controls.py --root "$PWD" --output /absolute/new/persistent/review-results
```

Do not use --write when the supplied receipt exists. The receipt is not silently repaired. tests/input_gates.py is only for an additional disposable extraction: it temporarily inserts/removes test entries in that extraction and restores exact predecessor bytes. Do not run it against an evidence master. The included gate run leaves Unix sockets and device entries untested, preserving the existing limitation.

The validation entries parse retained runtime and capture source as data; their audit/profile controls prohibit database/network operations and application/runtime calls. They never reopen a session. No host Python/Cryptography qualification follows from these offline checks. Do not run retained worker.py, a historical launcher, any prior controls or any lifecycle/pipeline as part of recovery.

The supplied recovered-root repetition used the separate pre-documentation recovery input recorded in results/recovery-input.json. Final packaging adds documentation, retained review provenance and result records; RESULTS.json explicitly verifies that all code, tests, receipt and predecessor dependency bytes are unchanged from that recovered input. Exact final archive integrity is checked separately, avoiding a self-referential archive identity claim.

Both completed Git saves remain complete: status fields at 2002804ea9b5755e7329720bce4895648587a881 and references at 6267f2c2017951a08d7210a98e1c386331c1c829. This task performs neither save again and makes no Git commit or push.
